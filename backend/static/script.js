
const messagesEl = document.getElementById("chatMessages");
const inputEl = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendButton");

document.getElementById("welcomeTime").textContent = formatTime(new Date());

sendBtn.addEventListener("click", handleSend);
inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

async function handleSend() {
    const text = inputEl.value.trim();
    if (!text) return;

    setInputEnabled(false);
    inputEl.value = "";

    appendMessage("user", text);

    const typingEl = showTypingIndicator();

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        const data = await res.json();

        typingEl.remove();
        appendMessage("bot", data.response);
    } catch (err) {
        typingEl.remove();
        appendMessage(
            "bot",
            "⚠️ Sorry, something went wrong. Please try again in a moment."
        );
        console.error("Chat error:", err);
    } finally {
        setInputEnabled(true);
        inputEl.focus();
    }
}


function appendMessage(role, text) {
    const isBot = role === "bot";
    const wrapper = document.createElement("div");
    wrapper.className = `message message--${role}`;

    const avatarSvg = isBot
        ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/></svg>`
        : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/></svg>`;

    wrapper.innerHTML = `
        <div class="message__avatar">${avatarSvg}</div>
        <div class="message__content">
            <p>${escapeHtml(text)}</p>
            <span class="message__time">${formatTime(new Date())}</span>
        </div>
    `;

    messagesEl.appendChild(wrapper);
    scrollToBottom();
}

function showTypingIndicator() {
    const el = document.createElement("div");
    el.className = "typing-indicator";
    el.innerHTML = `
        <div class="message__avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="currentColor"/></svg>
        </div>
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
    `;
    messagesEl.appendChild(el);
    scrollToBottom();
    return el;
}

function setInputEnabled(enabled) {
    inputEl.disabled = !enabled;
    sendBtn.disabled = !enabled;
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        messagesEl.scrollTop = messagesEl.scrollHeight;
    });
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}
