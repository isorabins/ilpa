import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export type Database = {
  public: {
    Tables: {
      conversations: {
        Row: {
          id: string
          user_id: string
          agent_type: string
          message_type: string
          content: string
          timestamp: string
          session_id: string | null
          metadata: any
        }
        Insert: {
          id?: string
          user_id: string
          agent_type?: string
          message_type: string
          content: string
          timestamp?: string
          session_id?: string | null
          metadata?: any
        }
        Update: {
          id?: string
          user_id?: string
          agent_type?: string
          message_type?: string
          content?: string
          timestamp?: string
          session_id?: string | null
          metadata?: any
        }
      }
      weekly_plans: {
        Row: {
          id: string
          user_id: string
          week_of: string
          session_id: string | null
          plan_content: any
          completion_data: any
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          week_of: string
          session_id?: string | null
          plan_content?: any
          completion_data?: any
          created_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          week_of?: string
          session_id?: string | null
          plan_content?: any
          completion_data?: any
          created_at?: string
        }
      }
      user_preferences: {
        Row: {
          id: string
          user_id: string
          preferences: any
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          user_id: string
          preferences?: any
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          user_id?: string
          preferences?: any
          created_at?: string
          updated_at?: string
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
  }
}