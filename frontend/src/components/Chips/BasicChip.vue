<script setup lang="ts">
defineProps({
  title: String,
  color: String,
  bgColor: String,
  compact: Boolean,
})
</script>

<template>
  <div :class="['chip', { compact }]" :style="{ backgroundColor: bgColor, color: color }">
    <span>{{ title }}</span>
  </div>
</template>

<style scoped lang="scss">
.chip {
  display: inline-block;
  width: auto;
  padding: 5px 10px;
  border-radius: 9999px;
  font-size: 14px;
  color: #fff; /* Default text color */
  background-color: var(--primary-color); /* Default color */
  flex-shrink: 0;
  flex-grow: 0;
  align-self: auto;

  &.compact {
    padding: 0px 6px;
    line-height: 16px;
    font-size: 13px;
  }
}
</style>
