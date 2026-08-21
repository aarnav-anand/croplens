import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import base64
import io
import re
import requests
from datetime import datetime, timezone

import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

try:
    from supabase import create_client
    SUPABASE_SDK_AVAILABLE = True
except ImportError:
    SUPABASE_SDK_AVAILABLE = False

# =================================================================
# PAGE CONFIG
# =================================================================
st.set_page_config(
    page_title="CropLens - AI Crop Doctor",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =================================================================
# CSS
# =================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; font-size: 16px; }
    .block-container { padding-top: 1rem; padding-bottom: 3rem; max-width: 720px; }

    /* FIX 1: language toggle — compact, never wraps */
    div[data-testid="stRadio"] > div { flex-wrap: nowrap !important; gap: 0.4em !important; }
    div[data-testid="stRadio"] label { white-space: nowrap; font-size: 0.85em; }

    div.stButton > button {
        width: 100%; min-height: 2.8em; font-size: 1em;
        font-weight: 600; border-radius: 10px; transition: all 0.2s ease;
    }
    div[data-testid="stFileUploader"] section { border-radius: 12px; padding: 1.2em; }

    /* sign-in card — compact */
    .cl-signin-wrap {
        background: linear-gradient(135deg, rgba(34,197,94,0.08) 0%, rgba(16,185,129,0.05) 100%);
        border: 1.5px solid rgba(34,197,94,0.3);
        border-radius: 14px;
        padding: 0.6em 1.4em 0.8em;
        margin: 0.5em 0;
        text-align: center;
    }
    .cl-signin-wrap .cl-signin-icon { font-size: 1.3em; line-height: 1; margin-bottom: 0; }
    .cl-signin-wrap h3 { margin: 0.1em 0 0.05em; font-size: 1.05em; font-weight: 700; }
    .cl-signin-wrap p  { margin: 0; font-size: 0.83em; color: #6b7280; }

    /* FIX 3: collapse the gap between the card div and stMarkdown elements */
    .cl-card {
        background: linear-gradient(135deg, rgba(34,197,94,0.07) 0%, rgba(16,185,129,0.05) 100%);
        border: 1px solid rgba(34,197,94,0.25);
        border-radius: 14px;
        padding: 1em 1.3em;
        margin-bottom: 0.5em;
    }
    /* hide the stMarkdown wrappers that open/close the card so there's no white gap */
    .cl-card-inner { padding: 0; }

    .cl-card-warn {
        background: rgba(251,191,36,0.1);
        border: 1px solid rgba(245,158,11,0.35);
        border-radius: 12px; padding: 0.9em 1.2em; margin-bottom: 1em;
    }
    .cl-card-danger {
        background: rgba(239,68,68,0.09);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 12px; padding: 0.9em 1.2em; margin-bottom: 1em;
    }
    .cl-badge {
        display: inline-block;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.3);
        color: #166534;
        border-radius: 20px; padding: 0.15em 0.8em;
        font-size: 0.82em; font-weight: 600;
    }
    .cl-treatment-box {
        background: rgba(240,253,244,0.9);
        border-left: 4px solid #22c55e;
        border-radius: 0 10px 10px 0;
        padding: 0.8em 1em; margin: 0.4em 0;
        color: #166534;
    }

    .cl-instructions li { margin-bottom: 0.4em; line-height: 1.6em; }

    /* FIX 4 & 5: hide default camera widget, show only when toggled */
    .camera-section { margin-top: 0.5em; }

    /* diagnosis name */
    .cl-disease-name { font-size: 1.35em; font-weight: 700; margin: 0.2em 0 0.5em; }

    @media (max-width: 480px) {
        html, body, [class*="css"] { font-size: 15px; }
        .block-container { padding-left: 0.6rem; padding-right: 0.6rem; }
        .cl-signin-wrap { padding: 1.2em 0.9em; }
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# TRANSLATIONS
# =================================================================
TEXT = {
    "en": {
        "app_title": "🌱 CropLens",
        "app_subtitle": "AI Crop Doctor",
        "tagline": "Point your phone at a leaf. Get a diagnosis in seconds.",
        "signin_title": "Sign In",
        "signin_subtitle": "Enter your DIF Code to continue",
        "dif_label": "DIF Code",
        "dif_placeholder": "e.g. AB12",
        "dif_help": "2 letters + 2 digits (e.g. AB12)",
        "signin_button": "Sign In →",
        "dif_invalid_format": "Invalid format — must be 2 letters then 2 digits (e.g. AB12).",
        "dif_not_found": "DIF code not found. Please check and try again.",
        "dif_error": "Could not connect to server. Please try again.",
        "signed_in_as": "Signed in",
        "credits_label": "Scans remaining",
        "credits_exhausted_title": "Credits Exhausted",
        "credits_exhausted_body": "Purchase more scans at",
        "signout": "Sign out",
        "instructions_title": "📸 How to take a good photo",
        "instructions": [
            "Take the photo in good daylight — avoid deep shadows or strong glare.",
            "Place the leaf on a plain, solid-colored background.",
            "Photograph only ONE leaf, filling most of the frame.",
            "Hold the camera steady directly above the leaf — avoid blur.",
        ],
        "upload_label": "📁 Upload a leaf photo",
        "open_camera": "📷 Open Camera",
        "close_camera": "✕ Close Camera",
        "take_photo_btn": "✅ Use This Photo",
        "uploaded_caption": "Your photo",
        "diagnosing": "Analyzing your leaf...",
        "gemini_analyzing": "Low confidence — consulting Gemini AI...",
        "diagnosis_title": "Diagnosis",
        "confidence_label": "Confidence",
        "low_confidence_warning": "Low confidence — AI-assisted diagnosis shown below.",
        "ai_diagnosed_label": "AI-Identified Disease",
        "ai_no_result": "Could not identify the disease. Please retake the photo.",
        "treatment_title": "🩺 Treatment & Care Advice",
        "symptoms_label": "Symptoms",
        "prevention_label": "Prevention",
        "treatment_label": "Treatment",
        "severity_label": "Severity",
        "gemini_treatment_label": "AI-Generated Treatment Advice",
        "gemini_no_treatment": "No treatment advice available. Please consult your local agricultural officer.",
        "report_button": "🚩 Report Outbreak",
        "report_dialog_title": "Report Disease Outbreak",
        "report_instructions": "Draw your farm boundary using the polygon tool, or drop a marker. Then enter your name and submit.",
        "locate_me": "📍 Locate Me",
        "locate_me_help": "Zoom the map to your current GPS location.",
        "notes_label": "Notes (optional)",
        "farmer_name_label": "Your name",
        "farmer_name_req": "Please enter your name before submitting.",
        "submit_report": "Submit Report",
        "submitting": "Submitting...",
        "report_success": "✅ Report submitted. Thank you!",
        "report_error": "Could not submit report. Please try again.",
        "no_polygon_warning": "Please draw your farm boundary on the map first.",
        "config_missing": "Reporting not configured. Contact the app administrator.",
        "disclaimer": "⚠️ CropLens is an AI-assisted tool, not a substitute for professional agronomic advice.",
        "map_caption": "Use the polygon tool (□) on the map to mark your farm",
        "water_location_error": "⛔ The selected location appears to be in a water body (ocean, sea, or lake). Please draw your farm boundary on land.",
        "view_treatment": "🩺 View Treatment & Care Advice",
        "treatment_modal_title": "Treatment & Care Advice",
        "modal_lang_label": "View in",
        "close": "Close",
    },
    "hi": {
        "app_title": "🌱 क्रॉपलेंस",
        "app_subtitle": "एआई फसल डॉक्टर",
        "tagline": "अपने फोन को पत्ती पर रखें। सेकंडों में निदान पाएं।",
        "signin_title": "साइन इन",
        "signin_subtitle": "जारी रखने के लिए DIF कोड दर्ज करें",
        "dif_label": "DIF कोड",
        "dif_placeholder": "जैसे AB12",
        "dif_help": "2 अक्षर + 2 अंक (जैसे AB12)",
        "signin_button": "साइन इन करें →",
        "dif_invalid_format": "अमान्य फ़ॉर्मेट — 2 अक्षर फिर 2 अंक होने चाहिए (जैसे AB12)।",
        "dif_not_found": "DIF कोड नहीं मिला। कृपया जांचें।",
        "dif_error": "सर्वर से कनेक्ट नहीं हो सका।",
        "signed_in_as": "साइन इन:",
        "credits_label": "शेष स्कैन",
        "credits_exhausted_title": "क्रेडिट समाप्त",
        "credits_exhausted_body": "अधिक स्कैन खरीदें:",
        "signout": "साइन आउट",
        "instructions_title": "📸 अच्छी फोटो कैसे लें",
        "instructions": [
            "फोटो अच्छी धूप में लें — गहरी छाया से बचें।",
            "पत्ती को एक सादे रंग की पृष्ठभूमि पर रखें।",
            "केवल एक पत्ती की फोटो लें, जो फ्रेम भरे।",
            "कैमरे को स्थिर रखें, पत्ती के ऊपर से — धुंधलापन से बचें।",
        ],
        "upload_label": "📁 पत्ती की फोटो अपलोड करें",
        "open_camera": "📷 कैमरा खोलें",
        "close_camera": "✕ कैमरा बंद करें",
        "take_photo_btn": "✅ यह फोटो उपयोग करें",
        "uploaded_caption": "आपकी फोटो",
        "diagnosing": "आपकी पत्ती का विश्लेषण हो रहा है...",
        "gemini_analyzing": "कम विश्वसनीयता — Gemini AI से निदान लिया जा रहा है...",
        "diagnosis_title": "निदान",
        "confidence_label": "विश्वसनीयता",
        "low_confidence_warning": "कम विश्वसनीयता — एआई-सहायता प्राप्त निदान नीचे दिखाया गया है।",
        "ai_diagnosed_label": "एआई द्वारा पहचाना रोग",
        "ai_no_result": "रोग की पहचान नहीं हो सकी। फोटो दोबारा लें।",
        "treatment_title": "🩺 उपचार और देखभाल",
        "symptoms_label": "लक्षण",
        "prevention_label": "रोकथाम",
        "treatment_label": "उपचार",
        "severity_label": "गंभीरता",
        "gemini_treatment_label": "एआई-जनित उपचार सलाह",
        "gemini_no_treatment": "उपचार सलाह उपलब्ध नहीं। कृषि अधिकारी से संपर्क करें।",
        "report_button": "🚩 प्रकोप रिपोर्ट करें",
        "report_dialog_title": "रोग प्रकोप रिपोर्ट करें",
        "report_instructions": "पॉलीगॉन टूल से खेत की सीमा बनाएं या मार्कर लगाएं। नाम दर्ज कर सबमिट करें।",
        "locate_me": "📍 मुझे ढूंढें",
        "locate_me_help": "मानचित्र को आपकी GPS स्थिति पर ले जाएगा।",
        "notes_label": "नोट्स (वैकल्पिक)",
        "farmer_name_label": "आपका नाम",
        "farmer_name_req": "सबमिट करने से पहले नाम दर्ज करें।",
        "submit_report": "रिपोर्ट सबमिट करें",
        "submitting": "सबमिट हो रहा है...",
        "report_success": "✅ रिपोर्ट सबमिट हो गई। धन्यवाद!",
        "report_error": "रिपोर्ट सबमिट नहीं हो सकी।",
        "no_polygon_warning": "पहले मानचित्र पर खेत की सीमा बनाएं।",
        "config_missing": "रिपोर्टिंग सेट नहीं है।",
        "disclaimer": "⚠️ क्रॉपलेंस एक एआई-सहायता प्राप्त टूल है, पेशेवर कृषि सलाह का विकल्प नहीं।",
        "map_caption": "पॉलीगॉन टूल (□) से मानचित्र पर खेत चिह्नित करें",
        "water_location_error": "⛔ चुना गया स्थान जल क्षेत्र (समुद्र, सागर या झील) में प्रतीत होता है। कृपया खेत की सीमा ज़मीन पर बनाएं।",
        "view_treatment": "🩺 उपचार सलाह देखें",
        "treatment_modal_title": "उपचार और देखभाल सलाह",
        "modal_lang_label": "भाषा चुनें",
        "close": "बंद करें",
    },
}

# =================================================================
# DISEASE INFO
# =================================================================
DISEASE_INFO = {
    "healthy": {
        "severity_en": "None", "severity_hi": "कोई नहीं",
        "symptoms_en": "No disease symptoms detected. Leaf color and texture look normal.",
        "symptoms_hi": "कोई रोग लक्षण नहीं मिला।",
        "prevention_en": "Keep up good field hygiene, proper plant spacing, and balanced watering.",
        "prevention_hi": "अच्छी खेत स्वच्छता और संतुलित सिंचाई बनाए रखें।",
        "treatment_en": "No treatment needed. Continue routine monitoring.",
        "treatment_hi": "किसी उपचार की आवश्यकता नहीं।",
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
    "black_rot": {
        "severity_en": "High", "severity_hi": "उच्च",
        "symptoms_en": "Circular brown-purple leaf spots; fruit develops dark mummified rot.",
        "symptoms_hi": "गोल भूरे-बैंगनी धब्बे; फल पर गहरे रंग का सड़ाव।",
        "prevention_en": "Prune dead wood in dormant season. Remove mummified fruit.",
        "prevention_hi": "मृत शाखाओं की छंटाई करें। सूखे फल हटाएं।",
        "treatment_en": "Remove infected material. Apply fungicide for black rot during wet periods.",
        "treatment_hi": "संक्रमित हिस्से हटाएं। नम मौसम में फफूंदनाशक लगाएं।",
    },
    "rust": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Orange-yellow powdery pustules on the underside of leaves.",
        "symptoms_hi": "पत्तियों के नीचे नारंगी-पीले पाउडर जैसे धब्बे।",
        "prevention_en": "Remove alternate host plants. Avoid overhead irrigation.",
        "prevention_hi": "वैकल्पिक मेज़बान पौधे हटाएं। ऊपर से सिंचाई से बचें।",
        "treatment_en": "Apply protectant fungicide at first sign and repeat through humid season.",
        "treatment_hi": "पहले लक्षण पर फफूंदनाशक लगाएं और नम मौसम में दोहराएं।",
    },
    "powdery_mildew": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "White to gray powdery coating on leaves and stems.",
        "symptoms_hi": "पत्तियों और तनों पर सफेद पाउडर जैसी परत।",
        "prevention_en": "Choose resistant varieties, avoid overcrowding, prune for airflow.",
        "prevention_hi": "प्रतिरोधी किस्में चुनें, छंटाई करें।",
        "treatment_en": "Apply sulfur-based or horticultural oil fungicide at first signs.",
        "treatment_hi": "पहले लक्षणों पर सल्फर आधारित फफूंदनाशक लगाएं।",
    },
    "leaf_blight": {
        "severity_en": "Moderate-High", "severity_hi": "मध्यम-उच्च",
        "symptoms_en": "Irregular brown lesions expanding from leaf edges or tips.",
        "symptoms_hi": "पत्ती के किनारों से फैलते भूरे घाव।",
        "prevention_en": "Rotate crops, remove crop debris, avoid overhead watering.",
        "prevention_hi": "फसल चक्र अपनाएं, अवशेष हटाएं।",
        "treatment_en": "Remove affected foliage. Apply fungicide labeled for leaf blight.",
        "treatment_hi": "प्रभावित पत्तियां हटाएं। फफूंदनाशक लगाएं।",
    },
    "leaf_spot": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Small gray-to-brown spots with defined edges, sometimes with a yellow halo.",
        "symptoms_hi": "स्पष्ट किनारों वाले छोटे भूरे धब्बे।",
        "prevention_en": "Rotate crops, remove debris, water at base.",
        "prevention_hi": "फसल चक्र अपनाएं, पौधे के आधार पर पानी दें।",
        "treatment_en": "Remove spotted leaves. Use fungicide labeled for leaf spot.",
        "treatment_hi": "धब्बेदार पत्तियां हटाएं। फफूंदनाशक लगाएं।",
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
    "early_blight": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Dark brown spots with concentric rings, starting on older lower leaves.",
        "symptoms_hi": "निचली पत्तियों पर गहरे भूरे छल्लेदार धब्बे।",
        "prevention_en": "Rotate crops, stake plants for airflow, mulch, water at base.",
        "prevention_hi": "फसल चक्र अपनाएं, पौधों को सहारा दें, मल्च करें।",
        "treatment_en": "Remove lower infected leaves. Apply fungicide for early blight.",
        "treatment_hi": "निचली संक्रमित पत्तियां हटाएं। फफूंदनाशक लगाएं।",
    },
    "late_blight": {
        "severity_en": "High — spreads fast", "severity_hi": "उच्च — तेज़ी से फैलता है",
        "symptoms_en": "Large water-soaked dark blotches; white fuzzy mold underneath in humid weather.",
        "symptoms_hi": "बड़े गहरे धब्बे; नम मौसम में नीचे सफेद फफूंद।",
        "prevention_en": "Plant resistant varieties, ensure good drainage, avoid overhead watering.",
        "prevention_hi": "प्रतिरोधी किस्में लगाएं, अच्छी जल निकासी सुनिश्चित करें।",
        "treatment_en": "Act immediately — remove and destroy infected plants. Apply fungicide. Contact extension office.",
        "treatment_hi": "तुरंत संक्रमित पौधे नष्ट करें। कृषि विस्तार कार्यालय से संपर्क करें।",
    },
    "leaf_mold": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Pale patches on upper surface; olive-green velvety mold underneath.",
        "symptoms_hi": "ऊपर हल्के धब्बे; नीचे मखमली फफूंद।",
        "prevention_en": "Improve ventilation, reduce humidity, avoid overhead watering.",
        "prevention_hi": "हवा का प्रवाह बेहतर बनाएं, नमी कम करें।",
        "treatment_en": "Remove affected leaves and improve airflow. Use fungicide if needed.",
        "treatment_hi": "प्रभावित पत्तियां हटाएं। फफूंदनाशक लगाएं।",
    },
    "spider_mites": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Tiny yellow/white speckling on leaves, fine webbing underneath.",
        "symptoms_hi": "पत्तियों पर छोटे पीले/सफेद धब्बे, नीचे बारीक जाला।",
        "prevention_en": "Keep plants well-watered, encourage natural predators.",
        "prevention_hi": "पौधों को अच्छी तरह सिंचित रखें।",
        "treatment_en": "Spray undersides with water. Use insecticidal soap or miticide.",
        "treatment_hi": "पत्तियों के नीचे पानी छिड़कें। कीटनाशी साबुन लगाएं।",
    },
    "target_spot": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Brown lesions with concentric rings (target-like) on leaves and stems.",
        "symptoms_hi": "पत्तियों पर संकेंद्रित छल्लों वाले भूरे घाव।",
        "prevention_en": "Rotate crops, remove plant debris, avoid dense planting.",
        "prevention_hi": "फसल चक्र अपनाएं, अवशेष हटाएं।",
        "treatment_en": "Remove infected leaves. Apply fungicide for target spot.",
        "treatment_hi": "संक्रमित पत्तियां हटाएं। फफूंदनाशक लगाएं।",
    },
    "yellow_leaf_curl_virus": {
        "severity_en": "High — no cure, manage vector", "severity_hi": "उच्च — कोई इलाज नहीं",
        "symptoms_en": "Upward-curling yellow leaves, stunted growth. Spread by whiteflies.",
        "symptoms_hi": "पत्तियां ऊपर मुड़कर पीली, बौनी वृद्धि। सफेद मक्खी से फैलता है।",
        "prevention_en": "Use insect-proof screens, plant certified virus-free seedlings.",
        "prevention_hi": "कीट-रोधी जाल लगाएं, प्रमाणित पौध लगाएं।",
        "treatment_en": "No cure. Remove infected plants. Control whitefly with insecticide.",
        "treatment_hi": "कोई इलाज नहीं। संक्रमित पौधे हटाएं। सफेद मक्खी नियंत्रित करें।",
    },
    "mosaic_virus": {
        "severity_en": "High — no cure", "severity_hi": "उच्च — कोई इलाज नहीं",
        "symptoms_en": "Mottled yellow-green mosaic pattern on leaves, distortion, stunted growth.",
        "symptoms_hi": "पत्तियों पर पीले-हरे मोज़ेक पैटर्न और विकृति।",
        "prevention_en": "Use virus-free seed, control aphid populations.",
        "prevention_hi": "वायरस-मुक्त बीज उपयोग करें, एफिड नियंत्रित करें।",
        "treatment_en": "No cure. Remove and destroy infected plants to prevent spread.",
        "treatment_hi": "कोई इलाज नहीं। संक्रमित पौधे नष्ट करें।",
    },
    "citrus_greening": {
        "severity_en": "Very High — fatal to trees", "severity_hi": "बहुत उच्च — घातक",
        "symptoms_en": "Blotchy asymmetric yellow mottling; small lopsided bitter fruit.",
        "symptoms_hi": "असममित पीला धब्बेदार पैटर्न; छोटे टेढ़े फल।",
        "prevention_en": "Use certified disease-free planting material, control psyllid vector.",
        "prevention_hi": "प्रमाणित रोगमुक्त पौध सामग्री उपयोग करें।",
        "treatment_en": "No cure. Remove infected trees. Consult agricultural department immediately.",
        "treatment_hi": "कोई इलाज नहीं। संक्रमित पेड़ हटाएं। कृषि विभाग से संपर्क करें।",
    },
    "esca": {
        "severity_en": "High", "severity_hi": "उच्च",
        "symptoms_en": "Tiger-stripe yellowing between leaf veins; sudden vine collapse in summer.",
        "symptoms_hi": "पत्ती की नसों के बीच धारीदार पैटर्न; गर्मियों में पौधे का मुरझाना।",
        "prevention_en": "Avoid large pruning wounds; seal cuts. Remove infected wood.",
        "prevention_hi": "बड़े छंटाई घावों से बचें। संक्रमित लकड़ी नष्ट करें।",
        "treatment_en": "No effective chemical cure. Remove infected vines. Consult specialist.",
        "treatment_hi": "कोई प्रभावी इलाज नहीं। विशेषज्ञ से संपर्क करें।",
    },
    "leaf_scorch": {
        "severity_en": "Moderate", "severity_hi": "मध्यम",
        "symptoms_en": "Purple-to-brown spots on leaves; edges drying and curling.",
        "symptoms_hi": "पत्तियों पर बैंगनी-भूरे धब्बे; किनारे सूखकर मुड़ना।",
        "prevention_en": "Remove old infected leaves after harvest, ensure good drainage.",
        "prevention_hi": "पुरानी संक्रमित पत्तियां हटाएं, जल निकासी सुनिश्चित करें।",
        "treatment_en": "Remove infected leaves. Apply fungicide labeled for leaf scorch.",
        "treatment_hi": "संक्रमित पत्तियां नष्ट करें। फफूंदनाशक लगाएं।",
    },
}

