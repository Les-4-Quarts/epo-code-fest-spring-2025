<script setup lang="ts">
// Components
import { ref, onMounted, watch } from 'vue'
import SvgIcon from '@jamescoyle/vue-icon'

const props = defineProps({
  title: String,
  color: {
    type: String,
    required: false,
    default: 'var(--neutral-hightest)',
  },
  bgColor: {
    type: String,
    required: false,
    default: 'cream',
  },
  icon: {
    type: String,
    required: false,
    default: 'mdiHome',
  },
})

const iconPath = ref<string | null>(null)

const loadIcon = async (iconName: string) => {
  try {
    const module = (await import('@mdi/js')) as unknown as Record<string, string>
    iconPath.value = module[iconName]
  } catch (error) {
    console.error(`Failed to load icon: ${iconName}`, error)
    iconPath.value = null
  }
}

// Load the icon when the component is mounted or when the icon prop changes
onMounted(() => loadIcon(props.icon))
watch(
  () => props.icon,
  (newIcon) => loadIcon(newIcon),
)
</script>

<template>
  <div class="basic-box" :style="{ color, backgroundColor: bgColor, borderColor: color }">
    <svg-icon v-if="iconPath" type="mdi" :path="iconPath" />
    <div class="body">
      <h2>{{ title }}</h2>
      <slot></slot>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.basic-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 10px;
  border: 2px solid;
  width: 300px;
  margin: 10px;

  svg {
    width: 30px;
    height: 30px;
    margin-right: 10px;
  }

  .body {
    display: flex;
    flex-direction: column;

    h2 {
      font-size: 20px;
      font-weight: bold;
    }
  }
}
</style>
