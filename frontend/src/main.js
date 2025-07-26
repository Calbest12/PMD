import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import services
import authService from './services/authService'
import projectService from './services/projectService'
import feedbackService from './services/feedbackService'
import aiService from './services/aiService'
import careerService from './services/careerService'

const app = createApp(App)

// Register services globally
app.config.globalProperties.$authService = authService
app.config.globalProperties.$projectService = projectService
app.config.globalProperties.$feedbackService = feedbackService
app.config.globalProperties.$aiService = aiService
app.config.globalProperties.$careerService = careerService

app.use(router).mount('#app')
