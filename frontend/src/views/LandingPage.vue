<template>
 <div>
   <EpmHeader />
  <div class="landing-container">
    <div class="overlay-box">
      <h1 class="main-title">Welcome to EPMG</h1>
      <p class="tagline">
        Project Management that develops<br />
        the People & the Organization
      </p>
      <div class="button-group">
        <router-link to="/signup" class="btn">Sign Up</router-link>
        <router-link to="/login" class="btn">Login</router-link>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import EpmHeader from '@/components/Header.vue'

export default {
  name: 'LandingPage',
  components: {
    EpmHeader
  }
}
</script>

<style scoped>
.landing-container {
  background: whitesmoke;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Montserrat', sans-serif;
}

.overlay-box {
  background-color: midnightblue;
  padding: 3rem;
  text-align: center;
  color: beige;
  max-width: 700px;
  width: 100%;
}

.main-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.tagline {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.btn {
  background-color: #f1d6ec;
  color: black;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border: none;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.3s ease;
}

.btn:hover {
  background-color: #e4c6dd;
}
</style>
