<template>
  <header class="navbar">
    <nav class="navbar-container">
      <!-- Logo -->
      <div class="navbar-logo">Enhanced Project Management</div>

      <!-- Navigation Menu -->
      <ul class="navbar-menu">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/dashboard">Dashboard</router-link></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#about">About</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'EpmHeader'
}
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo {
  font-size: 1.25rem;
  font-weight: bold;
  color: #1a237e; /* navy-blue */
}

.navbar-menu {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.navbar-menu a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s;
}

.navbar-menu a:hover {
  color: #1a237e;
}
</style>
