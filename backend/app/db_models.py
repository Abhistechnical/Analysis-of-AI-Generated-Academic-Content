"""
SQLAlchemy ORM models for prediction history and training runs.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base


class Prediction(Base):
    """Stores each prediction made by the system."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text_snippet = Column(String(200), nullable=False)
    full_text = Column(Text, nullable=False)
    prediction = Column(String(20), nullable=False)  # "AI Generated" or "Human Written"
    ai_probability = Column(Float, nullable=False)
    human_probability = Column(Float, nullable=False)
    word_count = Column(Integer, nullable=False)
    sentence_count = Column(Integer, nullable=False)
    avg_sentence_length = Column(Float, nullable=False)
    vocabulary_richness = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class TrainingRun(Base):
    """Stores metadata for each model training run."""
    __tablename__ = "training_runs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    algorithm = Column(String(50), nullable=False)
    num_samples = Column(Integer, nullable=False)
    train_accuracy = Column(Float, nullable=False)
    test_accuracy = Column(Float, nullable=False)
    precision_score = Column(Float, nullable=False)
    recall_score = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    is_active = Column(Integer, default=1)  # 1 = currently active model
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
