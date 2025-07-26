<template>
  <div class="career-development-container">
    <!-- Header Section -->
    <div class="module-header">
      <div class="header-content">
        <h2>Career Development</h2>
        <p class="header-description">Track and manage team member skill development goals</p>
      </div>
      <button @click="showForm = true" class="add-goal-btn">
        <i class="icon-plus"></i>
        Add Development Goal
      </button>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="form-modal-overlay" @click="closeForm">
      <div class="form-modal" @click.stop>
        <div class="form-header">
          <h3>{{ editMode ? 'Edit' : 'Add' }} Career Development Goal</h3>
          <button @click="closeForm" class="close-button">×</button>
        </div>
        
        <form @submit.prevent="submitForm" class="career-form">
          <!-- Team Member Selection -->
          <div class="form-group">
            <label for="teamMember" class="form-label">Team Member*</label>
            <select 
              id="teamMember"
              v-model="form.teamMemberId" 
              required
              :class="{ error: errors.teamMemberId }"
              class="form-select"
            >
              <option value="">Select Team Member</option>
              <option 
                v-for="member in teamMembers" 
                :key="member.id" 
                :value="member.id"
              >
                {{ member.name }} - {{ member.role }}
              </option>
            </select>
            <span v-if="errors.teamMemberId" class="error-message">{{ errors.teamMemberId }}</span>
          </div>

          <!-- Skill Information -->
          <div class="form-row">
            <div class="form-group">
              <label for="skillName" class="form-label">Skill Name*</label>
              <input 
                id="skillName"
                v-model="form.skillName" 
                type="text" 
                required
                :class="{ error: errors.skillName }"
                class="form-input"
                placeholder="e.g., Vue.js, Project Management"
              >
              <span v-if="errors.skillName" class="error-message">{{ errors.skillName }}</span>
            </div>

            <div class="form-group">
              <label for="category" class="form-label">Category</label>
              <select 
                id="category"
                v-model="form.category" 
                class="form-select"
              >
                <option value="">Select Category</option>
                <option value="technical">Technical</option>
                <option value="management">Management</option>
                <option value="communication">Communication</option>
                <option value="design">Design</option>
                <option value="analytics">Analytics</option>
              </select>
            </div>
          </div>

          <!-- Current and Target Levels -->
          <div class="form-row">
            <div class="form-group">
              <label for="currentLevel" class="form-label">Current Level*</label>
              <select 
                id="currentLevel"
                v-model="form.currentLevel" 
                required
                :class="{ error: errors.currentLevel }"
                class="form-select"
              >
                <option value="">Select Level</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="expert">Expert</option>
              </select>
              <span v-if="errors.currentLevel" class="error-message">{{ errors.currentLevel }}</span>
            </div>

            <div class="form-group">
              <label for="targetLevel" class="form-label">Target Level*</label>
              <select 
                id="targetLevel"
                v-model="form.targetLevel" 
                required
                :class="{ error: errors.targetLevel }"
                class="form-select"
              >
                <option value="">Select Level</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="expert">Expert</option>
              </select>
              <span v-if="errors.targetLevel" class="error-message">{{ errors.targetLevel }}</span>
            </div>
          </div>

          <!-- Timeline and Priority -->
          <div class="form-row">
            <div class="form-group">
              <label for="targetDate" class="form-label">Target Date*</label>
              <input 
                id="targetDate"
                v-model="form.targetDate" 
                type="date" 
                required
                :class="{ error: errors.targetDate }"
                class="form-input"
                :min="minDate"
              >
              <span v-if="errors.targetDate" class="error-message">{{ errors.targetDate }}</span>
            </div>

            <div class="form-group">
              <label for="priority" class="form-label">Priority</label>
              <select 
                id="priority"
                v-model="form.priority" 
                class="form-select"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>

          <!-- Progress Tracking -->
          <div class="form-group">
            <label for="currentProgress" class="form-label">
              Current Progress: {{ form.currentProgress }}%
            </label>
            <input 
              id="currentProgress"
              type="range"
              v-model="form.currentProgress"
              min="0"
              max="100"
              class="progress-slider"
            >
            <div class="progress-indicators">
              <span>0%</span>
              <span>25%</span>
              <span>50%</span>
              <span>75%</span>
              <span>100%</span>
            </div>
          </div>

          <!-- Learning Resources -->
          <div class="form-group">
            <label for="resources" class="form-label">Learning Resources</label>
            <div class="resources-container">
              <div 
                v-for="(resource, index) in form.resources" 
                :key="index"
                class="resource-item"
              >
                <input 
                  v-model="resource.name"
                  placeholder="Resource name"
                  class="resource-input"
                >
                <input 
                  v-model="resource.url"
                  placeholder="URL (optional)"
                  class="resource-input"
                >
                <button 
                  type="button" 
                  @click="removeResource(index)"
                  class="remove-resource-btn"
                >
                  ×
                </button>
              </div>
              <button 
                type="button" 
                @click="addResource"
                class="add-resource-btn"
              >
                <i class="icon-plus"></i>
                Add Resource
              </button>
            </div>
          </div>

          <!-- Notes and Description -->
          <div class="form-group">
            <label for="notes" class="form-label">Notes & Learning Plan</label>
            <textarea 
              id="notes"
              v-model="form.notes" 
              rows="4"
              class="form-textarea"
              placeholder="Describe the learning plan, milestones, or any additional notes..."
            ></textarea>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <button type="button" @click="closeForm" class="cancel-button">
              Cancel
            </button>
            <button type="submit" class="submit-button" :disabled="isSubmitting">
              <span v-if="isSubmitting">Saving...</span>
              <span v-else>{{ editMode ? 'Update' : 'Create' }} Goal</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Career Goals List -->
    <div class="goals-container">
      <!-- Filter and Search -->
      <div class="goals-filters">
        <div class="filter-group">
          <select v-model="filters.category" class="filter-select">
            <option value="">All Categories</option>
            <option value="technical">Technical</option>
            <option value="management">Management</option>
            <option value="communication">Communication</option>
            <option value="design">Design</option>
            <option value="analytics">Analytics</option>
          </select>
          <select v-model="filters.priority" class="filter-select">
            <option value="">All Priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <select v-model="filters.teamMember" class="filter-select">
            <option value="">All Team Members</option>
            <option 
              v-for="member in teamMembers" 
              :key="member.id" 
              :value="member.id"
            >
              {{ member.name }}
            </option>
          </select>
        </div>
        <input 
          v-model="filters.search"
          placeholder="Search skills..."
          class="search-input"
        >
      </div>

      <!-- Goals Grid -->
      <div class="goals-grid">
        <div 
          v-for="goal in filteredGoals" 
          :key="goal.id"
          class="goal-card"
        >
          <!-- Goal Header -->
          <div class="goal-header">
            <div class="goal-title-section">
              <h4 class="goal-title">{{ goal.skillName }}</h4>
              <div class="goal-meta">
                <span :class="'category-badge category-' + goal.category">{{ goal.category }}</span>
                <span :class="'priority-badge priority-' + goal.priority">{{ goal.priority }}</span>
              </div>
            </div>
            <div class="goal-actions">
              <button @click="editGoal(goal)" class="action-btn edit">
                <i class="icon-edit"></i>
              </button>
              <button @click="deleteGoal(goal.id)" class="action-btn delete">
                <i class="icon-trash"></i>
              </button>
            </div>
          </div>

          <!-- Team Member Info -->
          <div class="team-member-info">
            <img :src="goal.teamMember.avatar" :alt="goal.teamMember.name" class="member-avatar">
            <div class="member-details">
              <span class="member-name">{{ goal.teamMember.name }}</span>
              <span class="member-role">{{ goal.teamMember.role }}</span>
            </div>
          </div>
          
          <!-- Level Progression -->
          <div class="level-progression">
            <div class="level-item current">
              <span class="level-label">Current</span>
              <span :class="'level-badge level-' + goal.currentLevel">{{ goal.currentLevel }}</span>
            </div>
            <div class="progression-arrow">
              <i class="icon-arrow-right"></i>
            </div>
            <div class="level-item target">
              <span class="level-label">Target</span>
              <span :class="'level-badge level-' + goal.targetLevel">{{ goal.targetLevel }}</span>
            </div>
          </div>
          
          <!-- Progress Bar -->
          <div class="progress-section">
            <div class="progress-header">
              <span class="progress-label">Progress</span>
              <span class="progress-percentage">{{ goal.currentProgress }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: goal.currentProgress + '%' }"
                :class="getProgressColor(goal.currentProgress)"
              ></div>
            </div>
          </div>

          <!-- Learning Resources -->
          <div v-if="goal.resources && goal.resources.length > 0" class="resources-section">
            <h5>Learning Resources</h5>
            <div class="resources-list">
              <a 
                v-for="resource in goal.resources" 
                :key="resource.name"
                :href="resource.url" 
                target="_blank"
                class="resource-link"
              >
                <i class="icon-external-link"></i>
                {{ resource.name }}
              </a>
            </div>
          </div>

          <!-- Notes -->
          <div v-if="goal.notes" class="notes-section">
            <h5>Notes</h5>
            <p class="goal-notes">{{ goal.notes }}</p>
          </div>
          
          <!-- Goal Footer -->
          <div class="goal-footer">
            <div class="target-date">
              <i class="icon-calendar"></i>
              <span>Target: {{ formatDate(goal.targetDate) }}</span>
            </div>
            <div class="last-update">
              <i class="icon-clock"></i>
              <span>Updated {{ formatRelativeDate(goal.updatedAt) }}</span>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredGoals.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="icon-target"></i>
          </div>
          <h3>No Career Goals Found</h3>
          <p>Start tracking team member development by adding career goals.</p>
          <button @click="showForm = true" class="add-first-goal-btn">
            Add First Goal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CareerDevelopmentForm',
  data() {
    return {
      // ... existing data
      careerGoals: [], // Will be loaded from backend
      teamMembers: [], // Will be loaded from backend
      loading: false
    };
  },
  async mounted() {
    await this.loadData();
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        // Load career goals and team members from backend
        const [careerData, teamData] = await Promise.all([
          this.$careerService.getCareerForms(),
          this.$projectService.getProjects() // To get team members
        ]);

        this.careerGoals = careerData.results || [];
        // Extract team members from projects
        this.extractTeamMembers(teamData.results || []);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        this.loading = false;
      }
    },

    extractTeamMembers(projects) {
      const members = new Map();
      projects.forEach(project => {
        project.assigned_users?.forEach(user => {
          members.set(user.id, {
            id: user.id,
            name: user.first_name + ' ' + user.last_name,
            role: user.role,
            avatar: user.avatar || '/api/placeholder/40/40'
          });
        });
      });
      this.teamMembers = Array.from(members.values());
    },

    async submitForm() {
      if (!this.validateForm()) return;

      this.isSubmitting = true;
      try {
        const formData = {
          skill_name: this.form.skillName,
          category: this.form.category,
          current_level: this.form.currentLevel,
          target_level: this.form.targetLevel,
          target_date: this.form.targetDate,
          priority: this.form.priority,
          current_progress: this.form.currentProgress,
          resources: this.form.resources.filter(r => r.name.trim()),
          notes: this.form.notes
        };

        if (this.editMode) {
          await this.$careerService.updateCareerForm(this.editingGoalId, formData);
        } else {
          await this.$careerService.createCareerForm(formData);
        }

        await this.loadData(); // Refresh data
        this.closeForm();

      } catch (error) {
        console.error('Error saving goal:', error);
        alert('Failed to save goal: ' + error.message);
      } finally {
        this.isSubmitting = false;
      }
    },

    async deleteGoal(goalId) {
      if (confirm('Are you sure you want to delete this career goal?')) {
        try {
          await this.$careerService.deleteCareerForm(goalId);
          await this.loadData(); // Refresh data
        } catch (error) {
          console.error('Error deleting goal:', error);
          alert('Failed to delete goal: ' + error.message);
        }
      }
    }
  }
};
</script>

