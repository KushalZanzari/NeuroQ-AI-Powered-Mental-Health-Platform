from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class SymptomSubmission(Base):
    __tablename__ = "symptom_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Input data
    input_text = Column(Text, nullable=False)
    selected_symptoms = Column(Text)  # JSON string of selected symptoms
    mood_rating = Column(Integer)  # 1-10 scale
    sleep_hours = Column(Float)
    stress_level = Column(Integer)  # 1-10 scale
    
    # AI Prediction results
    predicted_disorder = Column(String(100))
    confidence_score = Column(Float)
    severity_level = Column(String(50))  # mild, moderate, severe
    
    # AI Generated guidance
    recommendations = Column(Text)
    next_steps = Column(Text)
    emergency_contact_suggested = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="symptom_submissions")
    
    def __repr__(self):
        return f"<SymptomSubmission(id={self.id}, user_id={self.user_id}, disorder='{self.predicted_disorder}')>"
