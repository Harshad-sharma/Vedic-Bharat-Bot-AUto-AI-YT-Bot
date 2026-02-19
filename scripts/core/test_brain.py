import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. लोड करें सीक्रेट चाबियाँ (Keys)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. चेक करें कि की (Key) मिली या नहीं
if not api_key:
    print("❌ Error: API Key nahi mili! .env file check karein.")
    exit()

# 3. दिमाग (Brain) को कॉन्फ़िगर करें
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash') # Flash model fast aur free hai

# 4. बोट से प्रश्न पूछें (Test Prompt)
print("🤖 Bot soch raha hai... (Thinking about Sanatan Dharma)")

try:
    response = model.generate_content(
        "Tum ek Vedic Scholar AI ho. Mujhe 'Sanatan Dharma' ka ek aisa 'Scientific Fact' batao "
        "jo bahut kam log jante hain. Jawab sirf 2 line mein Hindi mein do."
    )
    
    print("\n✨ BOT KA JAWAB:\n")
    print(response.text)
    print("\n✅ Test Successful! Dimag kaam kar raha hai.")

except Exception as e:
    print(f"\n❌ Error aagaya: {e}")