<template>
  <div class="diamond-container">
    <h3>Leadership Diamond</h3>
    <svg :width="size" :height="size" viewBod="0 0 200 200" class="diamond-chart">
        <!-- Axes -->
        <line x1="100" y1="0" x2="100" y2="200" class="axis" />
        <line x1="0" y1="100" x2="200" y2="100" class="axis" />

        <!-- Diamond Shape-->
        <polygon
          :points="diamondPoints"
          class="diamond"
        />

        <!-- Labels -->
//im putting sample values here going to go back and look at srs doc to see what should go here.
        <text x="100" y="15" class="label">Vision</text>
        <text x="100" y="15" class="label">Vision</text>
        <text x="100" y="15" class="label">Vision</text>
        <text x="100" y="15" class="label">Vision</text>
    </svg>
   </div>
</template>


<script>
export default {
    name: "LeadershipDiamond",
    props: {
        scores: {
          type: Object,
          required:true,
          default: () => ({
           //again these are the sample values still.
            vision: 50,
            execution: 50,
            empathy: 50,
            influence:50
          })
        }
      },
      computed: {
        diamondPoints() {
          const scale = 1;
          const center = 100;
          return [
            '${center},${center - this.scores.vision}', //again using vision, etc. as sample values.
            '${center + this.scores.influence},${center}',
            '${center},${center + this.scores.execution}'
            '${center - this.scores.empathy},${center}'
        ].join(" ");
      },
      size() {
        return 200;
      }
   }
};
</script>


<style scoped>
.diamond-container {
    text-align: center;
    margin: 2rem auto;
}

.diamond-chart {
    border: 1px solid #dddddd;
}

.axis {
    stroke: #cccccc;
    stroke-width: 1;
}

.diamond {
    fill: rgba(0, 123, 255, 0.4);
    stroke: #007bff
    stroke-width: 2;
}

.label {
    font-size: 12px;
    fill: #333333;
    text-anchor: middle;
    dominant-baseline: middle;
}
</style>