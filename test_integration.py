#!/usr/bin/env python3
"""
ILPA Integration Test Script
Tests that all core components are working together
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add backend to path
sys.path.append('backend')

async def test_configuration():
    """Test that configuration loads correctly"""
    print("🔧 Testing configuration...")
    try:
        from src.config import Config
        Config.validate()
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

async def test_database_client():
    """Test database client initialization"""
    print("🗄️ Testing database client...")
    try:
        from src.database.client import DatabaseClient
        db_client = DatabaseClient()
        print("✅ Database client initialized successfully")
        return True, db_client
    except Exception as e:
        print(f"❌ Database client initialization failed: {e}")
        return False, None

async def test_llm_router():
    """Test LLM router initialization"""
    print("🤖 Testing LLM router...")
    try:
        from src.llm.router import LLMRouter
        llm_router = LLMRouter()
        print("✅ LLM router initialized successfully")
        return True, llm_router
    except Exception as e:
        print(f"❌ LLM router initialization failed: {e}")
        return False, None

async def test_life_coach_agent(db_client, llm_router):
    """Test Life Coach Agent initialization"""
    print("👨‍💼 Testing Life Coach Agent...")
    try:
        from src.agents.life_coach_agent import LifeCoachAgent
        life_coach = LifeCoachAgent(db_client=db_client, llm_router=llm_router)
        print("✅ Life Coach Agent initialized successfully")
        return True, life_coach
    except Exception as e:
        print(f"❌ Life Coach Agent initialization failed: {e}")
        return False, None

async def test_full_integration():
    """Test complete system integration"""
    print("🚀 Starting ILPA Integration Test")
    print("=" * 50)
    
    # Test configuration
    if not await test_configuration():
        return False
    
    # Test database client
    db_success, db_client = await test_database_client()
    if not db_success:
        return False
    
    # Test LLM router
    llm_success, llm_router = await test_llm_router()
    if not llm_success:
        return False
    
    # Test Life Coach Agent
    agent_success, life_coach = await test_life_coach_agent(db_client, llm_router)
    if not agent_success:
        return False
    
    print("=" * 50)
    print("✅ All integration tests passed!")
    print()
    print("🎉 ILPA Core System is ready!")
    print()
    print("Next steps:")
    print("1. Run database migrations: Execute the SQL in backend/src/database/schema.sql in Supabase")
    print("2. Start the backend: cd backend && python main.py")
    print("3. Start the frontend: cd frontend && npm run dev")
    print("4. Create Vercel project for frontend deployment")
    print("5. Deploy backend to Heroku")
    
    return True

async def main():
    """Main test function"""
    try:
        success = await test_full_integration()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during testing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())