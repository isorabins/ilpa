-- ILPA Database Schema
-- Based on F@4 patterns with ILPA-specific extensions

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User conversations (F@4 pattern)
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'life_coach', -- 'life_coach', 'weekly_planning', domain agents
    message_type TEXT NOT NULL, -- 'user', 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    session_id TEXT,
    metadata JSONB DEFAULT '{}'
);

-- Short-term memory buffer (F@4 pattern)
CREATE TABLE memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'life_coach',
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    message_count INTEGER DEFAULT 1,
    session_id TEXT
);

-- Long-term memory summaries (F@4 pattern)
CREATE TABLE memory_summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'life_coach',
    summary_content TEXT NOT NULL,
    date_range_start DATE NOT NULL,
    date_range_end DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Domain agent data tables
CREATE TABLE health_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload', -- 'file_upload', 'conversation_extract' for Phase 2
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0,
    week_of DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE business_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload',
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0,
    week_of DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE creative_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload',
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0,
    week_of DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE travel_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload',
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0,
    week_of DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE relationships_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload',
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0,
    week_of DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Weekly planning sessions
CREATE TABLE planning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    session_id TEXT NOT NULL UNIQUE,
    week_of DATE NOT NULL,
    status TEXT DEFAULT 'active', -- 'active', 'completed', 'abandoned'
    opening_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Finalized weekly plans
CREATE TABLE weekly_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    week_of DATE NOT NULL,
    session_id TEXT REFERENCES planning_sessions(session_id),
    plan_content JSONB, -- {todos: [], priorities: [], insights: {}}
    completion_data JSONB DEFAULT '{}', -- Track todo completions
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- File upload tracking
CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    filename TEXT NOT NULL,
    domain TEXT NOT NULL, -- 'health', 'business', 'creative', 'travel', 'relationships'
    file_size INTEGER,
    processing_status TEXT DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User preferences
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE,
    preferences JSONB DEFAULT '{}', -- {name: 'John', communication_style: 'direct', etc.}
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_conversations_user_agent ON conversations(user_id, agent_type, timestamp DESC);
CREATE INDEX idx_memory_user_agent ON memory(user_id, agent_type, timestamp DESC);
CREATE INDEX idx_memory_summaries_user_agent ON memory_summaries(user_id, agent_type, date_range_start DESC);

CREATE INDEX idx_health_data_user_week ON health_data(user_id, week_of);
CREATE INDEX idx_business_data_user_week ON business_data(user_id, week_of);
CREATE INDEX idx_creative_data_user_week ON creative_data(user_id, week_of);
CREATE INDEX idx_travel_data_user_week ON travel_data(user_id, week_of);
CREATE INDEX idx_relationships_data_user_week ON relationships_data(user_id, week_of);

CREATE INDEX idx_planning_sessions_user ON planning_sessions(user_id, week_of);
CREATE INDEX idx_weekly_plans_user ON weekly_plans(user_id, week_of);
CREATE INDEX idx_uploaded_files_user ON uploaded_files(user_id, created_at DESC);

-- Security handled in application code via user_id filtering
-- All database operations will include WHERE user_id = ? clauses