<template>
    <div class="dashboard">
      <header class="dashboard-header">
        <h1>BillEase Observability Dashboard</h1>
        <p>See what customers are asking and how the chatbot is performing.</p>
      </header>
  
      <AnalyticsCards :analytics="analytics" />
  
      <section class="trace-section">
        <div class="trace-header">
          <h2>Traces</h2>
          <CategoryFilter v-model="selectedCategory" />
        </div>
        <TraceTable :traces="traces" />
      </section>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref, watch } from "vue";
  import { fetchAnalytics, fetchTraces } from "../api/client";
  import AnalyticsCards from "../components/AnalyticsCards.vue";
  import TraceTable from "../components/TraceTable.vue";
  import CategoryFilter from "../components/CategoryFilter.vue";
  
  const analytics = ref({ total: 0, avg_response_time: 0, categories: [] });
  const traces = ref([]);
  const selectedCategory = ref("");
  
  const loadAnalytics = async () => {
    analytics.value = await fetchAnalytics();
  };
  
  const loadTraces = async () => {
    traces.value = await fetchTraces(selectedCategory.value || "");
  };
  
  onMounted(async () => {
    await loadAnalytics();
    await loadTraces();
  });
  
  watch(selectedCategory, loadTraces);
  </script>
  
  <style scoped>
  .dashboard {
    max-width: 1100px;
    margin: 0 auto;
    padding: 24px 16px 80px;
  }
  
  .dashboard-header h1 {
    font-size: 1.6rem;
    margin-bottom: 4px;
  }
  
  .dashboard-header p {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-bottom: 20px;
  }
  
  .trace-section {
    margin-top: 24px;
    background: rgba(15, 23, 42, 0.9);
    border-radius: 16px;
    padding: 16px 18px;
    border: 1px solid rgba(148, 163, 184, 0.2);
  }
  
  .trace-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  </style>
  