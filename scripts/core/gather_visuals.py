import os
import json
import requests
import random
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
PEXELS_KEY = os.getenv("PEXELS_API_KEY")
PIXABAY_KEY = os.getenv("PIXABAY_API_KEY")

# Paths
IMAGE_DIR = "assets/visuals/raw_images"
VIDEO_DIR = "assets/visuals/video_clips"
AUDIO_DIR = "assets/audio/background_music"

def clear_previous_assets():
    print("🧹 Cleaning old assets...")
    for folder in [IMAGE_DIR, VIDEO_DIR, AUDIO_DIR]:
        os.makedirs(folder, exist_ok=True)
        for filename in os.listdir(folder):
            try: os.unlink(os.path.join(folder, filename))
            except: pass

# --- POLLINATIONS AI (Safe & Free) ---
def generate_ai_image(prompt, filename):
    print(f"      🎨 AI Painting (Strict Vedic): '{prompt[:20]}...'")
    
    # 🔥 FORCE VEDIC STYLE
    enhanced_prompt = f"ancient hindu {prompt}, vedic scriptures, sanskrit text, saffron colors, indian temple architecture, 8k, hyper-realistic, cinematic lighting"
    
    # Anti-Islamic Negative Prompt Logic (URL Hack)
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    
    # Seed randomizing for variety
    seed = random.randint(1, 10000)
    
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&model=flux&nologo=true&seed={seed}"
    
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(filename, 'wb') as f: f.write(response.content)
            print(f"      ✅ AI Image Saved.")
            return True
    except: pass
    return False

def download_stock_media(query, filename, is_video=True):
    # 🛡️ 1. RELIGIOUS FILTER (Strict Ban)
    banned_keywords = ["islam", "urdu", "arabic", "quran", "mosque", "dome", "green flag", "minaret"]
    
    if any(word in query.lower() for word in banned_keywords):
        print(f"      🛡️ BLOCKED NON-VEDIC QUERY: {query}")
        query = "ancient hindu temple architecture" # Safe Replacement

    # 🎨 2. SMART SWITCH: Text/Scripture -> AI Image
    # Stock sites par 'ancient script' mangne par aksar Urdu aati hai.
    # Isliye agar script mangi hai, to AI se Sanskrit banwao.
    text_triggers = ["text", "script", "writing", "book", "shloka", "mantra", "leaf"]
    if any(trigger in query.lower() for trigger in text_triggers):
        print(f"      🧠 Smart Visuals: '{query}' needs text. Using AI instead of Stock Video.")
        # Filename extension change karo (.mp4 -> .jpg)
        filename = filename.replace(".mp4", ".jpg") 
        return generate_ai_image(query, filename)

    # --- NORMAL STOCK DOWNLOAD LOGIC ---
    search_query = f"{query} ancient india hindu"
    print(f"      🌍 Stock Search: '{query[:15]}...'")

    # Try Pexels
    if Pexels_Download(search_query, filename, is_video): return True
    # Try Pixabay
    if Pixabay_Download(search_query, filename, is_video): return True
    
    # Agar Stock nahi mila -> To AI Image bana do (Fallback)
    filename = filename.replace(".mp4", ".jpg")
    return generate_ai_image(query, filename)

# --- HELPER FUNCTIONS ---
def Pexels_Download(query, filename, is_video):
    if not PEXELS_KEY: return False
    try:
        headers = {"Authorization": PEXELS_KEY}
        base = "https://api.pexels.com/videos/search" if is_video else "https://api.pexels.com/v1/search"
        url = f"{base}?query={query}&per_page=1&orientation=portrait"
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        link = None
        if is_video and data.get('videos'): link = data['videos'][0]['video_files'][0]['link']
        elif not is_video and data.get('photos'): link = data['photos'][0]['src']['large2x']
        if link:
            with open(filename, 'wb') as f: f.write(requests.get(link).content)
            print("      ✅ Pexels Asset Saved.")
            return True
    except: pass
    return False

def Pixabay_Download(query, filename, is_video):
    if not PIXABAY_KEY: return False
    try:
        base = "https://pixabay.com/api/videos/" if is_video else "https://pixabay.com/api/"
        url = f"{base}?key={PIXABAY_KEY}&q={query}&per_page=3"
        r = requests.get(url, timeout=10)
        data = r.json()
        link = None
        if is_video and data.get('hits'): link = data['hits'][0]['videos']['medium']['url']
        elif not is_video and data.get('hits'): link = data['hits'][0]['largeImageURL']
        if link:
            with open(filename, 'wb') as f: f.write(requests.get(link).content)
            print("      ✅ Pixabay Asset Saved.")
            return True
    except: pass
    return False

def download_background_music():
    # Folder check logic (Same as before)
    if os.path.exists(AUDIO_DIR):
        files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
        if files: return
    # Fallback
    try:
        r = requests.get("https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3")
        with open(f"{AUDIO_DIR}/bg_music.mp3", 'wb') as f: f.write(r.content)
    except: pass

def generate_visuals_from_script(script_data):
    clear_previous_assets()
    download_background_music()
    
    if not isinstance(script_data, dict):
        if os.path.exists("temp/latest_script.json"):
            with open("temp/latest_script.json", "r") as f: script_data = json.load(f)
        else: script_data = {}

    visual_plan = script_data.get("visual_plan", [])
    print(f"🚀 Collecting {len(visual_plan)} Assets...")

    for i, item in enumerate(visual_plan):
        query = item.get("query", "Ancient India")
        is_character = any(x in query.lower() for x in ["god", "shiva", "ram", "krishna", "face", "king", "sushruta"])
        
        filename = f"{IMAGE_DIR if is_character else VIDEO_DIR}/asset_{i+1:02d}.{'jpg' if is_character else 'mp4'}"
        
        if is_character:
            if not generate_ai_image(query, filename):
                download_stock_media(query, filename, is_video=False)
        else:
            download_stock_media(query, filename, is_video=True)
            
    print("✨ Visuals Collection Complete!")

if __name__ == "__main__":
    generate_visuals_from_script(None)