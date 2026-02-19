import os
import json
import time
from scripts.core.ai_rotator import get_smart_client, report_failure

def generate_viral_script(topic_name):
    max_retries = 15 # 15 baar alag-alag model try karega
    attempt = 0
    
    while attempt < max_retries:
        client, model_name = get_smart_client()
        print(f"✍️ Scripting with {model_name} (Attempt {attempt+1})...")
        
        try:
            # 🔥 TUMHARA EXACT PROMPT
            prompt = f"""
    Act as a Professional Documentarian for 'Vedic Bharat'.
    TOPIC: {topic_name}
    
    Create a detailed 59-second Hindi script.
    Break the visual plan into scenes. For EACH scene, estimate the duration (in seconds) based on the length of the spoken line.
    CRITICAL RULES:
        1. **MAX WORD COUNT: 110 WORDS.** (Strict Limit).
        2. Do not start with "Namaste" or "Hello". Start with the Hook.
        3. Do not say "Thanks for watching".
        4. Language: Hindi (Devanagari).
        5. **STRICTLY SANATAN/VEDIC VISUALS ONLY.** 2. NEVER suggest 'Arabic text', 'Urdu text', 'Mosques', or 'Green Domes'.
        6. Use prompts like: 'Ancient Sanskrit Scriptures on palm leaves', 'Saffron flag', 'Hindu Temple Architecture', 'Rishi Munis in Himalayas'.
        7. Visuals MUST match the spoken sentence exactly.
    CRITICAL VISUAL RULES (AESTHETIC CONTROL):
    1. NEVER suggest modern visuals like 'Computers', 'Labs', 'Scientists in white coats', 'Green Matrix code'.
    2. Instead of 'DNA', suggest 'Glowing Golden Kundalini Helix' or 'Nadi System'.
    3. Instead of 'Space/Rocket', suggest 'Vimana' or 'Cosmic Brahmanda'.
    4. Instead of 'Computer Code', suggest 'Sanskrit Manuscripts' or 'Sri Yantra geometry'.
    5. AVOID Islamic/Mughal architecture (No Domes/Arches). Focus on Shikharas/Stone Temples.
    6. Visuals must look like "Pinterest Aesthetic": Golden hour, cinematic, warm tones, divine, mystical.
    7. Visuals MUST match to the mentioned topic,thing,person ,etc .
    OUTPUT FORMAT (Strict JSON):
    {{
        "title": "English Title",
        "hook": "Hindi Hook line",
        "body": "Main Hindi Script",
        "cta": "Hindi CTA",
        "visual_plan": [
            {{"type": "IMAGE", "query": "Ancient gold sri yantra geometry close up spiritual"}},
            {{"type": "VIDEO", "query": "Golden particles floating in dark background cosmic"}},
            {{"type": "IMAGE", "query": "Lord Shiva cosmic form nebula art painting"}},
            {{"query": "Close up of Sanskrit Shloka on old paper", "duration": 4}}
        
            ... (Total 15-20 items)
        ]
    }}
    """
            
            response = client.models.generate_content(model=model_name, contents=prompt)
            
            # JSON cleaning logic
            text = response.text.replace("```json", "").replace("```", "").strip()
            if "{" in text: text = text[text.find("{"):text.rfind("}")+1]
            
            # Agar success ho gaya, to function yahi se data wapis bhej dega (Loop toot jayega)
            return json.loads(text)

        except Exception as e:
            print(f"❌ Error on {model_name}: {e}")
            report_failure(model_name) # Is model ko fail list me dalo
            time.sleep(2) # Agla try karne se pehle 2 second ruko
            attempt += 1 # Attempt badhao aur loop ghumao
            
    # Agar 15 attempts ke baad bhi fail ho jaye
    print("🚨 Sare models fail ho gaye! Script nahi ban payi.")
    return None