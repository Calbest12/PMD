<template>
  <div class="project-dashboard">
    <ProjectTile
      v-for="(project, index) in projectList"
      :key="index"
      :name="project.name"
      :status="project.status"
      :dueDate="project.dueDate"
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
        {
          name: "Q3 Strategy",
          status: "In Progress",
          dueDate: "2025-08-15"
        },
        {
          name: "AI Upgrade Pilot",
          status: "Planned",
          dueDate: "2025-09-01"
        },
        {
          name: "Casablanca Expansion",
          status: "Completed",
          dueDate: "2025-07-10"
        }
      ]
    };
  }
}
</script>

<style scoped>
.project-dashboard {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin: 40px auto;
}
</style>
