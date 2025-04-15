import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
    state: () => ({
        isDarkTheme: localStorage.getItem('isDarkTheme') === 'true' || false,
    }),
    actions: {
        toggleTheme() {
            this.isDarkTheme = !this.isDarkTheme;
            localStorage.setItem('isDarkTheme', this.isDarkTheme.toString());
        },
        setLightTheme() {
            this.isDarkTheme = false;
            localStorage.setItem('isDarkTheme', this.isDarkTheme.toString());
        },
        setDarkTheme() {
            this.isDarkTheme = true;
            localStorage.setItem('isDarkTheme', this.isDarkTheme.toString());
        },
    },
});