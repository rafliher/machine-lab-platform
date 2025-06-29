<template>
  <MainLayout>
    <div v-if="isLoading" class="isLoading-overlay">
      <div class="spinner"></div>
    </div>
    <div class="container-dashboard">
      <div class="chart-section">
        <h3>Grafik Kontainer Aktif</h3>
        <div class="chart-wrapper">
          <canvas id="containerChart"></canvas>
        </div>
      </div>

      <div class="header">
        <h3 class="header-title">Monitoring Container Aktif</h3>
        <button @click="showAddContainerForm = true" class="submit-upload">+ Tambah Container</button>
      </div>
      
      <div class="search-section">
        <input v-model="searchQuery" placeholder="Nama Container" class="input-name" />
      </div>

      <table class="container-table">
        <thead>
          <tr>
            <th>Nama</th>
            <th>Status</th>
            <th>UserId</th>
            <th>HostId</th>
            <th>ContainerId</th>
            <th>Created</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="container in filteredContainers" :key="container.id">
            <td>{{ container.name }}</td>
            <td :class="container.status">{{ container.status }}</td>
            <td>{{ container.user_id }}</td>
            <td>{{ container.host_id }}</td>
            <td>{{ container.id }}</td>
            <td>{{ formatDate(container.created_at) }}</td>
            <td>
              <button @click="viewDetail(container.id)" class="action-btn" title="Detail">
                <i class="fa fa-eye"></i> Detail
              </button>
              <button @click="restart(container.id)" class="action-btn" title="Restart">
                <i class="fa fa-rotate-right"></i> Restart
              </button>
              <button @click="remove(container.id)" class="action-btn" title="Hapus">
                <i class="fa fa-trash"></i> Delete
              </button>

            </td>
          </tr>
        </tbody>
      </table>
      <ContainerForm
        v-if="showAddContainerForm"
        @add-container="handleAddContainer"
        @close="showAddContainerForm = false"
      />
      <ContainerDetail
        v-if="showDetailModal"
        :detail="detailData"
        @close="showDetailModal = false"
      />
    </div>
  </MainLayout>
</template>

<script>
import Chart from 'chart.js/auto';
import MainLayout from '../layouts/MainLayout.vue';
import ContainerForm from '../components/ContainerForm.vue';
import ContainerDetail from '../components/ContainerDetail.vue';
import { listContainer, deleteContainer, restartContainer, getContainerData } from '../services/apiContainerService';
import dayjs from 'dayjs';
import { useToast } from 'vue-toastification';
import { addContainer } from '../services/apiContainerService';

