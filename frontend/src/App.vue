<template>
  <div id="app">
    <Navigation />
    <Slider />
    <DashboardTiles/>
  </div>
</template>

<script>
import Navigation from './components/Navigation.vue'
import Slider from './components/Slider.vue'
import DashboardTile from "@/components/DashboardTiles.vue";

export default {
  components: {
    DashboardTiles,
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
