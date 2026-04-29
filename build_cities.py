"""
GeoQuest – cities.json Generator
=================================
Lädt GeoNames-Daten (kostenlos, kein API-Key nötig) und erzeugt
eine saubere cities.json mit ~5.000 Städten.

Verwendung:
  pip install requests
  python build_cities.py

Output: cities.json (neben diesem Skript)
"""

import json, csv, io, zipfile, urllib.request, os, sys
from collections import defaultdict

# ── Konfiguration ────────────────────────────────────────────────────────────
MIN_POPULATION   = 50_000        # Alle Städte über 50k Einwohner (~5.000 Städte)
MAX_RANK_COUNTRY = 50            # Maximal die Top-50 je Land
OUTPUT_FILE      = "cities.json"

# GeoNames download (cities5000 = alle Städte mit mind. 5.000 Einwohnern)
GEONAMES_URL = "https://download.geonames.org/export/dump/cities5000.zip"

# Länder-Metadaten für Kontinent + Subregion
COUNTRY_INFO_URL = "https://download.geonames.org/export/dump/countryInfo.txt"

# ── Kontinent-Mapping (ISO2 → Kontinent) ────────────────────────────────────
CONTINENT_MAP = {
    "AF":"Africa","AN":"Antarctica",
    "AS":"Asia","EU":"Europe",
    "NA":"North America","OC":"Oceania","SA":"South America",
}

# Subregion-Mapping (ISO2 → Subregion) — für noch präzisere Distraktoren
SUBREGION_MAP = {
    # Ostasien
    "CN":"Eastern Asia","JP":"Eastern Asia","KR":"Eastern Asia",
    "TW":"Eastern Asia","MN":"Eastern Asia","KP":"Eastern Asia",
    # Südostasien
    "VN":"Southeast Asia","TH":"Southeast Asia","ID":"Southeast Asia",
    "PH":"Southeast Asia","MY":"Southeast Asia","SG":"Southeast Asia",
    "MM":"Southeast Asia","KH":"Southeast Asia","LA":"Southeast Asia",
    "TL":"Southeast Asia","BN":"Southeast Asia",
    # Südasien
    "IN":"Southern Asia","PK":"Southern Asia","BD":"Southern Asia",
    "LK":"Southern Asia","NP":"Southern Asia","AF":"Southern Asia",
    "IR":"Southern Asia",
    # Westasien / Naher Osten
    "TR":"Western Asia","SA":"Western Asia","IQ":"Western Asia",
    "SY":"Western Asia","JO":"Western Asia","LB":"Western Asia",
    "IL":"Western Asia","AE":"Western Asia","KW":"Western Asia",
    "YE":"Western Asia","OM":"Western Asia","QA":"Western Asia",
    "BH":"Western Asia","AZ":"Western Asia","GE":"Western Asia","AM":"Western Asia",
    # Zentralasien
    "KZ":"Central Asia","UZ":"Central Asia","TM":"Central Asia",
    "KG":"Central Asia","TJ":"Central Asia",
    # Nordafrika
    "EG":"Northern Africa","MA":"Northern Africa","DZ":"Northern Africa",
    "TN":"Northern Africa","LY":"Northern Africa","SD":"Northern Africa",
    # Westafrika
    "NG":"Western Africa","GH":"Western Africa","CI":"Western Africa",
    "SN":"Western Africa","ML":"Western Africa","BF":"Western Africa",
    "NE":"Western Africa","GN":"Western Africa","SL":"Western Africa",
    "LR":"Western Africa","TG":"Western Africa","BJ":"Western Africa",
    "GM":"Western Africa","GW":"Western Africa","CV":"Western Africa","MR":"Western Africa",
    # Ostafrika
    "ET":"Eastern Africa","TZ":"Eastern Africa","KE":"Eastern Africa",
    "UG":"Eastern Africa","MZ":"Eastern Africa","MG":"Eastern Africa",
    "ZM":"Eastern Africa","ZW":"Eastern Africa","RW":"Eastern Africa",
    "SO":"Eastern Africa","BI":"Eastern Africa","DJ":"Eastern Africa",
    # Zentralafrika
    "CD":"Middle Africa","CM":"Middle Africa","AO":"Middle Africa",
    "CF":"Middle Africa","CG":"Middle Africa","TD":"Middle Africa",
    "GA":"Middle Africa","GQ":"Middle Africa",
    # Südafrika
    "ZA":"Southern Africa","NA":"Southern Africa","BW":"Southern Africa",
    "LS":"Southern Africa","SZ":"Southern Africa",
    # Westeuropa
    "DE":"Western Europe","FR":"Western Europe","NL":"Western Europe",
    "BE":"Western Europe","AT":"Western Europe","CH":"Western Europe",
    "LU":"Western Europe","LI":"Western Europe","MC":"Western Europe",
    # Nordeuropa
    "GB":"Northern Europe","SE":"Northern Europe","NO":"Northern Europe",
    "DK":"Northern Europe","FI":"Northern Europe","IE":"Northern Europe",
    "IS":"Northern Europe","EE":"Northern Europe","LV":"Northern Europe","LT":"Northern Europe",
    # Südeuropa
    "IT":"Southern Europe","ES":"Southern Europe","PT":"Southern Europe",
    "GR":"Southern Europe","HR":"Southern Europe","RS":"Southern Europe",
    "BA":"Southern Europe","AL":"Southern Europe","MK":"Southern Europe",
    "ME":"Southern Europe","SI":"Southern Europe","CY":"Southern Europe","MT":"Southern Europe",
    # Osteuropa
    "RU":"Eastern Europe","UA":"Eastern Europe","PL":"Eastern Europe",
    "RO":"Eastern Europe","CZ":"Eastern Europe","HU":"Eastern Europe",
    "SK":"Eastern Europe","BG":"Eastern Europe","BY":"Eastern Europe",
    "MD":"Eastern Europe","RS":"Eastern Europe",
    # Nordamerika
    "US":"Northern America","CA":"Northern America","MX":"Central America",
    "GT":"Central America","HN":"Central America","SV":"Central America",
    "NI":"Central America","CR":"Central America","PA":"Central America",
    "CU":"Caribbean","DO":"Caribbean","HT":"Caribbean","JM":"Caribbean",
    # Südamerika
    "BR":"South America","CO":"South America","AR":"South America",
    "PE":"South America","VE":"South America","CL":"South America",
    "EC":"South America","BO":"South America","PY":"South America",
    "UY":"South America","GY":"South America","SR":"South America",
    # Ozeanien
    "AU":"Australia and New Zealand","NZ":"Australia and New Zealand",
    "PG":"Melanesia","FJ":"Melanesia","SB":"Melanesia","VU":"Melanesia",
    "WS":"Polynesia","TO":"Polynesia","KI":"Micronesia","MH":"Micronesia",
}

