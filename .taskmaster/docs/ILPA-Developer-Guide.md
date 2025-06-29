# ILPA Agent Implementation Guide - Final Developer Instructions

## 🎯 **Critical Context: This is NOT F@4**

Hey developer! Before you start coding, understand this fundamental difference:
- **F@4**: Single agent system (SimpleChatHandler)
- **ILPA**: Multi-agent orchestration system

While we're copying F@4's authentication, memory, and LLM router, the agent architecture is completely new. This guide shows you exactly how to build it using Claude best practices.

---

## 📋 **Project Overview - CORRECTED**

**Project**: Integrated Life Planning Assistant (ILPA)  
**Timeline**: 7-Day MVP Development  
**Tech Stack**: **Heroku (FastAPI backend)** + **Vercel (React frontend)**, Supabase, Claude Agents with OpenAI fallback  
**Core Concept**: Multi-agent orchestration system for integrated life guidance  

### **🎯 Success Metrics**
- File processing: <10s (text files only)
- Chat response: <3s  
- Planning session responsiveness: <3s
- Max file size: 10MB

### **🚀 MVP Philosophy**
**Copy, Don't Build**: Leverage F@4's proven patterns directly. No overengineering, no premature optimization, no complex features for personal MVP.

---

## 🏗️ **ILPA Agent Architecture Overview**

```
User Interactions:
├── Daily: User ↔ Life Coach Agent (conversational, with memory)
├── Anytime: User → File Upload → Domain Agent (stateless processing)
└── Weekly: User ↔ Planning Agent ↔ All Agents (orchestration)

Data Flow:
├── Conversations → Life Coach → conversations + memory tables
├── Files → Domain Agents → domain_data tables
└── Planning → Planning Agent reads all → weekly_plans table
```

### **🔧 Deployment Architecture - CORRECTED**
- **Backend**: **Heroku** (FastAPI + Uvicorn)
- **Frontend**: **Vercel** (Next.js + React)
- **Database**: Supabase (supports async operations)
- **AI**: Claude 3.5 Sonnet/Haiku + OpenAI GPT-4 fallback

---

## 📐 **Specific Agent Implementation Using Claude Best Practices**

### **1. Base Agent Classes (Two Types)**

Based on Claude best practices, we need TWO base classes because we have two fundamentally different agent types:

```python
# src/agents/base_conversational_agent.py
from src.llm_router import LLMRouter  # Copy from F@4
from abc import ABC, abstractmethod
import json

class ConversationalAgent(ABC):
    """For agents that have conversations (Life Coach, Planning)"""
    
    def __init__(self, agent_name: str, system_prompt: str, memory_system=None):
        self.agent_name = agent_name
        self.router = LLMRouter()  # F@4's router
        self.system_prompt = system_prompt
        self.memory = memory_system
        
    async def chat(self, user_id: str, message: str, session_id: str = None):
        """Handle conversation with optional memory context"""
        # Build messages following Claude best practices
        messages = []
        
        # Add memory context if available
        if self.memory:
            context = await self.memory.get_recent_conversations(user_id, session_id)
            if context:
                # Use XML tags for structure (Claude best practice)
                context_prompt = f"""<context>
Previous conversation context:
{json.dumps(context, indent=2)}
</context>

<current_message>
{message}
</current_message>"""
                messages.append({"role": "user", "content": context_prompt})
        else:
            messages.append({"role": "user", "content": message})
        
        # Get response
        response = await self.router.route_request(
            messages=messages,
            system=self.system_prompt,
            model="claude-3-5-sonnet-20241022"  # Best model for complex conversations
        )
        
        # Store in memory if available
        if self.memory and session_id:
            await self.memory.store_conversation(
                user_id=user_id,
                session_id=session_id,
                user_message=message,
                agent_response=response
            )
        
        return response


# src/agents/base_processing_agent.py
class ProcessingAgent(ABC):
    """For agents that process data without conversation (Domain Agents)"""
    
    def __init__(self, domain: str, system_prompt: str):
        self.domain = domain
        self.router = LLMRouter()  # F@4's router
        self.system_prompt = system_prompt
    
    async def process(self, content: str, instruction: str = None):
        """Process content and return structured output"""
        # Use XML structure for clarity (Claude best practice)
        prompt = f"""<task>
Process the following {self.domain} content and extract insights.
</task>

<content>
{content}
</content>

<instructions>
{instruction or f"Extract key {self.domain} insights and patterns."}
</instructions>

<output_format>
Provide structured insights as JSON with these fields:
- summary: Brief overview
- key_points: List of main insights
- actionable_items: Specific recommendations
- patterns: Any patterns noticed
</output_format>"""
        
        messages = [{"role": "user", "content": prompt}]
        
        response = await self.router.route_request(
            messages=messages,
            system=self.system_prompt,
            model="claude-3-5-haiku-20241022"  # Cheaper model for simple extraction
        )
        
        # Parse response as JSON
        try:
            return json.loads(response)
        except:
            # Fallback if not valid JSON
            return {"summary": response, "key_points": [], "actionable_items": [], "patterns": []}
```

