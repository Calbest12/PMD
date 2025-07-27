/* This is the actual code
& logic for calculating and
displaying the average team
response values below each
slider. Test and make sure
it shows the averages for
team responses correctly
once you get past the login
page error*/

<template>
    <div class="editable-sliders">
        <div v-for="(slider, index) in sliders" :key="index" class="slider-group">
            <Slider
             :label="slider.label"
             :min="slider.min"
             :max="slider.max"
             v-model:value="slider.value"
             @update:value="updateAverage(index, $event)"
           />
           <div class="average-display">
            Average Response: {{ slider.average.toFixed(2) }}
           </div>
        </div>
    </div>
</template>


<script>
import Slider from "./Slider.vue";

export default {
    name: "EditableSliders",
    components: {
      Slider
    },
    data() {
     return {
       sliders: [
        { label: "projectManagement", min: 0, max: 10, value: 5, values: [], average: 5 },
        { label: "leadership", min: 0, max: 10, value: 5, values: [], average: 5 },
        { label: "organizationalChange", min: 0, max: 10, value: 5, values: [], average: 5 },
      ]
    };
  },
  methods: {
    updateAverage(index, newVal) {
      const slider = this.sliders[index];
      slider.values.push(newVal);
      const sum = slider.values.reduce((a, b) => a + b, 0);
      slider.average = sum / slider.values.length;
    }
  }
};
</script>


<style scoped>
.slider-group {
    margin-bottom: 2 rem;
}
.average-display {
    font-weight: bold;
    color: #555555;
    margin-top: 0.5rem;
}
</style>