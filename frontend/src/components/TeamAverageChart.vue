<template>
  <div class="chart-container">
    <div class="chart-header">
      <h3>Team Performance Averages</h3>
      <div class="chart-controls">
        <select v-model="selectedTimeframe" @change="loadChartData" class="timeframe-select">
          <option value="all">All Time</option>
          <option value="month">Last Month</option>
          <option value="quarter">Last Quarter</option>
          <option value="year">Last Year</option>
        </select>
        <button @click="refreshChart" :disabled="loading" class="refresh-btn">
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <p>Loading chart data...</p>
    </div>

    <div v-else-if="hasData" class="chart-wrapper">
      <canvas ref="barChart"></canvas>
    </div>

    <div v-else class="no-data-state">
      <p>No feedback data available yet.</p>
      <p class="help-text">Submit some feedback to see your team's performance metrics!</p>
    </div>

    <div v-if="hasData" class="chart-stats">
      <div class="stat-item">
        <span class="stat-label">Overall Average:</span>
        <span class="stat-value">{{ overallAverage.toFixed(1) }}/7</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Feedback Entries:</span>
        <span class="stat-value">{{ totalEntries }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Last Updated:</span>
        <span class="stat-value">{{ lastUpdated }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: "TeamAverageChart",
  props: {
    scores: {
      type: Object,
      default: () => ({
        projectManagement: 0,
        leadership: 0,
        organizationalChange: 0
      })
    }
  },
  data() {
    return {
      chart: null,
      loading: false,
      selectedTimeframe: 'all',
      chartData: {
        projectManagement: 0,
        leadership: 0,
        organizationalChange: 0
      },
      totalEntries: 0,
      lastUpdated: 'Never'
    }
  },
  computed: {
    hasData() {
      return this.chartData.projectManagement > 0 ||
             this.chartData.leadership > 0 ||
             this.chartData.organizationalChange > 0;
    },
    overallAverage() {
      const values = Object.values(this.chartData);
      const sum = values.reduce((a, b) => a + b, 0);
      return values.length > 0 ? sum / values.length : 0;
    }
  },
  async mounted() {
    await this.loadChartData();
  },
  watch: {
    scores: {
      handler(newScores) {
        // Update chart when scores prop changes
        if (newScores && typeof newScores === 'object') {
          this.chartData = { ...newScores };
          this.updateChart();
        }
      },
      deep: true
    }
  },
  methods: {
    async loadChartData() {
      this.loading = true;

      try {
        // Get dashboard analytics which includes average scores
        const analytics = await this.$feedbackService.getDashboardAnalytics();

        if (analytics.success && analytics.average_scores) {
          this.chartData = {
            projectManagement: analytics.average_scores.PM || 0,
            leadership: analytics.average_scores.Leadership || 0,
            organizationalChange: analytics.average_scores.ChangeMgmt || 0
          };

          // Get additional stats
          const feedbackData = await this.$feedbackService.getSliderFeedback();
          if (feedbackData.success) {
            this.totalEntries = feedbackData.results.length;
            if (feedbackData.results.length > 0) {
              const latest = feedbackData.results[0]; // Assuming sorted by date
              this.lastUpdated = this.formatDate(latest.submitted_at);
            }
          }
        } else {
          // Use prop data as fallback
          this.chartData = { ...this.scores };
        }

        this.updateChart();
      } catch (error) {
        console.error('Error loading chart data:', error);
        // Use prop data as fallback
        this.chartData = { ...this.scores };
        this.updateChart();
      } finally {
        this.loading = false;
      }
    },

    async refreshChart() {
      await this.loadChartData();
    },

    updateChart() {
      if (this.chart) {
        // Update existing chart
        this.chart.data.datasets[0].data = [
          this.chartData.projectManagement,
          this.chartData.leadership,
          this.chartData.organizationalChange
        ];
        this.chart.update();
      } else {
        // Create new chart
        this.createChart();
      }
    },

    createChart() {
      if (!this.$refs.barChart) return;

      const ctx = this.$refs.barChart.getContext('2d');

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Project Management', 'Leadership', 'Change Management'],
          datasets: [{
            label: 'Team Average Score',
            data: [
              this.chartData.projectManagement,
              this.chartData.leadership,
              this.chartData.organizationalChange
            ],
            backgroundColor: [
              'rgba(26, 115, 232, 0.8)',
              'rgba(232, 113, 26, 0.8)',
              'rgba(40, 167, 69, 0.8)'
            ],
            borderColor: [
              'rgba(26, 115, 232, 1)',
              'rgba(232, 113, 26, 1)',
              'rgba(40, 167, 69, 1)'
            ],
            borderWidth: 2,
            borderRadius: 8,
            barThickness: 50
          }]
        },
        options: {
          indexAxis: 'y',
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              min: 0,
              max: 7,
              title: {
                display: true,
                text: 'Score (1-7 Likert Scale)',
                font: {
                  size: 12,
                  weight: 'bold'
                }
              },
              grid: {
                display: true,
                color: 'rgba(0, 0, 0, 0.1)'
              },
              ticks: {
                stepSize: 1
              }
            },
            y: {
              grid: {
                display: false
              },
              ticks: {
                font: {
                  size: 11
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  return `Average Score: ${context.raw.toFixed(1)}/7`;
                }
              }
            }
          },
          animation: {
            duration: 1000,
            easing: 'easeInOutQuart'
          }
        }
      });
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  },

  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  }
};
</script>

<style scoped>
.chart-container {
  max-width: 700px;
  margin: 40px auto;
  background: #ffffff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.chart-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
  font-weight: 600;
}

.chart-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.timeframe-select {
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
}

.refresh-btn {
  padding: 6px 16px;
  background: #1a73e8;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: #0f5bb5;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.chart-wrapper {
  height: 300px;
  position: relative;
}

.loading-state, .no-data-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.no-data-state .help-text {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #888;
}

.chart-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
  flex-wrap: wrap;
  gap: 15px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.stat-label {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #333;
}

@media (max-width: 600px) {
  .chart-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .chart-controls {
    justify-content: center;
  }

  .chart-stats {
    flex-direction: column;
    align-items: center;
  }

  .stat-item {
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    max-width: 200px;
  }
}
</style>
