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
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="dashboard-main">
//develop animated transitions between dashboard states:
      <transition name="fade" mode="out-in">
       <div :key="activeSection">

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

          <!-- Active Filters Display -->
          <div v-if="hasActiveFilters" class="active-filters">
            <div class="filter-tags">
              <span v-if="filters.status" class="filter-tag">
                Status: {{ filters.status }}
                <button @click="clearFilter('status')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.team" class="filter-tag">
                Team: {{ getTeamName(filters.team) }}
                <button @click="clearFilter('team')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.priority" class="filter-tag">
                Priority: {{ filters.priority }}
                <button @click="clearFilter('priority')" class="filter-remove">×</button>
              </span>
              <span v-if="filters.search" class="filter-tag">
                Search: "{{ filters.search }}"
                <button @click="clearFilter('search')" class="filter-remove">×</button>
              </span>
            </div>
            <button @click="clearAllFilters" class="clear-all-btn">
              Clear All Filters
            </button>
          </div>

          <!-- Results Summary -->
          <div class="results-summary">
            <div class="results-info">
              <span class="results-count">{{ filteredProjects.length }} of {{ projects.length }} projects</span>
              <span v-if="hasActiveFilters" class="filtered-indicator">
                <i class="fas fa-filter"></i>
                Filtered
              </span>
            </div>
            <div class="bulk-actions" v-if="selectedProjects.length > 0">
              <span class="selected-count">{{ selectedProjects.length }} selected</span>
              <button @click="bulkUpdateStatus" class="bulk-btn">Update Status</button>
              <button @click="bulkAssignTeam" class="bulk-btn">Assign Team</button>
              <button @click="bulkExport" class="bulk-btn">Export Selected</button>
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
                :class="{ 
                  selected: selectedProjects.includes(project.id),
                  'high-priority': project.priority === 'critical' || project.priority === 'high'
                }"
                @click="selectProject(project)"
              >
                <!-- Selection Checkbox -->
                <div class="project-checkbox">
                  <input 
                    type="checkbox"
                    :checked="selectedProjects.includes(project.id)"
                    @change="toggleProjectSelection(project.id)"
                    @click.stop
                  >
                </div>

                <!-- Project Header -->
                <div class="project-header">
                  <div class="project-title-section">
                    <h3 class="project-title">{{ project.name }}</h3>
                    <div class="project-badges">
                      <span :class="'status-badge status-' + project.status">{{ project.status }}</span>
                      <span :class="'priority-badge priority-' + project.priority">{{ project.priority }}</span>
                    </div>
                  </div>
                  <div class="project-menu">
                    <button @click.stop="toggleProjectMenu(project.id)" class="menu-btn">
                      <i class="fas fa-ellipsis-v"></i>
                    </button>
                    <div v-if="activeProjectMenu === project.id" class="project-dropdown">
                      <button @click="editProject(project)" class="dropdown-item">
                        <i class="fas fa-edit"></i> Edit
                      </button>
                      <button @click="duplicateProject(project)" class="dropdown-item">
                        <i class="fas fa-copy"></i> Duplicate
                      </button>
                      <button @click="archiveProject(project)" class="dropdown-item">
                        <i class="fas fa-archive"></i> Archive
                      </button>
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
                    <div class="team-avatars">
                      <img 
                        v-for="member in project.team.members.slice(0, 3)" 
                        :key="member.id"
                        :src="member.avatar" 
                        :alt="member.name"
                        :title="member.name"
                        class="team-avatar"
                      >
                      <span v-if="project.team.members.length > 3" class="team-count">
                        +{{ project.team.members.length - 3 }}
                      </span>
                    </div>
                    <span class="team-name">{{ project.team.name }}</span>
                  </div>
                  <div class="timeline-info">
                    <i class="fas fa-calendar"></i>
                    <span class="deadline" :class="{ overdue: isOverdue(project.deadline) }">
                      {{ formatDate(project.deadline) }}
                    </span>
                  </div>
                </div>

                <!-- Project Footer -->
                <div class="project-footer">
                  <div class="last-update">
                    <i class="fas fa-clock"></i>
                    <span>Updated {{ formatRelativeTime(project.updatedAt) }}</span>
                  </div>
                  <div class="project-insights">
                    <div class="insight-indicator" v-if="project.aiInsights > 0">
                      <i class="fas fa-brain"></i>
                      <span>{{ project.aiInsights }} insights</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- List View -->
            <div v-if="viewMode === 'list'" class="projects-list">
              <div class="list-header">
                <div class="list-column">Project</div>
                <div class="list-column">Team</div>
                <div class="list-column">Status</div>
                <div class="list-column">Progress</div>
                <div class="list-column">Deadline</div>
                <div class="list-column">Actions</div>
              </div>
              
              <div 
                v-for="project in paginatedProjects" 
                :key="project.id"
                class="list-row"
                :class="{ selected: selectedProjects.includes(project.id) }"
                @click="selectProject(project)"
              >
                <div class="list-column project-info">
                  <input 
                    type="checkbox"
                    :checked="selectedProjects.includes(project.id)"
                    @change="toggleProjectSelection(project.id)"
                    @click.stop
                    class="row-checkbox"
                  >
                  <div class="project-details">
                    <h4 class="project-name">{{ project.name }}</h4>
                    <p class="project-desc">{{ project.description }}</p>
                  </div>
                </div>
                
                <div class="list-column team-column">
                  <div class="team-display">
                    <img :src="project.team.members[0].avatar" :alt="project.team.name" class="team-lead-avatar">
                    <span>{{ project.team.name }}</span>
                  </div>
                </div>
                
                <div class="list-column">
                  <span :class="'status-badge status-' + project.status">{{ project.status }}</span>
                </div>
                
                <div class="list-column progress-column">
                  <div class="mini-progress">
                    <div class="mini-progress-bar">
                      <div 
                        class="mini-progress-fill" 
                        :style="{ width: project.progress + '%' }"
                      ></div>
                    </div>
                    <span class="mini-progress-text">{{ project.progress }}%</span>
                  </div>
                </div>
                
                <div class="list-column deadline-column">
                  <span :class="{ overdue: isOverdue(project.deadline) }">
                    {{ formatDate(project.deadline) }}
                  </span>
                </div>
                
                <div class="list-column actions-column">
                  <button @click.stop="editProject(project)" class="list-action-btn">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button @click.stop="viewProject(project)" class="list-action-btn">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button @click.stop="toggleProjectMenu(project.id)" class="list-action-btn">
                    <i class="fas fa-ellipsis-v"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredProjects.length === 0" class="empty-state">
              <div class="empty-icon">
                <i class="fas fa-folder-open"></i>
              </div>
              <h3>No Projects Found</h3>
              <p v-if="hasActiveFilters">
                No projects match your current filters. Try adjusting your search criteria.
              </p>
              <p v-else>
                You haven't created any projects yet. Get started by creating your first project.
              </p>
              <button @click="hasActiveFilters ? clearAllFilters() : (showCreateProject = true)" class="empty-action-btn">
                {{ hasActiveFilters ? 'Clear Filters' : 'Create Project' }}
              </button>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="pagination-container">
            <div class="pagination-info">
              Showing {{ (currentPage - 1) * itemsPerPage + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredProjects.length) }} of {{ filteredProjects.length }} projects
            </div>
            <div class="pagination-controls">
              <button 
                @click="goToPage(1)"
                :disabled="currentPage === 1"
                class="pagination-btn"
              >
                <i class="fas fa-angle-double-left"></i>
              </button>
              <button 
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="pagination-btn"
              >
                <i class="fas fa-chevron-left"></i>
              </button>
              
              <div class="page-numbers">
                <button 
                  v-for="page in visiblePages" 
                  :key="page"
                  @click="goToPage(page)"
                  :class="{ active: page === currentPage }"
                  class="page-btn"
                >
                  {{ page }}
                </button>
              </div>
              
              <button 
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="pagination-btn"
              >
                <i class="fas fa-chevron-right"></i>
              </button>
              <button 
                @click="goToPage(totalPages)"
                :disabled="currentPage === totalPages"
                class="pagination-btn"
              >
                <i class="fas fa-angle-double-right"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- Dashboard Sections Smooth Transitions -->
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
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-check"></i>
              </div>
              <div class="stat-content">
                <h3>{{ projects.filter(p => p.status === 'completed').length }}</h3>
                <p>Completed</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">
                <i class="fas fa-users"></i>
              </div>
              <div class="stat-content">
                <h3>{{ teams.length }}</h3>
                <p>Teams</p>
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
       </div>
      </transition>
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
          aiInsights: 3,
          team: {
            id: 1,
            name: 'Frontend Team',
            members: [
              { id: 1, name: 'John Doe', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150' },
              { id: 2, name: 'Jane Smith', avatar: 'https://images.unsplash.com/photo-1494790108755-2616b9a28f3a?w=150' },
              { id: 3, name: 'Mike Johnson', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150' },
              { id: 4, name: 'Sarah Wilson', avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150' }
            ]
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
          aiInsights: 2,
          team: {
            id: 2,
            name: 'Backend Team',
            members: [
              { id: 5, name: 'Alex Brown', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150' },
              { id: 6, name: 'Emily Davis', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150' }
            ]
          },
          updatedAt: '2024-01-14T14:20:00Z'
        },
        {
          id: 3,
          name: 'Database Migration',
          description: 'Migrate legacy database to cloud infrastructure',
          status: 'completed',
          priority: 'medium',
          progress: 100,
          deadline: '2024-01-30',
          aiInsights: 1,
          team: {
            id: 2,
            name: 'Backend Team',
            members: [
              { id: 7, name: 'David Miller', avatar: 'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?w=150' },
              { id: 8, name: 'Lisa Garcia', avatar: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150' },
              { id: 9, name: 'Tom Anderson', avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f7a?w=150' }
            ]
          },
          updatedAt: '2024-01-10T09:15:00Z'
        },
        {
          id: 4,
          name: 'E-commerce Platform',
          description: 'Build a scalable e-commerce solution with payment integration',
          status: 'active',
          priority: 'high',
          progress: 60,
          deadline: '2024-04-10',
          aiInsights: 4,
          team: {
            id: 1,
            name: 'Frontend Team',
            members: [
              { id: 1, name: 'John Doe', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150' },
              { id: 10, name: 'Rachel Green', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150' }
            ]
          },
          updatedAt: '2024-01-13T16:45:00Z'
        },
        {
          id: 5,
          name: 'API Documentation',
          description: 'Comprehensive API documentation and developer portal',
          status: 'on_hold',
          priority: 'low',
          progress: 40,
          deadline: '2024-06-01',
          aiInsights: 0,
          team: {
            id: 3,
            name: 'Design Team',
            members: [
              { id: 11, name: 'Chris Lee', avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150' }
            ]
          },
          updatedAt: '2024-01-08T11:20:00Z'
        }
      ]
    }
  },
  computed: {
    hasActiveFilters() {
      return this.filters.status || this.filters.team || this.filters.priority || 
             this.filters.search || this.filters.progressMin > 0 || this.filters.progressMax < 100;
    },
    
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
          p.team.name.toLowerCase().includes(query) ||
          p.team.members.some(m => m.name.toLowerCase().includes(query))
        );
      }
      
      // Apply progress range filter
      filtered = filtered.filter(p => 
        p.progress >= this.filters.progressMin && p.progress <= this.filters.progressMax
      );
      
      // Apply sorting
      filtered.sort((a, b) => {
        let aVal, bVal;
        
        switch (this.sortBy) {
          case 'name':
            aVal = a.name.toLowerCase();
            bVal = b.name.toLowerCase();
            break;
          case 'progress':
            aVal = a.progress;
            bVal = b.progress;
            break;
          case 'priority': {
            const priorityOrder = { low: 1, medium: 2, high: 3, critical: 4 };
            aVal = priorityOrder[a.priority];
            bVal = priorityOrder[b.priority];
            break; }
          case 'deadline':
            aVal = new Date(a.deadline);
            bVal = new Date(b.deadline);
            break;
          default: // updated
            aVal = new Date(a.updatedAt);
            bVal = new Date(b.updatedAt);
        }
        
        if (this.sortOrder === 'desc') {
          return bVal > aVal ? 1 : -1;
        } else {
          return aVal > bVal ? 1 : -1;
        }
      });
      
      return filtered;
    },
    
    totalPages() {
      return Math.ceil(this.filteredProjects.length / this.itemsPerPage);
    },
    
    paginatedProjects() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredProjects.slice(start, start + this.itemsPerPage);
    },
    
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      const half = Math.floor(maxVisible / 2);
      
      let start = Math.max(1, this.currentPage - half);
      let end = Math.min(this.totalPages, start + maxVisible - 1);
      
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1);
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      
      return pages;
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    
    setActiveSection(section) {
      this.activeSection = section;
      // Smooth transition effect
      const mainContent = document.querySelector('.dashboard-main');
      if (mainContent) {
        mainContent.style.opacity = '0';
        setTimeout(() => {
          mainContent.style.opacity = '1';
        }, 150);
      }
    },
    
    applyFilters() {
      this.currentPage = 1;
      // Debounce search to avoid too many calls
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        // Filters are reactive through computed property
      }, 300);
    },
    
    clearFilter(filterName) {
      if (filterName === 'progressMin' || filterName === 'progressMax') {
        this.filters.progressMin = 0;
        this.filters.progressMax = 100;
      } else {
        this.filters[filterName] = '';
      }
      this.applyFilters();
    },
    
    clearAllFilters() {
      this.filters = {
        status: '',
        team: '',
        priority: '',
        search: '',
        progressMin: 0,
        progressMax: 100
      };
      this.applyFilters();
    },
    
    clearSearch() {
      this.filters.search = '';
      this.applyFilters();
    },
    
    toggleSortOrder() {
      this.sortOrder = this.sortOrder === 'desc' ? 'asc' : 'desc';
      this.applyFilters();
    },
    
    selectProject(project) {
      this.$emit('project-selected', project);
    },
    
    toggleProjectSelection(projectId) {
      const index = this.selectedProjects.indexOf(projectId);
      if (index > -1) {
        this.selectedProjects.splice(index, 1);
      } else {
        this.selectedProjects.push(projectId);
      }
    },
    
    toggleProjectMenu(projectId) {
      this.activeProjectMenu = this.activeProjectMenu === projectId ? null : projectId;
    },
    
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    
    getTeamName(teamId) {
      const team = this.teams.find(t => t.id === parseInt(teamId));
      return team ? team.name : '';
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
    
    formatRelativeTime(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) return 'yesterday';
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
      return `${Math.floor(diffDays / 30)} months ago`;
    },
    
    // Action methods
    editProject(project) {
      console.log('Edit project:', project.name);
      this.$emit('edit-project', project);
    },
    
    duplicateProject(project) {
      console.log('Duplicate project:', project.name);
      this.$emit('duplicate-project', project);
    },
    
    archiveProject(project) {
      console.log('Archive project:', project.name);
      this.$emit('archive-project', project);
    },
    
    viewProject(project) {
      console.log('View project:', project.name);
      this.$emit('view-project', project);
    },
    
    exportProjects() {
      console.log('Export projects');
      this.$emit('export-projects', this.filteredProjects);
    },
    
    bulkUpdateStatus() {
      console.log('Bulk update status for:', this.selectedProjects);
      this.$emit('bulk-update-status', this.selectedProjects);
    },
    
    bulkAssignTeam() {
      console.log('Bulk assign team for:', this.selectedProjects);
      this.$emit('bulk-assign-team', this.selectedProjects);
    },
    
    bulkExport() {
      const selected = this.projects.filter(p => this.selectedProjects.includes(p.id));
      console.log('Bulk export:', selected);
      this.$emit('bulk-export', selected);
    }
  },
  
  mounted() {
    // Close project menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.project-menu')) {
        this.activeProjectMenu = null;
      }
    });
  },
  
  beforeUnmount() {
    // Clean up event listeners
    if (this.searchTimeout) {
      clearTimeout(this.searchTimeout);
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

.nav-item.active .nav-badge {
  background: rgba(255, 255, 255, 0.2);
}

.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
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
  }
  </style>
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

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.range-filter {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.range-input {
  width: 100%;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #64748b;
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

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
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

.sort-order-btn:hover {
  background: #f8fafc;
  color: #1e293b;
}

/* Active Filters */
.active-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f1f5f9;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.filter-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  border: 1px solid #e2e8f0;
  font-size: 0.875rem;
  color: #374151;
}

.filter-remove {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-remove:hover {
  color: #ef4444;
}

.clear-all-btn {
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.clear-all-btn:hover {
  background: #dc2626;
}

/* Results Summary */
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

.filtered-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #3b82f6;
  font-size: 0.875rem;
}

.bulk-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.selected-count {
  font-size: 0.875rem;
  color: #64748b;
}

.bulk-btn {
  padding: 0.5rem 0.75rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  color: #374151;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.bulk-btn:hover {
  background: #f8fafc;
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
  position: relative;
}

.project-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.project-card.selected {
  border-color: #3b82f6;
  background: #f8fafc;
}

.project-card.high-priority {
  border-left: 4px solid #ef4444;
}

.project-checkbox {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.project-title-section {
  flex: 1;
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

.project-menu {
  position: relative;
}

.menu-btn {
  padding: 0.25rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.menu-btn:hover {
  background: #f3f4f6;
  color: #374151;
}

.project-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  z-index: 20;
  min-width: 150px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background: none;
  border: none;
  text-align: left;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background: #f8fafc;
}

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
  margin-bottom: 1rem;
}

.team-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.team-avatars {
  display: flex;
  align-items: center;
}

.team-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid white;
  margin-left: -0.5rem;
}

.team-avatar:first-child {
  margin-left: 0;
}

.team-count {
  background: #f3f4f6;
  color: #6b7280;
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
  margin-left: 0.25rem;
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

.project-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #9ca3af;
  font-size: 0.75rem;
}

.last-update {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.insight-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #3b82f6;
}

/* Projects List View */
.projects-list {
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  margin-bottom: 2rem;
}

.list-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.list-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: all 0.2s;
}

.list-row:hover {
  background: #f8fafc;
}

.list-row.selected {
  background: #eff6ff;
  border-color: #3b82f6;
}

.list-column {
  display: flex;
  align-items: center;
}

.project-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.row-checkbox {
  margin-right: 0.75rem;
}

.project-details {
  flex: 1;
}

.project-name {
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.project-desc {
  color: #64748b;
  font-size: 0.75rem;
  margin: 0;
  line-height: 1.4;
}

.team-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.team-lead-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.mini-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.4s ease;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}

.fade-enter-to, .fade-leave-from {
    opacity: 1;
}