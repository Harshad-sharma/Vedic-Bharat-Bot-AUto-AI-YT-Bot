# scripts/core/query_sanitizer.py
import re

BAD_WORDS = [
    "computer","laptop","office","lab","scientist","microscope","robot","server",
    "coding","software","technology","modern","city","corporate"
]

GOOD_PREFIX = ["india", "ancient", "vedic", "spiritual", "cinematic", "temple", "aarti", "ghats", "sacred", "golden"]


def sanitize_query(q: str) -> str:
    q2 = q.lower()
    for w in BAD_WORDS:
        q2 = re.sub(rf"\b{re.escape(w)}\b", "", q2)
    q2 = re.sub(r"\s+", " ", q2).strip()
    # add aesthetic boosters
    boost = " ".join(GOOD_PREFIX[:3])
    return f"{boost} {q2}".strip()
