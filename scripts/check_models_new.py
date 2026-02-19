import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("🔍 CONNECTING TO GOOGLE (NEW SDK)...")
try:
    client = genai.Client(api_key=api_key)
    
    print("\n✅ AVAILABLE MODELS FOR YOU:")
    print("-" * 40)
    
    # Google se pucho ki list do
    for m in client.models.list():
        # Sirf wo models dikhao jo content generate kar sakte hain
        if "generateContent" in m.supported_actions:
            print(f"👉 {m.name}")
            
    print("-" * 40)
    print("TIP: Upar di gayi list mein se koi ek naam chuno.")

except Exception as e:
    print(f"❌ ERROR: {e}")