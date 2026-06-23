"""
Admin API endpoints.
POST /api/admin/upload-dataset - Upload a new training CSV
POST /api/admin/retrain       - Retrain the ML model
GET  /api/admin/history        - Get prediction history
GET  /api/admin/export         - Export history as CSV
"""
import io
import csv
import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.db_models import Prediction, TrainingRun
from app.models import (
    HistoryResponse, PredictionRecord, RetrainResponse, ModelMetrics
)
from app.ml.train import train_models, get_metrics, DATA_DIR, DATASET_PATH
from app.ml.predict import reload_model

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload a new CSV dataset for training."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    try:
        contents = await file.read()
        decoded = contents.decode("utf-8")

        # Validate CSV has required columns
        reader = csv.DictReader(io.StringIO(decoded))
        fieldnames = reader.fieldnames or []

        if "text" not in fieldnames or "label" not in fieldnames:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'text' and 'label' columns."
            )

        # Count rows
        rows = list(reader)
        if len(rows) < 10:
            raise HTTPException(
                status_code=400,
                detail="Dataset must contain at least 10 samples."
            )

        # Save to data directory
        os.makedirs(DATA_DIR, exist_ok=True)
        upload_path = DATASET_PATH
        with open(upload_path, "w", newline="", encoding="utf-8") as f:
            f.write(decoded)

        return {
            "status": "success",
            "message": f"Dataset uploaded: {len(rows)} samples",
            "filename": file.filename,
            "samples": len(rows),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/retrain", response_model=RetrainResponse)
async def retrain_model(db: Session = Depends(get_db)):
    """Retrain the ML model with the current dataset."""
    try:
        metrics = train_models()

        # Reload model in memory
        reload_model()

        best = metrics.get("best_metrics", {})

        # Save training run to DB
        run = TrainingRun(
            algorithm=metrics.get("best_model", "Unknown"),
            num_samples=metrics.get("dataset", {}).get("total_samples", 0),
            train_accuracy=best.get("train_accuracy", 0),
            test_accuracy=best.get("test_accuracy", 0),
            precision_score=best.get("precision", 0),
            recall_score=best.get("recall", 0),
            f1_score=best.get("f1_score", 0),
        )
        db.add(run)
        db.commit()

        return RetrainResponse(
            status="success",
            message=f"Model retrained successfully. Best: {metrics.get('best_model', 'N/A')}",
            metrics=ModelMetrics(
                accuracy=best.get("test_accuracy", 0),
                precision=best.get("precision", 0),
                recall=best.get("recall", 0),
                f1_score=best.get("f1_score", 0),
                train_accuracy=best.get("train_accuracy", 0),
                test_accuracy=best.get("test_accuracy", 0),
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")


@router.get("/history", response_model=HistoryResponse)
async def get_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Get paginated prediction history."""
    total = db.query(func.count(Prediction.id)).scalar()
    offset = (page - 1) * per_page

    predictions = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    return HistoryResponse(
        total=total,
        page=page,
        per_page=per_page,
        predictions=[
            PredictionRecord(
                id=p.id,
                text_snippet=p.text_snippet,
                prediction=p.prediction,
                ai_probability=p.ai_probability,
                human_probability=p.human_probability,
                word_count=p.word_count,
                sentence_count=p.sentence_count,
                created_at=p.created_at,
            )
            for p in predictions
        ],
    )


@router.get("/export")
async def export_history(db: Session = Depends(get_db)):
    """Export all prediction history as CSV."""
    predictions = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Text Snippet", "Prediction", "AI Probability",
        "Human Probability", "Words", "Sentences", "Date"
    ])

    for p in predictions:
        writer.writerow([
            p.id, p.text_snippet, p.prediction,
            f"{p.ai_probability:.4f}", f"{p.human_probability:.4f}",
            p.word_count, p.sentence_count,
            p.created_at.isoformat() if p.created_at else "",
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=prediction_history.csv"},
    )
