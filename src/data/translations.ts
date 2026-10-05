export interface TranslationBundle {
  app_title: string;
  app_subtitle: string;
  tagline: string;
  signin_title: string;
  signin_subtitle: string;
  dif_label: string;
  dif_placeholder: string;
  dif_help: string;
  signin_button: string;
  dif_invalid_format: string;
  dif_not_found: string;
  dif_error: string;
  signed_in_as: string;
  credits_label: string;
  credits_exhausted_title: string;
  credits_exhausted_body: string;
  signout: string;
  instructions_title: string;
  instructions: string[];
  upload_label: string;
  open_camera: string;
  close_camera: string;
  take_photo_btn: string;
  retake_photo_btn: string;
  uploaded_caption: string;
  crop_prompt: string;
  crop_placeholder: string;
  crop_analyze_btn: string;
  crop_warning: string;
  diagnosing: string;
  gemini_analyzing: string;
  diagnosis_title: string;
  confidence_label: string;
  low_confidence_warning: string;
  ai_diagnosed_label: string;
  ai_no_result: string;
  not_a_leaf: string;
  treatment_title: string;
  symptoms_label: string;
  prevention_label: string;
  treatment_label: string;
  severity_label: string;
  gemini_treatment_label: string;
  gemini_no_treatment: string;
  report_button: string;
  report_dialog_title: string;
  report_instructions: string;
  locate_me: string;
  locate_me_help: string;
  notes_label: string;
  farmer_name_label: string;
  farmer_name_req: string;
  submit_report: string;
  submitting: string;
  report_success: string;
  report_error: string;
  no_polygon_warning: string;
  config_missing: string;
  disclaimer: string;
  map_caption: string;
  water_location_error: string;
  hide_report: string;
  modal_lang_label: string;
  view_reports: string;
  demo_codes_hint: string;
}

