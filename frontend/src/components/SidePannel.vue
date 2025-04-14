<script setup lang="ts">
defineProps({
  isOpen: Boolean,
})
</script>

<template>
  <div class="side-panel" :class="{ open: isOpen }">
    <div class="header">
      <slot name="header"></slot>
    </div>
    <div class="content">
      <slot></slot>
    </div>
    <div class="footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* Container styles */
.side-panel {
  position: fixed;
  padding-left: 10px;
  padding-top: 50px;
  left: -300px; /* Hidden by default */
  top: 60px;
  width: 290px;
  height: calc(100vh - (60px + 50px)); /* Header + top padding */
  background-color: #f4f3f3;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
  transform: translateX(0);
  z-index: 1000;

  .header {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    padding: 10px;
    margin-right: 10px;
    border-bottom: 2px solid #000;
  }

  .content {
    overflow-y: auto;
    height: calc(100% - 50px); /* Adjust for header height */
  }

  .footer {
    display: flex;
    justify-content: space-around;
    gap: 10px;
    padding: 10px;
    margin-right: 10px;
    border-top: 2px solid #000;
  }
}

.side-panel.open {
  transform: translateX(300px); /* Slide in */
}
</style>
