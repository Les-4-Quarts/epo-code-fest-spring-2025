<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'

const language = useI18n()
const selectedODD = ref(null)
const selectedColor = ref('#cccccc')
const selectedGoals = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
const emit = defineEmits(['update-selection'])

const odds = ref([
  { id: 1, color: '#E5243B' },
  { id: 2, color: '#DDA63A' },
  { id: 3, color: '#4C9F38' },
  { id: 4, color: '#C5192D' },
  { id: 5, color: '#FF3A21' },
  { id: 6, color: '#26BDE2' },
  { id: 7, color: '#FCC30B' },
  { id: 8, color: '#A21942' },
  { id: 9, color: '#FD6925' },
  { id: 10, color: '#DD1367' },
  { id: 11, color: '#FD9D24' },
  { id: 12, color: '#BF8B2E' },
  { id: 13, color: '#3F7E44' },
  { id: 14, color: '#0A97D9' },
  { id: 15, color: '#56C02B' },
  { id: 16, color: '#00689D' },
  { id: 17, color: '#19486A' },
])

const getSdgImage = (n) => {
  if (language.locale.value === 'fr') {
    return new URL(`../../assets/images/SDG/French/sdg_${n}.png`, import.meta.url).href
  } else if (language.locale.value === 'en') {
    return new URL(`../../assets/images/SDG/English/sdg_${n}.png`, import.meta.url).href
  } else {
    return new URL(`../../assets/images/SDG/Deutsch/sdg_${n}.svg`, import.meta.url).href
  }
}

const toggleSelection = (n) => {
  if (n === 18) {
    // "Select All" toggles all
    if (selectedGoals.value.length < 17) {
      selectedGoals.value = Array.from({ length: 18 }, (_, i) => i + 1)
      emit('update-selection', selectedGoals.value)
    } else {
      selectedGoals.value = []
      emit('update-selection', selectedGoals.value)
    }
  } else {
    if (selectedGoals.value.includes(n)) {
      if (selectedGoals.value.includes(18)) {
        selectedGoals.value = selectedGoals.value.filter((g) => g !== 18)
      }
      selectedGoals.value = selectedGoals.value.filter((g) => g !== n)
      emit('update-selection', selectedGoals.value)
    } else {
      if (selectedGoals.value.length === 16) {
        selectedGoals.value.push(18)
      }

      selectedGoals.value.push(n)
      emit('update-selection', selectedGoals.value)
    }
  }
}
</script>

<template>
  <div class="map-and-sdg-container">
    <div class="sdg-grid">
      <div
        v-for="n in 18"
        :key="n"
        class="sdg-item"
        :class="{ selected: selectedGoals.includes(n) }"
        @click="toggleSelection(n)"
      >
        <img :src="getSdgImage(n)" :alt="`ODD ${n}`" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.map-and-sdg-container {
  display: grid;
  grid-row: auto;
}

.sdg-grid {
  display: grid;
  grid-template-columns: repeat(9, minmax(80px, 1fr));
  gap: 10px;
  margin: auto;
  height: 100%;
}

.sdg-item.selected {
  cursor: pointer;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
  opacity: 100%;
}

.sdg-item {
  cursor: pointer;
  transition: transform 0.2s;
  opacity: 0.5;
  height: auto;
  width: auto;
}

.sdg-item img {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
