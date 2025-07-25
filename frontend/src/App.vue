<template>
  <div id="app">
    <!-- view these components if on a dashboard route -->
    <div v-if="isDashboardPage">
    <Navigation />
    <Slider @submit-feedback="updateScores" />
    <TeamAverageChart :scores="scores" />
    </div>
    <router-view/> <!-- current route  -->
  </div>
</template>

<script>
import Navigation from './components/Navigation.vue'
import Slider from './components/Slider.vue'
import TeamAverageChart from './components/TeamAverageChart.vue'

export default {
  components: {
    Navigation,
    Slider,
    TeamAverageChart,
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
  computed: {
  isDashboardPage() {
    // This reads the current URL from Vue Router
    // then returns true only on your dashboard routes
    const { path } = this.$route
    return ['/dashboard', '/limited-dashboard'].includes(path)
  }
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
