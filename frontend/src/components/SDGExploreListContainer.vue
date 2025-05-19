<script setup lang="ts">
import BasicCard from '@/components/Cards/BasicCard.vue'
</script>

<template>
  <BasicCard class="list-container">Salut !</BasicCard>
</template>

<style lang="scss" scoped>
.list-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 50px;
  height: calc(82vh - (142px * 2));
  width: 75%;
}
</style>
