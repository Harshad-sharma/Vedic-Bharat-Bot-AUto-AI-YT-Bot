import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key nahi mili! .env file check karein.")
    exit()

genai.configure(api_key=api_key)

print("🔍 Analyzing Available Models & Limits...\n")

# --- OFFICIAL FREE TIER LIMITS (Google Documentation ke hisab se) ---
# Note: Ye limits Google change karta rehta hai, par abhi ye standard hain.
LIMITS_DB = {
    "gemini-1.5-flash":  {"rpm": 15, "rpd": 1500, "desc": "⚡ FASTEST & BEST FOR DEV"},
    "gemini-1.5-pro":    {"rpm": 2,  "rpd": 50,   "desc": "🧠 SMARTEST BUT SLOW"},
    "gemini-2.0-flash":  {"rpm": 10, "rpd": 1500, "desc": "🚀 NEW (Experimental)"},
    "gemini-1.0-pro":    {"rpm": 15, "rpd": 1500, "desc": "👴 OLD STABLE"},
}

try:
    models = genai.list_models()
    found_any = False
    
    print(f"{'MODEL NAME':<35} | {'INPUT LIMIT':<12} | {'OUTPUT LIMIT':<12} | {'ESTIMATED RATE LIMIT (Free)'}")
    print("-" * 110)

    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            found_any = True
            
            # Token limits API se milte hain
            input_limit = m.input_token_limit
            output_limit = m.output_token_limit
            
            # Rate limits humare Database se match karenge
            rate_info = "Unknown Limit"
            for key, val in LIMITS_DB.items():
                if key in m.name:
                    rate_info = f"{val['rpm']} RPM | {val['rpd']} RPD ({val['desc']})"
                    break
            
            print(f"{m.name:<35} | {input_limit:<12} | {output_limit:<12} | {rate_info}")

    print("-" * 110)
    print("\n📝 LEGEND:")
    print("   RPM = Requests Per Minute (Ek minute mein kitni baar bula sakte hain)")
    print("   RPD = Requests Per Day (Ek din mein kitni baar bula sakte hain)")

except Exception as e:
    print(f"❌ Error: {e}")