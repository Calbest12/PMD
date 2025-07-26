<template>
  <div class="sliders-container">
    <!-- Header -->
    <div class="sliders-header">
      <div class="header-content">
        <h2>Performance Metrics</h2>
        <p class="header-description">Real-time project and team performance indicators</p>
      </div>
      <div class="header-actions">
        <button @click="resetAllSliders" class="reset-btn">
          <i class="icon-refresh"></i>
          Reset All
        </button>
        <button @click="saveAllChanges" class="save-btn" :disabled="!hasUnsavedChanges">
          <i class="icon-save"></i>
          Save Changes
        </button>
      </div>
    </div>

    <!-- Sliders Grid -->
    <div class="sliders-grid">
      <div 
        v-for="slider in sliders" 
        :key="slider.id"
        class="slider-card"
        :class="{ 'read-only': !slider.isEditable, 'has-changes': slider.hasChanges }"
      >
        <!-- Slider Header -->
        <div class="slider-header">
          <div class="slider-info">
            <h3 class="slider-title">{{ slider.label }}</h3>
            <p class="slider-description">{{ slider.description }}</p>
            <div class="slider-category">
              <span :class="'category-badge category-' + slider.category">{{ slider.category }}</span>
            </div>
          </div>
          <div class="slider-value-display">
            <div class="current-value">{{ slider.currentValue }}</div>
            <div class="value-unit">{{ slider.unit || '%' }}</div>
            <div class="value-range">{{ slider.minValue }} - {{ slider.maxValue }}</div>
          </div>
        </div>

        <!-- Slider Controls -->
        <div class="slider-controls">
          <!-- Main Slider -->
          <div class="slider-wrapper">
            <input 
              type="range"
              :min="slider.minValue"
              :max="slider.maxValue"
              :step="slider.step || 1"
              v-model="slider.currentValue"
              @input="handleSliderInput(slider)"
              @change="handleSliderChange(slider)"
              :disabled="!slider.isEditable"
              class="slider-input"
              :style="{ 
                '--progress': ((slider.currentValue - slider.minValue) / (slider.maxValue - slider.minValue)) * 100 + '%',
                '--color': getSliderColor(slider.currentValue, slider.thresholds)
              }"
            >
            
            <!-- Threshold Markers -->
            <div class="threshold-markers" v-if="slider.thresholds">
              <div 
                v-for="threshold in slider.thresholds" 
                :key="threshold.value"
                class="threshold-marker"
                :style="{ 
                  left: ((threshold.value - slider.minValue) / (slider.maxValue - slider.minValue)) * 100 + '%' 
                }"
                :class="'threshold-' + threshold.type"
                :title="threshold.label + ': ' + threshold.value"
              ></div>
            </div>
          </div>

          <!-- Manual Input -->
          <div class="manual-input" v-if="slider.isEditable">
            <input 
              type="number"
              :min="slider.minValue"
              :max="slider.maxValue"
              :step="slider.step || 1"
              v-model.number="slider.currentValue"
              @input="handleSliderInput(slider)"
              @change="handleSliderChange(slider)"
              class="value-input"
            >
          </div>
        </div>

        <!-- Slider Labels -->
        <div class="slider-labels">
          <span class="min-label">{{ slider.minValue }}{{ slider.unit || '%' }}</span>
          <span class="max-label">{{ slider.maxValue }}{{ slider.unit || '%' }}</span>
        </div>

        <!-- Performance Indicator -->
        <div class="performance-indicator" v-if="slider.thresholds">
          <div class="indicator-bar">
            <div 
              class="indicator-fill"
              :style="{ 
                width: ((slider.currentValue - slider.minValue) / (slider.maxValue - slider.minValue)) * 100 + '%',
                background: getSliderColor(slider.currentValue, slider.thresholds)
              }"
            ></div>
          </div>
          <div class="performance-status">
            <span :class="'status-badge status-' + getPerformanceStatus(slider.currentValue, slider.thresholds)">
              {{ getPerformanceStatus(slider.currentValue, slider.thresholds) }}
            </span>
          </div>
        </div>

        <!-- Real-time Updates -->
        <div class="real-time-updates" v-if="slider.realTimeData">
          <div class="update-indicator">
            <div class="pulse-dot" :class="{ active: slider.isUpdating }"></div>
            <span>{{ slider.isUpdating ? 'Updating...' : 'Live Data' }}</span>
          </div>
          <div class="trend-indicator">
            <i :class="getTrendIcon(slider.trend)"></i>
            <span>{{ slider.trend > 0 ? '+' : '' }}{{ slider.trend }}%</span>
          </div>
        </div>

        <!-- Slider Footer -->
        <div class="slider-footer">
          <div class="update-info">
            <img 
              :src="slider.updatedBy.avatar" 
              :alt="slider.updatedBy.name" 
              class="updater-avatar"
            >
            <div class="update-details">
              <span class="updater-name">{{ slider.updatedBy.name }}</span>
              <span class="update-time">{{ formatTime(slider.updatedAt) }}</span>
            </div>
          </div>
          
          <div class="slider-actions" v-if="slider.isEditable">
            <button 
              @click="revertSlider(slider)" 
              class="action-btn revert"
              v-if="slider.hasChanges"
              title="Revert changes"
            >
              <i class="icon-undo"></i>
            </button>
            <button 
              @click="lockSlider(slider)" 
              class="action-btn lock"
              title="Lock slider"
            >
              <i class="icon-lock"></i>
            </button>
          </div>
          
          <div class="locked-indicator" v-else>
            <i class="icon-lock"></i>
            <span>Read Only</span>
          </div>
        </div>

        <!-- Change History -->
        <div class="change-history" v-if="slider.showHistory && slider.history">
          <h4>Recent Changes</h4>
          <div class="history-list">
            <div 
              v-for="change in slider.history.slice(0, 3)" 
              :key="change.id"
              class="history-item"
            >
              <div class="change-info">
                <span class="change-value">{{ change.oldValue }} → {{ change.newValue }}</span>
                <span class="change-user">by {{ change.user }}</span>
              </div>
              <span class="change-time">{{ formatTime(change.timestamp) }}</span>
            </div>
          </div>
          <button 
            @click="toggleHistory(slider)" 
            class="toggle-history-btn"
          >
            {{ slider.showHistory ? 'Hide' : 'Show' }} History
          </button>
        </div>
      </div>
    </div>

    <!-- Bulk Actions -->
    <div class="bulk-actions" v-if="hasUnsavedChanges">
      <div class="bulk-info">
        <i class="icon-info-circle"></i>
        <span>{{ unsavedChangesCount }} slider(s) have unsaved changes</span>
      </div>
      <div class="bulk-buttons">
        <button @click="revertAllChanges" class="bulk-btn revert">
          Revert All
        </button>
        <button @click="saveAllChanges" class="bulk-btn save">
          Save All Changes
        </button>
      </div>
    </div>

    <!-- Change Confirmation Modal -->
    <div v-if="showConfirmation" class="confirmation-modal-overlay" @click="closeConfirmation">
      <div class="confirmation-modal" @click.stop>
        <div class="modal-header">
          <h3>Confirm Changes</h3>
          <button @click="closeConfirmation" class="close-btn">×</button>
        </div>
        <div class="modal-content">
          <p>Are you sure you want to save the following changes?</p>
          <ul class="changes-list">
            <li v-for="change in pendingChanges" :key="change.id">
              <strong>{{ change.label }}:</strong> 
              {{ change.oldValue }} → {{ change.newValue }}
            </li>
          </ul>
        </div>
        <div class="modal-actions">
          <button @click="closeConfirmation" class="cancel-btn">Cancel</button>
          <button @click="confirmSave" class="confirm-btn">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditableSliders',
  data() {
    return {
      showConfirmation: false,
      pendingChanges: [],
      sliders: [
        {
          id: 1,
          label: 'Project Progress',
          description: 'Overall completion percentage of current project phase',
          category: 'progress',
          currentValue: 75,
          originalValue: 75,
          maxValue: 100,
          minValue: 0,
          step: 1,
          unit: '%',
          isEditable: true,
          hasChanges: false,
          isUpdating: false,
          realTimeData: true,
          trend: 2.5,
          thresholds: [
            { value: 25, type: 'danger', label: 'Critical' },
            { value: 50, type: 'warning', label: 'At Risk' },
            { value: 75, type: 'success', label: 'On Track' }
          ],
          updatedBy: {
            name: 'Sarah Johnson',
            avatar: '/api/placeholder/32/32'
          },
          updatedAt: '2024-01-15T10:30:00Z',
          showHistory: false,
          history: [
            {
              id: 1,
              oldValue: 70,
              newValue: 75,
              user: 'Sarah Johnson',
              timestamp: '2024-01-15T10:30:00Z'
            },
            {
              id: 2,
              oldValue: 65,
              newValue: 70,
              user: 'Mike Chen',
              timestamp: '2024-01-14T15:20:00Z'
            }
          ]
        },
        {
          id: 2,
          label: 'Team Velocity',
          description: 'Sprint velocity based on story points completed',
          category: 'performance',
          currentValue: 85,
          originalValue: 85,
          maxValue: 100,
          minValue: 0,
          step: 5,
          unit: 'pts',
          isEditable: true,
          hasChanges: false,
          isUpdating: false,
          realTimeData: true,
          trend: -1.2,
          thresholds: [
            { value: 40, type: 'danger', label: 'Poor' },
            { value: 70, type: 'warning', label: 'Average' },
            { value: 85, type: 'success', label: 'Excellent' }
          ],
          updatedBy: {
            name: 'Mike Chen',
            avatar: '/api/placeholder/32/32'
          },
          updatedAt: '2024-01-14T16:45:00Z',
          showHistory: false,
          history: []
        },
        {
          id: 3,
          label: 'Budget Utilization',
          description: 'Percentage of allocated budget currently utilized',
          category: 'budget',
          currentValue: 60,
          originalValue: 60,
          maxValue: 100,
          minValue: 0,
          step: 1,
          unit: '%',
          isEditable: false,
          hasChanges: false,
          isUpdating: true,
          realTimeData: true,
          trend: 3.8,
          thresholds: [
            { value: 80, type: 'warning', label: 'High Usage' },
            { value: 95, type: 'danger', label: 'Over Budget' }
          ],
          updatedBy: {
            name: 'System',
            avatar: '/api/placeholder/32/32'
          },
          updatedAt: '2024-01-15T08:00:00Z',
          showHistory: false,
          history: []
        },
        {
          id: 4,
          label: 'Code Quality',
          description: 'Overall code quality score based on automated analysis',
          category: 'quality',
          currentValue: 92,
          originalValue: 92,
          maxValue: 100,
          minValue: 0,
          step: 1,
          unit: '',
          isEditable: true,
          hasChanges: false,
          isUpdating: false,
          realTimeData: false,
          trend: 0,
          thresholds: [
            { value: 60, type: 'danger', label: 'Poor' },
            { value: 80, type: 'warning', label: 'Good' },
            { value: 90, type: 'success', label: 'Excellent' }
          ],
          updatedBy: {
            name: 'QA System',
            avatar: '/api/placeholder/32/32'
          },
          updatedAt: '2024-01-13T14:20:00Z',
          showHistory: false,
          history: []
        },
        {
          id: 5,
          label: 'Client Satisfaction',
          description: 'Client feedback and satisfaction rating from recent surveys',
          category: 'satisfaction',
          currentValue: 88,
          originalValue: 88,
          maxValue: 100,
          minValue: 0,
          step: 1,
          unit: '%',
          isEditable: true,
          hasChanges: false,
          isUpdating: false,
          realTimeData: false,
          trend: 5.2,
          thresholds: [
            { value: 50, type: 'danger', label: 'Unsatisfied' },
            { value: 75, type: 'warning', label: 'Satisfied' },
            { value: 90, type: 'success', label: 'Highly Satisfied' }
          ],
          updatedBy: {
            name: 'Client Manager',
            avatar: '/api/placeholder/32/32'
          },
          updatedAt: '2024-01-12T11:30:00Z',
          showHistory: false,
          history: []
        },
        {
          id: 6,
          label: 'Timeline Adherence',
          description: 'How well the project is adhering to planned timeline',
          category: 'timeline',
          currentValue: 78,
          originalValue: 78,
          maxValue: 100,
          minValue: 0,
          step: 1,
          unit: '%',
          isEditable: true,
          hasChanges: false,
          isUpdating: false,
          realTimeData: true,
          trend: -0.8,
          thresholds: [
            { value: 50, type: 'danger', label: 'Behind Schedule' },
            { value: 75, type: 'warning', label: 'At Risk' },
            { value: 90, type: 'success', label: 'On Schedule' }
          ],
          updatedBy: {
            name: 'Project Manager',
            avatar: '/api/placeholder/32/32'
          },
          updatedAt: '2024-01-15T09:45:00Z',
          showHistory: false,
          history: []
        }
      ]
    }
  },
  computed: {
    hasUnsavedChanges() {
      return this.sliders.some(slider => slider.hasChanges);
    },
    
    unsavedChangesCount() {
      return this.sliders.filter(slider => slider.hasChanges).length;
    },
    
    changedSliders() {
      return this.sliders.filter(slider => slider.hasChanges);
    }
  },
  mounted() {
    // Simulate real-time updates
    this.startRealTimeUpdates();
  },
  beforeUnmount() {
    if (this.realTimeInterval) {
      clearInterval(this.realTimeInterval);
    }
  },
  methods: {
    handleSliderInput(slider) {
      // Real-time visual feedback during drag
      this.updateSliderState(slider);
    },
    
    handleSliderChange(slider) {
      // Called when user finishes dragging or changing value
      this.updateSliderState(slider);
      this.logSliderChange(slider);
    },
    
    updateSliderState(slider) {
      const hasChanged = slider.currentValue !== slider.originalValue;
      slider.hasChanges = hasChanged;
      
      // Emit real-time update event
      this.$emit('slider-updated', {
        id: slider.id,
        label: slider.label,
        value: slider.currentValue,
        hasChanges: hasChanged
      });
    },
    
    logSliderChange(slider) {
      // Add to history if value actually changed
      if (slider.currentValue !== slider.originalValue) {
        const change = {
          id: Date.now(),
          oldValue: slider.originalValue,
          newValue: slider.currentValue,
          user: 'Current User',
          timestamp: new Date().toISOString()
        };
        
        if (!slider.history) slider.history = [];
        slider.history.unshift(change);
        
        console.log(`Slider "${slider.label}" changed from ${slider.originalValue} to ${slider.currentValue}`);
      }
    },
    
    revertSlider(slider) {
      slider.currentValue = slider.originalValue;
      slider.hasChanges = false;
      
      this.$emit('slider-reverted', {
        id: slider.id,
        label: slider.label,
        value: slider.currentValue
      });
    },
    
    lockSlider(slider) {
      slider.isEditable = false;
      this.$emit('slider-locked', { id: slider.id, label: slider.label });
    },
    
    resetAllSliders() {
      if (confirm('Are you sure you want to reset all sliders to their default values?')) {
        this.sliders.forEach(slider => {
          if (slider.isEditable) {
            slider.currentValue = slider.originalValue;
            slider.hasChanges = false;
          }
        });
        
        this.$emit('all-sliders-reset');
      }
    },
    
    saveAllChanges() {
      this.pendingChanges = this.changedSliders.map(slider => ({
        id: slider.id,
        label: slider.label,
        oldValue: slider.originalValue,
        newValue: slider.currentValue
      }));
      
      this.showConfirmation = true;
    },
    
    confirmSave() {
      // Simulate API call
      this.changedSliders.forEach(slider => {
        slider.originalValue = slider.currentValue;
        slider.hasChanges = false;
        slider.updatedAt = new Date().toISOString();
        slider.updatedBy = {
          name: 'Current User',
          avatar: '/api/placeholder/32/32'
        };
      });
      
      this.$emit('sliders-saved', this.pendingChanges);
      this.closeConfirmation();
      
      console.log('All changes saved successfully');
    },
    
    revertAllChanges() {
      if (confirm('Are you sure you want to revert all unsaved changes?')) {
        this.changedSliders.forEach(slider => {
          this.revertSlider(slider);
        });
      }
    },
    
    closeConfirmation() {
      this.showConfirmation = false;
      this.pendingChanges = [];
    },
    
    toggleHistory(slider) {
      slider.showHistory = !slider.showHistory;
    },
    
    getSliderColor(value, thresholds) {
      if (!thresholds) return '#3b82f6';
      
      const sortedThresholds = [...thresholds].sort((a, b) => a.value - b.value);
      
      for (let i = sortedThresholds.length - 1; i >= 0; i--) {
        if (value >= sortedThresholds[i].value) {
          switch (sortedThresholds[i].type) {
            case 'success': return '#10b981';
            case 'warning': return '#f59e0b';
            case 'danger': return '#ef4444';
            default: return '#3b82f6';
          }
        }
      }
      
      return '#ef4444'; // Default to danger if below all thresholds
    },
    
    getPerformanceStatus(value, thresholds) {
      if (!thresholds) return 'unknown';
      
      const sortedThresholds = [...thresholds].sort((a, b) => a.value - b.value);
      
      for (let i = sortedThresholds.length - 1; i >= 0; i--) {
        if (value >= sortedThresholds[i].value) {
          return sortedThresholds[i].type;
        }
      }
      
      return 'danger';
    },
    
    getTrendIcon(trend) {
      if (trend > 0) return 'icon-trending-up';
      if (trend < 0) return 'icon-trending-down';
      return 'icon-minus';
    },
    
    startRealTimeUpdates() {
      this.realTimeInterval = setInterval(() => {
        this.sliders.forEach(slider => {
          if (slider.realTimeData && !slider.hasChanges) {
            // Small random fluctuations for demo
            const change = (Math.random() - 0.5) * 2;
            const newValue = Math.max(
              slider.minValue,
              Math.min(slider.maxValue, slider.currentValue + change)
            );
            
            if (Math.abs(newValue - slider.currentValue) > 0.1) {
              slider.currentValue = Math.round(newValue * 10) / 10;
              slider.originalValue = slider.currentValue;
              slider.trend = change;
              slider.isUpdating = true;
              
              setTimeout(() => {
                slider.isUpdating = false;
              }, 1000);
            }
          }
        });
      }, 5000); // Update every 5 seconds
    },
    
    formatTime(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffMinutes = Math.floor((now - date) / (1000 * 60));
      
      if (diffMinutes < 1) return 'Just now';
      if (diffMinutes < 60) return `${diffMinutes}m ago`;
      if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`;
      return `${Math.floor(diffMinutes / 1440)}d ago`;
    }
  }
}
</script>

<style scoped>
.sliders-container {
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
  font-family: 'Inter', sans-serif;
}

.sliders-header {
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

.header-actions {
  display: flex;
  gap: 1rem;
}

.reset-btn, .save-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.reset-btn {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.reset-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.save-btn {
  background: #3b82f6;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #2563eb;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sliders-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.slider-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
  position: relative;
}

.slider-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.slider-card.has-changes {
  border-left: 4px solid #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%);
}

.slider-card.read-only {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1.5rem;
}

.slider-info {
  flex: 1;
}

.slider-title {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.125rem;
  font-weight: 600;
}

.slider-description {
  margin: 0 0 0.75rem 0;
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.4;
}

.category-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.category-progress { background: #dbeafe; color: #1e40af; }
.category-performance { background: #dcfce7; color: #166534; }
.category-budget { background: #fef3c7; color: #92400e; }
.category-quality { background: #f3e8ff; color: #7c3aed; }
.category-satisfaction { background: #fee2e2; color: #991b1b; }
.category-timeline { background: #e0f2fe; color: #0369a1; }

.slider-value-display {
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.current-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
}

.value-unit {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: -0.25rem;
}

.value-range {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 0.25rem;
}

.slider-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.slider-wrapper {
  flex: 1;
  position: relative;
}

.slider-input {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  cursor: pointer;
  position: relative;
}

.slider-input::-webkit-slider-track {
  height: 8px;
  background: linear-gradient(to right, 
    var(--color) 0%, 
    var(--color) var(--progress), 
    #e5e7eb var(--progress), 
    #e5e7eb 100%);
  border-radius: 4px;
}

.slider-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  background: var(--color);
  border-radius: 50%;
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  transition: all 0.2s;
}

.slider-input::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.slider-input::-moz-range-track {
  height: 8px;
  background: linear-gradient(to right, 
    var(--color) 0%, 
    var(--color) var(--progress), 
    #e5e7eb var(--progress), 
    #e5e7eb 100%);
  border-radius: 4px;
  border: none;
}

.slider-input::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: var(--color);
  border-radius: 50%;
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.slider-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.threshold-markers {
  position: absolute;
  top: -2px;
  left: 0;
  right: 0;
  height: 12px;
  pointer-events: none;
}

.threshold-marker {
  position: absolute;
  width: 2px;
  height: 12px;
  transform: translateX(-1px);
}

.threshold-marker.threshold-success { background: #10b981; }
.threshold-marker.threshold-warning { background: #f59e0b; }
.threshold-marker.threshold-danger { background: #ef4444; }

.manual-input {
  width: 80px;
}

.value-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  text-align: center;
}

.value-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #94a3b8;
  margin-bottom: 1rem;
}

.performance-indicator {
  margin-bottom: 1rem;
}

.indicator-bar {
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.indicator-fill {
  height: 100%;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.performance-status {
  display: flex;
  justify-content: center;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-success { background: #dcfce7; color: #166534; }
.status-warning { background: #fef3c7; color: #92400e; }
.status-danger { background: #fee2e2; color: #991b1b; }

.real-time-updates {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e2e8f0;
}

.update-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #64748b;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
  transition: all 0.2s;
}

.pulse-dot.active {
  background: #10b981;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.trend-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.trend-indicator .icon-trending-up { color: #10b981; }
.trend-indicator .icon-trending-down { color: #ef4444; }
.trend-indicator .icon-minus { color: #64748b; }

.slider-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.update-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.updater-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
}

.update-details {
  display: flex;
  flex-direction: column;
}

.updater-name {
  font-size: 0.75rem;
  font-weight: 500;
  color: #374151;
}

.update-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.slider-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.375rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn.revert:hover {
  background: #fef3c7;
  border-color: #f59e0b;
  color: #92400e;
}

.action-btn.lock:hover {
  background: #fee2e2;
  border-color: #ef4444;
  color: #991b1b;
}

.locked-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

.change-history {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f1f5f9;
}

.change-history h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 0.375rem;
  font-size: 0.75rem;
}

.change-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.change-value {
  font-weight: 500;
  color: #374151;
}

.change-user {
  color: #64748b;
}

.change-time {
  color: #94a3b8;
}

.toggle-history-btn {
  padding: 0.25rem 0.5rem;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  color: #64748b;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.2s;
}

.toggle-history-btn:hover {
  background: #f1f5f9;
  color: #374151;
}

.bulk-actions {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem 1.5rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  z-index: 50;
}

.bulk-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #f59e0b;
  font-size: 0.875rem;
  font-weight: 500;
}

.bulk-buttons {
  display: flex;
  gap: 0.75rem;
}

.bulk-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.bulk-btn.revert {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.bulk-btn.revert:hover {
  background: #e2e8f0;
}

.bulk-btn.save {
  background: #3b82f6;
  color: white;
}

.bulk-btn.save:hover {
  background: #2563eb;
}

.confirmation-modal-overlay {
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

.confirmation-modal {
  background: white;
  border-radius: 0.75rem;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.5rem 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.modal-content {
  padding: 1.5rem;
}

.modal-content p {
  margin: 0 0 1rem 0;
  color: #64748b;
}

.changes-list {
  list-style: none;
  padding: 0;
  margin: 0;
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
}

.changes-list li {
  padding: 0.5rem 0;
  color: #374151;
  font-size: 0.875rem;
}

.changes-list li:not(:last-child) {
  border-bottom: 1px solid #e2e8f0;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  padding: 1rem 1.5rem 1.5rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.cancel-btn, .confirm-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.cancel-btn {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.cancel-btn:hover {
  background: #f1f5f9;
}

.confirm-btn {
  background: #3b82f6;
  color: white;
}

.confirm-btn:hover {
  background: #2563eb;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .sliders-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  }
}

@media (max-width: 768px) {
  .sliders-container {
    padding: 1rem;
  }
  
  .sliders-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
    text-align: center;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .sliders-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .slider-header {
    flex-direction: column;
    gap: 1rem;
    align-items: start;
  }
  
  .slider-value-display {
    align-items: flex-start;
  }
  
  .slider-controls {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .manual-input {
    width: 100%;
  }
  
  .bulk-actions {
    position: static;
    transform: none;
    margin-top: 2rem;
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .bulk-buttons {
    justify-content: center;
  }
  
  .real-time-updates {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}
</style>