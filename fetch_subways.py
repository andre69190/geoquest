#!/usr/bin/env python3
"""
fetch_subways.py  –  GeoQuest Phase 11
======================================
Queries Wikidata SPARQL for metro/subway systems, fetches network
length and number of lines, resolves country codes, and writes
subways.json (sorted by network km, top N entries).

Usage:
    python fetch_subways.py            # default: top 60, writes subways.json
    python fetch_subways.py --top 80   # custom limit
    python fetch_subways.py --out data/subways.json

Requirements:
    pip install requests
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip install requests")
    sys.exit(1)


# ── Wikidata SPARQL endpoint ─────────────────────────────────────────────────
SPARQL_URL = "https://query.wikidata.org/sparql"
HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "GeoQuestSubwayScraper/1.0 (educational; contact: geoquest@example.com)"
}

# ── ISO 3166-1 alpha-2 lookup (Wikidata country QID → cc) ────────────────────
# We ask Wikidata for the ISO code directly in the query, so this dict is a
# fallback for any QIDs that slip through without a code.
FALLBACK_CC: dict[str, str] = {
    "Q148":  "cn",   # China
    "Q30":   "us",   # United States
    "Q145":  "gb",   # United Kingdom
    "Q17":   "jp",   # Japan
    "Q183":  "de",   # Germany
    "Q142":  "fr",   # France
    "Q159":  "ru",   # Russia
    "Q668":  "in",   # India
    "Q155":  "br",   # Brazil
    "Q96":   "mx",   # Mexico
    "Q38":   "it",   # Italy
    "Q29":   "es",   # Spain
    "Q219":  "bg",   # Bulgaria  (Sofia)
    "Q16":   "ca",   # Canada
    "Q258":  "za",   # South Africa
    "Q408":  "au",   # Australia
    "Q41":   "gr",   # Greece
    "Q45":   "pt",   # Portugal
    "Q31":   "be",   # Belgium
    "Q55":   "nl",   # Netherlands
    "Q36":   "pl",   # Poland
    "Q28":   "hu",   # Hungary
    "Q213":  "cz",   # Czech Republic
    "Q218":  "ro",   # Romania
    "Q34":   "se",   # Sweden
    "Q35":   "dk",   # Denmark
    "Q20":   "no",   # Norway
    "Q33":   "fi",   # Finland
    "Q39":   "ch",   # Switzerland
    "Q40":   "at",   # Austria
    "Q189":  "is",   # Iceland
    "Q229":  "cy",   # Cyprus
    "Q211":  "lv",   # Latvia
    "Q212":  "ua",   # Ukraine
    "Q115":  "et",   # Ethiopia
    "Q114":  "ke",   # Kenya
    "Q79":   "eg",   # Egypt
    "Q1033": "ng",   # Nigeria
    "Q117":  "gh",   # Ghana
    "Q265":  "jo",   # Jordan
    "Q801":  "il",   # Israel
    "Q794":  "ir",   # Iran
    "Q881":  "vn",   # Vietnam
    "Q884":  "kr",   # South Korea
    "Q865":  "tw",   # Taiwan
    "Q334":  "sg",   # Singapore
    "Q836":  "mm",   # Myanmar
    "Q819":  "la",   # Laos
    "Q833":  "my",   # Malaysia
    "Q836":  "mm",   # Myanmar
    "Q252":  "id",   # Indonesia
    "Q928":  "ph",   # Philippines
    "Q298":  "cl",   # Chile
    "Q414":  "ar",   # Argentina
    "Q241":  "cu",   # Cuba
    "Q733":  "py",   # Paraguay
    "Q750":  "bo",   # Bolivia
    "Q717":  "ve",   # Venezuela
    "Q739":  "co",   # Colombia
    "Q736":  "ec",   # Ecuador
    "Q419":  "pe",   # Peru
    "Q750":  "bo",   # Bolivia
    "Q766":  "jm",   # Jamaica
    "Q733":  "py",   # Paraguay
    "Q786":  "do",   # Dominican Republic
    "Q574":  "tl",   # Timor-Leste
    "Q685":  "ws",   # Samoa
    "Q971":  "ci",   # Côte d'Ivoire
    "Q1006": "gn",   # Guinea
    "Q1007": "gw",   # Guinea-Bissau
    "Q1008": "ci",   # Ivory Coast
    "Q1009": "cm",   # Cameroon
    "Q1010": "bw",   # Botswana
    "Q1011": "cv",   # Cape Verde
    "Q1013": "lr",   # Liberia
    "Q347":  "li",   # Liechtenstein
    "Q347":  "li",   # Liechtenstein
    "Q924":  "tz",   # Tanzania
    "Q1020": "mz",   # Mozambique
    "Q1025": "mr",   # Mauritania
    "Q1027": "ml",   # Mali
    "Q1032": "ne",   # Niger
    "Q1036": "ug",   # Uganda
    "Q1037": "rw",   # Rwanda
    "Q1039": "st",   # São Tomé and Príncipe
    "Q1041": "sn",   # Senegal
    "Q1042": "sc",   # Seychelles
    "Q1044": "sl",   # Sierra Leone
    "Q1045": "so",   # Somalia
    "Q1049": "sd",   # Sudan
    "Q1050": "sz",   # Eswatini
    "Q1056": "tg",   # Togo
    "Q1057": "zm",   # Zambia
    "Q1060": "zw",   # Zimbabwe
    "Q702":  "fj",   # Fiji
    "Q664":  "nz",   # New Zealand
    "Q398":  "bh",   # Bahrain
    "Q399":  "am",   # Armenia
    "Q400":  "az",   # Azerbaijan
    "Q403":  "rs",   # Serbia
    "Q404":  "ba",   # Bosnia and Herzegovina
    "Q237":  "va",   # Vatican City
    "Q238":  "sm",   # San Marino
    "Q239":  "mc",   # Monaco
    "Q244":  "jm",   # Jamaica
    "Q784":  "dm",   # Dominica
}


SPARQL_QUERY = """\
SELECT DISTINCT
  ?system
  ?systemLabel
  ?cityLabel
  ?countryLabel
  ?countryCode
  (MAX(?lengthKm) AS ?km)
  (COUNT(DISTINCT ?line) AS ?lineCount)
