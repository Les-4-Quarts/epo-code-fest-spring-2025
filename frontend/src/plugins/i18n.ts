import { createI18n } from "vue-i18n";
import fr from "@/locales/fr";
import en from "@/locales/en";
import de from "@/locales/de";

export default createI18n({
    legacy: false,
    locale: "en",
    fallbackLocale: "en",
    messages: {
        en,
        fr,
        de,
    },
});