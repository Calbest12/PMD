<template>
  <div class="auth-container">
    <h2>Login</h2>
    <p class="subtitle">Sign in to your account</p>

    <form @submit.prevent="onSubmit">
      <!-- Email -->
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter your email"
          required
          tabindex="1"
          :disabled="loading"
        />
      </div>

      <!-- Password -->
      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Enter your password"
          required
          tabindex="2"
          :disabled="loading"
        />
      </div>

      <!-- Submit -->
      <button type="submit" tabindex="3" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Continue' }}
      </button>
    </form>

    <!-- Forgot Password link -->
    <p class="links">
      <router-link to="/forgot">Forgot Password?</router-link>
    </p>

    <!-- Sign-up link -->
    <p class="signup-text" tabindex="4">
      Don't have an account?
      <router-link to="/signup">Sign up</router-link>
    </p>

    <!-- Status message -->
    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      message: '',
      messageClass: 'message',
      loading: false
    }
  },
  async mounted() {
    // Check if user is already authenticated
    if (this.$authService.isAuthenticated()) {
      this.$router.push('/dashboard')
    }
  },
  methods: {
    async onSubmit() {
      this.message = ''
      this.loading = true

      // Basic validation
      if (!this.email || !this.password) {
        this.showError('Both email and password are required.')
        this.loading = false
        return
      }

      try {
        const result = await this.$authService.login(this.email, this.password)

        if (result.success) {
          this.showSuccess('Login successful! Redirecting...')

          // Emit login success event to parent App component
          this.$emit('login-success', result.user)

          // Wait a moment then redirect
          setTimeout(() => {
            this.$router.push('/dashboard')
          }, 1000)
        } else {
          this.showError(result.error)
        }
      } catch (error) {
        console.error('Login error:', error)
        this.showError('An unexpected error occurred. Please try again.')
      } finally {
        this.loading = false
      }
    },

    showError(message) {
      this.message = message
      this.messageClass = 'message error'
    },

    showSuccess(message) {
      this.message = message
      this.messageClass = 'message success'
    }
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 360px;
  margin: 4rem auto;
  padding: 2rem;
  background: #e3f2fd;
  border-radius: 8px;
  color: #000;
  text-align: center;
}

.subtitle {
  margin-bottom: 1rem;
  font-size: 0.95rem;
  color: #555;
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 0.25rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #1976d2;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1rem;
}

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

input:focus {
  outline: none;
  border-color: #1565c0;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #1976d2;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover:not(:disabled) {
  background-color: #1565c0;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.links {
  margin: 0.5rem 0;
}

.links a {
  color: #1976d2;
  text-decoration: none;
}

.links a:hover {
  text-decoration: underline;
}

.signup-text {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #000;
}

.signup-text a {
  color: #1976d2;
  text-decoration: none;
}

.signup-text a:hover {
  text-decoration: underline;
}

.message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
}

.message.error {
  background-color: #ffebee;
  color: #c62828;
  border: 1px solid #ffcdd2;
}

.message.success {
  background-color: #e8f5e8;
  color: #2e7d32;
  border: 1px solid #c8e6c9;
}
</style>