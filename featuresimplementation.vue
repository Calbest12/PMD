<template>
  <div class="dashboard-container">
    <!-- Header with Leadership Visuals -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">Project Management Dashboard</h1>
        <div class="leadership-section">
          <div class="team-selector">
            <label for="team-filter">Filter by Team:</label>
            <select 
              id="team-filter" 
              v-model="selectedTeam" 
              @change="filterByTeam"
              class="team-select"
            >
              <option value="">All Teams</option>
              <option v-for="team in teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>
          <div class="member-toggle">
            <button 
              v-for="member in filteredMembers" 
              :key="member.id"
              @click="toggleMember(member.id)"
              :class="['member-btn', { active: selectedMembers.includes(member.id) }]"
            >
              <img :src="member.avatar" :alt="member.name" class="member-avatar">
              <span>{{ member.name }}</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Dashboard Layout -->
    <div class="dashboard-main">
      <!-- Sidebar Navigation -->
      <nav class="dashboard-sidebar">
        <div class="nav-section">
          <h3>Projects</h3>
          <div class="project-filters">
            <button 
              @click="setProjectFilter('all')"
              :class="['filter-btn', { active: projectFilter === 'all' }]"
            >
              All Projects
            </button>
            <button 
              @click="setProjectFilter('active')"
              :class="['filter-btn', { active: projectFilter === 'active' }]"
            >
              Active
            </button>
            <button 
              @click="setProjectFilter('completed')"
              :class="['filter-btn', { active: projectFilter === 'completed' }]"
            >
              Completed
            </button>
            <button 
              @click="setProjectFilter('overdue')"
              :class="['filter-btn', { active: projectFilter === 'overdue' }]"
            >
              Overdue
            </button>
          </div>
        </div>
        
        <div class="nav-section">
          <h3>Actions</h3>
          <button @click="showNewProjectForm = true" class="action-btn">
            + New Project
          </button>
          <button @click="showTeamForm = true" class="action-btn">
            + Add Team Member
          </button>
        </div>
      </nav>

      <!-- Main Content Area -->
      <main class="dashboard-content">
        <!-- Dashboard Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Total Projects</h3>
            <div class="stat-value">{{ filteredProjects.length }}</div>
          </div>
          <div class="stat-card">
            <h3>Active Projects</h3>
            <div class="stat-value">{{ activeProjects.length }}</div>
          </div>
          <div class="stat-card">
            <h3>Team Members</h3>
            <div class="stat-value">{{ filteredMembers.length }}</div>
          </div>
          <div class="stat-card">
            <h3>Completion Rate</h3>
            <div class="stat-value">{{ completionRate }}%</div>
          </div>
        </div>

        <!-- Projects Grid -->
        <div class="projects-section">
          <div class="section-header">
            <h2>Projects</h2>
            <div class="view-controls">
              <button 
                @click="viewMode = 'grid'"
                :class="['view-btn', { active: viewMode === 'grid' }]"
              >
                Grid
              </button>
              <button 
                @click="viewMode = 'list'"
                :class="['view-btn', { active: viewMode === 'list' }]"
              >
                List
              </button>
            </div>
          </div>

          <div :class="['projects-container', viewMode]">
            <div 
              v-for="project in filteredProjects" 
              :key="project.id"
              class="project-card"
            >
              <div class="project-header">
                <h3>{{ project.name }}</h3>
                <span :class="['status-badge', project.status]">
                  {{ project.status }}
                </span>
              </div>
              <p class="project-description">{{ project.description }}</p>
              <div class="project-meta">
                <div class="project-team">
                  <span class="meta-label">Team:</span>
                  <div class="team-avatars">
                    <img 
                      v-for="memberId in project.teamMembers" 
                      :key="memberId"
                      :src="getMemberById(memberId)?.avatar" 
                      :alt="getMemberById(memberId)?.name"
                      class="team-avatar"
                    >
                  </div>
                </div>
                <div class="project-progress">
                  <span class="meta-label">Progress:</span>
                  <div class="progress-bar">
                    <div 
                      class="progress-fill" 
                      :style="{ width: project.progress + '%' }"
                    ></div>
                  </div>
                  <span class="progress-text">{{ project.progress }}%</span>
                </div>
                <div class="project-deadline">
                  <span class="meta-label">Due:</span>
                  <span :class="{ overdue: isOverdue(project.deadline) }">
                    {{ formatDate(project.deadline) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- New Project Form Modal -->
    <div v-if="showNewProjectForm" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Create New Project</h2>
          <button @click="showNewProjectForm = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="submitProject" class="project-form">
          <div class="form-group">
            <label for="project-name">Project Name *</label>
            <input 
              id="project-name"
              v-model="newProject.name" 
              type="text" 
              required
              :class="{ error: errors.name }"
              @blur="validateField('name')"
            >
            <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
          </div>

          <div class="form-group">
            <label for="project-description">Description *</label>
            <textarea 
              id="project-description"
              v-model="newProject.description" 
              required
              :class="{ error: errors.description }"
              @blur="validateField('description')"
            ></textarea>
            <span v-if="errors.description" class="error-text">{{ errors.description }}</span>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="project-team">Team</label>
              <select id="project-team" v-model="newProject.teamId">
                <option value="">Select Team</option>
                <option v-for="team in teams" :key="team.id" :value="team.id">
                  {{ team.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="project-deadline">Deadline *</label>
              <input 
                id="project-deadline"
                v-model="newProject.deadline" 
                type="date" 
                required
                :class="{ error: errors.deadline }"
                @blur="validateField('deadline')"
              >
              <span v-if="errors.deadline" class="error-text">{{ errors.deadline }}</span>
            </div>
          </div>

          <div class="form-group">
            <label>Team Members</label>
            <div class="member-checkboxes">
              <label 
                v-for="member in filteredMembers" 
                :key="member.id"
                class="checkbox-label"
              >
                <input 
                  type="checkbox" 
                  :value="member.id" 
                  v-model="newProject.teamMembers"
                >
                <span>{{ member.name }}</span>
              </label>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="showNewProjectForm = false" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Team Member Form Modal -->
    <div v-if="showTeamForm" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Add Team Member</h2>
          <button @click="showTeamForm = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="submitTeamMember" class="team-form">
          <div class="form-group">
            <label for="member-name">Name *</label>
            <input 
              id="member-name"
              v-model="newMember.name" 
              type="text" 
              required
              :class="{ error: memberErrors.name }"
              @blur="validateMemberField('name')"
            >
            <span v-if="memberErrors.name" class="error-text">{{ memberErrors.name }}</span>
          </div>

          <div class="form-group">
            <label for="member-email">Email *</label>
            <input 
              id="member-email"
              v-model="newMember.email" 
              type="email" 
              required
              :class="{ error: memberErrors.email }"
              @blur="validateMemberField('email')"
            >
            <span v-if="memberErrors.email" class="error-text">{{ memberErrors.email }}</span>
          </div>

          <div class="form-group">
            <label for="member-role">Role</label>
            <select id="member-role" v-model="newMember.role">
              <option value="developer">Developer</option>
              <option value="designer">Designer</option>
              <option value="manager">Manager</option>
              <option value="analyst">Analyst</option>
            </select>
          </div>

          <div class="form-group">
            <label for="member-team">Team</label>
            <select id="member-team" v-model="newMember.teamId">
              <option value="">Select Team</option>
              <option v-for="team in teams" :key="team.id" :value="team.id">
                {{ team.name }}
              </option>
            </select>
          </div>

          <div class="form-actions">
            <button type="button" @click="showTeamForm = false" class="btn-secondary">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              Add Member
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EnhancedDashboard',
  data() {
    return {
      selectedTeam: '',
      selectedMembers: [],
      projectFilter: 'all',
      viewMode: 'grid',
      showNewProjectForm: false,
      showTeamForm: false,
      
      // Form data
      newProject: {
        name: '',
        description: '',
        teamId: '',
        deadline: '',
        teamMembers: []
      },
      newMember: {
        name: '',
        email: '',
        role: 'developer',
        teamId: ''
      },

      // Validation errors
      errors: {},
      memberErrors: {},

      // Sample data
      teams: [
        { id: 1, name: 'Frontend Team', color: '#3b82f6' },
        { id: 2, name: 'Backend Team', color: '#10b981' },
        { id: 3, name: 'Design Team', color: '#f59e0b' },
        { id: 4, name: 'QA Team', color: '#ef4444' }
      ],

      members: [
        { id: 1, name: 'Alice Johnson', email: 'alice@company.com', role: 'developer', teamId: 1, avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b17c?w=40&h=40&fit=crop&crop=face' },
        { id: 2, name: 'Bob Smith', email: 'bob@company.com', role: 'designer', teamId: 3, avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face' },
        { id: 3, name: 'Carol Davis', email: 'carol@company.com', role: 'manager', teamId: 2, avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=40&h=40&fit=crop&crop=face' },
        { id: 4, name: 'David Wilson', email: 'david@company.com', role: 'developer', teamId: 1, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=40&h=40&fit=crop&crop=face' },
        { id: 5, name: 'Eva Brown', email: 'eva@company.com', role: 'analyst', teamId: 4, avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=40&h=40&fit=crop&crop=face' }
      ],

      projects: [
        {
          id: 1,
          name: 'E-commerce Platform',
          description: 'Building a modern e-commerce platform with Vue.js and Node.js',
          status: 'active',
          progress: 75,
          deadline: '2025-08-15',
          teamMembers: [1, 2, 4]
        },
        {
          id: 2,
          name: 'Mobile App Redesign',
          description: 'Complete redesign of our mobile application',
          status: 'active',
          progress: 45,
          deadline: '2025-09-30',
          teamMembers: [2, 3]
        },
        {
          id: 3,
          name: 'API Documentation',
          description: 'Comprehensive API documentation for developers',
          status: 'completed',
          progress: 100,
          deadline: '2025-07-01',
          teamMembers: [3, 5]
        },
        {
          id: 4,
          name: 'Database Migration',
          description: 'Migrating legacy database to new infrastructure',
          status: 'overdue',
          progress: 30,
          deadline: '2025-07-20',
          teamMembers: [1, 3, 4]
        }
      ]
    }
  },

  computed: {
    filteredMembers() {
      if (!this.selectedTeam) return this.members;
      return this.members.filter(member => member.teamId == this.selectedTeam);
    },

    filteredProjects() {
      let projects = this.projects;

      // Filter by project status
      if (this.projectFilter !== 'all') {
        projects = projects.filter(project => project.status === this.projectFilter);
      }

      // Filter by selected members
      if (this.selectedMembers.length > 0) {
        projects = projects.filter(project => 
          project.teamMembers.some(memberId => this.selectedMembers.includes(memberId))
        );
      }

      return projects;
    },

    activeProjects() {
      return this.projects.filter(project => project.status === 'active');
    },

    completionRate() {
      if (this.projects.length === 0) return 0;
      const completed = this.projects.filter(project => project.status === 'completed').length;
      return Math.round((completed / this.projects.length) * 100);
    }
  },

  methods: {
    filterByTeam() {
      this.selectedMembers = [];
    },

    toggleMember(memberId) {
      const index = this.selectedMembers.indexOf(memberId);
      if (index > -1) {
        this.selectedMembers.splice(index, 1);
      } else {
        this.selectedMembers.push(memberId);
      }
    },

    setProjectFilter(filter) {
      this.projectFilter = filter;
    },

    getMemberById(id) {
      return this.members.find(member => member.id === id);
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },

    isOverdue(deadline) {
      return new Date(deadline) < new Date();
    },

    closeModal() {
      this.showNewProjectForm = false;
      this.showTeamForm = false;
      this.errors = {};
      this.memberErrors = {};
    },

    // Form validation
    validateField(field) {
      this.errors = { ...this.errors };
      
      switch(field) {
        case 'name':
          if (!this.newProject.name || this.newProject.name.length < 3) {
            this.errors.name = 'Project name must be at least 3 characters';
          } else {
            delete this.errors.name;
          }
          break;
        case 'description':
          if (!this.newProject.description || this.newProject.description.length < 10) {
            this.errors.description = 'Description must be at least 10 characters';
          } else {
            delete this.errors.description;
          }
          break;
        case 'deadline':
          if (!this.newProject.deadline) {
            this.errors.deadline = 'Deadline is required';
          } else if (new Date(this.newProject.deadline) < new Date()) {
            this.errors.deadline = 'Deadline cannot be in the past';
          } else {
            delete this.errors.deadline;
          }
          break;
      }
    },

    validateMemberField(field) {
      this.memberErrors = { ...this.memberErrors };
      
      switch(field) {
        case 'name':
          if (!this.newMember.name || this.newMember.name.length < 2) {
            this.memberErrors.name = 'Name must be at least 2 characters';
          } else {
            delete this.memberErrors.name;
          }
          break;
        case 'email':
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!this.newMember.email) {
            this.memberErrors.email = 'Email is required';
          } else if (!emailRegex.test(this.newMember.email)) {
            this.memberErrors.email = 'Please enter a valid email';
          } else {
            delete this.memberErrors.email;
          }
          break;
      }
    },

    // Form submissions
    async submitProject() {
      // Validate all fields
      this.validateField('name');
      this.validateField('description');
      this.validateField('deadline');

      if (Object.keys(this.errors).length > 0) {
        return;
      }

      try {
        // Simulate API call
        await this.createProject(this.newProject);
        
        // Reset form
        this.newProject = {
          name: '',
          description: '',
          teamId: '',
          deadline: '',
          teamMembers: []
        };
        this.showNewProjectForm = false;
        
        alert('Project created successfully!');
      } catch (error) {
        alert('Error creating project: ' + error.message);
      }
    },

    async submitTeamMember() {
      // Validate all fields
      this.validateMemberField('name');
      this.validateMemberField('email');

      if (Object.keys(this.memberErrors).length > 0) {
        return;
      }

      try {
        // Simulate API call
        await this.createTeamMember(this.newMember);
        
        // Reset form
        this.newMember = {
          name: '',
          email: '',
          role: 'developer',
          teamId: ''
        };
        this.showTeamForm = false;
        
        alert('Team member added successfully!');
      } catch (error) {
        alert('Error adding team member: ' + error.message);
      }
    },

    // Simulate API calls
    async createProject(projectData) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const newProject = {
            ...projectData,
            id: this.projects.length + 1,
            status: 'active',
            progress: 0
          };
          this.projects.push(newProject);
          resolve(newProject);
        }, 1000);
      });
    },

    async createTeamMember(memberData) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const newMember = {
            ...memberData,
            id: this.members.length + 1,
            avatar: `https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=40&h=40&fit=crop&crop=face`
          };
          this.members.push(newMember);
          resolve(newMember);
        }, 1000);
      });
    }
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard-container {
  min-height: 100vh;
  background: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header Styles */
.dashboard-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 1rem 2rem;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.leadership-section {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  align-items: center;
}

.team-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.team-select {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
}

.member-toggle {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.member-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.member-btn:hover, .member-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.member-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

/* Main Layout */
.dashboard-main {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  gap: 2rem;
  padding: 2rem;
}

/* Sidebar */
.dashboard-sidebar {
  width: 280px;
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  height: fit-content;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-section {
  margin-bottom: 2rem;
}

.nav-section h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
}

.project-filters {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-btn, .action-btn {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
}

.filter-btn:hover, .filter-btn.active {
  background: #f3f4f6;
  border-color: #3b82f6;
}

.action-btn {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  text-align: center;
}

.action-btn:hover {
  background: #2563eb;
}

/* Main Content */
.dashboard-content {
  flex: 1;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
}

/* Projects Section */
.projects-section {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.view-controls {
  display: flex;
  gap: 0.5rem;
}

.view-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.view-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* Projects Container */
.projects-container.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.projects-container.list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.project-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1.5rem;
  background: #fafafa;
  transition: all 0.2s;
}

.project-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.projects-container.list .project-card {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.project-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.active {
  background: #dbeafe;
  color: #1d4ed8;
}

.status-badge.completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.overdue {
  background: #fee2e2;
  color: #dc2626;
}

.project-description {
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.project-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.projects-container.list .project-meta {
  flex-direction: row;
  align-items: center;
  gap: 2rem;
}

.meta-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.project-team {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.team-avatars {
  display: flex;
  gap: 0.25rem;
}

.team-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid white;
}

.project-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar {
  width: 100px;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.875rem;
  color: #6b7280;
}

.project-deadline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.overdue {
  color: #dc2626;
  font-weight: 500;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}

.close-btn:hover {
  color: #374151;
}

/* Form Styles */
.project-form, .team-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group input.error,
.form-group textarea.error {
  border-color: #dc2626;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.error-text {
  color: #dc2626;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: block;
}

.member-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.checkbox-label:hover {
  background: #f9fafb;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: white;
  color: #374151;
  border-color: #d1d5db;
}

.btn-secondary:hover {
  background: #f9fafb;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .dashboard-main {
    flex-direction: column;
    padding: 1rem;
  }
  
  .dashboard-sidebar {
    width: 100%;
  }
  
  .leadership-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 1rem;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .projects-container.grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .project-meta {
    gap: 0.5rem;
  }
  
  .projects-container.list .project-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .member-checkboxes {
    grid-template-columns: 1fr;
  }
  
  .modal-overlay {
    padding: 0.5rem;
  }
}

@media (max-width: 480px) {
  .member-toggle {
    width: 100%;
  }
  
  .member-btn {
    flex: 1;
    justify-content: center;
    min-width: 0;
  }
  
  .member-btn span {
    display: none;
  }
  
  .project-card {
    padding: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
  }
}
</style>