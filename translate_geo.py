#!/usr/bin/env python3
"""
translate_geo.py  —  Phase 50
Enriches area.json, capitals_population.json, currencies.json, neighbors.json
with country-name translations for all 24 EU official languages + English.

Source: https://restcountries.com/v3.1/all  (free, no API key)

Usage:
    python3 translate_geo.py

Each entry gets new keys  name_en, name_fr, name_es, name_it, name_nl,
name_pt, name_pl, name_ro, name_hu, name_cs, name_sk, name_hr, name_sl,
name_bg, name_el, name_da, name_sv, name_fi, name_et, name_lv, name_lt,
name_mt, name_ga  (German stays in the existing 'countryLabel' field).
"""

import json
import urllib.request
import sys
import os

# ── Config ───────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
FILES       = [
    "area.json",
    "capitals_population.json",
    "currencies.json",
    "neighbors.json",
]
API_URL     = "https://restcountries.com/v3.1/all?fields=name,translations,cca2"

# restcountries translation-key → our suffix
# 'en' is special: taken from name.common
LANG_MAP = {
    "en":  None,          # handled separately via name.common
    "fr":  "fra",
    "es":  "spa",
    "it":  "ita",
    "nl":  "nld",
    "pt":  "por",
    "pl":  "pol",
    "ro":  "ron",
    "hu":  "hun",
    "cs":  "ces",
    "sk":  "slk",
    "hr":  "hrv",
    "sl":  "slv",
    "bg":  "bul",
    "el":  "ell",
    "da":  "dan",
    "sv":  "swe",
    "fi":  "fin",
    "et":  "est",
    "lv":  "lav",
    "lt":  "lit",
    "mt":  "mlt",
    "ga":  "gle",
    # German reference for matching (not written as new key)
    "_de": "deu",
}

# ── Fetch ────────────────────────────────────────────────────────────────────
def fetch_restcountries():
    print("Fetching restcountries.com …", end=" ", flush=True)
    req = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "translate_geo.py/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    print(f"{len(data)} countries loaded.")
    return data

# ── Build lookup table ────────────────────────────────────────────────────────
def build_lookup(countries):
    """
    Returns a dict:  german_name_lower -> {lang_code: translated_name, ...}
    Also indexes by English name (lower) and CCA2 code for broader matching.
    """
    by_de  = {}   # German common name → translations
    by_en  = {}   # English common name → translations
    by_cc  = {}   # CCA2 code → translations

    for c in countries:
        tr  = c.get("translations", {})
        nm  = c.get("name", {})
        cc  = c.get("cca2", "").upper()

        entry = {}
        # English
        entry["en"] = nm.get("common", "")
        # All other languages
        for lang, rc_key in LANG_MAP.items():
            if lang == "en" or lang == "_de":
                continue
            entry[lang] = tr.get(rc_key, {}).get("common", "") if rc_key else ""

        # German name for indexing
        de_name = tr.get("deu", {}).get("common", "").strip()
        en_name = entry["en"].strip()

        if de_name:
            by_de[de_name.lower()] = entry
        if en_name:
            by_en[en_name.lower()] = entry
        if cc:
            by_cc[cc] = entry

    return by_de, by_en, by_cc

# ── Match a German country label ──────────────────────────────────────────────
def lookup(label, by_de, by_en, by_cc):
    """Try DE lookup first, then EN, then give up gracefully."""
    key = label.strip().lower()
    if key in by_de:
        return by_de[key]
    # Partial / variant spellings  (e.g. "Tschechien" vs "Czechia")
    for de_key, entry in by_de.items():
        if key in de_key or de_key in key:
            return entry
    # English fallback (some entries in the JSONs might already be in English)
    if key in by_en:
        return by_en[key]
    return None

# ── Enrich one file ───────────────────────────────────────────────────────────
def enrich_file(path, by_de, by_en, by_cc):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"  ⚠ {os.path.basename(path)} is not a list — skipped.")
        return

    matched   = 0
    unmatched = []

    for entry in data:
        label = entry.get("countryLabel", "")
        if not label:
            continue

        tr = lookup(label, by_de, by_en, by_cc)
        if tr is None:
            unmatched.append(label)
            continue

        # Write translation keys (skip empty strings)
        for lang in ["en","fr","es","it","nl","pt","pl","ro","hu",
                     "cs","sk","hr","sl","bg","el","da","sv","fi",
                     "et","lv","lt","mt","ga"]:
            val = tr.get(lang, "")
            if val:
                entry[f"name_{lang}"] = val
        matched += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ {os.path.basename(path):35s} "
          f"{matched}/{len(data)} matched"
          + (f"  | {len(unmatched)} unmatched: {unmatched[:5]}" if unmatched else ""))

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    try:
        countries = fetch_restcountries()
    except Exception as e:
        print(f"ERROR fetching API: {e}", file=sys.stderr)
        sys.exit(1)

    by_de, by_en, by_cc = build_lookup(countries)
    print(f"Lookup table: {len(by_de)} DE / {len(by_en)} EN / {len(by_cc)} CC entries\n")

    for filename in FILES:
        path = os.path.join(BASE_DIR, filename)
        if not os.path.exists(path):
            print(f"  ⚠ {filename} not found — skipped.")
            continue
        enrich_file(path, by_de, by_en, by_cc)

    print("\nDone. Re-run gen.py to rebuild GeoQuest.html with the enriched data.")

if __name__ == "__main__":
    main()
