// frontend/src/services/feedbackService.js
import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

class FeedbackService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/feedback`
  }

  async submitSliderFeedback(feedbackData) {
    try {
      const response = await axios.post(`${this.baseURL}/slider/`, feedbackData)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Submit feedback error:', error)
      return {
        success: false,
        error: error.response?.data?.error || error.response?.data?.detail || 'Failed to submit feedback'
      }
    }
  }

  async getSliderFeedback(projectId = null) {
    try {
      const params = projectId ? { project: projectId } : {}
      const response = await axios.get(`${this.baseURL}/slider/`, { params })
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get slider feedback error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch feedback',
        results: []
      }
    }
  }

  async getPerformanceMetrics(projectId = null) {
    try {
      const params = projectId ? { project: projectId } : {}
      const response = await axios.get(`${this.baseURL}/metrics/`, { params })
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get performance metrics error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch metrics',
        results: []
      }
    }
  }

  async updatePerformanceMetric(metricData) {
    try {
      const response = await axios.post(`${this.baseURL}/metrics/`, metricData)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Update performance metric error:', error)
      return {
        success: false,
        error: error.response?.data || 'Failed to update metric'
      }
    }
  }

  async getDashboardAnalytics() {
    try {
      const response = await axios.get(`${API_BASE_URL}/dashboard/analytics/`)
      return { success: true, ...response.data }
    } catch (error) {
      console.error('Get dashboard analytics error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch analytics',
        total_projects: 0,
        active_projects: 0,
        completed_projects: 0,
        overdue_projects: 0,
        completion_rate: 0,
        average_scores: {
          PM: 0,
          Leadership: 0,
          ChangeMgmt: 0
        },
        recent_insights: []
      }
    }
  }

  async getUserFeedbackHistory(userId = null) {
    try {
      const params = userId ? { user: userId } : {}
      const response = await axios.get(`${this.baseURL}/slider/`, { params })
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get user feedback history error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch feedback history',
        results: []
      }
    }
  }

  async getTeamAnalytics(teamId = null) {
    try {
      const params = teamId ? { team: teamId } : {}
      const response = await axios.get(`${this.baseURL}/team-analytics/`, { params })
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get team analytics error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch team analytics'
      }
    }
  }

  // Helper method to format scores for charts
  formatScoresForChart(feedbackData) {
    const scores = {
      projectManagement: 0,
      leadership: 0,
      organizationalChange: 0
    }

    const categoryCounts = {
      PM: 0,
      Leadership: 0,
      ChangeMgmt: 0
    }

    // Calculate averages
    feedbackData.forEach(feedback => {
      if (feedback.category === 'PM') {
        scores.projectManagement += feedback.score
        categoryCounts.PM++
      } else if (feedback.category === 'Leadership') {
        scores.leadership += feedback.score
        categoryCounts.Leadership++
      } else if (feedback.category === 'ChangeMgmt') {
        scores.organizationalChange += feedback.score
        categoryCounts.ChangeMgmt++
      }
    })

    // Calculate averages
    scores.projectManagement = categoryCounts.PM > 0 ? scores.projectManagement / categoryCounts.PM : 0
    scores.leadership = categoryCounts.Leadership > 0 ? scores.leadership / categoryCounts.Leadership : 0
    scores.organizationalChange = categoryCounts.ChangeMgmt > 0 ? scores.organizationalChange / categoryCounts.ChangeMgmt : 0

    return scores
  }
}

export default new FeedbackService()