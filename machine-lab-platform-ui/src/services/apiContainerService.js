import api from './api';

export function listContainer() {
  return api.get('/containers/');
}

export function addContainer(userId, containerData) {
  return api.post(`/containers/launch?user_id=${userId}`, containerData);
}

export function getContainerData(containerId) {
  return api.get(`/containers/${containerId}`);
}

export function deleteContainer(containerId) {
  return api.delete(`/containers/${containerId}`);
}

export function restartContainer(containerId) {
  return api.post(`/containers/${containerId}/restart`);
}