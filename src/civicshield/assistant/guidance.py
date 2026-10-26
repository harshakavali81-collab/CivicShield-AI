"""Curated educational guidance. No LLM, live retrieval, invented citations or official alert claims."""
REFERENCE = {"title": "National Disaster Management Authority (India)", "url": "https://ndma.gov.in/"}
GUIDANCE = {
  "en": {
    "flood": "Move away from fast-moving water and flooded roads. Do not drive through floodwater. Check verified local warnings and follow evacuation directions from authorities.",
    "heat": "Stay hydrated, avoid strenuous outdoor activity during peak heat, seek shade, and get medical help for confusion, fainting or heatstroke symptoms.",
    "general": "Follow announcements from local emergency authorities. Prepare essential medications, drinking water and important contact numbers. For immediate danger, contact local emergency services.",
  },
  "te": {
    "flood": "వరద నీటిలో నడవకండి లేదా వాహనం నడపకండి. సురక్షితమైన ఎత్తైన ప్రదేశానికి వెళ్లి స్థానిక అధికారుల సూచనలు పాటించండి.",
    "heat": "తగినంత నీరు తాగండి, తీవ్రమైన ఎండలో బయట పనిని తగ్గించండి. వడదెబ్బ లక్షణాలు ఉంటే వెంటనే వైద్య సహాయం పొందండి.",
    "general": "స్థానిక అధికారుల అధికారిక సమాచారాన్ని అనుసరించండి. అత్యవసర మందులు, తాగునీరు, సంప్రదింపు నంబర్లు సిద్ధంగా ఉంచండి.",
  },
  "hi": {
    "flood": "बाढ़ के पानी में पैदल या वाहन से न जाएँ। ऊँचे सुरक्षित स्थान पर जाएँ और स्थानीय अधिकारियों के निर्देश मानें।",
    "heat": "पर्याप्त पानी पिएँ, तेज गर्मी में मेहनत कम करें और हीटस्ट्रोक के लक्षणों पर तुरंत चिकित्सा सहायता लें।",
    "general": "स्थानीय प्रशासन की आधिकारिक जानकारी का पालन करें। दवाइयाँ, पीने का पानी और जरूरी संपर्क नंबर तैयार रखें।",
  },
  "ta": {
    "flood": "வெள்ள நீரில் நடக்கவோ வாகனம் ஓட்டவோ வேண்டாம். உயரமான பாதுகாப்பான இடத்திற்குச் சென்று அதிகாரிகளின் அறிவுறுத்தல்களைப் பின்பற்றுங்கள்.",
    "heat": "போதிய தண்ணீர் குடிக்கவும். கடும் வெயிலில் வேலை செய்வதைத் தவிர்க்கவும். வெப்பத் தாக்க அறிகுறிகள் இருந்தால் மருத்துவ உதவி பெறவும்.",
    "general": "உள்ளூர் அதிகாரப்பூர்வ அறிவிப்புகளைப் பின்பற்றுங்கள். மருந்துகள், குடிநீர் மற்றும் அவசர தொடர்பு எண்களைத் தயாராக வையுங்கள்.",
  },
  "kn": {
    "flood": "ಪ್ರವಾಹದ ನೀರಿನಲ್ಲಿ ನಡೆಯಬೇಡಿ ಅಥವಾ ವಾಹನ ಚಲಾಯಿಸಬೇಡಿ. ಎತ್ತರದ ಸುರಕ್ಷಿತ ಸ್ಥಳಕ್ಕೆ ಹೋಗಿ ಅಧಿಕಾರಿಗಳ ಸೂಚನೆ ಪಾಲಿಸಿ.",
    "heat": "ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ. ತೀವ್ರ ಬಿಸಿಲಿನಲ್ಲಿ ಶ್ರಮ ತಪ್ಪಿಸಿ. ಶಾಖಾಘಾತದ ಲಕ್ಷಣಗಳಿದ್ದರೆ ತಕ್ಷಣ ವೈದ್ಯಕೀಯ ಸಹಾಯ ಪಡೆಯಿರಿ.",
    "general": "ಸ್ಥಳೀಯ ಅಧಿಕಾರಿಗಳ ಅಧಿಕೃತ ಸೂಚನೆಗಳನ್ನು ಅನುಸರಿಸಿ. ಔಷಧಿ, ಕುಡಿಯುವ ನೀರು ಮತ್ತು ತುರ್ತು ಸಂಪರ್ಕ ಸಂಖ್ಯೆಗಳನ್ನಿಟ್ಟುಕೊಳ್ಳಿ.",
  },
}
TERMS = {
    "flood": ("flood", "rain", "water", "వరద", "వర్ష", "बाढ़", "बारिश", "வெள்ள", "மழை", "ಪ್ರವಾಹ", "ಮಳೆ"),
    "heat": ("heat", "hot", "sun", "వేడి", "ఎండ", "गर्मी", "धूप", "வெப்ப", "வெயில்", "ಬಿಸಿ", "ಬಿಸಿಲು"),
}

def answer(question: str, language: str) -> dict:
    q = question.casefold()
    category = next((name for name, tokens in TERMS.items() if any(t in q for t in tokens)), "general")
    return {
        "language": language,
        "topic": category,
        "answer": GUIDANCE[language][category],
        "references": [REFERENCE],
        "source_type": "curated_educational_summary",
        "live_retrieval": False,
        "is_official_warning": False,
        "disclaimer": "Educational preparedness guidance; not a live official notice or emergency instruction.",
    }
