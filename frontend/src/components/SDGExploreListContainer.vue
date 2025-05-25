<script setup lang="ts">
import BasicCard from '@/components/Cards/BasicCard.vue'
import { computed, ref, watch, watchEffect, type PropType } from 'vue'
import InputField from './Fields/InputField.vue'
import type { Patent } from '@/types/Patent'
import type { SearchResult } from '@/types/SearchResult'
import SpinnerLoader from './Loaders/SpinnerLoader.vue'
import ItemList from './Lists/ItemList.vue'
import BasicButton from './Buttons/BasicButton.vue'
import { useRouter } from 'vue-router'

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
const isLoadingAnalysis = ref<string | null>(null)
const router = useRouter()

const patentsCache = ref<Record<number, Patent[]>>({}) // Dictionnaire pour stocker les pages préchargées
const page = ref(1)
const pageSize = ref(3)
const totalPages = ref(0)

const isPreloading = ref(false) // Global lock to prevent multiple preloads

async function fetchPage(pageNumber: number) {
  if (pageNumber === page.value) {
    isLoading.value = true // Show loading spinner
  }
  const first = (pageNumber - 1) * pageSize.value
  const last = pageNumber * pageSize.value
  if (!search.value.trim()) {
    console.log('Search query is empty, fetching without search')
    try {
      const response = await fetch(`${base_api_url}/patents`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Range: `${first}-${last}`,
        },
      })
      const data: SearchResult = await response.json()
      patentsCache.value[pageNumber] = data.patents

      totalPages.value = Math.ceil(data.total_count / pageSize.value)
    } catch (error) {
      console.error(`Error fetching page ${pageNumber}:`, error)
    } finally {
      isLoading.value = false // Hide loading spinner
    }
  } else {
    try {
      const response = await fetch(`${base_api_url}/patents/search?query=${search.value}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Range: `${first}-${last}`,
        },
      })
      const data: SearchResult = await response.json()
      patentsCache.value[pageNumber] = data.patents

      totalPages.value = Math.ceil(data.total_count / pageSize.value)
    } catch (error) {
      console.error(`Error fetching page ${pageNumber} with search "${search.value}":`, error)
    } finally {
      isLoading.value = false // Hide loading spinner
    }
  }
}

async function preloadPages() {
  if (isPreloading.value) return // Prevent multiple fetches

  isPreloading.value = true // Activate the lock
  const start = Math.max(1, page.value - 5)
  const end = Math.min(totalPages.value, page.value + 5)

  const pagesToLoad = []

  // Load the first 5 pages if they are not already loaded
  for (let i = 1; i <= Math.min(5, totalPages.value); i++) {
    if (!patentsCache.value[i]) {
      pagesToLoad.push(i)
    }
  }

  // Load the last 5 pages if they are not already loaded
  for (let i = Math.max(1, totalPages.value - 4); i <= totalPages.value; i++) {
    if (!patentsCache.value[i]) {
      pagesToLoad.push(i)
    }
  }

  // Load the pages around the current page if they are not already loaded
  for (let i = start; i <= end; i++) {
    if (!patentsCache.value[i]) {
      pagesToLoad.push(i)
    }
  }

  try {
    await Promise.all(pagesToLoad.map((pageNumber) => fetchPage(pageNumber)))
    cleanCache(start, end) // Clean the cache after preloading
  } catch (error) {
    console.error('Error preloading pages:', error)
  } finally {
    isPreloading.value = false // Release the lock
  }
}

function cleanCache(start: number, end: number) {
  const pagesToKeep = new Set<number>()

  // Keep the pages in the range of start and end
  for (let i = start; i <= end; i++) {
    pagesToKeep.add(i)
  }
  // Keep the first 5 pages
  for (let i = 1; i <= Math.min(5, totalPages.value); i++) {
    pagesToKeep.add(i)
  }
  // Keep the last 5 pages
  for (let i = Math.max(1, totalPages.value - 4); i <= totalPages.value; i++) {
    pagesToKeep.add(i)
  }

  // Remove pages outside the range of start and end
  for (const pageNumber in patentsCache.value) {
    if (!pagesToKeep.has(Number(pageNumber))) {
      delete patentsCache.value[pageNumber]
    }
  }
}

async function initializePages() {
  await fetchPage(page.value)
  await preloadPages()
}
initializePages()

watch(
  () => page.value,
  async (newPage) => {
    if (!patentsCache.value[newPage]) {
      await fetchPage(newPage)
    }
    await preloadPages()
  },
)

function analyze_patent(patent_number: string) {
  if (isLoadingAnalysis.value) {
    console.warn('Analysis already in progress, please wait.')
    return
  }
  isLoadingAnalysis.value = patent_number
  fetch(`${base_api_url}/patents/analyze/${patent_number}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error analyzing patent ${patent_number}: ${response.statusText}`)
      }
      return response.json()
    })
    .then((data) => {
      router.push({
        name: 'analyzed',
        params: { id: patent_number },
      })
    })
    .catch((error) => {
      console.error('Error during patent analysis:', error)
    })
    .finally(() => {
      isLoadingAnalysis.value = null
    })
}

const currentPatents = computed(() => patentsCache.value[page.value] || [])
</script>

<template>
  <BasicCard class="list-container">
    <SpinnerLoader v-if="isLoading" />

    <template v-else style="width: 100%">
      <div class="filter-header">
        <div class="search">
          <InputField
            class="search-input"
            placeholder="Search by name or code"
            type="text"
            v-model="search"
            icon="mdiMagnify"
            width="200px"
            :iconSize="18"
            :delete-option="true"
            @iconClick="
              () => {
                fetchPage(1)
                patentsCache = {}
              }
            "
            @deleteClick="
              () => {
                search = ''
                fetchPage(1)
                patentsCache = {}
              }
            "
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
        <ItemList
          v-for="patent in currentPatents"
          :key="patent.number"
          :title="patent.en_title"
          :sdgs="patent.sdgs"
          :button="
            patent.is_analyzed
              ? {
                  icon: 'mdiChevronRight',
                  action: () => {
                    console.log('View patent:', patent.number)
                  },
                }
              : {
                  text: 'Start analysis',
                  color: 'var(--neutral-lowest)',
                  bgColor: 'var(--primary-highter)',
                  action: () => {
                    analyze_patent(patent.number)
                  },
                  isLoading: isLoadingAnalysis === patent.number,
                }
          "
          :action="
            patent.is_analyzed
              ? () => {
                  router.push({
                    name: 'analyzed',
                    params: { id: patent.number },
                  })
                }
              : undefined
          "
        >
          <template #description class="description">
            <strong>{{ patent.number }}</strong> |
            {{ patent.en_abstract }}
          </template>
        </ItemList>
      </div>

      <div class="pagination">
        <span>{{ page }} of {{ totalPages }}</span>
        <div class="buttons">
          <BasicButton
            :icon="'mdiPageFirst'"
            :iconSize="24"
            :color="page === 1 ? 'var(--neutral-medium)' : 'var(--neutral-hightest)'"
            @click="page = 1"
          />
          <BasicButton
            :icon="'mdiChevronLeft'"
            :iconSize="24"
            :color="page === 1 ? 'var(--neutral-medium)' : 'var(--neutral-hightest)'"
            @click="page = page > 1 ? page - 1 : 1"
          />
          <BasicButton
            :icon="'mdiChevronRight'"
            :iconSize="24"
            :color="page === totalPages ? 'var(--neutral-medium)' : 'var(--neutral-hightest)'"
            @click="page = page < totalPages ? page + 1 : totalPages"
          />
          <BasicButton
            :icon="'mdiPageLast'"
            :iconSize="24"
            :color="page === totalPages ? 'var(--neutral-medium)' : 'var(--neutral-hightest)'"
            @click="page = totalPages"
          />
        </div>
      </div>
    </template>
  </BasicCard>
</template>

<style lang="scss" scoped>
.list-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 20px;
  height: calc(82vh - (142px * 2) + 30px);
  width: 75%;
  overflow-y: scroll;

  .filter-header {
    display: flex;
    justify-content: space-between;
    width: 450px;
    margin-bottom: 10px;

    .search-espacenet {
      display: flex;
      align-items: center;

      .search-input {
        margin-right: 5px;
      }
    }
  }

  .patent-list {
    display: flex;
    flex-direction: column;
    flex: 1;

    .description {
      strong {
        font-weight: 800;
      }
    }
  }

  .pagination {
    display: flex;
    gap: 10px;
    align-items: center;

    .buttons {
      width: 96px;
      display: flex;
      align-items: center;
      gap: 0px;

      ::v-deep(button) {
        padding: 0;
      }
    }
  }
}
</style>