WHERE {
  # metro / rapid-transit systems
  VALUES ?transitType {
    wd:Q5503  # rapid transit
    wd:Q928830 # metro system
  }
  ?system wdt:P31 ?transitType .

  # optional: total length in km
  OPTIONAL {
    ?system wdt:P2043 ?length .
    BIND(ROUND(?length) AS ?lengthKm)
  }

  # optional: count lines via hasPart or operatedBy lines
  OPTIONAL {
    ?line wdt:P361 ?system .
    ?line wdt:P31/wdt:P279* wd:Q15145593 .   # railway line
  }

  # city served
  OPTIONAL { ?system wdt:P856 ?website . }   # (just to keep the system active)
  OPTIONAL {
    ?system wdt:P131 ?city .
    ?city   wdt:P31/wdt:P279* wd:Q515 .       # city / municipality
  }

  # country
  OPTIONAL { ?system wdt:P17 ?country . }
  OPTIONAL {
    ?country wdt:P297 ?countryCode .
  }

  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "en,de" .
  }
}
GROUP BY ?system ?systemLabel ?cityLabel ?countryLabel ?countryCode
HAVING (MAX(?lengthKm) > 0)
ORDER BY DESC(?km)
LIMIT 150
"""


def run_sparql(query: str, retries: int = 3) -> list[dict]:
    """Execute a SPARQL query against Wikidata and return bindings."""
    for attempt in range(retries):
        try:
            resp = requests.get(
                SPARQL_URL,
                params={"query": query, "format": "json"},
                headers=HEADERS,
                timeout=60,
            )
            resp.raise_for_status()
            return resp.json()["results"]["bindings"]
        except requests.exceptions.Timeout:
            print(f"  Timeout (attempt {attempt+1}/{retries}), retrying…")
            time.sleep(5 * (attempt + 1))
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP error: {e}")
            if resp.status_code == 429:
                wait = 30
                print(f"  Rate-limited – waiting {wait}s…")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("SPARQL query failed after all retries")


def val(binding: dict, key: str) -> str:
    """Safely extract string value from a SPARQL binding."""
    return binding.get(key, {}).get("value", "")


def extract_qid(uri: str) -> str:
    """Extract Q-identifier from a Wikidata URI like http://www.wikidata.org/entity/Q123."""
    m = re.search(r"(Q\d+)$", uri)
    return m.group(1) if m else ""


