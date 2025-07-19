<template>
  <div class="tiles-container">
    <div
      v-for="(project, index) in projects"
      :key="index"
      class="dashboard-tile"
      @click="openProject(project)"
      >
      <div class="tile-header">
      <h2>{{ project.name }}</h2>
      </div>

      <p class="Status"><strong>Status:</strong>{{ project.status }}</p>
      <p class="Due-Date"><strong>Due Date:</strong> {{project.dueDate}}</p>
    </div>
  </div>
</template>


<script>
export default{
  name: 'DashboardTiles',
  props: {
    name: {
      type: String,
      required: true
    },
    status: {
      type: String,
      required: true
    },
    dueDate: {
      type: String,
      required: true
    }
},
  methods: {
    openProject(project){
      alert(`Opening project: ${project.name}`);
    }
  }
}
</script>



<style scoped>
.tiles-container {
  position: relative;
  top: -1000px;
  margin-right: 140px;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: flex-start;
  padding: 20px;
  height: 60vh;
  box-sizing: border-box;
}
.dashboard-tile{
  background: #FFFFFF;
  border-radius: 16px;
  padding: 20px;
  width: 300px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 6px solid #ff6a00;
  text-align: left;
}
.dashboard-tile:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.tile-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}
h2{
  margin: 0;
  font-size: 20px;
  font-weight:600;
  color: #2c3e50;
}
.Status,
.Due-Date {
  font-size: 14px;
  color: #555;
  margin: 4px 0;
}
</style>
