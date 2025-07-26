<template>
  <div class="container">
    <h2>Submit Performance Feedback</h2>

    <form @submit.prevent="handleSubmit">
      <!-- Project Selection -->
      <div class="form-group">
        <label for="project_select">Select Project</label>
        <select
          id="project_select"
          v-model="selectedProjectId"
          @change="loadExistingFeedback"
          required
          :disabled="loading"
        >
          <option value="">Choose a project...</option>
          <option
            v-for="project in projects"
            :key="project.id"
            :value="project.id"
          >
            {{ project.title }}
          </option>
        </select>
      </div>

      <!-- Show form only if project is selected -->
      <div v-if="selectedProjectId">
        <!-- Project Management -->
        <div class="slider-section">
          <label for="project_management">Project Management</label>
          <p class="reflection-question">How well did I manage tasks, time, and goals in this project?</p>
          <input
            type="range"
            id="project_management"
            min="1"
            max="7"
            v-model="projectManagement"
            :disabled="loading"
          />
          <div class="slider-labels">
            <span v-for="n in 7" :key="n">{{ n }}</span>
          </div>
          <div class="value-display">Selected: {{ projectManagement }}</div>
        </div>

        <!-- Leadership -->
        <div class="slider-section leadership-section">
          <label for="leadership">Leadership</label>
          <p class="reflection-question">Did I inspire, support, and guide my teammates effectively?</p>
          <input
            type="range"
            id="leadership"
            min="1"
            max="7"
            v-model="leadership"
            :disabled="loading"
          />
          <div class="slider-labels">
            <span v-for="n in 7" :key="n">{{ n }}</span>
          </div>
          <div class="value-display">Selected: {{ leadership }}</div>
        </div>

        <!-- Organizational Change Management -->
        <div class="slider-section change-section">
          <label for="organizational_change">Organizational Change Management</label>
          <p class="reflection-question">How well did I adapt to or support changes in this project?</p>
          <input
            type="range"
            id="organizational_change"
            min="1"
            max="7"
            v-model="organizationalChange"
            :disabled="loading"
          />
          <div class="slider-labels">
            <span v-for="n in 7" :key="n">{{ n }}</span>
          </div>
          <div class="value-display">Selected: {{ organizationalChange }}</div>
        </div>

        <button type="submit" :disabled="loading || !selectedProjectId">
          {{ loading ? 'Submitting...' : 'Submit Feedback' }}
        </button>
      </div>
    </form>

    <!-- Success/Error Messages -->
    <div v-if="message" :class="messageClass">
      {{ message }}
    </div>

    <!-- Loading indicator -->
    <div v-if="loading" class="loading-indicator">
      <p>{{ loadingMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "PerformanceSlider",
  data() {
    return {
      selectedProjectId: '',
      projects: [],
      projectManagement: 4,
      leadership: 4,
      organizationalChange: 4,
      loading: false,
      loadingMessage: '',
      message: '',
      messageClass: 'message'
    };
  },
  async mounted() {
    await this.loadProjects();
  },
  methods: {
    async loadProjects() {
      this.loading = true;
      this.loadingMessage = 'Loading your projects...';

      try {
        const result = await this.$projectService.getProjects({
          status: 'active' // Only show active projects
        });

        if (result.success) {
          this.projects = result.results || [];

          // Auto-select first project if only one exists
          if (this.projects.length === 1) {
            this.selectedProjectId = this.projects[0].id;
            await this.loadExistingFeedback();
          }
        } else {
          this.showError('Failed to load projects: ' + result.error);
        }
      } catch (error) {
        console.error('Error loading projects:', error);
        this.showError('Failed to load projects. Please try again.');
      } finally {
        this.loading = false;
        this.loadingMessage = '';
      }
    },

    async loadExistingFeedback() {
      if (!this.selectedProjectId) return;

      this.loading = true;
      this.loadingMessage = 'Loading existing feedback...';

      try {
        const result = await this.$feedbackService.getSliderFeedback(this.selectedProjectId);

        if (result.success && result.results.length > 0) {
          // Load existing scores for this project
          result.results.forEach(feedback => {
            if (feedback.category === 'PM') {
              this.projectManagement = feedback.score;
            } else if (feedback.category === 'Leadership') {
              this.leadership = feedback.score;
            } else if (feedback.category === 'ChangeMgmt') {
              this.organizationalChange = feedback.score;
            }
          });

          this.showSuccess('Loaded your previous feedback for this project.');
        }
      } catch (error) {
        console.error('Error loading existing feedback:', error);
        // Don't show error for this since it's optional
      } finally {
        this.loading = false;
        this.loadingMessage = '';
      }
    },

    async handleSubmit() {
      if (!this.selectedProjectId) {
        this.showError('Please select a project first.');
        return;
      }

      this.loading = true;
      this.loadingMessage = 'Submitting your feedback...';

      try {
        // Submit each category separately as your backend expects
        const submissions = [
          { category: 'PM', score: parseInt(this.projectManagement) },
          { category: 'Leadership', score: parseInt(this.leadership) },
          { category: 'ChangeMgmt', score: parseInt(this.organizationalChange) }
        ];

        let successCount = 0;
        for (const submission of submissions) {
          const result = await this.$feedbackService.submitSliderFeedback({
            project_id: this.selectedProjectId,
            category: submission.category,
            score: submission.score
          });

          if (result.success) {
            successCount++;
          } else {
            console.error(`Failed to submit ${submission.category}:`, result.error);
          }
        }

        if (successCount === submissions.length) {
          this.showSuccess('All feedback submitted successfully!');

          // Emit event to parent component for chart updates
          this.$emit('submit-feedback', {
            projectManagement: this.projectManagement,
            leadership: this.leadership,
            organizationalChange: this.organizationalChange
          });
        } else if (successCount > 0) {
          this.showWarning(`${successCount} out of ${submissions.length} feedback items submitted successfully.`);
        } else {
          this.showError('Failed to submit feedback. Please try again.');
        }

      } catch (error) {
        console.error('Submission error:', error);
        this.showError('An error occurred while submitting feedback. Please try again.');
      } finally {
        this.loading = false;
        this.loadingMessage = '';
      }
    },

    showError(message) {
      this.message = message;
      this.messageClass = 'message error';
      this.clearMessageAfterDelay();
    },

    showSuccess(message) {
      this.message = message;
      this.messageClass = 'message success';
      this.clearMessageAfterDelay();
    },

    showWarning(message) {
      this.message = message;
      this.messageClass = 'message warning';
      this.clearMessageAfterDelay();
    },

    clearMessageAfterDelay() {
      setTimeout(() => {
        this.message = '';
      }, 5000);
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

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: 600;
  margin-top: 25px;
  display: block;
  color: #1e2a38;
}

input[type="text"], select {
  width: 100%;
  padding: 10px 14px;
  font-size: 1rem;
  margin-top: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus, select:focus {
  border-color: #1a73e8;
}

select:disabled, input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

input[type=range]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

button:hover:not(:disabled) {
  background-color: #0f5bb5;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 6px;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message.warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.loading-indicator {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-style: italic;
}
</style>