<script setup lang="ts">
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiClose } from '@mdi/js'
import { onMounted, ref, watch } from 'vue'

const props = defineProps({
  label: String,
  placeholder: {
    type: String,
    required: false,
    default: '',
  },
  type: {
    type: String,
    required: false,
    default: 'text',
  },
  width: {
    type: String,
    required: false,
    default: '250px',
  },
  icon: {
    type: String,
    required: false,
    default: '',
  },
  iconSize: {
    type: Number,
    required: false,
    default: 24,
  },
  deleteOption: {
    type: Boolean,
    required: false,
    default: false,
  },
})

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

const model = defineModel()
const inputFocused = ref(false)

const inputRef = ref<HTMLInputElement | null>(null)

const handleBlur = () => {
  // Delay to allow @mousedown on the cross to execute first
  setTimeout(() => {
    inputFocused.value = false
  }, 0)
}

const clearInput = () => {
  model.value = ''
  inputRef.value?.focus() // Refocus the input
}
</script>

<template>
  <div>
    <label>{{ label }}</label>
    <div class="input">
      <SvgIcon v-if="iconPath" :path="iconPath" type="mdi" class="input-icon" :size="iconSize" />
      <input
        ref="inputRef"
        v-model="model"
        :placeholder="placeholder"
        :type="type"
        @focus="inputFocused = true"
        @blur="handleBlur"
        :style="{
          width: `calc(${props.width} - ${props.iconSize * (iconPath ? 1 : 0)}px - ${props.iconSize * (deleteOption ? 1 : 0)}px)`,
        }"
      />
      <SvgIcon
        v-if="deleteOption && model"
        :path="mdiClose"
        type="mdi"
        class="input-icon close-icon"
        :size="iconSize"
        @mousedown.prevent="clearInput"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
div {
  display: flex;
  flex-direction: column;
  width: 100%;

  label {
    font-weight: bold;
    margin-bottom: 2px;
  }

  .input {
    display: flex;
    align-items: center;
    flex-direction: row;
    padding: 5px;
    border-radius: 7px;

    &:focus-within {
      background-color: var(--neutral-low-opacity);
    }

    input {
      background-color: transparent;
      border: none;

      &:focus {
        outline: none;
        border: none;
      }
    }

    .input-icon {
      margin-right: 5px;
      color: var(--neutral);
    }
    .close-icon {
      cursor: pointer;
      color: var(--neutral);
      margin-left: auto;
    }
  }
}
</style>
