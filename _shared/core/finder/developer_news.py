"""
Real-estate developer news scraper (Partnerships bot).

Surfaces developer-pipeline announcements with project details (unit
count, location, timing, principal name) so the Partnerships bot can
populate `pipeline_note` and `personal_hook` automatically instead of
requiring hand-curation.

Sources (free, public news):
  - Crain's Chicago Business (chicagobusiness.com)
  - The Real Deal Chicago (therealdeal.com/chicago)
  - REJournals (rejournals.com)
  - Chicago Tribune real-estate
  - Block Club Chicago for ground-up announcements

Output: list of dicts with keys
  {
    "company_name": str,
    "company_website": str (best-guess),
    "principal_first": str,        # if quoted in coverage
    "principal_last": str,
    "town": str,                   # project town if mentioned
    "pipeline_note": str,          # 1-2 sentence project summary
    "source_url": str,
  }

The Partnerships bot's runner.cmd_load + research.research will further
enrich each row before drafting.
"""
import logging
import re
import time
from typing import Dict, Iterable, List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .multi_search import search as multi_search

log = logging.getLogger(__name__)

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15"
)
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
TIMEOUT = 12

DEV_NEWS_HOSTS = (
    "chicagobusiness.com",     # Crain's
    "therealdeal.com",         # TRD
    "rejournals.com",           # REJournals
    "bisnow.com",
    "chicagoyimby.com",
    "blockclubchicago.org",
    "urbanize.city",
    "chicagotribune.com",
)

# Project-detail regex: "230 units", "1,100 units", "12-story", etc.
UNIT_COUNT_RE = re.compile(
    r"\b(\d{1,3}(?:,\d{3})?)\s*(?:unit|townhome|condo|apartment|residence)s?\b",
    re.I,
)
DOLLAR_PROJECT_RE = re.compile(
    r"\$(\d{1,3}(?:\.\d+)?)\s*(million|billion|M|B)\b",
    re.I,
)
QUOTE_NAME_RE = re.compile(
    r'"\s*[^"]{30,400}\s*",?\s+(?:said|says|told|notes|adds)\s+'
    r'([A-Z][a-z]{1,15})\s+([A-Z][a-zA-Z\-\']{2,20})'
)
PRINCIPAL_RE = re.compile(
    r"\b([A-Z][a-z]{1,15})\s+([A-Z][a-zA-Z\-']{2,20}),\s+"
    r"(?:CEO|founder|co-founder|principal|managing partner|partner|president)",
    re.I,
)
COMPANY_RE = re.compile(
    r"\b([A-Z][A-Za-z&\.\s]{2,40}?)\s+"
    r"(?:LLC|LP|Group|Properties|Development|Partners|Capital|Realty|"
    r"Companies|Holdings|Ventures|Investments)\b"
)


def _fetch(url, timeout=TIMEOUT):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout,
                         allow_redirects=True)
        if r.status_code == 200 and r.text:
            return r.text
    except Exception as e:
        log.debug("fetch %s failed: %s", url, e)
    return None


