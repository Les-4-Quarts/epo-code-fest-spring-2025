<script setup lang="ts">
// Components
import BasicBox from './BasicBox.vue'
</script>

<template>
  <BasicBox
    title="Error"
    bgColor="var(--danger-color)"
    color="var(--danger-text-color)"
    icon="mdiCloseCircleOutline"
  >
    <slot></slot>
  </BasicBox>
</template>