GENERIC_FALLBACK = {
    "severity_en": "Unknown", "severity_hi": "अज्ञात",
    "symptoms_en": "Visible discoloration or spotting detected on the leaf.",
    "symptoms_hi": "पत्ती पर दिखाई देने वाला रंग बदलना या धब्बे।",
    "prevention_en": "Practice crop rotation, remove plant debris, avoid overhead watering.",
    "prevention_hi": "फसल चक्र अपनाएं, पौधे के अवशेष हटाएं।",
    "treatment_en": "Contact your local agricultural extension officer for a targeted treatment plan.",
    "treatment_hi": "स्थानीय कृषि विस्तार अधिकारी से संपर्क करें।",
}

CATEGORY_KEYWORDS = [
    ("healthy", "healthy"), ("scab", "scab"), ("black_rot", "black_rot"),
    ("rust", "rust"), ("powdery_mildew", "powdery_mildew"),
    ("leaf_blight", "leaf_blight"), ("northern_leaf_blight", "leaf_blight"),
    ("gray_leaf_spot", "leaf_spot"), ("cercospora", "leaf_spot"), ("septoria", "leaf_spot"),
    ("bacterial_spot", "bacterial_spot"), ("early_blight", "early_blight"),
    ("late_blight", "late_blight"), ("leaf_mold", "leaf_mold"),
    ("spider_mite", "spider_mites"), ("target_spot", "target_spot"),
    ("yellow_leaf_curl", "yellow_leaf_curl_virus"), ("mosaic_virus", "mosaic_virus"),
    ("haunglongbing", "citrus_greening"), ("citrus_greening", "citrus_greening"),
    ("esca", "esca"), ("leaf_scorch", "leaf_scorch"),
]


