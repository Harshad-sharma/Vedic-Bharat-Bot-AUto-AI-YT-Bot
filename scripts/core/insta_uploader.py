import os
import json
import time
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired, FeedbackRequired
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("INSTA_USER")
PASSWORD = os.getenv("INSTA_PASS")
SESSION_FILE = "insta_session.json"

def upload_to_instagram(video_path):
    print("📸 Preparing Instagram Upload (Smart Session Mode)...")
    
    # 1. Check Video
    if not os.path.exists(video_path):
        print("❌ Video file missing!")
        return False

    # 2. Prepare Caption
    caption = "Vedic Bharat #Shorts #Sanatan #Mystery"
    seo_path = "temp/seo_data.json"
    if os.path.exists(seo_path):
        try:
            with open(seo_path, "r", encoding="utf-8") as f:
                seo = json.load(f)
                # Clean text to avoid encoding errors
                title = seo.get('titles', ['Vedic Video'])[0]
                tags = seo.get('hashtags', '#Vedic')
                caption = f"{title}\n.\n{tags}"
        except: pass

    # 3. SMART LOGIN (With Session Saving)
    cl = Client()
    
    try:
        # Step A: Try loading old session
        if os.path.exists(SESSION_FILE):
            print("🔄 Loading saved session...")
            cl.load_settings(SESSION_FILE)
        
        # Step B: Login
        print("🔑 Logging in...")
        try:
            cl.login(USERNAME, PASSWORD)
        except ChallengeRequired:
            print("\n🚨 INSTAGRAM CHALLENGE DETECTED! 🚨")
            print("1. Please open Instagram App on your phone NOW.")
            print("2. You will see 'Was this you?' or a Code request.")
            print("3. Click 'Yes, It was me'.")
            print("4. Waiting 60 seconds for you to verify...")
            time.sleep(60)
            print("🔄 Retrying Login...")
            cl.login(USERNAME, PASSWORD)

        # Step C: Check if login worked
        if cl.user_id:
            print("✅ Login Successful! Saving session...")
            cl.dump_settings(SESSION_FILE) # Save for next time
        
        # 4. UPLOAD
        print("📤 Uploading Reel (This may take time)...")
        media = cl.clip_upload(
            path=video_path,
            caption=caption
        )
        
        print(f"✅ Instagram Success! Code: {media.code}")
        return True

    except Exception as e:
        print(f"❌ Instagram Error: {e}")
        # Agar session kharab hai to delete kar do taaki next time fresh login ho
        if os.path.exists(SESSION_FILE) and "login" in str(e).lower():
            os.remove(SESSION_FILE)
            print("⚠️ Invalid Session deleted. Will try fresh login next time.")
        return False