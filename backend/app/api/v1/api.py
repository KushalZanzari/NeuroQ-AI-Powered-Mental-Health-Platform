from fastapi import APIRouter
from app.api.v1.endpoints import auth, symptoms, chat, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
