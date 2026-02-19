import os
import json
import pickle
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "temp/token.pickle"
CLIENT_SECRETS_FILE = "client_secrets.json"
SEO_FILE = "temp/seo_data.json"
LOG_FILE = "temp/upload_history.json"

# 🗓️ 6 DISTINCT SLOTS FOR 6 VIDEOS
DAILY_SLOTS = [
    (8, 0),   # 08:00 AM 
    (10, 30), # 10:30 AM 
    (13, 0),  # 01:00 PM 
    (16, 0),  # 04:00 PM 
    (18, 30), # 06:30 PM 
    (21, 0)   # 09:00 PM 
]

def get_smart_slot():
    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    
    history = {}
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f: history = json.load(f)
        except: pass
        
    todays_uploads = history.get(today_str, [])
    
    for hour, minute in DAILY_SLOTS:
        slot_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        time_str = f"{hour:02d}:{minute:02d}"
        
        if time_str not in todays_uploads and slot_dt > now:
            print(f"📅 Smart Scheduler: Booking Slot {time_str}")
            todays_uploads.append(time_str)
            history[today_str] = todays_uploads
            with open(LOG_FILE, "w") as f: json.dump(history, f)
            return slot_dt

    tomorrow = now + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    first_slot = DAILY_SLOTS[0]
    
    print(f"📅 Smart Scheduler: Today full. Booking Tomorrow {first_slot[0]:02d}:{first_slot[1]:02d}")
    history[tomorrow_str] = [f"{first_slot[0]:02d}:{first_slot[1]:02d}"]
    with open(LOG_FILE, "w") as f: json.dump(history, f)
    
    return tomorrow.replace(hour=first_slot[0], minute=first_slot[1], second=0)

def get_authenticated_service():
    credentials = None
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print("❌ CRITICAL: 'client_secrets.json' missing in main folder.")
        return None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("🔄 Refreshing Expired Token...")
            credentials.refresh(Request())
        else:
            print("🆕 Need New Login! Opening Browser...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def upload_to_youtube(video_path, schedule_dt=None):
    print("📺 Preparing YouTube Upload Process...")
    
    if not schedule_dt:
        schedule_dt = get_smart_slot()
        
    if not os.path.exists(video_path):
        print(f"❌ Video file missing: {video_path}")
        return None

    # Load SEO
    if os.path.exists(SEO_FILE):
        with open(SEO_FILE, "r", encoding="utf-8") as f: seo = json.load(f)
    else:
        seo = {"titles": ["Vedic Bharat Shorts"], "description": "Ancient India", "hashtags": "#Shorts", "tags_list": "shorts, vedic"}

    youtube = get_authenticated_service()
    if not youtube:
        print("❌ Authentication Failed.")
        return None

    # ✅ Indian Timezone (IST) fix for YouTube API
    publish_at = schedule_dt.isoformat() + '+05:30'

    title = seo.get('titles', ["Vedic Shorts"])[0][:100]
    desc = f"{seo.get('description', '')}\n\n{seo.get('hashtags', '')}"
    tags = seo.get('tags_list', '').split(", ")

    body = {
        "snippet": {
            "title": title,
            "description": desc,
            "tags": tags,
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"🚀 Uploading & Scheduling for: {schedule_dt.strftime('%I:%M %p')} (IST)")

    try:
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status: 
                print(f"    Uploading... {int(status.progress() * 100)}%")

        print(f"✅ Success! Scheduled perfectly. Video ID: {response['id']}")
        return response['id']

    except HttpError as e:
        print(f"❌ YouTube API Error: {e}")
        return None