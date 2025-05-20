import './assets/main.css'
import { createApp } from 'vue'
import { registerPlugins } from './plugins'
import App from './App.vue'
import router from './router'

// Import the functions you need from the SDKs you need
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale,
    LinearScale,
} from 'chart.js'

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale,
    LinearScale
)

const app = createApp(App)
registerPlugins(app)
app.use(router)

app.mount('#app')
