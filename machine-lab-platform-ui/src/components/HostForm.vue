<template>
  <div class="host-form">
    <h3>{{ isEdit ? 'Edit Host' : 'Tambah Host' }}</h3>
    <form @submit.prevent="handleSubmit">
      <!-- hanya ditampilkan saat register -->
      <div v-if="!isEdit">
        <label>
          Nama Host:
          <input v-model="form.hostname" required />
        </label>
        <label>
          SSH Port:
          <input type="number" v-model.number="form.ssh_port" min="1" required />
        </label>
        <label>
          API Port:
          <input type="number" v-model.number="form.api_port" min="1" required />
        </label>
      </div>

      <!-- ditampilkan baik untuk edit maupun tambah -->
      <label>
        IP Address:
        <input v-model="form.ip" required />
      </label>
      <label>
        Maksimal Container:
        <input type="number" v-model.number="form.max_containers" min="1" required />
      </label>

      <div class="form-actions">
        <!-- Pastikan TIDAK ada @click di tombol submit -->
        <button type="submit">{{ isEdit ? 'Simpan' : 'Tambah' }}</button>
        <button type="button" @click="$emit('close')">Batal</button>
      </div>
    </form>
  </div>
</template>


<script>
export default {
  props: {
    host: {
      type: Object,
      default: () => ({})
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      form: {
        hostname: '',
        ip: '',
        ssh_port: 22,
        api_port: 8003,
        max_containers: 1
      }
    };
  },
  watch: {
    host: {
      immediate: true,
      handler(newHost) {
        if (this.isEdit) {
          this.form.ip = newHost.ip || '';
          this.form.max_containers = newHost.max_containers || 1;
        } else {
          this.form = { ...this.form, ...newHost };
        }
      }
    }
  },
  methods: {
    handleSubmit() {
        console.log('Clicked');
        if(this.isEdit){
            const data = {
                ip: this.form.ip,
                max_containers: this.form.max_containers,
            };
            this.$emit('edit-host', data);
        }
        else{
            const data = {
                hostname: this.form.hostname,
                ip: this.form.ip,
                ssh_port: this.form.ssh_port,
                api_port: this.form.api_port,
                max_containers: this.form.max_containers,
            };
            this.$emit('add-host', data);
        }
    },
  }
};
</script>

<style scoped>
.host-form {
  padding: 1em;
  background: #222;
  border-radius: 8px;
  color: #fff;
  font-family: 'Share Tech Mono', monospace;
}

label {
  display: block;
  margin-bottom: 1em;
  font-size: 14px;
}

input {
  width: 100%;
  padding: 0.5em;
  margin-top: 0.25em;
  background: #111;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1em;
}
</style>