def get_disease_info(raw_class_name: str) -> dict:
    key = raw_class_name.lower()
    for substring, category in CATEGORY_KEYWORDS:
        if substring in key:
            return DISEASE_INFO[category]
    return GENERIC_FALLBACK


def format_class_name(raw_class_name: str) -> tuple:
    parts = raw_class_name.split("___")
    crop = parts[0].replace("_", " ").strip()
    disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else ""
    return crop, disease


# =================================================================
# WATER BODY DETECTION
# Uses Nominatim reverse-geocoding (OpenStreetMap) to check whether
# a lat/lng point falls on a water body (ocean, sea, lake, river …).
# Returns True  → the point is in water (reject it).
# Returns False → the point is on land (allow it).
# Returns None  → the check could not be completed (allow with caution).
# =================================================================
def is_location_in_water(lat: float, lng: float) -> bool | None:
    """
    Query Nominatim reverse-geocode API.  When the coordinate is over open
    water Nominatim either returns no address at all or returns a place whose
    'type' / 'class' is a water-related OSM tag.  We treat both cases as water.
    """
    water_classes = {"water", "waterway", "natural"}
    water_types   = {
        "water", "sea", "ocean", "bay", "lake", "river", "stream",
        "canal", "reservoir", "pond", "wetland", "coastline",
    }
    try:
        url = (
            "https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat}&lon={lng}&format=jsonv2&zoom=10"
        )
        resp = requests.get(
            url,
            headers={"User-Agent": "CropLens/1.0 (crop disease reporting app)"},
            timeout=6,
        )
        if resp.status_code != 200:
            return None  # can't determine — let it through

        data = resp.json()

        # Nominatim returns {"error": "Unable to geocode"} for open-ocean points
        if "error" in data:
            return True

        osm_class = data.get("class", "")
        osm_type  = data.get("type", "")
        category  = data.get("category", "")

        if osm_class in water_classes or osm_type in water_types or category in water_classes:
            return True

        # Secondary check: if the display_name contains only water-related terms
        # and there is no meaningful address (no road, suburb, city, country …)
        address = data.get("address", {})
        land_keys = {
            "road", "suburb", "village", "town", "city", "state",
            "country", "county", "district", "neighbourhood",
        }
        if not any(k in address for k in land_keys):
            # No land address at all → treat as water
            return True

        return False

    except Exception:
        return None  # network error — allow with caution


