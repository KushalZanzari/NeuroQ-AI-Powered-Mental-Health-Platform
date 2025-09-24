from fastapi import WebSocket
from typing import List, Dict
import json
import asyncio
from app.services.ai_service import AIService

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, WebSocket] = {}
        self.ai_service = AIService()
    
    async def connect(self, websocket: WebSocket, user_id: int = None):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int = None):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending message: {e}")
    
    async def send_to_user(self, message: str, user_id: int):
        """Send a message to a specific user."""
        if user_id in self.user_connections:
            await self.send_personal_message(message, self.user_connections[user_id])
    
    async def broadcast(self, message: str):
        """Broadcast a message to all active connections."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
    
    async def handle_chat_message(self, websocket: WebSocket, message_data: dict, user_id: int):
        """Handle incoming chat messages and generate AI responses."""
        try:
            user_message = message_data.get("content", "")
            session_id = message_data.get("session_id")
            
            # Send typing indicator
            await self.send_personal_message(
                json.dumps({
                    "type": "typing",
                    "content": "AI is thinking...",
                    "session_id": session_id
                }),
                websocket
            )
            
            # Generate AI response (simplified for now)
            ai_response = await self._generate_ai_response(user_message, user_id)
            
            # Send AI response
            await self.send_personal_message(
                json.dumps({
                    "type": "message",
                    "content": ai_response,
                    "session_id": session_id,
                    "is_ai": True
                }),
                websocket
            )
            
        except Exception as e:
            print(f"Error handling chat message: {e}")
            await self.send_personal_message(
                json.dumps({
                    "type": "error",
                    "content": "Sorry, I encountered an error. Please try again.",
                    "session_id": session_id
                }),
                websocket
            )
    
    async def _generate_ai_response(self, user_message: str, user_id: int) -> str:
        """Generate AI response for chat messages."""
        try:
            # Simple keyword-based responses for demonstration
            # In production, you would use a more sophisticated AI model
            
            message_lower = user_message.lower()
            
            if any(word in message_lower for word in ["anxiety", "anxious", "worried"]):
                return "I understand you're feeling anxious. Try taking deep breaths and focusing on the present moment. Would you like to talk about what's making you feel this way?"
            
            elif any(word in message_lower for word in ["depressed", "sad", "down"]):
                return "I'm sorry you're feeling this way. It's important to remember that these feelings are temporary. Have you been able to maintain your daily routines?"
            
            elif any(word in message_lower for word in ["sleep", "insomnia", "tired"]):
                return "Sleep issues can significantly impact mental health. Try maintaining a consistent sleep schedule and creating a relaxing bedtime routine. How many hours of sleep are you getting?"
            
            elif any(word in message_lower for word in ["help", "support", "counseling"]):
                return "It's great that you're reaching out for help. Professional support can be very beneficial. Would you like me to help you find resources in your area?"
            
            else:
                return "Thank you for sharing that with me. I'm here to listen and help. Can you tell me more about how you're feeling today?"
                
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "I'm here to help. Please tell me more about what's on your mind."
