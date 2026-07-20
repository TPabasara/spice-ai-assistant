from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PerformanceSummary(BaseModel):
    total_conversations: int
    total_tokens_consumed: int
    average_latency_ms: float
    average_similarity_score: float

class EvaluationLogEntry(BaseModel):
    id: int
    session_id: int
    sender: str
    content: str
    prompt_used: Optional[str]
    tokens_used: Optional[int]
    latency_ms: Optional[float]
    similarity_score: Optional[float]
    timestamp: datetime

    class Config:
        from_attributes = True

class AnalyticsDashboardPayload(BaseModel):
    summary: PerformanceSummary
    recent_logs: List[EvaluationLogEntry]