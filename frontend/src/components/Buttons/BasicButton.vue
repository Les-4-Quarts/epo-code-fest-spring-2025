<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import SpinnerLoader from '../Loaders/SpinnerLoader.vue'
import { useRouter } from 'vue-router'
import type { RouteLocationRaw } from 'vue-router'
import { onMounted, ref, watch } from 'vue'

// Props
const props = defineProps({
  text: String,
  color: {
    type: String,
    default: 'black',
  },
  bgColor: {
    type: String,
    default: 'transparent',
  },
  icon: {
    type: String,
    required: false,
  },
  iconSize: {
    type: Number,
    default: 24,
  },
  activeColor: {
    type: String,
    default: 'var(--secondary-text-color)',
  },
  activeBgColor: {
    type: String,
    default: 'var(--primary-color)',
  },
  isActive: {
    type: Boolean,
    default: false,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  to: {
    type: Object as () => RouteLocationRaw,
    required: false,
  },
})

// Router
const router = useRouter()

// Emits
const emit = defineEmits(['click'])

// Methods
const onClick = () => {
  if (props.to) {
    router.push(props.to)
  } else {
    emit('click')
  }
}

//#region :    --- Icon

const iconPath = ref<string | undefined>(undefined)

const loadIcon = async (iconName: undefined | string) => {
  if (!iconName) {
    iconPath.value = undefined
    return
  }

  try {
    const module = (await import('@mdi/js')) as unknown as Record<string, string>
    iconPath.value = module[iconName]
  } catch (error) {
    console.error(`Failed to load icon: ${iconName}`, error)
    iconPath.value = 'undefined'
  }
}

// Load the icon when the component is mounted or when the icon prop changes
onMounted(() => loadIcon(props.icon))
watch(
  () => props.icon,
  (newIcon) => loadIcon(newIcon),
)

//#endregion : --- Icon
</script>

<template>
  <button
    @click="onClick"
    :disabled="isLoading || disabled"
    :class="['button', { disabled: disabled }, { 'is-active': isActive }]"
    :style="{
      color: isActive ? activeColor : color,
      backgroundColor: isActive ? activeBgColor : bgColor,
    }"
  >
    <SpinnerLoader v-if="isLoading" class="loader" :color="color" :size="1" />
    <template v-else>
      <SvgIcon
        v-if="icon"
        type="mdi"
        :path="iconPath"
        :size="iconSize"
        :style="{ color: isActive ? activeColor : color }"
        :class="['icon', { 'icon-with-text': text }]"
      />
      <span class="text">{{ text }}</span>
    </template>
  </button>
</template>

<style lang="scss" scoped>
button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;



  .icon {
    transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;


    &.icon-with-text {
      margin-left: -5px;
      margin-right: 5px;
      // Ca ne sert à rien
    }
  }

  &.disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }
}
</style>
