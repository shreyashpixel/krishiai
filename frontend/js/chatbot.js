/**
 * KrishiAI - "Krishi Sakha" AI Chatbot Controller
 */

let voiceAssistant = null;

function initChatbot() {
  const chatMessages = document.getElementById("chatMessages");
  const chatInput = document.getElementById("chatInput");
  const sendBtn = document.getElementById("btnSendChat");
  const voiceBtn = document.getElementById("btnVoiceChat");
  const suggestionsContainer = document.getElementById("chatSuggestions");

  // Initialize Voice Assistant
  voiceAssistant = new VoiceAssistant({
    onResult: (transcript) => {
      chatInput.value = transcript;
      handleSendMessage();
    },
    onStateChange: (isListening) => {
      if (voiceBtn) {
        if (isListening) {
          voiceBtn.classList.add("listening-active");
          voiceBtn.setAttribute("title", t("chat_voice_start"));
        } else {
          voiceBtn.classList.remove("listening-active");
          voiceBtn.setAttribute("title", "Voice Input (Click to speak)");
        }
      }
    }
  });

  if (voiceBtn) {
    voiceBtn.addEventListener("click", () => {
      voiceAssistant.toggle(currentLang);
    });
  }

  if (sendBtn) {
    sendBtn.addEventListener("click", handleSendMessage);
  }

  if (chatInput) {
    chatInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleSendMessage();
      }
    });
  }

  // Bind suggested chips
  if (suggestionsContainer) {
    suggestionsContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", () => {
        chatInput.value = chip.textContent.trim();
        handleSendMessage();
      });
    });
  }

  // Refresh suggested chips on language toggle
  window.addEventListener("languageChanged", (e) => {
    updateChatSuggestions(e.detail.lang);
  });
}

function updateChatSuggestions(lang) {
  const container = document.getElementById("chatSuggestions");
  if (!container) return;

  const suggestions = [
    t("chat_suggest_1"),
    t("chat_suggest_2"),
    t("chat_suggest_3"),
    t("chat_suggest_4")
  ];

  container.innerHTML = suggestions
    .map(s => `<button type="button" class="chip chip-suggestion">${s}</button>`)
    .join("");

  container.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const input = document.getElementById("chatInput");
      input.value = chip.textContent.trim();
      handleSendMessage();
    });
  });
}

async function handleSendMessage() {
  const chatInput = document.getElementById("chatInput");
  const chatMessages = document.getElementById("chatMessages");
  const text = chatInput.value.trim();
  if (!text) return;

  // Render User Message
  appendMessage("user", text);
  chatInput.value = "";

  // Render Loading Indicator
  const loadingId = appendLoadingIndicator();

  try {
    const apiKey = localStorage.getItem("krishiai_llm_key") || "";
    const response = await API.sendChatMessage(text, currentLang, apiKey);

    // Remove loading indicator
    removeLoadingIndicator(loadingId);

    // Render Bot Message
    appendMessage("bot", response.reply);

    // Optional TTS read out if user used voice
    if (voiceAssistant && voiceAssistant.isListening) {
      voiceAssistant.speak(response.reply, currentLang);
    }
  } catch (err) {
    removeLoadingIndicator(loadingId);
    appendMessage("bot", "⚠️ Sorry, could not process request right now. Please try again.");
  }
}

function appendMessage(sender, text) {
  const chatMessages = document.getElementById("chatMessages");
  if (!chatMessages) return;

  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-msg ${sender === "user" ? "chat-msg-user" : "chat-msg-bot"}`;

  const formattedHtml = formatChatMarkdown(text);

  if (sender === "bot") {
    msgDiv.innerHTML = `
      <div class="bot-avatar">🌱</div>
      <div class="msg-content">
        <div class="msg-sender-name">Krishi Sakha AI</div>
        <div class="msg-bubble">${formattedHtml}</div>
        <div class="msg-actions">
          <button type="button" class="btn-tts" title="Read aloud" onclick="speakBotText(this)">
            🔊 Speak
          </button>
        </div>
      </div>
    `;
  } else {
    msgDiv.innerHTML = `
      <div class="msg-content">
        <div class="msg-bubble">${escapeHtml(text)}</div>
      </div>
    `;
  }

  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function speakBotText(btn) {
  const bubble = btn.closest(".msg-content").querySelector(".msg-bubble");
  if (bubble && voiceAssistant) {
    voiceAssistant.speak(bubble.innerText, currentLang);
  }
}

function appendLoadingIndicator() {
  const chatMessages = document.getElementById("chatMessages");
  const id = `loading_${Date.now()}`;
  const div = document.createElement("div");
  div.id = id;
  div.className = "chat-msg chat-msg-bot";
  div.innerHTML = `
    <div class="bot-avatar">🌱</div>
    <div class="msg-content">
      <div class="msg-bubble typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return id;
}

function removeLoadingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function formatChatMarkdown(text) {
  // Bold **text**
  let out = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Italics *text*
  out = out.replace(/\*(.*?)\*/g, "<em>$1</em>");
  // Bullets • or -
  out = out.replace(/^[•-]\s*(.*)$/gm, "<li>$1</li>");
  out = out.replace(/(<li>.*<\/li>)/s, "<ul>$1</ul>");
  // Linebreaks
  out = out.replace(/\n/g, "<br/>");
  return out;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
