import os
from dotenv import load_dotenv

load_dotenv()

# 1. Project Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_FOLDER = os.path.join(BASE_DIR, "Assets")
MEDIA_FOLDER = os.path.join(ASSETS_FOLDER, "Visuals")
AUDIO_FOLDER = os.path.join(ASSETS_FOLDER, "Audio")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output_Videos")

os.makedirs(MEDIA_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 2. API KEYS (अब .env से लेंगे)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Instagram (optional - अगर रखना हो तो .env में डालो)
INSTA_USER = os.getenv("INSTA_USER")
INSTA_PASS = os.getenv("INSTA_PASS")

# 3. Channel Settings
CHANNEL_NAME = "Vaidic Bharat 108"
VIDEO_LANGUAGE = "hi"
DAILY_LIMIT = 6

# 4. Production Settings
PRODUCTION_MODE = True
API_DAILY_LIMIT = 18
API_HIT_COUNT = 0
USE_FALLBACK_ONLY = False