### **2. Life Coach Agent Implementation**

```python
# src/agents/life_coach_agent.py
from src.agents.base_conversational_agent import ConversationalAgent

class LifeCoachAgent(ConversationalAgent):
    """Primary conversational agent with full memory system"""
    
    def __init__(self, memory_system):
        system_prompt = """You are a compassionate and insightful life coach AI assistant. 
Your role is to:
- Listen deeply to what users share about their daily experiences
- Ask thoughtful follow-up questions to help them reflect
- Remember previous conversations and reference them naturally
- Help users identify patterns and connections in their life
- Provide supportive, non-judgmental guidance
- Encourage growth while accepting where they are

You have access to the user's conversation history. Reference it naturally when relevant, 
but don't overwhelm them with constant callbacks to previous discussions.

Keep responses conversational, warm, and focused on the user's wellbeing."""
        
        super().__init__(
            agent_name="life_coach",
            system_prompt=system_prompt,
            memory_system=memory_system
        )
    
    async def get_weekly_summary(self, user_id: str):
        """Generate summary for planning agent"""
        # Get last week's conversations
        recent_convos = await self.memory.get_conversations_since(
            user_id, 
            days_ago=7
        )
        
        if not recent_convos:
            return "No recent conversations to summarize."
        
        # Use Claude to summarize
        summary_prompt = f"""<task>
Summarize the key themes, challenges, and progress from these conversations for weekly planning.
</task>

<conversations>
{json.dumps(recent_convos, indent=2)}
</conversations>

<output_format>
Provide a summary focusing on:
1. Main themes discussed
2. Challenges mentioned
3. Progress or wins celebrated
4. Areas needing attention in the upcoming week
</output_format>"""
        
        messages = [{"role": "user", "content": summary_prompt}]
        
        return await self.router.route_request(
            messages=messages,
            system="You are a helpful assistant that summarizes conversations for planning purposes.",
            model="claude-3-5-sonnet-20241022"
        )
```

### **3. Domain Agent Implementation (All 5 Share This Pattern)**

