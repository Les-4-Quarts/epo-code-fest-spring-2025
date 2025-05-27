<script setup lang="ts">
import { marked } from 'marked'

//Locales
import { useI18n } from 'vue-i18n'
const { t, locale } = useI18n()

// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiClose, mdiArrowLeft } from '@mdi/js'
import SpinnerLoader from '@/components/Loaders/SpinnerLoader.vue'

// Refs
import { computed, ref } from 'vue'
import BasicChip from '@/components/Chips/BasicChip.vue'
import { Doughnut } from 'vue-chartjs'
import { useRoute } from 'vue-router'
import type { FullPatent } from '@/types/FullPatent'
const patent = ref<FullPatent | null>(null)
const isLoading = ref(false)
const sdgSelected = ref('')

const route = useRoute()
const patentNumber = route.params.id as string

// Fetch analysis result based on patent number
function fetchAnalysisResult() {
  isLoading.value = true
  fetch(`${import.meta.env.VITE_BASE_API_URL}/patents/full/${patentNumber}`)
    .then((response) => response.json())
    .then((data: FullPatent) => {
      patent.value = data
      isLoading.value = false
    })
    .catch((error) => {
      console.error('Error fetching analysis result:', error)
      isLoading.value = false
    })
}
fetchAnalysisResult()

const filteredResults = computed(() => {
  if (!patent.value?.sdg_summary) {
    return null
  }
  return patent.value.sdg_summary.filter((result) => result.sdg === sdgSelected.value)
})

const doughnutData = computed(() => {
  if (!patent.value?.sdg_summary) {
    return null
  }

  // Retrive all labels from the analysis result. Keep only unique labels
  const labels = patent.value.sdg_summary
    .map((result) => result.sdg)
    .filter((value, index, self) => self.indexOf(value) === index)

  // Count the number of times each label appears in the analysis result
  const data = labels.map((label) => {
    if (!patent.value?.sdg_summary) {
      return 0
    }
    return patent.value.sdg_summary.filter((result) => result.sdg === label).length
  })

  // Generate a color for each label
  const backgroundColor = labels.map((label) => {
    const color = cssvar(`--${label.slice(0, 3).toLowerCase()}-${label.slice(3)}`)
    return color
  })

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor,
      },
    ],
  }
})

const patent_title = computed(() => {
  if (!patent.value) {
    return ''
  }
  // Return the title in the current locale
  return (
    (patent.value as Record<string, any>)[`${locale.value}_title`] || patent.value.en_title || ''
  )
})

const country_flag = computed(() => {
  if (!patent.value) {
    return ''
  }
  // Return the country flag based on the patent's country code from REST Contries API
  return patent.value.country ? `https://flagcdn.com/${patent.value.country.toLowerCase()}.svg` : ''
})

// Methods
const renderMarkdown = (markdown: string | undefined) => {
  if (!markdown) return ''
  return marked(markdown, { breaks: true })
}

function backResults() {
  sdgSelected.value = ''
}

function closeResults() {
  sdgSelected.value = ''
  patent.value = null
  isLoading.value = false
  // Optionally, navigate back to the previous page or home
  // e.g., router.push({ name: 'Home' }) if using Vue Router
  window.history.back()
}

function cssvar(name: string) {
  return getComputedStyle(document.documentElement).getPropertyValue(name)
}
</script>

