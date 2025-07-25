<template>
  <div class="auth-container">
    <h2>Create Account</h2>

    <!-- Create Account Form -->
    <form @submit.prevent="register">
      <input v-model="name" type="text" placeholder="Full Name" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
      <button type="submit">Sign Up</button>
    </form>

    <!-- Link to log in page -->
    <div class="links">
      <button class="link-btn" @click="goToLoginPage">Already have an account? Log In</button>
    </div>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const message = ref('')

function goToLoginPage() {
  router.push('/login')
}

function register() {
  if (password.value !== confirmPassword.value) {
    message.value = 'Passwords do not match'
    return
  }
  message.value = `Account created for ${email.value} (demo only)`
}
</script>

<style scoped>
.auth-container {
  max-width: 360px;
  margin: 4rem auto;
  padding: 2rem;
  background: #e3f2fd;
  color: #000;
}
input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #1976d2;
  border-radius: 0;
}
button[type="submit"] {
  width: 100%;
  padding: 0.75rem;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 0;
}
.links {
  margin-top: 1rem;
  text-align: center;
}
.link-btn {
  background: none;
  border: none;
  color: #1976d2;
  font-size: 0.9rem;
  cursor: pointer;
  text-decoration: underline;
}
.message {
  margin-top: 1rem;
  color: #000;
  font-size: 0.9rem;
  text-align: center;
}
</style>
