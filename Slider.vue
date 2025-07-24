<template>
  <div class="container">
    <h2>Submit Performance Feedback</h2>

    <form @submit.prevent="handleSubmit">
      <!-- Project Name -->
      <label for="project_name">Project Name</label>
      <input type="text" id="project_name" v-model="projectName" required />

      <!-- Project Management -->
      <div class="slider-section">
        <label for="project_management">Project Management</label>
        <p class="reflection-question">How well did I manage tasks, time, and goals in this project?</p>
        <input type="range" id="project_management" min="1" max="7" v-model="projectManagement" />
        <div class="slider-labels">
          <span v-for="n in 7" :key="n">{{ n }}</span>
        </div>
        <div class="value-display">Selected: {{ projectManagement }}</div>
      </div>

      <!-- Leadership -->
      <div class="slider-section leadership-section">
        <label for="leadership">Leadership</label>
        <p class="reflection-question">Did I inspire, support, and guide my teammates effectively?</p>
        <input type="range" id="leadership" min="1" max="7" v-model="leadership" />
        <div class="slider-labels">
          <span v-for="n in 7" :key="n">{{ n }}</span>
        </div>
        <div class="value-display">Selected: {{ leadership }}</div>
      </div>

      <!-- Organizational Change Management -->
      <div class="slider-section change-section">
        <label for="organizational_change">Organizational Change Management</label>
        <p class="reflection-question">How well did I adapt to or support changes in this project?</p>
        <input type="range" id="organizational_change" min="1" max="7" v-model="organizationalChange" />
        <div class="slider-labels">
          <span v-for="n in 7" :key="n">{{ n }}</span>
        </div>
        <div class="value-display">Selected: {{ organizationalChange }}</div>
      </div>

      <button type="submit">Submit Feedback</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "PerformanceSlider",
  data() {
    return {
      projectName: '',
      projectManagement: 4,
      leadership: 4,
      organizationalChange: 4
    };
  },
  methods: {
    handleSubmit() {
      console.log("Feedback Submitted:", {
        projectName: this.projectName,
        projectManagement: this.projectManagement,
        leadership: this.leadership,
        organizationalChange: this.organizationalChange
      });
      alert("Feedback submitted!");
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', sans-serif;
}

.container {
  background: white;
  padding: 30px 40px;
  margin: 40px 20px;
  border-radius: 15px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  max-width: 650px;
  width: 100%;
}

h2 {
  text-align: center;
  color: #1e2a38;
  margin-bottom: 25px;
}

label {
  font-weight: 600;
  margin-top: 25px;
  display: block;
  color: #1e2a38;
}

input[type="text"] {
  width: 100%;
  padding: 10px 14px;
  font-size: 1rem;
  margin-top: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus {
  border-color: #1a73e8;
}

.slider-section {
  margin-top: 25px;
  padding: 20px;
  border-radius: 12px;
  background: #f9fbff;
  border-left: 6px solid #1a73e8;
}

.leadership-section {
  border-left-color: #e8711a;
}

.change-section {
  border-left-color: #28a745;
}

.reflection-question {
  font-size: 0.95em;
  color: #555;
  margin: 10px 0 5px 0;
  font-style: italic;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.85em;
  color: #666;
  margin-top: 4px;
}

input[type=range] {
  width: 100%;
  margin-top: 8px;
  appearance: none;
  height: 8px;
  border-radius: 5px;
  background: linear-gradient(to right, #d2e3fc, #1a73e8);
  outline: none;
}

input[type=range]::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  background: #1a73e8;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
}

input[type=range]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  background: #1a73e8;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
}

.value-display {
  text-align: right;
  font-size: 0.9em;
  margin-top: 5px;
  color: #444;
}

button {
  margin-top: 30px;
  padding: 14px 20px;
  width: 100%;
  font-size: 1rem;
  background-color: #1a73e8;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0f5bb5;
}
</style>
