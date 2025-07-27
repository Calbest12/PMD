<template>
  <div class="quadrants-grid">
    <div v-for="(v,name) in scores" :key="name" class="quadrant">
        <h4> {{ name }}</h4>
        <div class="bar-container">
            <div class="bar" :style="{ width: (v / 7 * 100) + '%' }"></div> //max value on likert scale
        </div>

        //score label
        <span>{{ v }} / 7</span>
       </div>
     </div>
</template>

<script setup>
    defineProps({
        scores: {
            type: Object,
            required: true
          }
       })
</script>

<style scoped>
.quadrants-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;

.quadrant {
    border: 1px solid #cccccc;
    padding: 1rem;
    border-radius: 4px;
}

.bar-container {
    background: #eeeeee;
    height: 8px;
    margin: 0.5rem 0;
    position: relative;
}

.bar {
    background: #28a745;
    height: 100%;
}
</style>