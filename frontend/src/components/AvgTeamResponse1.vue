/*Slider.vue double check with team about the
login issues and if these are the correct files
they should go into, & integrate this code into
that file. */

/* This represents an individual slider and
shows its value on change */

<template>
    <div class="slider-component">
    <label :for="label">{{ label }}</label>
    <input
        type="range"
        :id="label"
        v-model.number="sliderValue"
        :min="min"
        :max="max"
        @input="emitValue"
    />
    <span>{{ sliderValue }}</span>
   </div>
</template>


<script>
export default {
    name: "Slider",
    props: {
     label: String,
     min: {
     type: Number,
     default: 0
    },
    max: {
     type: Number,
     default: 10
    },
    value: {
      type: Number,
      default: 5
     }
    },
    data () {
      return {
        sliderValue: this.value
       };
      },
      methods: {
        emitValue(){
          this.$emit("update:value", this.sliderValue);
         }
       }
    };
</script>

<style scoped>
.slider-component {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
  }
</style>