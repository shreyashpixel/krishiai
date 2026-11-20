/**
 * KrishiAI - Chart.js Telemetry Visualizer
 * Includes real-time sliding window updating and offline HTML5 canvas rendering fallback.
 */

let telemetryChartInstance = null;
let npkChartInstance = null;
let yieldChartInstance = null;

const ChartTheme = {
  getColors() {
    const isDark = document.body.classList.contains("dark-mode");
    return {
      textColor: isDark ? "#e2e8f0" : "#2d3748",
      gridColor: isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.06)",
      moistureColor: "#2563eb",
      tempColor: "#e11d48",
      humidityColor: "#059669",
      npkActual: "#16a34a",
      npkTarget: isDark ? "rgba(255, 255, 255, 0.3)" : "rgba(0, 0, 0, 0.2)"
    };
  }
};

/**
 * Initializes the main dashboard telemetry time-series chart.
 */
function initTelemetryChart(historyData) {
  const ctx = document.getElementById("telemetryChart");
  if (!ctx) return;

  // Fallback if Chart.js is not loaded (offline CDN failure)
  if (typeof Chart === "undefined") {
    renderCanvasFallback(ctx, historyData);
    return;
  }

  const theme = ChartTheme.getColors();
  const labels = historyData.map(d => {
    const parts = (d.timestamp || "").split(" ");
    return parts[1] || parts[0] || "";
  });

  const moistureData = historyData.map(d => d.soil_moisture);
  const tempData = historyData.map(d => d.temperature);
  const humData = historyData.map(d => d.humidity);

  if (telemetryChartInstance) {
    telemetryChartInstance.destroy();
  }

  telemetryChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Soil Moisture (%)",
          data: moistureData,
          borderColor: theme.moistureColor,
          backgroundColor: "rgba(37, 99, 235, 0.1)",
          fill: true,
          tension: 0.35,
          yAxisID: "yMoisture",
          borderWidth: 2.5,
          pointRadius: 2.5
        },
        {
          label: "Temperature (°C)",
          data: tempData,
          borderColor: theme.tempColor,
          backgroundColor: "transparent",
          tension: 0.35,
          yAxisID: "yTemp",
          borderWidth: 2,
          pointRadius: 2
        },
        {
          label: "Humidity (%)",
          data: humData,
          borderColor: theme.humidityColor,
          backgroundColor: "transparent",
          tension: 0.35,
          yAxisID: "yMoisture",
          borderWidth: 1.5,
          borderDash: [4, 4],
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: "index",
        intersect: false
      },
      plugins: {
        legend: {
          position: "top",
          labels: { color: theme.textColor, font: { family: "Inter, sans-serif", size: 11 } }
        },
        tooltip: {
          backgroundColor: "rgba(15, 23, 42, 0.9)",
          titleFont: { size: 12 },
          bodyFont: { size: 11 }
        }
      },
      scales: {
        x: {
          grid: { color: theme.gridColor },
          ticks: { color: theme.textColor, maxTicksLimit: 8, font: { size: 10 } }
        },
        yMoisture: {
          type: "linear",
          position: "left",
          min: 10,
          max: 100,
          grid: { color: theme.gridColor },
          ticks: { color: theme.textColor, font: { size: 10 }, callback: v => `${v}%` },
          title: { display: true, text: "Moisture & Humidity (%)", color: theme.textColor, font: { size: 10 } }
        },
        yTemp: {
          type: "linear",
          position: "right",
          min: 10,
          max: 50,
          grid: { drawOnChartArea: false },
          ticks: { color: theme.textColor, font: { size: 10 }, callback: v => `${v}°C` },
          title: { display: true, text: "Temperature (°C)", color: theme.textColor, font: { size: 10 } }
        }
      }
    }
  });
}

/**
 * Pushes a new reading into the live chart sliding window.
 */
