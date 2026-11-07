# Vedic Bharat Bot - Auto AI YouTube Shorts Generator

An automated AI-powered system that generates and uploads Vedic/Spiritual YouTube Shorts in Hindi.

## Features

- **AI Topic Generation** – Unique Vedic & spiritual topics daily
- **Script Generation** – Viral-style Hindi scripts using Gemini
- **Voice Generation** – Automatic audio creation
- **Visuals Gathering** – Smart stock footage selection (Pixabay + Pexels)
- **Thumbnail Generation** – Auto-created attractive thumbnails
- **Smart Scheduling** – Uploads videos at optimal times (IST)
- **YouTube Upload** – Fully automated with SEO (title, description, tags)
- **Fallback System** – Multiple Gemini models with rotation for reliability

## Tech Stack

- Python 3.10+
- Google Gemini API
- YouTube Data API v3
- Pixabay & Pexels API
- MoviePy / FFmpeg for video editing

## Project Structure
├── config.py

├── main.py                 # Single video mode

├── daily_batch.py          # Batch mode

├── scripts/

│   └── core/

│       ├── ai_engine.py

│       ├── ai_rotator.py

│       ├── brainstorm.py

│       ├── generate_script.py

│       ├── generate_audio.py

│       ├── gather_visuals.py

│       ├── generate_thumbnail.py

│       ├── edit_video.py

│       ├── generate_seo.py

│       └── youtube_uploader.py

├── requirements.txt




## Setup

1. Clone the repository
```bash
git clone https://github.com/Harshad-sharma/Vedic-Bharat-Bot-AUto-AI-YT-Bot.git
cd Vedic-Bharat-Bot-AUto-AI-YT-Bot

└── .env.example






Install dependencies
Bashpip install -r requirements.txt
Create .env file from example
Bashcp .env.example .env
Add your API keys in .env:

GEMINI_API_KEY
PIXABAY_API_KEY
PEXELS_API_KEY

Place your client_secrets.json (YouTube OAuth) in the root folder.
Run the bot
Bashpython main.pyImportant Notes
Never commit your .env or client_secrets.json files.
This project is for educational and personal automation purposes.
Respect YouTube and stock media terms of service.
Some media sources may have copyright restrictions — always verify before uploading.
LicenseMIT License
