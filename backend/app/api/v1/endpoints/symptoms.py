from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.symptom import SymptomSubmission
from app.schemas.symptom import (
    SymptomSubmissionCreate, 
    SymptomSubmission as SymptomSubmissionSchema,
    SymptomHistory,
    SymptomPrediction
)
from app.api.v1.endpoints.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/submit", response_model=SymptomSubmissionSchema)
def submit_symptoms(
    symptom_data: SymptomSubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit symptoms for AI analysis."""
    # Create symptom submission record
    db_submission = SymptomSubmission(
        user_id=current_user.id,
        input_text=symptom_data.input_text,
        selected_symptoms=symptom_data.selected_symptoms,
        mood_rating=symptom_data.mood_rating,
        sleep_hours=symptom_data.sleep_hours,
        stress_level=symptom_data.stress_level
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    # Get AI prediction
    try:
        ai_service = AIService()
        prediction = ai_service.predict_mental_health(
            input_text=symptom_data.input_text,
            selected_symptoms=symptom_data.selected_symptoms,
            mood_rating=symptom_data.mood_rating,
            sleep_hours=symptom_data.sleep_hours,
            stress_level=symptom_data.stress_level
        )
        
        # Update submission with AI results
        db_submission.predicted_disorder = prediction.predicted_disorder
        db_submission.confidence_score = prediction.confidence_score
        db_submission.severity_level = prediction.severity_level
        db_submission.recommendations = prediction.recommendations
        db_submission.next_steps = prediction.next_steps
        db_submission.emergency_contact_suggested = prediction.emergency_contact_suggested
        
        db.commit()
        db.refresh(db_submission)
        
    except Exception as e:
        # Log error but don't fail the request
        print(f"AI prediction error: {str(e)}")
        # You might want to use proper logging here
    
    return db_submission

@router.get("/history", response_model=SymptomHistory)
def get_symptom_history(
    page: int = 1,
    per_page: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's symptom submission history."""
    offset = (page - 1) * per_page
    
    # Get total count
    total_count = db.query(SymptomSubmission).filter(
        SymptomSubmission.user_id == current_user.id
    ).count()
    
    # Get submissions with pagination
    submissions = db.query(SymptomSubmission).filter(
        SymptomSubmission.user_id == current_user.id
    ).order_by(SymptomSubmission.created_at.desc()).offset(offset).limit(per_page).all()
    
    return SymptomHistory(
        submissions=submissions,
        total_count=total_count,
        page=page,
        per_page=per_page
    )

@router.get("/{submission_id}", response_model=SymptomSubmissionSchema)
def get_symptom_submission(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific symptom submission."""
    submission = db.query(SymptomSubmission).filter(
        SymptomSubmission.id == submission_id,
        SymptomSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symptom submission not found"
        )
    
    return submission

@router.delete("/{submission_id}")
def delete_symptom_submission(
    submission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a symptom submission."""
    submission = db.query(SymptomSubmission).filter(
        SymptomSubmission.id == submission_id,
        SymptomSubmission.user_id == current_user.id
    ).first()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Symptom submission not found"
        )
    
    db.delete(submission)
    db.commit()
    
    return {"message": "Symptom submission deleted successfully"}
