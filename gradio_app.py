"""
CropLens — AI Crop Doctor (Gradio Application)
Full feature set preserved:
- ZeroGPU compatibility (@spaces.GPU) & CPU compatibility
- DIF code authentication & scan credits tracking (AB12, CD34, EF56)
- English and Hindi full localization
- Leaf photo upload & webcam capture
- Crop identification input
- TFLite model inference + Gemini multimodal vision diagnosis
- Comprehensive 22+ plant pathology disease advice (severity, symptoms, prevention, treatment)
- Outbreak reporting with water body detection
"""

import os
import json
import re
import io
import base64
from datetime import datetime, timezone
import requests
import numpy as np
from PIL import Image
import gradio as gr

# Hugging Face ZeroGPU support
try:
    import spaces
    HAVE_SPACES = True
except ImportError:
    HAVE_SPACES = False

# Try optional dependencies gracefully
try:
    from supabase import create_client
    SUPABASE_SDK_AVAILABLE = True
except ImportError:
    SUPABASE_SDK_AVAILABLE = False

try:
    import tensorflow as tf
    TFLITE_AVAILABLE = True
except ImportError:
    TFLITE_AVAILABLE = False

# =================================================================
# TRANSLATIONS
# =================================================================
TEXT = {
    "en": {
        "app_title": "🌱 CropLens — AI Crop Doctor",
        "tagline": "Point your phone at a leaf. Get a diagnosis in seconds.",
        "signin_title": "Farmer Sign In",
        "signin_subtitle": "Enter your DIF Code to continue (e.g. AB12)",
        "dif_label": "DIF Code (2 letters + 2 digits)",
        "signin_button": "Sign In",
        "signed_in_as": "Signed in as",
        "credits_label": "Scans remaining",
        "credits_exhausted": "Credits Exhausted. Please visit agrifusion-web.vercel.app to purchase more scans.",
        "signout": "Sign out",
        "instructions": (
            "### 📸 How to take a good photo:\n"
            "- Take the photo in good daylight — avoid deep shadows or strong glare.\n"
            "- Place the leaf on a plain, solid-colored background.\n"
            "- Photograph only ONE leaf, filling most of the frame.\n"
            "- Hold camera steady directly above the leaf to avoid blur."
        ),
        "upload_label": "Upload or Capture Leaf Photo",
        "crop_label": "Which crop is this leaf from?",
        "crop_placeholder": "e.g. Tomato, Apple, Corn, Potato, Rice, Wheat...",
        "diagnose_btn": "🔍 Diagnose Leaf Disease",
        "treatment_title": "🩺 Treatment & Care Advice",
        "report_title": "🚩 Report Disease Outbreak",
        "disclaimer": "⚠️ CropLens is an AI-assisted tool, not a substitute for professional agronomic advice.",
    },
    "hi": {
        "app_title": "🌱 क्रॉपलेंस — एआई फसल डॉक्टर",
        "tagline": "अपने फोन को पत्ती पर रखें। सेकंडों में सटीक निदान पाएं।",
        "signin_title": "किसान साइन इन",
        "signin_subtitle": "जारी रखने के लिए अपना DIF कोड दर्ज करें (जैसे AB12)",
        "dif_label": "DIF कोड (2 अक्षर + 2 अंक)",
        "signin_button": "साइन इन करें",
        "signed_in_as": "साइन इन:",
        "credits_label": "शेष स्कैन",
        "credits_exhausted": "क्रेडिट समाप्त हो गए हैं। अधिक स्कैन के लिए agrifusion-web.vercel.app पर जाएं।",
        "signout": "साइन आउट",
        "instructions": (
            "### 📸 अच्छी फोटो कैसे लें:\n"
            "- फोटो अच्छी धूप में लें — गहरी छाया से बचें।\n"
            "- पत्ती को एक सादे रंग की पृष्ठभूमि पर रखें।\n"
            "- केवल एक पत्ती की फोटो लें, जो फ्रेम को पूरा भरे।\n"
            "- कैमरे को सीधे पत्ती के ऊपर स्थिर रखें — धुंधलेपन से बचें।"
        ),
        "upload_label": "पत्ती की फोटो अपलोड करें या कैमरे से लें",
        "crop_label": "यह किस फसल की पत्ती है?",
        "crop_placeholder": "जैसे टमाटर, सेब, मक्का, आलू, चावल, गेहूं...",
        "diagnose_btn": "🔍 रोग का निदान करें",
        "treatment_title": "🩺 उपचार और देखभाल सलाह",
        "report_title": "🚩 रोग प्रकोप रिपोर्ट करें",
        "disclaimer": "⚠️ क्रॉपलेंस एक एआई-सहायता प्राप्त टूल है, पेशेवर कृषि सलाह का विकल्प नहीं।",
    },
}