# =================================================================
# SESSION STATE
# =================================================================
defaults = {
    "lang": "en",
    "map_polygon": None,
    "last_diagnosis": None,
    "show_report": False,
    "show_treatment": False,
    "farmer_dif": None,
    "farmer_credits": None,
    "credits_exhausted": False,
    "gemini_disease": None,
    "gemini_treatment_en": None,
    "gemini_treatment_hi": None,
    "last_image_hash": None,
    "show_camera": False,
    "pending_camera_img": None,
    "crop_input": None,            # crop name entered by user for low-confidence scans
    "ai_crop_confirmed": False,    # True once user has submitted crop name
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =================================================================
# SUPABASE & MODEL
# =================================================================
@st.cache_resource
def get_supabase_client():
    if not SUPABASE_SDK_AVAILABLE:
        return None
    try:
        return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    except Exception:
        return None

@st.cache_resource
def load_model():
    interp = tf.lite.Interpreter(model_path="croplens_model.tflite")
    interp.allocate_tensors()
    return interp

@st.cache_resource
def load_labels():
    with open("class_indices.json") as f:
        ci = json.load(f)
    return {v: k for k, v in ci.items()}

supabase = get_supabase_client()
interpreter = load_model()
labels = load_labels()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
IMG_SIZE = input_details[0]["shape"][1]

# =================================================================
# HELPERS
# =================================================================
DIF_PATTERN = re.compile(r'^[A-Za-z]{2}\d{2}$')

def validate_dif_format(code: str) -> bool:
    return bool(DIF_PATTERN.match(code.strip()))

def lookup_farmer(dif_code: str):
    if supabase is None:
        return None, "no_supabase"
    try:
        result = supabase.table("farmers").select("croplens").eq("dif_code", dif_code.upper()).execute()
        if result.data:
            return result.data[0]["croplens"], None
        return None, "not_found"
    except Exception as e:
        return None, str(e)

def decrement_credits(dif_code: str, current: int):
    new_val = max(current - 1, 0)
    try:
        supabase.table("farmers").update({"croplens": new_val}).eq("dif_code", dif_code.upper()).execute()
        return new_val
    except Exception:
        return None

def image_to_base64(pil_image: Image.Image) -> str:
    buf = io.BytesIO()
    pil_image.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def gemini_analyse(pil_image: Image.Image, gemini_key: str, crop_name: str = ""):
    """Single Gemini call: leaf check + disease diagnosis + treatment in both languages.
    crop_name is provided by the farmer before this call is made.
    Returns dict: is_leaf, disease, en_points, hi_points, error.
    """
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-3.5-flash:generateContent?key={gemini_key}"
    )
    b64 = image_to_base64(pil_image)
    crop_ctx = f"The farmer says this is a {crop_name} leaf. " if crop_name else ""
    prompt = (
        f"You are an expert plant pathologist and agricultural advisor.\n"
        f"{crop_ctx}"
        "Look at this image and respond using EXACTLY the format below — "
        "no extra text, no markdown, no explanation outside the format.\n\n"
        "IS_LEAF: YES or NO\n\n"
        "If IS_LEAF is NO, stop there. Write nothing else.\n\n"
        "If IS_LEAF is YES, continue:\n\n"
        "DISEASE: <disease name in 2-4 words, e.g. Early Blight, Apple Scab, Powdery Mildew. "
        "If healthy write: Healthy. NEVER write Unknown — always commit to your best diagnosis.>\n\n"
        "ENGLISH:\n"
        "- <treatment point 1>\n"
        "- <treatment point 2>\n"
        "- <treatment point 3>\n"
        "- <treatment point 4>\n\n"
        "HINDI:\n"
        "- <treatment point 1 in Hindi>\n"
        "- <treatment point 2 in Hindi>\n"
        "- <treatment point 3 in Hindi>\n"
        "- <treatment point 4 in Hindi>\n\n"
        "RULES:\n"
        "- Disease name must be 2-4 words maximum.\n"
        "- All 4 treatment points are mandatory in both languages.\n"
        "- If unsure, commit to the most likely disease based on visible symptoms.\n"
        "- Do not add any text outside this format."
    )
    payload = {"contents": [{"parts": [
        {"inlineData": {"mimeType": "image/jpeg", "data": b64}},
        {"text": prompt}
    ]}]}

    try:
        resp = requests.post(url, json=payload, timeout=45)
        resp.raise_for_status()

        # Gemini can return HTTP 200 without a usable response.
        # Treat that as a failed scan so it cannot consume a credit.
        response_json = resp.json()
        candidates = response_json.get("candidates") or []
        if not candidates:
            raise RuntimeError("Gemini returned no candidates.")

        parts = (candidates[0].get("content") or {}).get("parts") or []
        text_parts = [
            p.get("text", "").strip()
            for p in parts
            if isinstance(p, dict) and p.get("text")
        ]
        text = "\n".join(text_parts).strip()

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        # ── Parse response ──
        is_leaf = True
        disease = None
        en_points, hi_points = [], []
        current = None

        for line in text.splitlines():
            l = line.strip()
            if l.upper().startswith("IS_LEAF:"):
                val = l.split(":", 1)[1].strip().upper()
                is_leaf = val.startswith("Y")
            elif l.upper().startswith("DISEASE:"):
                disease = l.split(":", 1)[1].strip()
            elif l.upper().startswith("ENGLISH"):
                current = "en"
            elif l.upper().startswith("HINDI"):
                current = "hi"
            elif l and l[0] in "-•*":
                clean = l.lstrip("-•* ").strip()
                if clean:
                    if current == "en":
                        en_points.append(clean)
                    elif current == "hi":
                        hi_points.append(clean)
            elif l and len(l) > 2 and l[0].isdigit() and l[1] in ".):":
                clean = l[2:].strip()
                if clean:
                    if current == "en":
                        en_points.append(clean)
                    elif current == "hi":
                        hi_points.append(clean)

        # A successful leaf diagnosis must contain the fields that the UI
        # actually displays. Otherwise treat it as a failed scan.
        if is_leaf and (not disease or not en_points or not hi_points):
            raise RuntimeError("Gemini returned an incomplete diagnosis.")

        return {
            "is_leaf":   is_leaf,
            "disease":   disease,
            "en_points": en_points or None,
            "hi_points": hi_points or None,
            "error":     None,
        }

    except Exception as e:
        return {
            "is_leaf":   True,   # fail open
            "disease":   None,
            "en_points": None,
            "hi_points": None,
            "error":     str(e),
        }


