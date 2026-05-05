"""Partnerships email-bot CLI. Opus 4.7 for hyper-personalization."""
import sys
from pathlib import Path

SHARED_ROOT = Path(__file__).resolve().parents[2] / "_shared"
sys.path.insert(0, str(SHARED_ROOT))

import config as bot_config  # noqa: E402
from core import runner  # noqa: E402
from core.runner import BotConfig  # noqa: E402

_orig = runner._payload_from_prospect


def _payload(p, bot_name):
    base = _orig(p, bot_name)
    base.update(bot_config.build_payload_extras(p))
    return base


runner._payload_from_prospect = _payload


CFG = BotConfig(
    bot_name="partnerships",
    project_dir=Path(__file__).resolve().parent,
    sender_name="Paradise Home Design - Partnerships",
    sender_address=bot_config.GMAIL_ADDRESS,
    sender_phone="(847) 681-9000",
    accent_color="#1F1F22",                      # near-black, premium
    cta_label="View portfolio",
    brand_label="Paradise Home Design",
    brand_sub="Multifamily Kitchen + Bath Supply Partner",
    footer_line=("Paradise Home Design Inc. 225 E Deerpath Rd, "
                 "Lake Forest IL. 38 years. Reply STOP to opt out."),
    model="claude-opus-4-7",
    max_words=155,
    api_key=bot_config.API_KEY,
    gmail_app_password=bot_config.GMAIL_APP_PASSWORD,
    enrichment_kind="developer",
    # Partnerships targets multifamily / townhome / condo developers,
    # not homeowners. developer_news is the primary discovery vector;
    # architects cross-references which firms work with which
    # developers (so we know who else is on the GC team).
    default_discover_sources="developer_news,architects",
)

if __name__ == "__main__":
    runner.run(CFG)
