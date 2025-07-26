import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

class AuthService {
  constructor() {
    this.baseURL = API_BASE_URL
    this.setupInterceptors()
  }

  setupInterceptors() {
    // Add auth token to requests
    axios.interceptors.request.use(
      config => {
        const token = this.getToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      error => Promise.reject(error)
    )

    // Handle token expiration
    axios.interceptors.response.use(
      response => response,
      async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            const newToken = await this.refreshToken()
            originalRequest.headers.Authorization = `Bearer ${newToken}`
            return axios(originalRequest)
          } catch (refreshError) {
            this.logout()
            window.location.href = '/login'
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  async login(email, password) {
    try {
      const response = await axios.post(`${this.baseURL}/auth/login/`, {
        email,
        password
      })

      const { access, refresh, user } = response.data

      // Store tokens and user data
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user_data', JSON.stringify(user))
      localStorage.setItem('isAuthenticated', 'true')

      return { success: true, user }
    } catch (error) {
      console.error('Login error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || error.response?.data?.non_field_errors?.[0] || 'Login failed'
      }
    }
  }

  async register(userData) {
    try {
      const response = await axios.post(`${this.baseURL}/auth/register/`, userData)

      // Auto-login after registration
      if (response.data.access) {
        const { access, refresh, user } = response.data
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user_data', JSON.stringify(user))
        localStorage.setItem('isAuthenticated', 'true')
        return { success: true, user }
      }

      return { success: true, data: response.data }
    } catch (error) {
      console.error('Registration error:', error)
      return {
        success: false,
        error: error.response?.data || 'Registration failed'
      }
    }
  }

  async logout() {
    try {
      const refreshToken = this.getRefreshToken()
      if (refreshToken) {
        // Note: Your backend doesn't have a logout endpoint yet
        // await axios.post(`${this.baseURL}/auth/logout/`, {
        //   refresh: refreshToken
        // })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local storage regardless
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_data')
      localStorage.removeItem('isAuthenticated')
    }
  }

  async forgotPassword(email) {
    try {
      const response = await axios.post(`${this.baseURL}/auth/forgot-password/`, {
        email
      })
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Forgot password error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to send reset email'
      }
    }
  }

  async resetPassword(newPassword) {
    try {
      const response = await axios.post(`${this.baseURL}/auth/reset-password/`, {
        new_password: newPassword
      })
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Reset password error:', error)
      return {
        success: false,
        error: error.response?.data?.detail || 'Password reset failed'
      }
    }
  }

  getToken() {
    return localStorage.getItem('access_token')
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token')
  }

  getCurrentUser() {
    const userData = localStorage.getItem('user_data')
    return userData ? JSON.parse(userData) : null
  }

  isAuthenticated() {
    return localStorage.getItem('isAuthenticated') === 'true' && this.getToken()
  }

  async refreshToken() {
    try {
      const refreshToken = this.getRefreshToken()
      if (!refreshToken) throw new Error('No refresh token')

      const response = await axios.post(`${this.baseURL}/auth/refresh/`, {
        refresh: refreshToken
      })

      const { access } = response.data
      localStorage.setItem('access_token', access)

      return access
    } catch (error) {
      console.error('Token refresh error:', error)
      this.logout()
      throw error
    }
  }

  async getCurrentUserProfile() {
    try {
      const response = await axios.get(`${this.baseURL}/users/me/`)
      return { success: true, user: response.data }
    } catch (error) {
      console.error('Get user profile error:', error)
      return { success: false, error: error.response?.data }
    }
  }
}

export default new AuthService()