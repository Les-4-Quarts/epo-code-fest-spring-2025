<script setup lang="ts">
//Locales
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
</script>

<template>
  <div class="home">
    <BasicCard class="home-card" :title="$t('home.welcome')"> </BasicCard>
  </div>
</template>

<style lang="scss" scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;

  .home-card {
    width: 412px;
    height: 504px;
  }
}
</style>
