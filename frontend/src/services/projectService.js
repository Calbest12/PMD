// frontend/src/services/projectService.js
import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

class ProjectService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/projects`
  }

  async getProjects(filters = {}) {
    try {
      const params = new URLSearchParams()

      // Add filters to params
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
      console.error('Get projects error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch projects',
        results: []
      }
    }
  }

  async getProject(projectId) {
    try {
      const response = await axios.get(`${this.baseURL}/${projectId}/`)
      return { success: true, project: response.data }
    } catch (error) {
      console.error('Get project error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Project not found'
      }
    }
  }

  async createProject(projectData) {
    try {
      const response = await axios.post(`${this.baseURL}/`, projectData)
      return { success: true, project: response.data }
    } catch (error) {
      console.error('Create project error:', error)
      return {
        success: false,
        error: error.response?.data || 'Failed to create project'
      }
    }
  }

  async updateProject(projectId, projectData) {
    try {
      const response = await axios.patch(`${this.baseURL}/${projectId}/`, projectData)
      return { success: true, project: response.data }
    } catch (error) {
      console.error('Update project error:', error)
      return {
        success: false,
        error: error.response?.data || 'Failed to update project'
      }
    }
  }

  async deleteProject(projectId) {
    try {
      await axios.delete(`${this.baseURL}/${projectId}/`)
      return { success: true }
    } catch (error) {
      console.error('Delete project error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to delete project'
      }
    }
  }

  async addProjectMember(projectId, userId) {
    try {
      const response = await axios.post(`${this.baseURL}/${projectId}/add_member/`, {
        user_id: userId
      })
      return { success: true, message: response.data.message }
    } catch (error) {
      console.error('Add member error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to add member'
      }
    }
  }

  async removeProjectMember(projectId, userId) {
    try {
      const response = await axios.post(`${this.baseURL}/${projectId}/remove_member/`, {
        user_id: userId
      })
      return { success: true, message: response.data.message }
    } catch (error) {
      console.error('Remove member error:', error)
      return {
        success: false,
        error: error.response?.data?.error || 'Failed to remove member'
      }
    }
  }

  async getProjectAnalytics(projectId) {
    try {
      const response = await axios.get(`${this.baseURL}/${projectId}/analytics/`)
      return { success: true, analytics: response.data }
    } catch (error) {
      console.error('Get project analytics error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch analytics'
      }
    }
  }

  // Helper method to get teams for project assignment
  async getTeams() {
    try {
      const response = await axios.get(`${API_BASE_URL}/teams/`)
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get teams error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch teams',
        results: []
      }
    }
  }

  // Helper method to get users for project assignment
  async getUsers() {
    try {
      const response = await axios.get(`${API_BASE_URL}/users/`)
      return {
        success: true,
        results: response.data.results || response.data
      }
    } catch (error) {
      console.error('Get users error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to fetch users',
        results: []
      }
    }
  }
}

export default new ProjectService()
