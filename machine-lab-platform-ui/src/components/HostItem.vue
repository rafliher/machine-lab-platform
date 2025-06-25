<template>
  <div class="host-item">
    <h3>{{ host.name }}</h3>
    <p>IP: {{ host.ip }}</p>
    <p>Status: <span :class="host.status">{{ host.status }}</span></p>
  </div>
</template>

<script>
export default {
  props: ['host']
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

.host-item {
  background: rgba(20, 20, 30, 0.95);
  padding: 1.25em;
  border-radius: 10px;
  font-family: 'Share Tech Mono', monospace;
  color: #f5f5f5;
  box-shadow: 0px 0px 15px #ff3d3d40, 0px 0px 5px #ff3d3d20;
  border: 1px solid #ff3d3d30;
  transition: transform 0.2s, box-shadow 0.2s;
}

.host-item:hover {
  transform: translateY(-3px);
  box-shadow: 0px 0px 25px #ff3d3d80;
}

.host-item h3 {
  font-size: 1.25rem;
  color: #ff3d3d;
  text-transform: uppercase;
}

.host-item p {
  font-size: 0.95rem;
  margin: 0.25em 0;
}

.host-item .running {
  color: #00ff00;
  text-shadow: 0px 0px 5px #00ff00;
}

.host-item .stopped {
  color: #ff3d3d;
  text-shadow: 0px 0px 5px #ff3d3d;
}
</style>

