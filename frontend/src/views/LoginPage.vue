<template>
  <div class="auth-container">
    <h2>Login</h2>
    <p class="subtitle">Sign in to your account</p>

    <form @submit.prevent="onSubmit">
      <!-- Email or Username -->
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter your email"
          required
          tabindex="1"
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
        />
      </div>

      <!-- Submit -->
      <button type="submit" tabindex="3">Continue</button>
    </form>

    <!-- Forgot Password link -->
    <p class="links">
      <router-link to="/forgot">Forgot Password?</router-link>
    </p>

    <!-- Sign-up link -->
    <p class="signup-text" tabindex="4">
      Don’t have an account?
      <router-link to="/signup">Sign up</router-link>
    </p>

    <!-- Optional status -->
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email    = ref('')
const password = ref('')
const message  = ref('')
const router   = useRouter()

function onSubmit() {
  message.value = ''
  // Basic front-end check
  if (!email.value || !password.value) {
    message.value = 'Both fields are required.'
    return
  }
  // For now, just redirect to the components for the dashboard
  router.push('/dashboard')
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
}
button:hover {
  background-color: #1565c0;
}
.links {
  margin: 0.5rem 0;
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
  color: #b00020;
}
</style>
