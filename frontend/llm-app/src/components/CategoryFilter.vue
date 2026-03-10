<template>
    <select v-model="model" class="filter">
      <option value="">All Categories</option>
      <option>Billing</option>
      <option>Refund</option>
      <option>Account Access</option>
      <option>Cancellation</option>
      <option>General Inquiry</option>
    </select>
  </template>
  
  <script setup>
  const model = defineModel();
  </script>
  
  <style scoped>
  .filter {
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.6);
    background: rgba(15, 23, 42, 0.9);
    color: #e2e8f0;
    font-size: 0.85rem;
  }
  </style>
  