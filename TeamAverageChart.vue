<template>
  <div class="chart-container">
    <canvas ref="barChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: "TeamAverageChart",
  props: {
    averages: {
      type: Object,
      default: () => ({
        projectManagement: 5.1,
        leadership: 4.6,
        organizationalChange: 5.8
      })
    }
  },
  mounted() {
    const ctx = this.$refs.barChart.getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Project Management', 'Leadership', 'Change Mgmt'],
        datasets: [{
          label: 'Team Average Score',
          data: [
            this.averages.projectManagement,
            this.averages.leadership,
            this.averages.organizationalChange
          ],
          backgroundColor: ['#1a73e8', '#e8711a', '#28a745'],
          borderRadius: 6,
          barThickness: 30
        }]
      },
      options: {
        indexAxis: 'y',
        scales: {
          x: {
            min: 1,
            max: 7,
            title: {
              display: true,
              text: 'Likert Scale (1–7)'
            }
          }
        },
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => `Score: ${context.raw.toFixed(1)}`
            }
          }
        }
      }
    });
  }
};
</script>

<style scoped>
.chart-container {
  max-width: 700px;
  margin: 40px auto;
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
}
</style>
