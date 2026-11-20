/**
 * KrishiAI - Main Single Page Application Controller
 */

let currentSensorState = null;
let isDemoRunning = false;
let currentDemoIndex = 0;
let demoSteps = [];

document.addEventListener("DOMContentLoaded", async () => {
  initTheme();
  initLanguage();
  initNavigation();
  initTelemetry();
  initCropRecommender();
  initDiseaseScanner();
  initIrrigationPlanner();
  initWeatherAdvisory();
  initYieldCalculator();
  initFertilizerCalculator();
  initCropCalendar();
  initSustainabilityMeter();
  initChatbot();
  initDemoMode();
});

// --- Theme Management ---
function initTheme() {
  const savedTheme = localStorage.getItem("krishiai_theme") || "light";
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    document.getElementById("themeToggleBtn")?.classList.add("active");
  }

  document.getElementById("themeToggleBtn")?.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("krishiai_theme", isDark ? "dark" : "light");
    window.dispatchEvent(new Event("themeChanged"));
  });
}

// --- Language Management ---
function initLanguage() {
  const savedLang = localStorage.getItem("krishiai_lang") || "en";
  const langSelect = document.getElementById("langSelect");
  if (langSelect) {
    langSelect.value = savedLang;
    langSelect.addEventListener("change", (e) => {
      setLanguage(e.target.value);
    });
  }
  setLanguage(savedLang);
}

