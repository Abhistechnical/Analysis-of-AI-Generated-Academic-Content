"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ─── Analysis ───────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Academic text to analyze")


class ContentStatistics(BaseModel):
    total_words: int
    total_sentences: int
    avg_sentence_length: float
    vocabulary_richness: float


class AIIndicator(BaseModel):
    name: str
    value: str        # "High", "Medium", "Low"
    score: float      # 0.0 - 1.0


class FeatureImportance(BaseModel):
    name: str
    score: float


class AnalyzeResponse(BaseModel):
    prediction: str                          # "AI Generated" or "Human Written"
    ai_probability: float
    human_probability: float
    statistics: ContentStatistics
    indicators: List[AIIndicator]
    feature_importances: List[FeatureImportance]


# ─── Model Info ─────────────────────────────────────────────
class AlgorithmInfo(BaseModel):
    name: str
    description: str
    is_active: bool


class DatasetInfo(BaseModel):
    total_samples: int
    ai_samples: int
    human_samples: int
    train_size: int
    test_size: int


class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    train_accuracy: float
    test_accuracy: float


class ModelInfoResponse(BaseModel):
    algorithms: List[AlgorithmInfo]
    dataset: DatasetInfo
    metrics: ModelMetrics
    active_algorithm: str


# ─── Admin / History ────────────────────────────────────────
class PredictionRecord(BaseModel):
    id: int
    text_snippet: str
    prediction: str
    ai_probability: float
    human_probability: float
    word_count: int
    sentence_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    total: int
    page: int
    per_page: int
    predictions: List[PredictionRecord]


class RetrainResponse(BaseModel):
    status: str
    message: str
    metrics: Optional[ModelMetrics] = None
