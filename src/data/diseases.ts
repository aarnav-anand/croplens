export interface DiseaseDetail {
  severity_en: string;
  severity_hi: string;
  symptoms_en: string;
  symptoms_hi: string;
  prevention_en: string;
  prevention_hi: string;
  treatment_en: string;
  treatment_hi: string;
}

export const DISEASE_INFO: Record<string, DiseaseDetail> = {
  healthy: {
    severity_en: "None",
    severity_hi: "कोई नहीं",
    symptoms_en: "No disease symptoms detected. Leaf color and texture look normal.",
    symptoms_hi: "कोई रोग लक्षण नहीं मिला। पत्ती का रंग और बनावट सामान्य है।",
    prevention_en: "Keep up good field hygiene, proper plant spacing, and balanced watering.",
    prevention_hi: "अच्छी खेत स्वच्छता, उचित पौधों की दूरी और संतुलित सिंचाई बनाए रखें।",
    treatment_en: "No treatment needed. Continue routine monitoring.",
    treatment_hi: "किसी उपचार की आवश्यकता नहीं। नियमित निगरानी जारी रखें।",
  },
  scab: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Olive-green to brown scabby spots on leaves and fruit.",
    symptoms_hi: "पत्तियों और फलों पर पपड़ीदार जैतून-हरे से भूरे धब्बे।",
    prevention_en: "Destroy fallen leaves after harvest. Choose resistant varieties.",
    prevention_hi: "फसल कटाई के बाद गिरी पत्तियां नष्ट करें। प्रतिरोधी किस्में चुनें।",
    treatment_en: "Remove infected leaves/fruit. Apply copper- or sulfur-based fungicide at bud break.",
    treatment_hi: "संक्रमित पत्तियां हटाएं। कली निकलने के समय कॉपर या सल्फर फफूंदनाशक लगाएं।",
  },
  black_rot: {
    severity_en: "High",
    severity_hi: "उच्च",
    symptoms_en: "Circular brown-purple leaf spots; fruit develops dark mummified rot.",
    symptoms_hi: "गोल भूरे-बैंगनी धब्बे; फल पर गहरे रंग का सड़ाव।",
    prevention_en: "Prune dead wood in dormant season. Remove mummified fruit.",
    prevention_hi: "मृत शाखाओं की छंटाई करें। सूखे फल हटाएं।",
    treatment_en: "Remove infected material. Apply fungicide for black rot during wet periods.",
    treatment_hi: "संक्रमित हिस्से हटाएं। नम मौसम में फफूंदनाशक लगाएं।",
  },
  rust: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Orange-yellow powdery pustules on the underside of leaves.",
    symptoms_hi: "पत्तियों के नीचे नारंगी-पीले पाउडर जैसे धब्बे।",
    prevention_en: "Remove alternate host plants. Avoid overhead irrigation.",
    prevention_hi: "वैकल्पिक मेज़बान पौधे हटाएं। ऊपर से सिंचाई से बचें।",
    treatment_en: "Apply protectant fungicide at first sign and repeat through humid season.",
    treatment_hi: "पहले लक्षण पर फफूंदनाशक लगाएं और नम मौसम में दोहराएं।",
  },
  powdery_mildew: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "White to gray powdery coating on leaves and stems.",
    symptoms_hi: "पत्तियों और तनों पर सफेद पाउडर जैसी परत।",
    prevention_en: "Choose resistant varieties, avoid overcrowding, prune for airflow.",
    prevention_hi: "प्रतिरोधी किस्में चुनें, पौधों में पर्याप्त दूरी रखें और छंटाई करें।",
    treatment_en: "Apply sulfur-based or horticultural oil fungicide at first signs.",
    treatment_hi: "पहले लक्षणों पर सल्फर आधारित फफूंदनाशक या तेल का छिड़काव करें।",
  },
  leaf_blight: {
    severity_en: "Moderate-High",
    severity_hi: "मध्यम-उच्च",
    symptoms_en: "Irregular brown lesions expanding from leaf edges or tips.",
    symptoms_hi: "पत्ती के किनारों या नोकों से फैलते अनियमित भूरे घाव।",
    prevention_en: "Rotate crops, remove crop debris, avoid overhead watering.",
    prevention_hi: "फसल चक्र अपनाएं, फसल के अवशेष हटाएं, ऊपर से पानी न दें।",
    treatment_en: "Remove affected foliage. Apply fungicide labeled for leaf blight.",
    treatment_hi: "प्रभावित पत्तियां हटाएं। लीफ ब्लाइट हेतु अनुमोदित फफूंदनाशक लगाएं।",
  },
  leaf_spot: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Small gray-to-brown spots with defined edges, sometimes with a yellow halo.",
    symptoms_hi: "स्पष्ट किनारों वाले छोटे धूसर-भूरे धब्बे, कभी-कभी पीले घेरे के साथ।",
    prevention_en: "Rotate crops, remove debris, water at base.",
    prevention_hi: "फसल चक्र अपनाएं, पौधे के आधार पर पानी दें।",
    treatment_en: "Remove spotted leaves. Use fungicide labeled for leaf spot.",
    treatment_hi: "धब्बेदार पत्तियां हटाएं। लीफ स्पॉट रोधक फफूंदनाशक लगाएं।",
  },
  bacterial_spot: {
    severity_en: "Moderate-High",
    severity_hi: "मध्यम-उच्च",
    symptoms_en: "Dark water-soaked spots on leaves and fruit with yellow halo.",
    symptoms_hi: "पत्तियों और फलों पर पीले घेरे वाले गहरे जल-सिक्त धब्बे।",
    prevention_en: "Use disease-free seed, avoid wet-field work, rotate crops.",
    prevention_hi: "रोगमुक्त बीज उपयोग करें, गीले खेत में काम न करें।",
    treatment_en: "Remove infected plants promptly. Apply copper-based bactericide early.",
    treatment_hi: "संक्रमित पौधे तुरंत हटाएं। कॉपर बैक्टीरियानाशक का शीघ्र प्रयोग करें।",
  },
  early_blight: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Dark brown spots with concentric rings, starting on older lower leaves.",
    symptoms_hi: "निचली पुरानी पत्तियों पर गहरे भूरे संकेंद्रित छल्लेदार धब्बे।",
    prevention_en: "Rotate crops, stake plants for airflow, mulch, water at base.",
    prevention_hi: "फसल चक्र अपनाएं, पौधों को सहारा दें, मल्चिंग करें।",
    treatment_en: "Remove lower infected leaves. Apply fungicide for early blight.",
    treatment_hi: "निचली संक्रमित पत्तियां हटाएं। अगेती झुलसा फफूंदनाशक लगाएं।",
  },
  late_blight: {
    severity_en: "High — spreads fast",
    severity_hi: "उच्च — तेज़ी से फैलता है",
    symptoms_en: "Large water-soaked dark blotches; white fuzzy mold underneath in humid weather.",
    symptoms_hi: "बड़े गहरे धब्बे; नम मौसम में पत्तियों के नीचे सफेद फफूंद।",
    prevention_en: "Plant resistant varieties, ensure good drainage, avoid overhead watering.",
    prevention_hi: "प्रतिरोधी किस्में लगाएं, अच्छी जल निकासी सुनिश्चित करें।",
    treatment_en: "Act immediately — remove and destroy infected plants. Apply fungicide. Contact extension office.",
    treatment_hi: "तुरंत संक्रमित पौधे नष्ट करें। फफूंदनाशक लगाएं और कृषि विभाग से संपर्क करें।",
  },
  leaf_mold: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Pale patches on upper surface; olive-green velvety mold underneath.",
    symptoms_hi: "ऊपरी सतह पर हल्के धब्बे; नीचे मखमली जैतून-हरी फफूंद।",
    prevention_en: "Improve ventilation, reduce humidity, avoid overhead watering.",
    prevention_hi: "हवा का संचार बेहतर बनाएं, नमी कम करें।",
    treatment_en: "Remove affected leaves and improve airflow. Use fungicide if needed.",
    treatment_hi: "प्रभावित पत्तियां हटाएं और वेंटिलेशन सुधारें।",
  },
  spider_mites: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Tiny yellow/white speckling on leaves, fine webbing underneath.",
    symptoms_hi: "पत्तियों पर छोटे पीले/सफेद धब्बे, नीचे बारीक जाला।",
    prevention_en: "Keep plants well-watered, encourage natural predators.",
    prevention_hi: "पौधों को अच्छी तरह सिंचित रखें, मित्र कीटों को बढ़ावा दें।",
    treatment_en: "Spray undersides with water. Use insecticidal soap or miticide.",
    treatment_hi: "पत्तियों के नीचे पानी छिड़कें। कीटनाशी साबुन या माइटिसाइड लगाएं।",
  },
  target_spot: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Brown lesions with concentric rings (target-like) on leaves and stems.",
    symptoms_hi: "पत्तियों पर संकेंद्रित छल्लों वाले लक्ष्य जैसे भूरे घाव।",
    prevention_en: "Rotate crops, remove plant debris, avoid dense planting.",
    prevention_hi: "फसल चक्र अपनाएं, पौधे के अवशेष हटाएं, घना न रोपें।",
    treatment_en: "Remove infected leaves. Apply fungicide for target spot.",
    treatment_hi: "संक्रमित पत्तियां हटाएं। लक्षित धब्बा फफूंदनाशक लगाएं।",
  },
  yellow_leaf_curl_virus: {
    severity_en: "High — no cure, manage vector",
    severity_hi: "उच्च — कोई इलाज नहीं",
    symptoms_en: "Upward-curling yellow leaves, stunted growth. Spread by whiteflies.",
    symptoms_hi: "पत्तियां ऊपर मुड़कर पीली पड़ जाती हैं, बौनी वृद्धि। सफेद मक्खी से फैलता है।",
    prevention_en: "Use insect-proof screens, plant certified virus-free seedlings.",
    prevention_hi: "कीट-रोधी जाल लगाएं, प्रमाणित पौध लगाएं।",
    treatment_en: "No cure. Remove infected plants. Control whitefly with insecticide.",
    treatment_hi: "कोई रासायनिक इलाज नहीं। संक्रमित पौधे नष्ट करें व सफेद मक्खी नियंत्रित करें।",
  },
  mosaic_virus: {
    severity_en: "High — no cure",
    severity_hi: "उच्च — कोई इलाज नहीं",
    symptoms_en: "Mottled yellow-green mosaic pattern on leaves, distortion, stunted growth.",
    symptoms_hi: "पत्तियों पर पीले-हरे मोज़ेक पैटर्न और विकृति, पौधे का छोटा रहना।",
    prevention_en: "Use virus-free seed, control aphid populations.",
    prevention_hi: "वायरस-मुक्त बीज उपयोग करें, माहू/एफिड नियंत्रित करें।",
    treatment_en: "No cure. Remove and destroy infected plants to prevent spread.",
    treatment_hi: "कोई इलाज नहीं। फैलाव रोकने हेतु संक्रमित पौधे नष्ट करें।",
  },
  citrus_greening: {
    severity_en: "Very High — fatal to trees",
    severity_hi: "बहुत उच्च — वृक्षों के लिए घातक",
    symptoms_en: "Blotchy asymmetric yellow mottling; small lopsided bitter fruit.",
    symptoms_hi: "असममित पीला धब्बेदार पैटर्न; छोटे टेढ़े-मेढ़े कड़वे फल।",
    prevention_en: "Use certified disease-free planting material, control psyllid vector.",
    prevention_hi: "प्रमाणित रोगमुक्त पौध सामग्री उपयोग करें, सिट्रस सिलिड कीट को नियंत्रित करें।",
    treatment_en: "No cure. Remove infected trees. Consult agricultural department immediately.",
    treatment_hi: "कोई रासायनिक इलाज नहीं। संक्रमित पेड़ तुरंत हटाएं। कृषि विभाग से संपर्क करें।",
  },
  esca: {
    severity_en: "High",
    severity_hi: "उच्च",
    symptoms_en: "Tiger-stripe yellowing between leaf veins; sudden vine collapse in summer.",
    symptoms_hi: "पत्ती की नसों के बीच बाघ जैसी धारियां; गर्मियों में बेल का अचानक सूखना।",
    prevention_en: "Avoid large pruning wounds; seal cuts. Remove infected wood.",
    prevention_hi: "बड़े छंटाई घावों से बचें, घावों पर लेप लगाएं।",
    treatment_en: "No effective chemical cure. Remove infected vines. Consult specialist.",
    treatment_hi: "कोई प्रभावी इलाज नहीं। संक्रमित बेलें हटाएं व विशेषज्ञ से परामर्श लें।",
  },
  leaf_scorch: {
    severity_en: "Moderate",
    severity_hi: "मध्यम",
    symptoms_en: "Purple-to-brown spots on leaves; edges drying and curling.",
    symptoms_hi: "पत्तियों पर बैंगनी-भूरे धब्बे; किनारे सूखकर मुड़ना।",
    prevention_en: "Remove old infected leaves after harvest, ensure good drainage.",
    prevention_hi: "पुरानी संक्रमित पत्तियां हटाएं, जल निकासी सुनिश्चित करें।",
    treatment_en: "Remove infected leaves. Apply fungicide labeled for leaf scorch.",
    treatment_hi: "संक्रमित पत्तियां नष्ट करें। फफूंदनाशक लगाएं।",
  },
};