// --- Navigation / Tabs ---
function initNavigation() {
  const navLinks = document.querySelectorAll(".nav-tab-btn");
  navLinks.forEach(btn => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      switchTab(tabId);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".nav-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

  const targetBtn = document.querySelector(`.nav-tab-btn[data-tab="${tabId}"]`);
  const targetPane = document.getElementById(`tab-${tabId}`);

  if (targetBtn) targetBtn.classList.add("active");
  if (targetPane) targetPane.classList.add("active");

  // Trigger resize for charts if switching into dashboard or yield
  window.dispatchEvent(new Event("resize"));
}

// --- Telemetry & Live Stream ---
async function initTelemetry() {
  try {
    const history = await API.getSensorHistory(30);
    initTelemetryChart(history);
    if (history.length > 0) {
      updateSensorCards(history[history.length - 1]);
    }
  } catch (err) {
    console.warn("Could not fetch historical telemetry", err);
  }

  // Connect WebSocket / Fallback Streamer
  new TelemetryStreamer((reading) => {
    currentSensorState = reading;
    updateSensorCards(reading);
    updateLiveChartReading(reading);
  });

  // Simulator Event Buttons
  document.querySelectorAll(".btn-sim-action").forEach(btn => {
    btn.addEventListener("click", async () => {
      const eventType = btn.getAttribute("data-sim-event");
      showToast(`Simulation Event: Triggering ${eventType.toUpperCase()}...`, "info");
      try {
        const res = await API.triggerSimulator(eventType);
        updateSensorCards(res.current_readings);
        showToast(`Simulation mode switched to ${eventType}`, "success");
      } catch (err) {
        showToast("Error triggering simulation", "danger");
      }
    });
  });
}

function updateSensorCards(data) {
  if (!data) return;

  // Farm Health Score Gauge
  const healthEl = document.getElementById("valHealthScore");
  const healthFill = document.getElementById("healthScoreFill");
  if (healthEl) healthEl.textContent = data.health_score;
  if (healthFill) healthFill.style.width = `${data.health_score}%`;

  // Condition Alert Banner
  const alertBanner = document.getElementById("farmAlertBanner");
  if (alertBanner) {
    alertBanner.textContent = data.condition_alert || t("optimal_conditions");
    alertBanner.className = `alert-banner ${data.health_score < 60 ? "alert-danger" : (data.health_score < 80 ? "alert-warning" : "alert-success")}`;
  }

  // Metrics
  setCardValue("valMoisture", `${data.soil_moisture}%`);
  setCardValue("valTemp", `${data.temperature} °C`);
  setCardValue("valHumidity", `${data.humidity}%`);
  setCardValue("valPh", data.ph);
  setCardValue("valNpk", `${Math.round(data.nitrogen)} : ${Math.round(data.phosphorus)} : ${Math.round(data.potassium)}`);

  // Update NPK bar chart
  initNpkChart(data.nitrogen, data.phosphorus, data.potassium);
}

function setCardValue(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

// --- Crop Recommendation ---
function initCropRecommender() {
  const form = document.getElementById("cropRecForm");
  const quickFillBtn = document.getElementById("btnQuickFillSensors");

  if (quickFillBtn) {
    quickFillBtn.addEventListener("click", () => {
      if (!currentSensorState) {
        showToast("Waiting for live sensor data...", "warning");
        return;
      }
      document.getElementById("recN").value = Math.round(currentSensorState.nitrogen);
      document.getElementById("recP").value = Math.round(currentSensorState.phosphorus);
      document.getElementById("recK").value = Math.round(currentSensorState.potassium);
      document.getElementById("recPh").value = currentSensorState.ph;
      document.getElementById("recTemp").value = currentSensorState.temperature;
      document.getElementById("recHumidity").value = currentSensorState.humidity;
      document.getElementById("recRainfall").value = 110;
      showToast("Populated fields from live IoT sensor readings!", "success");
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        n: parseFloat(document.getElementById("recN").value),
        p: parseFloat(document.getElementById("recP").value),
        k: parseFloat(document.getElementById("recK").value),
        ph: parseFloat(document.getElementById("recPh").value),
        temperature: parseFloat(document.getElementById("recTemp").value),
        humidity: parseFloat(document.getElementById("recHumidity").value),
        rainfall: parseFloat(document.getElementById("recRainfall").value)
      };

      const btn = form.querySelector("button[type='submit']");
      btn.disabled = true;
      btn.textContent = "Analyzing Soil Profile...";

      try {
        const res = await API.recommendCrop(payload);
        renderCropResults(res.predictions);
        showToast("Crop recommendation model completed successfully!", "success");
      } catch (err) {
        showToast(err.message, "danger");
      } finally {
        btn.disabled = false;
        btn.textContent = t("btn_predict_crop");
      }
    });
  }
}

function renderCropResults(predictions) {
  const container = document.getElementById("cropRecResults");
  if (!container) return;

  if (!predictions || predictions.length === 0) {
    container.innerHTML = `<p class="empty-state">No matching crops found for this profile.</p>`;
    return;
  }

  container.innerHTML = predictions.map((c, i) => `
    <div class="crop-card ${i === 0 ? 'crop-card-top' : ''}">
      <div class="crop-card-header">
        <span class="crop-rank-badge">#${c.rank} Match</span>
        <h3 class="crop-name">${c.crop}</h3>
        <span class="crop-conf-tag">${c.confidence}% Confidence</span>
      </div>
      <div class="crop-progress-bar">
        <div class="crop-progress-fill" style="width: ${c.confidence}%"></div>
      </div>
      <div class="crop-meta-grid">
        <div class="crop-meta-item">
          <span class="meta-label">Season</span>
          <span class="meta-val">${c.season}</span>
        </div>
        <div class="crop-meta-item">
          <span class="meta-label">Water Need</span>
          <span class="meta-val">${c.water_requirement}</span>
        </div>
        <div class="crop-meta-item">
          <span class="meta-label">Ideal Soil</span>
          <span class="meta-val">${c.soil_type}</span>
        </div>
      </div>
    </div>
  `).join("");
}

// --- Plant Disease Scanner ---
function initDiseaseScanner() {
  const dropZone = document.getElementById("leafDropZone");
  const fileInput = document.getElementById("leafFileInput");

  if (dropZone && fileInput) {
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
      if (e.dataTransfer.files.length > 0) {
        handleDiseaseUpload(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener("change", (e) => {
      if (e.target.files.length > 0) {
        handleDiseaseUpload(e.target.files[0]);
      }
    });
  }

  // Sample leaf buttons
  document.querySelectorAll(".btn-sample-leaf").forEach(btn => {
    btn.addEventListener("click", async () => {
      const dType = btn.getAttribute("data-disease-type");
      showToast(`Generating and testing sample: ${dType}...`, "info");
      try {
        const res = await API.testSampleLeaf(dType);
        renderDiseaseDiagnosis(res);
        showToast("Diagnosis complete!", "success");
      } catch (err) {
        showToast("Sample analysis failed", "danger");
      }
    });
  });
}

async function handleDiseaseUpload(file) {
  showToast("Scanning leaf specimen for foliar pathogens...", "info");
  
  // Show local preview
  const previewImg = document.getElementById("leafPreviewImg");
  if (previewImg) {
    previewImg.src = URL.createObjectURL(file);
    previewImg.style.display = "block";
  }

  try {
    const res = await API.detectDisease(file);
    renderDiseaseDiagnosis(res);
    showToast("Pathology diagnosis complete!", "success");
  } catch (err) {
    showToast("Error scanning image: " + err.message, "danger");
  }
}

function renderDiseaseDiagnosis(data) {
  const container = document.getElementById("diseaseDiagnosisResult");
  if (!container) return;

  const isHealthy = data.detected_disease === "Healthy";
  const sevColor = isHealthy ? "#10b981" : (data.severity > 60 ? "#ef4444" : "#f59e0b");

  container.innerHTML = `
    <div class="diagnosis-card ${isHealthy ? 'diagnosis-healthy' : 'diagnosis-alert'}">
      <div class="diagnosis-header">
        <div>
          <span class="diagnosis-badge" style="background: ${sevColor}">${data.stage}</span>
          <h3 class="diagnosis-title">${data.title}</h3>
        </div>
        <div class="diagnosis-conf">
          <div class="conf-num">${data.confidence}%</div>
          <div class="conf-lbl">Confidence</div>
        </div>
      </div>
      
      <p class="diagnosis-desc">${data.description}</p>

      <div class="severity-meter-box">
        <div class="sev-lbl-row">
          <span>${t("severity_label")}</span>
          <span style="font-weight: bold; color: ${sevColor}">${data.severity}%</span>
        </div>
        <div class="sev-bar-bg">
          <div class="sev-bar-fill" style="width: ${data.severity}%; background: ${sevColor}"></div>
        </div>
      </div>

      <div class="remedy-grid">
        <div class="remedy-box organic-remedy">
          <h4>🍃 ${t("organic_remedy")}</h4>
          <p>${data.organic_treatment}</p>
        </div>
        <div class="remedy-box chemical-remedy">
          <h4>🧪 ${t("chemical_remedy")}</h4>
          <p>${data.chemical_treatment}</p>
        </div>
      </div>

      <div class="prevention-tip">
        <strong>🛡️ Prevention & Agronomic Care:</strong> ${data.prevention}
      </div>
    </div>
  `;
}

// --- Smart Irrigation ---
function initIrrigationPlanner() {
  const form = document.getElementById("irrigationForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        crop: document.getElementById("irrigCrop").value,
        moisture: parseFloat(document.getElementById("irrigMoisture").value || (currentSensorState?.soil_moisture || 40)),
        area_acres: parseFloat(document.getElementById("irrigArea").value || 3.5),
        rain_forecast_mm: parseFloat(document.getElementById("irrigRainForecast").value || 0.0)
      };

      try {
        const plan = await API.planIrrigation(payload);
        renderIrrigationPlan(plan);
        showToast("Irrigation budget calculated!", "success");
      } catch (err) {
        showToast(err.message, "danger");
      }
    });
  }
}

