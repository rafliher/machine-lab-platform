import Cookies from 'vue-cookies';

export function isAuthenticated() {
  return !!Cookies.get('token');
}