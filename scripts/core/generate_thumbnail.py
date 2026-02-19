import os
import json
import requests
import time
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import urllib.parse
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Paths
OUTPUT_PATH = "output/shorts/thumbnail.jpg"
TEMP_IMG = "temp/raw_thumb.jpg"

# ✅ FIXED: Correct Router URL for Stable Diffusion XL (Free & High Quality)
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_thumbnail_image(prompt):
    print(f"🎨 Generating Thumbnail Background: '{prompt[:40]}...'")
    
    if not HF_TOKEN:
        print("❌ Error: HF_TOKEN missing! Thumbnail skipped.")
        return False

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Professional Prompt Engineering for High CTR
    enhanced_prompt = (
        f"youtube thumbnail background, {prompt}, ancient indian vedic mystery, "
        f"hyper-realistic, 8k resolution, dramatic lighting, "
        f"glowing eyes, dark moody atmosphere, cinematic composition, masterpiece"
    )
    
    payload = {"inputs": enhanced_prompt}

    for attempt in range(3): # Retry logic
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                with open(TEMP_IMG, 'wb') as f:
                    f.write(response.content)
                print("      ✅ Background Generated.")
                return True
            
            elif response.status_code == 503:
                print("      ⏳ Model loading... waiting 15s...")
                time.sleep(15)
                continue
            
            else:
                print(f"      ❌ HF Error {response.status_code}")
                break
                
        except Exception as e:
            print(f"      ❌ Connection Error: {e}")
            time.sleep(5)
            
    return False

def add_text_to_thumbnail(text):
    print(f"✍️ Adding Viral Text: '{text}'")
    try:
        if not os.path.exists(TEMP_IMG):
            return False

        img = Image.open(TEMP_IMG).convert("RGBA")
        # Resize to YouTube Shorts / Reel Ratio (9:16) -> 1080x1920
        img = img.resize((1080, 1920))
        
        # Create a transparent overlay for text
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # --- FONT LOGIC (Windows Safe) ---
        try:
            # Try Bold Arial first
            font = ImageFont.truetype("arialbd.ttf", 90)
        except:
            try:
                # Fallback to standard Arial
                font = ImageFont.truetype("arial.ttf", 90)
            except:
                # Last resort
                print("⚠️ Warning: Arial font not found, using default.")
                font = ImageFont.load_default()

        # --- TEXT WRAPPING ---
        # Simple logic to break long lines
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            # Break line every 2-3 words depending on length
            if len(" ".join(current_line)) > 12: 
                lines.append(" ".join(current_line))
                current_line = []
        if current_line: lines.append(" ".join(current_line))

        # --- DRAWING ---
        # Draw a dark gradient box at the bottom for readability
        # Box starts at Y=1200
        draw.rectangle([0, 1100, 1080, 1920], fill=(0, 0, 0, 180))

        # Text Positioning
        y_text = 1300
        for line in lines:
            # Calculate width to center text
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x_text = (1080 - text_width) / 2
            
            # 1. Black Stroke (Outline) for visibility
            stroke_width = 4
            for adj_x in range(-stroke_width, stroke_width+1):
                for adj_y in range(-stroke_width, stroke_width+1):
                    draw.text((x_text+adj_x, y_text+adj_y), line, font=font, fill="black")

            # 2. Main Yellow/Gold Text
            draw.text((x_text, y_text), line, font=font, fill="#FFD700") # Gold color
            
            y_text += 110 # Line height

        # Merge and Save
        final_img = Image.alpha_composite(img, overlay)
        final_img = final_img.convert("RGB") # Remove alpha for JPEG
        
        # Ensure output folder exists
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        final_img.save(OUTPUT_PATH, quality=95)
        
        print(f"✅ Final Thumbnail Saved: {OUTPUT_PATH}")
        return True

    except Exception as e:
        print(f"❌ Text Overlay Error: {e}")
        return False

def create_thumbnail():
    script_path = "temp/latest_script.json"
    if not os.path.exists(script_path): 
        print("❌ Script file missing.")
        return

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Topic for Image, Hook for Text
        topic = data.get("title", "Vedic Mystery")
        # Hook ka sirf pehla sentence ya 4-5 words lo
        raw_hook = data.get("hook", "Unsolved Mystery")
        short_hook = " ".join(raw_hook.split()[:5]).replace('"', '').upper()

        if generate_thumbnail_image(topic):
            add_text_to_thumbnail(short_hook)
            
    except Exception as e:
        print(f"❌ Thumbnail Logic Error: {e}")

if __name__ == "__main__":
    create_thumbnail()