function renderIrrigationPlan(plan) {
  const container = document.getElementById("irrigationResults");
  if (!container) return;

  container.innerHTML = `
    <div class="irrigation-card">
      <div class="irrig-badge-row">
        <span class="badge ${plan.urgency === 'URGENT' ? 'badge-danger' : (plan.urgency === 'MODERATE' ? 'badge-warning' : 'badge-success')}">
          ${plan.urgency} Action
        </span>
        <span class="irrig-time-pill">⏰ ${plan.time_to_irrigate}</span>
      </div>

      <div class="irrig-stat-grid">
        <div class="irrig-stat-item highlight">
          <span class="irrig-stat-val">${plan.water_required_litres.toLocaleString()} L</span>
          <span class="irrig-stat-lbl">${t("water_needed")}</span>
        </div>
        <div class="irrig-stat-item">
          <span class="irrig-stat-val">${plan.drip_runtime_minutes} mins</span>
          <span class="irrig-stat-lbl">${t("drip_runtime")}</span>
        </div>
        <div class="irrig-stat-item success">
          <span class="irrig-stat-val">${plan.water_saved_litres.toLocaleString()} L</span>
          <span class="irrig-stat-lbl">${t("water_saved")}</span>
        </div>
      </div>

      <div class="irrig-rec-text">
        <p>${plan.recommendation}</p>
      </div>
    </div>
  `;
}