export default {
  components: { MainLayout, ContainerForm, ContainerDetail },
  data() {
    return {
      zipFile: null,
      searchQuery: '',
      showAddContainerForm: false,
      containers: [],
      isLoading: false,
      showDetailModal: false,
      detailData: {},
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  computed: {
    filteredContainers() {
      const q = this.searchQuery.toLowerCase();
      return this.containers.filter(c =>
        c.name.toLowerCase().includes(q) ||
        c.host_id.toLowerCase().includes(q) ||
        c.status.toLowerCase().includes(q)
      );
    }
  },
  methods: {
    async handleAddContainer(user_id, data) {
      if (this.isLoading) return;
      if (!data) return;
      this.isLoading = true;
      try {
        await addContainer(user_id, data);
        this.fetchContainers();
        this.toast.success('Container berhasil ditambahkan');
        this.showAddHostModal = false;
      } catch (error) {
        console.error('Gagal menambahkan container:', error);
        this.toast.error('Gagal menambahkan container');
      } finally {
        this.isLoading = false;
      }
    },
    async viewDetail(id) {
      this.isLoading = true;
      try {
        const res = await getContainerData(id);
        this.detailData = res.data;
        this.showDetailModal = true;
      } catch (err) {
        console.error('Gagal mengambil detail:', err);
        this.toast.error('Gagal mengambil detail container');
      } finally {
        this.isLoading = false;
      }
    },
    formatDate(datetime) {
      return dayjs(datetime).format('YYYY-MM-DD HH:mm');
    },
    async fetchContainers() {
      this.isLoading = true;
      try {
        const res = await listContainer();
        this.containers = res.data;
        this.renderChart();
      } catch (error) {
        console.error(error);
        this.toast.error('Gagal memuat data container');
      } finally {
        this.isLoading = false;
      }
    },
    async restart(id) {
      this.isLoading = true;
      console.log(this.isLoading);
      try {
        await restartContainer(id);
        this.fetchContainers();
        this.toast.success('Container berhasil direstart');
      } catch (error) {
        console.error(error);
        this.toast.error('Gagal me-restart container');
      } finally {
        this.isLoading = false;
      }
    },
    async remove(id) {
      this.isLoading = true;
      try {
        await deleteContainer(id);
        this.toast.success('Container dihapus');
        this.fetchContainers();
      } catch (error) {
        console.error(error);
        this.toast.error('Gagal menghapus container');
      } finally {
        this.isLoading = false;
      }
    },
    renderChart() {
      const running = this.containers.filter(c => c.status === 'running').length;
      const stopped = this.containers.filter(c => c.status === 'stopped').length;
      const ctx = document.getElementById('containerChart');
      if (ctx._chart) {
        ctx._chart.destroy();
      }
      const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Running', 'Stopped'],
          datasets: [{
            data: [running, stopped],
            backgroundColor: ['#2ecc71', '#e74c3c']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
      });
      ctx._chart = chart;
    }
  },
  mounted() {
    this.fetchContainers();
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.container-dashboard {
  margin: 2em auto;
  width: 100%;
  max-width: 1200px;
  background: rgba(20, 20, 30, 0.95);
  padding: 2em;
  border-radius: 12px;
  font-family: 'Share Tech Mono', monospace;
  color: #f5f5f5;
}

.header {
  margin-top: 2em;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
}


.header-title {
  margin-bottom: 0.5em;
  font-size: 1.25rem;
  font-weight: 600;
  color: #ff3d3d;
}

.upload-btn {
  background: #ff3d3d;
  color: #f5f5f5;
  padding: 0.5em 1em;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  text-transform: uppercase;
}

.input-name {
  padding: 0.5em;
  border-radius: 8px;
  border: 1px solid #ff3d3d;
  min-width: 180px;
  background: #222;
  color: #f5f5f5;
}

.submit-upload {
  background-color: #ff3d3d;
  color: #f5f5f5;
  border: none;
  padding: 0.5em 1em;
  border-radius: 8px;
  cursor: pointer;
  text-transform: uppercase;
}

.submit-upload:hover {
  box-shadow: 0px 0px 15px #ff3d3d80;
}

.container-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1em;
  font-size: 0.95rem;
}

.container-table th,
.container-table td {
  padding: 0.75em;
  text-align: left;
  border-bottom: 1px solid #ff3d3d30;
}

.container-table th {
  background: #222;
  color: #ff3d3d;
  text-transform: uppercase;
}

.running {
  color: #00ff00;
  font-weight: bold;
}

.stopped {
  color: #ff3d3d;
  font-weight: bold;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  margin-right: 0.5em;
  font-size: 14px;
  color: #f5f5f5;
}

.action-btn:hover {
  color: #ff3d3d;
}

.chart-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1em;
  margin-bottom: 2em;
}

.chart-wrapper {
  width: 200px;
  height: 200px;
  background: #111;
  padding: 1em;
  border-radius: 12px;
  box-shadow: 0px 0px 25px #ff3d3d30;
}

.chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
}

.isLoading-overlay {
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

.modal-content {
  background: #1e1e2f;
  padding: 2em;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  color: #f5f5f5;
  font-family: monospace;
  box-shadow: 0 0 25px #ff3d3d40;
}

</style>
