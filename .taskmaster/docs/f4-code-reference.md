# F@4 Code Reference Guide for ILPA

## 🎯 **How to Use This Guide**
This document maps specific files from your existing F@4 repositories to ILPA implementation tasks. Each section shows:
- **Exact file paths** in F@4 repos
- **What patterns to extract**
- **How to adapt for ILPA**
- **Where to implement in ILPA**

---

## 🗂️ **Repository Structure Reference**

```
/Applications/app_life_coach/
├── fridays-at-four/          # Backend F@4 patterns
├── FAF_website/              # Frontend F@4 patterns  
└── [ILPA implementation]     # Your new code goes here
```

---

## 🔧 **Backend Patterns (Task-Specific)**

### **Task 2: Base Agent & LLM Router**
```bash
# Reference Files:
fridays-at-four/src/main.py                    # FastAPI setup patterns
fridays-at-four/src/simple_memory.py           # Base agent structure
fridays-at-four/src/claude_client.py           # Direct Claude API calls

# Key Patterns to Extract:
- FastAPI app initialization (main.py:1-50)
- Singleton agent pattern (simple_memory.py:15-45)
- Direct Anthropic API integration (claude_client.py:1-100)
- Streaming response handling (main.py:80-120)

# Implement in ILPA:
src/agents/base_agent.py                       # Base agent class
src/llm/router.py                              # LLM routing logic
src/llm/providers/anthropic.py                # Anthropic integration
src/llm/providers/openai.py                   # OpenAI fallback
```

### **Task 3: Database Client & Models**
```bash
# Reference Files:
fridays-at-four/supabase/schema.sql           # Database schema patterns
fridays-at-four/src/database.py               # Database client setup
fridays-at-four/src/models/                   # Model definitions

# Key Patterns to Extract:
- Async database client (database.py:1-80)
- User filtering everywhere (all models)
- Auto-dependency creation (schema.sql:50-100)
- Connection pooling (database.py:20-40)

# Implement in ILPA:
src/database/client.py                        # Database client
src/models/user.py                            # User model
src/models/conversation.py                    # Conversation model
src/models/memory.py                          # Memory model
src/models/domain_data.py                     # Domain data models
```

### **Task 4: Authentication Middleware**
```bash
# Reference Files:
fridays-at-four/src/auth/                     # Auth patterns
fridays-at-four/src/middleware/               # Middleware patterns

# Key Patterns to Extract:
- JWT validation (auth/jwt.py:1-50)
- FastAPI dependencies (middleware/auth.py:1-40)
- Supabase integration (auth/supabase.py:1-80)
- Session management (auth/session.py:1-60)

# Implement in ILPA:
src/auth/middleware.py                        # Auth middleware
src/auth/dependencies.py                      # FastAPI dependencies
src/auth/jwt_handler.py                       # JWT logic
```

### **Task 16: F@4 Memory System**
```bash
# Reference Files (CRITICAL):
fridays-at-four/src/simple_memory.py          # Memory management core
fridays-at-four/src/memory_bank.py            # Memory bank patterns
fridays-at-four/supabase/migrations/          # Memory table schemas

# Key Patterns to Extract:
- Memory buffer management (simple_memory.py:60-100)
- Conversation storage (simple_memory.py:120-160)
- Memory retrieval methods (memory_bank.py:40-80)
- Nightly summarization (simple_memory.py:180-220)

# Implement in ILPA:
src/memory/memory_manager.py                  # Core memory system
src/memory/conversation_store.py              # Conversation storage
src/memory/buffer.py                          # Memory buffer
src/memory/summarizer.py                      # Nightly summarizer
```

### **Tasks 17-21: Domain Agents**
```bash
# Reference Files:
fridays-at-four/src/agents/                   # Agent base patterns
fridays-at-four/src/file_processing/          # File processing patterns

# Key Patterns to Extract:
- Agent inheritance (agents/base.py:1-50)
- File processing pipeline (file_processing/processor.py:1-100)
- NLP integration patterns (agents/nlp.py:1-80)
- Insight extraction (agents/analyzer.py:40-90)

# Implement in ILPA:
src/agents/domain/health_agent.py             # Health domain agent
src/agents/domain/business_agent.py           # Business domain agent  
src/agents/domain/creative_agent.py           # Creative domain agent
src/agents/domain/travel_agent.py             # Travel domain agent
src/agents/domain/relationships_agent.py      # Relationships domain agent
```

---

## 🌐 **Frontend Patterns (Task-Specific)**