<template>
  <div class="analyze">
    <SpinnerLoader v-if="isLoading" :size="16" :border-width="1" />

    <BasicCard v-else-if="!sdgSelected" class="analyze-result-card">
      <div class="content">
        <SvgIcon class="close" type="mdi" :path="mdiClose" @click="closeResults" />
        <div class="title">
          <h2>{{ patent_title }}</h2>
          <div class="flag">
            <img v-if="country_flag" :src="country_flag" alt="Country Flag" />
          </div>
        </div>

        <div class="applicants section">
          <h3>{{ $t('analyze.applicants') }}</h3>
          <ul>
            <li v-for="(applicant, index) in patent?.applicants || []" :key="index">
              {{ applicant.name }}
            </li>
          </ul>
        </div>

        <div class="abstract section">
          <h3>{{ $t('analyze.abstract') }}</h3>
          <p class="abstract">
            {{ patent?.en_abstract || patent?.fr_abstract || patent?.de_abstract }}
          </p>
        </div>

        <div class="results section">
          <div class="results-text">
            <h3>{{ $t('analyze.sdg') }}</h3>
            <div
              v-for="(result, index) in patent?.sdg_summary || []"
              :key="index"
              @click="sdgSelected = result.sdg"
              class="result"
            >
              <BasicChip
                class="chip"
                :title="result.sdg"
                color="white"
                :bgColor="`var(--${result.sdg.slice(0, 3).toLowerCase()}-${result.sdg.slice(3)})`"
              />
              <div v-html="renderMarkdown(result.sdg_reason)"></div>
            </div>
          </div>
          <div class="camembert">
            <Doughnut
              v-if="doughnutData"
              :data="doughnutData"
              :options="{
                plugins: {
                  legend: {
                    display: false,
                  },
                },
              }"
            />
          </div>
        </div>
      </div>
    </BasicCard>

    <BasicCard v-else class="analyze-result-card">
      <div class="content">
        <SvgIcon class="back" type="mdi" :path="mdiArrowLeft" @click="backResults" />
        <SvgIcon class="close" type="mdi" :path="mdiClose" @click="closeResults" />
        <h2>{{ $t('analyze.about') }}</h2>
        <div class="results">
          <div class="results-text">
            <div>
              <BasicChip
                class="chip"
                :title="sdgSelected"
                color="white"
                :bgColor="`var(--${sdgSelected.slice(0, 3).toLowerCase()}-${sdgSelected.slice(3)})`"
              />
            </div>
            <div v-for="(result, index) in filteredResults" :key="index">
              <div v-html="renderMarkdown(result.sdg_details)"></div>
            </div>
          </div>
        </div>
      </div>
    </BasicCard>
  </div>
</template>

<style lang="scss" scoped>
.analyze {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;

  .analyze-result-card {
    width: 90%;
    height: 90vh;
    overflow-y: scroll;
    overflow-x: hidden;

    .content {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 30px;

      .title {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 30px;
        width: 100%;

        .flag {
          img {
            width: 64px;
          }
        }
      }

      .section {
        width: 100%;
        padding: 0 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;

        h3 {
          font-size: 32px;
          font-weight: 700;
          margin-bottom: 10px;
        }

        p {
          font-size: 16px;
          font-weight: 400;
          line-height: 1.5;
        }

        ul {
          list-style-type: disc;
          padding-left: 20px;

          li {
            margin-bottom: 5px;
          }
        }
      }

      .close,
      .back {
        position: absolute;
        cursor: pointer;

        &:hover {
          scale: 110%;
        }
      }

      .close {
        top: 20px;
        right: 20px;
      }

      .back {
        top: 20px;
        left: 20px;
      }

      h2 {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
      }

      .results {
        display: flex;
        flex-direction: row;
        // height: 100%;
        width: 100%;
        gap: 30px;
        padding: 0px 15px;
        position: relative;

        .result {
          padding: 5px;
          cursor: pointer;

          &:hover {
            background-color: var(--neutral-light);
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
          }
        }

        .results-text {
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          flex: 1;
          gap: 40px;

          h3 {
            margin-bottom: -10px;
          }

          .chip {
            margin-bottom: 15px;
            font-size: 13px;
            font-weight: 500;
          }

          p {
            font-size: 20px;
            font-weight: 400;
          }
        }

        .camembert {
          width: 233px !important;
          height: 233px !important;
          position: relative;
          top: 50%;
          transform: translateY(-50%); // To center perfectly
        }
      }
    }
  }
}
</style>
