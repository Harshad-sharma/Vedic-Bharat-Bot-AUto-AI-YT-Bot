

import os

# 1. Project Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_FOLDER = os.path.join(BASE_DIR, "Assets")
MEDIA_FOLDER = os.path.join(ASSETS_FOLDER, "Visuals")
AUDIO_FOLDER = os.path.join(ASSETS_FOLDER, "Audio")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "Output_Videos")

# Folders automatically create karna (Professional approach)
os.makedirs(MEDIA_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 2. API KEYS (यहाँ अपनी असली Keys डालनी हैं)
# Gemini API Key (Script ke liye)
GEMINI_API_KEY = "AIzaSyAqDxD_IuWyno-4k3GsI3Nn9uyJ6lM0hCE"
PIXABAY_API_KEY = "31461744-a7ab646003d17e83b64b53b61"
PEXELS_API_KEY = "WpP0tfIORhZnH7yiCYuhjbtOEPHbTshlYYHIzBy4YQamuE7hvZwxaqeg" 

# --- 2. INSTAGRAM LOGIN (Real) ---
INSTA_USER = "madhavshree23"
INSTA_PASS = "7354002961"

# 3. Channel Settings
CHANNEL_NAME = "Vaidic Bharat 108"
VIDEO_LANGUAGE = "hi" # Hindi
DAILY_LIMIT = 6

# 4. Production Settings
PRODUCTION_MODE = True
API_DAILY_LIMIT = 18
API_HIT_COUNT = 0
USE_FALLBACK_ONLY = False
