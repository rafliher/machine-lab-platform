<template>
  <div class="modal-overlay">
    <div class="modal-box">
      <h3 class="modal-title">Detail Container</h3>

      <div class="detail-grid">
        <div class="detail-row">
          <span class="label">ID:</span>
          <span class="value">{{ detail.id }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Nama:</span>
          <span class="value">{{ detail.name }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Host ID:</span>
          <span class="value">{{ detail.host_id }}</span>
        </div>
        <div class="actions" :style="{marginTop: '0'}">
          <button class="btn-vpn" :disabled="downloading" @click="downloadVpn()">
            {{ downloading ? 'Downloading…' : 'Download User VPN Profile' }}
          </button>
          <button class="btn-vpn" :disabled="rotating" @click="rotateVpn()">
            {{ rotating ? 'Rotating…' : 'Rotate User VPN Profile' }}
          </button>
        </div>
        <div class="detail-row">
          <span class="label">User ID:</span>
          <span class="value">{{ detail.user_id }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Status:</span>
          <span class="value" :class="detail.status">{{ detail.status }}</span>
        </div>
        <div class="detail-row">
          <span class="label">IP Address:</span>
          <span class="value">{{ detail.ip_address }}</span>
        </div>
      </div>

      <div class="actions">
        <button @click="$emit('close')" class="btn-close">Tutup</button>
      </div>
    </div>
  </div>
</template>

<script>
import { saveAs } from 'file-saver'
import { getVpnProfile, rotateVpnProfile } from '../services/apiUserService'

export default {
  props: {
    detail: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      downloading: false,
      rotating: false
    }
  },
  methods: {
    async downloadVpn() {
      this.downloading = true
      try {
        // call the API to get (or create) the profile
        const resp = await getVpnProfile(this.detail.user_id)
        const blob = new Blob([resp.data], {
          type: 'application/x-openvpn-profile'
        })
        saveAs(blob, `${this.detail.user_id}.ovpn`)
      } catch (e) {
        console.error('Failed to download VPN profile', e)
        this.$notify({
          type: 'error',
          title: 'Error',
          text: 'Could not download VPN profile.'
        })
      } finally {
        this.downloading = false
      }
    },
    async rotateVpn() {
      this.rotating = true
      try {
        // call the API to revoke + re-create the profile
        const resp = await rotateVpnProfile(this.detail.user_id)
        const blob = new Blob([resp.data], {
          type: 'application/x-openvpn-profile'
        })
        saveAs(blob, `${this.detail.user_id}.ovpn`)
      } catch (e) {
        console.error('Failed to rotate VPN profile', e)
        this.$notify({
          type: 'error',
          title: 'Error',
          text: 'Could not rotate VPN profile.'
        })
      } finally {
        this.rotating = false
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 10, 10, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-box {
  background: #1e1e2f;
  padding: 2em;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  color: #f5f5f5;
  box-shadow: 0 0 25px #ff3d3d40;
  font-family: 'Share Tech Mono', monospace;
}

.modal-title {
  font-size: 1.4rem;
  margin-bottom: 1.5em;
  color: #ff3d3d;
}

.detail-grid {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #ff3d3d30;
  padding-bottom: 0.5em;
}

.label {
  font-weight: bold;
  color: #ff3d3d;
}

.value {
  color: #f5f5f5;
}

.running {
  color: #00ff00;
}

.stopped {
  color: #ff3d3d;
}

.actions {
  margin-top: 2em;
  text-align: right;
  display: flex;
  gap: 0.5em;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.btn-vpn {
  background-color: #0066cc;
  color: #fff;
  border: none;
  padding: 0.5em 1em;
  border-radius: 6px;
  cursor: pointer;
}

.btn-vpn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-vpn:hover:not([disabled]) {
  box-shadow: 0 0 10px #0066cc80;
}

.btn-close {
  background-color: #ff3d3d;
  color: #fff;
  border: none;
  padding: 0.5em 1.2em;
  border-radius: 6px;
  cursor: pointer;
}

.btn-close:hover {
  box-shadow: 0 0 10px #ff3d3d80;
}
</style>