export const GENERIC_FALLBACK: DiseaseDetail = {
  severity_en: "Unknown",
  severity_hi: "अज्ञात",
  symptoms_en: "Visible discoloration or spotting detected on the leaf.",
  symptoms_hi: "पत्ती पर दिखाई देने वाला रंग बदलना या धब्बे पाए गए।",
  prevention_en: "Practice crop rotation, remove plant debris, avoid overhead watering.",
  prevention_hi: "फसल चक्र अपनाएं, पौधे के अवशेष हटाएं, ऊपर से सिंचाई से बचें।",
  treatment_en: "Contact your local agricultural extension officer for a targeted treatment plan.",
  treatment_hi: "सटीक उपचार योजना हेतु स्थानीय कृषि विस्तार अधिकारी से संपर्क करें।",
};

export const CATEGORY_KEYWORDS: [string, string][] = [
  ["healthy", "healthy"],
  ["scab", "scab"],
  ["black_rot", "black_rot"],
  ["rust", "rust"],
  ["powdery_mildew", "powdery_mildew"],
  ["leaf_blight", "leaf_blight"],
  ["northern_leaf_blight", "leaf_blight"],
  ["gray_leaf_spot", "leaf_spot"],
  ["cercospora", "leaf_spot"],
  ["septoria", "leaf_spot"],
  ["bacterial_spot", "bacterial_spot"],
  ["early_blight", "early_blight"],
  ["late_blight", "late_blight"],
  ["leaf_mold", "leaf_mold"],
  ["spider_mite", "spider_mites"],
  ["target_spot", "target_spot"],
  ["yellow_leaf_curl", "yellow_leaf_curl_virus"],
  ["mosaic_virus", "mosaic_virus"],
  ["haunglongbing", "citrus_greening"],
  ["citrus_greening", "citrus_greening"],
  ["esca", "esca"],
  ["leaf_scorch", "leaf_scorch"],
];

export function getDiseaseInfo(rawClassName: string): DiseaseDetail {
  const key = rawClassName.toLowerCase().replace(/[\s-]+/g, "_");
  for (const [substring, category] of CATEGORY_KEYWORDS) {
    if (key.includes(substring)) {
      return DISEASE_INFO[category] || GENERIC_FALLBACK;
    }
  }
  return GENERIC_FALLBACK;
}
