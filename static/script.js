// === Load Chart Data ===
function loadCharts() {
  fetch("/get_threats")
    .then(res => res.json())
    .then(data => {
      const barCtx = document.getElementById("threatChart").getContext("2d");
      const pieCtx = document.getElementById("pieChart").getContext("2d");

      const colors = ["#f43f5e", "#3b82f6", "#facc15", "#22c55e", "#a855f7", "#000000"];

      // Destroy old charts if needed
      if (window.barChart) window.barChart.destroy();
      if (window.pieChart) window.pieChart.destroy();

      // Bar Chart
      window.barChart = new Chart(barCtx, {
        type: "bar",
        data: {
          labels: data.types,
          datasets: [{
            label: "Threat Count",
            data: data.counts,
            backgroundColor: colors
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              ticks: { color: "#000000" }
            },
            y: {
              beginAtZero: true,
              ticks: { color: "#000000" }
            }
          },
          plugins: {
            title: {
              display: true,
              text: 'Threat Count by Type',
              color: '#000000',
              font: { size: 18 }
            },
            legend: {
              labels: {
                color: "#000000"
              }
            },
            tooltip: {
              bodyColor: "#000000",
              backgroundColor: "#ffffff",
              titleColor: "#000000"
            }
          }
        }
      });

      // Pie Chart
      window.pieChart = new Chart(pieCtx, {
        type: "pie",
        data: {
          labels: data.types,
          datasets: [{
            data: data.counts,
            backgroundColor: colors
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: {
                color: "#000000"
              }
            },
            tooltip: {
              bodyColor: "#000000",
              backgroundColor: "#ffffff",
              titleColor: "#000000"
            }
          }
        }
      });
    });
}


// === Render Threat Table ===
function renderThreatTable(threats) {
  const tbody = document.querySelector("#threatsTable tbody");
  tbody.innerHTML = "";

  threats.forEach(t => {
    const status = (t.status || "Pending").toLowerCase();
    const statusMap = {
      pending: "🟡",
      resolved: "🟢",
      escalated: "🔴",
      triaged: "🔵"
    };

    const emoji = statusMap[status] || "🟡";
    const statusClass = `status-pill status-${status}`;

    const row = `
      <tr>
        <td>${t.timestamp}</td>
        <td>${t.source}</td>
        <td>${t.event}</td>
        <td><span class="${statusClass}">${emoji} ${t.status}</span></td>
      </tr>`;
    tbody.innerHTML += row;
  });
}

// === Load AI Insight Table ===
function loadAIInsights() {
  fetch("/get_ai_insights")
    .then(res => res.json())
    .then(insights => {
      // Remove old AI insight card if it exists
      const oldCard = document.querySelector(".card.ai-insights");
      if (oldCard) oldCard.remove();

      const card = document.createElement("div");
      card.classList.add("card", "ai-insights");
      card.innerHTML = `
        <h3>🧠 AI Threat Insights</h3>
        <table>
          <thead>
            <tr><th>Event</th><th>Status</th><th>AI Insight</th></tr>
          </thead>
          <tbody>
            ${insights.map(row => {
              const cls = "status-pill status-" + (row.status || "pending").toLowerCase();
              return `
                <tr>
                  <td>${row.event}</td>
                  <td><span class="${cls}">${row.status}</span></td>
                  <td>${row.ai}</td>
                </tr>`;
            }).join("")}
          </tbody>
        </table>
      `;
      document.getElementById("dashboardGrid").appendChild(card);
    });
}

// === Load Threat Table with AI
function loadThreatTable() {
  fetch("/get_all_threats")
    .then(res => res.json())
    .then(renderThreatTable);

  loadAIInsights();
}

// === Init WebSocket Updates ===
function initSocket() {
  const socket = io();
  socket.on("new_threat", data => {
    alert(`⚠️ New Threat Detected: ${data.threat.event} from ${data.threat.source}`);
    loadCharts();
    loadThreatTable();
  });
}

// === Page Bootstrap ===
window.addEventListener("DOMContentLoaded", () => {
  loadCharts();
  loadThreatTable();
  initSocket();
});