// --- Weather Advisory ---
async function initWeatherAdvisory() {
  const detectBtn = document.getElementById("btnDetectLocation");
  if (detectBtn) {
    detectBtn.addEventListener("click", () => {
      if (navigator.geolocation) {
        showToast("Acquiring GPS location...", "info");
        navigator.geolocation.getCurrentPosition(
          async (pos) => {
            const { latitude, longitude } = pos.coords;
            loadWeather(latitude, longitude);
          },
          (err) => {
            showToast("GPS denied. Loading default Pune agro-climate zone.", "warning");
            loadWeather();
          }
        );
      } else {
        loadWeather();
      }
    });
  }

  // Initial load
  loadWeather();
}

async function loadWeather(lat = null, lon = null) {
  try {
    const data = await API.getWeather(lat, lon);
    renderWeather(data);
  } catch (err) {
    console.warn("Could not load weather", err);
  }
}

function renderWeather(data) {
  const container = document.getElementById("weatherForecastCards");
  const advisoriesBox = document.getElementById("weatherAdvisoriesBox");
  if (!container) return;

  // Render 7-day cards
  container.innerHTML = (data.daily_forecast || []).map(d => `
    <div class="weather-day-card">
      <div class="w-day-name">${d.day}</div>
      <div class="w-icon">${getWeatherEmoji(d.icon)}</div>
      <div class="w-temps">
        <span class="w-temp-max">${d.temp_max}°</span>
        <span class="w-temp-min">${d.temp_min}°</span>
      </div>
      <div class="w-cond">${d.condition}</div>
      <div class="w-precip">🌧️ ${d.precipitation_mm} mm (${d.precipitation_prob}%)</div>
      <div class="w-wind">💨 ${d.wind_kmh} km/h</div>
    </div>
  `).join("");

  // Render advisories
  if (advisoriesBox) {
    advisoriesBox.innerHTML = (data.advisories || []).map(adv => `
      <div class="weather-adv-item adv-${adv.type}">
        <div class="adv-badge">${adv.badge}</div>
        <h4>${adv.title}</h4>
        <p>${adv.detail}</p>
      </div>
    `).join("");
  }
}

function getWeatherEmoji(icon) {
  const map = {
    "sun": "☀️",
    "sun-cloud": "🌤️",
    "cloud-sun": "⛅",
    "cloud": "☁️",
    "cloud-fog": "🌫️",
    "cloud-drizzle": "🌦️",
    "cloud-rain": "🌧️",
    "cloud-lightning": "⛈️"
  };
  return map[icon] || "⛅";
}

// --- Yield & Mandi Profit ---
function initYieldCalculator() {
  const form = document.getElementById("yieldForm");
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        crop: document.getElementById("yieldCrop").value,
        area_acres: parseFloat(document.getElementById("yieldArea").value || 3.5),
        season: document.getElementById("yieldSeason").value,
        soil_type: document.getElementById("yieldSoil").value,
        irrigation_type: document.getElementById("yieldIrrigation").value
      };

      try {
        const res = await API.predictYield(payload);
        renderYieldResults(res);
        renderYieldEconomicChart(res.gross_revenue, res.total_cost, res.net_profit);
        showToast("Yield & Mandi profit computed!", "success");
      } catch (err) {
        showToast(err.message, "danger");
      }
    });
  }
}