```python
# src/agents/domain_agents.py
from src.agents.base_processing_agent import ProcessingAgent
from src.database import DatabaseClient
import json
from datetime import datetime, timedelta

class DomainAgent(ProcessingAgent):
    """Generic domain agent for all 5 domains - MVP: TEXT FILES ONLY"""
    
    def __init__(self, domain: str, db_client: DatabaseClient):
        self.db = db_client
        
        # Domain-specific prompts
        domain_prompts = {
            "health": "You are a health insights analyst. Focus on physical health, mental wellbeing, exercise, nutrition, sleep, and wellness practices.",
            "business": "You are a business strategy analyst. Focus on work projects, career development, professional goals, and business outcomes.",
            "creative": "You are a creative project analyst. Focus on artistic endeavors, creative processes, inspiration, and creative output.",
            "travel": "You are a travel experience analyst. Focus on travel plans, location experiences, cultural insights, and adventure goals.",
            "relationships": "You are a relationships analyst. Focus on social connections, family dynamics, friendships, and interpersonal growth."
        }
        
        system_prompt = domain_prompts.get(domain, f"You are a {domain} analyst.")
        super().__init__(domain=domain, system_prompt=system_prompt)
    
    async def process_file(self, user_id: str, file_content: str, filename: str):
        """Process uploaded file and store insights - MVP: TEXT ONLY"""
        # MVP: Only support text files
        supported_extensions = ['.txt', '.md']
        if not filename.endswith(tuple(supported_extensions)):
            return {"error": "Only .txt and .md files supported in MVP"}
        
        # Extract insights using base class method
        insights = await self.process(
            content=file_content,
            instruction=f"Extract {self.domain}-related insights from this file."
        )
        
        # Store in domain table
        await self.db.create_with_user_filter(
            table=f"{self.domain}_data",
            data={
                "content": file_content[:1000],  # Store first 1000 chars
                "insights": json.dumps(insights),
                "filename": filename,
                "processed_at": datetime.utcnow().isoformat()
            },
            user_id=user_id
        )
        
        return insights
    
    async def get_weekly_summary(self, user_id: str):
        """Get domain summary for planning agent"""
        # Query this week's data
        week_start = datetime.utcnow() - timedelta(days=7)
        
        data = await self.db.get_user_filtered(
            table=f"{self.domain}_data",
            user_id=user_id,
            filters={"created_at__gte": week_start.isoformat()}
        )
        
        if not data:
            return {"domain": self.domain, "summary": f"No {self.domain} data this week", "recommendations": []}
        
        # Aggregate insights
        all_insights = [json.loads(item['insights']) for item in data]
        
        # Generate weekly summary using Claude
        summary_prompt = f"""<task>
Create a weekly {self.domain} summary and recommendations for planning.
</task>

<insights>
{json.dumps(all_insights, indent=2)}
</insights>

<output_format>
Return JSON with:
{{
  "domain": "{self.domain}",
  "summary": "Brief overview of this week's {self.domain} insights",
  "key_patterns": ["pattern1", "pattern2"],
  "recommendations": ["specific recommendation 1", "specific recommendation 2", "specific recommendation 3"],
  "priority": "high|medium|low"
}}
</output_format>"""
        
        response = await self.process(
            content=json.dumps(all_insights),
            instruction=summary_prompt
        )
        
        return response


# Factory function to create domain agents
def create_domain_agents(db_client: DatabaseClient):
    """Create all 5 domain agents"""
    domains = ["health", "business", "creative", "travel", "relationships"]
    return {domain: DomainAgent(domain, db_client) for domain in domains}
```

### **4. Weekly Planning Agent (The Orchestrator)**

