import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import './assets/main.css';



import VueCookies from 'vue-cookies';

const app = createApp(App);
app.use(router);
app.use(store);
app.use(VueCookies);
app.use(Toast);
app.mount('#app');