<template>
  <div class="ai-insights-container">
    <!-- AI Insights per Module -->
    <div class="insights-grid">
      <div 
        v-for="module in modules" 
        :key="module.id"
        class="module-insights"
      >
        <div class="module-header">
          <h3>{{ module.name }}</h3>
          <div class="insights-count">
            <i class="icon-ai"></i>
            <span>{{ module.insights.length }} insights</span>
          </div>
        </div>

        <!-- AI Insights Placeholders -->
        <div class="insights-list">
          <div 
            v-for="insight in module.insights" 
            :key="insight.id"
            :class="'insight-card insight-' + insight.type"
          >
            <div class="insight-header">
              <div class="insight-type-badge">
                <i :class="getInsightIcon(insight.type)"></i>
                {{ insight.type }}
              </div>
              <div class="confidence-score">
                {{ Math.round(insight.confidence * 100) }}%
              </div>
            </div>
            
            <h4 class="insight-title">{{ insight.title }}</h4>
            <p class="insight-content">{{ insight.content }}</p>
            
            <div class="insight-actions">
              <button class="action-btn primary" @click="applyInsight(insight)">
                Apply Suggestion
              </button>
              <button class="action-btn secondary" @click="dismissInsight(insight)">
                Dismiss
              </button>
            </div>
            
            <div class="insight-footer">
              <span class="generated-time">Generated {{ formatTime(insight.createdAt) }}</span>
              <span class="ai-model">GPT-4 Analysis</span>
            </div>
          </div>

          <!-- Empty State Placeholder -->
          <div v-if="module.insights.length === 0" class="empty-insights">
            <div class="empty-icon">
              <i class="icon-brain"></i>
            </div>
            <h4>AI Analysis in Progress</h4>
            <p>Our AI is analyzing {{ module.name.toLowerCase() }} data to generate insights...</p>
            <div class="loading-bar">
              <div class="loading-progress" :style="{ width: module.analysisProgress + '%' }"></div>
            </div>
            <span class="progress-text">{{ module.analysisProgress }}% complete</span>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Insights Summary Panel -->
    <div class="insights-summary">
      <h3>AI Insights Summary</h3>
      <div class="summary-stats">
        <div class="stat-card">
          <div class="stat-value">{{ totalInsights }}</div>
          <div class="stat-label">Total Insights</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ highConfidenceInsights }}</div>
          <div class="stat-label">High Confidence</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ criticalInsights }}</div>
          <div class="stat-label">Critical Issues</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIInsights',
  data() {
    return {
      modules: [
        {
          id: 1,
          name: 'Project Management',
          analysisProgress: 85,
          insights: [
            {
              id: 1,
              type: 'performance',
              title: 'Timeline Optimization Detected',
              content: 'Based on current task dependencies, reordering tasks could reduce project timeline by 12 days.',
              confidence: 0.89,
              createdAt: '2024-01-15T10:30:00Z'
            },
            {
              id: 2,
              type: 'risk',
              title: 'Resource Bottleneck Warning',
              content: 'UI Designer allocation shows potential bottleneck in weeks 3-4. Consider adding backup resources.',
              confidence: 0.76,
              createdAt: '2024-01-15T09:15:00Z'
            }
          ]
        },
        {
          id: 2,
          name: 'Team Performance',
          analysisProgress: 92,
          insights: [
            {
              id: 3,
              type: 'suggestion',
              title: 'Collaboration Enhancement',
              content: 'Teams show 23% higher productivity when using paired programming for complex features.',
              confidence: 0.84,
              createdAt: '2024-01-15T11:45:00Z'
            }
          ]
        },
        {
          id: 3,
          name: 'Budget Tracking',
          analysisProgress: 67,
          insights: []
        },
        {
          id: 4,
          name: 'Career Development',
          analysisProgress: 43,
          insights: [
            {
              id: 4,
              type: 'opportunity',
              title: 'Skill Gap Analysis',
              content: 'Investing in React training for 3 team members could improve delivery speed by 18%.',
              confidence: 0.91,
              createdAt: '2024-01-14T16:20:00Z'
            }
          ]
        }
      ]
    }
  },
  computed: {
    totalInsights() {
      return this.modules.reduce((total, module) => total + module.insights.length, 0);
    },
    highConfidenceInsights() {
      return this.modules.reduce((total, module) => {
        return total + module.insights.filter(insight => insight.confidence >= 0.8).length;
      }, 0);
    },
    criticalInsights() {
      return this.modules.reduce((total, module) => {
        return total + module.insights.filter(insight => insight.type === 'risk').length;
      }, 0);
    }
  },
  methods: {
    getInsightIcon(type) {
      const icons = {
        performance: 'icon-trending-up',
        risk: 'icon-alert-triangle',
        suggestion: 'icon-lightbulb',
        opportunity: 'icon-target'
      };
      return icons[type] || 'icon-info';
    },
    
    applyInsight(insight) {
      console.log('Applying insight:', insight.title);
      // In real app, this would trigger the suggested action
    },
    
    dismissInsight(insight) {
      const module = this.modules.find(m => m.insights.some(i => i.id === insight.id));
      if (module) {
        module.insights = module.insights.filter(i => i.id !== insight.id);
      }
    },
    
    formatTime(dateString) {
      const date = new Date(dateString);
      const now = new Date();
      const diffMinutes = Math.floor((now - date) / (1000 * 60));
      
      if (diffMinutes < 60) return `${diffMinutes}m ago`;
      if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`;
      return `${Math.floor(diffMinutes / 1440)}d ago`;
    }
  }
}
</script>

<style scoped>
.ai-insights-container {
  padding: 1.5rem;
  background: #f8fafc;
  min-height: 100vh;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.module-insights {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.module-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.insights-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6366f1;
  font-weight: 500;
}

.insights-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.insight-card {
  padding: 1.25rem;
  border-radius: 0.75rem;
  border-left: 4px solid;
  background: #f8fafc;
  transition: all 0.2s;
}

.insight-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.insight-performance {
  border-left-color: #10b981;
  background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
}

.insight-risk {
  border-left-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #fef5f5 100%);
}

.insight-suggestion {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%);
}

.insight-opportunity {
  border-left-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
}

.insight-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.insight-type-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.confidence-score {
  font-weight: 600;
  color: #059669;
  font-size: 0.875rem;
}

.insight-title {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.insight-content {
  margin: 0 0 1rem 0;
  color: #475569;
  line-height: 1.5;
  font-size: 0.875rem;
}

.insight-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-btn.primary {
  background: #6366f1;
  color: white;
}

.action-btn.primary:hover {
  background: #4f46e5;
}

.action-btn.secondary {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.action-btn.secondary:hover {
  background: #e2e8f0;
}

.insight-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: #94a3b8;
}

.empty-insights {
  text-align: center;
  padding: 2rem 1rem;
  color: #64748b;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #cbd5e1;
}

.empty-insights h4 {
  margin: 0 0 0.5rem 0;
  color: #374151;
}

.empty-insights p {
  margin: 0 0 1.5rem 0;
  font-size: 0.875rem;
}

.loading-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.loading-progress {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  border-radius: 4px;
  transition: width 0.3s ease;
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: 200px 0; }
}

.progress-text {
  font-size: 0.75rem;
  font-weight: 500;
  color: #6366f1;
}

.insights-summary {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.insights-summary h3 {
  margin: 0 0 1.5rem 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
}
</style>