<script setup lang="ts">
// Components
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiWeatherSunny, mdiWeatherNight } from '@mdi/js'

// Stores
import { useThemeStore } from '@/stores/themeStore'
const themeStore = useThemeStore()

defineProps({
  isOpen: Boolean,
})
</script>

<template>
  <div class="side-panel" :class="{ open: isOpen }">
    <div class="header">
      <h1>EPA</h1>
    </div>
    <div class="content"></div>
    <div class="footer">
      <SvgIcon
        class="theme-icon"
        :path="themeStore.isDarkTheme ? mdiWeatherSunny : mdiWeatherNight"
        type="mdi"
        @click="themeStore.toggleTheme"
        :color="
          themeStore.isDarkTheme ? 'var(--secondary-text-color)' : 'var(--primary-text-color)'
        "
        :size="24"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* Container styles */
.side-panel {
  --vertical-padding: 50px;
  --horizontal-padding: 10px;
  --height: 100vh;
  --width: 300px;

  position: fixed;
  width: calc(var(--width) - var(--horizontal-padding) * 2);
  height: calc(var(--height) - var(--vertical-padding) * 2);
  padding: var(--vertical-padding) var(--horizontal-padding);
  left: calc(-1 * var(--width)); /* Hidden by default */
  transform: translateX(0);
  transition: transform 0.3s ease-in-out;
  z-index: 1000;

  background-color: #f4f3f3;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);

  .header {
    display: flex;
    padding: 10px;
    border-bottom: 2px solid #000;
  }

  .content {
    overflow-y: auto;
    height: calc(var(--height) - 2 * var(--vertical-padding) - 40px); /* Adjust for header height */
  }

  .footer {
    display: flex;
    padding: 10px;
    border-top: 2px solid #000;

    .theme-icon {
      cursor: pointer;
      margin-left: auto;
    }
  }
}

.dark .side-panel {
  background-color: #292524;
  color: var(--secondary-text-color);

  .header,
  .footer {
    border-color: var(--secondary-text-color);
  }
}

.side-panel.open {
  transform: translateX(var(--width)); /* Slide in */
}
</style>
