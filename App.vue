<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 relative overflow-hidden flex items-center justify-center">
    <!-- Floating Background Elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full mix-blend-screen filter blur-xl opacity-20 animate-blob"></div>
      <div class="absolute top-40 right-10 w-72 h-72 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full mix-blend-screen filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-20 w-72 h-72 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full mix-blend-screen filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-violet-600 to-purple-600 rounded-full mix-blend-screen filter blur-3xl opacity-10 animate-pulse"></div>
    </div>

    <!-- Login/Auth Views -->
    <div v-if="!isAuthenticated" class="w-full relative z-10">
      <router-view @login-success="handleLoginSuccess" @user-authenticated="handleLoginSuccess" />
    </div>

    <!-- Main Application (Performance Hub) -->
    <div v-else class="w-full max-w-6xl mx-auto px-6 relative z-10">
      <!-- Header with Logout -->
      <div class="absolute top-6 right-6">
        <div class="flex items-center space-x-4">
          <div v-if="currentUser" class="text-right">
            <p class="text-white font-medium">Welcome back!</p>
            <p class="text-gray-400 text-sm">{{ currentUser.name || currentUser.email }}</p>
          </div>
          <button 
            @click="logout"
            class="px-6 py-3 bg-gray-800/60 backdrop-blur-sm rounded-xl text-gray-300 hover:text-white hover:bg-gray-700/50 transition-all duration-300 flex items-center space-x-2 border border-gray-700/50"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
            <span class="font-medium">Logout</span>
          </button>
        </div>
      </div>

      <!-- Centered Logo Section -->
      <div class="text-center mb-12 mt-20">
        <div class="flex items-center justify-center space-x-6 mb-8">
          <!-- Logo with existing logo -->
          <div class="relative">
            <div class="w-20 h-20 bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-purple-500/40 transform rotate-3 hover:rotate-0 transition-transform duration-300">
              <img src="./assets/logo.png" alt="PMD Logo" class="w-12 h-12 object-contain" />
            </div>
            <div class="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center animate-bounce shadow-lg">
              <span class="text-lg">✨</span>
            </div>
          </div>
          <div class="text-center">
            <h1 class="text-5xl font-black bg-gradient-to-r from-white via-purple-300 to-cyan-300 bg-clip-text text-transparent">
              Performance Hub
            </h1>
            <p class="text-lg text-gray-400 font-medium mt-2">Where excellence meets insights 🚀</p>
          </div>
        </div>
        
        <!-- Centered Navigation -->
        <nav class="flex justify-center">
          <div class="flex space-x-3 bg-gray-800/60 backdrop-blur-sm rounded-2xl p-3 shadow-2xl shadow-black/50 border border-gray-700/50">
            <button 
              @click="currentView = 'dashboard'"
              :class="[
                'px-8 py-4 rounded-xl font-semibold transition-all duration-300 flex items-center space-x-3 text-base',
                currentView === 'dashboard' 
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-2xl shadow-purple-500/30 transform scale-105' 
                  : 'text-gray-300 hover:text-white hover:bg-gray-700/50'
              ]"
            >
              <div class="relative">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M7 12l3-3 3 3 4-4"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 21l4-4 4 4"/>
                </svg>
                <div class="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <span>Dashboard</span>
            </button>
            <button 
              @click="currentView = 'forms'"
              :class="[
                'px-8 py-4 rounded-xl font-semibold transition-all duration-300 flex items-center space-x-3 text-base',
                currentView === 'forms' 
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-2xl shadow-purple-500/30 transform scale-105' 
                  : 'text-gray-300 hover:text-white hover:bg-gray-700/50'
              ]"
            >
              <div class="relative">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
                </svg>
                <div class="absolute -top-1 -right-1 w-3 h-3 bg-pink-400 rounded-full animate-pulse"></div>
              </div>
              <span>Feedback</span>
            </button>
          </div>
        </nav>
      </div>

      <!-- Main Content - Centered -->
      <div class="flex justify-center">
        <div class="w-full max-w-5xl">
          <!-- Dashboard View -->
          <div v-if="currentView === 'dashboard'" class="space-y-10 relative z-10">
            <!-- Hero Welcome Section -->
            <div class="text-center mb-16">
              <div class="inline-flex items-center space-x-3 bg-gradient-to-r from-purple-900/50 to-pink-900/50 px-6 py-3 rounded-full mb-8 border border-purple-500/30">
                <span class="text-3xl">🎯</span>
                <span class="text-lg font-bold bg-gradient-to-r from-purple-300 to-pink-300 bg-clip-text text-transparent">Performance Analytics</span>
              </div>
              <h2 class="text-5xl font-black text-white mb-8">
                Team Performance 
                <span class="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                  Insights
                </span>
              </h2>
              <p class="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                Discover patterns, celebrate achievements, and unlock your team's full potential with beautiful data visualization ✨
              </p>
            </div>

            <!-- Stats Cards Row -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              <!-- Team Score Card -->
              <div class="group bg-gradient-to-br from-purple-600 via-purple-500 to-pink-600 p-6 rounded-3xl shadow-2xl shadow-purple-500/30 text-white transform hover:scale-105 transition-all duration-300 cursor-pointer border border-purple-400/20">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-purple-100 text-sm font-medium mb-2">Team Average</p>
                    <p class="text-3xl font-black">{{ (averageScore || 0).toFixed(1) }}</p>
                    <p class="text-purple-200 text-xs">Out of 7.0</p>
                  </div>
                  <div class="text-4xl transform group-hover:scale-110 transition-transform duration-300">
                    🏆
                  </div>
                </div>
              </div>

              <!-- Projects Card -->
              <div class="group bg-gradient-to-br from-cyan-600 via-blue-500 to-cyan-600 p-6 rounded-3xl shadow-2xl shadow-cyan-500/30 text-white transform hover:scale-105 transition-all duration-300 cursor-pointer border border-cyan-400/20">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-cyan-100 text-sm font-medium mb-2">Active Projects</p>
                    <p class="text-3xl font-black">12</p>
                    <p class="text-cyan-200 text-xs">+3 this month</p>
                  </div>
                  <div class="text-4xl transform group-hover:scale-110 transition-transform duration-300">
                    🚀
                  </div>
                </div>
              </div>

              <!-- Growth Card -->
              <div class="group bg-gradient-to-br from-emerald-600 via-green-500 to-emerald-600 p-6 rounded-3xl shadow-2xl shadow-emerald-500/30 text-white transform hover:scale-105 transition-all duration-300 cursor-pointer border border-emerald-400/20">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-emerald-100 text-sm font-medium mb-2">Growth Rate</p>
                    <p class="text-3xl font-black">+24%</p>
                    <p class="text-emerald-200 text-xs">vs last quarter</p>
                  </div>
                  <div class="text-4xl transform group-hover:scale-110 transition-transform duration-300">
                    📈
                  </div>
                </div>
              </div>
            </div>

            <!-- Performance Chart Card -->
            <div class="bg-gray-900/90 backdrop-blur-xl rounded-3xl shadow-2xl shadow-black/50 border border-gray-700/50 p-8 mb-10 transform hover:scale-[1.02] transition-all duration-500">
              <div class="flex items-center justify-between mb-8">
                <div class="flex items-center space-x-4">
                  <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center shadow-2xl shadow-indigo-500/40">
                    <span class="text-2xl">📊</span>
                  </div>
                  <div>
                    <h3 class="text-2xl font-bold text-white">Performance Metrics</h3>
                    <p class="text-gray-400 text-sm">Real-time team performance data</p>
                  </div>
                </div>
                <div class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2 text-sm text-emerald-400 bg-emerald-900/30 px-3 py-1.5 rounded-full border border-emerald-500/30">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                    <span class="font-medium">Live</span>
                  </div>
                </div>
              </div>
              <TeamAverageChart :scores="scores" />
            </div>

            <!-- Interactive Feedback Section -->
            <div class="bg-gray-900/90 backdrop-blur-xl rounded-3xl shadow-2xl shadow-black/50 border border-gray-700/50 p-8 mb-10 transform hover:scale-[1.02] transition-all duration-500">
              <div class="text-center mb-10">
                <div class="inline-flex items-center space-x-3 bg-gradient-to-r from-yellow-900/50 to-orange-900/50 px-4 py-2 rounded-full mb-4 border border-yellow-500/30">
                  <span class="text-2xl">⭐</span>
                  <span class="text-sm font-bold bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">Rate Your Performance</span>
                </div>
                <h3 class="text-3xl font-bold text-white mb-3">Submit Your Feedback</h3>
                <p class="text-gray-300 text-lg">Help us understand your experience and improve together</p>
              </div>
              <Slider @submit-feedback="updateScores" />
            </div>

            <!-- Project Dashboard -->
            <div class="bg-gray-900/90 backdrop-blur-xl rounded-3xl shadow-2xl shadow-black/50 border border-gray-700/50 p-8 transform hover:scale-[1.02] transition-all duration-500">
              <div class="flex items-center space-x-4 mb-8">
                <div class="w-12 h-12 bg-gradient-to-r from-pink-500 to-rose-500 rounded-2xl flex items-center justify-center shadow-2xl shadow-pink-500/40">
                  <span class="text-2xl">🎨</span>
                </div>
                <div>
                  <h3 class="text-3xl font-bold text-white">Project Overview</h3>
                  <p class="text-gray-400">Manage and track your active projects</p>
                </div>
              </div>
              <ProjectDashboard />
            </div>
          </div>

          <!-- Forms View -->
          <div v-if="currentView === 'forms'" class="space-y-10 relative z-10">
            <div class="text-center mb-16">
              <div class="inline-flex items-center space-x-3 bg-gradient-to-r from-pink-900/50 to-purple-900/50 px-6 py-3 rounded-full mb-8 border border-pink-500/30">
                <span class="text-3xl">🌟</span>
                <span class="text-lg font-bold bg-gradient-to-r from-pink-300 to-purple-300 bg-clip-text text-transparent">Feedback Hub</span>
              </div>
              <h2 class="text-5xl font-black text-white mb-8">
                Performance 
                <span class="bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
                  Feedback
                </span>
              </h2>
              <p class="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                Share your insights, track your growth, and help shape a better tomorrow 🎯
              </p>
            </div>
            
            <div class="bg-gray-900/90 backdrop-blur-xl rounded-3xl shadow-2xl shadow-black/50 border border-gray-700/50 p-10 transform hover:scale-[1.02] transition-all duration-500">
              <div class="flex items-center space-x-4 mb-8">
                <div class="w-16 h-16 bg-gradient-to-r from-violet-500 to-purple-500 rounded-3xl flex items-center justify-center shadow-2xl shadow-violet-500/40">
                  <span class="text-3xl">🎭</span>
                </div>
                <div>
                  <h3 class="text-3xl font-bold text-white">Interactive Feedback</h3>
                  <p class="text-gray-400 text-lg">Customize your experience with advanced controls</p>
                </div>
              </div>
              <EditableSliders />
            </div>
          </div>
        </div>
      </div>

      <!-- Cute Footer -->
      <footer class="text-center mt-16 pt-8 border-t border-gray-700/50">
        <div class="flex items-center justify-center space-x-3 mb-4">
          <span class="text-2xl">💖</span>
          <span class="text-gray-300 font-medium">Made with love</span>
          <span class="text-2xl">✨</span>
        </div>
        <p class="text-gray-400 text-sm">
          &copy; 2024 Performance Hub • Built with Vue.js & lots of coffee ☕
        </p>
        <div class="flex items-center justify-center space-x-4 mt-4">
          <div class="w-2 h-2 bg-pink-400 rounded-full animate-bounce"></div>
          <div class="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
