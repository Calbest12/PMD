<template>
  <div class="glass-card">
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <div v-for="tab in tabs" :key="tab.id" class="content" :class="{ active: activeTab === tab.id }">
      <h2>{{ tab.icon }} {{ tab.label }}</h2>
      <p>{{ tab.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "NavigationTabs",
  data() {
    return {
      activeTab: "projects",
      tabs: [
        {
          id: "projects",
          label: "Projects",
          icon: "🚀",
          description:
            "Stay on top of your timelines and milestones. Manage tasks visually with style and speed. Collaborate and conquer your goals with clarity and control."
        },
        {
          id: "teams",
          label: "Teams",
          icon: "👥",
          description:
            "Lead your team like a pro. Assign roles, track progress, and stay aligned with powerful team management tools built to impress and perform."
        },
        {
          id: "reports",
          label: "Reports",
          icon: "📊",
          description:
            "Turn data into insights. Create stunning visualizations and intelligent summaries that make decision-making delightful."
        }
      ]
    };
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Poppins', sans-serif;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  color: #fff;
}

.glass-card {
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  max-width: 800px;
  width: 100%;
  padding: 2rem;
  animation: popIn 0.6s ease;
}

@keyframes popIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.tab {
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  background: linear-gradient(145deg, #1f2d3d, #3a506b);
  color: #fff;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  position: relative;
}

.tab:hover {
  transform: translateY(-2px);
  background: linear-gradient(145deg, #00c9ff, #92fe9d);
  color: #111;
}

.tab.active {
  background: linear-gradient(145deg, #ff6a00, #ee0979);
  color: white;
  box-shadow: 0 8px 20px rgba(238, 9, 121, 0.4);
}

.content {
  display: none;
  animation: fadeIn 0.5s ease-in;
}

.content.active {
  display: block;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  background: linear-gradient(to right, #00c9ff, #92fe9d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #f0f0f0;
}

@media (max-width: 600px) {
  .tab {
    flex: 1 1 100%;
    text-align: center;
  }
}
</style>
