<template>
  <div id="app">
    <Navigation />
    <Slider />
  </div>
</template>

<script>
import Navigation from './components/Navigation.vue'
import Slider from './components/Slider.vue'
import TeamAverageChart from './components/TeamAverageChart.vue'
import ProjectDashboard from './components/ProjectDashboard.vue'

export default {
  components: {
    Navigation,
    Slider,
    TeamAverageChart,
    ProjectDashboard
  },
  data() {
    return {
      scores: {
        projectManagement: 4,
        leadership: 4,
        organizationalChange: 4
      }
    };
  },
  methods: {
    updateScores(newScores) {
      this.scores = { ...newScores };
    }
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