import Slider from './components/Slider.vue'
import TeamAverageChart from './components/TeamAverageChart.vue'
import ProjectDashboard from './components/ProjectDashboard.vue'
import EditableSliders from './components/EditableSliders.vue'

export default {
  name: 'App',
  components: {
    Slider,
    TeamAverageChart,
    ProjectDashboard,
    EditableSliders
  },
  data() {
    return {
      currentView: 'dashboard',
      isAuthenticated: false,
      currentUser: null,
      scores: {
        projectManagement: 4,
        leadership: 4,
        organizationalChange: 4
      }
    };
  },
  watch: {
    // Watch for authentication changes
    isAuthenticated(newVal) {
      if (newVal) {
        // User just logged in, make sure we show the dashboard
        this.currentView = 'dashboard';
      }
    },
    
    // Watch for route changes
    '$route'(to) {
      // If user is authenticated and on an auth route, redirect
      if (this.isAuthenticated && ['/login', '/signup', '/forgot-password', '/reset-password'].includes(to.path)) {
        this.$router.push('/dashboard').catch(() => {
          this.$router.push('/');
        });
      }
    }
  },
  mounted() {
    // Check if user is already logged in (e.g., from localStorage or token)
    this.checkAuthStatus();
  },
  methods: {
    updateScores(newScores) {
      if (newScores && typeof newScores === 'object') {
        this.scores = { ...this.scores, ...newScores };
      }
    },
    
    handleLoginSuccess(userData) {
      console.log('Login event received:', userData); // Minimal debug
      this.isAuthenticated = true;
      this.currentUser = userData || { email: 'user@example.com', name: 'User' };
      this.currentView = 'dashboard';
      
      // Save auth state to localStorage
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
      
      // Force reactivity update
      this.$forceUpdate();
      
      // Navigate to dashboard if route exists
      this.$nextTick(() => {
        if (this.$router && this.$router.push) {
          this.$router.push('/dashboard').catch(() => {
            // Route doesn't exist, just stay on current route
          });
        }
      });
    },
    
    logout() {
      this.isAuthenticated = false;
      this.currentUser = null;
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('currentUser');
      // Navigate back to login
      this.$router.push('/login').catch(() => {
        // Handle case where /login route might not exist
        this.$router.push('/');
      });
    },
    
    checkAuthStatus() {
      // Check if user was previously authenticated
      const isAuth = localStorage.getItem('isAuthenticated');
      const userData = localStorage.getItem('currentUser');
      
      if (isAuth === 'true' && userData) {
        this.isAuthenticated = true;
        this.currentUser = JSON.parse(userData);
        
        // If we're currently on a login/auth route, navigate away
        const currentPath = this.$route.path;
        if (currentPath === '/login' || currentPath === '/signup' || currentPath === '/forgot-password' || currentPath === '/reset-password') {
          this.$router.push('/dashboard').catch(() => {
            // If dashboard route doesn't exist, push to root
            this.$router.push('/');
          });
        }
      } else {
        // If not authenticated, navigate to login
        const currentPath = this.$route.path;
        if (currentPath !== '/login' && currentPath !== '/signup' && currentPath !== '/forgot-password' && currentPath !== '/reset-password') {
          this.$router.push('/login').catch(() => {
            this.$router.push('/');
          });
        }
      }
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}

/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #8b5cf6, #ec4899);
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #7c3aed, #db2777);
}

/* Custom animations */
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.animate-blob {
  animation: blob 8s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

/* Enhanced button animations for dark theme */
button {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

button:hover {
  transform: translateY(-3px);
}

button:active {
  transform: translateY(0) scale(0.98);
}

/* Card hover animations for dark theme */
.bg-gray-900\/90:hover {
  box-shadow: 0 40px 80px -12px rgba(0, 0, 0, 0.8), 0 0 40px rgba(139, 92, 246, 0.3);
}

/* Enhanced gradient animations */
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient-shift 6s ease infinite;
}

/* Glow effects for dark theme */
.shadow-2xl {
  filter: drop-shadow(0 0 20px rgba(139, 92, 246, 0.3));
}

/* Text glow effect */
.text-white {
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
}
</style>