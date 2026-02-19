import os

def create_structure():
    # यह हमारे प्रोजेक्ट का नक्शा (Map) है
    folders = [
        "assets/audio/background_music", # बैकग्राउंड म्यूजिक यहाँ रहेगा
        "assets/audio/sfx",              # साउंड इफेक्ट्स (घंटी, शंख)
        "assets/visuals/raw_images",     # डाउनलोड की गई इमेजेस
        "assets/visuals/video_clips",    # वीडियो क्लिप्स
        "assets/fonts",                  # हिंदी फोंट्स
        "assets/templates",              # चैनल का लोगो, इंट्रो, आउट्रो
        "config",                        # सेटिंग्स और क्रेडेंशियल्स
        "database",                      # बोट की याददाश्त (Memory/Logs)
        "scripts/core",                  # मुख्य दिमाग (Brain)
        "scripts/modules",               # छोटे हिस्से (Editing, Uploading)
        "output/shorts",                 # फाइनल वीडियो यहाँ बनेगी
        "output/reels",                  # इंस्टाग्राम वाली वीडियो
        "temp",                          # रफ काम के लिए (बाद में डिलीट होगा)
        "logs"                           # बोट ने क्या काम किया, उसका रिकॉर्ड
    ]

    files = {
        "config/settings.json": "{}",           # सेटिंग्स फाइल
        "config/prompts.txt": "",               # AI प्रॉम्प्ट्स
        "database/history.json": "[]",          # पिछली वीडियो की हिस्ट्री
        "database/feedback.json": "{}",         # यूजर फीडबैक (Self-Learning)
        ".env": "# API Keys yahan dalenge (Surakshit)", # सीक्रेट कीज़
        "requirements.txt": "",                 # पाइथन लाइब्रेरी लिस्ट
        "main.py": "# Bot ka start button"      # स्टार्ट बटन
    }

    print("🚀 Initializing Vedic Bharat Bot Structure...")

    # फोल्डर्स बनाना
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created Folder: {folder}")

    # फाइल्स बनाना
    for file_path, content in files.items():
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"📄 Created File: {file_path}")
        else:
            print(f"⏩ File already exists: {file_path}")

    print("\n✨ Project Structure Ready! Har Har Mahadev! ✨")

if __name__ == "__main__":
    create_structure()