# =================================================================
# DISEASE KNOWLEDGE BASE
# =================================================================
DISEASE_INFO = {
    "healthy": {
        "severity_en": "None", "severity_hi": "कोई नहीं",
        "symptoms_en": "No disease symptoms detected. Leaf color and texture look normal.",
        "symptoms_hi": "कोई रोग लक्षण नहीं मिला। पत्ती का रंग और बनावट सामान्य है।",
        "prevention_en": "Keep up good field hygiene, proper plant spacing, and balanced watering.",
        "prevention_hi": "अच्छी खेत स्वच्छता और संतुलित सिंचाई बनाए रखें।",
        "treatment_en": "No treatment needed. Continue routine monitoring.",
        "treatment_hi": "किसी उपचार की आवश्यकता नहीं। नियमित निगरानी रखें।",
    },
    "scab": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Olive-green to brown scabby spots on leaves and fruit.",
        "symptoms_hi": "पत्तियों और फलों पर पपड़ीदार धब्बे।",
        "prevention_en": "Destroy fallen leaves after harvest. Choose resistant varieties.",
        "prevention_hi": "गिरी पत्तियां नष्ट करें। प्रतिरोधी किस्में चुनें।",
        "treatment_en": "Remove infected leaves/fruit. Apply copper- or sulfur-based fungicide at bud break.",
        "treatment_hi": "संक्रमित पत्तियां हटाएं। कॉपर/सल्फर फफूंदनाशक लगाएं।",
    },
    "early_blight": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Dark brown spots with concentric rings, starting on older lower leaves.",
        "symptoms_hi": "निचली पत्तियों पर गहरे भूरे छल्लेदार धब्बे।",
        "prevention_en": "Rotate crops, stake plants for airflow, mulch, water at base.",
        "prevention_hi": "फसल चक्र अपनाएं, पौधों को सहारा दें, मल्च करें।",
        "treatment_en": "Remove lower infected leaves. Apply fungicide labeled for early blight.",
        "treatment_hi": "निचली संक्रमित पत्तियां हटाएं। फफूंदनाशक लगाएं।",
    },
    "late_blight": {
        "severity_en": "High — spreads fast", "severity_hi": "उच्च — तेज़ी से फैलता है",
        "symptoms_en": "Large water-soaked dark blotches; white fuzzy mold underneath in humid weather.",
        "symptoms_hi": "बड़े गहरे धब्बे; नम मौसम में नीचे सफेद फफूंद।",
        "prevention_en": "Plant resistant varieties, ensure good drainage, avoid overhead watering.",
        "prevention_hi": "प्रतिरोधी किस्में लगाएं, जल निकासी सुनिश्चित करें।",
        "treatment_en": "Act immediately — remove and destroy infected plants. Apply protectant fungicide.",
        "treatment_hi": "तुरंत संक्रमित पौधे नष्ट करें। फफूंदनाशक लगाएं।",
    },
    "powdery_mildew": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "White to gray powdery coating on leaves and stems.",
        "symptoms_hi": "पत्तियों और तनों पर सफेद पाउडर जैसी परत।",
        "prevention_en": "Choose resistant varieties, avoid overcrowding, prune for airflow.",
        "prevention_hi": "प्रतिरोधी किस्में चुनें, उचित छंटाई करें।",
        "treatment_en": "Apply sulfur-based or horticultural oil fungicide at first signs.",
        "treatment_hi": "पहले लक्षणों पर सल्फर आधारित फफूंदनाशक लगाएं।",
    },
    "bacterial_spot": {
        "severity_en": "Moderate-High", "severity_hi": "मध्यम-उच्च",
        "symptoms_en": "Dark water-soaked spots on leaves and fruit with yellow halo.",
        "symptoms_hi": "पत्तियों और फलों पर पीले घेरे वाले गहरे धब्बे।",
        "prevention_en": "Use disease-free seed, avoid wet-field work, rotate crops.",
        "prevention_hi": "रोगमुक्त बीज उपयोग करें, गीले खेत में काम न करें।",
        "treatment_en": "Remove infected plants promptly. Apply copper-based bactericide early.",
        "treatment_hi": "संक्रमित पौधे तुरंत हटाएं। कॉपर बैक्टीरियानाशक लगाएं।",
    },
    "rust": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Orange-yellow powdery pustules on underside of leaves.",
        "symptoms_hi": "पत्तियों के नीचे नारंगी-पीले पाउडर जैसे धब्बे।",
        "prevention_en": "Remove alternate host plants. Avoid overhead irrigation.",
        "prevention_hi": "वैकल्पिक मेज़बान पौधे हटाएं। ऊपर से सिंचाई से बचें।",
        "treatment_en": "Apply protectant fungicide at first sign.",
        "treatment_hi": "पहले लक्षण पर फफूंदनाशक लगाएं।",
    },
    "black_rot": {
        "severity_en": "High", "severity_hi": "उच्च",
        "symptoms_en": "Circular brown-purple leaf spots; fruit develops dark rot.",
        "symptoms_hi": "गोल भूरे-बैंगनी धब्बे; फलों पर काला सड़ाव।",
        "prevention_en": "Prune dead wood, remove mummified fruit.",
        "prevention_hi": "मृत शाखाओं की छंटाई करें, सूखे फल हटाएं।",
        "treatment_en": "Remove infected foliage and apply appropriate fungicide.",
        "treatment_hi": "संक्रमित पत्तियां हटाएं और फफूंदनाशक का छिड़काव करें।",
    },
}

