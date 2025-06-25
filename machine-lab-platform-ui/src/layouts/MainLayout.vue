<template>
  <div>
    <Navbar />
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script>
import Navbar from '../components/NavigationBar.vue';
export default {
  components: { Navbar }
};
</script>

<style>
.main-content {
  padding: 2em;
}
</style>