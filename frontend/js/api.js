/**
 * KrishiAI - API Client & Telemetry WebSocket Streamer
 */
const API = {
  baseUrl: "",

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, options);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server returned status ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  },

  // 1. Telemetry
  getCurrentSensors() {
    return this.request("/api/sensors/current");
  },

  getSensorHistory(limit = 30) {
    return this.request(`/api/sensors/history?limit=${limit}`);
  },

  triggerSimulator(event) {
    return this.request(`/api/simulator/trigger?event=${encodeURIComponent(event)}`, {
      method: "POST"
    });
  },

  // 2. Crop Recommendation
  recommendCrop(data) {
    return this.request("/api/crop/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  },

  // 3. Disease Detection
  detectDisease(file) {
    const formData = new FormData();
    formData.append("file", file);
    return fetch("/api/disease/detect", {
      method: "POST",
      body: formData
    }).then(res => {
      if (!res.ok) throw new Error("Diagnosis failed");
      return res.json();
    });
  },

  testSampleLeaf(diseaseType) {
    return this.request(`/api/disease/sample-leaf?disease_type=${encodeURIComponent(diseaseType)}`);
  },

  // 4. Irrigation
  planIrrigation(data) {
    return this.request("/api/irrigation/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  },

  // 5. Weather
  getWeather(lat = null, lon = null) {
    let url = "/api/weather";
    if (lat && lon) {
      url += `?lat=${lat}&lon=${lon}`;
    }
    return this.request(url);
  },

  // 6. Yield & Profit
  predictYield(data) {
    return this.request("/api/yield/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  },

  // 7. Fertilizer
  calculateFertilizer(data) {
    return this.request("/api/fertilizer/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
  },

  // 8. Calendar
  getCalendar(crop, startDate = "") {
    let url = `/api/calendar?crop=${encodeURIComponent(crop)}`;
    if (startDate) url += `&start_date=${encodeURIComponent(startDate)}`;
    return this.request(url);
  },

  // 9. Sustainability
  getSustainability(area = 3.5, crop = "Sugarcane") {
    return this.request(`/api/sustainability?area=${area}&crop=${encodeURIComponent(crop)}`);
  },

  // 10. Chatbot
  sendChatMessage(message, language = "en", apiKey = "") {
    return this.request("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, language, api_key: apiKey })
    });
  },

  // 11. Demo Steps
  getDemoSteps() {
    return this.request("/api/demo/steps");
  },

  // 12. PDF Report URL
  getPdfDownloadUrl() {
    return "/api/report/pdf";
  }
};

/**
 * WebSocket Live Telemetry Listener with Automatic Fallback Polling
 */
class TelemetryStreamer {
  constructor(onUpdate) {
    this.onUpdate = onUpdate;
    this.ws = null;
    this.pollInterval = null;
    this.connect();
  }

  connect() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/sensors`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log("WebSocket connected for live field telemetry.");
        if (this.pollInterval) {
          clearInterval(this.pollInterval);
          this.pollInterval = null;
        }
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onUpdate(data);
        } catch (e) {
          console.error("Error parsing telemetry frame", e);
        }
      };

      this.ws.onerror = (err) => {
        console.warn("WebSocket encountered issue; engaging HTTP polling fallback.", err);
        this.fallbackPolling();
      };

      this.ws.onclose = () => {
        console.log("WebSocket closed; starting fallback polling.");
        this.fallbackPolling();
      };
    } catch (e) {
      this.fallbackPolling();
    }
  }

  fallbackPolling() {
    if (!this.pollInterval) {
      this.pollInterval = setInterval(async () => {
        try {
          const data = await API.getCurrentSensors();
          this.onUpdate(data);
        } catch (e) {
          // Silent catch in offline/reconnect
        }
      }, 3000);
    }
  }
}