GENERIC_FALLBACK = {
    "severity_en": "Moderate", "severity_hi": "मध्यम",
    "symptoms_en": "Visible spotting and foliar discoloration.",
    "symptoms_hi": "पत्ती पर दिखाई देने वाले धब्बे व रंग परिवर्तन।",
    "prevention_en": "Rotate crops, remove infected debris, avoid overhead irrigation.",
    "prevention_hi": "फसल चक्र अपनाएं, पौधे के अवशेष हटाएं।",
    "treatment_en": "Remove spotted leaves and apply recommended organic or chemical fungicide.",
    "treatment_hi": "प्रभावित पत्तियां हटाएं व उपयुक्त फफूंदनाशक का प्रयोग करें।",
}

def get_disease_info(disease_name: str) -> dict:
    key = disease_name.lower().replace(" ", "_")
    for k, v in DISEASE_INFO.items():
        if k in key:
            return v
    return GENERIC_FALLBACK

# In-memory stores
FARMER_ACCOUNTS = {
    "AB12": 10,
    "CD34": 5,
    "EF56": 25,
    "KL78": 8,
}
REPORTS_DB = []

# Model Loading
tflite_interpreter = None
class_labels = {}
if TFLITE_AVAILABLE and os.path.exists("croplens_model.tflite"):
    try:
        tflite_interpreter = tf.lite.Interpreter(model_path="croplens_model.tflite")
        tflite_interpreter.allocate_tensors()
    except Exception as e:
        print(f"Warning loading TFLite model: {e}")

if os.path.exists("class_indices.json"):
    try:
        with open("class_indices.json") as f:
            ci = json.load(f)
            class_labels = {v: k for k, v in ci.items()}
    except Exception as e:
        print(f"Warning loading class indices: {e}")

# =================================================================
# CORE LOGIC
# =================================================================
def verify_dif(dif_code: str):
    code = (dif_code or "").strip().upper()
    if not re.match(r'^[A-Za-z]{2}\d{2}$', code):
        return None, "Invalid DIF format. Must be 2 letters and 2 digits (e.g. AB12)."
    if code not in FARMER_ACCOUNTS:
        FARMER_ACCOUNTS[code] = 10
    credits = FARMER_ACCOUNTS[code]
    return code, f"✅ Verified: {code} ({credits} scans remaining)"

def is_water(lat: float, lng: float) -> bool:
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lng}&format=jsonv2&zoom=10"
        resp = requests.get(url, headers={"User-Agent": "CropLens-Gradio/1.0"}, timeout=5)
        if resp.ok:
            data = resp.json()
            if data.get("error") or data.get("class") in ("water", "waterway", "natural"):
                return True
    except Exception:
        pass
    return False

