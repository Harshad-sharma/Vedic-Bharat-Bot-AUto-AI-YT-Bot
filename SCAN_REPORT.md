# SCAN REPORT
- Generated: 2026-02-14 17:39:04
- Root: `D:\Vedic_AI_Bot`
- Total files: 54
- Python files: 21
- Entrypoints: D:\Vedic_AI_Bot\main.py

## .env
- Exists: True
- Keys found: GEMINI_API_KEY, HF_TOKEN, PIXABAY_API_KEY, PEXELS_API_KEY, INSTA_USER, INSTA_PASS

## requirements.txt
- google-generativeai
- edge-tts
- moviepy
- requests
- python-dotenv
- pillow
- instagrapi
- google-auth-oauthlib
- google-api-python-client
- asyncio
- Pillow<10.0.0
- moviepy==1.0.3

## Top Imports (by frequency)
- `os` : 19
- `json` : 13
- `dotenv` : 10
- `google` : 8
- `random` : 6
- `re` : 4
- `time` : 4
- `scripts` : 2
- `PIL` : 2
- `numpy` : 2
- `requests` : 2
- `ast` : 1
- `datetime` : 1
- `pathlib` : 1
- `subprocess` : 1
- `sys` : 1
- `moviepy` : 1
- `asyncio` : 1
- `edge_tts` : 1
- `imageio_ffmpeg` : 1
- `whisper` : 1
- `playwright` : 1
- `dataclasses` : 1
- `google_auth_oauthlib` : 1
- `googleapiclient` : 1
- `pickle` : 1

## Suspected Dead/Unused Python Files (heuristic)
- D:\Vedic_AI_Bot\config.py
- D:\Vedic_AI_Bot\scan_project.py
- D:\Vedic_AI_Bot\setup_final.py
- D:\Vedic_AI_Bot\setup_project.py

## Smoke Test (run main.py)
- Ran: True
- Return code: 1

### STDOUT (last part)
```
==========================================

```

### STDERR (last part)
```
D:\Vedic_AI_Bot\scripts\core\brainstorm.py:4: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving 
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
Traceback (most recent call last):
  File "D:\Vedic_AI_Bot\main.py", line 69, in <module>
    run_automation()
  File "D:\Vedic_AI_Bot\main.py", line 14, in run_automation
    print("\U0001f680 VEDIC BHARAT AUTOMATION BOT - STARTING")
  File "C:\Users\harsh\AppData\Local\Programs\Python\Python311\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680' in position 0: character maps to <undefined>

```

## Python Files Map (first ~200)
- D:\Vedic_AI_Bot\config.py
- D:\Vedic_AI_Bot\main.py
- D:\Vedic_AI_Bot\scan_project.py
- D:\Vedic_AI_Bot\scripts\core\brainstorm.py
- D:\Vedic_AI_Bot\scripts\core\check_models.py
- D:\Vedic_AI_Bot\scripts\core\check_models_limits.py
- D:\Vedic_AI_Bot\scripts\core\edit_video.py
- D:\Vedic_AI_Bot\scripts\core\gather_visuals.py
- D:\Vedic_AI_Bot\scripts\core\generate_audio.py
- D:\Vedic_AI_Bot\scripts\core\generate_script.py
- D:\Vedic_AI_Bot\scripts\core\generate_seo.py
- D:\Vedic_AI_Bot\scripts\core\generate_thumbnail.py
- D:\Vedic_AI_Bot\scripts\core\insta_uploader.py
- D:\Vedic_AI_Bot\scripts\core\llm_client.py
- D:\Vedic_AI_Bot\scripts\core\offline_fallback.py
- D:\Vedic_AI_Bot\scripts\core\query_sanitizer.py
- D:\Vedic_AI_Bot\scripts\core\script_normalizer.py
- D:\Vedic_AI_Bot\scripts\core\test_brain.py
- D:\Vedic_AI_Bot\scripts\core\youtube_uploader.py
- D:\Vedic_AI_Bot\setup_final.py
- D:\Vedic_AI_Bot\setup_project.py
