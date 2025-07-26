<template>
  <div class="dashboard-layout">
    <!-- Main Dashboard Structure -->
    <div class="dashboard-wrapper">
      <!-- Sidebar Navigation -->
      <aside class="dashboard-sidebar" :class="{ collapsed: sidebarCollapsed }">
        <div class="sidebar-header">
          <div class="logo-section">
            <div class="logo-icon">
              <i class="fas fa-layer-group"></i>
            </div>
            <h1 v-if="!sidebarCollapsed" class="logo-text">PMgt</h1>
          </div>
          <button
            @click="toggleSidebar"
            class="sidebar-toggle"
            :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
          >
            <i :class="sidebarCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left'"></i>
          </button>
        </div>

        <nav class="sidebar-navigation">
          <ul class="nav-menu">
            <li
              v-for="item in navigationItems"
              :key="item.id"
              :class="{ active: activeSection === item.id }"
              @click="setActiveSection(item.id)"
              class="nav-item"
            >
              <i :class="item.icon"></i>
              <span v-if="!sidebarCollapsed" class="nav-label">{{ item.label }}</span>
              <span v-if="!sidebarCollapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
            </li>
          </ul>
        </nav>

        <!-- User Profile Section -->
        <div class="sidebar-footer" v-if="!sidebarCollapsed">
          <div class="user-profile">
            <img :src="currentUser.avatar" :alt="currentUser.name" class="user-avatar">
            <div class="user-info">
              <span class="user-name">{{ currentUser.name }}</span>
              <span class="user-role">{{ currentUser.role }}</span>
            </div>
          </div>
          <button @click="logout" class="logout-btn">
            <i class="fas fa-sign-out-alt"></i>
            Logout
          </button>
        </div>

        <!-- Collapsed sidebar logout -->
        <div v-else class="sidebar-footer collapsed">
          <button @click="logout" class="logout-btn-collapsed" title="Logout">
            <i class="fas fa-sign-out-alt"></i>
          </button>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="dashboard-main">
        <!-- Projects Section with Filtering -->
        <div v-if="activeSection === 'projects'" class="projects-section">
          <!-- Projects Header -->
          <div class="section-header">
            <div class="header-title">
              <h2>Projects Dashboard</h2>
              <p class="header-subtitle">Manage and monitor all your projects</p>
            </div>
            <div class="header-actions">
              <button @click="showCreateProject = true" class="action-btn primary">
                <i class="fas fa-plus"></i>
                New Project
              </button>
              <button @click="exportProjects" class="action-btn secondary">
                <i class="fas fa-download"></i>
                Export
              </button>
            </div>
          </div>

          <!-- Advanced Filtering Controls -->
          <div class="filtering-controls">
            <div class="filters-section">
              <div class="filter-group">
                <label class="filter-label">Status</label>
                <select v-model="filters.status" @change="applyFilters" class="filter-select">
                  <option value="">All Status</option>
                  <option value="planning">Planning</option>
                  <option value="active">Active</option>
                  <option value="on_hold">On Hold</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">Team</label>
                <select v-model="filters.team" @change="applyFilters" class="filter-select">
                  <option value="">All Teams</option>
                  <option v-for="team in teams" :key="team.id" :value="team.id">
                    {{ team.name }}
                  </option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">Priority</label>
                <select v-model="filters.priority" @change="applyFilters" class="filter-select">
                  <option value="">All Priorities</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">Progress Range</label>
                <div class="range-filter">
                  <input
                    type="range"
                    v-model="filters.progressMin"
                    @input="applyFilters"
                    min="0"
                    max="100"
                    class="range-input"
                  >
                  <input
                    type="range"
                    v-model="filters.progressMax"
                    @input="applyFilters"
                    min="0"
                    max="100"
                    class="range-input"
                  >
                  <div class="range-labels">
                    <span>{{ filters.progressMin }}%</span>
                    <span>{{ filters.progressMax }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="search-section">
              <div class="search-container">
                <i class="fas fa-search search-icon"></i>
                <input
                  v-model="filters.search"
                  @input="applyFilters"
                  placeholder="Search projects, descriptions, or team members..."
                  class="search-input"
                >
                <button
                  v-if="filters.search"
                  @click="clearSearch"
                  class="clear-search-btn"
                >
                  <i class="fas fa-times"></i>
                </button>
              </div>
            </div>

            <div class="view-controls">
              <div class="view-toggle">
                <button
                  :class="{ active: viewMode === 'grid' }"
                  @click="viewMode = 'grid'"
                  class="view-btn"
                  title="Grid View"
                >
                  <i class="fas fa-th"></i>
                </button>
                <button
                  :class="{ active: viewMode === 'list' }"
                  @click="viewMode = 'list'"
                  class="view-btn"
                  title="List View"
                >
                  <i class="fas fa-list"></i>
                </button>
              </div>

              <div class="sort-controls">
                <select v-model="sortBy" @change="applyFilters" class="sort-select">
                  <option value="updated">Last Updated</option>
                  <option value="name">Name</option>
                  <option value="progress">Progress</option>
                  <option value="priority">Priority</option>
                  <option value="deadline">Deadline</option>
                </select>
                <button
                  @click="toggleSortOrder"
                  class="sort-order-btn"
                  :title="sortOrder === 'desc' ? 'Sort Ascending' : 'Sort Descending'"
                >
                  <i :class="sortOrder === 'desc' ? 'fas fa-arrow-down' : 'fas fa-arrow-up'"></i>
                </button>
              </div>
            </div>
          </div>

          <!-- Results Summary -->
          <div class="results-summary">
            <div class="results-info">
              <span class="results-count">{{ filteredProjects.length }} of {{ projects.length }} projects</span>
            </div>
          </div>

          <!-- Projects Display -->
          <div class="projects-container">
            <!-- Grid View -->
            <div v-if="viewMode === 'grid'" class="projects-grid">
              <div
                v-for="project in paginatedProjects"
                :key="project.id"
                class="project-card"
                @click="selectProject(project)"
              >
                <!-- Project Header -->
                <div class="project-header">
                  <div class="project-title-section">
                    <h3 class="project-title">{{ project.name }}</h3>
                    <div class="project-badges">
                      <span :class="'status-badge status-' + project.status">{{ project.status }}</span>
                      <span :class="'priority-badge priority-' + project.priority">{{ project.priority }}</span>
                    </div>
                  </div>
                </div>

                <!-- Project Description -->
                <p class="project-description">{{ project.description }}</p>

                <!-- Progress Section -->
                <div class="progress-section">
                  <div class="progress-header">
                    <span class="progress-label">Progress</span>
                    <span class="progress-value">{{ project.progress }}%</span>
                  </div>
                  <div class="progress-bar">
                    <div
                      class="progress-fill"
                      :style="{ width: project.progress + '%' }"
                      :class="getProgressClass(project.progress)"
                    ></div>
                  </div>
                </div>

                <!-- Team and Timeline -->
                <div class="project-meta">
                  <div class="team-info">
                    <span class="team-name">{{ project.team.name }}</span>
                  </div>
                  <div class="timeline-info">
                    <i class="fas fa-calendar"></i>
                    <span class="deadline" :class="{ overdue: isOverdue(project.deadline) }">
                      {{ formatDate(project.deadline) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredProjects.length === 0" class="empty-state">
              <div class="empty-icon">
                <i class="fas fa-folder-open"></i>
              </div>
              <h3>No Projects Found</h3>
              <p>You haven't created any projects yet.</p>
              <button @click="showCreateProject = true" class="empty-action-btn">
                Create Project
              </button>
            </div>
          </div>
        </div>

        <!-- Dashboard Sections -->
        <div v-if="activeSection === 'overview'" class="overview-section">
          <div class="section-header">
            <div class="header-title">
              <h2>Dashboard Overview</h2>
              <p class="header-subtitle">Get insights into your project portfolio</p>
            </div>
          </div>
          <div class="overview-stats">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-folder"></i>
              </div>
              <div class="stat-content">
                <h3>{{ projects.length }}</h3>
                <p>Total Projects</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-play"></i>
              </div>
              <div class="stat-content">
                <h3>{{ projects.filter(p => p.status === 'active').length }}</h3>
                <p>Active Projects</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeSection === 'analytics'" class="analytics-section">
          <div class="section-header">
            <div class="header-title">
              <h2>Analytics & Reports</h2>
              <p class="header-subtitle">Track performance and generate insights</p>
            </div>
          </div>
          <div class="analytics-placeholder">
            <i class="fas fa-chart-bar"></i>
            <p>Analytics dashboard coming soon...</p>
          </div>
        </div>

        <div v-if="activeSection === 'team'" class="team-section">
          <div class="section-header">
            <div class="header-title">
              <h2>Team Management</h2>
              <p class="header-subtitle">Manage team members and assignments</p>
            </div>
          </div>
          <div class="teams-grid">
            <div v-for="team in teams" :key="team.id" class="team-card">
              <h3>{{ team.name }}</h3>
              <p>{{ getTeamProjectCount(team.id) }} projects</p>
            </div>
          </div>
        </div>

        <div v-if="activeSection === 'settings'" class="settings-section">
          <div class="section-header">
            <div class="header-title">
              <h2>Settings</h2>
              <p class="header-subtitle">Configure your dashboard preferences</p>
            </div>
          </div>
          <div class="settings-placeholder">
            <i class="fas fa-cog"></i>
            <p>Settings panel coming soon...</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardLayout',
  data() {
    return {
      sidebarCollapsed: false,
      activeSection: 'projects',
      viewMode: 'grid',
      sortBy: 'updated',
      sortOrder: 'desc',
      currentPage: 1,
      itemsPerPage: 12,
      selectedProjects: [],
      activeProjectMenu: null,
      showCreateProject: false,
      searchTimeout: null,
      filters: {
        status: '',
        team: '',
        priority: '',
        search: '',
        progressMin: 0,
        progressMax: 100
      },
      navigationItems: [
        { id: 'overview', label: 'Overview', icon: 'fas fa-home', badge: null },
        { id: 'projects', label: 'Projects', icon: 'fas fa-folder', badge: 15 },
        { id: 'analytics', label: 'Analytics', icon: 'fas fa-chart-bar', badge: null },
        { id: 'team', label: 'Team', icon: 'fas fa-users', badge: 8 },
        { id: 'settings', label: 'Settings', icon: 'fas fa-cog', badge: null }
      ],
      currentUser: {
        name: 'Sarah Johnson',
        role: 'Project Manager',
        avatar: 'https://images.unsplash.com/photo-1494790108755-2616b9a28f3a?w=150'
      },
      teams: [
        { id: 1, name: 'Frontend Team' },
        { id: 2, name: 'Backend Team' },
        { id: 3, name: 'Design Team' },
        { id: 4, name: 'QA Team' }
      ],
      projects: [
        {
          id: 1,
          name: 'Website Redesign',
          description: 'Complete overhaul of company website with modern design and improved UX',
          status: 'active',
          priority: 'high',
          progress: 75,
          deadline: '2024-03-15',
          team: {
            id: 1,
            name: 'Frontend Team'
          },
          updatedAt: '2024-01-15T10:30:00Z'
        },
        {
          id: 2,
          name: 'Mobile App Development',
          description: 'Native mobile application for iOS and Android platforms',
          status: 'planning',
          priority: 'critical',
          progress: 25,
          deadline: '2024-05-20',
          team: {
            id: 2,
            name: 'Backend Team'
          },
          updatedAt: '2024-01-14T14:20:00Z'
        }
      ]
    }
  },
  computed: {
    filteredProjects() {
      let filtered = [...this.projects];

      // Apply status filter
      if (this.filters.status) {
        filtered = filtered.filter(p => p.status === this.filters.status);
      }

      // Apply team filter
      if (this.filters.team) {
        filtered = filtered.filter(p => p.team.id === parseInt(this.filters.team));
      }

      // Apply priority filter
      if (this.filters.priority) {
        filtered = filtered.filter(p => p.priority === this.filters.priority);
      }

      // Apply search filter
      if (this.filters.search) {
        const query = this.filters.search.toLowerCase();
        filtered = filtered.filter(p =>
          p.name.toLowerCase().includes(query) ||
          p.description.toLowerCase().includes(query) ||
          p.team.name.toLowerCase().includes(query)
        );
      }

      // Apply progress range filter
      filtered = filtered.filter(p =>
        p.progress >= this.filters.progressMin && p.progress <= this.filters.progressMax
      );

      return filtered;
    },

    paginatedProjects() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredProjects.slice(start, start + this.itemsPerPage);
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },

    setActiveSection(section) {
      this.activeSection = section;
    },

    applyFilters() {
      this.currentPage = 1;
    },

    clearSearch() {
      this.filters.search = '';
      this.applyFilters();
    },

    selectProject(project) {
      this.$emit('project-selected', project);
    },

    getTeamProjectCount(teamId) {
      return this.projects.filter(p => p.team.id === teamId).length;
    },

    getProgressClass(progress) {
      if (progress >= 80) return 'progress-excellent';
      if (progress >= 60) return 'progress-good';
      if (progress >= 40) return 'progress-fair';
      return 'progress-poor';
    },

    isOverdue(deadline) {
      return new Date(deadline) < new Date();
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    },

    exportProjects() {
      console.log('Export projects');
      this.$emit('export-projects', this.filteredProjects);
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
* {
  box-sizing: border-box;
}

.dashboard-layout {
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Inter', sans-serif;
}

.dashboard-wrapper {
  display: flex;
  min-height: 100vh;
}

/* Sidebar Styles */
.dashboard-sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
}

.dashboard-sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.sidebar-toggle {
  padding: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.sidebar-toggle:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.sidebar-navigation {
  flex: 1;
  padding: 1rem 0;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.5rem;
  margin: 0.25rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.nav-item:hover {
  background: #f8fafc;
  color: #1e293b;
}

.nav-item.active {
  background: #3b82f6;
  color: white;
}

.nav-label {
  font-weight: 500;
}

.nav-badge {
  background: rgba(255, 255, 255, 0.2);
  color: currentColor;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  margin-left: auto;
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}

.user-role {
  color: #64748b;
  font-size: 0.75rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s;
  width: 100%;
}

.logout-btn:hover {
  background: #dc2626;
}

.logout-btn i {
  font-size: 0.875rem;
}

.sidebar-footer.collapsed {
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
}

.logout-btn-collapsed {
  width: 40px;
  height: 40px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  margin: 0 auto;
}

.logout-btn-collapsed:hover {
  background: #dc2626;
}

/* Main Content */
.dashboard-main {
  flex: 1;
  overflow-y: auto;
  transition: opacity 0.15s ease;
}

.projects-section {
  padding: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.header-title h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.header-subtitle {
  color: #64748b;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
}

.action-btn.secondary {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.action-btn.secondary:hover {
  background: #f8fafc;
  color: #1e293b;
}

/* Filtering Controls */
.filtering-controls {
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: flex-end;
}

.filters-section {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 150px;
}

.filter-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  color: #374151;
  cursor: pointer;
}

.search-section {
  flex: 1;
  min-width: 250px;
}

.search-container {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.clear-search-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}

.view-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.view-toggle {
  display: flex;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.view-btn {
  padding: 0.5rem 0.75rem;
  background: white;
  border: none;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.view-btn.active {
  background: #3b82f6;
  color: white;
}

.sort-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.sort-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  color: #374151;
}

.sort-order-btn {
  padding: 0.5rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.results-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.results-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.results-count {
  font-weight: 500;
  color: #374151;
}

/* Projects Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.project-card {
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.project-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.project-header {
  margin-bottom: 1rem;
}

.project-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.project-badges {
  display: flex;
  gap: 0.5rem;
}

.status-badge, .priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-planning { background: #fef3c7; color: #92400e; }
.status-active { background: #d1fae5; color: #065f46; }
.status-on_hold { background: #fee2e2; color: #991b1b; }
.status-completed { background: #dbeafe; color: #1e40af; }

.priority-low { background: #f3f4f6; color: #374151; }
.priority-medium { background: #fef3c7; color: #92400e; }
.priority-high { background: #fed7aa; color: #c2410c; }
.priority-critical { background: #fee2e2; color: #991b1b; }

.project-description {
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.progress-section {
  margin-bottom: 1.5rem;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.progress-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
}

.progress-bar {
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-excellent { background: #10b981; }
.progress-good { background: #3b82f6; }
.progress-fair { background: #f59e0b; }
.progress-poor { background: #ef4444; }

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.team-name {
  font-size: 0.875rem;
  color: #374151;
}

.timeline-info {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #6b7280;
  font-size: 0.875rem;
}

.deadline.overdue {
  color: #ef4444;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
}

.empty-icon {
  font-size: 3rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.empty-action-btn {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.empty-action-btn:hover {
  background: #2563eb;
}

/* Overview Section */
.overview-section {
  padding: 2rem;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 1.5rem;
}

.stat-content h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.stat-content p {
  color: #64748b;
  margin: 0;
  font-size: 0.875rem;
}

/* Other Sections */
.analytics-section,
.team-section,
.settings-section {
  padding: 2rem;
}

.analytics-placeholder,
.settings-placeholder {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  color: #9ca3af;
}

.analytics-placeholder i,
.settings-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.team-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
}

.team-card h3 {
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.team-card p {
  color: #64748b;
  margin: 0;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .dashboard-wrapper {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    height: auto;
  }

  .projects-section {
    padding: 1rem;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>