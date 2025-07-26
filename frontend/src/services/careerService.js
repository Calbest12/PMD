// frontend/src/services/careerService.js
import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

class CareerService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/career-development`
  }

  async getCareerForms(filters = {}) {
    try {
      const params = new URLSearchParams()
      
      Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
          params.append(key, filters[key])
        }
      })

      const response = await axios.get(`${this.baseURL}/`, { params })
      return {
        success: true,
        results: response.data.results || response.data,
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous
      }
    } catch (error) {
      console.error('Get career forms error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch career forms',
        results: []
      }
    }
  }

  async getCareerForm(formId) {
    try {
      const response = await axios.get(`${this.baseURL}/${formId}/`)
      return { success: true, form: response.data }
    } catch (error) {
      console.error('Get career form error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Career form not found'
      }
    }
  }

  async createCareerForm(formData) {
    try {
      const response = await axios.post(`${this.baseURL}/`, formData)
      return { success: true, form: response.data }
    } catch (error) {
      console.error('Create career form error:', error)
      return {
        success: false,
        error: error.response?.data || 'Failed to create career form'
      }
    }
  }

  async updateCareerForm(formId, formData) {
    try {
      const response = await axios.patch(`${this.baseURL}/${formId}/`, formData)
      return { success: true, form: response.data }
    } catch (error) {
      console.error('Update career form error:', error)
      return {
        success: false,
        error: error.response?.data || 'Failed to update career form'
      }
    }
  }

  async deleteCareerForm(formId) {
    try {
      await axios.delete(`${this.baseURL}/${formId}/`)
      return { success: true }
    } catch (error) {
      console.error('Delete career form error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to delete career form'
      }
    }
  }

  async getUserCareerProgress(userId = null) {
    try {
      const params = userId ? { user: userId } : {}
      const response = await axios.get(`${this.baseURL}/progress/`, { params })
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get career progress error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch career progress'
      }
    }
  }

  async getSkillGapAnalysis(userId = null) {
    try {
      const params = userId ? { user: userId } : {}
      const response = await axios.get(`${this.baseURL}/skill-gap-analysis/`, { params })
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Get skill gap analysis error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch skill gap analysis'
      }
    }
  }

  async getCareerRecommendations(userId = null) {
    try {
      const params = userId ? { user: userId } : {}
      const response = await axios.get(`${this.baseURL}/recommendations/`, { params })
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get career recommendations error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch career recommendations',
        results: []
      }
    }
  }

  // Helper methods for data formatting
  formatCareerFormsForDisplay(forms) {
    return forms.map(form => ({
      ...form,
      progressPercentage: form.current_progress || 0,
      isOverdue: form.is_overdue,
      timeUntilDeadline: this.calculateTimeUntilDeadline(form.target_date),
      skillGap: this.calculateSkillGap(form.current_level, form.target_level)
    }))
  }

  calculateTimeUntilDeadline(targetDate) {
    const target = new Date(targetDate)
    const now = new Date()
    const diffTime = target - now
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays < 0) return 'Overdue'
    if (diffDays === 0) return 'Due today'
    if (diffDays === 1) return '1 day left'
    if (diffDays < 7) return `${diffDays} days left`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks left`
    return `${Math.floor(diffDays / 30)} months left`
  }

  calculateSkillGap(currentLevel, targetLevel) {
    const levels = ['beginner', 'intermediate', 'advanced', 'expert']
    const currentIndex = levels.indexOf(currentLevel)
    const targetIndex = levels.indexOf(targetLevel)
    return Math.max(0, targetIndex - currentIndex)
  }

  getSkillCategories() {
    return [
      { value: 'technical', label: 'Technical', color: '#3b82f6' },
      { value: 'management', label: 'Management', color: '#8b5cf6' },
      { value: 'communication', label: 'Communication', color: '#10b981' },
      { value: 'design', label: 'Design', color: '#f59e0b' },
      { value: 'analytics', label: 'Analytics', color: '#ef4444' }
    ]
  }

  getSkillLevels() {
    return [
      { value: 'beginner', label: 'Beginner', order: 1 },
      { value: 'intermediate', label: 'Intermediate', order: 2 },
      { value: 'advanced', label: 'Advanced', order: 3 },
      { value: 'expert', label: 'Expert', order: 4 }
    ]
  }

  getPriorityLevels() {
    return [
      { value: 'low', label: 'Low', color: '#6b7280' },
      { value: 'medium', label: 'Medium', color: '#f59e0b' },
      { value: 'high', label: 'High', color: '#ef4444' },
      { value: 'critical', label: 'Critical', color: '#dc2626' }
    ]
  }
}

export default new CareerService()