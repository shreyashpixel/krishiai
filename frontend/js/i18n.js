/**
 * KrishiAI - Multilingual Dictionary (English, हिंदी, मराठी)
 * Supports dynamic real-time language switching across the entire UI.
 */
const I18N = {
  en: {
    app_title: "KrishiAI",
    app_tagline: "Autonomous Smart Agriculture & Precision Agronomy",
    dashboard: "Dashboard",
    crop_rec: "Crop Recommendation",
    disease_detect: "Disease Detection",
    irrigation: "Smart Irrigation",
    weather: "Weather Advisory",
    yield_profit: "Yield & Profit",
    fertilizer: "Fertilizer Calc",
    calendar: "Crop Calendar",
    sustainability: "Eco Footprint",
    chatbot_title: "Krishi Sakha AI",
    start_demo: "Start Demo",
    download_pdf: "Export PDF Report",
    live_status: "IoT Active",
    offline_status: "Offline Simulation",
    farm_health: "Farm Health Score",
    optimal_conditions: "All telemetry within optimal agro-climatic boundaries.",
    
    // Cards
    soil_moisture: "Soil Moisture",
    temperature: "Root Zone Temp",
    humidity: "Air Humidity",
    soil_ph: "Soil pH",
    npk_nutrients: "NPK Nutrients",
    water_saved: "Water Conserved",
    carbon_offset: "Carbon Mitigation",
    
    // Simulation
    sim_controls: "Demo Environmental Simulators",
    sim_normal: "Normal Cycle",
    sim_drought: "Simulate Drought",
    sim_rain: "Simulate Heavy Rain",
    sim_pest: "Simulate Pest Attack",
    sim_irrigate: "Trigger Micro-Drip",
    
    // Crop Recommendation
    crop_rec_title: "Machine Learning Crop Recommendation",
    crop_rec_desc: "Trained on regional agro-climatic datasets across 24 crops including Maharashtra cash crops.",
    quick_fill_sensors: "Auto-fill with Live IoT Sensors",
    btn_predict_crop: "Predict Optimal Crops",
    rec_results_title: "Predicted Top Crops (Random Forest)",
    
    // Disease
    disease_title: "Foliar Plant Disease Diagnosis",
    disease_desc: "Upload or capture a leaf photo to analyze chlorophyll distribution and necrotic lesion ratios.",
    drop_leaf_here: "Drag & drop leaf photo here, or click to browse",
    test_sample_leaf: "Quick Test with Sample Leaves:",
    sample_blight: "Leaf Blight",
    sample_rust: "Foliar Rust",
    sample_mildew: "Powdery Mildew",
    sample_healthy: "Healthy Leaf",
    sample_deficiency: "Chlorosis / Deficiency",
    severity_label: "Severity Index",
    organic_remedy: "Organic & Biological Remedy",
    chemical_remedy: "Chemical Intervention",
    
    // Irrigation
    irrig_title: "Precision Smart Irrigation Planner",
    irrig_desc: "AI water budgeting incorporating root-zone soil moisture, weather forecast, and crop stage.",
    water_needed: "Water Needed",
    drip_runtime: "Drip Run Time",
    btn_calc_irrigation: "Calculate Water Quota",
    
    // Weather
    weather_title: "7-Day Agro-Meteorological Forecast",
    weather_desc: "Open-Meteo precision forecast for agricultural spray windows and frost/heat warnings.",
    detect_location: "Detect My Location",
    
    // Yield
    yield_title: "Yield & APMC Mandi Profit Predictor",
    yield_desc: "Estimate production tonnage, input expenses, and market revenue based on regional mandi prices.",
    btn_predict_yield: "Calculate Projected Returns",
    expected_yield: "Expected Yield",
    total_cost: "Total Cultivation Cost",
    gross_revenue: "Gross Mandi Revenue",
    net_profit: "Estimated Net Profit",
    
    // Fertilizer
    fert_title: "Precision Soil Fertilizer Calculator",
    fert_desc: "Calculates exact commercial fertilizer bags (Urea, DAP, MOP) to avoid excess chemical runoff.",
    btn_calc_fert: "Calculate Exact Dosage",
    
    // Calendar
    cal_title: "Stage-Wise Crop Calendar",
    cal_desc: "Automated growth timeline with fertigation milestones and critical pest scouting alerts.",
    
    // Sustainability
    sust_title: "Carbon & Water Ecological Footprint",
    sust_desc: "Quantifies groundwater preserved and greenhouse gases avoided through smart AI interventions.",
    
    // Chatbot
    chat_placeholder: "Ask about crops, soil, pests, irrigation in English, हिंदी, or मराठी...",
    chat_voice_start: "Listening (Speak now)...",
    chat_suggest_1: "What is my current soil moisture?",
    chat_suggest_2: "How much water do I need to irrigate?",
    chat_suggest_3: "Suggest fertilizers for sugarcane",
    chat_suggest_4: "How to cure leaf blight disease?"
  },
  
  hi: {
    app_title: "कृषिAI",
    app_tagline: "एआई आधारित स्मार्ट कृषि एवं परिशुद्ध खेती प्रणाली",
    dashboard: "डैशबोर्ड",
    crop_rec: "फसल सुझाव (ML)",
    disease_detect: "पादप रोग पहचान",
    irrigation: "स्मार्ट सिंचाई",
    weather: "मौसम सलाह",
    yield_profit: "उपज व लाभ",
    fertilizer: "उर्वरक गणक",
    calendar: "फसल कैलेंडर",
    sustainability: "पर्यावरण बचत",
    chatbot_title: "कृषि सखा एआई",
    start_demo: "डेमो शुरू करें",
    download_pdf: "पीडीएफ रिपोर्ट डाउनलोड",
    live_status: "आईओटी सक्रिय",
    offline_status: "ऑफलाइन सिमुलेशन",
    farm_health: "खेत स्वास्थ्य स्कोर",
    optimal_conditions: "सभी कृषि-मौसम मापदंड अनुकूल स्तर पर हैं।",
    
    soil_moisture: "मिट्टी की नमी",
    temperature: "जड़ तापमान",
    humidity: "हवा में आर्द्रता",
    soil_ph: "मिट्टी का pH",
    npk_nutrients: "NPK पोषक तत्व",
    water_saved: "जल संरक्षण",
    carbon_offset: "कार्बन बचत",
    
    sim_controls: "पर्यावरणीय सिमुलेटर",
    sim_normal: "सामान्य स्थिति",
    sim_drought: "सूखा सिमुलेट करें",
    sim_rain: "भारी बारिश सिमुलेट करें",
    sim_pest: "कीट हमला सिमुलेट करें",
    sim_irrigate: "ड्रिप सिंचाई चालू करें",
    
    crop_rec_title: "मशीन लर्निंग फसल चयन प्रणाली",
    crop_rec_desc: "24 प्रमुख फसलों और क्षेत्रीय कृषि आंकड़ों पर प्रशिक्षित रैंडम फॉरेस्ट मॉडल।",
    quick_fill_sensors: "सेंसर डेटा स्वतः भरें",
    btn_predict_crop: "उपयुक्त फसलें जानें",
    rec_results_title: "सर्वोत्तम अनुशंसित फसलें (Random Forest)",
    
    disease_title: "पत्ती रोग पहचान एवं निदान",
    disease_desc: "रोगग्रस्त पत्ती की फोटो अपलोड करें और तुरंत जैविक व रासायनिक उपचार पाएं।",
    drop_leaf_here: "पत्ती की फोटो यहां खींचें या अपलोड करें",
    test_sample_leaf: "नमूना पत्तियों से जांचें:",
    sample_blight: "पत्ती झुलसा (Blight)",
    sample_rust: "गेरुआ (Rust)",
    sample_mildew: "चूर्णी फफूंद (Mildew)",
    sample_healthy: "स्वस्थ पत्ती",
    sample_deficiency: "पोषक तत्व कमी",
    severity_label: "रोग की तीव्रता",
    organic_remedy: "जैविक एवं देसी उपचार",
    chemical_remedy: "रासायनिक कीटनाशक उपचार",
    
    irrig_title: "स्मार्ट सटीक सिंचाई योजनाकार",
    irrig_desc: "मिट्टी की नमी और मौसम पूर्वानुमान के आधार पर आवश्यक जल का सटीक अनुमान।",
    water_needed: "आवश्यक जल मात्रा",
    drip_runtime: "ड्रिप चलाने का समय",
    btn_calc_irrigation: "सिंचाई मात्रा गणना करें",
    
    weather_title: "7-दिवसीय कृषि मौसम पूर्वानुमान",
    weather_desc: "छिड़काव एवं कीट नियंत्रण के लिए ओपन-मेटियो आधारित मौसम सलाह।",
    detect_location: "मेरा स्थान पहचानें",
    
    yield_title: "उपज एवं मंडी मुनाफा गणक",
    yield_desc: "मंडी दरों और लागत के आधार पर अनुमानित उत्पादन और शुद्ध लाभ की गणना।",
    btn_predict_yield: "संभावित आय की गणना करें",
    expected_yield: "अनुमानित कुल उपज",
    total_cost: "कुल खेती लागत",
    gross_revenue: "मंडी से कुल आय",
    net_profit: "शुद्ध मुनाफा",
    
    fert_title: "सटीक उर्वरक एवं खाद गणक",
    fert_desc: "मिट्टी परीक्षण के अनुसार यूरिया, डीएपी व पोटाश की सटीक बोरियां।",
    btn_calc_fert: "खाद की मात्रा निकालें",
    
    cal_title: "फसल विकास कैलेंडर",
    cal_desc: "बुवाई से कटाई तक प्रत्येक चरण के कार्य और जरूरी अनुस्मारक।",
    
    sust_title: "जल एवं कार्बन फुटप्रिंट बचत",
    sust_desc: "एआई स्मार्ट खेती से बचाए गए भूजल और ग्रीनहाउस गैसों का ब्योरा।",
    
    chat_placeholder: "फसल, खाद, रोग, सिंचाई पर हिंदी, मराठी या अंग्रेजी में पूछें...",
    chat_voice_start: "सुन रहा हूँ (अब बोलें)...",
    chat_suggest_1: "मेरे खेत की नमी कितनी है?",
    chat_suggest_2: "सिंचाई के लिए कितना पानी चाहिए?",
    chat_suggest_3: "गन्ने के लिए खाद की मात्रा बताएं",
    chat_suggest_4: "पत्ती झुलसा रोग का उपचार क्या है?"
  },
  
  mr: {
    app_title: "कृषीAI",
    app_tagline: "आर्टिफिशियल इंटेलिजन्स आधारित स्मार्ट शेती प्रणाली",
    dashboard: "डॅशबोर्ड",
    crop_rec: "पीक शिफारस (ML)",
    disease_detect: "रोग निदान",
    irrigation: "स्मार्ट सिंचन",
    weather: "हवामान अंदाज",
    yield_profit: "उत्पादन व नफा",
    fertilizer: "खत गणक",
    calendar: "पीक दिनदर्शिका",
    sustainability: "पर्यावरण संवर्धन",
    chatbot_title: "कृषी सखा एआय",
    start_demo: "डेमो सुरू करा",
    download_pdf: "पीडीएफ अहवाल मिळवा",
    live_status: "आयओटी चालू",
    offline_status: "ऑफलाइन सिम्युलेशन",
    farm_health: "शेती आरोग्य निर्देशांक",
    optimal_conditions: "शेतातील सर्व हवामान व माती घटक उत्तम स्थितीत आहेत.",
    
    soil_moisture: "जमिनीतील ओलावा",
    temperature: "मुळांचे तापमान",
    humidity: "हवेतील आर्द्रता",
    soil_ph: "जमिनीचा सामू (pH)",
    npk_nutrients: "NPK अन्नद्रव्ये",
    water_saved: "पाण्याची बचत",
    carbon_offset: "कार्बन उत्सर्जन घट",
    
    sim_controls: "पर्यावरण सिम्युलेटर नियंत्रणे",
    sim_normal: "सामान्य स्थिती",
    sim_drought: "दुष्काळ सिम्युलेट करा",
    sim_rain: "मुसळधार पाऊस सिम्युलेट करा",
    sim_pest: "कीड प्रादुर्भाव सिम्युलेट करा",
    sim_irrigate: "ठिबक सिंचन सुरू करा",
    
    crop_rec_title: "मशीन लर्निंग पीक शिफारस",
    crop_rec_desc: "महाराष्ट्रातील मुख्य नगदी पिके (ऊस, कापूस, सोयाबीन, कांदा, द्राक्षे) यांसह २४ पिकांसाठी प्रशिक्षित.",
    quick_fill_sensors: "सेंसर डेटा थेट भरा",
    btn_predict_crop: "योग्य पिके शोधा",
    rec_results_title: "शिफारस केलेली सर्वोत्तम पिके (Random Forest)",
    
    disease_title: "पानावरील रोग निदान व उपचार",
    disease_desc: "पानाचा फोटो अपलोड करा आणि त्वरित जैविक व रासायनिक उपाय मिळवा.",
    drop_leaf_here: "येथे पानाचा फोटो अपलोड करा किंवा क्लिक करा",
    test_sample_leaf: "नमुना पानांवरून चाचणी घ्या:",
    sample_blight: "करपा रोग (Blight)",
    sample_rust: "तांबेरा (Rust)",
    sample_mildew: "भुरी रोग (Mildew)",
    sample_healthy: "निरोगी पान",
    sample_deficiency: "अन्नद्रव्य कमतरता",
    severity_label: "रोगाची तीव्रता",
    organic_remedy: "सेंद्रिय व जैविक उपाय",
    chemical_remedy: "रासायनिक फवारणी",
    
    irrig_title: "अचूक स्मार्ट सिंचन नियोजन",
    irrig_desc: "जमिनीतील ओलावा आणि पावसाचा अंदाज पाहून ठिबक सिंचनाची वेळ व पाणी ठरवा.",
    water_needed: "आवश्यक पाणी",
    drip_runtime: "ठिबक सिंचन वेळ",
    btn_calc_irrigation: "पाण्याची गरज मोजा",
    
    weather_title: "७ दिवसांचा कृषी हवामान अंदाज",
    weather_desc: "फवारणीची योग्य वेळ आणि हवामान संकटांची पूर्वसूचना देणारा अंदाज.",
    detect_location: "माझे ठिकाण शोधा",
    
    yield_title: "उत्पादन व बाजारभाव नफा गणक",
    yield_desc: "बाजार समिती (APMC) हमीभाव आणि उत्पादन खर्चावर आधारित निव्वळ नफा.",
    btn_predict_yield: "संभाव्य नफा मोजा",
    expected_yield: "अपेक्षित एकूण उत्पादन",
    total_cost: "एकूण उत्पादन खर्च",
    gross_revenue: "बाजार समितीतील एकूण उत्पन्न",
    net_profit: "अपेक्षित निव्वळ नफा",
    
    fert_title: "माती परीक्षणानुसार अचूक खत गणक",
    fert_desc: "युरिया, डीएपी आणि पोटाशच्या अचूक गोण्या व सेंद्रिय गांडूळ खत पद्धती.",
    btn_calc_fert: "खतांची मात्रा काढा",
    
    cal_title: "टप्प्याटप्प्याने पीक दिनदर्शिका",
    cal_desc: "लागवडीपासून काढणीपर्यंतचे सर्व महत्त्वाचे टप्पे व फवारणीच्या आठवणी.",
    
    sust_title: "जल व कार्बन बचत निर्देशांक",
    sust_desc: "स्मार्ट शेती तंत्रज्ञानामुळे वाचवलेले लाखो लिटर पाणी व पर्यावरण संवर्धन.",
    
    chat_placeholder: "पीक, खते, रोग किंवा सिंचनाबद्दल मराठी, हिंदी किंवा इंग्रजीत विचारा...",
    chat_voice_start: "ऐकत आहे (आता बोला)...",
    chat_suggest_1: "जमिनीतील सध्याचा ओलावा किती आहे?",
    chat_suggest_2: "पिकाला किती लिटर पाणी द्यावे?",
    chat_suggest_3: "उसासाठी खतांचे प्रमाण सांगा",
    chat_suggest_4: "पानावरील करपा रोगावर काय उपाय करावा?"
  }
};

let currentLang = "en";

function setLanguage(lang) {
  if (!I18N[lang]) lang = "en";
  currentLang = lang;
  
  // Apply data-i18n attributes
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (I18N[lang][key]) {
      el.textContent = I18N[lang][key];
    }
  });

  // Apply placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (I18N[lang][key]) {
      el.placeholder = I18N[lang][key];
    }
  });

  // Save to localStorage
  localStorage.setItem("krishiai_lang", lang);
  
  // Dispatch custom event for dynamic components
  window.dispatchEvent(new CustomEvent("languageChanged", { detail: { lang } }));
}

function t(key) {
  return (I18N[currentLang] && I18N[currentLang][key]) || (I18N["en"][key]) || key;
}
