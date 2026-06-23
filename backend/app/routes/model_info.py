"""
Model Info API endpoint.
GET /api/model-info - Return model metadata, algorithms, and metrics.
"""
from fastapi import APIRouter
from app.models import ModelInfoResponse, AlgorithmInfo, DatasetInfo, ModelMetrics
from app.ml.train import get_metrics, is_trained

router = APIRouter(prefix="/api", tags=["model-info"])

ALGORITHM_DESCRIPTIONS = {
    "Logistic Regression": (
        "A linear model that estimates the probability of a binary outcome "
        "using a logistic function. Effective for text classification with "
        "TF-IDF features due to its interpretability and efficiency."
    ),
    "Random Forest": (
        "An ensemble learning method that constructs multiple decision trees "
        "during training and outputs the class that is the mode of the individual "
        "trees. Handles non-linear relationships and feature interactions well."
    ),
    "SVM": (
        "Support Vector Machine finds the optimal hyperplane that maximally "
        "separates the two classes in high-dimensional feature space. "
        "Particularly effective for text classification with kernel tricks."
    ),
}


@router.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """Return information about the trained model, dataset, and metrics."""
    metrics_data = get_metrics()

    if not metrics_data:
        # Return defaults if no model trained yet
        return ModelInfoResponse(
            algorithms=[
                AlgorithmInfo(
                    name=name, description=desc, is_active=False
                ) for name, desc in ALGORITHM_DESCRIPTIONS.items()
            ],
            dataset=DatasetInfo(
                total_samples=0, ai_samples=0, human_samples=0,
                train_size=0, test_size=0
            ),
            metrics=ModelMetrics(
                accuracy=0, precision=0, recall=0,
                f1_score=0, train_accuracy=0, test_accuracy=0
            ),
            active_algorithm="None",
        )

    best = metrics_data.get("best_model", "")
    best_metrics = metrics_data.get("best_metrics", {})
    dataset = metrics_data.get("dataset", {})

    algorithms = []
    for name, desc in ALGORITHM_DESCRIPTIONS.items():
        algorithms.append(AlgorithmInfo(
            name=name,
            description=desc,
            is_active=(name == best),
        ))

    return ModelInfoResponse(
        algorithms=algorithms,
        dataset=DatasetInfo(
            total_samples=dataset.get("total_samples", 0),
            ai_samples=dataset.get("ai_samples", 0),
            human_samples=dataset.get("human_samples", 0),
            train_size=dataset.get("train_size", 0),
            test_size=dataset.get("test_size", 0),
        ),
        metrics=ModelMetrics(
            accuracy=best_metrics.get("test_accuracy", 0),
            precision=best_metrics.get("precision", 0),
            recall=best_metrics.get("recall", 0),
            f1_score=best_metrics.get("f1_score", 0),
            train_accuracy=best_metrics.get("train_accuracy", 0),
            test_accuracy=best_metrics.get("test_accuracy", 0),
        ),
        active_algorithm=best,
    )
