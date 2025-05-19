<script setup lang="ts">
import { RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
import { ref } from 'vue'
import SidePanel from './components/SidePanel.vue'

import { useThemeStore } from './stores/themeStore'
const themeStore = useThemeStore()

const componentKey = ref(Date.now())
</script>

<template>
  <div :class="['container', { dark: themeStore.isDarkTheme }]">
    <div class="page">
      <SidePanel is-open />
      <main>
        <RouterView :key="componentKey" />
      </main>
    </div>
    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--neutral-lowest);
  color: var(--neutral-hightest);

  transition:
    background-color 0.3s ease-in-out,
    color 0.3s ease-in-out;

  // Background image
  background-image: url('@/assets/images/background.svg');
  background-repeat: no-repeat;
  background-size: 150%;
  background-position: center;
  background-attachment: fixed;
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
}

.page {
  display: flex;
  flex-direction: row;
  flex: 1;

  main {
    display: flex;
    flex: 1;
    margin-left: 180px;
  }
}
</style>
