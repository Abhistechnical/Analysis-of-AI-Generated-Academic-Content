"""
Model training pipeline.

Trains Logistic Regression, Random Forest, and SVM classifiers
using TF-IDF + linguistic features. Selects the best performing model.
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score
)
from scipy.sparse import hstack, csr_matrix

from app.ml.features import extract_feature_vector
from app.ml.dataset import generate_dataset

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATASET_PATH = os.path.join(DATA_DIR, "dataset.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
TFIDF_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "feature_scaler.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")


def ensure_dataset():
    """Generate dataset if it doesn't exist."""
    if not os.path.exists(DATASET_PATH):
        print("Generating synthetic dataset...")
        generate_dataset(DATASET_PATH, num_samples=1000)
    return DATASET_PATH


def prepare_features(texts: list, tfidf: TfidfVectorizer = None,
                     scaler: StandardScaler = None, fit: bool = False):
    """
    Prepare combined feature matrix from texts.

    Combines TF-IDF features with custom linguistic features.
    """
    # Extract custom features
    custom_features = np.array([extract_feature_vector(t) for t in texts])

    if fit:
        # Fit and transform
        if tfidf is None:
            tfidf = TfidfVectorizer(
                max_features=500,
                ngram_range=(1, 2),
                stop_words="english",
                min_df=2,
                max_df=0.95
            )
        tfidf_matrix = tfidf.fit_transform(texts)

        if scaler is None:
            scaler = StandardScaler()
        custom_scaled = scaler.fit_transform(custom_features)
    else:
        tfidf_matrix = tfidf.transform(texts)
        custom_scaled = scaler.transform(custom_features)

    # Combine: TF-IDF (sparse) + custom features (dense → sparse)
    combined = hstack([tfidf_matrix, csr_matrix(custom_scaled)])

    return combined, tfidf, scaler


def train_models(dataset_path: str = None) -> dict:
    """
    Train all models and save the best one.

    Returns dict with metrics for all models and the selected best.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Load dataset
    path = dataset_path or ensure_dataset()
    df = pd.read_csv(path)
    texts = df["text"].tolist()
    labels = df["label"].values

    print(f"Loaded dataset: {len(texts)} samples")

    # Train/test split
    X_texts_train, X_texts_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # Prepare features
    X_train, tfidf, scaler = prepare_features(X_texts_train, fit=True)
    X_test, _, _ = prepare_features(X_texts_test, tfidf=tfidf, scaler=scaler)

    # Define classifiers
    classifiers = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, random_state=42, C=1.0
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=42, max_depth=20
        ),
        "SVM": SVC(
            kernel="rbf", probability=True, random_state=42, C=1.0
        ),
    }

    results = {}
    best_model = None
    best_f1 = -1
    best_name = ""

    for name, clf in classifiers.items():
        print(f"\nTraining {name}...")
        clf.fit(X_train, y_train)

        # Evaluate
        y_pred_train = clf.predict(X_train)
        y_pred_test = clf.predict(X_test)

        train_acc = accuracy_score(y_train, y_pred_train)
        test_acc = accuracy_score(y_test, y_pred_test)
        prec = precision_score(y_test, y_pred_test, zero_division=0)
        rec = recall_score(y_test, y_pred_test, zero_division=0)
        f1 = f1_score(y_test, y_pred_test, zero_division=0)

        results[name] = {
            "train_accuracy": round(train_acc, 4),
            "test_accuracy": round(test_acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
        }

        print(f"  Train Acc: {train_acc:.4f} | Test Acc: {test_acc:.4f} | F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model = clf
            best_name = name

    print(f"\nBest model: {best_name} (F1={best_f1:.4f})")

    # Save artifacts
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(tfidf, TFIDF_PATH)
    joblib.dump(scaler, SCALER_PATH)

    # Save metrics
    all_metrics = {
        "best_model": best_name,
        "models": results,
        "dataset": {
            "total_samples": len(texts),
            "ai_samples": int(sum(labels)),
            "human_samples": int(len(labels) - sum(labels)),
            "train_size": len(y_train),
            "test_size": len(y_test),
        },
        "best_metrics": results[best_name],
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(all_metrics, f, indent=2)

    print(f"Models and metrics saved to {MODEL_DIR}")
    return all_metrics


def is_trained() -> bool:
    """Check if a trained model exists."""
    return all(os.path.exists(p) for p in [MODEL_PATH, TFIDF_PATH, SCALER_PATH, METRICS_PATH])


def get_metrics() -> dict:
    """Load saved metrics."""
    if not os.path.exists(METRICS_PATH):
        return {}
    with open(METRICS_PATH, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    train_models()
