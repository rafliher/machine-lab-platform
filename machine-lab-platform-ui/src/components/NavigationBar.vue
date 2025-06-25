<template>
  <nav class="navbar">
    <div class="brand">CyberBox</div>
    <div class="links">
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/hosts">Hosts</router-link>
      <router-link to="/changepassword">Ganti Password</router-link>
      <button @click="logout">Logout</button>
    </div>
  </nav>
</template>

<script>
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
export default {
  name: 'NavigationBar',
  setup() {
    const store = useStore();
    const router = useRouter();
    const logout = () => {
      store.dispatch('auth/logout');
      router.push('/');
    };
    return { logout };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(15, 15, 20, 0.95);
  padding: 1em 2em;
  font-family: 'Share Tech Mono', monospace;
  color: #f5f5f5;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0px 0px 20px #ff3d3d40;
  border-radius: 0 0 12px 12px;
}

.brand {
  font-size: 1.5em;
  font-weight: bold;
  color: #ff3d3d;
  text-shadow: 0px 0px 5px #ff3d3d;
}

.links {
  display: flex;
  align-items: center;
  gap: 1em;
}

.links a {
  text-decoration: none;
  color: #f5f5f5;
  padding: 0.5em 1em;
  border-radius: 8px;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
  transition: all 0.2s;
}

.links a:hover {
  background: #ff3d3d;
  color: #111;
  text-shadow: none;
}

.links a.router-link-active {
  background-color: #ff3d3d;
  color: #111;
}

.links button {
  padding: 0.5em 1em;
  font-size: 0.9rem;
  font-weight: bold;
  color: #f5f5f5;
  background-color: #ff3d3d;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.links button:hover {
  background-color: #ff0000;
  transform: translateY(-2px);
  box-shadow: 0px 0px 15px #ff3d3d80;
}
</style>
