<template>
  <MainLayout>
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
    </div>
    <div class="host-management">
      <div class="header">
        <h2>Manajemen Host</h2>
        <button class="add-button" @click="showAddHostModal = true">+ Tambah Host</button>
      </div>
      <div class="search-section">
        <input v-model="searchQuery" placeholder="Nama Hosts" class="input-name" />
      </div>
      <table class="host-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nama Host</th>
            <th>IP Address</th>
            <th>Status</th>
            <th>Memory Usage</th>
            <th>Waktu Deploy</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="host in filteredHosts" :key="host.id">
            <td>{{ host.id }}</td>
            <td>{{ host.hostname }}</td>
            <td>{{ host.ip }}</td>
            <td :class="host.status">{{ host.status }}</td>
            <td>
              <div class="usage-bar">
                <div class="usage-fill" :style="{ width: host.mem_percent + '%' }"></div>
              </div>
              <small>{{ host.mem_percent }}%</small>
            </td>
            <td>{{ formatTime(host.last_seen) }}</td>
            <td class="actions">
              <button class="edit" @click="editHost(host)">
                <i class="fa fa-edit"></i>
              </button>
              <button class="delete" @click="deleteHost(host.id)">
                <i class="fa fa-trash"></i>
              </button>
              <button class="monitor">
                <i class="fa fa-chart-bar"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <HostForm
        v-if="showAddHostModal"
        :key="'add-host-form'"
        @add-host="handleAddHost"
        @close="showAddHostModal = false"
      />
      <HostForm
        v-if="showEditHostModal"
        :key="'edit-host-form'"
        :host="selectedHost"
        :isEdit="true"
        @edit-host="handleEditHost"
        @close="showEditHostModal = false"
      />
    </div>
    <div v-if="showCredentialModal" class="modal-credential-overlay">
      <div class="modal-credential-content">
        <h3 class="modal-title">Host Ditambahkan</h3>
        <p><strong>Host ID:</strong></p>
        <div class="code-box">{{ newHostCredentials.host_id }}</div>
        <p><strong>Server Key:</strong></p>
        <div class="code-box">{{ newHostCredentials.server_key }}</div>
        <button class="close-button" @click="showCredentialModal = false">Tutup</button>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import { listHost, deleteHost } from '../services/apiHostService';
import HostForm from '../components/HostForm.vue';
import { registerHost, updateHost } from '../services/apiHostService';
import { useToast } from 'vue-toastification';
import MainLayout from '../layouts/MainLayout.vue';
import dayjs from 'dayjs';

