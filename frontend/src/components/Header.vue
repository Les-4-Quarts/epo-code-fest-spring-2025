<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="ts">
import { useAuthStore } from '@/stores/authStore'
import { computed, ref } from 'vue'

// Components
import LinkActiveButton from './Buttons/LinkActiveButton.vue'
import BasicButton from './Buttons/BasicButton.vue'

import { useRouter } from 'vue-router'
const router = useRouter()

import { useRoute } from 'vue-router'
const route = useRoute()

const activeTab = computed(() => {
  return route.path
})
</script>

<template>
  <header>
    <router-link to="/" class="title">
      <img :src="Logo" alt="Logo" width="100px" />
    </router-link>
    <nav>
      <LinkActiveButton text="Home" :isActive="activeTab === '/'" to="/" />
      <LinkActiveButton text="About" :isActive="activeTab === '/about'" to="/about" />
    </nav>
  </header>
</template>

<style lang="scss" scoped>
header {
  display: flex;
  padding: 20px;
  background-color: #f4f3f3;
  z-index: 1002;
  align-items: center;
  height: 20px;

  nav {
    display: flex;

    margin-right: 20px;

    button {
      margin-right: 10px;
    }
  }
}

.title {
  font-size: 24px;
  font-weight: bold;
  text-decoration: none;
  color: var(--primary-text-color);
  margin-right: 30px;
}
</style>
