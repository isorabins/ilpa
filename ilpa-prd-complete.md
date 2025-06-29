# Multi-Agent Life Planning System - PRD

## Executive Summary

**Project Name:** Integrated Life Planning Assistant (ILPA)
**Timeline:** 1 week for Phase 1 production-ready MVP
**Tech Stack:** Vercel (FastAPI + React), Supabase, Claude Agents with OpenAI fallback
**Development Approach:** Test-driven, leverage existing F@4 codebase patterns, clean and minimal

### The Core Concept: Interactive Life Coaching Through AI

This system fundamentally reimagines personal life planning by moving beyond static productivity tools to create an **interactive coaching experience** where specialized AI agents work together to provide integrated life guidance. The user has natural conversations with a Life Coach Agent throughout the week, then collaborates with a Weekly Planning Agent to create integrated plans using insights from domain-specific agents and uploaded artifacts.

**The Revolutionary Insight:** Most productivity and planning tools treat life areas as separate silos—health apps, business apps, creative apps, finance apps. This system recognizes that these areas actually support and influence each other when planned integratively. A person building a business while maintaining health goals and creative output needs planning that understands how these domains connect and reinforce each other.

### Phase 1 Architecture: Proven Patterns, Clear Separation

**Life Coach Agent:**
- Single point of contact for daily conversations
- Natural conversation interface about any life topic
- Persistent memory using F@4's proven conversation + memory table pattern
- SQL search tools to query domain tables when specifically asked
- Note: In Phase 1, Life Coach won't have access to domain data to keep it simple
- **Sample Prompt Direction:** "You are a supportive life coach who helps users reflect on their daily experiences, challenges, and growth. You remember past conversations and provide continuity..."

**Domain Agents (5 specialized):**
- Health Agent, Business Agent, Creative Agent, Travel Agent, Relationships Agent
- Process uploaded files and extract domain-specific insights
- Generate domain reports for Weekly Planning Agent
- Follow Claude agent best practices: simple, focused, stateless design
- Work entirely in background - users never interact with them directly

**Example File Types by Domain:**
- **Health:** Daily journal entries, workout logs, medical notes, mood tracking, sleep logs, nutrition diaries
- **Business:** Meeting notes, project updates, revenue reports, strategy docs, client feedback, goal tracking
- **Creative:** Writing drafts, project ideas, inspiration notes, progress logs, brainstorming sessions
- **Travel:** Trip planning docs, location research, travel journals, itineraries, experience reflections
- **Relationships:** Reflection notes, communication logs, social event planning, relationship insights

**Domain Agent Summary Format:**
Each domain agent delivers a structured weekly recommendation report:
```json
{
  "domain": "health",
  "week_of": "2024-01-15",
  "overview": "Based on your uploads, here's what I recommend focusing on this week...",
  "key_insights": [
    "You've been consistently exercising 4x/week",
    "Sleep quality improved when you meditated"
  ],
  "trends": [
    "Energy levels correlate with morning routine consistency",
    "Stress decreases with regular outdoor activities"
  ],
  "weekly_recommendations": [
    "Continue morning meditation practice",
    "Add one outdoor walk on low-energy days",
    "Track water intake to maintain hydration"
  ],
  "priority_level": "high" // high/medium/low based on user's current focus
}
```

