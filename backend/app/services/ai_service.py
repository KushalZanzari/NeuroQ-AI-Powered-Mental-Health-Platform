from typing import List, Optional
import os
from app.schemas.symptom import SymptomPrediction
from app.core.config import settings

class AIService:
    def __init__(self):
        self.disorder_labels = [
            "Anxiety", "Depression", "Bipolar Disorder", "PTSD", 
            "OCD", "ADHD", "Eating Disorder", "Substance Abuse",
            "Schizophrenia", "Personality Disorder", "No Disorder"
        ]
        # Lightweight keyword maps for heuristic scoring (no heavy deps)
        self.keyword_map = {
            "Anxiety": ["anxiety", "anxious", "worry", "panic", "nervous"],
            "Depression": ["depressed", "sad", "hopeless", "empty", "down"],
            "Bipolar Disorder": ["manic", "mania", "mood swings", "euphoric"],
            "PTSD": ["flashbacks", "nightmares", "trauma", "startle"],
            "OCD": ["obsessive", "compulsive", "checking", "rituals", "intrusive"],
            "ADHD": ["focus", "attention", "hyper", "restless", "impulsive"],
            "Eating Disorder": ["eating", "binge", "purge", "anorexia", "bulimia"],
            "Substance Abuse": ["drinking", "alcohol", "drugs", "substances", "addiction"],
            "Schizophrenia": ["voices", "hallucinations", "paranoid", "delusions"],
            "Personality Disorder": ["relationships", "identity", "unstable", "abandonment"],
        }
    
    # Backward-compat API no-op for previous calls
    def load_model(self):
        return
    
    def predict_mental_health(
        self,
        input_text: str,
        selected_symptoms: Optional[List[str]] = None,
        mood_rating: Optional[int] = None,
        sleep_hours: Optional[float] = None,
        stress_level: Optional[int] = None
    ) -> SymptomPrediction:
        """Predict mental health disorder based on input."""
        try:
            input_text_lower = (input_text or "").lower()
            all_tokens = set(input_text_lower.split())
            if selected_symptoms:
                all_tokens.update([s.lower() for s in selected_symptoms])

            # Simple keyword scoring
            scores = {label: 0 for label in self.disorder_labels}
            for label, keywords in self.keyword_map.items():
                for kw in keywords:
                    if kw in input_text_lower:
                        scores[label] += 1

            # Fallback to No Disorder if nothing matched
            disorder_name = max(scores, key=lambda k: scores[k]) if any(scores.values()) else "No Disorder"

            # Confidence heuristic
            base = scores.get(disorder_name, 0)
            # Normalize to a rough confidence between 0.5 and 0.95
            confidence_score = 0.5 + min(base, 5) * 0.09
            
            # Determine severity level
            severity_level = self._determine_severity(confidence_score, mood_rating, stress_level)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(disorder_name, severity_level)
            
            # Generate next steps
            next_steps = self._generate_next_steps(disorder_name, severity_level)
            
            # Determine if emergency contact is suggested
            emergency_suggested = self._should_suggest_emergency_contact(
                disorder_name, severity_level, input_text
            )
            
            return SymptomPrediction(
                predicted_disorder=disorder_name,
                confidence_score=confidence_score,
                severity_level=severity_level,
                recommendations=recommendations,
                next_steps=next_steps,
                emergency_contact_suggested=emergency_suggested
            )
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            # Return safe default prediction
            return SymptomPrediction(
                predicted_disorder="No Disorder",
                confidence_score=0.5,
                severity_level="mild",
                recommendations="Please consult with a mental health professional for a proper assessment.",
                next_steps="Consider speaking with a therapist or counselor.",
                emergency_contact_suggested=False
            )
    
    # Legacy function removed; heuristic path does not require feature prep
    
    def _determine_severity(self, confidence: float, mood_rating: Optional[int], stress_level: Optional[int]) -> str:
        """Determine severity level based on confidence and other factors."""
        if confidence > 0.8 or (mood_rating and mood_rating <= 3) or (stress_level and stress_level >= 8):
            return "severe"
        elif confidence > 0.6 or (mood_rating and mood_rating <= 5) or (stress_level and stress_level >= 6):
            return "moderate"
        else:
            return "mild"
    
    def _generate_recommendations(self, disorder: str, severity: str) -> str:
        """Generate personalized recommendations based on disorder and severity."""
        recommendations = {
            "Anxiety": {
                "mild": "Practice deep breathing exercises, maintain a regular sleep schedule, and consider mindfulness meditation.",
                "moderate": "Consider therapy or counseling, practice relaxation techniques, and maintain a healthy lifestyle.",
                "severe": "Seek immediate professional help, consider medication consultation, and have a support system in place."
            },
            "Depression": {
                "mild": "Maintain regular exercise, establish a daily routine, and stay connected with loved ones.",
                "moderate": "Consider therapy, maintain physical activity, and monitor your mood patterns.",
                "severe": "Seek immediate professional help, consider medication, and ensure you have emergency contacts."
            },
            "No Disorder": {
                "mild": "Continue maintaining good mental health practices and regular self-care.",
                "moderate": "Continue current practices and consider preventive mental health measures.",
                "severe": "Continue current practices and consider regular mental health check-ins."
            }
        }
        
        return recommendations.get(disorder, recommendations["No Disorder"]).get(severity, recommendations["No Disorder"]["mild"])
    
    def _generate_next_steps(self, disorder: str, severity: str) -> str:
        """Generate next steps based on disorder and severity."""
        if severity == "severe":
            return "1. Contact a mental health professional immediately\n2. Reach out to emergency services if needed\n3. Inform a trusted friend or family member\n4. Follow up with regular appointments"
        elif severity == "moderate":
            return "1. Schedule an appointment with a mental health professional\n2. Practice recommended coping strategies\n3. Monitor your symptoms\n4. Consider joining a support group"
        else:
            return "1. Continue self-care practices\n2. Monitor your mental health\n3. Consider preventive counseling\n4. Maintain healthy lifestyle habits"
    
    def _should_suggest_emergency_contact(self, disorder: str, severity: str, input_text: str) -> bool:
        """Determine if emergency contact should be suggested."""
        emergency_keywords = ["suicide", "kill myself", "end it all", "not worth living", "harm myself"]
        
        if severity == "severe" or any(keyword in input_text.lower() for keyword in emergency_keywords):
            return True
        
        return False
