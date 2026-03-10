<template>
    <section class="stats">
      <div class="card">
        <h3>Total Traces</h3>
        <p class="value">{{ analytics.total }}</p>
      </div>
      <div class="card">
        <h3>Average Response Time</h3>
        <p class="value">{{ analytics.avg_response_time }}s</p>
      </div>
      <div class="card large">
        <h3>Category Breakdown</h3>
        <ul>
          <li v-for="cat in analytics.categories" :key="cat.name">
            <span>{{ cat.name }}</span>
            <span>{{ cat.count }} ({{ cat.percentage }}%)</span>
          </li>
        </ul>
      </div>
    </section>
  </template>
  
  <script setup>
  defineProps({
    analytics: {
      type: Object,
      required: true
    }
  });
  </script>
  
  <style scoped>
  .stats {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }
  
  .card {
    flex: 1;
    min-width: 220px;
    background: rgba(15, 23, 42, 0.9);
    border-radius: 16px;
    padding: 14px 16px;
    border: 1px solid rgba(148, 163, 184, 0.2);
  }
  
  .card.large {
    flex: 2;
  }
  
  h3 {
    font-size: 0.9rem;
    color: #cbd5f5;
    margin-bottom: 6px;
  }
  
  .value {
    font-size: 1.4rem;
    font-weight: 600;
  }
  
  ul {
    list-style: none;
    margin-top: 6px;
  }
  
  li {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #e2e8f0;
    padding: 2px 0;
  }
  </style>
  