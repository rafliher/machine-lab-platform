import api from './api';

export function login(username, password) {
  return api.post('/auth/login', { "email": username, password });
}

export function logout() {
  return api.post('/logout');
}

export function changePassword(currentPassword, newPassword) {
  return api.post('/change-password', { currentPassword, newPassword });
}

export function getAccessKey() {
  return api.get('/access-key');
}
