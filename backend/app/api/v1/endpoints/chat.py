from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSession as ChatSessionSchema,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistory
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/sessions", response_model=ChatSessionSchema)
def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    db_session = ChatSession(
        user_id=current_user.id,
        session_name=session_data.session_name
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return db_session

@router.get("/sessions", response_model=ChatHistory)
def get_chat_sessions(
    page: int = 1,
    per_page: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's chat sessions."""
    offset = (page - 1) * per_page
    
    # Get total count
    total_count = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).count()
    
    # Get sessions with pagination
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.created_at.desc()).offset(offset).limit(per_page).all()
    
    return ChatHistory(
        sessions=sessions,
        total_count=total_count,
        page=page,
        per_page=per_page
    )

@router.get("/sessions/{session_id}", response_model=ChatSessionSchema)
def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific chat session with messages."""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return session

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
def send_message(
    session_id: int,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message in a chat session."""
    # Verify session exists and belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # Create user message
    db_message = ChatMessage(
        session_id=session_id,
        user_id=current_user.id,
        message=message_data.message,
        is_user_message=True
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # TODO: Process message with AI and create response
    # For now, we'll create a placeholder response
    ai_response = "Thank you for your message. I'm here to help with your mental health concerns. How are you feeling today?"
    
    # Create AI response message
    ai_message = ChatMessage(
        session_id=session_id,
        user_id=current_user.id,
        message=ai_response,
        response=ai_response,
        is_user_message=False,
        ai_model_used="placeholder"
    )
    
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    return db_message

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
def get_session_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a chat session."""
    # Verify session exists and belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    return messages

@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a chat session."""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    db.delete(session)
    db.commit()
    
    return {"message": "Chat session deleted successfully"}
