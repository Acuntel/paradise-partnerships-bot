"""Partnerships bot test previews. Master prompt: senior bizdev voice,
verbatim opener locked, hyper-personalized hook, body cap 155 words,
NO discount, NO P.S."""
import sys
from pathlib import Path

SHARED_ROOT = Path(__file__).resolve().parents[2] / "_shared"
sys.path.insert(0, str(SHARED_ROOT))

from core import make_samples  # noqa: E402

import run as bot_run  # noqa: E402


SIGNOFF = (
    "- The Partnership Team\n"
    "Paradise Home Design Inc\n"
    "225 E Deerpath Rd, Lake Forest IL\n"
    "partnerships@paradisehomedesigninc.com\n"
    "(847) 681-9000\n"
    "Portfolio: paradisehomedesigninc.com/gallery.html"
)


SAMPLES = [
    {
        "subject": "On 400 Lake Shore, quick supply question",
        "body_text": (
            "Hi Curt, we're going to do a quicker and a better job than "
            "anyone you've ever worked with before. Saw the Crain's "
            "Newsmaker of the Year piece, congrats.\n\n"
            "Paradise has been doing high-end kitchen, bath, and "
            "cabinetry packages out of Lake Forest for 38 years. We "
            "carry Adelphi, Candlelight, Medallion, and Fabuwood, and "
            "the Deerpath showroom is set up for unit-level spec.\n\n"
            "On 400 Lake Shore, you're looking at 1,135 unit kitchens "
            "and baths across two towers, broken ground in February. "
            "That's our sweet spot.\n\n"
            "We design, supply, and install. One PO. One accountable "
            "team. No cabinet-installer finger-pointing.\n\n"
            "20 minutes at your office or the site, your pick. What "
            "does next Tuesday or Wednesday look like?\n\n"
            f"{SIGNOFF}"
        ),
        "hero_key": "kitchen_marble_brass",
        "thumb_keys": ["kitchen_marble_arch", "kitchen_black_island", "kitchen_white_modern"],
        "fname": "01_curt_related_midwest.html",
    },
    {
        "subject": "Saw the Real Deal cover, also Foundry kitchens",
        "body_text": (
            "Hi Jim, we're going to do a quicker and a better job than "
            "anyone you've ever worked with before. Caught the Real "
            "Deal cover last fall, great read.\n\n"
            "Paradise has been doing kitchen and bath supply packages "
            "out of Lake Forest for 38 years. We carry Adelphi, "
            "Candlelight, Medallion, and Fabuwood, and the Deerpath "
            "showroom is built for spec at scale.\n\n"
            "On Foundry Park, you're looking at up to 3,737 units across "
            "the next decade since the February full city approval. "
            "That's the volume our shop was built for.\n\n"
            "We'll match your current supplier's number and beat their "
            "lead time, in writing.\n\n"
            "20 minutes at your Chicago office or the Deerpath showroom, "
            "your pick. What does next Tuesday or Wednesday look like?\n\n"
            f"{SIGNOFF}"
        ),
        "hero_key": "kitchen_marble_arch",
        "thumb_keys": ["kitchen_marble_brass", "kitchen_black_island", "kitchen_white_modern"],
        "fname": "02_jim_jdl_development.html",
    },
    {
        "subject": "Faster + cheaper kitchen package for Optima",
        "body_text": (
            "Hi David, we're going to do a quicker and a better job than "
            "anyone you've ever worked with before. The father-son "
            "Hovey design legacy out of Glencoe since 1978 is the kind "
            "of bench we respect.\n\n"
            "Paradise has been doing high-end kitchen, bath, and "
            "cabinetry packages out of Lake Forest for 38 years. The "
            "Deerpath showroom carries Adelphi, Candlelight, Medallion, "
            "and Fabuwood.\n\n"
            "On Optima Lumina, you're looking at 128 luxury condos in "
            "Wilmette since the mid-2025 groundbreaking. Adjacent to "
            "the completed Verdana, that's our sweet spot.\n\n"
            "Our showroom is 32 minutes from your Glencoe office. "
            "We'll drive.\n\n"
            "20 minutes at your office or the site, your pick. What "
            "does next Tuesday or Wednesday look like?\n\n"
            f"{SIGNOFF}"
        ),
        "hero_key": "kitchen_marble_brass",
        "thumb_keys": ["kitchen_marble_arch", "kitchen_black_island", "kitchen_white_modern"],
        "fname": "03_david_optima.html",
    },
    {
        "subject": "On Solo Cup, quick supply question",
        "body_text": (
            "Hi Tony, we're going to do a quicker and a better job than "
            "anyone you've ever worked with before. The unanimous "
            "Highland Park council vote on Solo Cup is rare in that "
            "village. Well done.\n\n"
            "Paradise has been doing high-end kitchen, bath, and "
            "cabinetry packages out of Lake Forest for 38 years. We "
            "carry Adelphi, Candlelight, Medallion, and Fabuwood, and "
            "we're 12 minutes north up Sheridan from the Solo Cup site.\n\n"
            "On the Solo Cup townhomes, you're looking at 227 unit-level "
            "kitchens and baths on 9 acres since the February approval. "
            "That's our sweet spot.\n\n"
            "We design, supply, and install. One PO. One accountable "
            "team. No cabinet-installer finger-pointing.\n\n"
            "20 minutes at your office or the site, your pick. What "
            "does next Tuesday or Wednesday look like?\n\n"
            f"{SIGNOFF}"
        ),
        "hero_key": "kitchen_white_modern",
        "thumb_keys": ["kitchen_white_pendants", "kitchen_marble_brass", "bath_double_vanity"],
        "fname": "04_tony_habitat_company.html",
    },
    {
        "subject": "Faster + cheaper kitchen package for Sterling Bay",
        "body_text": (
            "Hi Andy, we're going to do a quicker and a better job than "
            "anyone you've ever worked with before. Saw the 47-story "
            "tower with Magellan hit pre-leasing this quarter, "
            "congrats.\n\n"
            "Paradise has been doing high-end kitchen, bath, and "
            "cabinetry packages out of Lake Forest for 38 years. We "
            "carry Adelphi, Candlelight, Medallion, and Fabuwood, and "
            "we've spec'd luxury towers for North Shore developers "
            "since 1988.\n\n"
            "On the Magellan tower and the remaining Lincoln Yards "
            "south parcels, the unit-level kitchen and bath spec is "
            "exactly the volume our shop was built for.\n\n"
            "We'll match your current supplier's number and beat their "
            "lead time, in writing.\n\n"
            "20 minutes at your office or the site, your pick. What "
            "does next Tuesday or Wednesday look like?\n\n"
            f"{SIGNOFF}"
        ),
        "hero_key": "kitchen_black_island",
        "thumb_keys": ["kitchen_marble_brass", "kitchen_marble_arch", "kitchen_white_modern"],
        "fname": "05_andy_sterling_bay.html",
    },
]


if __name__ == "__main__":
    paths = make_samples.generate(bot_run.CFG, SAMPLES)
    for p in paths:
        print("wrote", p)
