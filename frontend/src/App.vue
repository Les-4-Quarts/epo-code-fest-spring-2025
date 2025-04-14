<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import { ref } from 'vue'

const componentKey = ref(Date.now())
</script>

<template>
  <div class="container">
    <Header class="header" />
    <div class="page">
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
}

.header {
  position: fixed;
  width: 100%;
}

.page {
  margin-top: 79px;
  display: flex;
  flex: 1;

  main {
    display: flex;
    flex: 1;
  }
}
</style>
