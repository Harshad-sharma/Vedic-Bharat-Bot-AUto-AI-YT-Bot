import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("🔍 Google se pooch raha hoon ki kon-kon se models available hain...\n")

try:
    models = genai.list_models()
    found_any = False
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
            found_any = True
    
    if not found_any:
        print("❌ Koi model nahi mila! API Key check karein.")

except Exception as e:
    print(f"❌ Error: {e}")