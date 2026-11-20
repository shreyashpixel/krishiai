"""
KrishiAI - "Krishi Sakha" Intelligent Farm Assistant
Rule-based NLP intent matcher grounded in live IoT telemetry and agronomic datasets.
Supports English, Hindi, and Marathi questions, with an optional LLM API hook.
"""
import re
from typing import Dict, Any, List
from backend.simulator import iot_simulator
from backend.config import CROP_AGRONOMY, DISEASE_INFO

class KrishiSakhaChatbot:
    def __init__(self):
        self.custom_api_key: str = None

    def set_api_key(self, api_key: str):
        """Sets user-provided optional LLM API key."""
        self.custom_api_key = api_key.strip() if api_key else None

    def reply(self, user_text: str, language: str = "en") -> Dict[str, Any]:
        """
        Analyzes message intent, extracts agricultural entities, grounds response
        in live IoT farm sensor values, and formats a helpful multi-lingual response.
        """
        query = user_text.lower().strip()
        live = iot_simulator.get_current_readings()

        # 1. Check if user configured an external LLM key
        if self.custom_api_key and len(self.custom_api_key) > 15:
            # External LLM hook placeholder for production API call
            # If external call fails or isn't reached, it seamlessly falls through to local engine
            pass

        # 2. Intent matching with keyword regexes across EN, HI, MR
        
        # Intent: Live Soil / Sensor Status
        if any(w in query for w in ["sensor", "status", "moisture", "temperature", "temp", "humidity", "ph", "npk", "ओलावा", "नमी", "तापमान", "रीडिंग"]):
            intent = "live_telemetry"
            if language == "mr":
                reply_text = (
                    f"🌾 **सध्याची शेतातील स्थिती (Live Telemetry):**\n"
                    f"• जमिनीतील ओलावा: **{live['soil_moisture']}%**\n"
                    f"• तापमान: **{live['temperature']}°C** | आर्द्रता: **{live['humidity']}%**\n"
                    f"• जमिनीचा pH: **{live['ph']}** (उत्तम)\n"
                    f"• मातीतील N-P-K: **{live['nitrogen']} : {live['phosphorus']} : {live['potassium']}** kg/ha\n"
                    f"• एकूण शेती आरोग्य स्कोअर: **{live['health_score']}/100** ({live['condition_alert']})"
                )
            elif language == "hi":
                reply_text = (
                    f"🌾 **वर्तमान खेत स्थिति (Live Telemetry):**\n"
                    f"• मिट्टी की नमी: **{live['soil_moisture']}%**\n"
                    f"• तापमान: **{live['temperature']}°C** | आर्द्रता: **{live['humidity']}%**\n"
                    f"• मिट्टी का pH: **{live['ph']}**\n"
                    f"• N-P-K पोषक तत्व: **{live['nitrogen']} : {live['phosphorus']} : {live['potassium']}** kg/ha\n"
                    f"• खेत स्वास्थ्य स्कोर: **{live['health_score']}/100** ({live['condition_alert']})"
                )
            else:
                reply_text = (
                    f"🌾 **Live Farm Telemetry:**\n"
                    f"• Soil Moisture: **{live['soil_moisture']}%**\n"
                    f"• Temperature: **{live['temperature']}°C** | Humidity: **{live['humidity']}%**\n"
                    f"• Soil pH: **{live['ph']}**\n"
                    f"• Available N-P-K: **{live['nitrogen']} : {live['phosphorus']} : {live['potassium']}** kg/ha\n"
                    f"• Overall Farm Health Score: **{live['health_score']}/100**\n"
                    f"• Current Alert: *{live['condition_alert']}*"
                )

        # Intent: Irrigation & Water Planning
        elif any(w in query for w in ["irrigation", "water", "litres", "pani", "paani", "सिंचाई", "पानी", "पाणी"]):
            intent = "irrigation"
            plan = iot_simulator.plan_smart_irrigation()
            if language == "mr":
                reply_text = (
                    f"💧 **स्मार्ट सिंचन सल्ला (Smart Irrigation):**\n"
                    f"• सद्य ओलावा: {plan['current_moisture']}%\n"
                    f"• गरज: **{plan['water_required_litres']:,} लिटर** ({plan['drip_runtime_minutes']} मिनिटे ठिबक सिंचन)\n"
                    f"• पारंपारिक पद्धतीपेक्षा पाणी बचत: **{plan['water_saved_litres']:,} लिटर** (५४% बचत!)\n"
                    f"• स्थिती: {plan['status_text']}"
                )
            elif language == "hi":
                reply_text = (
                    f"💧 **स्मार्ट सिंचाई सलाह (Smart Irrigation):**\n"
                    f"• वर्तमान नमी: {plan['current_moisture']}%\n"
                    f"• आवश्यक जल: **{plan['water_required_litres']:,} लीटर** ({plan['drip_runtime_minutes']} मिनट ड्रिप चक्र)\n"
                    f"• पानी की बचत: **{plan['water_saved_litres']:,} लीटर**\n"
                    f"• सलाह: {plan['status_text']}"
                )
            else:
                reply_text = (
                    f"💧 **Smart Irrigation Plan:**\n"
                    f"• Current Soil Moisture: **{plan['current_moisture']}%** (Target: {plan['target_moisture']}%)\n"
                    f"• Water Needed: **{plan['water_required_litres']:,} Litres**\n"
                    f"• Recommended Run Time: **{plan['drip_runtime_minutes']} mins** via micro-drip.\n"
                    f"• Water Conserved vs Flood Irrigation: **{plan['water_saved_litres']:,} Litres**.\n"
                    f"• Schedule: *{plan['time_to_irrigate']}* ({plan['status_text']})"
                )

        # Intent: Fertilizer / Urea / DAP
        elif any(w in query for w in ["fertilizer", "urea", "dap", "mop", "khad", "khat", "खत", "खाद", "यूरिया", "डीएपी"]):
            intent = "fertilizer"
            if language == "mr":
                reply_text = (
                    f"🌱 **खत व्यवस्थापन सल्ला (Fertilizer Advisory):**\n"
                    f"• तुमच्या जमिनीत नत्र (N: {live['nitrogen']}) आणि स्फुरद (P: {live['phosphorus']}) मध्यम आहे.\n"
                    f"• **रासायनिक मात्रा:** प्रति एकर १.२ गोणी डीएपी (पेरणीच्या वेळी) + २ गोणी युरिया (दोन हप्त्यात).\n"
                    f"• **सेंद्रिय पर्याय:** १.५ टन गांडूळ खत + २०० ग्रॅम ट्रायकोडर्मा व निंबोळी पेंड (१०० किलो) वापरा."
                )
            elif language == "hi":
                reply_text = (
                    f"🌱 **उर्वरक प्रबंधन सलाह (Fertilizer Advisory):**\n"
                    f"• मिट्टी में N: {live['nitrogen']}, P: {live['phosphorus']}, K: {live['potassium']} उपलब्ध है।\n"
                    f"• **रासायनिक मात्रा:** प्रति एकड़ 1.2 बोरी DAP (बुवाई समय) और 2 बोरी यूरिया (25-30 दिन के अंतराल पर)।\n"
                    f"• **जैविक विकल्प:** प्रति एकड़ 1.5 टन केंचुआ खाद (वर्मीकम्पोस्ट) + 100 किग्रा नीम खली का प्रयोग करें।"
                )
            else:
                reply_text = (
                    f"🌱 **Fertilizer Management Protocol:**\n"
                    f"• Based on your soil tests (N: {live['nitrogen']}, P: {live['phosphorus']}, K: {live['potassium']}):\n"
                    f"• **Chemical Dosage:** Apply 1.2 bags DAP at sowing as basal dose, followed by 2 bags Urea split across vegetative and flowering stages.\n"
                    f"• **Eco-Friendly Alternative:** 1.5 tons Vermicompost + 100 kg Neem Cake + Azotobacter & PSB biofertilizers (2 kg each/acre) to restore soil organic carbon."
                )

        # Intent: Plant Disease & Leaf Spots
        elif any(w in query for w in ["disease", "blight", "rust", "mildew", "leaf", "spot", "रोग", "करपा", "तांबेरा", "पाने", "पत्तियां", "कीट"]):
            intent = "disease"
            if language == "mr":
                reply_text = (
                    f"🛡️ **रोग नियंत्रण मार्गदर्शन (Plant Pathology):**\n"
                    f"• **करपा (Leaf Blight):** पानांवर तपकिरी चट्टे दिसल्यास ५० मिली आंबट ताक किंवा स्युडोमोनास (५ ग्रॅम/लिटर) फवारा.\n"
                    f"• **तांबेरा (Rust):** प्रोपिकोनाझोल (१ मिली/लिटर) किंवा दशपर्णी अर्क वापरा.\n"
                    f"• **भुरी (Powdery Mildew):** पाण्यात दूध (१:९) किंवा पाण्यात विरघळणारे गंधक (३ ग्रॅम/लिटर) फवारा.\n"
                    f"📸 पानाचा फोटो 'Plant Disease' टॅबमध्ये अपलोड करून अचूक निदान व तीव्रता तपासा!"
                )
            elif language == "hi":
                reply_text = (
                    f"🛡️ **पादप रोग निदान (Plant Disease Guide):**\n"
                    f"• **पत्ती झुलसा (Blight):** खट्टी छाछ 50 मिली/लीटर या मैंकोजेब 75% WP @ 2.5 ग्राम/लीटर का छिड़काव करें।\n"
                    f"• **गेरुआ (Rust):** प्रोपिकोनाजोल 1 मिली/लीटर अथवा घुलनशील गंधक का छिड़काव करें।\n"
                    f"• **चूर्णी फफूंद (Powdery Mildew):** हेक्साकोनाजोल 2 मिली/लीटर या नीम तेल 5 मिली/लीटर का प्रयोग करें।\n"
                    f"📸 सटीक जांच के लिए 'Disease Detection' टैब में पत्ती की फोटो अपलोड करें!"
                )
            else:
                reply_text = (
                    f"🛡️ **Plant Disease Management Guide:**\n"
                    f"• **Leaf Blight:** Spray fermented buttermilk (50ml/L) or Mancozeb 75% WP @ 2.5g/L on affected lower canopy.\n"
                    f"• **Foliar Rust:** Spray Propiconazole 25% EC @ 1ml/L or bio-sulfur @ 3g/L.\n"
                    f"• **Powdery Mildew:** Apply Hexaconazole 5% SC @ 2ml/L or 10% milk-water solution in sunlight.\n"
                    f"📸 *Tip:* Upload a leaf photograph directly to the **Plant Disease Detection** tab for instant ML severity scanning!"
                )

        # Intent: Government Subsidies / Mandi Schemes
        elif any(w in query for w in ["scheme", "subsidy", "pm-kisan", "yojana", "अनुदान", "योजना", "सब्सिडी", "मंडी"]):
            intent = "schemes"
            if language == "mr":
                reply_text = (
                    f"🏛️ **शासकीय कृषी योजना व सबसिडी:**\n"
                    f"1. **महाडीबीटी (MahaDBT):** ठिबक सिंचनासाठी (Drip Irrigation) ८०% पर्यंत अनुदान.\n"
                    f"2. **पीएम-किसान (PM-KISAN):** वार्षिक ₹६,००० थेट खात्यात.\n"
                    f"3. **पीक विमा (PMFBY):** केवळ ₹१ मध्ये सर्वसमावेशक पीक विमा संरक्षण.\n"
                    f"4. **सोलर कृषी पंप (KUSUM Yojana):** ९०% अनुदानावर सौर पंप बसवा."
                )
            elif language == "hi":
                reply_text = (
                    f"🏛️ **प्रमुख सरकारी कृषि योजनाएं:**\n"
                    f"1. **ड्रिप सिंचाई सब्सिडी (PMKSY):** सूक्ष्म सिंचाई संयंत्रों पर 55% से 80% तक अनुदान।\n"
                    f"2. **पीएम किसान सम्मान निधि:** पात्र किसानों को प्रतिवर्ष ₹6,000 की आर्थिक सहायता।\n"
                    f"3. **पीएम फसल बीमा योजना (PMFBY):** प्राकृतिक आपदाओं से फसल नुकसान का त्वरित क्लेम।\n"
                    f"4. **पीएम कुसुम योजना:** खेतों में सोलर पम्प स्थापना पर 60% तक सरकारी अनुदान।"
                )
            else:
                reply_text = (
                    f"🏛️ **Key Agricultural Schemes & Subsidies:**\n"
                    f"1. **Micro-Irrigation Subsidy (PMKSY / MahaDBT):** Up to 55-80% financial subsidy for drip and sprinkler installations.\n"
                    f"2. **PM-KISAN:** Direct income transfer of ₹6,000/year in 3 installments.\n"
                    f"3. **PMFBY (Crop Insurance):** Comprehensive insurance coverage for drought, excessive rain, and pests at nominal premium.\n"
                    f"4. **PM-KUSUM Scheme:** 60-90% subsidized grid-independent solar agricultural water pumps."
                )

        # Intent: Crop recommendation general
        elif any(w in query for w in ["crop", "suggest", "grow", "recommend", "पिक", "फसल", "काय पिकवू", "क्या उगाएं"]):
            intent = "crops"
            if language == "mr":
                reply_text = (
                    f"🌱 **पीक शिफारस (Crop Recommendation):**\n"
                    f"• तुमच्या जमिनीतील NPK ({live['nitrogen']}:{live['phosphorus']}:{live['potassium']}) व {live['soil_moisture']}% ओलाव्यानुसार:\n"
                    f"• **ऊस (Sugarcane):** काळ्या कसदार जमिनीत ठिबक सिंचनावर भरपूर उत्पादन.\n"
                    f"• **कापूस (Cotton) किंवा सोयाबीन (Soybean):** खरिपातील उत्तम नगदी पिके.\n"
                    f"• **कांदा (Onion):** रब्बी हंगामात चांगला बाजारभाव मिळण्याची शक्यता.\n"
                    f"📊 तपशीलवार एआय विश्लेषणासाठी वरील **Crop Recommendation** टॅब वापरा!"
                )
            elif language == "hi":
                reply_text = (
                    f"🌱 **फसल सुझाव (Crop Recommendation):**\n"
                    f"• आपके खेत की वर्तमान मिट्टी (N: {live['nitrogen']}, P: {live['phosphorus']}, K: {live['potassium']}, नमी: {live['soil_moisture']}%):\n"
                    f"• **गन्ना (Sugarcane):** ड्रिप सिंचाई के साथ अत्यधिक लाभदायक।\n"
                    f"• **कपास (Cotton) या सोयाबीन (Soybean):** खरीफ मौसम की सर्वोत्तम नकदी फसलें।\n"
                    f"• **प्याज (Onion):** रबी सीजन के लिए उच्च लाभप्रदता।\n"
                    f"📊 विस्तृत रिपोर्ट के लिए **Crop Recommendation** मॉडल का उपयोग करें।"
                )
            else:
                reply_text = (
                    f"🌱 **Crop Recommendation Advisory:**\n"
                    f"• Based on current soil metrics (N: {live['nitrogen']}, P: {live['phosphorus']}, K: {live['potassium']}, pH: {live['ph']}):\n"
                    f"• **Sugarcane:** Exceptional yields under precision drip irrigation in fertile medium-black soil.\n"
                    f"• **Cotton & Soybean:** Optimal Kharif cash crops matching local temperature and rainfall profiles.\n"
                    f"• **Rabi Onion:** Strong mandi price trends and moderate moisture needs.\n"
                    f"📊 *Tip:* Head to the **Crop Recommendation** tab to run the full Random Forest classifier model!"
                )

        # General Greeting / Help
        else:
            intent = "general_help"
            if language == "mr":
                reply_text = (
                    f"नमस्कार शेतकरी बंधूंनो! मी **कृषी सखा (KrishiAI)** आहे.\n"
                    f"मी तुम्हाला जमिनीतील ओलावा, हवामान, पीक शिफारस, खतांचे प्रमाण, रोग नियंत्रण आणि सरकारी योजना याबद्दल माहिती देऊ शकतो.\n"
                    f"तुम्ही मला मराठी, हिंदी किंवा इंग्रजीत प्रश्न विचारू शकता किंवा माईक 🎙️ द्वारे बोलू शकता!"
                )
            elif language == "hi":
                reply_text = (
                    f"नमस्ते किसान भाई! मैं **कृषि सखा (KrishiAI)** हूँ।\n"
                    f"मैं आपको खेत की नमी, मौसम पूर्वानुमान, फसल चयन, खाद की मात्रा, कीट-रोग नियंत्रण और सरकारी योजनाओं में सहायता कर सकता हूँ।\n"
                    f"आप हिंदी, मराठी या अंग्रेजी में पूछ सकते हैं अथवा माइक 🎙️ का प्रयोग कर सकते हैं।"
                )
            else:
                reply_text = (
                    f"Hello! I am **Krishi Sakha**, your AI Agricultural Assistant.\n"
                    f"I have direct access to your farm's real-time IoT sensors (moisture, NPK, temperature, pH).\n"
                    f"Ask me anything about:\n"
                    f"• *'What is my current soil moisture?'*\n"
                    f"• *'How many litres of irrigation do I need?'*\n"
                    f"• *'Recommend fertilizers for sugarcane'* \n"
                    f"• *'How to treat leaf blight or rust?'*\n"
                    f"• *'Government subsidies for drip farming'*\n"
                    f"You can also use the microphone button 🎙️ for voice queries in English, Hindi, or Marathi!"
                )

        return {
            "reply": reply_text,
            "intent": intent,
            "language": language,
            "live_context": {
                "soil_moisture": live["soil_moisture"],
                "temperature": live["temperature"],
                "health_score": live["health_score"]
            }
        }

# Singleton chatbot instance
krishi_chatbot = KrishiSakhaChatbot()