<style scoped>
.career-development-container {
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.header-content h2 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.875rem;
  font-weight: 700;
}

.header-description {
  margin: 0;
  color: #64748b;
  font-size: 1rem;
}

.add-goal-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-goal-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

/* Form Modal Styles */
.form-modal-overlay {
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
  padding: 2rem;
}

.form-modal {
  background: white;
  border-radius: 1rem;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.form-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.close-button:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.career-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 500;
  font-size: 0.875rem;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input.error, .form-select.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.error-message {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: block;
}

.progress-slider {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.progress-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: #3b82f6;
  border-radius: 50%;
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.progress-indicators {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #64748b;
}

.resources-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.resource-item {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.resource-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.remove-resource-btn {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.add-resource-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f1f5f9;
  border: 1px dashed #d1d5db;
  border-radius: 0.375rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.add-resource-btn:hover {
  background: #e2e8f0;
  border-color: #9ca3af;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

.cancel-button, .submit-button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.cancel-button {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.cancel-button:hover {
  background: #f1f5f9;
}

.submit-button {
  background: #3b82f6;
  color: white;
}

.submit-button:hover:not(:disabled) {
  background: #2563eb;
}

.submit-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Goals Container Styles */
.goals-container {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  overflow: hidden;
}

.goals-filters {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.filter-group {
  display: flex;
  gap: 0.75rem;
  flex: 1;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background: white;
}

.search-input {
  width: 250px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.goal-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.goal-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.goal-title {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.125rem;
  font-weight: 600;
}

.goal-meta {
  display: flex;
  gap: 0.5rem;
}

.category-badge, .priority-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.category-technical { background: #dbeafe; color: #1e40af; }
.category-management { background: #f3e8ff; color: #7c3aed; }
.category-communication { background: #dcfce7; color: #166534; }
.category-design { background: #fef3c7; color: #92400e; }
.category-analytics { background: #fee2e2; color: #991b1b; }

.priority-critical { background: #fee2e2; color: #991b1b; }
.priority-high { background: #fef3c7; color: #92400e; }
.priority-medium { background: #dbeafe; color: #1e40af; }
.priority-low { background: #f0f9ff; color: #0369a1; }

.goal-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.edit:hover {
  background: #f0f9ff;
  border-color: #3b82f6;
  color: #3b82f6;
}

.action-btn.delete:hover {
  background: #fef2f2;
  border-color: #ef4444;
  color: #ef4444;
}

.team-member-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.member-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #e2e8f0;
}

.member-details {
  display: flex;
  flex-direction: column;
}

.member-name {
  font-weight: 500;
  color: #1e293b;
}

.member-role {
  font-size: 0.875rem;
  color: #64748b;
}

.level-progression {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.level-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.level-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 500;
}

.level-badge {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
}

/* Add any additional styles here */
</style>