```python
# src/agents/weekly_planning_agent.py
from src.agents.base_conversational_agent import ConversationalAgent
from typing import Dict
import uuid
import json

class WeeklyPlanningAgent(ConversationalAgent):
    """Orchestrates weekly planning by gathering insights from all agents"""
    
    def __init__(self, life_coach_agent, domain_agents: Dict[str, DomainAgent], db_client):
        self.life_coach = life_coach_agent
        self.domain_agents = domain_agents
        self.db = db_client
        
        system_prompt = """You are a strategic weekly planning assistant. Your role is to:
- Review insights from all life domains and daily conversations
- Help users create integrated, realistic weekly plans
- Identify connections between different life areas
- Prioritize based on the user's current situation and goals
- Create actionable, specific tasks that consider the whole person

You have access to summaries from:
1. Daily life coaching conversations
2. Health domain insights
3. Business domain insights
4. Creative domain insights
5. Travel domain insights
6. Relationships domain insights

Guide users through creating a balanced, achievable weekly plan."""
        
        super().__init__(
            agent_name="weekly_planning",
            system_prompt=system_prompt,
            memory_system=None  # Planning agent doesn't need memory
        )
    
    async def start_planning_session(self, user_id: str):
        """Initialize planning session with all domain insights"""
        # 1. Get Life Coach summary
        coach_summary = await self.life_coach.get_weekly_summary(user_id)
        
        # 2. Get all domain summaries
        domain_summaries = {}
        for domain_name, agent in self.domain_agents.items():
            domain_summaries[domain_name] = await agent.get_weekly_summary(user_id)
        
        # 3. Get last week's plan completion (if exists)
        last_week_plan = await self._get_last_week_plan(user_id)
        
        # 4. Create planning context using XML structure
        planning_context = f"""<planning_context>
<life_coach_insights>
{coach_summary}
</life_coach_insights>

<domain_insights>
{json.dumps(domain_summaries, indent=2)}
</domain_insights>

<last_week_plan>
{json.dumps(last_week_plan, indent=2) if last_week_plan else "No previous plan"}
</last_week_plan>
</planning_context>

Let's create this week's plan. Start by reviewing what happened last week and the insights from each life area."""
        
        # 5. Generate opening message
        messages = [{"role": "user", "content": planning_context}]
        
        opening_message = await self.router.route_request(
            messages=messages,
            system=self.system_prompt,
            model="claude-3-5-sonnet-20241022"  # Best model for complex planning
        )
        
        # 6. Store session
        session_id = str(uuid.uuid4())
        await self.db.create_with_user_filter(
            table="planning_sessions",
            data={
                "session_id": session_id,
                "status": "active",
                "domain_summaries": json.dumps(domain_summaries),
                "coach_summary": coach_summary,
                "opening_message": opening_message
            },
            user_id=user_id
        )
        
        return {
            "session_id": session_id,
            "opening_message": opening_message,
            "context": {
                "coach_insights": coach_summary,
                "domain_insights": domain_summaries,
                "last_week": last_week_plan
            }
        }
    
    async def continue_planning_conversation(self, user_id: str, session_id: str, user_message: str):
        """Handle planning dialogue"""
        # Get session context
        session = await self.db.get_user_filtered(
            table="planning_sessions",
            user_id=user_id,
            filters={"session_id": session_id}
        )
        
        if not session:
            raise ValueError("Session not found")
        
        # Build conversation with context
        context = f"""<session_context>
Domain Summaries: {session[0]['domain_summaries']}
Coach Summary: {session[0]['coach_summary']}
</session_context>

User says: {user_message}"""
        
        response = await self.chat(user_id, context, session_id)
        
        # Check if plan is ready to finalize
        if "PLAN_COMPLETE" in response or "finalize" in user_message.lower():
            return await self._finalize_plan(user_id, session_id, response)
        
        return {"response": response, "status": "continuing"}
    
    async def _finalize_plan(self, user_id: str, session_id: str, plan_content: str):
        """Save finalized weekly plan"""
        # Extract structured plan using Claude
        extract_prompt = f"""<task>
Extract the weekly plan from this conversation into a structured format.
</task>

<plan_content>
{plan_content}
</plan_content>

<output_format>
Return JSON with:
{{
  "week_theme": "Overall theme or focus",
  "priorities": ["priority 1", "priority 2", "priority 3"],
  "todos": [
    {{"task": "specific task", "domain": "health|business|creative|travel|relationships", "priority": "high|medium|low"}},
    ...
  ],
  "daily_habits": ["habit 1", "habit 2"],
  "notes": "Any additional notes"
}}
</output_format>"""
        
        messages = [{"role": "user", "content": extract_prompt}]
        
        structured_plan = await self.router.route_request(
            messages=messages,
            system="You are a helpful assistant that extracts structured data from text.",
            model="claude-3-5-haiku-20241022"  # Simple extraction task
        )
        
        # Save plan
        plan_data = json.loads(structured_plan)
        await self.db.create_with_user_filter(
            table="weekly_plans",
            data={
                "session_id": session_id,
                "plan_content": plan_data,
                "created_at": datetime.utcnow().isoformat()
            },
            user_id=user_id
        )
        
        # Update session status
        await self.db.update_session_status(session_id, "completed")
        
        return {"status": "completed", "plan": plan_data}
```

---

## 🎮 **Agent Registry Pattern (How It All Connects)**

```python
# src/agents/agent_registry.py
from src.agents.life_coach_agent import LifeCoachAgent
from src.agents.domain_agents import create_domain_agents
from src.agents.weekly_planning_agent import WeeklyPlanningAgent
from src.simple_memory import MemorySystem  # Copy from F@4

class AgentRegistry:
    """Central registry for all agents - singleton pattern"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
        
        # Initialize once
        self.db_client = DatabaseClient()  # From F@4 patterns
        self.memory_system = MemorySystem(self.db_client)  # From F@4
        
        # Initialize agents
        self.life_coach = LifeCoachAgent(self.memory_system)
        self.domain_agents = create_domain_agents(self.db_client)
        self.planning_agent = WeeklyPlanningAgent(
            life_coach_agent=self.life_coach,
            domain_agents=self.domain_agents,
            db_client=self.db_client
        )
        
        self.initialized = True
    
    def get_agent(self, agent_type: str):
        """Get specific agent by type"""
        if agent_type == "life_coach":
            return self.life_coach
        elif agent_type == "planning":
            return self.planning_agent
        elif agent_type in self.domain_agents:
            return self.domain_agents[agent_type]
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

# Global registry instance
agent_registry = AgentRegistry()
```

