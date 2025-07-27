<template>
  <div class="project-dashboard">
    <h2>Project Modules</h2>
    <div v-for="(module, index) in modules" :key="index" class="module-block">
      <h3>{{ module.name }}</h3>
      <EditableSliders
        :initialSliders="module.sliders"
        @sliders-updated="updateModuleScores(index, $event)"
      />
      <p class="score-display">Performance Score: {{ module.score.toFixed(2) }}</p>
    </div>
  </div>
</template>


<script>
import EditableSliders from "./EditableSliders.vue";

export default {
    name: "ProjectDashboard",
    components: {
      EditableSliders
    },
    data() {
      return {
        modules: [
          {
            name: "Frontend",
            sliders: [
              { label: "projectManagement", min: 0, max: 10, value: 5 },
              { label: "leadership", min: 0, max: 10, value: 5 },
              { label: "organizationalChange", min: 0, max: 10, value: 5 }
            ],
            score: 5
          },
          {
          name: "Backend",
            sliders: [
              { label: "projectManagement", min: 0, max: 10, value: 5 },
              { label: "leadership", min: 0, max: 10, value: 5 },
              { label: "organizationalChange", min: 0, max: 10, value: 5 }
            ],
            score: 5
          }
        ]
      };
    },
    methods: {
     updateModuleScores(index, updatedSliders) {
        const values = updatedSliders.map(slider=> slider.value);
        const average = values.reduce((a,b) => a + b, 0) / values.length;
        this.modules[index].score = average;
     }
   }
};
</script>


<style scoped>
.project-dashboard {
    padding: 2rem;
}

.module-block {
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px solid #dddddd;
    border-radius: 8px;
}

.score-display {
    font-weight: bold;
    margin-top: 0.5rem;
}
</style>