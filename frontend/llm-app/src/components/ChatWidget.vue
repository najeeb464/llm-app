<template>
  <div>
    <div class="chat-widget" v-if="visible">
      <div class="chat-container">
        <header class="chat-header">
          <div class="chat-header__brand">
            <div class="chat-header__icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <div>
              <h1 class="chat-header__title">BillEase Support</h1>
              <p class="chat-header__status">
                <span class="status-dot"></span>
                Online — Typically replies instantly
              </p>
            </div>
          </div>
          <button class="close-btn" @click="visible = false">×</button>
        </header>
  
        <main class="chat-messages" ref="messagesEl">
          <div class="message message--bot">
            <div class="message__avatar">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <div class="message__content">
              <p>👋 Hi there! I'm your BillEase support assistant. How can I help you today?</p>
              <span class="message__time">{{ formatTime(new Date()) }}</span>
            </div>
          </div>
  
          <div
            v-for="m in messages"
            :key="m.id"
            class="message"
            :class="m.role === 'bot' ? 'message--bot' : 'message--user'"
          >
            <div class="message__avatar">
              <svg
                v-if="m.role === 'bot'"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                  fill="currentColor"
                />
              </svg>
              <svg
                v-else
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
              >
                <path
                  d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <div class="message__content">
              <p>{{ m.text }}</p>
              <span class="message__time">{{ formatTime(m.time) }}</span>
            </div>
          </div>
  
          <div v-if="loading" class="typing-indicator">
            <div class="message__avatar">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                  fill="currentColor"
                />
              </svg>
            </div>
            <div class="typing-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </main>
  
        <footer class="chat-input">
          <div class="chat-input__wrapper">
            <input
              v-model="input"
              @keydown.enter.prevent="handleSend"
              type="text"
              class="chat-input__field"
              placeholder="Type your message…"
            />
            <button
              class="chat-input__send"
              :disabled="!input.trim() || loading"
              @click="handleSend"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path
                  d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"
                  fill="currentColor"
                />
              </svg>
            </button>
          </div>
          <p class="chat-input__hint">
            Each message is independent — no conversation history is retained.
          </p>
        </footer>
      </div>
  
      <!-- <button v-else class="launcher" @click="visible = true">
      </button> -->
    </div>
    <button class="launcher" v-show="!visible" @click="visible = true">
      💬
  </button>
</div>
  </template>
  
  <script setup>
  import { ref, nextTick } from "vue";
  import { sendChat } from "../api/client";
  
  const visible = ref(true);
  const input = ref("");
  const messages = ref([]);
  const loading = ref(false);
  const messagesEl = ref(null);
  let idCounter = 0;
  
  const formatTime = (date) =>
    new Date(date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  
  const scrollToBottom = async () => {
    await nextTick();
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
    }
  };
  
  const refreshData= async () =>{
    // await nextTick();
    await fetchAnalytics();
    await fetchTraces();
  }
  const handleSend = async () => {
    const text = input.value.trim();
    if (!text || loading.value) return;
  
    messages.value.push({
      id: ++idCounter,
      role: "user",
      text,
      time: new Date()
    });
    input.value = "";
    await scrollToBottom();
  
    loading.value = true;
    try {
      const res = await sendChat(text);
      messages.value.push({
        id: ++idCounter,
        role: "bot",
        text: res.response,
        time: new Date()
      });
    } catch (e) {
      messages.value.push({
        id: ++idCounter,
        role: "bot",
        text: "⚠️ Sorry, something went wrong. Please try again in a moment.",
        time: new Date()
      });
    } finally {
      loading.value = false;
      await scrollToBottom();
    }
  };
  </script>
  
  <style scoped>
  .chat-widget {
    position: fixed;
    bottom: 20px;
    left: 20px;
    z-index: 9999;
  }
  
  .launcher {
    width: 52px;
    height: 52px;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
    font-size: 1.4rem;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.7);
  }
  
  .chat-container {
    width: 360px;
    height: 520px;
    background: rgba(17, 24, 39, 0.85);
    border-radius: 20px;
    border: 1px solid rgba(148, 163, 184, 0.3);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  /* reuse your styles, simplified */
  .chat-header {
    padding: 12px 14px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .chat-header__brand {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .chat-header__icon {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .chat-header__title {
    font-size: 0.95rem;
    font-weight: 600;
  }
  
  .chat-header__status {
    font-size: 0.7rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
  }
  
  .close-btn {
    background: none;
    border: none;
    color: #94a3b8;
    font-size: 1.2rem;
    cursor: pointer;
  }
  
  .chat-messages {
    flex: 1;
    padding: 10px 12px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .message {
    display: flex;
    gap: 8px;
    max-width: 90%;
  }
  
  .message--bot {
    align-self: flex-start;
  }
  
  .message--user {
    align-self: flex-end;
    flex-direction: row-reverse;
  }
  
  .message__avatar {
    width: 26px;
    height: 26px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(99, 102, 241, 0.2);
    color: #818cf8;
  }
  
  .message__content {
    padding: 8px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    line-height: 1.4;
  }
  
  .message--bot .message__content {
    background: rgba(30, 41, 59, 0.9);
  }
  
  .message--user .message__content {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
  }
  
  .message__time {
    display: block;
    font-size: 0.65rem;
    color: #94a3b8;
    margin-top: 4px;
  }
  
  .typing-indicator {
    display: flex;
    gap: 8px;
    align-self: flex-start;
  }
  
  .typing-dots {
    display: flex;
    gap: 4px;
    padding: 8px 10px;
    background: rgba(30, 41, 59, 0.9);
    border-radius: 12px;
  }
  
  .typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background: #94a3b8;
    animation: bounce 1.4s infinite ease-in-out;
  }
  
  .typing-dots span:nth-child(2) {
    animation-delay: 0.15s;
  }
  .typing-dots span:nth-child(3) {
    animation-delay: 0.3s;
  }
  
  @keyframes bounce {
    0%, 60%, 100% {
      transform: translateY(0);
      opacity: 0.4;
    }
    30% {
      transform: translateY(-5px);
      opacity: 1;
    }
  }
  
  .chat-input {
    padding: 10px 12px;
    border-top: 1px solid rgba(148, 163, 184, 0.2);
  }
  
  .chat-input__wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(15, 23, 42, 0.9);
    border-radius: 999px;
    padding: 4px 6px 4px 12px;
  }
  
  .chat-input__field {
    flex: 1;
    background: none;
    border: none;
    outline: none;
    color: #e2e8f0;
    font-size: 0.8rem;
  }
  
  .chat-input__send {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    cursor: pointer;
  }
  
  .chat-input__send:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  
  .chat-input__hint {
    margin-top: 4px;
    font-size: 0.65rem;
    color: #64748b;
    text-align: center;
  }
  </style>
  