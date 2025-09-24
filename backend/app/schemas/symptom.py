from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SymptomInput(BaseModel):
    input_text: str
    selected_symptoms: Optional[List[str]] = None
    mood_rating: Optional[int] = None  # 1-10 scale
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None  # 1-10 scale

class SymptomPrediction(BaseModel):
    predicted_disorder: str
    confidence_score: float
    severity_level: str
    recommendations: str
    next_steps: str
    emergency_contact_suggested: bool

class SymptomSubmissionCreate(SymptomInput):
    pass

class SymptomSubmissionUpdate(BaseModel):
    input_text: Optional[str] = None
    selected_symptoms: Optional[List[str]] = None
    mood_rating: Optional[int] = None
    sleep_hours: Optional[float] = None
    stress_level: Optional[int] = None

class SymptomSubmissionInDB(SymptomInput):
    id: int
    user_id: int
    predicted_disorder: Optional[str] = None
    confidence_score: Optional[float] = None
    severity_level: Optional[str] = None
    recommendations: Optional[str] = None
    next_steps: Optional[str] = None
    emergency_contact_suggested: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

class SymptomSubmission(SymptomSubmissionInDB):
    pass

class SymptomHistory(BaseModel):
    submissions: List[SymptomSubmission]
    total_count: int
    page: int
    per_page: int
