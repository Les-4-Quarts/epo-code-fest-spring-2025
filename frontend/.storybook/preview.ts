// filepath: frontend/.storybook/preview.ts
import type { Preview } from '@storybook/vue3';
import { themes } from '@storybook/theming';
import '../src/assets/main.css';

const preview: Preview = {
  parameters: {
    darkMode: {
      // Dark theme
      dark: { ...themes.dark, appBg: 'black' },
      // Light theme
      light: { ...themes.light, appBg: 'white' },
      // Default theme
      current: 'light',
    },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
  tags: ['autodocs'],
};

export default preview;