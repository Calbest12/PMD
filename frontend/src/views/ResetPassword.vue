<template>
  <div class="auth-container">
    <h2>Reset Password</h2>

    <!-- New Password field -->
    <div class="form-group">
      <label for="newPassword">New Password</label>
      <input
        id="newPassword"
        v-model="newPassword"
        type="password"
        placeholder="Enter new password"
        @keyup.enter="onSubmit"
        tabindex="1"
        required
      />
    </div>

    <!-- Confirm Password field -->
    <div class="form-group">
      <label for="confirmPassword">Confirm Password</label>
      <input
        id="confirmPassword"
        v-model="confirmPassword"
        type="password"
        placeholder="Re‑enter new password"
        @keyup.enter="onSubmit"
        tabindex="2"
        required
      />
    </div>

    <!-- Show mismatch warning -->
    <p v-if="confirmPassword && !passwordsMatch" class="error">
      Passwords do not match.
    </p>

    <!-- Submit button is disabled until passwordsMatch -->
    <button
      @click="onSubmit"
      :disabled="!passwordsMatch || !newPassword"
      tabindex="3"
    >
      Reset Password
    </button>

    <!-- Feedback message -->
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const newPassword     = ref('')
const confirmPassword = ref('')
const message         = ref('')
const router          = useRouter()

// check two fields match?????
const passwordsMatch = computed(
  () => newPassword.value && newPassword.value === confirmPassword.value
)

function onSubmit() {
  message.value = ''

  // first validation
  if (!newPassword.value || !confirmPassword.value) {
    message.value = 'Both fields are required.'
    return
  }
  if (!passwordsMatch.value) {
    message.value = 'Passwords do not match.'
    return
  }

  // for backend stuff???
  // await axios.post('/api/password/reset', { new_password: newPassword.value })

  // simulate success
  message.value = 'Your password has been reset!'

  // redirect back to log in
  setTimeout(() => router.push('/'), 1500)
}
</script>

<style scoped>
.auth-container {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  max-width: 320px; width: 90%;
  padding: 2rem;
  background: #e3f2fd;
  border-radius: 8px;
  color: #000;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.25rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #b0bec5;
  border-radius: 4px;
}
.error {
  color: #b00020;
  font-size: 0.9rem;
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
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
button:focus:not(:disabled) {
  outline: 2px solid #1565c0;
}
.message {
  margin-top: 1rem;
  font-size: 0.9rem;
  text-align: center;
}
</style>
