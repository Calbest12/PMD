<template>
  <div id="app">
    <!-- Only show header if NOT on login, signup, forgot, or reset -->
    <AppHeader v-if="showHeader && isLandingPage" />

    <!-- Landing page (public) -->
    <LandingPage v-if="!isAuthenticated && isLandingPage" />

    <!-- Show dashboard components if authenticated and on dashboard route -->
    <div v-if="isDashboardPage && isAuthenticated">
      <Navigation />
      <Slider @submit-feedback="updateScores" />
      <TeamAverageChart :scores="scores" />
    </div>

    <!-- Router view for all pages -->
    <router-view
        v-if="!isLandingPage || isAuthenticated"
        @login-success="handleLoginSuccess"
        @user-authenticated="handleLoginSuccess" />
  </div>
</template>

<script>

import AppHeader from './components/Header.vue'
import Navigation from './components/Navigation.vue'
import Slider from './components/Slider.vue'
import TeamAverageChart from './components/TeamAverageChart.vue'
import LandingPage from './views/LandingPage.vue'


export default {
  name: 'App',
  components: {
    AppHeader,
    Navigation,
    Slider,
    TeamAverageChart,
    LandingPage
  },
  data() {
    return {
      isAuthenticated: false,
      currentUser: null,
      currentProjectId: null,
      scores: {
        projectManagement: 4,
        leadership: 4,
        organizationalChange: 4
      },
      dashboardData: {
        totalProjects: 0,
        activeProjects: 0,
        completedProjects: 0,
        averageScore: 0
      },
      loading: false
    };
  },
  computed: {
    isDashboardPage() {
      return this.$route && (
        this.$route.path.includes('/dashboard') ||
        (this.$route.path === '/' && this.isAuthenticated)
      );
    },

    isLandingPage() {
  const authRoutes = ['/login', '/signup', '/forgot', '/reset', '/dashboard']
  return !authRoutes.includes(this.$route.path)
    },

    averageScore() {
      const scores = Object.values(this.scores);
      return scores.reduce((a, b) => a + b, 0) / scores.length;
    }
  },
  async mounted() {
    this.checkAuthStatus();
    if (this.isAuthenticated) {
      await this.loadDashboardData();
      await this.loadCurrentProject();
    }
  },
  methods: {
    async updateScores(newScores) {
      if (!newScores || typeof newScores !== 'object') return;

      this.loading = true;
      try {
        // Submit each category to backend
        const categories = [
          { key: 'projectManagement', category: 'PM' },
          { key: 'leadership', category: 'Leadership' },
          { key: 'organizationalChange', category: 'ChangeMgmt' }
        ];

        for (const cat of categories) {
          if (newScores[cat.key] !== undefined) {
            await this.$feedbackService.submitSliderFeedback({
              project_id: this.currentProjectId,
              category: cat.category,
              score: newScores[cat.key]
            });
          }
        }

        this.scores = { ...this.scores, ...newScores };
        await this.loadDashboardData();

        console.log('Feedback submitted successfully');
      } catch (error) {
        console.error('Failed to update scores:', error);
      } finally {
        this.loading = false;
      }
    },

    async handleLoginSuccess(userData) {
      console.log('Login success event received:', userData);
      this.isAuthenticated = true;
      this.currentUser = userData || { email: 'user@example.com', name: 'User' };

      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('currentUser', JSON.stringify(this.currentUser));

      await this.loadDashboardData();
      await this.loadCurrentProject();

      this.$nextTick(() => {
        if (this.$router && this.$router.push) {
          this.$router.push('/dashboard').catch(() => {});
        }
      });
    },

    async logout() {
      try {
        await this.$authService.logout();
      } catch (error) {
        console.error('Logout error:', error);
      }

      this.isAuthenticated = false;
      this.currentUser = null;
      this.currentProjectId = null;

      this.$router.push('/login').catch(() => {
        this.$router.push('/');
      });
    },

    checkAuthStatus() {
      try {
        const isAuth = this.$authService.isAuthenticated();
        const userData = this.$authService.getCurrentUser();

        if (isAuth && userData) {
          this.isAuthenticated = true;
          this.currentUser = userData;
        } else {
          this.isAuthenticated = false;
          this.currentUser = null;
        }
      } catch (error) {
        console.error('Auth status check error:', error);
        this.isAuthenticated = false;
        this.currentUser = null;
      }
    },

    async loadDashboardData() {
      try {
        const analytics = await this.$feedbackService.getDashboardAnalytics();

        if (analytics.success) {
          this.dashboardData = {
            totalProjects: analytics.total_projects || 0,
            activeProjects: analytics.active_projects || 0,
            completedProjects: analytics.completed_projects || 0,
            overduProjects: analytics.overdue_projects || 0,
            averageScore: analytics.completion_rate || 0
          };

          if (analytics.average_scores) {
            this.scores = {
              projectManagement: analytics.average_scores.PM || 0,
              leadership: analytics.average_scores.Leadership || 0,
              organizationalChange: analytics.average_scores.ChangeMgmt || 0
            };
          }
        }
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      }
    },

    async loadCurrentProject() {
      try {
        const projects = await this.$projectService.getProjects({ status: 'active' });
        if (projects.success && projects.results && projects.results.length > 0) {
          this.currentProjectId = projects.results[0].id;
        }
      } catch (error) {
        console.error('Failed to load current project:', error);
      }
    }
  },

  watch: {
    '$route'() {
      this.checkAuthStatus();
    }
  }
};
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