export default {
  name: 'HostManagement',
  components: { MainLayout, HostForm },
  data() {
    return {
      hosts: [],
      showEditHostModal: false,
      selectedHost: null,
      showAddHostModal: false,
      isLoading: false,
      showCredentialModal: false,
      searchQuery: '',
      newHostCredentials: {
        host_id: '',
        server_key: ''
      },
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    filteredHosts() {
      const q = this.searchQuery.toLowerCase();
      return this.hosts.filter(c =>
        c.hostname.toLowerCase().includes(q) ||
        c.ip.toLowerCase().includes(q) ||
        c.status.toLowerCase().includes(q)
      );
    }
  },
  methods: {
    async fetchHosts() {
      try {
        const response = await listHost();
        this.hosts = response.data;
      } catch (error) {
        console.error('Gagal mengambil data host:', error);
        this.toast.error('Gagal memuat data host');
      }
    },
    formatTime(timeString) {
      return dayjs(timeString).format('YYYY-MM-DD HH:mm');
    },
    async handleAddHost(data) {
      if (this.loading) return;
      if (!data) return;
      this.isLoading = true;
      try {
        const response = await registerHost(data);
        this.newHostCredentials = {
          host_id: response.data.host_id,
          server_key: response.data.server_key
        };
        this.showCredentialModal = true;
        this.fetchHosts();
        this.toast.success('Host berhasil ditambahkan');
        this.showAddHostModal = false;
      } catch (error) {
        console.error('Gagal menambahkan host:', error);
        this.toast.error('Gagal menambahkan host');
      } finally {
        this.isLoading = false;
      }
    },
    async handleEditHost(data) {
      if (this.loading) return;
      this.isLoading = true;
      try {
        await updateHost(this.selectedHost.id, data);
        this.fetchHosts();
        this.toast.success('Host berhasil diperbarui');
        this.showEditHostModal = false;
        this.selectedHost = null;
      } catch (error) {
        console.error('Gagal mengedit host:', error);
        this.toast.error('Gagal memperbarui host');
      } finally {
        this.isLoading = false;
      }
    },
    editHost(host) {
      this.selectedHost = host;
      this.showEditHostModal = true;
    },
    async deleteHost(id) {
      if (confirm('Yakin ingin menghapus host ini?')) {
        this.isLoading = true;
        try {
          await deleteHost(id);
          this.fetchHosts();
          this.toast.success('Host berhasil dihapus');
        } catch (error) {
          console.error('Gagal menghapus host:', error);
          this.toast.error('Gagal menghapus host');
        } finally {
          this.isLoading = false;
        }
      }
    }
  },
  mounted() {
    this.fetchHosts();
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.host-management {
  background: rgba(20, 20, 30, 0.95);
  padding: 2em;
  border-radius: 12px;
  font-family: 'Share Tech Mono', monospace;
  color: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
}

.header h2 {
  font-size: 1.5rem;
  color: #ff3d3d;
}

.add-button {
  background-color: #ff3d3d;
  color: #f5f5f5;
  border: none;
  padding: 0.5em 1em;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  text-transform: uppercase;
  transition: box-shadow 0.2s, transform 0.2s;
}

.add-button:hover {
  box-shadow: 0px 0px 15px #ff3d3d80;
  transform: translateY(-2px);
}

.host-table {
  margin-top: 1em;
  width: 100%;
  border-collapse: collapse;
  background: #111;
  border-radius: 12px;
  overflow: hidden;
}

.host-table th,
.host-table td {
  padding: 0.75em 1em;
  text-align: left;
  border-bottom: 1px solid #ff3d3d30;
}

.host-table th {
  background-color: #222;
  color: #ff3d3d;
  text-transform: uppercase;
}

.healthy {
  color: #00ff00;
  font-weight: bold;
}

.unhealthy {
  color: #ff3d3d;
  font-weight: bold;
}

.usage-bar {
  height: 8px;
  width: 100%;
  background: #333;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 4px;
}

.usage-fill {
  height: 100%;
  background: #ff3d3d;
  transition: width 0.3s ease;
}

.actions button {
  margin-right: 0.5em;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 0.25em 0.5em;
  border-radius: 6px;
  color: #f5f5f5;
  transition: color 0.2s, box-shadow 0.2s;
}

.actions button:hover {
  color: #ff3d3d;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(20, 20, 30, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.spinner {
  border: 6px solid #ccc;
  border-top: 6px solid #ff3d3d;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.modal-credential-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(10, 10, 20, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-credential-content {
  background: #1c1c2b;
  border: 1px solid #ff3d3d60;
  padding: 2em;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  font-family: 'Share Tech Mono', monospace;
  color: #f5f5f5;
  text-align: center;
  box-shadow: 0px 0px 20px #ff3d3d40;
}

.modal-title {
  color: #ff3d3d;
  margin-bottom: 1em;
  font-size: 1.3rem;
}

.input-name {
  padding: 0.5em;
  border-radius: 8px;
  border: 1px solid #ff3d3d;
  min-width: 180px;
  background: #222;
  color: #f5f5f5;
}

.code-box {
  background-color: #111;
  border: 1px solid #ff3d3d50;
  padding: 0.75em;
  margin: 0.5em 0 1em;
  border-radius: 8px;
  word-break: break-all;
  color: #00ff88;
}

.close-button {
  margin-top: 1em;
  background-color: #ff3d3d;
  color: #f5f5f5;
  border: none;
  padding: 0.5em 1.5em;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  text-transform: uppercase;
  transition: background 0.2s, transform 0.2s;
}

.close-button:hover {
  background-color: #e62e2e;
  transform: scale(1.05);
}

</style>
