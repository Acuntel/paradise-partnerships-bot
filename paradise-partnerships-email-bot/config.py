"""Partnerships email-bot config. Uses Opus 4.7 for hyper-personalization
on a smaller, hand-curated developer pool."""
import os
import random
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent
SHARED_ROOT = PROJECT_DIR.parents[1] / "_shared"
sys.path.insert(0, str(SHARED_ROOT))


def _load_api_key():
    if os.getenv("ANTHROPIC_API_KEY"):
        return os.getenv("ANTHROPIC_API_KEY")
    for p in [
        PROJECT_DIR / ".env",
        SHARED_ROOT / ".env",
        Path.home() / "Desktop" / "Client Website email bot" / ".env",
        Path.home() / "Desktop" / "Hermann Email Bot" / ".env",
    ]:
        if p.exists():
            load_dotenv(p, override=False)
            if os.getenv("ANTHROPIC_API_KEY"):
                return os.getenv("ANTHROPIC_API_KEY")
    return ""


def _load_app_password():
    if os.getenv("PARTNERSHIPS_GMAIL_APP_PASSWORD"):
        return os.getenv("PARTNERSHIPS_GMAIL_APP_PASSWORD")
    return os.getenv("GMAIL_APP_PASSWORD", "")


API_KEY = _load_api_key()
GMAIL_ADDRESS = "partnerships@paradisehomedesigninc.com"
GMAIL_APP_PASSWORD = _load_app_password()


def build_payload_extras(prospect_row):
    from core import gallery
    # Partnerships: always premium imagery (developer-grade hero shots)
    hero_key, thumb_keys = gallery.pick_for(
        prospect_row.get("town") or "Chicago", focus="kitchen",
    )
    # Force ultra-tier imagery if available
    preferred = ["kitchen_marble_brass", "kitchen_marble_arch",
                 "kitchen_black_island", "kitchen_white_modern"]
    available = [k for k in preferred if k in gallery.valid_keys()]
    if available:
        hero_key = available[0]
        thumb_keys = [k for k in available[1:4]
                      if k != hero_key][:3] or thumb_keys

    return {
        "include_ps": False,
        "subject_bucket": random.choice([
            "project_specific", "personal", "direct",
        ]),
        "available_gallery_keys": [hero_key] + thumb_keys,
        "suggested_hero": hero_key,
        "suggested_thumbs": thumb_keys,
    }
