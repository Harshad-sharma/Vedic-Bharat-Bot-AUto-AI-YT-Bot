import os
import sys
import json
import time
import logging
import io

# --- FIX 1: WINDOWS EMOJI CRASH FIX ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# --- FIX 2: LOGGING TO FILE ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_history.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def log(msg):
    logging.info(msg)

# Import Core Modules (Instagram Removed for Stability)
try:
    from scripts.core.brainstorm import get_unique_topic
    from scripts.core.generate_script import generate_viral_script
    from scripts.core.gather_visuals import generate_visuals_from_script
    from scripts.core.script_normalizer import normalize_script
    from scripts.core.edit_video import create_short_video
    from scripts.core.generate_seo import generate_seo_data 
    from scripts.core.generate_thumbnail import create_thumbnail 
    from scripts.core.youtube_uploader import upload_to_youtube
except ImportError as e:
    log(f"❌ CRITICAL IMPORT ERROR: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

def run_automation():
    log("==========================================")
    log("🚀 VEDIC BHARAT BOT - SINGLE VIDEO MODE")
    log("==========================================")

    # 1) Topic with Retry
    topic = None
    for attempt in range(3):
        try:
            topic = get_unique_topic()
            if topic: break
        except Exception as e:
            log(f"⚠️ Topic Error (Attempt {attempt+1}): {e}")
            time.sleep(5)
            
    if not topic:
        log("❌ Critical: Topic generation failed after 3 attempts.")
        return
    log(f"🎯 Locked Topic: {topic}")

    # 2) Script
    script_data = generate_viral_script(topic)
    if not script_data:
        log("❌ Script generation failed.")
        return

    script_data = normalize_script(script_data)

    os.makedirs("temp", exist_ok=True)
    with open("temp/latest_script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=4, ensure_ascii=False)

    # 3) Audio
    log("🎤 Starting Audio Engine...")
    try:
        exit_code = os.system("python scripts/core/generate_audio.py")
        if exit_code != 0: 
            log("⚠️ Audio script returned a warning (Check logs).")
    except Exception as e:
        log(f"⚠️ Audio execution error: {e}")

    # 4) Visuals & SEO & Thumbnail
    try:
        generate_visuals_from_script(script_data)
        generate_seo_data()
        create_thumbnail()
        log("✅ PHASE 1 COMPLETE: All Assets Ready!")
    except Exception as e:
        log(f"❌ Asset Generation Failed: {e}")
        return

    # 5) Video Render
    log("🎬 Rendering Final Video...")
    try:
        create_short_video() 
        log("✅ VIDEO RENDERED SUCCESSFULLY!")
    except Exception as e:
        log(f"❌ Rendering Failed: {e}")
        return

    # 6) UPLOAD (YouTube Only)
    log("📤 Starting Upload Process...")
    
    # Path Verification
    video_path = os.path.abspath("output/shorts/final_short.mp4")
    
    if not os.path.exists(video_path):
        log(f"❌ Upload Failed: File not found at {video_path}")
        return

    # YouTube Upload
    try:
        log(f"🚀 Uploading to YouTube: {video_path}")
        yt_id = upload_to_youtube(video_path) 
        if yt_id: 
            log(f"📺 YouTube Success! Video ID: {yt_id}")
        else:
            log("⚠️ YouTube Upload returned no ID (Check youtube_uploader logs).")
    except Exception as e:
        log(f"❌ YouTube Crash: {e}")

    log("==========================================")
    log("🎉 MISSION COMPLETE. LOGS SAVED.")
    log("==========================================")

if __name__ == "__main__":
    try:
        run_automation()
    except Exception as e:
        log(f"❌ FATAL ERROR IN MAIN LOOP: {e}")
    
    print("\nProcess finished.")
    # input("Press Enter to close window...") # Uncomment if you want window to stay open