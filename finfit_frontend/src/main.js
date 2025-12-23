import { createApp } from 'vue'
import App from './App.vue';
import { useKakao } from 'vue3-kakao-maps/@utils';
import { createPinia } from 'pinia'

import router from './router'
import { API_KEY } from './pages/apikey';

useKakao(API_KEY);
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