---

## 🔌 **SIMPLIFIED API Endpoints (7 Total, Not 23)**

```python
# src/api/endpoints.py
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from src.agents.agent_registry import agent_registry
from src.auth import get_current_user  # From F@4

router = APIRouter()

# Life Coach endpoints
@router.post("/api/chat")
async def chat_with_life_coach(
    message: str,
    session_id: str = None,
    user_id: str = Depends(get_current_user)
):
    """Daily conversation with Life Coach"""
    try:
        agent = agent_registry.get_agent("life_coach")
        response = await agent.chat(user_id, message, session_id)
        return {"response": response, "agent": "life_coach"}
    except Exception as e:
        logger.error(f"Life Coach failed: {e}")
        return {"error": "Chat failed, please try again"}

# Domain file upload
@router.post("/api/upload/{domain}")
async def upload_to_domain(
    domain: str,
    file: UploadFile,
    user_id: str = Depends(get_current_user)
):
    """Upload file to specific domain agent - TEXT FILES ONLY"""
    # Max file size check
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    try:
        agent = agent_registry.get_agent(domain)
        content = await file.read()
        
        # For MVP, just extract text
        text_content = content.decode('utf-8', errors='ignore')
        
        insights = await agent.process_file(user_id, text_content, file.filename)
        return {"status": "processed", "domain": domain, "insights": insights}
    except Exception as e:
        logger.error(f"Domain {domain} processing failed: {e}")
        return {"error": "File processing failed, please try again"}

# Planning endpoints
@router.post("/api/planning/start")
async def start_planning_session(user_id: str = Depends(get_current_user)):
    """Start weekly planning session"""
    try:
        agent = agent_registry.get_agent("planning")
        session_data = await agent.start_planning_session(user_id)
        return session_data
    except Exception as e:
        logger.error(f"Planning start failed: {e}")
        return {"error": "Failed to start planning session"}

@router.post("/api/planning/{session_id}/message")
async def planning_conversation(
    session_id: str,
    message: str,
    user_id: str = Depends(get_current_user)
):
    """Continue planning conversation"""
    try:
        agent = agent_registry.get_agent("planning")
        response = await agent.continue_planning_conversation(user_id, session_id, message)
        return response
    except Exception as e:
        logger.error(f"Planning conversation failed: {e}")
        return {"error": "Planning conversation failed"}

@router.post("/api/planning/{session_id}/finalize")
async def finalize_plan(
    session_id: str,
    user_id: str = Depends(get_current_user)
):
    """Finalize and save weekly plan"""
    try:
        agent = agent_registry.get_agent("planning")
        plan = await agent._finalize_plan(user_id, session_id, "User requested finalization")
        return plan
    except Exception as e:
        logger.error(f"Plan finalization failed: {e}")
        return {"error": "Failed to finalize plan"}

@router.get("/api/plans/current")
async def get_current_plan(user_id: str = Depends(get_current_user)):
    """Get current week's plan"""
    try:
        # Get this week's plan from database
        week_start = datetime.utcnow() - timedelta(days=7)
        plans = await db.get_user_filtered(
            "weekly_plans",
            user_id,
            {"created_at__gte": week_start.isoformat()}
        )
        return {"plans": plans}
    except Exception as e:
        logger.error(f"Get current plan failed: {e}")
        return {"error": "Failed to get current plan"}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
```

---

## 🔧 **F@4 Code Reference System - CORRECTED**

