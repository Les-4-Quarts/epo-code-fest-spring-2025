<script setup lang="ts">
import { marked } from 'marked'

//Locales
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiPlusBox, mdiClose, mdiArrowLeft } from '@mdi/js'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import SpinnerLoader from '@/components/Loaders/SpinnerLoader.vue'

// Refs
import { computed, ref } from 'vue'
import BasicChip from '@/components/Chips/BasicChip.vue'
import { Doughnut } from 'vue-chartjs'
import type { Analysis } from '@/types/Analysis'
const selectedFile = ref<File | null>(null)
const analysisResult = ref<Analysis[] | null>(null)
const isLoading = ref(false)
const sdgSelected = ref('')

const filteredResults = computed(() => {
  if (!analysisResult.value) {
    return null
  }
  return analysisResult.value.filter((result) => result.sdg === sdgSelected.value)
})

const doughnutData = computed(() => {
  if (!analysisResult.value) {
    return null
  }

  // Retrive all labels from the analysis result. Keep only unique labels
  const labels = analysisResult.value
    .map((result) => result.sdg)
    .filter((value, index, self) => self.indexOf(value) === index)

  // Count the number of times each label appears in the analysis result
  const data = labels.map((label) => {
    if (!analysisResult.value) {
      return 0
    }
    return analysisResult.value.filter((result) => result.sdg === label).length
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

// Methods
const renderMarkdown = (markdown: string | undefined) => {
  if (!markdown) return ''
  return marked(markdown, { breaks: true })
}

function openFileDialog() {
  const fileInput = document.getElementById('file-input') as HTMLInputElement
  if (fileInput) {
    fileInput.click()
  }
}

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    // Verify thah the file is a PDF
    if (input.files[0].type !== 'application/pdf') {
      alert(t('analyze.error.fileType'))
      return
    }
    selectedFile.value = input.files[0]
  }
}

function handleFileSend() {
  const base_api_url = import.meta.env.VITE_BASE_API_URL
  const file = selectedFile.value
  isLoading.value = true
  if (file) {
    // Create a FormData object to send the file
    const formData = new FormData()
    formData.append('pdf_file', file)

    // Send the file to the backend
    fetch(`${base_api_url}/patents/analyze`, {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then((data) => {
        analysisResult.value = data
      })
      .catch((error) => {
        console.error('Error uploading file:', error)
      })
      .finally(() => {
        isLoading.value = false
        selectedFile.value = null // Reset the selected file
      })
  }
}

function backResults() {
  sdgSelected.value = ''
}

function closeResults() {
  analysisResult.value = null
}

function cssvar(name: string) {
  return getComputedStyle(document.documentElement).getPropertyValue(name)
}
</script>

<template>
  <div class="analyze">
    <BasicCard class="analyze-card" v-if="!isLoading && !analysisResult">
      <div class="content" @click="openFileDialog">
        <SvgIcon type="mdi" :path="mdiPlusBox" :size="86" />
        <h2>{{ $t('analyze.upload') }}</h2>

        <div v-if="selectedFile" class="file-info">
          <span>{{ $t('analyze.fileSelected') }}: {{ selectedFile.name }}</span>
          <BasicButton
            :text="$t('analyze.analyze')"
            @click="handleFileSend"
            color="var(--neutral-lowest)"
            bg-color="var(--primary-highter)"
          />
        </div>
      </div>

      <!-- Hidden input -->
      <input id="file-input" type="file" style="display: none" @change="handleFileChange" />
    </BasicCard>

    <SpinnerLoader v-else-if="isLoading" :size="16" :border-width="1" />

    <BasicCard v-else-if="!sdgSelected" class="analyze-result-card">
      <div class="content">
        <SvgIcon class="close" type="mdi" :path="mdiClose" @click="closeResults" />
        <h2>{{ $t('analyze.about') }}</h2>
        <div class="results">
          <div class="results-text">
            <div
              v-for="(result, index) in analysisResult"
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
              <p>
                {{ result.sdg_details }}
              </p>
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

  .analyze-card {
    width: 412px;
    height: 504px;
    transition:
      transform 0.3s ease-in-out,
      background-color 0.3s ease-in-out,
      color 0.3s ease-in-out;

    .content {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 29px;

      h2 {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
      }

      .file-info {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 40px;
        gap: 10px;

        span {
          font-size: 20px;
          font-weight: 400;
          text-align: center;
        }

        button:hover {
          scale: 110%;
        }
      }
    }
    &:hover {
      transform: scale(105%);
      cursor: pointer;
    }
  }

  .analyze-result-card {
    width: 90%;
    height: 90vh;

    .content {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 29px;

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
        overflow-y: scroll;
        height: 100%;
        width: 100%;
        gap: 30px;
        padding: 0px 15px;

        .result {
          cursor: pointer;
        }

        .results-text {
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          flex: 1;
          gap: 41px;

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
          position: sticky;
          top: 50%;
          transform: translateY(-50%); // To center perfectly
        }
      }
    }
  }
}
</style>