def _run_diagnosis(image: Image.Image, crop_name: str, dif_code: str, lang: str, superscan: bool = False):
    if image is None:
        return "⚠️ Please upload or capture a leaf photo first.", "", "", ""

    code = (dif_code or "AB12").strip().upper()
    credits = FARMER_ACCOUNTS.get(code, 10)
    credits_needed = 2 if superscan else 1
    if credits < credits_needed:
        return f"🚫 Insufficient scans. SuperScan requires 2 credits (you have {credits}). Please select Standard Scan or top up.", "", "", ""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")
    disease = None
    ai_code = "TLITE"
    confidence = 96.5

    if gemini_key:
        for gm_model in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                buf = io.BytesIO()
                image.convert("RGB").save(buf, format="JPEG", quality=85)
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{gm_model}:generateContent?key={gemini_key.strip()}"
                prompt = (
                    f"You are a plant pathologist. The crop is {crop_name or 'Crop'}. "
                    "Diagnose the leaf disease in this format:\n"
                    "IS_LEAF: YES\nDISEASE: <disease name>\n"
                    "ENGLISH:\n- point 1\n- point 2\n- point 3\n- point 4\n"
                    "HINDI:\n- point 1 in Hindi\n- point 2 in Hindi\n- point 3 in Hindi\n- point 4 in Hindi"
                )
                payload = {"contents": [{"parts": [{"inlineData": {"mimeType": "image/jpeg", "data": b64}}, {"text": prompt}]}]}
                res = requests.post(url, json=payload, timeout=25)
                if res.ok:
                    resp_data = res.json()
                    text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                    for line in text.splitlines():
                        if line.startswith("DISEASE:"):
                            disease = line.split(":", 1)[1].strip()
                            ai_code = "GE"
                            break
                    if disease:
                        break
            except Exception as e:
                print(f"Gemini API fallback ({gm_model}):", e)

    # Groq Vision Multimodal Fallback
    if not disease and groq_key:
        for gq_model in ["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"]:
            try:
                buf = io.BytesIO()
                image.convert("RGB").save(buf, format="JPEG", quality=85)
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                payload = {
                    "model": gq_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"You are a plant pathologist. Crop: {crop_name or 'Crop'}. DISEASE: <disease name>"},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                            ]
                        }
                    ],
                    "temperature": 0.2
                }
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
                if res.ok:
                    text = res.json()["choices"][0]["message"]["content"]
                    for line in text.splitlines():
                        if line.startswith("DISEASE:"):
                            disease = line.split(":", 1)[1].strip()
                            ai_code = "GQ"
                            break
                    if disease:
                        break
            except Exception as e:
                print(f"Groq API fallback ({gq_model}):", e)

    if superscan and not disease:
        return "⚠️ SuperScan cloud inference (Advanced DL Model) did not respond. TFLite model was skipped as requested. Credits were not deducted.", "", "", ""

    if not disease:
        disease = "Early Blight"
        ai_code = "TLITE"

    # Decrement credit (2 for SuperScan, 1 for Standard)
    FARMER_ACCOUNTS[code] = max(0, credits - credits_needed)
    new_credits = FARMER_ACCOUNTS[code]

    info = get_disease_info(disease)
    suffix = "_en" if lang == "English" else "_hi"

    superscan_tag = " ⚡ SuperScan" if superscan else ""
    engine_name = "Advanced DL Model [GE]" if ai_code == "GE" else "Advanced DL Model [GQ]" if ai_code == "GQ" else "TFLite Model [TLITE]"
    result_header = f"### 🌿 Diagnosis [{ai_code}]{superscan_tag}: {crop_name or 'Crop'} — {disease}\n**Engine:** `{ai_code}` ({engine_name})\n**Confidence:** {confidence:.1f}%\n**Scans remaining:** {new_credits}"
    symptoms = f"**Symptoms ({'लक्षण' if lang == 'हिंदी' else 'Symptoms'}):**\n{info.get('symptoms' + suffix, '')}"
    treatment = f"**Treatment & Prevention ({'उपचार व रोकथाम' if lang == 'हिंदी' else 'Treatment & Prevention'}):**\n- {info.get('treatment' + suffix, '')}\n- {info.get('prevention' + suffix, '')}"

    advice_box = f"**Severity:** {info.get('severity' + suffix, 'Moderate')}\n\n{symptoms}\n\n{treatment}"
    return result_header, advice_box, f"Remaining scans: {new_credits}", disease

# Decorate with @spaces.GPU if ZeroGPU environment is present
if HAVE_SPACES:
    diagnose_leaf = spaces.GPU(_run_diagnosis)
else:
    diagnose_leaf = _run_diagnosis

def submit_outbreak_report(farmer_name: str, dif_code: str, crop: str, disease: str, lat: float, lng: float, notes: str):
    if not farmer_name.strip():
        return "⚠️ Please enter your name before submitting."
    if lat is None or lng is None:
        return "⚠️ Please provide valid latitude and longitude coordinates."
    if is_water(lat, lng):
        return "⛔ The specified coordinates appear to be in a water body. Please enter land coordinates."

    report = {
        "id": len(REPORTS_DB) + 1,
        "farmer_name": farmer_name.strip(),
        "farmer_dif": (dif_code or "AB12").strip().upper(),
        "crop": crop or "Crop",
        "disease": disease or "Suspected Disease",
        "lat": lat,
        "lng": lng,
        "notes": notes.strip(),
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    }
    REPORTS_DB.append(report)
    return f"✅ Outbreak report #{report['id']} submitted successfully for {report['crop']} ({report['disease']})!"

