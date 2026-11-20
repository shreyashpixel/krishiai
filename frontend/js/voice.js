/**
 * KrishiAI - Voice Recognition & Speech Synthesis (Web Speech API)
 * Supports multilingual Indian accents for English, Hindi, and Marathi.
 */

class VoiceAssistant {
  constructor(options = {}) {
    this.recognition = null;
    this.isListening = false;
    this.ttsEnabled = true;
    this.onResult = options.onResult || (() => {});
    this.onStateChange = options.onStateChange || (() => {});

    this.initRecognition();
  }

  initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Web Speech API not supported in this browser.");
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;

    this.recognition.onstart = () => {
      this.isListening = true;
      this.onStateChange(true);
    };

    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      this.onResult(transcript);
    };

    this.recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      this.isListening = false;
      this.onStateChange(false);
    };

    this.recognition.onend = () => {
      this.isListening = false;
      this.onStateChange(false);
    };
  }

  toggle(lang = "en") {
    if (!this.recognition) {
      alert("Voice input is not supported in this browser. Please use Chrome, Edge, or a WebSpeech-enabled browser.");
      return;
    }

    if (this.isListening) {
      this.recognition.stop();
    } else {
      // Map language code to BCP 47
      const langMap = {
        en: "en-IN",
        hi: "hi-IN",
        mr: "mr-IN"
      };
      this.recognition.lang = langMap[lang] || "en-IN";
      try {
        this.recognition.start();
      } catch (e) {
        console.error("Could not start recognition", e);
      }
    }
  }

  speak(text, lang = "en") {
    if (!this.ttsEnabled || !window.speechSynthesis) return;

    window.speechSynthesis.cancel(); // Stop any pending speech

    // Strip markdown formatting for cleaner speech
    const cleanText = text.replace(/[*#_`•]/g, "").replace(/\n+/g, ". ");

    const utterance = new SpeechSynthesisUtterance(cleanText);
    const langMap = {
      en: "en-IN",
      hi: "hi-IN",
      mr: "mr-IN"
    };
    utterance.lang = langMap[lang] || "en-IN";
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    window.speechSynthesis.speak(utterance);
  }
}
