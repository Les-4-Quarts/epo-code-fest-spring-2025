<script setup lang="ts">
import { RouterView } from 'vue-router'
import Footer from './components/Footer.vue'
import { ref } from 'vue'
import SidePannel from './components/SidePannel.vue'

import { useThemeStore } from './stores/themeStore'
const themeStore = useThemeStore()

const componentKey = ref(Date.now())
</script>

<template>
  <div :class="['container', { dark: themeStore.isDarkTheme }]">
    <div class="page">
      <SidePannel is-open />
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

  &.dark {
    color: var(--secondary-text-color);
    background-color: var(--dark-color);
  }
}

.page {
  display: flex;
  flex-direction: row;
  flex: 1;

  main {
    display: flex;
    flex: 1;
    margin-left: 300px;
  }
}
</style>