def clean_name(label: str) -> str:
    """
    Strip suffixes like 'Metro', 'Subway', 'Underground', 'Rapid Transit'
    from system labels to get a clean city name.
    """
    suffixes = [
        r"\s+(Metro|Metropolitan|Subway|Underground|Tube|Rapid\s+Transit"
        r"|U-Bahn|S-Bahn|MRT|LRT|Rail|Transit|System|Network|Railway|Line).*$"
    ]
    result = label
    for pat in suffixes:
        result = re.sub(pat, "", result, flags=re.IGNORECASE).strip()
    return result


def build_entries(bindings: list[dict], top_n: int) -> list[dict]:
    """Convert SPARQL bindings → clean subway entries."""
    seen_systems: set[str] = set()
    entries: list[dict] = []

    for row in bindings:
        qid = extract_qid(val(row, "system"))
        if qid in seen_systems:
            continue
        seen_systems.add(qid)

        system_label = val(row, "systemLabel")
        city_label   = val(row, "cityLabel") or clean_name(system_label)
        country_label = val(row, "countryLabel")

        # ISO code from Wikidata (P297), else fallback
        cc_raw = val(row, "countryCode").lower()
        if not cc_raw:
            country_qid = extract_qid(val(row, "country") if "country" in row else "")
            cc_raw = FALLBACK_CC.get(country_qid, "")

        if not cc_raw or len(cc_raw) != 2:
            continue   # skip entries without a valid country code

        try:
            km = int(float(val(row, "km")))
        except (ValueError, TypeError):
            continue

        try:
            lines = int(val(row, "lineCount")) or 1
        except (ValueError, TypeError):
            lines = 1

        if km < 5:
            continue   # filter out tram/light-rail stubs

        entries.append({
            "city":    city_label,
            "country": country_label,
            "cc":      cc_raw,
            "km":      km,
            "lines":   lines,
        })

        if len(entries) >= top_n:
            break

    # sort descending by km
    entries.sort(key=lambda x: x["km"], reverse=True)
    return entries[:top_n]


def main():
    parser = argparse.ArgumentParser(description="Fetch subway data from Wikidata")
    parser.add_argument("--top", type=int, default=60,
                        help="Number of systems to include (default: 60)")
    parser.add_argument("--out", type=str, default="subways.json",
                        help="Output JSON file path (default: subways.json)")
    args = parser.parse_args()

    print(f"Querying Wikidata SPARQL for top {args.top} metro systems…")
    try:
        bindings = run_sparql(SPARQL_QUERY)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    print(f"  → {len(bindings)} raw results received")

    entries = build_entries(bindings, args.top)
    print(f"  → {len(entries)} clean entries after filtering")

    if not entries:
        print("WARNING: No valid entries found. Check SPARQL query or Wikidata availability.")
        sys.exit(1)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nWrote {len(entries)} entries to: {out_path}")
    print("\nTop 10 preview:")
    for i, e in enumerate(entries[:10], 1):
        print(f"  {i:2}. {e['city']:<20} {e['country']:<20} {e['km']:>5} km  {e['lines']:>3} lines  [{e['cc']}]")

    print("\nTo use in GeoQuest gen.py, copy the file to the project folder and")
    print("update SUBWAYS = json.load(open('subways.json')) in gen.py.")


if __name__ == "__main__":
    main()
