from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models.chat import ChatSession, ChatMessage
from app.ai.agents.workflow import agent_graph
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: int | None = None

@router.post("/query")
async def chat_interaction(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Executes the agentic LangGraph execution loop for a user query.
    """
    # Manage session creation if not provided
    if not payload.session_id:
        session = ChatSession(title=payload.message[:30])
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = session.id
    else:
        session_id = payload.session_id

    # Log incoming user message
    user_msg = ChatMessage(session_id=session_id, sender="user", content=payload.message)
    db.add(user_msg)
    
    # Run the compiled state graph
    initial_state = {
        "messages": [{"role": "user", "content": payload.message}],
        "retrieved_context": [],
        "next_step": "agent"
    }
    
    try:
        final_output = agent_graph.invoke(initial_state)
        ai_response_text = final_output["messages"][-1].content
        
        # Log response metrics to database
        ai_msg = ChatMessage(
            session_id=session_id,
            sender="ai",
            content=ai_response_text,
            prompt_used="agentic_rag_v1"
        )
        db.add(ai_msg)
        db.commit()
        
        return {
            "session_id": session_id,
            "response": ai_response_text
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Agent Execution Failure: {str(e)}")