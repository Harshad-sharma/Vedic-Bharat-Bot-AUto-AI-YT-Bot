import os
import json
import datetime
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ✅ TUMHARI LIST (Strictly only these models)
MODEL_POOL = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-tts",
    "gemma-3-1b-it",
    "gemma-3-4b-it",
    "gemma-3-12b-it",
    "gemma-3-27b-it",
    "gemma-3n-e4b-it",
    "gemma-3n-e2b-it",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-3-pro-preview",
    "gemini-3-flash-preview"
]

STATE_FILE = "temp/model_state.json"

def get_smart_client():
    # State Load
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try: state = json.load(f)
            except: state = {}

    today = str(datetime.date.today())
    
    # Reset failures on new day
    if state.get("last_run_date") != today:
        state = {"last_run_date": today, "failed_models": [], "current_index": 0}

    failed_list = state.get("failed_models", [])
    current_idx = state.get("current_index", 0)

    # Find next working model
    selected_model = None
    attempts = 0
    total_models = len(MODEL_POOL)
    
    while attempts < total_models:
        model_name = MODEL_POOL[current_idx % total_models]
        
        if model_name not in failed_list:
            selected_model = model_name
            # Update Index for next time
            state["current_index"] = (current_idx + 1) % total_models
            break
            
        # 🔥 FIX: Ye +5 tha, isko +1 kar diya taaki koi model skip na ho
        current_idx += 1
        attempts += 1
    
    # Save State
    with open(STATE_FILE, "w") as f: json.dump(state, f)
    
    # Agar sab fail ho gaye, to wapis pehle wale ko utha lo (Desperate Mode)
    if not selected_model:
        selected_model = "gemini-2.5-flash" 
        # Reset failed list kyunki shayad quota wapis aa gaya ho
        state["failed_models"] = [] 
        with open(STATE_FILE, "w") as f: json.dump(state, f)

    client = genai.Client(api_key=api_key)
    return client, selected_model

def report_failure(model_name):
    print(f"⚠️ Model Failed: {model_name}. Marking as cooldown for today.")
    
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try: state = json.load(f)
            except: state = {}
        
    failed = state.get("failed_models", [])
    if model_name not in failed:
        failed.append(model_name)
        
    state["failed_models"] = failed
    with open(STATE_FILE, "w") as f: json.dump(state, f)