def _year_tokens(months: int):
    """Yield year-string tokens covering the requested historical window.

    months=12 -> ['2026', '2025']
    months=24 -> ['2026', '2025', '2024']
    months=36 -> ['2026', '2025', '2024', '2023']
    """
    import datetime as _dt
    today = _dt.date.today()
    years = max(1, (months + 11) // 12)
    return [str(today.year - i) for i in range(years + 1)]


def _article_urls(towns, max_results=10, months: int = 12):
    """Discover developer-news articles mentioning Chicago multifamily +
    target towns. Wider query coverage = more announcements.
    """
    base = [
        # Project-type variants
        '"Chicago" "multifamily" "units" announced',
        '"Chicago" "multifamily" "units" approved',
        '"Chicago" "multifamily" project breaks ground',
        '"Chicago" "townhome" development plan approved',
        '"Chicago" "townhome" "units" announced',
        '"Chicago" condominium project unit count',
        '"Chicago" "condo" tower announced',
        '"Chicago" "mixed-use" tower units',
        '"Chicago" "build-to-rent" community',
        '"Chicago" "senior living" "units" announced',
        '"Chicago" "hospitality" "rooms" hotel announced',
        '"Chicago" "boutique hotel" rooms',
        '"Chicago" "podium" apartment units',
        '"Chicago" "high-rise" residential units',
        '"Chicago" "low-rise" residential units',
        # Stage-of-pipeline variants
        '"Chicago" multifamily groundbreaking',
        '"Chicago" multifamily topping out',
        '"Chicago" multifamily lease-up',
        '"Chicago" affordable housing units approved',
        '"Chicago" mixed-income development units',
        # Suburban-belt variants
        '"North Shore" Illinois multifamily development units',
        '"Lake County" Illinois multifamily project units',
        '"DuPage County" multifamily development units',
        '"Cook County" multifamily project announced',
        '"McHenry County" multifamily project',
        # Site-restricted dives across each publication
        'site:chicagobusiness.com Chicago multifamily',
        'site:chicagobusiness.com townhome development',
        'site:chicagobusiness.com developer announces',
        'site:therealdeal.com chicago development',
        'site:therealdeal.com chicago multifamily',
        'site:therealdeal.com chicago condo tower',
        'site:rejournals.com Chicago multifamily',
        'site:rejournals.com Chicago townhome',
        'site:rejournals.com Chicago groundbreaking',
        'site:bisnow.com chicago multifamily',
        'site:bisnow.com chicago developer',
        'site:chicagoyimby.com multifamily',
        'site:chicagoyimby.com proposed',
        'site:blockclubchicago.org development announced',
        'site:urbanize.city chicago units approved',
        # Principal-role queries (drag the principal name out of coverage)
        '"Chicago" multifamily CEO announces',
        '"Chicago" developer founder announces',
        '"Chicago" "managing partner" multifamily',
        '"Chicago" "principal" residential development',
    ]

    # Vintage queries broaden historical reach via year-tagged searches.
    # Most search engines surface time-relevant hits even without
    # explicit date operators, so a year token in the query is enough.
    for year in _year_tokens(months):
        base.append(f'"Chicago" multifamily {year}')
        base.append(f'"Chicago" "townhome" {year}')
        base.append(f'site:chicagobusiness.com Chicago multifamily {year}')
        base.append(f'site:therealdeal.com chicago development {year}')
        base.append(f'site:rejournals.com Chicago {year} multifamily')

    queries = list(base)
    # Cover ALL towns (was first 8) -- doubles or triples surburban hits.
    for town in towns:
        queries.append(f'"{town}" Illinois multifamily development')
        queries.append(f'"{town}" Illinois townhome project')

    log.info("developer-news: built %d search queries (months=%d, towns=%d)",
             len(queries), months, len(towns))
    seen = set()
    urls = []
    for q in queries:
        for hit in multi_search(q, max_results=max_results):
            url = hit.get("url", "")
            host = urlparse(url).netloc.lower()
            if not any(h in host for h in DEV_NEWS_HOSTS):
                continue
            if url in seen:
                continue
            seen.add(url)
            urls.append(url)
        time.sleep(0.3)
    return urls


def _extract_project_details(text, towns):
    """Pull project unit-count + location from an article body."""
    units = None
    location = None
    for m in UNIT_COUNT_RE.finditer(text):
        try:
            units = int(m.group(1).replace(",", ""))
            break
        except ValueError:
            continue
    for town in towns:
        if town.lower() in text.lower():
            location = town
            break
    return units, location


def _extract_principal(text):
    """Pull principal name (CEO/founder/principal) and quoted speakers."""
    for m in PRINCIPAL_RE.finditer(text):
        return m.group(1), m.group(2)
    for m in QUOTE_NAME_RE.finditer(text):
        return m.group(1), m.group(2)
    return None, None


def _extract_company(text):
    for m in COMPANY_RE.finditer(text):
        name = m.group(1).strip().rstrip(",.;:")
        if name in ("The", "A", "An"):
            continue
        if len(name) >= 4:
            return name
    return None


_NEWS_FALSE_POSITIVE_NAMES = (
    "subscribe", "related articles", "commercial real estate",
    "news section", "speaker information", "speaker topics",
    "about team", "illinois finance", "newsletter",
    "real deal", "the real deal", "crain", "bisnow", "rejournals",
    "block club", "urbanize", "tribune", "sun-times", "yimby",
    "chicago business", "real estate weekly", "press release",
)


def _is_news_artifact(name: str) -> bool:
    """Reject extracted 'companies' that are obviously news-page artifacts
    (sidebar headers, subscription CTAs, byline blocks, masthead names)."""
    if not name:
        return True
    n = name.lower().strip()
    return any(token in n for token in _NEWS_FALSE_POSITIVE_NAMES)


def recent_developer_announcements(towns: Iterable[str],
                                     max_total: int = 60,
                                     months: int = 12,
                                     ) -> List[Dict[str, str]]:
    towns = list(towns)
    log.info("developer-news: scanning over %d Chicago-area towns",
             len(towns))
    seen_articles = set()
    seen_companies = set()
    out = []

    for url in _article_urls(towns, months=months):
        if len(out) >= max_total:
            break
        if url in seen_articles:
            continue
        seen_articles.add(url)
        html = _fetch(url)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)[:8000]
        units, location = _extract_project_details(text, towns)
        principal_first, principal_last = _extract_principal(text)
        company = _extract_company(text)

        if not company or not (units or location):
            continue
        if _is_news_artifact(company):
            log.debug("skip news-artifact company: %s", company)
            continue
        ckey = company.lower().strip()
        if ckey in seen_companies:
            continue
        seen_companies.add(ckey)

        pieces = []
        if units:
            pieces.append(f"{units} units")
        if location:
            pieces.append(f"in {location}")
        for m in DOLLAR_PROJECT_RE.finditer(text):
            pieces.append(f"${m.group(1)}{m.group(2)} project")
            break
        pipeline_note = ", ".join(pieces) + "." if pieces else ""

        out.append({
            "company_name": company,
            "company_website": "",
            "principal_first": principal_first or "",
            "principal_last": principal_last or "",
            "town": location or "",
            "pipeline_note": pipeline_note,
            "source_url": url,
        })
        log.info("  %s -- %s", company, pipeline_note)
        time.sleep(0.5)

    log.info("developer-news: %d unique developer announcements",
             len(out))
    return out
