# Paradise Partnerships Email Bot

## What this is

Hyper-personalized cold-outreach to ~100 hand-curated Chicagoland
developers, signed by **The Partnership Team**
(partnerships@paradisehomedesigninc.com). Uses **Opus 4.7** for the
generation.

The pitch is a faster + cheaper + better kitchen + bath supply package
than whoever the developer currently uses, plus design and install in a
single contract. The bait is the verbatim opener and the proof of
research, not money.

## Pitch contract

See `MASTER_PROMPT.md`. Body cap 155 words. **First sentence is locked
verbatim**: "We're going to do a quicker and a better job than anyone
you've ever worked with before."

## Sender

- Name: Paradise Home Design - Partnerships
- Email: partnerships@paradisehomedesigninc.com
- Sign-off: "- The Partnership Team / Paradise Home Design Inc / 225 E Deerpath Rd, Lake Forest IL"
- NO P.S. (senior audience; spouse line is for homeowner bots only).

## Volume

Target ~5-10 sends/day. These are artisanal. Seed the local DB with the
28 developers from `~/Desktop/Paradise Home Bots/Paradise Home Call Bots/paradise-homes-call-bot/prospects.md`
once you confirm contact emails via DDG-scrape (no Hunter, no Apollo).

## Commands

```bash
python run.py load data/sample_leads.csv
python run.py verify
python run.py preview 5
python run.py draft 5
```

## Schema

Each developer row has these required fields:

- first_name, last_name, email, company_name, company_website, town
- pipeline_note: 1-2 sentences of true, public pipeline detail
- personal_hook: 1 sentence of true, public personal detail (article,
  award, alumni status, social-media post about a hobby)

The bot's master prompt uses `pipeline_note` and `personal_hook`
verbatim. Source these by hand from public press releases, LinkedIn,
Crain's, Real Deal. **Never invent.**
