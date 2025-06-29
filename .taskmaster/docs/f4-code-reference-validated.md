# F@4 Code Reference Guide - Research Validated

## 🔬 **Research-Validated Best Practices (2024)**

This guide combines actual F@4 codebase patterns with current industry best practices to ensure your ILPA implementation is robust and modern.

---

## ✅ **F@4 Pattern Validation Results**

### **✅ Confirmed F@4 Files & Patterns**
```bash
# ACTUAL F@4 Files (Validated):
fridays-at-four/src/simple_memory.py           ✅ Memory management core
fridays-at-four/src/claude_client_simple.py    ✅ Claude API integration  
fridays-at-four/src/main.py                    ✅ FastAPI application setup
fridays-at-four/src/llm_router.py              ✅ LLM routing logic
fridays-at-four/src/config.py                  ✅ Configuration patterns

# NON-EXISTENT Files (Updated):
fridays-at-four/src/database.py                ❌ DOESN'T EXIST
fridays-at-four/src/claude_client.py           ❌ DOESN'T EXIST
```

### **🔧 Corrected File References**
```bash
# Task 2: Base Agent & LLM Router - CORRECTED
fridays-at-four/src/claude_client_simple.py    # Claude API patterns
fridays-at-four/src/llm_router.py              # LLM routing logic
fridays-at-four/src/main.py                    # FastAPI + streaming

# Task 3: Database Client & Models - CORRECTED  
fridays-at-four/src/simple_memory.py           # Supabase client usage
fridays-at-four/supabase/schema.sql            # Schema reference
```

---

## 🏗️ **Backend Implementation Guide (Research-Validated)**

### **Task 2: Base Agent & LLM Router**

**✅ F@4 Patterns to Copy:**
```python
# From fridays-at-four/src/claude_client_simple.py (lines 1-106)
class SimpleClaudeClient:
    def __init__(self, credentials: ClaudeCredentials):
        self.client = AsyncAnthropic(api_key=credentials.api_key)
    
    async def send_message(self, messages, stream=False):
        if stream:
            return self._stream_message(messages, model, max_tokens, temperature)
        else:
            message = await self.client.messages.create(...)
            return message.content[0].text
```

**✅ 2024 Best Practices Applied:**
- ✅ Use `AsyncAnthropic` client (official Anthropic SDK)
- ✅ Implement streaming with `async for text in stream.text_stream`
- ✅ Use `aiohttp` patterns for async HTTP calls
- ✅ Implement exponential backoff for rate limiting

**🔧 ILPA Implementation:**
```python
# src/llm/providers/anthropic.py
class AnthropicProvider(BaseProvider):
    def __init__(self):
        self.client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    async def send_message(self, messages: List[Dict], stream: bool = False):
        # Copy F@4 streaming pattern exactly
        if stream:
            return self._stream_message(messages)
        # ... rest from F@4 claude_client_simple.py
```

---

### **Task 3: Database Client & Models**

**❌ F@4 Database File Missing - Use Research Best Practices:**

**✅ 2024 Best Practices (Research-Validated):**
```python
# src/database/client.py - NEW IMPLEMENTATION
import asyncpg
from fastapi import FastAPI

class DatabaseClient:
    def __init__(self):
        self.pool = None
    
    async def startup(self):
        # Use Supabase direct connection (research-validated)
        self.pool = await asyncpg.create_pool(
            dsn="postgresql://user:password@host:port/dbname"
        )
    
    async def get_connection(self):
        async with self.pool.acquire() as connection:
            yield connection
```

**✅ F@4 Pattern Reference:**
```python
# From fridays-at-four/src/simple_memory.py (lines 25-50)
def __init__(self, supabase_client, user_id: str, buffer_size: int = 100):
    self.supabase = supabase_client
    self.user_id = user_id
    
# User filtering pattern (lines 85-95):
memory_data = {
    'user_id': self.user_id,  # Always filter by user_id
    'memory_type': 'message',
    'content': formatted_content,
}
```

---

### **Task 16: F@4 Memory System (CRITICAL)**

**✅ Direct F@4 Pattern Copy:**
```python
# From fridays-at-four/src/simple_memory.py (lines 1-334)
class SimpleMemory:
    def __init__(self, supabase_client, user_id: str, buffer_size: int = 100):
        self.supabase = supabase_client
        self.user_id = user_id
        self.buffer_size = buffer_size
    
    async def add_message(self, thread_id: str, message: str, role: str):
        # Deduplication logic (lines 70-85)
        message_hash = self._generate_message_hash(thread_id, formatted_content, role)
        if await self._is_message_duplicate(message_hash, thread_id, formatted_content):
            return
            
        # Storage pattern (lines 95-110)
        memory_data = {
            'user_id': self.user_id,
            'memory_type': 'message', 
            'content': f"{role}: {sanitized_message}",
            'metadata': {'thread_id': thread_id, 'message_hash': message_hash}
        }
        self.supabase.table('memory').insert(memory_data).execute()
```