def get_gemini_key():
    try:
        return st.secrets["gemini"]["api_key"]
    except Exception:
        return None

# =================================================================
# HEADER — language toggle first, then header uses updated T
# =================================================================

# T must be set before anything renders — initialise from session state
T = TEXT[st.session_state.lang]

# Language toggle on its own row so it is never clipped
choice = st.radio(
    "🌐 Language / भाषा",
    options=["en", "hi"],
    format_func=lambda x: "English" if x == "en" else "हिंदी",
    horizontal=True,
    index=0 if st.session_state.lang == "en" else 1,
    key="lang_selector",
)
# Update both session state and T immediately after the widget
st.session_state.lang = choice
T = TEXT[st.session_state.lang]

st.markdown(f"## {T['app_title']}")
st.caption(f"{T['app_subtitle']}  ·  {T['tagline']}")
st.divider()

# =================================================================
# SIGN-IN GATE
# =================================================================
if st.session_state.farmer_dif is None:
    # FIX 2: smaller, tighter sign-in card
    st.markdown(f"""
    <div class="cl-signin-wrap">
        <div class="cl-signin-icon">🌾</div>
        <h3>{T["signin_title"]}</h3>
        <p>{T["signin_subtitle"]}</p>
    </div>
    """, unsafe_allow_html=True)

    dif_input = st.text_input(
        T["dif_label"],
        placeholder=T["dif_placeholder"],
        help=T["dif_help"],
        max_chars=4,
    ).strip().upper()

    if st.button(T["signin_button"], type="primary"):
        if not dif_input:
            st.warning(T["dif_help"])
        elif not validate_dif_format(dif_input):
            st.error(T["dif_invalid_format"])
        else:
            with st.spinner("Checking..."):
                credits, err = lookup_farmer(dif_input)
            if err == "not_found":
                st.error(T["dif_not_found"])
            elif err is not None and err != "no_supabase":
                st.error(T["dif_error"])
            else:
                st.session_state.farmer_dif = dif_input
                st.session_state.farmer_credits = credits
                st.rerun()
    st.stop()

