from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatMessageCreate(BaseModel):
    message: str
    session_id: Optional[int] = None

class ChatMessageResponse(BaseModel):
    id: int
    message: str
    response: Optional[str] = None
    is_user_message: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatSessionCreate(BaseModel):
    session_name: Optional[str] = None

class ChatSessionUpdate(BaseModel):
    session_name: Optional[str] = None
    is_active: Optional[bool] = None

class ChatSessionInDB(BaseModel):
    id: int
    user_id: int
    session_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ChatSession(ChatSessionInDB):
    messages: List[ChatMessageResponse] = []

class ChatHistory(BaseModel):
    sessions: List[ChatSession]
    total_count: int
    page: int
    per_page: int

class WebSocketMessage(BaseModel):
    type: str  # "message", "typing", "error"
    content: str
    session_id: Optional[int] = None
    user_id: Optional[int] = None
