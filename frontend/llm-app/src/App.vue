<template>
  <div class="app-root">
    <router-view />
    <!-- <Dashboard /> -->
    <ChatWidget />
  </div>
</template>

<script setup>
import ChatWidget from "./components/ChatWidget.vue";
</script>

<style>
.app-root {
  min-height: 100vh;
  background: #0a0e1a;
  color: #f1f5f9;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
</style>