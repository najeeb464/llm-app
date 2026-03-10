async function loadStats() {
    const res = await fetch("/analytics");
    const data = await res.json();

    document.getElementById("totalTraces").textContent = data.total;
    document.getElementById("avgResponse").textContent = data.avg_response_time + "s";

    const breakdownEl = document.getElementById("categoryBreakdown");
    breakdownEl.innerHTML = "";

    data.categories.forEach(cat => {
        const div = document.createElement("div");
        div.className = "category-item";
        div.innerHTML = `
            <strong>${cat.name}</strong>: ${cat.count} (${cat.percentage}%)
        `;
        breakdownEl.appendChild(div);
    });
}

async function loadTraces(category = "") {
    const url = category ? `/traces?category=${category}` : "/traces";
    const res = await fetch(url);
    const traces = await res.json();

    const tbody = document.getElementById("traceTableBody");
    tbody.innerHTML = "";

    traces.forEach(trace => {
        const row = document.createElement("tr");
        row.className = "trace-row";

        row.innerHTML = `
            <td>${trace.timestamp}</td>
            <td>${truncate(trace.user_message)}</td>
            <td>${truncate(trace.bot_response)}</td>
            <td><span class="category-badge category-${trace.category}">${trace.category}</span></td>
            <td>${trace.response_time}s</td>
        `;

        row.addEventListener("click", () => toggleDetails(row, trace));
        tbody.appendChild(row);
    });
}

function truncate(text, max = 60) {
    return text.length > max ? text.slice(0, max) + "…" : text;
}

function toggleDetails(row, trace) {
    const existing = row.nextSibling;
    if (existing && existing.classList.contains("trace-details")) {
        existing.remove();
        return;
    }

    const details = document.createElement("tr");
    details.className = "trace-details";
    details.innerHTML = `
        <td colspan="5">
            <strong>User:</strong> ${trace.user_message}<br><br>
            <strong>Bot:</strong> ${trace.bot_response}
        </td>
    `;

    row.after(details);
}

document.getElementById("categoryFilter").addEventListener("change", (e) => {
    loadTraces(e.target.value);
});

loadStats();
loadTraces();
