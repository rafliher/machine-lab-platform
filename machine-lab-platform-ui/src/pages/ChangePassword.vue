<template>
  <MainLayout>
    <div class="change-password">
      <h2>Ganti Password</h2>
      <form @submit.prevent="submit">
        <input v-model="currentPassword" type="password" placeholder="Password Saat Ini" required />
        <input v-model="newPassword" type="password" placeholder="Password Baru" required />
        <button type="submit">Ganti</button>
        <p v-if="message" class="message">{{ message }}</p>
      </form>
    </div>
  </MainLayout>
</template>

<script>
import MainLayout from '../layouts/MainLayout.vue';
import { changePassword } from '../services/authService';

export default {
  components: { MainLayout },
  data() {
    return {
      currentPassword: '',
      newPassword: '',
      message: ''
    };
  },
  methods: {
    async submit() {
      try {
        await changePassword(this.currentPassword, this.newPassword);
        this.message = 'Password berhasil diganti';
        this.currentPassword = '';
        this.newPassword = '';
      } catch (err) {
        this.message = 'Gagal mengganti password';
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.change-password {
  max-width: 400px;
  margin: auto;
  padding: 2em;
  border-radius: 12px;
  font-family: 'Share Tech Mono', monospace;
  background: rgba(20, 20, 30, 0.95);
  color: #f5f5f5;
  text-align: center;
  box-shadow: 0px 0px 25px #ff3d3d40;
}

.change-password h2 {
  font-size: 1.5rem;
  color: #ff3d3d;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.change-password form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.change-password input {
  padding: 0.9rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  color: #f5f5f5;
  background: #222;
  box-shadow: inset 0px 0px 5px #ff3d3d40;
}

.change-password input:focus {
  outline: none;
  box-shadow: 0px 0px 15px #ff3d3d80, inset 0px 0px 8px #ff3d3d40;
}

.change-password button {
  padding: 1rem;
  font-size: 1rem;
  font-weight: bold;
  color: #f5f5f5;
  background: linear-gradient(45deg, #ff3d3d, #ff0000);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.change-password button:hover {
  transform: translateY(-2px);
  box-shadow: 0px 0px 20px #ff3d3d80;
}

.message {
  font-size: 0.9rem;
  color: #ff7070;
  text-align: center;
}
</style>
