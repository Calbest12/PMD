<template>
  <div class="quadrants-container">
    <h3>Leadership Quadrants</h3>
    <div class="quadrants-grid>
        <div class="quadrant-label tl">Strategic Leader</div> //sample values for now
        <div class="quadrant-label tr">Driving Leader</div>
        <div class="quadrant-label bl">Supportive Leader</div>
        <div class="quadrant-label br">Operational Leader</div>

        <div
          v-for="(member, index) in members"
          :key="index"
          class="leader-dot"
          :style="positionDot(member)"
          :title="member.name"
       ></div>
     </div>
   </div>
</template>

<script>
    export default {
        name: "LeadershipQuadrant",
        props: {
          members: {
            type: Array,
            default: () => [
                { name: "Hind", execution: 80, influence: 20 };
                { name: "Bob", execution: 60, influence: 70 };
                { name: "Alice", execution: 30, influence: 30 };
                { name: "User", execution: 90, influence: 90 };
            ]
        }
    },
    methods: {
        positionDot(member) {
            const x = (member.influence / 100) * 100;
            const y = (100 - member.execution / 100 * 100); //flips y-axis
            return {
                left: '${x}%',
                top: '${y}%',
            };
        }
    }
};
</script>

<style scoped>
.quadrants-container {
text-align: center;
margin: 2rem auto;
width: 400px;
}

.quadrants-grid {
    position: relative;
    width: 100%
    height: 400px
    border: 2px solid #333;
    background: linear-gradient(to right, transparent 49.5%, #333333 50%, transparent 50.5%),
                linear-gradient(to bottom, transparent 49.5%, #333333 50%, transparent 50.5%);
}

.quadrant-label {
    position: absolute;
    width: 50%;
    height: 50%;
    font-size: 0.9rem;
    color: #555555;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-weight: bold;
    pointer-events: none;
}

.tl { top: 0; left: 0; }
.tr { top: 0; left: 50%; }
.bl { top: 50%; left: 0; }
.br { top: 50%; left: 50%; }

.leader-dot {
    position: absolute;
    width: 12px;
    height: 12px;
    background-color: #007bff;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: 0.3s ease;
    cursor: pointer;
}
</style>