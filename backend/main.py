#!/usr/bin/env python3
"""
ILPA Backend Main Application
FastAPI application following F@4 patterns
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio
import logging
from contextlib import asynccontextmanager

# Import our modules
from src.config import Config
from src.database.client import DatabaseClient
from src.llm.router import LLMRouter
from src.agents.life_coach_agent import LifeCoachAgent

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    try:
        # Validate configuration
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Initialize database client
        app.state.db_client = DatabaseClient()
        logger.info("Database client initialized")
        
        # Initialize LLM router
        app.state.llm_router = LLMRouter()
        logger.info("LLM router initialized")
        
        # Initialize Life Coach Agent
        app.state.life_coach_agent = LifeCoachAgent(
            db_client=app.state.db_client,
            llm_router=app.state.llm_router
        )
        logger.info("Life Coach Agent initialized")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down ILPA backend")

# Create FastAPI app
app = FastAPI(
    title="ILPA Backend",
    description="Integrated Life Planning Assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": Config.ENVIRONMENT,
        "message": "ILPA Backend is running"
    }

# Request/Response models
class ChatMessage(BaseModel):
    content: str
    user_id: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

# Chat endpoint (basic implementation)
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_life_coach(message: ChatMessage):
    """
    Chat with the Life Coach Agent
    """
    try:
        # Get Life Coach Agent from app state
        life_coach = app.state.life_coach_agent
        
        # Process the message
        response = await life_coach.process_message(
            user_id=message.user_id,
            content=message.content,
            session_id=message.session_id
        )
        
        return ChatResponse(
            response=response["content"],
            session_id=response["session_id"],
            timestamp=response["timestamp"]
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Conversation history endpoint
@app.get("/api/chat/history/{user_id}")
async def get_conversation_history(user_id: str, limit: Optional[int] = 50):
    """Get conversation history for a user"""
    try:
        db_client = app.state.db_client
        history = await db_client.get_conversation_history(user_id, limit)
        return {"conversations": history}
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if Config.ENVIRONMENT == "development" else False
    )