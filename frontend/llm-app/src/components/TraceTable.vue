<template>
    <table class="table">
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>User Message</th>
          <th>Bot Response</th>
          <th>Category</th>
          <th>Response Time</th>
        </tr>
      </thead>
      <tbody>
        {{ traces }}
        
  
        <tr v-for="trace in traces" :key="trace.id" @click="toggle(trace.id)" class="row">
            <td>{{ trace.timestamp }}</td>
            <td>{{ truncate(trace.user_message) }}</td>
            <td>{{ truncate(trace.bot_response) }}</td>
            <td>
              <span class="badge" :class="'badge-' + trace.category.replace(' ', '-')">
                {{ trace.category }}
              </span>
            </td>
            <td>{{ trace.response_time }}s</td>
          </tr>
          <!-- <tr v-if="openId === trace.id" class="details">
            <td colspan="5">
              <strong>User:</strong> {{ trace.user_message }}<br /><br />
              <strong>Bot:</strong> {{ trace.bot_response }}
            </td>
          </tr>  -->
      </tbody>
    </table>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  defineProps({
    traces: {
      type: Array,
      required: true
    }
  });
  
  const openId = ref(null);
  
  const toggle = (id) => {
    openId.value = openId.value === id ? null : id;
  };
  
  const truncate = (text, max = 60) =>
    text.length > max ? text.slice(0, max) + "…" : text;
  </script>
  
  <style scoped>
  .table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }
  
  th,
  td {
    padding: 8px 6px;
    border-bottom: 1px solid rgba(30, 41, 59, 0.9);
  }
  
  .row {
    cursor: pointer;
  }
  
  .row:hover {
    background: rgba(15, 23, 42, 0.8);
  }
  
  .details td {
    background: rgba(15, 23, 42, 0.95);
  }
  
  .badge {
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.75rem;
    color: #0f172a;
    font-weight: 600;
  }
  
  .badge-Billing {
    background: #38bdf8;
  }
  .badge-Refund {
    background: #f97373;
  }
  .badge-Account-Access {
    background: #22c55e;
  }
  .badge-Cancellation {
    background: #f97316;
  }
  .badge-General-Inquiry {
    background: #a855f7;
  }
  </style>
  