import os
import json
import asyncio
import edge_tts
from dotenv import load_dotenv

load_dotenv()

# Voice Settings
VOICE = 'hi-IN-SwaraNeural'
RATE = '+25%'  # Speed thodi fast rakhi hai viral shorts ke liye
PITCH = '+0Hz'

async def generate_voiceover():
    print("🎤 Starting Audio Engine (Fast Mode - No Captions)...")

    script_path = "temp/latest_script.json"
    output_audio = "temp/voiceover.mp3"

    if not os.path.exists(script_path):
        print("❌ Error: Script file not found!")
        return

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Clean Text
        raw_text = f"{data.get('hook', '')} {data.get('body', '')} {data.get('cta', '')}"
        clean_text = raw_text.replace("*", "").replace("#", "").strip()

        print(f"🔄 Generating Audio ({len(clean_text)} chars)...")

        # Generate Audio Only (No Subtitles)
        communicate = edge_tts.Communicate(clean_text, VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(output_audio)
        print(f"✅ Audio Created: {output_audio}")

    except Exception as e:
        print(f"❌ Audio Error: {e}")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(generate_voiceover())