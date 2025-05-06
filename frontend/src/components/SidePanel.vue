<script setup lang="ts">
// Components
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiWeatherSunny, mdiWeatherNight } from '@mdi/js'
import BigButton from './Buttons/BigButton.vue'

// Stores
import { useThemeStore } from '@/stores/themeStore'
const themeStore = useThemeStore()

// Locales
import { useI18n } from 'vue-i18n'
const { locale, t } = useI18n()

import { useRoute } from 'vue-router'
import { computed } from 'vue'
const route = useRoute()

const activeTab = computed(() => {
  return route.name
})

import { useRouter } from 'vue-router'
const router = useRouter()

function changeLanguage(event: Event) {
  const selectedLanguage = (event.target as HTMLSelectElement).value
  locale.value = selectedLanguage
}

// Props
defineProps({
  isOpen: Boolean,
})
</script>

<template>
  <div class="side-panel" :class="{ open: isOpen }">
    <div class="header">
      <h1 @click="router.push({ name: 'home' })">CEP</h1>
    </div>
    <div class="content">
      <BigButton
        :text="$t('panel.analyze-patent')"
        icon="mdiProgressUpload"
        :is-active="activeTab === 'analyze'"
        :to="{ name: 'analyze' }"
      />
      <BigButton
        :text="$t('panel.explore-patents')"
        icon="mdiMapSearchOutline"
        :is-active="activeTab === 'explore'"
        :to="{ name: 'explore' }"
      />
      <BigButton
        :text="$t('panel.search-applicant')"
        icon="mdiBriefcaseSearchOutline"
        :is-active="activeTab === 'applicant'"
        :to="{ name: 'applicant' }"
      />
    </div>
    <div class="footer">
      <select class="language-selector" @change="changeLanguage">
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
      </select>
      <SvgIcon
        class="theme-icon"
        :path="themeStore.isDarkTheme ? mdiWeatherSunny : mdiWeatherNight"
        type="mdi"
        @click="themeStore.toggleTheme"
        :color="themeStore.isDarkTheme ? 'var(--secondary-text-color)' : 'var(--neutral-hightest)'"
        :size="24"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
/* Container styles */
.side-panel {
  --vertical-padding: 10px;
  --horizontal-padding: 10px;
  --height: 100vh;
  --width: 180px;

  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  width: calc(var(--width) - var(--horizontal-padding) * 2);
  height: calc(var(--height) - var(--vertical-padding) * 2);
  padding: var(--vertical-padding) var(--horizontal-padding);
  left: calc(-1 * var(--width)); /* Hidden by default */
  transform: translateX(0);
  transition: transform 0.3s ease-in-out;
  z-index: 1000;

  background-color: var(--neutral-lower);
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);

  .header {
    display: flex;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;

    h1 {
      font-size: 64px;
      font-weight: 800;
      color: var(--neutral-hightest);
    }
  }

  .content {
    overflow-y: auto;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
  }

  .footer {
    display: flex;
    padding: 10px;

    .theme-icon {
      cursor: pointer;
      margin-left: auto;
    }

    .language-selector {
      margin-left: 10px;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 4px;
      background-color: #fff;
      color: #000;
      font-size: 14px;
    }
  }
}
.side-panel.open {
  transform: translateX(var(--width)); /* Slide in */
}
</style>
