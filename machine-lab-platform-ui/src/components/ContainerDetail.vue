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
          <span class="label">Image:</span>
          <span class="value">{{ detail.image }}</span>
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
export default {
  props: {
    detail: {
      type: Object,
      required: true
    }
  }
};
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