**✅ 2024 Best Practices Validation:**
- ✅ Message deduplication with hashing (F@4 pattern validated)
- ✅ Rolling buffer with configurable size (F@4: 100 messages)
- ✅ User-scoped memory isolation (F@4: user_id filtering)
- ✅ Async background summarization (F@4: asyncio.create_task)

---

## 🌐 **Frontend Implementation Guide (Research-Validated)**

### **Task 11: Chat Interface**

**✅ 2024 Best Practices (Research-Validated):**
```typescript
// app/components/chat/ChatInterface.tsx
import { useState, useEffect } from 'react'
import { useChat } from '../hooks/useChat'

export default function ChatInterface() {
  const { messages, sendMessage, isStreaming } = useChat()
  
  // Streaming response handling (2024 best practice)
  useEffect(() => {
    if (isStreaming) {
      // Update UI in real-time as tokens arrive
    }
  }, [isStreaming])
}

// hooks/useChat.ts - WebSocket + SSE for streaming
export function useChat() {
  const [messages, setMessages] = useState([])
  
  const sendMessage = async (content: string) => {
    // Optimistic UI update (2024 best practice)
    setMessages(prev => [...prev, { role: 'user', content }])
    
    // Stream response from FastAPI
    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: content, stream: true })
    })
    
    const reader = response.body?.getReader()
    // Process streaming tokens...
  }
}
```

### **Task 14: Frontend Authentication**

**✅ 2024 Best Practices (Research-Validated):**
```typescript
// app/hooks/useAuth.ts
export function useAuth() {
  // Use httpOnly cookies for JWT (2024 security best practice)
  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      credentials: 'include', // Send httpOnly cookies
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
  }
}

// middleware.ts - Route protection
export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}
```

---

## 🔄 **Implementation Strategy (Research-Optimized)**

### **1. Direct Copy (Minimal Changes)**
```bash
# These F@4 patterns are current and can be copied directly:
fridays-at-four/src/claude_client_simple.py    → src/llm/providers/anthropic.py
fridays-at-four/src/simple_memory.py           → src/memory/memory_manager.py (adapt)
fridays-at-four/src/config.py                  → src/config.py
```

### **2. Research-Enhanced Patterns**
```bash
# Use F@4 as reference + 2024 best practices:
Database Client    → Use asyncpg + connection pooling (research-guided)
FastAPI Setup     → Copy F@4 main.py + add 2024 CORS/middleware patterns
Frontend Auth     → httpOnly cookies + Next.js 14 middleware (research-guided)
```

### **3. New Implementations (Research-Guided)**
```bash
# No F@4 equivalent - use 2024 best practices:
Multi-agent routing    → Research patterns for agent isolation
File upload system     → Research patterns for async file processing
Planning interface     → Research patterns for drag-and-drop + state management
```

---

## 🎯 **Validation Checklist**

### **✅ F@4 Pattern Accuracy**
- ✅ Memory system uses exact F@4 deduplication logic
- ✅ Claude client uses official Anthropic SDK (validated)
- ✅ FastAPI setup follows F@4 CORS and middleware patterns
- ✅ User filtering applied everywhere (F@4 security pattern)

### **✅ 2024 Best Practices**
- ✅ AsyncAnthropic client for Claude API
- ✅ Supabase direct connection with asyncpg
- ✅ httpOnly cookies for JWT security
- ✅ WebSocket + SSE for real-time features
- ✅ React 18+ patterns with Zustand/Context

### **✅ ILPA-Specific Enhancements**
- ✅ Multi-agent memory isolation
- ✅ Domain-specific file processing
- ✅ Weekly planning interface
- ✅ Streaming chat with life coach agent

---

## 🚀 **Implementation Commands**

```bash
# 1. Study F@4 patterns first:
cat fridays-at-four/src/simple_memory.py        # Memory patterns
cat fridays-at-four/src/claude_client_simple.py # Claude integration
cat fridays-at-four/src/main.py | head -100     # FastAPI setup

# 2. Copy validated patterns:
cp fridays-at-four/src/claude_client_simple.py src/llm/providers/anthropic.py

# 3. Search for specific patterns:
grep -r "user_id" fridays-at-four/src/          # User filtering patterns
grep -r "stream" fridays-at-four/src/           # Streaming patterns
```

This guide ensures you leverage proven F@4 patterns while implementing current 2024 best practices for a robust, scalable ILPA system! 