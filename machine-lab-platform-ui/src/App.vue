<template>
  <router-view />
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #0d0d0d;
  color: #2c3e50;
}
body::before {
  content: '';
  position: absolute;
  top: 0%; left: 0%; 
  width: 100%; height: 100%;
  background:
    linear-gradient(#ff3d3d10 1px, transparent 1px),
    linear-gradient(90deg, #ff3d3d10 1px, transparent 1px);
  background-size: 40px 40px;
  animation: gridMove 30s linear infinite;
  z-index: -1;
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
a {
  text-decoration: none;
}
button {
  font-family: inherit;
}
</style>