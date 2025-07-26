import api from './api';

/**
 * Download (or create) an OpenVPN profile for a given clientName.
 * Returns a Blob you can save as `${clientName}.ovpn`.
 */
export function getVpnProfile(clientName) {
  return api.post(
    '/users/vpn',
    { client_name: clientName },
    { responseType: 'blob' }
  );
}

/**
 * Rotate (revoke + re-generate) an OpenVPN profile for a given clientName.
 * Returns a Blob you can save as `${clientName}.ovpn`.
 */
export function rotateVpnProfile(clientName) {
  return api.post(
    `/users/vpn/${encodeURIComponent(clientName)}/rotate`,
    null,
    { responseType: 'blob' }
  );
}
