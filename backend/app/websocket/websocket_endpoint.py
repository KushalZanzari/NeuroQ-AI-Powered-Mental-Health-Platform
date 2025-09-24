from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.routing import APIRouter
import json
from typing import Optional

from app.websocket.connection_manager import ConnectionManager
from app.core.security import verify_token
from app.core.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

# Global connection manager
connection_manager = ConnectionManager()

async def get_current_user_from_token(token: str, db: Session) -> Optional[User]:
    """Get current user from JWT token."""
    email = verify_token(token)
    if not email:
        return None
    
    user = db.query(User).filter(User.email == email).first()
    return user

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time chat."""
    # Verify user token
    user = await get_current_user_from_token(token, db)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Connect user
    await connection_manager.connect(websocket, user.id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            message_type = message_data.get("type", "message")
            
            if message_type == "message":
                await connection_manager.handle_chat_message(
                    websocket, message_data, user.id
                )
            elif message_type == "typing":
                # Handle typing indicator
                await connection_manager.send_personal_message(
                    json.dumps({
                        "type": "typing_received",
                        "user_id": user.id,
                        "session_id": message_data.get("session_id")
                    }),
                    websocket
                )
            else:
                # Echo back unknown message types
                await connection_manager.send_personal_message(
                    json.dumps({
                        "type": "echo",
                        "content": f"Received: {message_data}",
                        "session_id": message_data.get("session_id")
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, user.id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        connection_manager.disconnect(websocket, user.id)
