<template>
  <div class="subpage-container">
    <!-- Subpage Header with Last Update and Responsible Team Member -->
    <div class="subpage-header">
      <div class="header-left">
        <button @click="goBack" class="back-button">
          <i class="icon-arrow-left"></i>
          Back
        </button>
        <div class="page-title">
          <h1>{{ pageTitle }}</h1>
          <div class="page-meta">
            <div class="last-update">
              <i class="icon-clock"></i>
              <span>Last updated {{ formatDate(lastUpdateDate) }}</span>
            </div>
            <div class="responsible-member">
              <img :src="responsibleMember.avatar" :alt="responsibleMember.name" class="member-avatar">
              <div class="member-info">
                <span class="member-name">{{ responsibleMember.name }}</span>
                <span class="member-role">{{ responsibleMember.role }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="header-actions">
        <button class="action-btn secondary">
          <i class="icon-download"></i>
          Export
        </button>
        <button class="action-btn primary">
          <i class="icon-edit"></i>
          Edit
        </button>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-container">
      <div class="tabs-navigation">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="setActiveTab(tab.id)"
        >
          <i :class="tab.icon"></i>
          {{ tab.label }}
          <span v-if="tab.count" class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- History Tab -->
        <div v-if="activeTab === 'history'" class="history-tab">
          <div class="tab-header">
            <h3>Project History</h3>
            <div class="history-filters">
              <select v-model="historyFilter" class="filter-select">
                <option value="">All Activities</option>
                <option value="updates">Updates</option>
                <option value="tasks">Tasks</option>
                <option value="meetings">Meetings</option>
                <option value="milestones">Milestones</option>
              </select>
            </div>
          </div>

          <!-- Collapsible History Sections -->
          <div class="collapsible-sections">
            <div 
              v-for="historyGroup in filteredHistory" 
              :key="historyGroup.date"
              class="collapsible-section"
            >
              <div 
                class="section-header clickable"
                @click="toggleHistorySection(historyGroup.date)"
              >
                <div class="section-title">
                  <h4>{{ historyGroup.date }}</h4>
                  <span class="entries-count">{{ historyGroup.entries.length }} activities</span>
                </div>
                <i :class="historyGroup.expanded ? 'icon-chevron-up' : 'icon-chevron-down'"></i>
              </div>
              
              <div v-if="historyGroup.expanded" class="section-content">
                <div class="history-timeline">
                  <div 
                    v-for="entry in historyGroup.entries" 
                    :key="entry.id"
                    class="history-entry"
                  >
                    <div class="entry-indicator">
                      <div :class="'entry-dot entry-' + entry.type"></div>
                      <div class="entry-line"></div>
                    </div>
                    <div class="entry-content">
                      <div class="entry-header">
                        <span class="entry-time">{{ entry.time }}</span>
                        <span :class="'entry-type-badge type-' + entry.type">{{ entry.type }}</span>
                      </div>
                      <div class="entry-action">{{ entry.action }}</div>
                      <div class="entry-description">{{ entry.description }}</div>
                      <div class="entry-user">
                        <img :src="entry.user.avatar" :alt="entry.user.name" class="user-avatar-small">
                        <span>{{ entry.user.name }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sliders Tab -->
        <div v-if="activeTab === 'sliders'" class="sliders-tab">
          <div class="tab-header">
            <h3>Performance Metrics</h3>
            <button @click="resetAllSliders" class="reset-button">
              <i class="icon-refresh"></i>
              Reset All
            </button>
          </div>

          <div class="sliders-grid">
            <div 
              v-for="slider in sliders" 
              :key="slider.id"
              class="slider-card"
            >
              <div class="slider-header">
                <div class="slider-info">
                  <h4>{{ slider.label }}</h4>
                  <p class="slider-description">{{ slider.description }}</p>
                </div>
                <div class="slider-value-display">
                  <span class="current-value">{{ slider.currentValue }}</span>
                  <span class="max-value">/ {{ slider.maxValue }}</span>
                </div>
              </div>
              
              <div class="slider-container">
                <input 
                  type="range"
                  :min="slider.minValue"
                  :max="slider.maxValue"
                  v-model="slider.currentValue"
                  @input="updateSlider(slider)"
                  :disabled="!slider.isEditable"
                  class="slider-input"
                  :style="{ '--progress': (slider.currentValue / slider.maxValue) * 100 + '%' }"
                >
                <div class="slider-labels">
                  <span>{{ slider.minValue }}</span>
                  <span>{{ slider.maxValue }}</span>
                </div>
              </div>
              
              <div class="slider-footer">
                <div class="update-info">
                  <i class="icon-user"></i>
                  <span>{{ slider.updatedBy }}</span>
                </div>
                <div class="update-time">
                  <i class="icon-clock"></i>
                  <span>{{ formatDate(slider.updatedAt) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Insights Tab -->
        <div v-if="activeTab === 'insights'" class="insights-tab">
          <div class="tab-header">
            <h3>AI Insights</h3>
            <div class="insights-actions">
              <button @click="refreshInsights" class="refresh-button">
                <i class="icon-refresh"></i>
                Refresh
              </button>
              <select v-model="insightFilter" class="filter-select">
                <option value="">All Types</option>
                <option value="performance">Performance</option>
                <option value="risk">Risk</option>
                <option value="suggestion">Suggestion</option>
                <option value="trend">Trend</option>
              </select>
            </div>
          </div>

          <div class="insights-container">
            <div 
              v-for="insight in filteredInsights" 
              :key="insight.id"
              :class="'insight-card insight-' + insight.type"
            >
              <div class="insight-header">
                <div class="insight-type">
                  <i :class="getInsightIcon(insight.type)"></i>
                  <span>{{ insight.type }}</span>
                </div>
                <div class="insight-meta">
                  <div class="confidence-score">
                    <span class="confidence-label">Confidence</span>
                    <div class="confidence-bar">
                      <div class="confidence-fill" :style="{ width: insight.confidence * 100 + '%' }"></div>
                    </div>
                    <span class="confidence-value">{{ Math.round(insight.confidence * 100) }}%</span>
                  </div>
                </div>
              </div>
              
              <h4 class="insight-title">{{ insight.title }}</h4>
              <p class="insight-content">{{ insight.content }}</p>
              
              <div class="insight-actions">
                <button class="action-btn primary small" @click="applyInsight(insight)">
                  Apply
                </button>
                <button class="action-btn secondary small" @click="saveInsight(insight)">
                  Save
                </button>
                <button class="action-btn danger small" @click="dismissInsight(insight)">
                  Dismiss
                </button>
              </div>
              
              <div class="insight-footer">
                <span class="generated-time">Generated {{ formatDate(insight.createdAt) }}</span>
                <span class="ai-badge">AI Generated</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SubpageTemplate',
  props: {
    pageTitle: {
      type: String,
      default: 'Project Details'
    },
    lastUpdateDate: {
      type: String,
      default: '2024-01-15T10:30:00Z'
    },
    responsibleMember: {
      type: Object,
      default: () => ({
        name: 'Sarah Johnson',
        role: 'Project Manager',
        avatar: '/api/placeholder/40/40'
      })
    }
  },
  data() {
    return {
      activeTab: 'history',
      historyFilter: '',
      insightFilter: '',
      tabs: [
        { id: 'history', label: 'History', icon: 'icon-clock', count: 15 },
        { id: 'sliders', label: 'Metrics', icon: 'icon-sliders', count: 6 },
        { id: 'insights', label: 'AI Insights', icon: 'icon-brain', count: 4 }
      ],
      historyData: [
        {
          date: 'January 15, 2024',
          expanded: true,
          entries: [
            {
              id: 1,
              time: '10:30 AM',
              type: 'update',
              action: 'Progress Updated',
              description: 'Project progress updated to 75% completion',
              user: { name: 'Sarah Johnson', avatar: '/api/placeholder/24/24' }
            },
            {
              id: 2,
              time: '09:15 AM',
              type: 'task',
              action: 'Task Completed',
              description: 'UI mockups completed and approved by stakeholders',
              user: { name: 'Mike Chen', avatar: '/api/placeholder/24/24' }
            },
            {
              id: 3,
              time: '08:45 AM',
              type: 'milestone',
              action: 'Milestone Reached',
              description: 'Design phase completed successfully',
              user: { name: 'Design Team', avatar: '/api/placeholder/24/24' }
            }
          ]
        },
        {
          date: 'January 14, 2024',
          expanded: false,
          entries: [
            {
              id: 4,
              time: '4:45 PM',
              type: 'meeting',
              action: 'Team Meeting',
              description: 'Weekly sprint review and planning session',
              user: { name: 'Alex Rodriguez', avatar: '/api/placeholder/24/24' }
            },
            {
              id: 5,
              time: '2:30 PM',
              type: 'update',
              action: 'Status Update',
              description: 'Technical documentation updated',
              user: { name: 'Tech Writer', avatar: '/api/placeholder/24/24' }
            }
          ]
        },
        {
          date: 'January 13, 2024',
          expanded: false,
          entries: [
            {
              id: 6,
              time: '11:20 AM',
              type: 'task',
              action: 'Code Review',
              description: 'Frontend components reviewed and merged',
              user: { name: 'Senior Developer', avatar: '/api/placeholder/24/24' }
            }
          ]
        }
      ],
      sliders: [
        {
          id: 1,
          label: 'Project Progress',
          description: 'Overall completion percentage',
          currentValue: 75,
          maxValue: 100,
          minValue: 0,
          isEditable: true,
          updatedBy: 'Sarah Johnson',
          updatedAt: '2024-01-15T10:30:00Z'
        },
        {
          id: 2,
          label: 'Team Performance',
          description: 'Team velocity and efficiency metric',
          currentValue: 85,
          maxValue: 100,
          minValue: 0,
          isEditable: true,
          updatedBy: 'Mike Chen',
          updatedAt: '2024-01-14T16:45:00Z'
        },
        {
          id: 3,
          label: 'Budget Utilization',
          description: 'Percentage of allocated budget used',
          currentValue: 60,
          maxValue: 100,
          minValue: 0,
          isEditable: false,
          updatedBy: 'System',
          updatedAt: '2024-01-15T08:00:00Z'
        },
        {
          id: 4,
          label: 'Quality Score',
          description: 'Code quality and testing coverage',
          currentValue: 92,
          maxValue: 100,
          minValue: 0,
          isEditable: true,
          updatedBy: 'QA Team',
          updatedAt: '2024-01-13T14:20:00Z'
        },
        {
          id: 5,
          label: 'Client Satisfaction',
          description: 'Client feedback and satisfaction rating',
          currentValue: 88,
          maxValue: 100,
          minValue: 0,
          isEditable: true,
          updatedBy: 'Client Manager',
          updatedAt: '2024-01-12T11:30:00Z'
        },
        {
          id: 6,
          label: 'Timeline Adherence',
          description: 'How well we are sticking to planned timeline',
          currentValue: 78,
          maxValue: 100,
          minValue: 0,
          isEditable: true,
          updatedBy: 'Project Manager',
          updatedAt: '2024-01-15T09:45:00Z'
        }
      ],
              insights: [
                {
                  id: 1,
                  type: 'performance',
                  title: 'Project Timeline Optimization',
                  content: 'Based on current progress metrics, the project is likely to complete 3 days ahead of schedule with current team velocity.',
                  confidence: 0.89,
                  createdAt: '2024-01-15T12:00:00Z'
                }
              ]
            };
          },
          computed: {
            filteredHistory() {
              if (!this.historyFilter) return this.historyData;
              return this.historyData.map(group => ({
                ...group,
                entries: group.entries.filter(entry => 
                  this.historyFilter === '' || entry.type === this.historyFilter
                )
              })).filter(group => group.entries.length > 0);
            },
            filteredInsights() {
              if (!this.insightFilter) return this.insights;
              return this.insights.filter(insight => insight.type === this.insightFilter);
            }
          },
          methods: {
            goBack() {
              this.$emit('go-back');
            },
            setActiveTab(tabId) {
              this.activeTab = tabId;
            },
            formatDate(dateStr) {
              const date = new Date(dateStr);
              return date.toLocaleString(undefined, {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              });
            },
            toggleHistorySection(date) {
              this.historyData = this.historyData.map(group =>
                group.date === date
                  ? { ...group, expanded: !group.expanded }
                  : group
              );
            },
            resetAllSliders() {
              this.sliders = this.sliders.map(slider => ({
                ...slider,
                currentValue: slider.minValue
              }));
            },
            updateSlider(slider) {
              slider.updatedAt = new Date().toISOString();
              slider.updatedBy = 'You';
            },
            refreshInsights() {
              // Placeholder for refreshing insights
            },
            getInsightIcon(type) {
              switch (type) {
                case 'performance': return 'icon-speedometer';
                case 'risk': return 'icon-alert';
                case 'suggestion': return 'icon-lightbulb';
                case 'trend': return 'icon-trending-up';
                default: return 'icon-info';
              }
            },
            applyInsight(insight) {
              // Placeholder for applying insight
            },
            saveInsight(insight) {
              // Placeholder for saving insight
            },
            dismissInsight(insight) {
              // Placeholder for dismissing insight
            }
          }
        };
      </script>