function renderYieldResults(data) {
  const container = document.getElementById("yieldResultsBox");
  if (!container) return;

  container.innerHTML = `
    <div class="yield-summary-card">
      <div class="yield-header">
        <h3>${data.crop} (${data.area_acres} Acres)</h3>
        <span class="roi-badge">ROI: ${data.roi_percent}%</span>
      </div>

      <div class="yield-stat-grid">
        <div class="yield-stat-item">
          <span class="stat-lbl">${t("expected_yield")}</span>
          <span class="stat-val">${data.total_expected_yield} ${data.unit}s</span>
          <span class="stat-sub">(${data.yield_per_acre} ${data.unit}/acre)</span>
        </div>
        <div class="yield-stat-item">
          <span class="stat-lbl">${t("total_cost")}</span>
          <span class="stat-val cost">₹${data.total_cost.toLocaleString()}</span>
          <span class="stat-sub">(₹${data.cost_per_acre.toLocaleString()}/acre)</span>
        </div>
        <div class="yield-stat-item">
          <span class="stat-lbl">${t("gross_revenue")}</span>
          <span class="stat-val rev">₹${data.gross_revenue.toLocaleString()}</span>
          <span class="stat-sub">(Mandi ₹${data.mandi_price_per_unit}/${data.unit})</span>
        </div>
        <div class="yield-stat-item highlight">
          <span class="stat-lbl">${t("net_profit")}</span>
          <span class="stat-val profit">₹${data.net_profit.toLocaleString()}</span>
          <span class="stat-sub">(₹${data.profit_per_acre.toLocaleString()}/acre)</span>
        </div>
      </div>

      <div class="yield-narrative">
        <p>${data.recommendation}</p>
      </div>
    </div>
  `;
}

// --- Fertilizer Calculator ---
function initFertilizerCalculator() {
  const form = document.getElementById("fertilizerForm");
  const quickFillBtn = document.getElementById("btnFertQuickFill");

  if (quickFillBtn) {
    quickFillBtn.addEventListener("click", () => {
      if (!currentSensorState) return;
      document.getElementById("fertN").value = Math.round(currentSensorState.nitrogen);
      document.getElementById("fertP").value = Math.round(currentSensorState.phosphorus);
      document.getElementById("fertK").value = Math.round(currentSensorState.potassium);
      showToast("Imported live soil test values!", "success");
    });
  }

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = {
        crop: document.getElementById("fertCrop").value,
        soil_n: parseFloat(document.getElementById("fertN").value),
        soil_p: parseFloat(document.getElementById("fertP").value),
        soil_k: parseFloat(document.getElementById("fertK").value),
        area_acres: parseFloat(document.getElementById("fertArea").value || 1.0)
      };

      try {
        const res = await API.calculateFertilizer(payload);
        renderFertilizerResults(res);
        showToast("Precision fertilizer protocol computed!", "success");
      } catch (err) {
        showToast(err.message, "danger");
      }
    });
  }
}

