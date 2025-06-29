#!/usr/bin/env python3
"""
Configuration module for ILPA
Handles environment variables and app settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # LLM API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    
    # Database Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Authentication & Security
    JWT_SECRET = os.getenv("JWT_SECRET")
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", 12))
    
    # Application Configuration
    ENVIRONMENT = os.getenv("PYTHON_ENV", "development")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))
    ALLOWED_FILE_TYPES = os.getenv("ALLOWED_FILE_TYPES", ".txt,.md,.pdf,.docx,.json").split(",")
    
    # Agent System Configuration
    MEMORY_BUFFER_SIZE = int(os.getenv("MEMORY_BUFFER_SIZE", 100))
    MEMORY_CLEANUP_INTERVAL_HOURS = int(os.getenv("MEMORY_CLEANUP_INTERVAL_HOURS", 24))
    ENABLE_NIGHTLY_SUMMARIZATION = os.getenv("ENABLE_NIGHTLY_SUMMARIZATION", "true").lower() == "true"
    
    # Domain Agents Configuration
    ENABLE_HEALTH_AGENT = os.getenv("ENABLE_HEALTH_AGENT", "true").lower() == "true"
    ENABLE_BUSINESS_AGENT = os.getenv("ENABLE_BUSINESS_AGENT", "true").lower() == "true"
    ENABLE_CREATIVE_AGENT = os.getenv("ENABLE_CREATIVE_AGENT", "true").lower() == "true"
    ENABLE_TRAVEL_AGENT = os.getenv("ENABLE_TRAVEL_AGENT", "true").lower() == "true"
    ENABLE_RELATIONSHIPS_AGENT = os.getenv("ENABLE_RELATIONSHIPS_AGENT", "true").lower() == "true"
    
    # Planning Agent Configuration
    MAX_PLANNING_SESSION_MINUTES = int(os.getenv("MAX_PLANNING_SESSION_MINUTES", 60))
    PLANNING_SESSION_TIMEOUT_MINUTES = int(os.getenv("PLANNING_SESSION_TIMEOUT_MINUTES", 30))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "debug").upper()
    ENABLE_SQL_LOGGING = os.getenv("ENABLE_SQL_LOGGING", "false").lower() == "true"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_vars = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY", 
            "SUPABASE_URL",
            "SUPABASE_ANON_KEY",
            "JWT_SECRET"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True