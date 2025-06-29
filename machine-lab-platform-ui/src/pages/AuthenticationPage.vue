<template>
  <MainLayout>
    <div class="admin-auth">
      <h2>Autentikasi Admin</h2>

      <div class="token-box">
        <p class="token-label">Admin Key (JWT)</p>
        <textarea readonly :value="adminToken" class="token-display"></textarea>
      </div>

      <button @click="rotateToken" class="rotate-btn">🔁 Rotate Key</button>

      <hr class="divider" />

      <h3 class="section-title">Reset Password</h3>
      <form @submit.prevent="resetPassword">
        <input v-model="currentPassword" type="password" placeholder="Password Saat Ini" required />
        <input v-model="newPassword" type="password" placeholder="Password Baru" required />
        <button type="submit" class="reset-btn">🔒 Reset Password</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </MainLayout>
</template>

<script>
import MainLayout from '../layouts/MainLayout.vue';
import { getAdminToken, rotateKey, changePassword } from '../services/authService';

export default {
  components: { MainLayout },
  data() {
    return {
      adminToken: '',
      message: '',
      currentPassword: '',
      newPassword: ''
    };
  },
  async mounted() {
    try {
      const token = await getAdminToken();
      this.adminToken = token;
    } catch (err) {
      this.message = 'Gagal mengambil admin key.';
    }
  },
  methods: {
    async rotateToken() {
      try {
        const newToken = await rotateKey();
        this.adminToken = newToken.data.admin_key;
        this.message = 'Admin key berhasil dirotasi.';
      } catch (err) {
        console.error(err);
        this.message = 'Gagal merotasi admin key.';
      }
    },
    async resetPassword() {
      try {
        await changePassword(this.currentPassword, this.newPassword);
        this.message = 'Password berhasil direset.';
        this.currentPassword = '';
        this.newPassword = '';
      } catch (err) {
        console.error(err);
        this.message = 'Gagal reset password.';
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.admin-auth {
  max-width: 600px;
  margin: auto;
  padding: 2em;
  border-radius: 12px;
  font-family: 'Share Tech Mono', monospace;
  background: rgba(20, 20, 30, 0.95);
  color: #f5f5f5;
  text-align: center;
  box-shadow: 0px 0px 25px #ff3d3d40;
}

.admin-auth h2 {
  font-size: 1.5rem;
  color: #ff3d3d;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.token-box {
  margin: 1rem 0;
  text-align: left;
  padding-right: 2rem;
}

.token-label {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #ccc;
}

.token-display {
  width: 100%;
  min-height: 100px;
  padding: 1rem;
  border-radius: 8px;
  background: #222;
  color: #f5f5f5;
  border: none;
  font-size: 0.9rem;
  resize: none;
  box-shadow: inset 0px 0px 5px #ff3d3d40;
}

.rotate-btn,
.reset-btn {
  padding: 1rem;
  font-size: 1rem;
  font-weight: bold;
  color: #f5f5f5;
  background: linear-gradient(45deg, #ff3d3d, #ff0000);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-transform: uppercase;
  margin-top: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
  width: 100%;
}

.rotate-btn:hover,
.reset-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0px 0px 20px #ff3d3d80;
}

form {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 0.9rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  color: #f5f5f5;
  background: #222;
  box-shadow: inset 0px 0px 5px #ff3d3d40;
}

input:focus {
  outline: none;
  box-shadow: 0px 0px 15px #ff3d3d80, inset 0px 0px 8px #ff3d3d40;
}

.section-title {
  margin-top: 2rem;
  font-size: 1.2rem;
  color: #ff7070;
}

.divider {
  border: none;
  border-top: 1px solid #444;
  margin: 2rem 0;
}

.message {
  font-size: 0.9rem;
  color: #ff7070;
  text-align: center;
  margin-top: 1rem;
}
</style>