### **✅ Copy F@4 Files Directly (DO NOT MODIFY)**
```bash
# Backend files to copy exactly:
fridays-at-four/src/llm_router.py              # LLM routing with fallback
fridays-at-four/src/simple_memory.py           # Memory system (NO embeddings)
fridays-at-four/src/claude_client_simple.py    # Claude API integration
fridays-at-four/src/main.py                    # FastAPI auth patterns
fridays-at-four/src/config.py                  # Configuration patterns

# Frontend files to copy:
FAF_website/auth/                               # Authentication pages
FAF_website/hoc/withPrivateRoute.tsx           # Auth HOCs
FAF_website/hoc/withPublicRoute.tsx            # Public route wrapper
FAF_website/app/providers.tsx                  # Auth context
FAF_website/components/ui/                      # UI components
```

### **🔧 F@4 Memory System - NO EMBEDDINGS**
```python
# Copy from fridays-at-four/src/simple_memory.py EXACTLY
class MemorySystem:
    def __init__(self, db_client):
        self.db = db_client
        self.conversation_buffer = {}  # In-memory buffer
    
    async def get_relevant_memories(self, user_id: str, keyword: str):
        """KEYWORD search, NOT semantic search"""
        results = await self.db.supabase.table('memories')\
            .select('*')\
            .eq('user_id', user_id)\
            .ilike('content', f'%{keyword}%')\
            .execute()
        return results.data
```

