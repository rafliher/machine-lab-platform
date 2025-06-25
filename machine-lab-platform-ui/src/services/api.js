import axios from 'axios';
import Cookies from 'vue-cookies';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
});

api.interceptors.request.use(config => {
  const token = Cookies.get('token');
  if (token) {
    config.headers['X-Admin-Key'] = token;
  }
  return config;
});

export default api;