export const TEXT: Record<"en" | "hi", TranslationBundle> = {
  en: {
    app_title: "🌱 CropLens",
    app_subtitle: "AI Crop Doctor",
    tagline: "Point your phone at a leaf. Get a diagnosis in seconds.",
    signin_title: "Sign In",
    signin_subtitle: "Enter your DIF Code to continue",
    dif_label: "DIF Code",
    dif_placeholder: "e.g. AB12",
    dif_help: "2 letters + 2 digits (e.g. AB12)",
    signin_button: "Sign In →",
    dif_invalid_format: "Invalid format — must be 2 letters then 2 digits (e.g. AB12).",
    dif_not_found: "DIF code not found. Please check and try again.",
    dif_error: "Could not connect to server. Please try again.",
    signed_in_as: "Signed in",
    credits_label: "Scans remaining",
    credits_exhausted_title: "Credits Exhausted",
    credits_exhausted_body: "Purchase more scans at",
    signout: "Sign out",
    instructions_title: "📸 How to take a good photo",
    instructions: [
      "Take the photo in good daylight — avoid deep shadows or strong glare.",
      "Place the leaf on a plain, solid-colored background.",
      "Photograph only ONE leaf, filling most of the frame.",
      "Hold the camera steady directly above the leaf — avoid blur.",
    ],
    upload_label: "📁 Upload a leaf photo",
    open_camera: "📷 Open Camera",
    close_camera: "✕ Close Camera",
    take_photo_btn: "📸 Snap Photo",
    retake_photo_btn: "🔄 Retake Photo",
    uploaded_caption: "Your leaf photo",
    crop_prompt: "Which crop is this leaf from?",
    crop_placeholder: "e.g. Tomato, Apple, Corn, Potato, Rice, Wheat...",
    crop_analyze_btn: "Analyse →",
    crop_warning: "Please enter the crop name.",
    diagnosing: "Analyzing your leaf...",
    gemini_analyzing: "Consulting AI plant pathologist...",
    diagnosis_title: "Diagnosis",
    confidence_label: "Confidence",
    low_confidence_warning: "Low confidence — AI-assisted diagnosis shown below.",
    ai_diagnosed_label: "AI-Identified Disease",
    ai_no_result: "Could not identify the disease. Please retake the photo.",
    not_a_leaf: "Not a leaf photo. Please capture a clear leaf photo.",
    treatment_title: "🩺 Treatment & Care Advice",
    symptoms_label: "Symptoms",
    prevention_label: "Prevention",
    treatment_label: "Treatment",
    severity_label: "Severity",
    gemini_treatment_label: "AI-Generated Treatment Advice",
    gemini_no_treatment: "No treatment advice available. Please consult your local agricultural officer.",
    report_button: "🚩 Report Outbreak",
    report_dialog_title: "Report Disease Outbreak",
    report_instructions: "Click on the map to pin your farm location. Then enter your name and submit.",
    locate_me: "📍 Locate Me",
    locate_me_help: "Zoom the map to your current GPS location.",
    notes_label: "Notes (optional)",
    farmer_name_label: "Your name",
    farmer_name_req: "Please enter your name before submitting.",
    submit_report: "Submit Report",
    submitting: "Submitting...",
    report_success: "✅ Outbreak report submitted successfully. Thank you!",
    report_error: "Could not submit report. Please try again.",
    no_polygon_warning: "Please click on the map to pin your farm location first.",
    config_missing: "Reporting service not available. Contact app administrator.",
    disclaimer: "⚠️ CropLens is an AI-assisted tool, not a substitute for professional agronomic advice.",
    map_caption: "Click on the interactive map to mark your farm field coordinates",
    water_location_error: "⛔ The selected location appears to be in a water body (ocean, sea, or lake). Please mark your farm on land.",
    hide_report: "✕ Close Report Form",
    modal_lang_label: "View advice in",
    view_reports: "Recent Community Reports",
    demo_codes_hint: "Demo DIF Codes: AB12 (10 scans), CD34 (5 scans), EF56 (25 scans)",
  },
  hi: {
    app_title: "🌱 क्रॉपलेंस",
    app_subtitle: "एआई फसल डॉक्टर",
    tagline: "अपने फोन को पत्ती पर रखें। सेकंडों में सटीक निदान पाएं।",
    signin_title: "साइन इन",
    signin_subtitle: "जारी रखने के लिए DIF कोड दर्ज करें",
    dif_label: "DIF कोड",
    dif_placeholder: "जैसे AB12",
    dif_help: "2 अक्षर + 2 अंक (जैसे AB12)",
    signin_button: "साइन इन करें →",
    dif_invalid_format: "अमान्य फ़ॉर्मेट — 2 अक्षर फिर 2 अंक होने चाहिए (जैसे AB12)।",
    dif_not_found: "DIF कोड नहीं मिला। कृपया जांचें।",
    dif_error: "सर्वर से कनेक्ट नहीं हो सका। कृपया पुनः प्रयास करें।",
    signed_in_as: "साइन इन:",
    credits_label: "शेष स्कैन",
    credits_exhausted_title: "क्रेडिट समाप्त",
    credits_exhausted_body: "अधिक स्कैन खरीदें:",
    signout: "साइन आउट",
    instructions_title: "📸 अच्छी फोटो कैसे लें",
    instructions: [
      "फोटो अच्छी धूप में लें — गहरी छाया या चमक से बचें।",
      "पत्ती को एक सादे रंग की पृष्ठभूमि पर रखें।",
      "केवल एक पत्ती की फोटो लें, जो पूरे फ्रेम को भरे।",
      "कैमरे को स्थिर रखें, सीधे पत्ती के ऊपर से — धुंधलेपन से बचें।",
    ],
    upload_label: "📁 पत्ती की फोटो अपलोड करें",
    open_camera: "📷 कैमरा खोलें",
    close_camera: "✕ कैमरा बंद करें",
    take_photo_btn: "📸 फोटो खींचें",
    retake_photo_btn: "🔄 दोबारा फोटो लें",
    uploaded_caption: "आपकी पत्ती की फोटो",
    crop_prompt: "यह किस फसल की पत्ती है?",
    crop_placeholder: "जैसे टमाटर, सेब, मक्का, आलू, चावल, गेहूं...",
    crop_analyze_btn: "विश्लेषण करें →",
    crop_warning: "कृपया फसल का नाम दर्ज करें।",
    diagnosing: "आपकी पत्ती का विश्लेषण हो रहा है...",
    gemini_analyzing: "एआई पादप रोग विशेषज्ञ से परामर्श लिया जा रहा है...",
    diagnosis_title: "निदान",
    confidence_label: "विश्वसनीयता",
    low_confidence_warning: "कम विश्वसनीयता — एआई-सहायता प्राप्त निदान नीचे दिखाया गया है।",
    ai_diagnosed_label: "एआई द्वारा पहचाना रोग",
    ai_no_result: "रोग की पहचान नहीं हो सकी। फोटो दोबारा लें।",
    not_a_leaf: "यह पत्ती की फोटो नहीं है। कृपया स्पष्ट पत्ती की फोटो लें।",
    treatment_title: "🩺 उपचार और देखभाल सलाह",
    symptoms_label: "लक्षण",
    prevention_label: "रोकथाम",
    treatment_label: "उपचार",
    severity_label: "गंभीरता",
    gemini_treatment_label: "एआई-जनित उपचार सलाह",
    gemini_no_treatment: "उपचार सलाह उपलब्ध नहीं। स्थानीय कृषि अधिकारी से संपर्क करें।",
    report_button: "🚩 प्रकोप रिपोर्ट करें",
    report_dialog_title: "रोग प्रकोप रिपोर्ट करें",
    report_instructions: "मानचित्र पर क्लिक करके अपने खेत का स्थान चिह्नित करें। फिर नाम दर्ज कर सबमिट करें।",
    locate_me: "📍 मुझे ढूंढें",
    locate_me_help: "मानचित्र को आपकी वर्तमान जीपीएस स्थिति पर ले जाएगा।",
    notes_label: "नोट्स (वैकल्पिक)",
    farmer_name_label: "आपका नाम",
    farmer_name_req: "सबमिट करने से पहले कृपया अपना नाम दर्ज करें।",
    submit_report: "रिपोर्ट सबमिट करें",
    submitting: "सबमिट हो रहा है...",
    report_success: "✅ रोग प्रकोप रिपोर्ट सफलतापूर्वक सबमिट हो गई। धन्यवाद!",
    report_error: "रिपोर्ट सबमिट नहीं हो सकी। कृपया दोबारा प्रयास करें।",
    no_polygon_warning: "कृपया पहले मानचित्र पर क्लिक करके खेत का स्थान चुनें।",
    config_missing: "रिपोर्टिंग सेवा उपलब्ध नहीं है।",
    disclaimer: "⚠️ क्रॉपलेंस एक एआई-सहायता प्राप्त टूल है, पेशेवर कृषि सलाह का विकल्प नहीं।",
    map_caption: "खेत का स्थान चिह्नित करने के लिए मानचित्र पर क्लिक करें",
    water_location_error: "⛔ चुना गया स्थान जल क्षेत्र (समुद्र, झील या नदी) में प्रतीत होता है। कृपया खेत की स्थिति ज़मीन पर लगाएं।",
    hide_report: "✕ फॉर्म बंद करें",
    modal_lang_label: "सलाह की भाषा",
    view_reports: "हालिया समुदाय रिपोर्ट्स",
    demo_codes_hint: "डेमो DIF कोड: AB12 (10 स्कैन), CD34 (5 स्कैन), EF56 (25 स्कैन)",
  },
};
