<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}
</style>