# =================================================================
# SIGNED-IN HEADER BAR
# FIX 8: credits come directly from session state which is updated
#         immediately after each scan decrement — no refresh needed
# =================================================================
bar_col1, bar_col2, bar_col3 = st.columns([3, 3, 1])
with bar_col1:
    st.markdown(f'<span class="cl-badge">✅ {T["signed_in_as"]}: {st.session_state.farmer_dif}</span>', unsafe_allow_html=True)
with bar_col2:
    if st.session_state.farmer_credits is not None:
        c = st.session_state.farmer_credits
        clr = "#22c55e" if c > 5 else ("#f59e0b" if c > 2 else "#ef4444")
        st.markdown(
            f'<div style="background:{clr};color:white;border-radius:8px;'
            f'padding:0.3em 0.8em;font-weight:700;text-align:center;font-size:0.88em;">'
            f'🔬 {T["credits_label"]}: {c}</div>',
            unsafe_allow_html=True
        )
with bar_col3:
    if st.button("↩", help=T["signout"]):
        for k in ["farmer_dif","farmer_credits","credits_exhausted","last_diagnosis",
                  "gemini_disease","gemini_treatment_en","gemini_treatment_hi",
                  "last_image_hash","show_camera","pending_camera_img"]:
            st.session_state[k] = None if k not in ("credits_exhausted","show_camera") else False
        st.rerun()

st.markdown("")

if st.session_state.credits_exhausted:
    st.error(f"### 🚫 {T['credits_exhausted_title']}\n\n{T['credits_exhausted_body']} **[agrifusion-web.vercel.app](https://agrifusion-web.vercel.app)**")
    st.stop()

# =================================================================
# FIX 3: INSTRUCTIONS CARD — single st.markdown, no wrapper gap
# =================================================================
tips_html = "".join(f"<li>{tip}</li>" for tip in T["instructions"])
st.markdown(
    f'<div class="cl-card"><b>{T["instructions_title"]}</b>'
    f'<ul class="cl-instructions" style="margin:0.5em 0 0;">{tips_html}</ul></div>',
    unsafe_allow_html=True
)

# =================================================================
# IMAGE INPUT
# FIX 4: Camera is off by default; toggled with a button.
# FIX 5: Camera shows a "Use This Photo" submit button after capture.
# =================================================================
uploaded_file = st.file_uploader(T["upload_label"], type=["jpg", "jpeg", "png"])

# Camera toggle button
cam_label = T["close_camera"] if st.session_state.show_camera else T["open_camera"]
if st.button(cam_label, key="cam_toggle"):
    st.session_state.show_camera = not st.session_state.show_camera
    st.session_state.pending_camera_img = None
    st.rerun()

camera_file = None
if st.session_state.show_camera:
    raw_cam = st.camera_input("", label_visibility="collapsed", key="camera_widget")
    if raw_cam is not None:
        # Show preview + submit button
        prev_col, btn_col = st.columns([3, 1])
        with prev_col:
            st.image(raw_cam, width=480)
        with btn_col:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(T["take_photo_btn"], type="primary", key="confirm_photo"):
                st.session_state.pending_camera_img = raw_cam.getvalue()
                st.session_state.show_camera = False
                st.rerun()

# Resolve final image source
if st.session_state.pending_camera_img:
    image_bytes_final = st.session_state.pending_camera_img
    image_source_label = "camera"
elif uploaded_file:
    image_bytes_final = uploaded_file.getvalue()
    image_source_label = "upload"
else:
    image_bytes_final = None
    image_source_label = None

# =================================================================
# DIAGNOSIS
# =================================================================
CONTACT_MSG_EN = "Model not responding. Please contact vajashivam8@gmail.com / 9321379188"
CONTACT_MSG_HI = "मॉडल प्रतिक्रिया नहीं दे रहा। कृपया संपर्क करें: vajashivam8@gmail.com / 9321379188"
APP_FAIL_EN = "Application failed. Please contact codecraftchampions/9321379188 for assistance"
APP_FAIL_HI = "एप्लिकेशन विफल हुआ। कृपया सहायता के लिए codecraftchampions/9321379188 पर संपर्क करें।"
CONFIDENCE_THRESHOLD = 95

