<template>
  <div class="dashboard-view">
    <!-- Dashboard Navigation -->
    <div class="dashboard-nav">
      <div class="nav-header">
        <h1>Performance Management Dashboard</h1>
        <button @click="logout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
          Logout
        </button>
      </div>
      <div class="nav-links">
        <router-link to="/dashboard" class="nav-link" active-class="active">Simple Dashboard</router-link>
        <router-link to="/dashboard/advanced" class="nav-link" active-class="active">Advanced Layout</router-link>
        <router-link to="/dashboard/features" class="nav-link" active-class="active">Features Demo</router-link>
        <router-link to="/career-development" class="nav-link" active-class="active">Career Development</router-link>
        <router-link to="/ai-insights" class="nav-link" active-class="active">AI Insights</router-link>
        <router-link to="/metrics" class="nav-link" active-class="active">Editable Metrics</router-link>
      </div>
    </div>

    <!-- Main Dashboard Content -->
    <div class="dashboard-container">
      <!-- Navigation Tabs Component -->
      <Navigation />

      <!-- Dashboard Grid -->
      <div class="dashboard-grid">
        <!-- Feedback Section -->
        <div class="dashboard-section">
          <h2>Submit Feedback</h2>
          <Slider @submit-feedback="handleFeedbackSubmit" />
        </div>

        <!-- Charts Section -->
        <div class="dashboard-section">
          <h2>Team Performance</h2>
          <TeamAverageChart :scores="scores" />
        </div>
      </div>

      <!-- Projects Section -->
      <div class="dashboard-section full-width">
        <h2>Projects Overview</h2>
        <ProjectDashboard />
      </div>

      <!-- Dashboard Tiles -->
      <div class="dashboard-section full-width">
        <h2>Project Tiles</h2>
        <DashboardTiles />
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <h3>Quick Access</h3>
        <div class="action-buttons">
          <button @click="showCareerForm = !showCareerForm" class="action-btn">
            {{ showCareerForm ? 'Hide' : 'Show' }} Career Development
          </button>
          <button @click="showAIInsights = !showAIInsights" class="action-btn">
            {{ showAIInsights ? 'Hide' : 'Show' }} AI Insights
          </button>
          <button @click="showEditableSliders = !showEditableSliders" class="action-btn">
            {{ showEditableSliders ? 'Hide' : 'Show' }} Editable Metrics
          </button>
        </div>
      </div>

      <!-- Conditionally Show Components -->
      <div v-if="showCareerForm" class="dashboard-section full-width">
        <h2>Career Development</h2>
        <CareerDevelopmentForm />
      </div>

      <div v-if="showAIInsights" class="dashboard-section full-width">
        <h2>AI Insights</h2>
        <AIInsight />
      </div>

      <div v-if="showEditableSliders" class="dashboard-section full-width">
        <h2>Editable Performance Metrics</h2>
        <EditableSliders />
      </div>
    </div>
  </div>
</template>

<script>
// Import ALL your reusable components from components folder
import Navigation from '@/components/Navigation.vue'
import Slider from '@/components/Slider.vue'
import TeamAverageChart from '@/components/TeamAverageChart.vue'
import ProjectDashboard from '@/views/ProjectDashboard.vue'
import DashboardTiles from '@/components/DashboardTiles.vue'
import EditableSliders from '@/components/EditableSliders.vue'
import CareerDevelopmentForm from '@/components/CareerDevelopmentForm.vue'
import AIInsight from '@/components/AIInsight.vue'

export default {
  name: 'DashboardView',
  components: {
    Navigation,
    Slider,
    TeamAverageChart,
    ProjectDashboard,
    DashboardTiles,
    EditableSliders,
    CareerDevelopmentForm,
    AIInsight
  },
  data() {
    return {
      scores: {
        projectManagement: 4,
        leadership: 4,
        organizationalChange: 4
      },
      // Toggle states for showing/hiding components
      showCareerForm: false,
      showAIInsights: false,
      showEditableSliders: false
    }
  },
  methods: {
    handleFeedbackSubmit(newScores) {
      this.scores = { ...this.scores, ...newScores }
      // Emit to parent App.vue if needed
      this.$emit('submit-feedback', newScores)
      console.log('Feedback submitted:', newScores)
    },

    async logout() {
      try {
        // Call the auth service logout
        await this.$authService.logout()

        // Redirect to login page
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
        // Still redirect even if logout fails
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.dashboard-view {
  background: #f8fafc;
  min-height: 100vh;
}

.dashboard-nav {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.dashboard-nav h1 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #dc2626;
}

.logout-btn i {
  font-size: 0.875rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.nav-link {
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  color: #475569;
  text-decoration: none;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.active {
  background: #3b82f6;
  color: white;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.dashboard-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.dashboard-section.full-width {
  grid-column: 1 / -1;
  margin-bottom: 2rem;
}

.dashboard-section h2 {
  margin: 0 0 1rem 0;
  color: #1e293b;
  font-size: 1.25rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.quick-actions {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.quick-actions h3 {
  margin: 0 0 1rem 0;
  color: #1e293b;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background: #2563eb;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 0 1rem 1rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .nav-links {
    flex-direction: column;
  }

  .action-buttons {
    flex-direction: column;
  }

  .nav-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .logout-btn {
    justify-content: center;
  }
}
</style>