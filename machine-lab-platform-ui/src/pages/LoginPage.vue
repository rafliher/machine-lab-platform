<template>
  <div class="login-page">
    <div class="login-container">
      <h2 class="title">Welcome to <span class="highlight">CyberBox</span></h2>
      <form class="login-form" @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="Enter your username" required />
        <input v-model="password" type="password" placeholder="Enter your password" required />
        <button type="submit">Access Portal</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import Cookies from 'vue-cookies';
import { login } from '../services/authService';
export default {
  name: 'LoginPage',
  setup() {
    const username = ref('');
    const password = ref('');
    const error = ref('');
    const router = useRouter();
    const store = useStore();
    const handleLogin = async () => {
      try {
        const response = await login(username.value, password.value);
        Cookies.set("token", response.data.admin_key);
        await store.dispatch("auth/setUser", response.data.user);
        router.push("/dashboard");
      } catch {
        error.value = "Invalid username or password";
      }
    };
    return { username, password, error, handleLogin };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.login-page {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Share Tech Mono', monospace;
  position: relative;
  overflow: hidden;
  background: #0d0d0d;
}

.login-page::before {
  content: '';
  position: absolute;
  top: 0%; left: 0%; 
  width: 100%; height: 100%;
  background:
    linear-gradient(#ff3d3d10 1px, transparent 1px),
    linear-gradient(90deg, #ff3d3d10 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 30s linear infinite;
  z-index: 0;
}

@keyframes gridMove {
  from {
    background-position: 0 0, 0 0;
  }
  to {
    background-position: 40px 40px, 40px 40px;
  }
}


@keyframes drift {
  from { transform: translate(0, 0); }
  to { transform: translate(100px, 100px); }
}

.login-container {
  padding: 2.5rem;
  border-radius: 12px;
  max-width: 420px;
  width: 100%;
  text-align: center;
  background: rgba(20, 20, 30, 0.95);
  box-shadow: 0px 0px 25px #ff3d3d50, 0px 0px 10px #ff3d3d30;
  position: relative;
  z-index: 1;
}

.title {
  font-size: 1.9rem;
  color: #f0f0f0;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.highlight {
  color: #ff3d3d;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.login-form input {
  padding: 1rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  color: #f5f5f5;
  background: #222;
  box-shadow: inset 0px 0px 5px #ff3d3d50;
}

.login-form input:focus {
  outline: none;
  box-shadow: 0px 0px 15px #ff3d3d80, inset 0px 0px 8px #ff3d3d40;
}

.login-form button {
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

.login-form button:hover {
  transform: translateY(-3px);
  box-shadow: 0px 0px 20px #ff3d3d80;
}

.error {
  color: #ff7070;
  font-size: 0.9rem;
}
</style>

