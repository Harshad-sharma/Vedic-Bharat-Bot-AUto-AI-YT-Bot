import google.generativeai as genai
import os
import time
import random
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 🧠 HUMAN STRATEGY: Hierarchy of Models
# Pehle sabse fast aur stable try karo. Fail ho to naya try karo.
MODEL_PRIORITY = [
    "gemini-1.5-flash",          # Priority 1: Stable King (1500 Req/Day)
    "gemini-flash-latest",       # Priority 2: Latest Stable
    "gemini-2.0-flash-lite-preview-02-05", # Priority 3: Ultra Lite
    "gemini-pro"                 # Priority 4: Old Reliable
]

def smart_generate(prompt):
    """
    Ye function insaan ki tarah behave karega.
    Ek model fail hua to dusra try karega.
    """
    for model_name in MODEL_PRIORITY:
        try:
            print(f"   🧠 Trying Brain: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            # Agar response khali hai to error maano
            if not response.text:
                raise ValueError("Empty response")
                
            return response.text.strip()
            
        except Exception as e:
            print(f"   ⚠️ Brain {model_name} Failed. Switching...")
            time.sleep(2) # Thoda saas lene do
            continue # Agle model par jao

    # Agar sare models fail ho gaye
    print("   ❌ ALL BRAINS FAILED. System collapsed.")
    return None