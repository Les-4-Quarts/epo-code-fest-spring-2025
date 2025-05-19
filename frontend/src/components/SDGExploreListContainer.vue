<script setup lang="ts">
import BasicCard from '@/components/Cards/BasicCard.vue'
import { ref, type PropType } from 'vue'
import InputField from './Fields/InputField.vue'
import type { Patent } from '@/types/Patent'
import type { SearchResult } from '@/types/SearchResult'
import SpinnerLoader from './Loaders/SpinnerLoader.vue'

const props = defineProps({
  selectedSDGs: {
    type: Array as PropType<string[]>,
    default: () => [],
  },
})

const search = defineModel('search', {
  type: String,
  default: '',
})

const searchEspacenet = defineModel('searchEspacenet', {
  type: Boolean,
  default: false,
})

const base_api_url = import.meta.env.VITE_BASE_API_URL
const isLoading = ref(false)

//#region :    --- Get patents

const patents = ref<Patent[]>([])
const page = ref(1)
const pageSize = ref(10)
const totalPages = ref(0)

async function getPatents() {
  const first = (page.value - 1) * pageSize.value + 1
  const last = page.value * pageSize.value
  isLoading.value = true
  fetch(`${base_api_url}/patents`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Range: `${first}-${last}`,
    },
  })
    .then((response) => response.json())
    .then((data: SearchResult) => {
      patents.value = data.patents
      totalPages.value = Math.ceil(data.total_count / pageSize.value)
    })
    .catch((error) => {
      console.error('Error fetching patents:', error)
    })
    .finally(() => {
      isLoading.value = false
    })
}
getPatents()
//#endregion : --- Get patents
</script>

<template>
  <BasicCard class="list-container">
    <SpinnerLoader v-if="isLoading" />

    <template v-else style="width: 100%">
      <div class="filter-header">
        <div class="search">
          <InputField
            class="search-input"
            placeholder="Search for patents"
            type="text"
            v-model="search"
            icon="mdiMagnify"
            width="200px"
            :iconSize="18"
            :delete-option="true"
          />
        </div>
        <div class="search-espacenet">
          <input
            type="checkbox"
            class="search-input"
            id="searchEspacenet"
            v-model="searchEspacenet"
          />
          <label for="search-espacenet">Search with Espacenet</label>
        </div>
      </div>

      <div class="patent-list">
        <div v-for="patent in patents" :key="patent.number" class="patent-item">
          <h3>{{ patent.en_title }}</h3>
          <p>
            <!--  Truncate the abstract to 300 characters -->
            (
            {{ patent.en_abstract.split(' ').slice(0, 300).join(' ') }}
            {{ patent.en_abstract.length > 300 ? '...' : '' }}
            )
          </p>
          <p>Publication Number: {{ patent.number }}</p>
          <p>Publication Date: {{ patent.publication_date }}</p>
        </div>
      </div>

      <div class="pagination"></div>
    </template>
  </BasicCard>
</template>

<style lang="scss" scoped>
.list-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 50px;
  height: calc(82vh - (142px * 2));
  width: 75%;

  .filter-header {
    display: flex;
    justify-content: space-between;
    width: 450px;
    margin-bottom: 20px;

    .search-espacenet {
      display: flex;
      align-items: center;

      .search-input {
        margin-right: 5px;
      }
    }
  }
}
</style>