if image_bytes_final:
    img_hash = hash(image_bytes_final)
    try:
        image = Image.open(io.BytesIO(image_bytes_final)).convert("RGB")
    except Exception:
        st.error("Could not read the image. Please try uploading again.")
        image_bytes_final = None
        st.stop()
    st.image(image, caption=T["uploaded_caption"], width=680)

    # New image — reset all diagnosis state, wait for crop name
    if img_hash != st.session_state.last_image_hash:
        if st.session_state.farmer_credits is not None and st.session_state.farmer_credits <= 0:
            st.session_state.credits_exhausted = True
            st.rerun()
        st.session_state.last_diagnosis      = None
        st.session_state.gemini_disease      = None
        st.session_state.gemini_treatment_en = None
        st.session_state.gemini_treatment_hi = None
        st.session_state.ai_crop_confirmed   = False
        st.session_state.crop_input          = None
        st.session_state.last_image_hash     = img_hash

    # ── STEP 1: Ask crop name before doing anything ──
    if not st.session_state.ai_crop_confirmed:
        lang = st.session_state.lang
        crop_label       = "Which crop is this leaf from?" if lang == "en" else "यह किस फसल की पत्ती है?"
        crop_placeholder = "e.g. Tomato, Wheat, Rice..." if lang == "en" else "जैसे टमाटर, गेहूं, चावल..."
        crop_btn         = "Analyse →" if lang == "en" else "विश्लेषण करें →"
        st.info(crop_label)

        # Use st.form to avoid SessionInfo / rerun conflicts from manual st.rerun() inside callbacks
        with st.form(key="crop_form"):
            crop_val = st.text_input(crop_label, placeholder=crop_placeholder,
                                     label_visibility="collapsed")
            submitted = st.form_submit_button(crop_btn, type="primary")

        if submitted:
            if crop_val.strip():
                st.session_state.crop_input = crop_val.strip()
                gkey = get_gemini_key()

                # ── STEP 2: Single Gemini call (leaf + disease + treatment) ──
                ai = None
                if gkey:
                    spin_msg = "Analysing your photo..." if lang == "en" else "फोटो का विश्लेषण हो रहा है..."
                    with st.spinner(spin_msg):
                        ai = gemini_analyse(image, gkey, crop_val.strip())

                is_leaf    = ai["is_leaf"]   if ai else True
                ai_err     = ai["error"]     if ai else "No API key configured"
                ai_disease = ai["disease"]   if ai else None
                ai_en      = ai["en_points"] if ai else None
                ai_hi      = ai["hi_points"] if ai else None

                # ── STEP 3: Run TFLite only if it's a leaf ──
                confidence, raw_class, crop_name_m, disease_name_m, info = 0, None, "", "", None
                if is_leaf:
                    img_r = image.resize((IMG_SIZE, IMG_SIZE))
                    arr   = np.array(img_r).astype(np.float32) / 255.0
                    arr   = np.expand_dims(arr, 0)
                    interpreter.set_tensor(input_details[0]["index"], arr)
                    interpreter.invoke()
                    output     = interpreter.get_tensor(output_details[0]["index"])[0]
                    top_idx    = int(np.argmax(output))
                    confidence = float(output[top_idx]) * 100
                    raw_class  = labels[top_idx]
                    crop_name_m, disease_name_m = format_class_name(raw_class)
                    info       = get_disease_info(raw_class)

                # ── Store all results ──
                st.session_state.last_diagnosis = {
                    "is_leaf":    is_leaf,
                    "ai_err":     ai_err,
                    "confidence": confidence,
                    "raw_class":  raw_class,
                    "crop":       crop_name_m,
                    "disease":    disease_name_m,
                    "info":       info,
                }
                st.session_state.gemini_disease      = ai_disease
                st.session_state.gemini_treatment_en = ai_en
                st.session_state.gemini_treatment_hi = ai_hi

                # ── Decrement credit ONLY if a result will actually be shown ──
                # The rerun below guarantees that this stored result/error is
                # rendered before the user sees the completed scan.
                #
                # Gemini failure = failed scan: show the error and DO NOT
                # charge the farmer, regardless of what TFLite produced.
                gemini_success = (
                    is_leaf
                    and not ai_err
                    and bool(ai_disease)
                    and bool(ai_en)
                    and bool(ai_hi)
                )
                tflite_success = is_leaf and confidence >= CONFIDENCE_THRESHOLD

                if ai_err:
                    # The Gemini request itself failed — never charge the
                    # farmer for this scan, even if the TFLite model produced
                    # a high-confidence result on its own.
                    scan_success = False
                else:
                    scan_success = gemini_success or tflite_success

                if scan_success and st.session_state.farmer_credits is not None and supabase is not None:
                    new_c = decrement_credits(
                        st.session_state.farmer_dif,
                        st.session_state.farmer_credits
                    )
                    if new_c is not None:
                        st.session_state.farmer_credits = new_c

                if st.session_state.farmer_credits is not None and st.session_state.farmer_credits <= 0:
                    st.session_state.credits_exhausted = True

                # Mark as confirmed, then immediately rerun so the result
                # (or the Gemini error) is actually rendered.
                #
                # Without this rerun Streamlit finishes the button-click run
                # immediately after the API call. That was why the credit could
                # decrease while the user saw no result.
                st.session_state.ai_crop_confirmed = True
                st.rerun()
            else:
                st.warning("Please enter the crop name." if lang == "en"
                           else "कृपया फसल का नाम दर्ज करें।")

    # ── DISPLAY (only after crop name submitted and analysis done) ──
    elif st.session_state.last_diagnosis is not None:
        diag        = st.session_state.last_diagnosis
        lang        = st.session_state.lang
        is_leaf     = diag.get("is_leaf", True)
        ai_err      = diag.get("ai_err")
        confidence  = diag.get("confidence", 0)
        crop_name_d = diag.get("crop", "")
        disease_name= diag.get("disease", "")
        info        = diag.get("info")
        gd          = st.session_state.gemini_disease

        # ── NOT A LEAF ──
        if not is_leaf:
            msg = "Not a leaf photo" if lang == "en" else "यह पत्ती की फोटो नहीं है"
            st.markdown(f'<div class="cl-disease-name">\u26a0\ufe0f {msg}</div>', unsafe_allow_html=True)
            st.caption(T["disclaimer"])

        # ── API ERROR (Gemini request failed — no credit was charged) ──
        elif ai_err and not gd:
            st.subheader(T["diagnosis_title"])
            st.error(
                f'⚠️ {APP_FAIL_EN if lang == "en" else APP_FAIL_HI}'
            )
            st.caption(
                "No scan credit was used for this failed attempt."
                if lang == "en"
                else "इस असफल प्रयास के लिए कोई स्कैन क्रेडिट नहीं काटा गया।"
            )
            st.caption(T["disclaimer"])

        # ── HIGH CONFIDENCE ≥95%: TFLite result ──
        elif confidence >= CONFIDENCE_THRESHOLD:
            st.subheader(T["diagnosis_title"])
            headline = f"{crop_name_d} \u2014 {disease_name}" if disease_name else crop_name_d
            st.markdown(f'<div class="cl-disease-name">{headline}</div>', unsafe_allow_html=True)
            st.progress(min(int(confidence), 100), text=f"{T['confidence_label']}: {confidence:.1f}%")
            st.markdown("")
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.button(T["view_treatment"], key="open_treatment", type="primary",
                          on_click=lambda: st.session_state.update(show_treatment=True))
            with btn_col2:
                st.button(T["report_button"], key="open_report", type="secondary",
                          on_click=lambda: st.session_state.update(show_report=True))
            st.caption(T["disclaimer"])

        # ── LOW CONFIDENCE <95%: Gemini result ──
        else:
            st.subheader(T["diagnosis_title"])
            headline = gd if (gd and gd.lower() not in ("unknown",)) else (
                "Unable to diagnose" if lang == "en" else "निदान संभव नहीं"
            )
            st.markdown(f'<div class="cl-disease-name">{headline}</div>', unsafe_allow_html=True)
            st.markdown("")
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.button(T["view_treatment"], key="open_treatment", type="primary",
                          on_click=lambda: st.session_state.update(show_treatment=True))
            with btn_col2:
                st.button(T["report_button"], key="open_report", type="secondary",
                          on_click=lambda: st.session_state.update(show_report=True))
            st.caption(T["disclaimer"])

    if st.session_state.credits_exhausted:
        st.error(
            f"### \U0001f6ab {T['credits_exhausted_title']}\n\n"
            f"{T['credits_exhausted_body']} **[agrifusion-web.vercel.app](https://agrifusion-web.vercel.app)**"
        )

