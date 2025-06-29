#!/usr/bin/env python3
"""
Life Coach Agent for ILPA
Handles daily conversations with memory context
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from src.database.client import DatabaseClient
from src.llm.router import LLMRouter
from src.memory.simple_memory import SimpleMemory

logger = logging.getLogger(__name__)

class LifeCoachAgent:
    """Life Coach Agent for daily conversations with memory"""
    
    def __init__(self, db_client: DatabaseClient, llm_router: LLMRouter):
        """Initialize Life Coach Agent"""
        self.db_client = db_client
        self.llm_router = llm_router
        self.agent_type = "life_coach"
        
        # Life Coach system prompt
        self.system_prompt = """You are a supportive life coach who helps users reflect on their daily experiences, challenges, and growth. 

Key characteristics:
- Supportive and empathetic, but not overly therapeutic
- Focus on practical life planning and goal achievement
- Help users connect different areas of their life (health, business, creativity, travel, relationships)
- Ask thoughtful follow-up questions to encourage reflection
- Remember past conversations and provide continuity
- Guide users toward actionable insights

Keep responses conversational and helpful. You're a trusted friend who happens to be excellent at life coaching."""
        
        logger.info("Life Coach Agent initialized")
    
    async def process_message(self, user_id: str, content: str, 
                             session_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a message from the user"""
        try:
            # Generate session ID if not provided
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Get memory context for this user
            memory_context = await self._get_memory_context(user_id)
            
            # Save user message to conversations
            await self.db_client.save_conversation(
                user_id=user_id,
                agent_type=self.agent_type,
                message_type="user",
                content=content,
                session_id=session_id
            )
            
            # Save to memory buffer
            await self.db_client.save_memory(
                user_id=user_id,
                agent_type=self.agent_type,
                content=f"User: {content}",
                session_id=session_id
            )
            
            # Build conversation context
            conversation_context = self._build_conversation_context(memory_context, content)
            
            # Get response from LLM
            response_content = await self._generate_response(conversation_context)
            
            # Save assistant response
            await self.db_client.save_conversation(
                user_id=user_id,
                agent_type=self.agent_type,
                message_type="assistant", 
                content=response_content,
                session_id=session_id
            )
            
            # Save assistant response to memory
            await self.db_client.save_memory(
                user_id=user_id,
                agent_type=self.agent_type,
                content=f"Assistant: {response_content}",
                session_id=session_id
            )
            
            # Clean up old memories if needed
            await self._cleanup_memory_if_needed(user_id)
            
            return {
                "content": response_content,
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_type": self.agent_type
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    async def _get_memory_context(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent memory context for the user"""
        try:
            memories = await self.db_client.get_memory(
                user_id=user_id,
                agent_type=self.agent_type,
                limit=limit
            )
            return memories
            
        except Exception as e:
            logger.error(f"Error getting memory context: {str(e)}")
            return []
    
    def _build_conversation_context(self, memory_context: List[Dict], current_message: str) -> str:
        """Build conversation context for LLM"""
        context_parts = [self.system_prompt]
        
        if memory_context:
            context_parts.append("\\n\\nRecent conversation context:")
            for memory in reversed(memory_context[-5:]):  # Last 5 memory entries
                context_parts.append(memory.get('content', ''))
        
        context_parts.append(f"\\n\\nCurrent message: {current_message}")
        context_parts.append("\\nPlease respond as the life coach:")
        
        return "\\n".join(context_parts)
    
    async def _generate_response(self, conversation_context: str) -> str:
        """Generate response using LLM router"""
        try:
            # Use the LLM router to get a response
            response = await self.llm_router.generate_response(
                prompt=conversation_context,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I'm having trouble processing your message right now. Could you try again?"
    
    async def _cleanup_memory_if_needed(self, user_id: str):
        """Clean up old memories if buffer is too full"""
        try:
            from src.config import Config
            
            # Get current memory count
            memories = await self.db_client.get_memory(
                user_id=user_id,
                agent_type=self.agent_type,
                limit=1000
            )
            
            if len(memories) > Config.MEMORY_BUFFER_SIZE:
                await self.db_client.cleanup_memory(
                    user_id=user_id,
                    agent_type=self.agent_type,
                    keep_count=Config.MEMORY_BUFFER_SIZE
                )
                
        except Exception as e:
            logger.error(f"Error cleaning up memory: {str(e)}")
            # Don't raise - this is a background cleanup task