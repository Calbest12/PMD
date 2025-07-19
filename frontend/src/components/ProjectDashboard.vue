<template>
  <div class="project-dashboard">
    <ProjectTile
      v-for="(project, index) in projectList"
      :key="index"
      :title="project.title"
      :description="project.description"
    />
  </div>
</template>

<script>
import ProjectTile from './ProjectTile.vue'

export default {
  name: "ProjectDashboard",
  components: {
    ProjectTile
  },
  data() {
    return {
      projectList: [
        { title: "Q3 Strategy", description: "Team-wide goals for the quarter" },
        { title: "AI Upgrade Pilot", description: "Evaluating new leadership features" }
      ]
    }
  }
}
</script>

<style scoped>
.project-dashboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 700px;
  margin: 40px auto;
}
</style>
