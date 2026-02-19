import os
import random
import json
from moviepy.editor import *
from moviepy.video.fx.all import resize, speedx, fadein

# Config
ASSETS_DIR = "assets/visuals"
AUDIO_FILE = "temp/voiceover.mp3"
SCRIPT_FILE = "temp/latest_script.json"
BGM_DIR = "assets/audio/background_music"
OUTPUT_FILE = "output/shorts/final_short.mp4"

def create_short_video():
    print("🎬 Starting Cinematic Editing (Professional Mode)...")
    
    # 1. Check Voiceover
    if not os.path.exists(AUDIO_FILE): 
        print("❌ Voiceover missing! Cannot render.")
        return
        
    voiceover = AudioFileClip(AUDIO_FILE)
    
    # 2. Load Visual Plan
    visual_plan = []
    if os.path.exists(SCRIPT_FILE):
        with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
            visual_plan = json.load(f).get("visual_plan", [])

    # 3. Gather Asset Paths
    # Hum map banayenge taaki script ke hisab se sahi asset mile
    image_files = sorted([os.path.join(f"{ASSETS_DIR}/raw_images", f) for f in os.listdir(f"{ASSETS_DIR}/raw_images") if f.endswith('.jpg')])
    video_files = sorted([os.path.join(f"{ASSETS_DIR}/video_clips", f) for f in os.listdir(f"{ASSETS_DIR}/video_clips") if f.endswith('.mp4')])
    
    asset_map = {}
    for f in image_files + video_files:
        try: 
            # File name format: asset_01.jpg -> index 1
            idx = int(f.split('_')[-1].split('.')[0])
            asset_map[idx] = f
        except: pass

    # 4. Create Clips
    clips = []
    default_dur = 4 # Fallback duration
    
    # Kitne scenes banane hain? (Script items ya Assets count)
    total_scenes = len(visual_plan) if visual_plan else len(asset_map)

    for i in range(total_scenes):
        idx = i + 1
        filepath = asset_map.get(idx)
        
        # Backup: Agar asset missing hai to koi random utha lo
        if not filepath and asset_map: 
            filepath = random.choice(list(asset_map.values()))
            
        if not filepath: continue

        # Duration logic
        clip_duration = visual_plan[i].get("duration", default_dur) if i < len(visual_plan) else default_dur

        try:
            if filepath.endswith(".mp4"):
                # --- VIDEO PROCESSING ---
                clip = VideoFileClip(filepath)
                
                # Cinematic Slow Mo (0.9x)
                clip = clip.fx(speedx, 0.9)
                
                # Loop if short
                if clip.duration < clip_duration: 
                    clip = vfx.loop(clip, duration=clip_duration)
                else: 
                    clip = clip.subclip(0, clip_duration)
                
                # CROP 9:16 (Center)
                target_ratio = 9/16
                current_ratio = clip.w / clip.h
                
                if current_ratio > target_ratio:
                    # Too wide -> Crop width
                    new_width = clip.h * target_ratio
                    clip = clip.crop(x1=clip.w/2 - new_width/2, width=new_width, height=clip.h)
                
                # Resize to HD Vertical
                clip = clip.resize(height=1920)
                clip = clip.fadein(0.5)
                
            else:
                # --- IMAGE PROCESSING ---
                clip = ImageClip(filepath).set_duration(clip_duration)
                
                # Pan/Zoom Effect (Ken Burns)
                # Image ko thoda bada karke zoom karenge
                clip = clip.resize(height=2300) 
                clip = clip.crop(x1=clip.w/2 - 540, y1=clip.h/2 - 960, width=1080, height=1920)
                
                # Slight Zoom Animation
                clip = clip.resize(lambda t : 1 + 0.02 * t) 
                clip = clip.fadein(0.5)

            clips.append(clip)
        except Exception as e:
            print(f"⚠️ Skipped asset {idx}: {e}")

    if not clips:
        print("❌ No clips generated.")
        return

    # ... (Upar ka code same rahega) ...

    # 5. Concatenate
    final_video = concatenate_videoclips(clips, method="compose")
    
    # 6. Audio Sync (Natural Ending)
    # 🔥 CHANGE: Hum video ko sirf tabhi katenge agar wo Audio se lambi ho.
    # Hum 59s ka hard cut nahi lagaenge.
    if final_video.duration > voiceover.duration:
        final_video = final_video.subclip(0, voiceover.duration)
    else:
        # Agar video choti hai audio se, to last frame ko extend kar do
        final_video = final_video.set_duration(voiceover.duration)

    # 7. Add BGM (From your folder)
    # Aapke folder se koi bhi random mp3 utha lega
    bgm_files = [f for f in os.listdir(BGM_DIR) if f.endswith('.mp3')]
    final_audio = voiceover
    
    if bgm_files:
        bgm_path = os.path.join(BGM_DIR, random.choice(bgm_files)) # Random pick from your folder
        print(f"      🎵 Adding BGM: {os.path.basename(bgm_path)}")
        
        bgm = AudioFileClip(bgm_path)
        
        # Loop music to match video
        if bgm.duration < final_video.duration:
            bgm = afx.audio_loop(bgm, duration=final_video.duration)
        else:
            bgm = bgm.subclip(0, final_video.duration)
            
        bgm = bgm.volumex(0.15) # Volume Low
        final_audio = CompositeAudioClip([voiceover, bgm])

    final_video = final_video.set_audio(final_audio)
    
    # 8. Render
    print("🚀 Rendering Final Video...")
    final_video.write_videofile(
        OUTPUT_FILE, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac", 
        bitrate="5000k", 
        preset="ultrafast",
        threads=4
    )
    print(f"✅ Video Ready: {OUTPUT_FILE}")