### **🚫 What NOT to Build**
- ❌ Embeddings or semantic search (F@4 doesn't use these)
- ❌ Rate limiting systems (not needed for personal MVP)
- ❌ Unit tests (test with real usage)
- ❌ Complex file parsing (text files only)
- ❌ Custom auth endpoints (copy F@4's)
- ❌ Connection pooling setup (Supabase handles automatically)

---

## 📅 **CORRECTED 7-Day Development Timeline**

### **Pre-requisites (Day 0)**
```bash
# Check these BEFORE starting:
- [ ] Anthropic API key obtained
- [ ] OpenAI API key obtained  
- [ ] Supabase project created
- [ ] Both F@4 repos cloned and working locally
- [ ] Heroku CLI installed and logged in
- [ ] Vercel CLI installed and logged in
```

### **Day 1: Foundation + F@4 Integration**
1. **Copy F@4 core files** (auth, memory, LLM router)
2. **Set up Heroku backend project**
3. **Create simplified database schema** (no vectors)
4. **Test F@4 patterns work with your database**

### **Day 2: Life Coach Agent**
1. **Create base agent classes** (ConversationalAgent, ProcessingAgent)
2. **Implement LifeCoachAgent with memory**
3. **Test conversation flow end-to-end**
4. **Verify memory persistence works**

### **Day 3: Domain Agents**
1. **Implement generic DomainAgent class**
2. **Create all 5 domain agents using factory**
3. **Test file processing (text files only)**
4. **Create agent registry pattern**

### **Day 4: Planning Agent**
1. **Implement WeeklyPlanningAgent orchestration**
2. **Test gathering summaries from all agents**
3. **Test planning conversation flow**
4. **Test plan finalization and storage**

### **Day 5: API Integration**
1. **Create 7 FastAPI endpoints** (not 23)
2. **Connect all agents to endpoints**
3. **Test full workflow: chat → upload → plan**
4. **Add error handling everywhere**

### **Day 6: Frontend**
1. **Copy F@4 auth components** (don't build new)
2. **Adapt F@4 chat interface for ILPA**
3. **Create simple file upload UI**
4. **Create planning interface**

### **Day 7: Deploy & Test**
1. **Deploy backend to Heroku**
2. **Deploy frontend to Vercel**
3. **End-to-end testing**
4. **Fix deployment issues**

---

## 🗃️ **Database Schema - SIMPLIFIED (NO VECTORS)**

```sql
-- Copy F@4's conversation pattern
CREATE TABLE conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Simple memory (NO VECTOR COLUMNS)
CREATE TABLE memories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    content TEXT NOT NULL,
    keywords TEXT[], -- For simple keyword search
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Domain data tables (5 simple tables)
CREATE TABLE health_data (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    content TEXT NOT NULL,
    insights JSONB,
    filename TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Repeat for: business_data, creative_data, travel_data, relationships_data

-- Planning sessions
CREATE TABLE planning_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    session_id TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    domain_summaries JSONB,
    coach_summary TEXT,
    opening_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Weekly plans
CREATE TABLE weekly_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    session_id TEXT NOT NULL,
    plan_content JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🚀 **Deployment Configuration - CORRECTED**

### **Heroku Backend Setup**
```bash
# Create Heroku app
heroku create ilpa-backend

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
heroku config:set SUPABASE_URL=your_url
heroku config:set SUPABASE_ANON_KEY=your_key
heroku config:set JWT_SECRET_KEY=your_secret

# Create Procfile
echo "web: uvicorn src.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
git push heroku main
```

### **Vercel Frontend Setup**
```bash
# Create Vercel project
vercel init ilpa-frontend

# Set environment variables in Vercel dashboard:
NEXT_PUBLIC_API_URL=https://ilpa-backend.herokuapp.com
NEXT_PUBLIC_SUPABASE_URL=your_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_key

# Deploy
vercel deploy
```

### **FastAPI CORS Configuration**
```python
# src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ⚠️ **Critical Implementation Notes**

### **1. Model Selection Strategy**
- **Life Coach & Planning**: `claude-3-5-sonnet-20241022` (complex conversations)
- **Domain Agents**: `claude-3-5-haiku-20241022` (simple extraction, cheaper)
- **Fallback**: OpenAI GPT-4 (F@4's router handles automatically)

### **2. Memory Management - CORRECTED**
- **ONLY Life Coach has memory** - Domain and Planning agents are stateless
- **Use F@4's keyword search** - NO embeddings or semantic search
- **Supabase DOES support async** - the previous claim was incorrect
- **Session IDs are UUIDs** - generate for each conversation thread

### **3. File Processing - MVP ONLY**
```python
# Only support text files for MVP
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
supported_extensions = ['.txt', '.md']

async def process_file(file: UploadFile):
    if not file.filename.endswith(tuple(supported_extensions)):
        raise HTTPException(400, "Only .txt and .md files supported")
    
    content = await file.read()
    text = content.decode('utf-8', errors='ignore')
    return text
```

### **4. Error Handling Pattern**
```python
# Wrap all agent calls
try:
    response = await agent.process(...)
except Exception as e:
    logger.error(f"Agent {agent_name} failed: {e}")
    return {"error": "Processing failed, please try again"}
```

### **5. Testing Strategy - NO UNIT TESTS**
```python
# Create ONE test script for full workflow
async def test_full_workflow():
    # 1. Test life coach chat
    response = await life_coach.chat("user123", "I'm stressed")
    assert response
    
    # 2. Test file upload
    insights = await health_agent.process_file("user123", "Ran 5k", "log.txt")
    assert insights
    
    # 3. Test planning session
    session = await planning_agent.start_planning_session("user123")
    assert session["opening_message"]
    
    print("✅ Full workflow test passed")

# Run with: python test_workflow.py
```

---

## ✅ **Final Checklist - CORRECTED**

### **Technical Corrections**
- [ ] ✅ **Heroku for backend**, not Vercel  
- [ ] ✅ **Supabase supports async** - use it properly
- [ ] ✅ **NO embeddings/semantic search** - keyword search only
- [ ] ✅ **7 API endpoints**, not 23 tasks
- [ ] ✅ **Text files only** for MVP
- [ ] ✅ **Copy F@4 auth** - don't build new
- [ ] ✅ **No unit tests** - test with real usage

### **Agent Architecture**
- [ ] Life Coach is the ONLY agent with memory
- [ ] Domain agents are stateless processors  
- [ ] Planning agent orchestrates but doesn't store conversation
- [ ] Agent registry provides clean singleton access
- [ ] All agents use F@4's LLM router for fallback
- [ ] Error handling at every level
- [ ] User data isolation (user_id filtering everywhere)

### **Deployment Ready**
- [ ] Heroku app created and configured
- [ ] Vercel project created and configured
- [ ] CORS configured for frontend domain
- [ ] Environment variables set in both platforms
- [ ] Database schema applied to Supabase

**Remember**: This is a multi-agent system, NOT a single agent like F@4. Each agent has a specific role and they communicate through the database, not directly with each other. Keep it simple, follow Claude best practices, and copy F@4 patterns exactly where specified. 