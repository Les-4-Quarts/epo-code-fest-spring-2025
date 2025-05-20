<script setup lang="ts">
import type { PropType } from 'vue'
import BasicChip from '../Chips/BasicChip.vue'
import BigButton from '../Buttons/BigButton.vue'
import BasicButton from '../Buttons/BasicButton.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'ItemList',
  },
  sdgs: {
    type: Array as PropType<string[]>,
    default: () => [],
  },
  button: {
    type: Object as PropType<{
      text?: string
      icon?: string
      color?: string
      bgColor?: string
      action?: () => void
    }>,
  },
  action: {
    type: Function as PropType<() => void>,
    optional: true,
  },
})
</script>

<template>
  <div :class="['item-list', { cliclkable: action }]" @click="action">
    <div class="first-column">
      <div class="first-line">
        <h3>{{ title }}</h3>
        <div class="chips">
          <BasicChip
            v-for="(sdg, index) in sdgs"
            :title="sdg"
            color="white"
            :bgColor="sdg ? `var(--${sdg.slice(0, 3).toLowerCase()}-${sdg.slice(3)})` : undefined"
            compact
          />
        </div>
      </div>
      <div class="second-line">
        <p class="description">
          <slot name="description" />
        </p>
      </div>
    </div>
    <div class="second-column">
      <BasicButton
        v-if="button"
        :text="button.text"
        :icon="button.icon"
        :iconSize="64"
        :color="button.color"
        :bgColor="button.bgColor"
        @click="button.action"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.item-list {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0 1rem 1rem;
  gap: 0.5rem;

  &.cliclkable {
    cursor: pointer;
    transition: all 0.2s ease-in-out;

    &:hover {
      color: var(--warning-highter);
      background-color: var(--neutral-light);
      box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
      border-radius: 8px;

      .second-column button {
        color: var(--warning-highter);
      }
    }
  }

  .first-column {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    .first-line {
      display: flex;
      justify-content: baseline;
      align-items: center;
      gap: 2rem;

      h3 {
        font-size: 24px;
        font-weight: 600;
        color: var(--text-color);
        max-width: 75%;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        line-clamp: 2;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
      }
    }

    .second-line {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;

      ::v-deep(.description) {
        line-height: 1.2;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        line-clamp: 2;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
  }

  .second-column {
    ::v-deep(button) {
      width: 72px;
    }
  }
}
</style>