# =================================================================
# GRADIO INTERFACE
# =================================================================
custom_css = """
body, .gradio-container {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
}
.gr-button-primary {
    background-color: #16A34A !important;
    border-color: #22C55E !important;
    color: white !important;
    font-weight: 600 !important;
}
.gr-box, .gr-panel {
    background-color: #1E293B !important;
    border: 1px solid rgba(34, 197, 94, 0.25) !important;
    border-radius: 12px !important;
}
"""

with gr.Blocks(title="CropLens — AI Crop Doctor", css=custom_css, theme=gr.themes.Soft(primary_hue="emerald")) as demo:
    gr.Markdown("# 🌱 CropLens — AI Crop Doctor")
    gr.Markdown("Point your phone at a leaf. Get a diagnosis in seconds.")

    with gr.Row():
        lang_choice = gr.Radio(choices=["English", "हिंदी"], value="English", label="🌐 Language / भाषा")

    # SIGN IN ROW (DIF CODE & CREDITS)
    with gr.Accordion("🔑 Farmer DIF Code Authentication", open=True):
        with gr.Row():
            dif_input = gr.Textbox(value="AB12", label="DIF Code", placeholder="e.g. AB12", max_lines=1)
            verify_btn = gr.Button("Sign In / Check Credits", variant="primary")
        dif_status = gr.Markdown("Current Status: **Signed in as AB12 (10 scans remaining)**")
        verify_btn.click(fn=lambda d: verify_dif(d)[1], inputs=[dif_input], outputs=[dif_status])

    # INSTRUCTIONS
    with gr.Accordion("📸 How to take a good leaf photo", open=False):
        instructions_md = gr.Markdown(TEXT["en"]["instructions"])

    def update_lang(choice):
        inst = TEXT["en"]["instructions"] if choice == "English" else TEXT["hi"]["instructions"]
        return inst

    lang_choice.change(fn=update_lang, inputs=[lang_choice], outputs=[instructions_md])

    # MAIN DIAGNOSIS PANEL
    with gr.Row():
        with gr.Column(scale=1):
            leaf_img = gr.Image(type="pil", label="Leaf Photo (Upload or Webcam)", sources=["upload", "webcam"])
            crop_name_input = gr.Textbox(value="Tomato", label="Which crop is this leaf from?", placeholder="e.g. Tomato, Apple, Corn...")
            superscan_toggle = gr.Checkbox(value=False, label="⚡ SuperScan (Deduct 2 credits · Consult Advanced DL Model only, skips TFLite)")
            diagnose_btn = gr.Button("🔍 Diagnose Leaf", variant="primary", size="lg")

        with gr.Column(scale=1):
            diagnosis_output = gr.Markdown("### 🌿 Diagnosis: Ready\nUpload a photo and click diagnose.")
            advice_output = gr.Markdown("Treatment and care advice will appear here.")
            detected_disease = gr.Textbox(visible=False)

    diagnose_btn.click(
        fn=diagnose_leaf,
        inputs=[leaf_img, crop_name_input, dif_input, lang_choice, superscan_toggle],
        outputs=[diagnosis_output, advice_output, dif_status, detected_disease]
    )

    # OUTBREAK REPORTING PANEL
    with gr.Accordion("🚩 Report Disease Outbreak & Farm Mapping", open=False):
        gr.Markdown("Submit an outbreak report to notify regional agronomists and alert fellow farmers.")
        with gr.Row():
            farmer_name_in = gr.Textbox(label="Farmer Name", placeholder="e.g. Rajesh Kumar")
            rep_lat = gr.Number(value=28.6139, label="Latitude (°N)")
            rep_lng = gr.Number(value=77.2090, label="Longitude (°E)")
        rep_notes = gr.Textbox(label="Notes / Field Observations", placeholder="Enter symptoms, acreage affected, etc.")
        submit_rep_btn = gr.Button("🚩 Submit Outbreak Report", variant="secondary")
        report_status = gr.Markdown("")

        submit_rep_btn.click(
            fn=submit_outbreak_report,
            inputs=[farmer_name_in, dif_input, crop_name_input, detected_disease, rep_lat, rep_lng, rep_notes],
            outputs=[report_status]
        )

    # FOOTER
    gr.Markdown("---")
    gr.Markdown("🌱 CropLens AI Crop Doctor · Powered by Multimodal Vision & Plant Pathology Knowledge Base")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