# =================================================================
# TREATMENT ADVICE DIALOG
# Lets the farmer toggle between English and Hindi treatment advice
# inside the modal, independent of the app's main language setting.
# =================================================================
if st.session_state.get("show_treatment") and st.session_state.last_diagnosis:

    @st.dialog(T["treatment_modal_title"], width="large")
    def treatment_dialog():
        diag = st.session_state.last_diagnosis
        confidence = diag.get("confidence", 0)
        info = diag.get("info")
        gd = st.session_state.gemini_disease

        modal_lang = st.radio(
            T["modal_lang_label"],
            options=["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "हिंदी",
            horizontal=True,
            index=0 if st.session_state.lang == "en" else 1,
            key="treatment_modal_lang",
        )

        is_tflite_path = confidence >= CONFIDENCE_THRESHOLD and info is not None

        if is_tflite_path:
            crop_name_d = diag.get("crop", "")
            disease_name = diag.get("disease", "")
            headline = f"{crop_name_d} — {disease_name}" if disease_name else crop_name_d
            st.markdown(f'<div class="cl-disease-name">{headline}</div>', unsafe_allow_html=True)

            labels_map = {
                "severity_":   ("Severity", "गंभीरता"),
                "symptoms_":   ("Symptoms", "लक्षण"),
                "prevention_": ("Prevention", "रोकथाम"),
                "treatment_":  ("Treatment", "उपचार"),
            }
            for key, (label_en, label_hi) in labels_map.items():
                label = label_en if modal_lang == "en" else label_hi
                val = info.get(key + modal_lang, info.get(key + "en", "")) if info else ""
                if val:
                    st.markdown(f'<div class="cl-treatment-box"><b>{label}:</b> {val}</div>',
                                unsafe_allow_html=True)
        else:
            headline = gd if (gd and gd.lower() not in ("unknown",)) else (
                "Unable to diagnose" if modal_lang == "en" else "निदान संभव नहीं"
            )
            st.markdown(f'<div class="cl-disease-name">{headline}</div>', unsafe_allow_html=True)
            points = (st.session_state.gemini_treatment_hi if modal_lang == "hi"
                      else st.session_state.gemini_treatment_en)
            if points:
                for pt in points:
                    if pt.strip():
                        st.markdown(f'<div class="cl-treatment-box">\u2022 {pt}</div>',
                                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="cl-card-danger">\u26a0\ufe0f '
                    f'{APP_FAIL_EN if modal_lang == "en" else APP_FAIL_HI}</div>',
                    unsafe_allow_html=True
                )

        st.caption(T["disclaimer"])
        if st.button(T["close"], key="close_treatment_modal"):
            st.session_state.show_treatment = False
            st.rerun()

    treatment_dialog()

# =================================================================
# REPORT OUTBREAK DIALOG
# =================================================================
if st.session_state.get("show_report") and st.session_state.last_diagnosis:

    @st.dialog(T["report_dialog_title"], width="large")
    def report_dialog():
        diagnosis = st.session_state.last_diagnosis
        st.write(T["report_instructions"])

        # Map centred on India; farmer draws polygon to mark their farm
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="OpenStreetMap")

        Draw(
            export=False,
            draw_options={"polygon": True, "polyline": False, "rectangle": True,
                          "circle": False, "marker": True, "circlemarker": False},
            edit_options={"edit": True, "remove": True},
        ).add_to(m)

        map_data = st_folium(m, height=380, use_container_width=True, key="report_map",
                             returned_objects=["all_drawings", "last_active_drawing"])
        st.caption(T["map_caption"])

        drawn_geojson = None
        center_lat = center_lng = None
        if map_data:
            drawings = map_data.get("all_drawings") or []
            if drawings:
                drawn_geojson = drawings
                first = drawings[0]
                geom_type = first.get("geometry", {}).get("type", "")
                coords = first.get("geometry", {}).get("coordinates", [])
                if geom_type == "Point" and coords:
                    center_lng, center_lat = coords[0], coords[1]
                elif geom_type in ("Polygon", "MultiPolygon") and coords:
                    flat = coords[0] if geom_type == "Polygon" else coords[0][0]
                    center_lat = sum(c[1] for c in flat) / len(flat)
                    center_lng = sum(c[0] for c in flat) / len(flat)

        if drawn_geojson:
            st.success(f"✅ Farm mapped — {len(drawn_geojson)} shape(s) drawn.")

        farmer_name = st.text_input(T["farmer_name_label"])
        notes = st.text_area(T["notes_label"])

        col_a, col_b = st.columns(2)
        with col_a:
            submit_clicked = st.button(T["submit_report"], type="primary")
        with col_b:
            if st.button(T["close"]):
                st.session_state.show_report = False
                st.rerun()

        if submit_clicked:
            if not farmer_name.strip():
                st.warning(T["farmer_name_req"])
            elif not drawn_geojson:
                st.warning(T["no_polygon_warning"])
            elif center_lat is None or center_lng is None:
                st.warning(T["no_polygon_warning"])
            elif supabase is None:
                st.error(T["config_missing"])
            else:
                # ------------------------------------------------------------------
                # Water-body guard: reject submissions where the drawn shape's
                # centroid falls on an ocean, sea, or lake.
                # ------------------------------------------------------------------
                in_water = is_location_in_water(center_lat, center_lng)
                if in_water is True:
                    st.error(T["water_location_error"])
                    st.stop()
                # in_water is None → check failed (network issue) — allow through
                with st.spinner(T["submitting"]):
                    try:
                        # Always store the exact disease name shown to the user:
                        # Gemini text when AI path was used, readable TFLite name otherwise.
                        gd   = st.session_state.gemini_disease
                        conf = diagnosis.get("confidence", 0)
                        ai_path = conf < CONFIDENCE_THRESHOLD and bool(gd)

                        final_disease = gd if ai_path else diagnosis.get("disease", "")
                        final_crop    = st.session_state.get("crop_input") or diagnosis.get("crop", "")

                        supabase.table("outbreak_reports").insert({
                            "disease_class": final_disease,
                            "crop":          final_crop,
                            "disease":       final_disease,
                            "confidence":    conf,
                            "farmer_name":   farmer_name.strip(),
                            "farmer_dif":    st.session_state.farmer_dif,
                            "farm_geojson":  json.dumps(drawn_geojson),
                            "center_lat":    center_lat,
                            "center_lng":    center_lng,
                            "notes":         notes or None,
                            "language":      st.session_state.lang,
                            "reported_at":   datetime.now(timezone.utc).isoformat(),
                        }).execute()
                        st.success(T["report_success"])
                        st.session_state.show_report = False
                        st.session_state.map_polygon = None
                        st.rerun()
                    except Exception as ex:
                        st.error(f"{T['report_error']} ({ex})")

    report_dialog()