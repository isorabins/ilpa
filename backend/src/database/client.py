#!/usr/bin/env python3
"""
Database Client for ILPA
Supabase integration following F@4 patterns
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from supabase import create_client, Client
from src.config import Config

logger = logging.getLogger(__name__)

class DatabaseClient:
    """Database client with user filtering following F@4 patterns"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_SERVICE_ROLE_KEY
        )
        logger.info("Database client initialized")
    
    async def get_conversation_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for a user"""
        try:
            result = self.supabase.table('conversations') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('timestamp', desc=True) \
                .limit(limit) \
                .execute()
            
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            raise
    
    async def save_conversation(self, user_id: str, agent_type: str, message_type: str, 
                               content: str, session_id: Optional[str] = None, 
                               metadata: Optional[Dict] = None) -> Dict:
        """Save a conversation message"""
        try:
            conversation_data = {
                'user_id': user_id,
                'agent_type': agent_type,
                'message_type': message_type,
                'content': content,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'session_id': session_id,
                'metadata': metadata or {}
            }
            
            result = self.supabase.table('conversations') \
                .insert(conversation_data) \
                .execute()
            
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            raise
    
    async def save_memory(self, user_id: str, agent_type: str, content: str, 
                         session_id: Optional[str] = None) -> Dict:
        """Save to memory table"""
        try:
            memory_data = {
                'user_id': user_id,
                'agent_type': agent_type,
                'content': content,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'session_id': session_id,
                'message_count': 1
            }
            
            result = self.supabase.table('memory') \
                .insert(memory_data) \
                .execute()
            
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error saving memory: {str(e)}")
            raise
    
    async def get_memory(self, user_id: str, agent_type: str = 'life_coach', 
                        limit: int = 100) -> List[Dict]:
        """Get memory for a user and agent type"""
        try:
            result = self.supabase.table('memory') \
                .select('*') \
                .eq('user_id', user_id) \
                .eq('agent_type', agent_type) \
                .order('timestamp', desc=True) \
                .limit(limit) \
                .execute()
            
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting memory: {str(e)}")
            raise
    
    async def cleanup_memory(self, user_id: str, agent_type: str = 'life_coach', 
                           keep_count: int = 100) -> int:
        """Clean up old memory entries, keeping only the most recent ones"""
        try:
            # Get all memory entries for this user/agent
            all_memories = await self.get_memory(user_id, agent_type, limit=1000)
            
            if len(all_memories) <= keep_count:
                return 0
            
            # Delete the oldest entries
            entries_to_delete = all_memories[keep_count:]
            deleted_count = 0
            
            for entry in entries_to_delete:
                self.supabase.table('memory') \
                    .delete() \
                    .eq('id', entry['id']) \
                    .execute()
                deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old memory entries for user {user_id}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up memory: {str(e)}")
            raise
    
    async def save_weekly_plan(self, user_id: str, week_of: str, session_id: str,
                              plan_content: Dict, completion_data: Optional[Dict] = None) -> Dict:
        """Save a weekly plan"""
        try:
            plan_data = {
                'user_id': user_id,
                'week_of': week_of,
                'session_id': session_id,
                'plan_content': plan_content,
                'completion_data': completion_data or {},
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            result = self.supabase.table('weekly_plans') \
                .insert(plan_data) \
                .execute()
            
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error saving weekly plan: {str(e)}")
            raise
    
    async def get_weekly_plan(self, user_id: str, week_of: str) -> Optional[Dict]:
        """Get a weekly plan for a specific week"""
        try:
            result = self.supabase.table('weekly_plans') \
                .select('*') \
                .eq('user_id', user_id) \
                .eq('week_of', week_of) \
                .order('created_at', desc=True) \
                .limit(1) \
                .execute()
            
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error getting weekly plan: {str(e)}")
            raise
    
    async def save_domain_data(self, user_id: str, domain: str, source_type: str,
                              raw_content: str, processed_insights: Dict,
                              confidence_score: float = 1.0, week_of: Optional[str] = None) -> Dict:
        """Save domain agent data"""
        try:
            table_name = f"{domain}_data"
            
            domain_data = {
                'user_id': user_id,
                'source_type': source_type,
                'raw_content': raw_content,
                'processed_insights': processed_insights,
                'confidence_score': confidence_score,
                'week_of': week_of,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            result = self.supabase.table(table_name) \
                .insert(domain_data) \
                .execute()
            
            return result.data[0] if result.data else {}
            
        except Exception as e:
            logger.error(f"Error saving {domain} domain data: {str(e)}")
            raise
    
    async def get_domain_data(self, user_id: str, domain: str, limit: int = 50) -> List[Dict]:
        """Get domain data for a user"""
        try:
            table_name = f"{domain}_data"
            
            result = self.supabase.table(table_name) \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .limit(limit) \
                .execute()
            
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting {domain} domain data: {str(e)}")
            raise