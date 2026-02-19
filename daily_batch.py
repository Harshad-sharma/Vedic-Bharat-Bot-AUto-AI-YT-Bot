import os
import json
import time
import shutil
import sys
import io
import logging
from datetime import datetime, timedelta

# --- FIX: WINDOWS EMOJI CRASH FIX (CRITICAL) ---
# Ye magic lines Windows console ko UTF-8 mode me force karengi
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("batch_history.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def log(msg):
    logging.info(msg)

# Import Core Modules
try:
    from scripts.core.brainstorm import get_unique_topic
    from scripts.core.generate_script import generate_viral_script
    from scripts.core.gather_visuals import generate_visuals_from_script
    from scripts.core.script_normalizer import normalize_script
    from scripts.core.edit_video import create_short_video
    from scripts.core.generate_seo import generate_seo_data 
    from scripts.core.generate_thumbnail import create_thumbnail 
    from scripts.core.youtube_uploader import upload_to_youtube
    from scripts.core.insta_uploader import upload_to_instagram
except ImportError as e:
    log(f"❌ Import Error: {e}")
    sys.exit(1)

# Config
TOTAL_VIDEOS = 6
START_DELAY_HOURS = 2 
GAP_HOURS = 4 

def clean_temp():
    if os.path.exists("temp"):
        for f in os.listdir("temp"):
            if f.endswith(".json") or f.endswith(".mp3") or f.endswith(".jpg"):
                try: os.remove(os.path.join("temp", f))
                except: pass

def run_batch():
    log("==========================================")
    log(f"🚀 VEDIC BHARAT PRODUCT LAUNCHED ({TOTAL_VIDEOS} Videos/Day)")
    log("==========================================")

    current_time = datetime.utcnow()
    
    for i in range(TOTAL_VIDEOS):
        log(f"\n🎬 STARTING PRODUCTION: VIDEO #{i+1}")
        clean_temp()
        
        # 1. Topic (With Backup)
        topic = get_unique_topic()
        if not topic: 
            log("❌ Topic failed. Skipping.")
            continue
        log(f"🎯 Topic: {topic}")

        # 2. Script
        script_data = generate_viral_script(topic)
        if not script_data: continue
        
        script_data = normalize_script(script_data)
        os.makedirs("temp", exist_ok=True)
        with open("temp/latest_script.json", "w", encoding="utf-8") as f:
            json.dump(script_data, f, indent=4)

        # 3. Audio & Visuals (New Features Active)
        log("🎤 Generating Deep Voice...")
        if os.system("python scripts/core/generate_audio.py") != 0:
            log("❌ Audio script failed.")
            continue
            
        log("👁️ Gathering Smart Visuals...")
        try:
            generate_visuals_from_script(script_data)
            generate_seo_data()
            create_thumbnail()
        except Exception as e:
            log(f"⚠️ Asset Error: {e}")

        # 4. Render
        log("⚙️ Rendering Cinematic Video...")
        try:
            create_short_video()
        except Exception as e:
            log(f"❌ Render Error: {e}")
            continue

        video_path = "output/shorts/final_short.mp4"
        batch_filename = f"output/shorts/batch_video_{i+1}.mp4"
        
        if os.path.exists(video_path):
            shutil.move(video_path, batch_filename)
        else:
            log("❌ Final video file missing. Skipping upload.")
            continue

        # 5. UPLOAD & SCHEDULE
        schedule_time = current_time + timedelta(hours=START_DELAY_HOURS + (i * GAP_HOURS))
        log(f"⏰ Schedule Time: {schedule_time}")
        
        # YouTube
        yt_id = upload_to_youtube(batch_filename, schedule_dt=schedule_time)
        if yt_id: log(f"✅ YouTube Scheduled: {yt_id}")
        
       

    log("\n==========================================")
    log("😴 BATCH FINISHED. System going to sleep.")
    log("==========================================")

if __name__ == "__main__":
    try:
        run_batch()
    except Exception as e:
        log(f"❌ FATAL ERROR: {e}")
        input("Press Enter to exit...")