import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Brain, Calendar, Upload, Users, Briefcase, Heart } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Welcome to <span className="text-blue-600">ILPA</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            Your Integrated Life Planning Assistant - combining AI coaching with multi-domain planning 
            to help you achieve balance across health, business, creativity, travel, and relationships.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/auth/sign-up">
              <Button size="lg" className="px-8">
                Get Started
              </Button>
            </Link>
            <Link href="/auth/sign-in">
              <Button variant="outline" size="lg" className="px-8">
                Sign In
              </Button>
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          <Card>
            <CardHeader>
              <Brain className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle>AI Life Coach</CardTitle>
              <CardDescription>
                Daily conversations with your personal AI coach for reflection and guidance
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Calendar className="h-8 w-8 text-green-600 mb-2" />
              <CardTitle>Weekly Planning</CardTitle>
              <CardDescription>
                Integrated planning sessions that combine insights from all life domains
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Upload className="h-8 w-8 text-purple-600 mb-2" />
              <CardTitle>Domain Insights</CardTitle>
              <CardDescription>
                Upload files and get AI-powered insights across 5 specialized domains
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Heart className="h-8 w-8 text-red-600 mb-2" />
              <CardTitle>Health Tracking</CardTitle>
              <CardDescription>
                Monitor wellness, exercise, and mental health patterns
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Briefcase className="h-8 w-8 text-indigo-600 mb-2" />
              <CardTitle>Business Growth</CardTitle>
              <CardDescription>
                Track projects, goals, and professional development
              </CardDescription>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader>
              <Users className="h-8 w-8 text-orange-600 mb-2" />
              <CardTitle>Life Balance</CardTitle>
              <CardDescription>
                Creative pursuits, travel planning, and relationship management
              </CardDescription>
            </CardHeader>
          </Card>
        </div>

        {/* How It Works */}
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
            How It Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 dark:bg-blue-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-blue-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Daily Conversations</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Chat with your AI life coach about your day, challenges, and goals
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 dark:bg-green-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Upload & Analyze</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Share files across health, business, creative, travel, and relationship domains
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 dark:bg-purple-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-purple-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Integrated Planning</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Weekly planning sessions that create balanced, actionable plans
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}