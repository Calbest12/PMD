<template>
  <div class="project-dashboard">

  //Form for adding project tiles, so they are dynamically displayed.
  <form @submit.prevent="addProject" class="project-form">
   <input v-model="newProject.name" placeholder="Project Name" required />
   <select v-model="newProject.status" required>
    <option disabled value="">Select Status</option>
    <option>Planned</option>
    <option>In Progress</option>
    <option>Completed</option>
    </select>
    <input v-model="newProject.dueDate" type="date" required />
    <button type="submit">Add Project</button>
    </form>

  <!-- Render Project Tiles Dynamically -->
    <DashboardTiles :projects="projectList" />
  </div>
</template>


<script>
import DashboardTiles from '../components/DashboardTiles.vue'

export default {
  name: "ProjectDashboard",
  components: {
    DashboardTiles
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
      ],
      newProject: {
        name: "",
        status: "",
        dueDate: ""
       }
    };
  },
  methods: {
    addProject() {
        this.projectList.push({ ...this.newProject}); // I still have to double check if ... worked.
        this.newProject.name = "";
        this.newProject.status = "";
        this.newProject.dueDate = "";
      }
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

.project-form {
width: 100%;
max-width: 800px;
margin-bottom: 30px;
display: flex;
gap: 10px;
justify-content: center;
flex-wrap: wrap;
}

.project-form input,
.project-form select {
    padding: 8px 12px;
    font-size: 14px;
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    min-width: 150px;
}
.project-form button {
    padding: 8px 16px;
    font-size: 14px;
    background-color: #FFFFFF;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}

.project-form button:hover {
    background-color: #FFFFFF;
}
</style>
