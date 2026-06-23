"""
Prediction engine for AI vs Human text detection.

Loads trained model and provides predictions with confidence scores,
AI indicators, and feature importances.
"""
import os
import joblib
import numpy as np
from scipy.sparse import hstack, csr_matrix

from app.ml.features import (
    extract_features,
    extract_feature_vector,
    FEATURE_NAMES,
)
from app.ml.train import MODEL_PATH, TFIDF_PATH, SCALER_PATH, is_trained

# Cached model artifacts
_model = None
_tfidf = None
_scaler = None


def load_model():
    """Load trained model artifacts into memory."""
    global _model, _tfidf, _scaler

    if not is_trained():
        raise RuntimeError("No trained model found. Please train the model first.")

    _model = joblib.load(MODEL_PATH)
    _tfidf = joblib.load(TFIDF_PATH)
    _scaler = joblib.load(SCALER_PATH)

    print("Model loaded successfully.")


def reload_model():
    """Force reload of model artifacts (after retraining)."""
    global _model, _tfidf, _scaler
    _model = None
    _tfidf = None
    _scaler = None
    load_model()


def _ensure_loaded():
    """Ensure model is loaded."""
    if _model is None:
        load_model()


def predict(text: str) -> dict:
    """
    Predict whether text is AI-generated or Human-written.

    Returns a dict with:
    - prediction: "AI Generated" or "Human Written"
    - ai_probability: float (0-1)
    - human_probability: float (0-1)
    - statistics: word count, sentence count, etc.
    - indicators: AI-detection indicators
    - feature_importances: importance of each feature
    """
    _ensure_loaded()

    # Extract features
    features = extract_features(text)
    feature_vector = extract_feature_vector(text)

    # Prepare for model
    tfidf_vec = _tfidf.transform([text])
    custom_scaled = _scaler.transform([feature_vector])
    combined = hstack([tfidf_vec, csr_matrix(custom_scaled)])

    # Predict
    proba = _model.predict_proba(combined)[0]
    prediction_idx = np.argmax(proba)

    ai_prob = float(proba[1])
    human_prob = float(proba[0])
    prediction = "AI Generated" if prediction_idx == 1 else "Human Written"

    # Statistics
    statistics = {
        "total_words": features["word_count"],
        "total_sentences": features["sentence_count"],
        "avg_sentence_length": features["avg_sentence_length"],
        "vocabulary_richness": features["vocabulary_richness"],
    }

    # AI Indicators
    indicators = _compute_indicators(features)

    # Feature importances (from the custom features)
    importances = _compute_feature_importances(feature_vector)

    return {
        "prediction": prediction,
        "ai_probability": round(ai_prob, 4),
        "human_probability": round(human_prob, 4),
        "statistics": statistics,
        "indicators": indicators,
        "feature_importances": importances,
    }


def _compute_indicators(features: dict) -> list:
    """Compute AI detection indicators from linguistic features."""
    indicators = []

    # Repetitive Patterns
    rep_score = features["repetition_score"]
    rep_level = "High" if rep_score > 0.15 else ("Medium" if rep_score > 0.05 else "Low")
    indicators.append({
        "name": "Repetitive Patterns",
        "value": rep_level,
        "score": round(rep_score, 4)
    })

    # Sentence Uniformity
    uni_score = features["sentence_uniformity"]
    uni_level = "High" if uni_score > 0.6 else ("Medium" if uni_score > 0.3 else "Low")
    indicators.append({
        "name": "Sentence Uniformity",
        "value": uni_level,
        "score": round(uni_score, 4)
    })

    # Lexical Diversity (inverted: low diversity = more AI-like)
    lex_score = features["lexical_diversity"]
    lex_level = "Low" if lex_score < 0.4 else ("Medium" if lex_score < 0.6 else "High")
    indicators.append({
        "name": "Lexical Diversity",
        "value": lex_level,
        "score": round(lex_score, 4)
    })

    # Predictability
    pred_score = features["predictability_score"]
    pred_level = "High" if pred_score > 0.5 else ("Medium" if pred_score > 0.3 else "Low")
    indicators.append({
        "name": "Predictability Score",
        "value": pred_level,
        "score": round(pred_score, 4)
    })

    return indicators


def _compute_feature_importances(feature_vector: list) -> list:
    """
    Compute feature importance scores.
    Uses model coefficients if available (LR), otherwise uses feature magnitudes.
    """
    importances = []

    # Try to get model-specific importances
    try:
        if hasattr(_model, 'coef_'):
            # Logistic Regression / SVM: use last N coefficients (custom features)
            coefs = np.abs(_model.coef_[0][-len(FEATURE_NAMES):])
            total = coefs.sum() if coefs.sum() > 0 else 1
            for name, coef in zip(FEATURE_NAMES, coefs):
                importances.append({
                    "name": name,
                    "score": round(float(coef / total), 4)
                })
        elif hasattr(_model, 'feature_importances_'):
            # Random Forest: use last N importances
            fi = _model.feature_importances_[-len(FEATURE_NAMES):]
            total = fi.sum() if fi.sum() > 0 else 1
            for name, imp in zip(FEATURE_NAMES, fi):
                importances.append({
                    "name": name,
                    "score": round(float(imp / total), 4)
                })
        else:
            raise AttributeError("No importance method available")
    except (AttributeError, IndexError):
        # Fallback: use feature magnitudes
        total = sum(abs(v) for v in feature_vector) or 1
        for name, val in zip(FEATURE_NAMES, feature_vector):
            importances.append({
                "name": name,
                "score": round(abs(val) / total, 4)
            })

    # Sort by importance descending
    importances.sort(key=lambda x: x["score"], reverse=True)
    return importances
