<template>
  <div class="auth-container">
    <h2>Forgot Password</h2>
    <div class="form-group">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        type="email"
        placeholder="Enter your email"
        @keyup.enter="sendLink"
        required
      />
    </div>
    <button @click="sendLink">Send Reset Link</button>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const email   = ref('')
const message = ref('')
function sendLink() { //can change this
  message.value = `If that email exists, you’ll get a reset link shortly.`
}
</script>


<style scoped>
.auth-container {
  max-width: 320px;
  margin: 4rem auto;
  padding: 2rem;
  background: #e3f2fd;
  border-radius: 8px;
  color: #000;
}
.form-group {
  margin-bottom: 1rem;
}
button {
  width: 100%;
  padding: 0.75rem;
  background-color: #1976d2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.message {
  margin-top: 1rem;
  color: #000;
  font-size: 0.9rem;
  text-align: center;
}
</style>