function updateLiveChartReading(reading) {
  if (!telemetryChartInstance) return;

  const labels = telemetryChartInstance.data.labels;
  const timeLabel = (reading.timestamp || "").split(" ")[1] || "Now";

  labels.push(timeLabel);
  telemetryChartInstance.data.datasets[0].data.push(reading.soil_moisture);
  telemetryChartInstance.data.datasets[1].data.push(reading.temperature);
  telemetryChartInstance.data.datasets[2].data.push(reading.humidity);

  // Keep last 25 points
  if (labels.length > 25) {
    labels.shift();
    telemetryChartInstance.data.datasets[0].data.shift();
    telemetryChartInstance.data.datasets[1].data.shift();
    telemetryChartInstance.data.datasets[2].data.shift();
  }

  telemetryChartInstance.update("none"); // Update without expensive animation hitch
}

/**
 * Initializes soil N-P-K nutrient bar chart.
 */
function initNpkChart(n, p, k) {
  const ctx = document.getElementById("npkChart");
  if (!ctx || typeof Chart === "undefined") return;

  const theme = ChartTheme.getColors();

  if (npkChartInstance) {
    npkChartInstance.destroy();
  }

  npkChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
      datasets: [
        {
          label: "Current Field Value (kg/ha)",
          data: [n, p, k],
          backgroundColor: ["#16a34a", "#eab308", "#8b5cf6"],
          borderRadius: 6
        },
        {
          label: "Optimal Target (kg/ha)",
          data: [75, 50, 55],
          backgroundColor: theme.npkTarget,
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: { color: theme.textColor, font: { size: 11 } }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: theme.textColor, font: { size: 11 } }
        },
        y: {
          grid: { color: theme.gridColor },
          ticks: { color: theme.textColor, font: { size: 10 } },
          min: 0,
          max: 120
        }
      }
    }
  });
}

/**
 * Renders Yield vs Cost vs Net Profit chart in the Yield Predictor tab.
 */
function renderYieldEconomicChart(grossRevenue, totalCost, netProfit) {
  const ctx = document.getElementById("yieldEconomicsChart");
  if (!ctx || typeof Chart === "undefined") return;

  const theme = ChartTheme.getColors();

  if (yieldChartInstance) {
    yieldChartInstance.destroy();
  }

  yieldChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Cultivation Cost", "Gross Revenue", "Net Profit"],
      datasets: [
        {
          label: "Amount (₹)",
          data: [totalCost, grossRevenue, netProfit],
          backgroundColor: [
            "#ef4444", // Cost: red
            "#3b82f6", // Revenue: blue
            "#10b981"  // Net Profit: green
          ],
          borderRadius: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: context => ` ₹ ${context.parsed.y.toLocaleString("en-IN")}`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: theme.textColor, font: { weight: "bold" } }
        },
        y: {
          grid: { color: theme.gridColor },
          ticks: {
            color: theme.textColor,
            callback: v => `₹${(v / 1000).toFixed(0)}k`
          }
        }
      }
    }
  });
}

/**
 * Offline HTML5 Canvas Fallback if Chart.js CDN is blocked.
 */
function renderCanvasFallback(canvas, data) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width = canvas.parentElement.clientWidth || 500;
  const h = canvas.height = 240;

  ctx.fillStyle = "#f8fafc";
  ctx.fillRect(0, 0, w, h);

  ctx.strokeStyle = "#cbd5e1";
  ctx.strokeRect(0, 0, w, h);

  ctx.fillStyle = "#1e293b";
  ctx.font = "12px sans-serif";
  ctx.fillText("Offline Telemetry Graph (Canvas Fallback)", 15, 25);

  if (!data || data.length === 0) return;

  // Plot Moisture line
  ctx.beginPath();
  ctx.strokeStyle = "#2563eb";
  ctx.lineWidth = 2;
  const step = (w - 40) / Math.max(1, data.length - 1);

  data.forEach((d, i) => {
    const x = 20 + i * step;
    const y = h - 30 - ((d.soil_moisture / 100) * (h - 60));
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  ctx.fillStyle = "#2563eb";
  ctx.fillText(`Soil Moisture: ${data[data.length - 1].soil_moisture}%`, 20, h - 10);
}

// Refresh chart styles on theme toggle
window.addEventListener("themeChanged", () => {
  if (telemetryChartInstance) telemetryChartInstance.options.scales.x.ticks.color = ChartTheme.getColors().textColor;
  if (telemetryChartInstance) telemetryChartInstance.update();
  if (npkChartInstance) npkChartInstance.update();
});
