<script setup lang="ts">
import ListContainer from '@/components/SDGExploreListContainer.vue'
import MapODD from '@/components/Map/MapODD.vue'
import { ref } from 'vue'

const selectedGoals = ref<number[]>([])
</script>

<template>
  <div class="explore-container">
    <div class="explore-content">
      <div class="map-section">
        <div class="map-wrapper">
          <MapODD ref="mapODD" />
        </div>
      </div>
    </div>
    <ListContainer :selectedSDGs="selectedGoals.map((n: number) => `SDG${n}`)" />
  </div>
</template>

<style lang="scss" scoped>
.explore-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.explore-content {
  width: 1400px;
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
}

.map-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.map-wrapper {
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.country-details h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.5rem;
}
</style>
