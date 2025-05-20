<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiChevronDown, mdiChevronUp } from '@mdi/js'
import { ref, type PropType } from 'vue'

const props = defineProps({
  options: {
    type: Array as PropType<{ label: string; value: string }[]>,
    required: true,
  },
  orientation: {
    type: String as PropType<'top' | 'bottom'>,
    required: false,
    default: 'bottom',
  },
  width: {
    type: String,
    required: false,
    default: '100%',
  },
})

const model = defineModel()
const isOpen = ref(false)
</script>

<template>
  <div class="select-input">
    <div class="select-container" @click="isOpen = !isOpen" :style="{ width }">
      <span>{{ options.find((option) => option.value === model)?.label }}</span>
      <SvgIcon class="icon" :path="isOpen ? mdiChevronUp : mdiChevronDown" type="mdi" />
    </div>
    <div :class="['options', orientation]" v-if="isOpen" :style="{ width }">
      <div
        v-for="option in options"
        :key="option.value"
        class="option"
        :class="{ 'is-active': model === option.value }"
        @click="
          () => {
            model = option.value
            isOpen = false
          }
        "
      >
        {{ option.label }}
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.select-input {
  position: relative;
  width: 100%;
  cursor: pointer;

  .select-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 10px;
    font-size: 12px;
    line-height: 16px;
    background-color: var(--neutral-lowest);
    border-radius: 8px;
    transition:
      background-color 0.3s ease-in-out,
      color 0.3s ease-in-out;

    &:hover {
      background-color: var(--neutral-lower);
    }
  }

  .icon {
    margin-left: auto;
  }

  .options {
    position: absolute;
    width: 100%;
    padding: 5px;
    background-color: var(--neutral-lowest);
    border-radius: 4px;
    z-index: 10;

    &.top {
      bottom: calc(100% + 5px);
    }

    &.bottom {
      top: calc(100% + 5px);
    }

    .option {
      padding: 6px;
      font-size: 12px;
      border-radius: 2px;
      text-align: center;
      cursor: pointer;

      &:hover {
        background-color: var(--neutral-low);
      }

      &.is-active {
        background-color: var(--primary-highter);
        color: var(--neutral-lowest);
      }
    }
  }
}
</style>
