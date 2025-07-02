<template>
  <div id="app">
    <Navigation />
    <Slider />
  </div>
</template>

<script>
import Navigation from './components/Navigation.vue'
import Slider from './components/Slider.vue'

export default {
  components: {
    Navigation,
    Slider
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
