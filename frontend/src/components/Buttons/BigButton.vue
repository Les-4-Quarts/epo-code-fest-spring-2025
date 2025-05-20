<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import BasicButton from './BasicButton.vue'

// Props
const props = defineProps({
  text: String,
  icon: {
    type: String,
    required: false,
  },
  isActive: {
    type: Boolean,
    default: false,
  },
  to: {
    type: Object as () => RouteLocationRaw,
    required: false,
  },
})
</script>

<template>
  <BasicButton
    class="big-button"
    :text="text"
    :color="'var(--neutral-medium)'"
    :icon="icon"
    :iconSize="43"
    :activeColor="'var(--neutral-hightest)'"
    :activeBgColor="'var(--neutral-low)'"
    :isActive="isActive"
    :to="to"
    @click="$emit('click')"
  />
</template>

<style lang="scss" scoped>
.big-button {
  flex-direction: column;
  width: 113px;
  height: 107px;
  transition:
    background-color 0.3s ease-in-out,
    color 0.3s ease-in-out;

  ::v-deep(.icon){
    margin-left: 0 !important;
    margin-right: 0 !important;

  }

  ::v-deep(.text) {
    font-size: 15px;
    font-weight: 800;
  }

  &:hover:not(.is-active) {
    background-color: var(--neutral-medium) !important;
    color: var(--neutral-highter) !important;

    ::v-deep(.icon) {
      color: var(--neutral-highter) !important;
    }
  }
}
</style>