function renderFertilizerResults(data) {
  const container = document.getElementById("fertilizerResultsBox");
  if (!container) return;

  const comm = data.commercial_recommendations;
  const eco = data.eco_friendly_alternative;

  container.innerHTML = `
    <div class="fert-results-card">
      <div class="fert-bags-grid">
        <div class="fert-bag-item urea">
          <div class="bag-icon">🌾</div>
          <div class="bag-title">Urea (46% N)</div>
          <div class="bag-count">${comm.urea.bags_45kg} Bags (45kg)</div>
          <div class="bag-weight">${comm.urea.total_kg} kg total</div>
        </div>

        <div class="fert-bag-item dap">
          <div class="bag-icon">🌱</div>
          <div class="bag-title">DAP (18:46:0)</div>
          <div class="bag-count">${comm.dap.bags_50kg} Bags (50kg)</div>
          <div class="bag-weight">${comm.dap.total_kg} kg total</div>
        </div>

        <div class="fert-bag-item mop">
          <div class="bag-icon">🥔</div>
          <div class="bag-title">MOP Potash (60% K)</div>
          <div class="bag-count">${comm.mop.bags_50kg} Bags (50kg)</div>
          <div class="bag-weight">${comm.mop.total_kg} kg total</div>
        </div>
      </div>

      <div class="fert-split-box">
        <h4>📅 Split Fertigation / Application Schedule</h4>
        <div class="split-timeline">
          ${(data.split_application_schedule || []).map(s => `
            <div class="split-step">
              <strong>${s.stage}:</strong> ${s.application}
            </div>
          `).join("")}
        </div>
      </div>

      <div class="fert-eco-box">
        <h4>🌿 ${eco.title}</h4>
        <p>• <b>Compost / FYM:</b> ${eco.fym_vermicompost}</p>
        <p>• <b>Neem Seed Cake:</b> ${eco.neem_cake}</p>
        <p>• <b>Bio-fertilizers:</b></p>
        <ul>${eco.biofertilizers.map(b => `<li>${b}</li>`).join("")}</ul>
      </div>
    </div>
  `;
}

// --- Crop Calendar ---
async function initCropCalendar() {
  const cropSelect = document.getElementById("calendarCropSelect");
  if (cropSelect) {
    cropSelect.addEventListener("change", () => loadCalendar(cropSelect.value));
  }
  loadCalendar("Sugarcane");
}

async function loadCalendar(crop) {
  try {
    const data = await API.getCalendar(crop);
    renderCalendar(data);
  } catch (err) {
    console.warn("Could not load calendar", err);
  }
}

function renderCalendar(data) {
  const container = document.getElementById("calendarTimelineBox");
  const activeStageBox = document.getElementById("calendarActiveStage");
  if (!container) return;

  if (activeStageBox) {
    activeStageBox.innerHTML = `
      <div class="cal-status-banner">
        <span>🌱 Active Stage: <b>${data.current_active_stage}</b></span>
        <span>Days into Season: <b>${data.days_since_sowing} / ${data.total_crop_days} Days</b> (${data.progress_percent}%)</span>
      </div>
      <div class="cal-main-progress-bar">
        <div class="cal-main-progress-fill" style="width: ${data.progress_percent}%"></div>
      </div>
    `;
  }

  container.innerHTML = (data.timeline || []).map(t => `
    <div class="cal-milestone ${t.status}">
      <div class="cal-marker">Day ${t.day}</div>
      <div class="cal-card">
        <div class="cal-card-hdr">
          <span class="cal-date">${t.date}</span>
          <span class="cal-alert-pill">${t.alert}</span>
        </div>
        <h4>${t.title}</h4>
        <p>${t.description}</p>
      </div>
    </div>
  `).join("");
}

// --- Sustainability Meter ---
async function initSustainabilityMeter() {
  try {
    const data = await API.getSustainability(3.5, "Sugarcane");
    renderSustainability(data);
  } catch (err) {
    console.warn("Could not load sustainability", err);
  }
}

