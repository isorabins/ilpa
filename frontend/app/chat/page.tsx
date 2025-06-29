'use client'

import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { useToast } from '@/hooks/use-toast'
import { Send, Menu, X, User, LogOut, MessageSquare, RefreshCcw, Brain, Calendar, Heart, Briefcase, Users } from 'lucide-react'

// API Configuration
const API_BASE = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000';

// Types
interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: string
}

interface Thread {
  thread_id: string
  messages: Message[]
  last_message_time: string
  message_count: number
}

// API Client
class ILPAAPI {
  async sendMessage(userId: string, threadId: string, message: string): Promise<{ response: string; thread_id: string }> {
    const response = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        thread_id: threadId,
        message: message
      })
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  }
}

// Helper function to generate a thread ID
const generateThreadId = () => {
  return `thread_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

export default function Chat() {
  const router = useRouter()
  const { toast } = useToast()
  const api = new ILPAAPI()
  
  // Mock user for now - will integrate with real auth later
  const user = { id: 'demo-user', email: 'demo@example.com' }
  
  // UI State
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [sending, setSending] = useState(false)
  const [input, setInput] = useState("")
  const [hasTyped, setHasTyped] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  
  // Chat State
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Hello! I'm your AI Life Coach. How are you feeling today? What's on your mind?",
      timestamp: new Date().toISOString(),
    },
  ])
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim() || sending) return

    const threadId = currentThreadId || generateThreadId();
    if (!currentThreadId) {
      setCurrentThreadId(threadId);
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    const currentInput = input
    setInput("")
    setSending(true)
    setIsStreaming(true)
    
    try {
      // For now, simulate a response until backend is connected
      setTimeout(() => {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: "Thank you for sharing that with me. I'm here to help you reflect on your experiences and work toward your goals. Can you tell me more about what's been on your mind lately? (This is a demo response - backend connection coming soon!)",
          role: "assistant",
          timestamp: new Date().toISOString(),
        }
        setMessages(prev => [...prev, assistantMessage])
        setIsStreaming(false)
        setSending(false)
      }, 1500)
    } catch (error) {
      console.error('Failed to send message:', error)
      toast({
        title: "Error",
        description: "Failed to get a response. Please try again.",
      })
      setSending(false)
      setIsStreaming(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (isStreaming) return

    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value
    setInput(value)
    
    if (value.trim()) {
      setHasTyped(true)
    } else {
      setHasTyped(false)
    }
    
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar - F@4 Style */}
      <div className={`${sidebarCollapsed ? "w-16" : "w-80"} bg-amber-50 border-r border-amber-200 transition-all duration-300 flex-shrink-0`}>
        {/* Sidebar Header */}
        <div className="flex items-center justify-between p-4 border-b border-amber-200">
          {!sidebarCollapsed && (
            <h2 className="font-medium text-gray-900">ILPA Life Coach</h2>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          >
            {sidebarCollapsed ? <Menu className="h-4 w-4" /> : <X className="h-4 w-4" />}
          </Button>
        </div>

        {!sidebarCollapsed && (
          <>
            {/* Life Domains Status */}
            <div className="p-4 border-b border-amber-200">
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-gray-800">Life Domains</h3>
                
                <Card className="bg-white border-amber-200">
                  <CardContent className="p-3">
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Heart className="h-4 w-4 text-red-600" />
                          <span className="text-sm">Health</span>
                        </div>
                        <span className="text-xs text-gray-600">Active</span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Briefcase className="h-4 w-4 text-blue-600" />
                          <span className="text-sm">Business</span>
                        </div>
                        <span className="text-xs text-gray-600">Planning</span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Brain className="h-4 w-4 text-purple-600" />
                          <span className="text-sm">Creative</span>
                        </div>
                        <span className="text-xs text-gray-600">Ideas</span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Users className="h-4 w-4 text-green-600" />
                          <span className="text-sm">Relationships</span>
                        </div>
                        <span className="text-xs text-gray-600">Growing</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Conversation Context */}
            <div className="flex-1 p-4">
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-gray-800">Today's Conversation</h3>
                <Card className="bg-amber-25 border-amber-200">
                  <CardContent className="p-3">
                    <div className="space-y-2">
                      <p className="text-xs text-gray-700">Ongoing conversation</p>
                      <p className="text-xs text-gray-900">
                        Your AI Life Coach remembers your goals, challenges, and progress. 
                        Continue where you left off.
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* User Menu */}
            <div className="p-4 border-t border-amber-200">
              <Button
                variant="ghost"
                className="w-full justify-start"
                onClick={() => {
                  toast({ title: "Demo Mode", description: "Sign out functionality coming soon!" })
                }}
              >
                <LogOut className="h-4 w-4 mr-2" />
                <span className="text-sm">Sign Out</span>
              </Button>
            </div>
          </>
        )}

        {/* Collapsed Sidebar Content */}
        {sidebarCollapsed && (
          <div className="flex flex-col items-center space-y-4 p-2 mt-4">
            <Button variant="ghost" size="sm">
              <User className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1 h-screen">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-300 bg-white">
          <div /> {/* Spacer */}
          <h1 className="font-medium text-gray-900">Chat with Your Life Coach</h1>
          <Button variant="outline" size="sm">
            <MessageSquare className="h-4 w-4 mr-2" />
            Help
          </Button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          <div className="max-w-3xl mx-auto">
            {messages.map((message) => (
              <div key={message.id} className="mb-8">
                {message.role === "assistant" ? (
                  // AI Message - Left-aligned like F@4
                  <div className="flex items-start gap-3">
                    <Avatar className="h-8 w-8 bg-blue-600 flex-shrink-0">
                      <AvatarFallback className="text-white text-sm">AI</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 max-w-2xl">
                      <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">
                        {message.content}
                        {isStreaming && message.id === messages[messages.length - 1]?.id && (
                          <span className="inline-block w-2 h-5 bg-blue-600 ml-1 animate-pulse">|</span>
                        )}
                      </p>
                    </div>
                  </div>
                ) : (
                  // User Message - Right-aligned bubble like F@4
                  <div className="flex justify-end mb-2">
                    <div className="bg-white border border-gray-300 rounded-2xl px-4 py-3 max-w-xl shadow-sm">
                      <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">
                        {message.content}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area - F@4 Style */}
        <div className="p-6 bg-white border-t border-gray-300">
          <div className="max-w-3xl mx-auto">
            <div className="max-w-2xl mx-auto bg-white border border-gray-400 rounded-3xl p-1 shadow-lg">
              <div className="flex items-end gap-2">
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={handleInputChange}
                  onKeyDown={handleKeyDown}
                  placeholder="Message your Life Coach..."
                  rows={1}
                  disabled={isStreaming}
                  className="flex-1 resize-none border-none outline-none bg-transparent px-4 py-3 min-h-[44px] max-h-[200px] text-gray-900 placeholder-gray-500"
                />
                <Button
                  onClick={handleSendMessage}
                  size="sm"
                  disabled={!hasTyped || isStreaming}
                  className={`rounded-full min-w-[36px] h-9 p-0 mr-1 mb-1 transition-all ${
                    hasTyped && !isStreaming 
                      ? "bg-gray-900 hover:bg-gray-800 text-white" 
                      : "bg-gray-300 text-gray-600"
                  }`}
                >
                  {isStreaming ? (
                    <RefreshCcw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
            
            {/* Disclaimer */}
            <p className="text-xs text-gray-600 text-center mt-3 max-w-lg mx-auto">
              Your AI Life Coach can make mistakes. Please use your best judgment.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}