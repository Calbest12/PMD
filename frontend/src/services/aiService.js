// frontend/src/services/aiService.js
import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

class AIService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/ai`
  }

  async getInsights(filters = {}) {
    try {
      const params = new URLSearchParams()
      
      Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
          params.append(key, filters[key])
        }
      })

      const response = await axios.get(`${this.baseURL}/insights/`, { params })
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get AI insights error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch insights',
        results: []
      }
    }
  }

  async getInsight(insightId) {
    try {
      const response = await axios.get(`${this.baseURL}/insights/${insightId}/`)
      return { success: true, insight: response.data }
    } catch (error) {
      console.error('Get insight error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Insight not found'
      }
    }
  }

  async applyInsight(insightId) {
    try {
      const response = await axios.post(`${this.baseURL}/insights/${insightId}/apply/`)
      return { success: true, message: response.data.message }
    } catch (error) {
      console.error('Apply insight error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to apply insight'
      }
    }
  }

  async dismissInsight(insightId) {
    try {
      const response = await axios.post(`${this.baseURL}/insights/${insightId}/dismiss/`)
      return { success: true, message: response.data.message }
    } catch (error) {
      console.error('Dismiss insight error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to dismiss insight'
      }
    }
  }

  async sendChatMessage(message, context = {}) {
    try {
      const response = await axios.post(`${this.baseURL}/chat/`, {
        message,
        context
      })
      return { 
        success: true, 
        response: response.data.response,
        timestamp: response.data.timestamp
      }
    } catch (error) {
      console.error('AI Chat error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'AI service temporarily unavailable'
      }
    }
  }

  async getChatHistory(limit = 20) {
    try {
      const response = await axios.get(`${this.baseURL}/chat/history/`, {
        params: { limit }
      })
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get chat history error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch chat history',
        results: []
      }
    }
  }

  async uploadTrainingData(data) {
    try {
      const response = await axios.post(`${this.baseURL}/training-data/`, data)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Upload training data error:', error)
      return {
        success: false,
        error: error.response?.data || 'Failed to upload training data'
      }
    }
  }

  async getTrainingDataStatus() {
    try {
      const response = await axios.get(`${this.baseURL}/training-data/`)
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get training data status error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch training data status',
        results: []
      }
    }
  }

  // Helper method to format insights for display
  formatInsightsForDisplay(insights) {
    return insights.map(insight => ({
      ...insight,
      confidencePercentage: Math.round(insight.confidence_score * 100),
      timeAgo: this.formatTimeAgo(insight.created_at),
      typeColor: this.getInsightTypeColor(insight.insight_type)
    }))
  }

  getInsightTypeColor(type) {
    const colors = {
      feedback: '#10b981',
      suggestion: '#f59e0b',
      recommendation: '#3b82f6',
      performance: '#8b5cf6',
      risk: '#ef4444',
      opportunity: '#06b6d4',
      trend: '#84cc16'
    }
    return colors[type] || '#6b7280'
  }

  formatTimeAgo(dateString) {
    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 1) return '1 day ago'
    if (diffDays < 7) return `${diffDays} days ago`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
    return `${Math.floor(diffDays / 30)} months ago`
  }
}

export default new AIService()