from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.database.models.chat import ChatMessage, ChatSession
from app.schemas.analytics import AnalyticsDashboardPayload, PerformanceSummary, EvaluationLogEntry
from app.api.deps import get_current_admin_user
from app.database.models.user import User

router = APIRouter()

@router.get("/dashboard", response_model=AnalyticsDashboardPayload)
def get_evaluation_analytics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user) # Secure: Admin validation required
):
    """
    Computes statistical summaries of the AI Agent performance metrics 
    and returns recent conversational evaluation traces.
    """
    # 1. Compute aggregate metrics over all database rows safely
    metrics_query = db.query(
        func.count(ChatSession.id).label("total_convs"),
        func.coalesce(func.sum(ChatMessage.tokens_used), 0).label("total_tokens"),
        func.coalesce(func.avg(ChatMessage.latency_ms), 0.0).label("avg_latency"),
        func.coalesce(func.avg(ChatMessage.similarity_score), 0.0).label("avg_similarity")
    ).select_from(ChatSession).outerjoin(ChatMessage).first()

    summary_data = PerformanceSummary(
        total_conversations=metrics_query.total_convs,
        total_tokens_consumed=metrics_query.total_tokens,
        average_latency_ms=round(float(metrics_query.avg_latency), 2),
        average_similarity_score=round(float(metrics_query.avg_similarity), 4)
    )

    # 2. Fetch the latest AI evaluation traces for auditing
    recent_messages = db.query(ChatMessage).filter(
        ChatMessage.sender == "ai"
    ).order_by(ChatMessage.timestamp.desc()).limit(10).all()

    logs = [EvaluationLogEntry.model_validate(msg) for msg in recent_messages]

    return AnalyticsDashboardPayload(summary=summary_data, recent_logs=logs)
