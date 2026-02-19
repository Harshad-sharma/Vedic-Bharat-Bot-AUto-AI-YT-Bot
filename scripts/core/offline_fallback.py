# scripts/core/offline_fallback.py
import json, random, os

OFFLINE_BANK = os.path.join("scripts", "offline_bank.json")

def offline_generate(prompt: str) -> str:
    """
    Minimal, safe fallback:
    - if prompt asks for TOPIC => pick from list
    - if prompt asks for JSON script => return a template JSON filled
    """
    try:
        with open(OFFLINE_BANK, "r", encoding="utf-8") as f:
            bank = json.load(f)
    except Exception:
        bank = {"topics": [], "scripts": []}

    p = prompt.lower()

    if "topic" in p or "ब्रेनस्टॉर्म" in p:
        topics = bank.get("topics") or [
            "गरुड़ पुराण में कर्म का विज्ञान",
            "शिव तांडव का ध्वनि-विज्ञान",
            "वेदों में समय की अवधारणा",
            "हनुमान जी और अडिग संकल्प"
        ]
        return random.choice(topics)

    # script fallback (JSON)
    scripts = bank.get("scripts") or []
    if scripts:
        return json.dumps(random.choice(scripts), ensure_ascii=False)

    # hard template
    return json.dumps({
        "topic": "सनातन का एक कम-ज्ञात सत्य",
        "language": "hi",
        "duration_sec": 60,
        "scenes": [
            {"type":"IMAGE","keyword":"Ancient temple golden light","text":"क्या आप जानते हैं..."},
            {"type":"VIDEO","keyword":"Cinematic spiritual energy","text":"यह विचार वेदों में मिलता है..."},
            {"type":"IMAGE","keyword":"Vedic manuscript glowing","text":"इसका मतलब है..."},
            {"type":"IMAGE","keyword":"Sunrise meditation silhouette","text":"अगर यह वीडियो पसंद आया... follow करें"}
        ],
        "cta":"ऐसी ही और वीडियोज़ के लिए Follow/Subscribe"
    }, ensure_ascii=False)
