import os
import random
import time
from scripts.core.ai_rotator import get_smart_client, report_failure

def get_unique_topic():
    max_retries = 15 # 15 baar alag-alag model try karega
    attempt = 0
    
    # Thodi variety ke liye topics ki list, taaki bot bore na kare
    categories = [
        "Scientific logic behind Hindu traditions",
        "Ancient Indian Engineering Marvels",
        "Ayurveda vs Modern Medicine Facts",
        "Lost Temples and Technologies of India",
        "Vedic Cosmology and Astronomy",
        "Untold mysteries of Indian Epics"
    ]
    selected_category = random.choice(categories)
    
    while attempt < max_retries:
        # Har attempt me naya model aur naya client aayega
        client, model_name = get_smart_client() 
        print(f"🧠 Brainstorming with {model_name} (Attempt {attempt+1})...")
        
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=f"Give me one unique, viral, mystery-based topic about '{selected_category}' for a YouTube Short. Output ONLY the topic sentence."
            )
            
            topic = response.text.strip()
            if topic:
                return topic # ✅ Success! Yahi se topic wapis chala jayega aur loop toot jayega
                
        except Exception as e:
            print(f"❌ Error on {model_name}: {e}")
            report_failure(model_name) # Is model ko aaj ke liye fail list me dalo
            time.sleep(2) # Agla try karne se pehle 2 second saans lo
            attempt += 1 # Attempt badhao aur loop ghumao
            
    # Agar 15 attempts ke baad bhi sare models dead nikle (Jo ki normally nahi hoga)
    print("🚨 Sare models fail ho gaye! Fallback topic use kar rahe hain.")
    return "Ancient Indian Surgery Secrets: How Sushruta mapped the human body."