function renderSustainability(data) {
  const container = document.getElementById("sustainabilityBox");
  if (!container) return;

  container.innerHTML = `
    <div class="sust-card">
      <div class="sust-top-row">
        <div class="sust-score-circle">
          <div class="score-num">${data.sustainability_index}</div>
          <div class="score-lbl">Eco Index / 100</div>
        </div>
        <div class="sust-narrative-top">
          <h3>Ecological Resource Impact</h3>
          <p>${data.eco_summary}</p>
        </div>
      </div>

      <div class="sust-metric-grid">
        <div class="sust-metric-item water">
          <div class="icon">💧</div>
          <div class="val">${data.water_saved_litres.toLocaleString()} L</div>
          <div class="lbl">Freshwater Conserved (${data.water_saved_m3} m³)</div>
        </div>
        <div class="sust-metric-item carbon">
          <div class="icon">🌍</div>
          <div class="val">${data.total_co2e_saved_kg} kg</div>
          <div class="lbl">CO₂e Mitigation</div>
        </div>
        <div class="sust-metric-item trees">
          <div class="icon">🌳</div>
          <div class="val">${data.trees_equivalent}</div>
          <div class="lbl">Tree Planting Equivalent</div>
        </div>
        <div class="sust-metric-item runoff">
          <div class="icon">🛡️</div>
          <div class="val">${data.nitrogen_saved_kg} kg</div>
          <div class="lbl">Nitrate Runoff Prevented</div>
        </div>
      </div>

      <div class="sust-badges-row">
        ${(data.badges || []).map(b => `
          <div class="eco-badge-card">
            <div class="badge-icon">🏅</div>
            <div>
              <div class="badge-name">${b.name}</div>
              <div class="badge-desc">${b.desc}</div>
            </div>
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

// --- Demo Mode Presentation Flow ---
async function initDemoMode() {
  const startDemoBtn = document.getElementById("btnStartDemo");
  const modal = document.getElementById("demoWalkthroughModal");
  const nextBtn = document.getElementById("btnDemoNext");
  const exitBtn = document.getElementById("btnDemoExit");

  try {
    const res = await API.getDemoSteps();
    demoSteps = res.steps || [];
  } catch (e) {
    console.warn("Could not load demo script", e);
  }

  if (startDemoBtn) {
    startDemoBtn.addEventListener("click", () => {
      if (demoSteps.length === 0) return;
      isDemoRunning = true;
      currentDemoIndex = 0;
      modal.style.display = "block";
      runDemoStep(0);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      currentDemoIndex++;
      if (currentDemoIndex < demoSteps.length) {
        runDemoStep(currentDemoIndex);
      } else {
        exitDemo();
      }
    });
  }

  if (exitBtn) {
    exitBtn.addEventListener("click", exitDemo);
  }
}

async function runDemoStep(index) {
  const step = demoSteps[index];
  if (!step) return;

  // Switch to corresponding tab
  switchTab(step.tab);

  // Update modal text
  const titleEl = document.getElementById("demoStepTitle");
  const narrativeEl = document.getElementById("demoStepNarrative");
  const stepCounterEl = document.getElementById("demoStepCounter");

  if (titleEl) titleEl.textContent = step.title;
  if (narrativeEl) narrativeEl.textContent = step.narrative;
  if (stepCounterEl) stepCounterEl.textContent = `Step ${index + 1} of ${demoSteps.length}`;

  // Execute step action
  switch (step.action) {
    case "trigger_drought":
      await API.triggerSimulator("drought");
      showToast("Simulated environmental drought event!", "warning");
      break;
    case "plan_irrigation":
      await API.triggerSimulator("irrigate");
      document.getElementById("btnCalcIrrigation")?.click();
      break;
    case "run_crop_rec":
      document.getElementById("btnQuickFillSensors")?.click();
      setTimeout(() => {
        document.getElementById("cropRecForm")?.dispatchEvent(new Event("submit"));
      }, 500);
      break;
    case "scan_sample_leaf":
      document.querySelector(".btn-sample-leaf[data-disease-type='Leaf Blight']")?.click();
      break;
    case "calc_fertilizer":
      document.getElementById("btnFertQuickFill")?.click();
      setTimeout(() => {
        document.getElementById("fertilizerForm")?.dispatchEvent(new Event("submit"));
      }, 500);
      break;
    case "calc_yield":
      document.getElementById("yieldForm")?.dispatchEvent(new Event("submit"));
      break;
  }
}

function exitDemo() {
  isDemoRunning = false;
  const modal = document.getElementById("demoWalkthroughModal");
  if (modal) modal.style.display = "none";
  API.triggerSimulator("normal");
  showToast("Demo presentation completed. Returned to normal monitoring mode.", "info");
}

// --- Toast Notifications ---
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add("fade-out");
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}
