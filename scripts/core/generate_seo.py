import os
import json
import re
import time
from scripts.core.ai_rotator import get_smart_client, report_failure

def generate_seo_data():
    print("📝 Generating Viral SEO (Smart Mode)...")
    
    script_path = "temp/latest_script.json"
    output_path = "temp/seo_data.json"

    # Agar script hi nahi hai, to SEO kiska banaye?
    if not os.path.exists(script_path):
        print("❌ Script file missing.")
        return None

    try:
        # Script padho (Isko loop ke bahar rakha hai taaki baar-baar file na padhe)
        with open(script_path, "r", encoding="utf-8") as f:
            script_data = json.load(f)
            
        script_body = script_data.get('body', '')
        
        # 🔥 ZIDDI LOOP START
        max_retries = 15
        attempt = 0
        
        while attempt < max_retries:
            # 🧠 Smart AI Client (Har attempt me naya model aayega)
            client, model_name = get_smart_client()
            print(f"      🤖 SEO using {model_name} (Attempt {attempt+1})...")

            prompt = f"""
            Based on this Hindi Script: "{script_body[:500]}..."
            
            Generate YouTube Shorts Metadata.
            
            OUTPUT JSON FORMAT:
            {{
                "titles": ["Title 1", "Title 2", "Title 3"],
                "description": "Write a 2-line description with keywords.",
                "hashtags": "#tag1 #tag2 #tag3 #shorts #vedic",
                "tags_list": "tag1, tag2, tag3, tag4"
            }}
            """

            try:
                # API Call
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                # Cleaning Response
                text = response.text.replace("```json", "").replace("```", "").strip()
                if "{" in text: text = text[text.find("{"):text.rfind("}")+1]
                
                seo_data = json.loads(text)
                
                # Save SEO
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(seo_data, f, indent=4, ensure_ascii=False)
                    
                print("✅ SEO Data Saved.")
                return seo_data # ✅ Success! Yahi se wapis jao aur loop tod do

            except Exception as e:
                print(f"❌ SEO Error on {model_name}: {e}")
                report_failure(model_name) # Brain ko batao ye model fail ho gaya
                time.sleep(2) # 2 second ruko agla model try karne se pehle
                attempt += 1
                
        # Agar 15 attempts ke baad bhi SEO na bane
        print("🚨 Sare models fail ho gaye! SEO nahi ban paya.")
        return None

    except Exception as e:
        print(f"❌ Critical Error in SEO script: {e}")
        return None