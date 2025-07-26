import api from './api';
import Cookies from 'vue-cookies';

export function login(username, password) {
  return api.post('/auth/login', { "email": username, password });
}

export function logout() {
  return api.post('/logout');
}

export function changePassword(currentPassword, newPassword) {
  return api.post('/auth/change-password', { "current_password": currentPassword, "new_password": newPassword });
}

export function rotateKey() {
  return api.post('/auth/rotate-key');
}
export function getAdminToken() {
  return Cookies.get("token");
}