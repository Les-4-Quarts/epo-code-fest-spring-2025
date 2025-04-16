import i18n from "./i18n";
import pinia from "./pinia";

import type { App } from "vue";

export function registerPlugins(app: App) {
    app.use(i18n);
    app.use(pinia);
}