<script setup lang="ts">
//Locales
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<template>
  <div class="home">
    <h1>{{ $t('home.welcome') }}</h1>
  </div>
</template>

<style lang="scss" scoped></style>
