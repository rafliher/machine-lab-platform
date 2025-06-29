<template>
  <div class="container-form">
    <h3>Tambah Container</h3>
    <form @submit.prevent="submit">
      <label>
        User ID:
        <input v-model="userId" required placeholder="Masukkan User ID" />
      </label>
      <label>
        Container Name:
        <input v-model="name" required placeholder="Masukkan Nama Container" />
      </label>

      <label>
        File ZIP:
        <input type="file" accept=".zip" @change="handleFileUpload" required />
      </label>

      <div class="form-actions">
        <button type="submit">Upload</button>
        <button type="button" @click="$emit('close')">Batal</button>
      </div>
    </form>
  </div>
</template>

<script>

export default {
  data() {
    return {
      userId: '',
      name: '',
      file: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async submit() {
      if (!this.userId || !this.file) {
        alert('User ID dan file ZIP harus diisi.');
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        this.$emit('add-container', this.userId, this.name, formData);
        this.$emit('close');
      } catch (error) {
        console.error('Gagal menambahkan container:', error);
        alert('Gagal menambahkan container.');
      }
    }
  }
};
</script>

<style scoped>
.container-form {
  background: #222;
  padding: 1em;
  border-radius: 8px;
  font-family: 'Share Tech Mono', monospace;
  color: #fff;
}

label {
  display: block;
  margin-bottom: 1em;
}

input[type="text"],
input[type="file"] {
  width: 100%;
  background: #111;
  color: #fff;
  border: 1px solid #555;
  border-radius: 4px;
  padding: 0.5em;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1em;
}
</style>
