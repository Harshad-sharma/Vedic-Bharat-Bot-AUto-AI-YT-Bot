# scripts/core/script_normalizer.py
import re

def normalize_script(script_data: dict, default_scene_count: int = 18) -> dict:
    """
    Guarantee: script_data['scenes'] हमेशा मौजूद रहे.
    अगर scenes नहीं हैं तो script/text से auto scenes बना देगा.
    """
    if not isinstance(script_data, dict):
        raise ValueError("script_data dict नहीं है")

    # अगर scenes already हैं तो OK
    scenes = script_data.get("scenes")
    if isinstance(scenes, list) and len(scenes) > 0:
        return script_data

    # script text ढूंढो (आपके generate_script.py जो भी दे रहा हो)
    text = (
        script_data.get("script")
        or script_data.get("text")
        or script_data.get("content")
        or ""
    ).strip()

    # अगर text भी नहीं मिला तो fallback
    if not text:
        text = "जय श्री राम। आज हम सनातन का एक रोचक तथ्य जानेंगे। अंत तक देखिए।"

    # lines में split
    lines = [ln.strip() for ln in re.split(r"[।.!?\n]", text) if ln.strip()]

    # अगर lines कम हैं तो words के chunks बना दो
    if len(lines) < 8:
        words = text.split()
        chunk = max(6, len(words) // default_scene_count)
        lines = [" ".join(words[i:i+chunk]) for i in range(0, len(words), chunk)]

    # scenes create
    new_scenes = []
    for i, ln in enumerate(lines[:default_scene_count]):
        new_scenes.append({
            "type": "VIDEO" if i % 3 == 0 else "IMAGE",
            "keyword": "vedic spiritual cinematic golden temple energy",
            "text": ln
        })

    script_data["scenes"] = new_scenes
    script_data.setdefault("duration_sec", 60)
    script_data.setdefault("cta", "ऐसी ही और वीडियोज़ के लिए Follow/Subscribe करें")
    return script_data