### **Task 11: Chat Interface**
```bash
# Reference Files:
FAF_website/app/components/Chat/              # Chat components
FAF_website/app/hooks/useChat.ts              # Chat hooks
FAF_website/app/api/chat/                     # Chat API integration

# Key Patterns to Extract:
- Real-time chat UI (Chat/ChatComponent.tsx:1-150)
- Message streaming (hooks/useChat.ts:40-80)
- Chat history (Chat/ChatHistory.tsx:1-100)
- Typing indicators (Chat/TypingIndicator.tsx:1-50)

# Implement in ILPA:
app/components/chat/ChatInterface.tsx         # Main chat component
app/hooks/useLifeCoach.ts                     # Life coach chat hook
app/components/chat/MessageStream.tsx         # Streaming messages
```

### **Task 12: Planning Interface**
```bash
# Reference Files:
FAF_website/app/components/Planning/          # Planning UI patterns
FAF_website/app/hooks/usePlanning.ts          # Planning state management

# Key Patterns to Extract:
- Interactive planning UI (Planning/PlanningSession.tsx:1-200)
- Drag-and-drop (Planning/DragDrop.tsx:1-120)
- Plan visualization (Planning/PlanViewer.tsx:1-150)

# Implement in ILPA:
app/components/planning/WeeklyPlanner.tsx     # Weekly planning interface
app/components/planning/PlanBuilder.tsx       # Interactive plan builder
app/hooks/useWeeklyPlanning.ts                # Planning state management
```

### **Task 14: Frontend Authentication**
```bash
# Reference Files:
FAF_website/app/auth/                         # Auth components
FAF_website/app/hooks/useAuth.ts              # Auth state management
FAF_website/app/middleware.ts                 # Route protection

# Key Patterns to Extract:
- Login/register forms (auth/AuthForms.tsx:1-150)
- JWT management (hooks/useAuth.ts:20-80)
- Protected routes (middleware.ts:1-60)
- Session handling (auth/SessionManager.tsx:1-100)

# Implement in ILPA:
app/components/auth/LoginForm.tsx             # Login form
app/components/auth/RegisterForm.tsx          # Register form
app/hooks/useAuth.ts                          # Auth state management
app/middleware.ts                             # Route protection
```

---

## 📦 **Direct Copy vs Adapt Strategy**

### **Direct Copy (Minimal Changes)**
```bash
# These files can be copied almost directly:
fridays-at-four/src/claude_client.py          → src/llm/providers/anthropic.py
fridays-at-four/src/database.py               → src/database/client.py
FAF_website/app/hooks/useAuth.ts               → app/hooks/useAuth.ts
FAF_website/app/middleware.ts                  → app/middleware.ts
```

### **Adapt & Extend**
```bash
# These files need significant adaptation:
fridays-at-four/src/simple_memory.py          → src/memory/ (split into multiple files)
fridays-at-four/src/main.py                   → src/main.py (add ILPA-specific routes)
FAF_website/app/components/Chat/               → app/components/chat/ (add life coach features)
```

### **Reference Only**
```bash
# These files are for pattern reference only:
fridays-at-four/supabase/schema.sql           # Reference for ILPA schema design
FAF_website/app/components/Planning/           # Reference for planning UI concepts
fridays-at-four/src/agents/                   # Reference for agent architecture
```

---

## 🚀 **Implementation Workflow**

### **For Each Task:**

1. **📖 Study Reference Files**
   ```bash
   # Example for Task 2:
   cat fridays-at-four/src/main.py | head -50
   cat fridays-at-four/src/simple_memory.py
   ```

2. **📋 Extract Key Patterns**
   - Copy specific functions/classes
   - Note configuration patterns
   - Understand data flow

3. **🔧 Adapt for ILPA**
   - Modify for multi-agent architecture
   - Add ILPA-specific features
   - Update imports and dependencies

4. **✅ Validate Integration**
   - Test with existing F@4 patterns
   - Ensure compatibility
   - Maintain F@4 design principles

---

## 🎯 **Quick Reference Commands**

```bash
# View F@4 backend structure:
find fridays-at-four/src -name "*.py" | head -20

# View F@4 frontend structure:  
find FAF_website/app -name "*.tsx" | head -20

# Search for specific patterns:
grep -r "claude" fridays-at-four/src/
grep -r "useChat" FAF_website/app/

# Copy reference files to new location:
cp fridays-at-four/src/claude_client.py src/llm/providers/anthropic.py
```

---

## 💡 **Key Success Factors**

1. **🔍 Always Reference First** - Study F@4 files before implementing
2. **📝 Adapt, Don't Copy Blindly** - Understand the patterns, then adapt
3. **🧪 Test Early** - Validate F@4 patterns work in ILPA context
4. **📚 Document Changes** - Note what you modified and why
5. **🔄 Iterate** - Refine based on integration results

This guide ensures you leverage F@4 patterns effectively while building ILPA! 