import { createApp } from 'vue'; // Vue 3 使用 createApp
import App from './App.vue';
import router from './router';

createApp(App)
  .use(router)
  .mount('#app');
  