**Weekly Planning Agent:**
- Interactive coaching conversation for weekly planning
- Reviews last week's plan completion status first
- Pulls insights from: Life Coach conversations/memory + all Domain Agent summaries
- Creates integrated weekly plans through collaborative dialogue
- Saves finalized plans to weekly_plans table
- 30-60 minute planning sessions (acceptable for personal use initially)
- **Context Assembly Order:**
  1. Previous week's plan and completion status
  2. Life Coach conversation summary (last 2 weeks)
  3. Domain agent recommendations (ordered by user's domain priorities)
- **Sample Prompt Direction:** "Guide the user through creating an integrated weekly plan. Start by reviewing last week's accomplishments and challenges, then incorporate recommendations from all life domains..."

**Memory Architecture (F@4 Pattern):**
- **conversations table**: All interactions stored permanently
- **memory table**: Short-term buffer with async background summarizations
- **Nightly summarizer**: Processes conversations → long-term memory (never summary of summary)
- **Memory table cleanup**: Deletes when hits 100 messages

**File Upload System:**
- User selects domain → routes to appropriate Domain Agent
- Domain Agents process files and store insights in domain tables
- Weekly Planning Agent accesses these insights during planning sessions

### Why This Approach Works

**For the User:**
- **Natural daily conversations** - just talk to Life Coach about anything
- **Intelligent domain organization** - Domain Agents automatically understand and categorize uploaded content
- **Integrated weekly planning** - Weekly Planning Agent sees full picture across all life areas
- **Collaborative plan creation** - user actively participates in creating plans they'll actually follow

**For the Architecture:**
- **Proven F@4 patterns** - conversation + memory system already battle-tested
- **Clean separation of concerns** - each agent has one clear responsibility
- **Phase 1 simplicity** - no complex domain extraction from conversations yet
- **Phase 2 ready** - architecture supports adding conversation → domain extraction later

---

## CRITICAL: Developer Setup Instructions (DO THIS FIRST!)

Before writing ANY code, the developer MUST complete these setup steps to ensure they can work independently:

### 1. Clone and Study F@4 Repositories
```bash
# Clone both repositories
git clone [fridays-at-four backend repo]
git clone [FAF_website frontend repo]

# Study the working code patterns, especially:
# - Authentication flow (Supabase integration)
# - Memory system (SimpleMemory class)
# - LLM Router (Claude + OpenAI fallback)
# - Chat streaming implementation
# - Database patterns
```

### 2. Set Up All Required Services

**Vercel Account:**
- Create new Vercel account if needed
- Install Vercel CLI: `npm i -g vercel`
- Login to Vercel CLI: `vercel login`
- Create new project for ILPA
- Verify can deploy with: `vercel --prod`

**Supabase:**
- Create new Supabase project for ILPA (or use F@4 dev database initially)
- Save all credentials:
  - Project URL
  - Anon Key
  - Service Role Key
- Install Supabase CLI
- Login to Supabase CLI
- Run initial migrations from F@4

**API Keys:**
- Anthropic API key (REQUIRED - get from Anthropic console)
- OpenAI API key (REQUIRED - for fallback)
- Store in `.env` file locally

### 3. Verify Everything Works
```bash
# Test Vercel deployment
vercel --prod

# Test Supabase connection
supabase db remote status

# Test API keys work
# Create simple test script to verify Claude API works
```

### 4. Create Project Structure
- Copy F@4 structure exactly
- Remove unused features (Slack, Zoom integrations)
- Keep auth, memory, and chat systems intact

---

## Developer Instructions & Philosophy

### Master Developer Approach
You are a senior full-stack developer who values:
- **Speed through simplicity** - Reuse F@4 patterns aggressively, don't reinvent wheels
- **Clean, readable code** - Every function should be obvious in purpose
- **Test-first mentality** - Write failing tests, then make them pass
- **Minimal viable features** - Build exactly what's needed for Phase 1, nothing more

### Test-Driven Development Protocol

**TDD Cycle for Every Feature:**
1. **Red:** Write a failing test that describes the behavior you want
2. **Green:** Write the minimal code to make the test pass
3. **Refactor:** Clean up code while keeping tests green
4. **Repeat:** Move to next smallest piece of functionality

**Testing Rules:**
- Every agent method gets a unit test before implementation
- Every API endpoint gets an integration test
- Every database operation includes user_id filtering validation
- Mock LLM responses for consistent testing
- Use real test database for integration tests
- Test LLM router fallback behavior

### Code Quality Standards

**File Organization (F@4 Pattern):**
```
src/
├── agents/
│   ├── base_agent.py              # Abstract base class with LLM router
│   ├── life_coach_agent.py        # Daily conversations + memory
│   ├── weekly_planning_agent.py   # Interactive planning sessions
│   ├── domain_agents/
│   │   ├── health_agent.py        # Health file processing + insights
│   │   ├── business_agent.py      # Business file processing + insights
│   │   ├── creative_agent.py      # Creative file processing + insights
│   │   ├── travel_agent.py        # Travel file processing + insights
│   │   └── relationships_agent.py # Relationships file processing + insights
│   └── nightly_summarizer.py     # Background memory processing
├── api/
│   ├── routers/
│   │   ├── conversations.py       # Life Coach chat endpoints
│   │   ├── uploads.py            # File upload to domain agents
│   │   ├── planning.py           # Weekly planning session endpoints
│   │   └── insights.py           # Domain data retrieval
│   └── main.py                   # FastAPI app with CORS
├── database/
│   ├── models.py                 # Supabase table schemas
│   ├── migrations/               # Database migrations
│   └── client.py                 # Database client with user filtering
├── llm/
│   ├── router.py                 # LLM routing (F@4 pattern)
│   └── prompts.py                # Agent prompts and templates
├── memory/
│   ├── conversation_manager.py   # F@4 conversation pattern
│   ├── memory_manager.py         # F@4 memory pattern  
│   └── summarizer.py             # Nightly background processing
└── tests/
    ├── unit/                     # Unit tests by module
    ├── integration/              # Cross-system tests
    └── fixtures/                 # Test data and mocks
```

**Code Style Rules:**
- Functions do one thing well
- No function longer than 20 lines
- Clear variable names (`health_insights` not `hi`)
- Type hints on all functions
- **User ID filtering EVERYWHERE** - no data leakage between users
- Comments explain "why", not "what"

---

## Technical Architecture

### Database Schema (Phase 1 - F@4 + Domain Extensions)

```sql
-- User conversations (F@4 pattern)
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'life_coach', -- 'life_coach', 'weekly_planning'
    message_type TEXT NOT NULL, -- 'user', 'assistant'
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    session_id TEXT, -- For grouping related messages
    metadata JSONB DEFAULT '{}'
);

-- Short-term memory buffer (F@4 pattern)
CREATE TABLE memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'life_coach',
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    message_count INTEGER DEFAULT 1,
    session_id TEXT
);

-- Long-term memory summaries (F@4 pattern)
CREATE TABLE memory_summaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'life_coach',
    summary_content TEXT NOT NULL,
    date_range_start DATE NOT NULL,
    date_range_end DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Domain agent data tables (separate for each domain)
CREATE TABLE health_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload', -- Ready for Phase 2 'conversation_extract'
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0, -- For weighing insights
    week_of DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE business_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'file_upload',
    raw_content TEXT,
    processed_insights JSONB,
    confidence_score FLOAT DEFAULT 1.0,
    week_of DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Similar tables for creative_data, travel_data, relationships_data

-- Weekly planning sessions
CREATE TABLE planning_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    session_id TEXT NOT NULL UNIQUE,
    week_of DATE NOT NULL,
    status TEXT DEFAULT 'active', -- 'active', 'completed', 'abandoned'
    opening_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Finalized weekly plans
CREATE TABLE weekly_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    week_of DATE NOT NULL,
    session_id TEXT REFERENCES planning_sessions(session_id),
    plan_content JSONB, -- {todos: [], priorities: [], insights: {}}
    completion_data JSONB DEFAULT '{}', -- Track todo completions
    created_at TIMESTAMP DEFAULT NOW()
);

-- File upload tracking
CREATE TABLE uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    filename TEXT NOT NULL,
    domain TEXT NOT NULL, -- 'health', 'business', etc.
    file_size INTEGER,
    processing_status TEXT DEFAULT 'pending',
    processed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- User preferences (manually populated initially)
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    preferences JSONB DEFAULT '{}', -- {name: 'John', age: 35, profession: 'Software Engineer', communication_style: 'direct'}
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance with user filtering
CREATE INDEX idx_conversations_user_agent ON conversations(user_id, agent_type, timestamp DESC);
CREATE INDEX idx_memory_user_agent ON memory(user_id, agent_type, timestamp DESC);
CREATE INDEX idx_health_data_user_week ON health_data(user_id, week_of);
CREATE INDEX idx_business_data_user_week ON business_data(user_id, week_of);
-- Similar indexes for other domain tables
CREATE INDEX idx_planning_sessions_user ON planning_sessions(user_id, week_of);
CREATE INDEX idx_weekly_plans_user ON weekly_plans(user_id, week_of);
```

### Agent Architecture (Claude Best Practices)

**Base Agent Pattern:**
Follow Claude agent best practices - simple, focused, stateless design. Each agent should have a single clear responsibility. Use the F@4 LLM router pattern for all agents.

**Life Coach Agent (Daily Conversations):**
- Handles daily conversations with memory context
- Uses F@4's SimpleMemory pattern exactly
- Stores all conversations in both conversations and memory tables
- Does NOT access domain data in Phase 1 (simplicity)
- System prompt focuses on supportive, reflective conversation

**Domain Agents (File Processing Specialists):**
Each domain agent (Health, Business, Creative, Travel, Relationships):
- Processes uploaded files for their specific domain
- Extracts structured insights and stores as JSON
- Generates domain reports when requested by Weekly Planning Agent
- Works entirely in background - no user interaction
- Adds confidence scores to insights for future relevance scoring

**Weekly Planning Agent (Interactive Coaching):**
- Starts planning sessions with context from all sources
- Receives summaries from domain agents (not raw data)
- Receives Life Coach conversation summaries
- Facilitates interactive planning conversation
- Saves finalized plans to database
- Uses collaborative, coaching-oriented prompts

### API Layer (FastAPI on Vercel)

**Core Endpoints with User Security:**
Copy F@4's authentication pattern exactly. Every endpoint must validate user_id from JWT token.

**Required Endpoints:**
- `/api/chat` - Daily conversation with Life Coach
- `/api/upload` - File upload to specific domain
- `/api/planning/start` - Begin weekly planning session
- `/api/planning/{session_id}/message` - Continue planning conversation
- `/api/planning/{session_id}/finalize` - Save completed plan
- `/api/plans/{week_of}` - Retrieve weekly plan
- `/api/plans/{plan_id}/todos/{todo_index}` - Update todo completion

### Memory System (F@4 Pattern)

**Copy F@4's memory system exactly:**
- SimpleMemory class for conversation persistence
- Nightly summarizer for long-term memory
- 100-message rolling window in memory table
- Never summarize summaries (prevent degradation)
- Vercel cron job for nightly processing

### Frontend (React + F@4 Components)

**Reuse F@4 Components:**
- Chat interface for Life Coach conversations
- Streaming message display
- Authentication flow
- User profile management

**New Components (Keep Simple):**
- File upload with domain selection dropdown
- Weekly planning chat interface (reuse chat components)
- Basic plan display showing todos and priorities
- Simple navigation between Life Coach and Planning modes

---

## Development Timeline (7 Days - Phase 1)

### Day 1: Foundation & LLM Infrastructure
**Morning:**
- [ ] Complete ALL environment setup (Vercel, Supabase, API keys)
- [ ] Verify can deploy to Vercel and connect to Supabase
- [ ] Copy F@4 project structure
- [ ] Set up Git repository

**Afternoon:**
- [ ] Copy F@4 LLM router exactly
- [ ] Copy F@4 database client with user filtering
- [ ] Copy F@4 authentication middleware
- [ ] Test basic FastAPI app deploys to Vercel

**Success Criteria:** Can authenticate user and make LLM calls with fallback

### Day 2: Life Coach Agent & Memory System
**Morning:**
- [ ] Copy F@4 SimpleMemory class exactly
- [ ] Implement LifeCoachAgent using F@4 chat patterns
- [ ] Set up conversation storage (copy F@4)

**Afternoon:**
- [ ] Copy F@4 nightly summarizer
- [ ] Set up Vercel cron for summarization
- [ ] Test conversation persistence and retrieval

**Success Criteria:** Life Coach works exactly like F@4 chat

### Day 3: Domain Agents & File Processing
**Morning:**
- [ ] Create base domain agent class
- [ ] Implement HealthAgent with simple file processing
- [ ] Test file upload and insight extraction

**Afternoon:**
- [ ] Implement remaining 4 domain agents (keep simple)
- [ ] Create file upload API endpoint
- [ ] Test all agents process files successfully

**Success Criteria:** All 5 domain agents can process files and store insights

### Day 4: Weekly Planning Agent
**Morning:**
- [ ] Create WeeklyPlanningAgent class
- [ ] Implement session management
- [ ] Create domain report aggregation

**Afternoon:**
- [ ] Build interactive planning conversation flow
- [ ] Implement plan finalization and storage
- [ ] Test complete planning workflow

**Success Criteria:** Can complete full planning session from start to finalized plan

### Day 5: Frontend Development
**Morning:**
- [ ] Set up React app (copy F@4 structure)
- [ ] Copy F@4 authentication components
- [ ] Copy F@4 chat interface exactly

**Afternoon:**
- [ ] Create simple file upload component
- [ ] Adapt chat interface for planning sessions
- [ ] Add basic navigation

**Success Criteria:** Frontend supports daily chat and file upload

### Day 6: Integration & Testing
**Morning:**
- [ ] End-to-end testing of complete workflow
- [ ] Fix integration issues
- [ ] Test with real files and conversations

**Afternoon:**
- [ ] Polish UI for personal use
- [ ] Add basic plan display
- [ ] Performance optimization if needed

**Success Criteria:** System works reliably end-to-end

### Day 7: Personal Use Testing
**Morning:**
- [ ] Deploy to production Vercel
- [ ] Run through complete weekly cycle
- [ ] Upload real personal files

**Afternoon:**
- [ ] Have real planning session
- [ ] Document any issues found
- [ ] Quick fixes for critical bugs

**Success Criteria:** System ready for daily personal use

---

## Phase 2 Planning (Future Enhancement)

### Domain Extraction from Conversations
- **Nightly Agent**: Extract domain insights from daily Life Coach conversations
- **Enhanced Planning**: Weekly Planning Agent gets richer data from both files and conversations
- **Pattern Recognition**: Cross-domain insights from natural conversation flow

### Advanced Features
- **Conversation Quality Scoring**: Track how well Life Coach understands user context
- **Domain Report Intelligence**: More sophisticated analysis and trend detection
- **Plan Effectiveness Tracking**: Monitor completion rates and adjust recommendations
- **Multi-week Planning**: Monthly and quarterly planning capabilities
- **Quick Planning Mode**: 5-minute plan generation for busy weeks
- **Webhooks**: Real-time updates when domain data changes

---

## Success Metrics

### MVP Feature List (Phase 1 Must-Haves)
- [ ] File upload to 5 domains with insight extraction
- [ ] Weekly planning sessions that aggregate domain agent recommendations
- [ ] Daily Life Coach conversations with memory
- [ ] Nightly conversation summarization
- [ ] Basic authentication (from F@4)
- [ ] Simple UI for chat and file uploads

### Performance Requirements
- **File processing time:** < 10 seconds per file
- **Chat response time:** < 3 seconds for first token
- **Planning session responsiveness:** < 3 seconds per response
- **Maximum file size:** 10MB
- **Context window management:** Handle gracefully (defer optimization to Phase 2)

### Technical Success
- [ ] All automated tests pass (copy F@4 test patterns)
- [ ] LLM router fallback works reliably under rate limits
- [ ] User data isolation verified (no cross-user data leakage)
- [ ] Memory system handles conversation summarization effectively
- [ ] File processing works for all 5 domain types
- [ ] Planning sessions complete successfully start to finish

### User Experience Success
- [ ] **Daily conversations feel natural and contextual** - Life Coach remembers previous interactions
- [ ] **File uploads provide valuable domain insights** - processed content enhances planning
- [ ] **Weekly planning feels collaborative** - user actively participates in plan creation
- [ ] **Plans are actionable and realistic** - based on real data about user's life
- [ ] **Memory system works invisibly** - conversations have continuity without feeling overwhelming
- [ ] **Domain organization is helpful** - insights are categorized usefully for planning

### Production Readiness
- [ ] **Authentication and security** - F@4's auth system works perfectly
- [ ] **Performance acceptable** - responses within 3 seconds
- [ ] **Error handling robust** - graceful degradation when services fail
- [ ] **Deployment simple** - single command to deploy updates
- [ ] **Personal use validated** - system handles real daily usage

---

## Risk Mitigation

### High-Risk Areas
1. **User data isolation** → Use F@4's proven user_id filtering everywhere
2. **LLM router reliability** → Copy F@4's fallback system exactly
3. **Memory system complexity** → Use F@4 patterns without modification
4. **Agent coordination** → Keep agents simple and independent

### Contingency Plans
- **If domain agents struggle with file processing** → Store raw content, improve processing later
- **If weekly planning is too complex** → Simplify to basic report aggregation
- **If memory system has issues** → F@4's system is proven, debug integration
- **If deployment issues on Vercel** → F@4 deploys successfully, follow same pattern

### Phase 1 Scope Protection
- **Focus on core workflow**: daily chat → file uploads → weekly planning
- **Defer advanced features**: conversation domain extraction, webhooks, quick planning
- **Leverage proven patterns**: F@4 code works in production, reuse aggressively
- **Test with real use case**: personal daily use validates functionality

**Key Philosophy:** Build something that works perfectly for daily personal use before expanding functionality. Every feature must prove its value through actual usage, and the system should feel natural and helpful from day one. Reuse F@4 code wherever possible - it's already production-tested.