print("⬇  Lade countryInfo.txt …")
country_meta = {}  # iso2 → {continent, subregion, country_name}
try:
    with urllib.request.urlopen(COUNTRY_INFO_URL, timeout=30) as r:
        for line in io.TextIOWrapper(r, encoding="utf-8"):
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 9:
                continue
            iso2      = parts[0].strip()
            name      = parts[4].strip()
            continent = CONTINENT_MAP.get(parts[8].strip(), "Unknown")
            subregion = SUBREGION_MAP.get(iso2, continent)
            country_meta[iso2] = {"country": name, "continent": continent, "subregion": subregion}
    print(f"   {len(country_meta)} Länder geladen.")
except Exception as e:
    print(f"⚠  countryInfo.txt nicht erreichbar: {e}")
    print("   Verwende eingebettetes Fallback-Mapping …")

print("⬇  Lade cities5000.zip (~6 MB) …")
try:
    with urllib.request.urlopen(GEONAMES_URL, timeout=60) as r:
        zip_data = r.read()
    print("   Download OK.")
except Exception as e:
    sys.exit(f"✗ Download fehlgeschlagen: {e}")

print("⚙  Verarbeite Daten …")
cities_raw = []
with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
    fname = [f for f in z.namelist() if f.endswith(".txt")][0]
    with z.open(fname) as f:
        reader = csv.reader(io.TextIOWrapper(f, encoding="utf-8"), delimiter="\t")
        for row in reader:
            if len(row) < 15:
                continue
            try:
                pop = int(row[14])
            except ValueError:
                pop = 0
            if pop < MIN_POPULATION:
                continue

            iso2      = row[8].strip()
            meta      = country_meta.get(iso2, {})
            country   = meta.get("country", iso2)
            continent = meta.get("continent", "Unknown")
            subregion = meta.get("subregion", continent)

            if continent == "Unknown" or not iso2:
                continue

            cities_raw.append({
                "id":         int(row[0]),
                "name":       row[1].strip(),
                "asciiName":  row[2].strip(),
                "country":    country,
                "countryCode": iso2.lower(),
                "continent":  continent,
                "subregion":  subregion,
                "population": pop,
                "lat":        float(row[4]) if row[4] else 0,
                "lon":        float(row[5]) if row[5] else 0,
                "timezone":   row[17].strip() if len(row) > 17 else "",
            })

print(f"   {len(cities_raw)} Städte vor Filterung.")

# ── Rang je Land berechnen ────────────────────────────────────────────────────
cities_raw.sort(key=lambda x: x["population"], reverse=True)
rank_counter = defaultdict(int)
result = []
for city in cities_raw:
    cc = city["countryCode"]
    rank_counter[cc] += 1
    if rank_counter[cc] > MAX_RANK_COUNTRY:
        continue
    city["rank_in_country"] = rank_counter[cc]
    result.append(city)

# Nur eindeutige Namen (ASCII) je Land behalten
seen = set()
final = []
for city in result:
    key = (city["countryCode"], city["asciiName"].lower())
    if key not in seen:
        seen.add(key)
        final.append(city)

# ── Sortieren & ausgeben ──────────────────────────────────────────────────────
final.sort(key=lambda x: (-x["population"]))

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_FILE)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, separators=(",", ":"))

size_kb = os.path.getsize(out_path) // 1024
print(f"\n✓ {len(final)} Städte → {OUTPUT_FILE}  ({size_kb} KB)")
print(f"  Kontinente: {sorted(set(c['continent'] for c in final))}")
print(f"  Länder: {len(set(c['countryCode'] for c in final))}")
print(f"\n  Nächste Schritte:")
print(f"  1. cities.json neben GeoQuest.html ablegen")
print(f"  2. In GeoQuest.html die CITIES-Konstante durch")
print(f"     fetch('cities.json') ersetzen (oder alles inline lassen)")
