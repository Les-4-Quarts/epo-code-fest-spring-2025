<script setup lang="ts">
//Locales
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

// Components
import BasicCard from '@/components/Cards/BasicCard.vue'
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiPlusBox } from '@mdi/js'
import BasicButton from '@/components/Buttons/BasicButton.vue'
import SpinnerLoader from '@/components/Loaders/SpinnerLoader.vue'

// Refs
import { ref } from 'vue'
import BasicChip from '@/components/Chips/BasicChip.vue'
const selectedFile = ref<File | null>(null)
const analysisResult = ref([
  {
    text: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 1: No Poverty',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 2: Zero Hunger',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 1: No Poverty',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 3: Good Health and Well-being',
  },

  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 2: Zero Hunger',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 2: Zero Hunger',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 2: Zero Hunger',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 2: Zero Hunger',
  },
  {
    text: '  Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas numquam, libero illum error possimus atque recusandae repellat deserunt ut. Dolor quam at repellat, eveniet unde ex quo voluptatem perferendis esse?',
    sdg: 'SDG 2: Zero Hunger',
  },
])
const isLoading = ref(false)

// Methods
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
        console.log('File uploaded successfully:', data)
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
</script>

<template>
  <div class="analyze">
    <BasicCard class="analyze-card" v-if="!isLoading && !analysisResult">
      <div class="content" @click="openFileDialog">
        <SvgIcon type="mdi" :path="mdiPlusBox" :size="86" />
        <h2>{{ $t('analyze.upload') }}</h2>

        <div v-if="selectedFile" class="file-info">
          <span>{{ $t('analyze.fileSelected') }}: {{ selectedFile.name }}</span>
          <BasicButton :text="$t('analyze.analyze')" @click="handleFileSend" />
        </div>
      </div>

      <!-- Hidden input -->
      <input id="file-input" type="file" style="display: none" @change="handleFileChange" />
    </BasicCard>

    <SpinnerLoader v-else-if="isLoading" :size="16" :border-width="1" />

    <BasicCard v-else class="analyze-result-card">
      <div class="content">
        <h2>{{ $t('analyze.about') }}</h2>
        <div class="results">
          <div class="results-text">
            <div v-for="(result, index) in analysisResult" :key="index">
              <BasicChip
                class="chip"
                :title="result.sdg"
                color="white"
                :bgColor="`var(--${result.sdg.split(':')[0].trim().toLowerCase().replace(' ', '-')})`"
              />
              <p>
                {{ result.text }}
              </p>
            </div>
          </div>
          <div class="camembert"></div>
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
          font-weight: 600;
          text-align: center;
        }

        button:hover {
          scale: 110%;
        }
      }
    }

    &:hover {
      scale: 105%;
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
        gap: 30px;
        padding: 0px 15px;

        .results-text {
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          gap: 41px;

          .chip {
            margin-bottom: 15px;
            font-size: 13px;
            font-weight: 500;
          }

          p {
            font-size: 20px;
            font-weight: 600;
          }
        }

        .camembert {
          width: 233px;
          height: 233px;
          background-color: var(--neutral-highter);
          border-radius: 50%;
          flex-shrink: 0; // Prevent the camembert from shrinking
          position: sticky;
          top: 50%;
          transform: translateY(-50%); // To center perfectly
        }
      }
    }
  }
}
</style>
