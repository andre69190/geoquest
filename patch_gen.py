#!/usr/bin/env python3
"""
patch_gen.py — GeoQuest Phases 54/55/56/59 source patches
Idempotent: safe to run multiple times.
Usage:  python patch_gen.py
Then:   python gen.py
"""
import os, sys

GEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py')
if not os.path.exists(GEN):
    sys.exit(f'ERROR: {GEN} not found')

print(f'Reading {GEN} ...')
with open(GEN, 'r', encoding='utf-8') as f:
    src = f.read()

applied  = []
skipped  = []
missing  = []

def patch(label, old, new):
    global src
    if old in src:
        src = src.replace(old, new, 1)
        applied.append(label)
        print(f'  + {label}')
    elif new in src:
        skipped.append(label)
        print(f'  . {label}  (already applied)')
    else:
        missing.append(label)
        print(f'  ! {label}  *** NOT FOUND — check gen.py manually ***')

print()
print('=== Fix 1 — Phase 55: rename local t → _tr (stops shadowing global t()) ===')
patch('_tr = tier(st)',
    old='const col=tc(),p=pct(),t=tier(st);',
    new='const col=tc(),p=pct(),_tr=tier(st);')
patch('${_tr.l} streak label',
    old='${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${t.l}</div>`:""}',
    new='${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${_tr.l}</div>`:""}')

print()
print('=== Fix 2 — Phase 54: German error messages in doRegister ===')
_OLD_REGISTER_ERR = (
    '    if(error){S.authError=error.message;S.authLoading=false;render();return;}\n'
    '    const uid=data.user?.id;'
)
_NEW_REGISTER_ERR = (
    '    if(error){\n'
    '      const _em=error.message||"";\n'
    '      S.authError=\n'
    '        _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":\n'
    '        _em.includes("Password should be")||_em.includes("password")?"Passwort zu schwach (mind. 6 Zeichen).":\n'
    '        _em.includes("valid email")||_em.includes("invalid format")||_em.includes("Unable to validate email")?"Bitte eine gültige E-Mail-Adresse eingeben.":\n'
    '        _em.includes("rate limit")||_em.includes("too many")?"Zu viele Versuche. Bitte kurz warten.":\n'
    '        _em||"Registrierung fehlgeschlagen.";\n'
    '      S.authLoading=false;render();return;\n'
    '    }\n'
    '    const uid=data.user?.id;'
)
patch('doRegister German error mapping', _OLD_REGISTER_ERR, _NEW_REGISTER_ERR)

_OLD_CATCH = (
    '  }catch(err){\n'
    '    S.authError=err.message||"Unbekannter Fehler.";\n'
    '    S.authLoading=false;\n'
    '    render();\n'
    '  }\n'
    '}\n'
    '\n'
    '/* Phase 27: Login */'
)
_NEW_CATCH = (
    '  }catch(err){\n'
    '    const _em=err.message||"";\n'
    '    S.authError=\n'
    '      _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":\n'
    '      _em.includes("valid email")||_em.includes("invalid format")?"Bitte eine gültige E-Mail-Adresse eingeben.":\n'
    '      _em||"Unbekannter Fehler.";\n'
    '    S.authLoading=false;\n'
    '    render();\n'
    '  }\n'
    '}\n'
    '\n'
    '/* Phase 27: Login */'
)
patch('doRegister catch-block German errors', _OLD_CATCH, _NEW_CATCH)

print()
print('=== Fix 3 — Phase 56: Joker guard clauses + disabled button state ===')
_OLD_FREEZE = (
    'function useFreeze(){\n'
    '  if(S.freezeActive)return;\n'
    '  const pu=loadPU();if(\\!(pu.freeze>0)){showToast("Kein Zeit-Stopp mehr\\!");return;}\n'
    '  pu.freeze--;savePU(pu);\n'
    '  clearInterval(tIv);S.freezeActive=true;\n'
    '  const bar=document.querySelector(".tbar");if(bar)bar.classList.add("frozen");\n'
    '  render();\n'
    '  setTimeout(()=>{\n'
    '    S.freezeActive=false;\n'
    '    const b2=document.querySelector(".tbar");if(b2)b2.classList.remove("frozen");\n'
    '    tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);answer(null);}else render();},1000);\n'
    '  },10000);\n'
    '}'
)
_NEW_FREEZE = (
    'function useFreeze(){\n'
    '  if(S.freezeActive)return;\n'
    '  const pu=loadPU();\n'
    '  if(\\!(pu.freeze>0)){showToast("Kein Zeit-Stopp mehr\\!");return;}\n'
    '  if(S.ph\\!=="playing"&&S.ph\\!=="feedback")return;\n'
    '  pu.freeze--;savePU(pu);\n'
    '  clearInterval(tIv);S.freezeActive=true;\n'
    '  const bar=document.querySelector(".tbar");if(bar)bar.classList.add("frozen");\n'
    '  render();\n'
    '  setTimeout(()=>{\n'
    '    if(S.ph\\!=="playing"&&S.ph\\!=="feedback"){S.freezeActive=false;return;}\n'
    '    S.freezeActive=false;\n'
    '    const b2=document.querySelector(".tbar");if(b2)b2.classList.remove("frozen");\n'
    '    if(S.ph==="playing"&&S.sel===null){\n'
    '      tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);answer(null);}else render();},1000);\n'
    '    }\n'
    '  },10000);\n'
    '}'
)
patch('useFreeze softlock guard', _OLD_FREEZE, _NEW_FREEZE)

_OLD_BTN_50 = (
    '<button class="pu-btn${S.half_removed?" pu-used":""}" onclick="useFiveO()" '
    'title="50/50-Joker (${pu.five0||0} \\u00fcbrig)">\\u2702 50/50 '
    '<span style="font-size:.62rem">(${pu.five0||0})</span></button>'
)
_NEW_BTN_50 = (
    '<button class="pu-btn${S.half_removed?" pu-used":""}" onclick="useFiveO()" '
    '${(S.half_removed||(pu.five0||0)===0)?"disabled":""} '
    'title="50/50-Joker (${pu.five0||0} \\u00fcbrig)">\\u2702 50/50 '
    '<span style="font-size:.62rem">(${pu.five0||0})</span></button>'
)
patch('50/50 button disabled when count=0', _OLD_BTN_50, _NEW_BTN_50)

_OLD_BTN_FRZ = (
    '<button class="pu-btn${S.freezeActive?" freeze-on":""}" onclick="useFreeze()" '
    'title="Zeit-Stopp (${pu.freeze||0} \\u00fcbrig)">\\u{1F9CA} Freeze '
    '<span style="font-size:.62rem">(${pu.freeze||0})</span></button>'
)
_NEW_BTN_FRZ = (
    '<button class="pu-btn${S.freezeActive?" freeze-on":""}" onclick="useFreeze()" '
    '${(S.freezeActive||(pu.freeze||0)===0)?"disabled":""} '
    'title="Zeit-Stopp (${pu.freeze||0} \\u00fcbrig)">\\u{1F9CA} Freeze '
    '<span style="font-size:.62rem">(${pu.freeze||0})</span></button>'
)
patch('Freeze button disabled when count=0', _OLD_BTN_FRZ, _NEW_BTN_FRZ)

print()
print('=== Fix 4 — HTML assembly: inject fresh CSS + ensure file write ===')
_OLD_ASSEMBLE = (
    "HTML = _HTML_HEAD + '<script>\\n' + JS + '\\n' + _HTML_TAIL\n"
    "\n"
    "out = 'GeoQuest.html'\n"
    "# Post-process: backslash-bang to plain bang (raw-string convention in JS block)\n"
    "HTML = HTML.replace('\\\\!', '!')\n"
    "with open(out, 'w', encoding='utf-8') as _f:\n"
    "    _f.write(HTML)\n"
    "print(f'Written: {len(HTML):,} chars → {out}')\n"
)
_NEW_ASSEMBLE = (
    "# Inject fresh CSS from geoquest_css.txt (overrides the static CSS in _HTML_HEAD)\n"
    "_si = _HTML_HEAD.find('<style>')\n"
    "_se = _HTML_HEAD.find('</style>') + len('</style>')\n"
    "if _si >= 0 and _se > _si:\n"
    "    _HTML_HEAD = _HTML_HEAD[:_si] + '<style>\\n' + CSS + '\\n</style>' + _HTML_HEAD[_se:]\n"
    "HTML = _HTML_HEAD + '<script>\\n' + JS + '\\n' + _HTML_TAIL\n"
    "HTML = HTML.replace('\\\\!', '!')\n"
    "out = 'GeoQuest.html'\n"
    "with open(out, 'w', encoding='utf-8') as _f:\n"
    "    _f.write(HTML)\n"
    "print(f'Written: {len(HTML):,} chars → {out}')\n"
)
patch('HTML assembly uses fresh CSS variable', _OLD_ASSEMBLE, _NEW_ASSEMBLE)

print()
print('=== Fix 5 — Phase 59a: Spotter input focus-loss (remove render() from oninput) ===')
_OLD_SPOTTER = "oninput=\"S.spotterInput=this.value.toUpperCase();this.value=this.value.toUpperCase();S.spotterMsg='';render()\""
_NEW_SPOTTER = "oninput=\"S.spotterInput=this.value.toUpperCase();this.value=this.value.toUpperCase();S.spotterMsg=''\""
patch('Spotter oninput: drop render() to preserve focus', _OLD_SPOTTER, _NEW_SPOTTER)

print()
print('=== Fix 6 — Phase 59b: Dynamic Home Header (greeting + GeoCoins / guest CTA) ===')
_OLD_HOME_HDR = '  return`${renderDailyHero()}\n    <div class="pvp-hero" onclick="S.mpModal=true;render()" role="button" aria-label="Live 1vs1 starten">'
_NEW_HOME_HDR = (
    '  /* Phase 59: Dynamic Home Header */\n'
    "  const _li=sbUser&&sbProfile?.username;\n"
    "  const _un=sbProfile?.username||(sbUser?.email?.split('@')[0]||'Gast');\n"
    "  const _gc=(sbProfile?.geo_coins||0).toLocaleString();\n"
    "  const _hdr=_li\n"
    "    ?`<div style=\"display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem .6rem;margin-bottom:.1rem\">\n"
    "        <div style=\"font-size:1.05rem;font-weight:700;color:var(--text)\">Hallo, ${_un} \\u{1F44B}</div>\n"
    "        <div style=\"display:flex;align-items:center;gap:5px;background:var(--bg2);border-radius:20px;padding:.28rem .75rem;font-size:.82rem;font-weight:700;color:#f59e0b;border:1px solid rgba(245,158,11,.25)\">\\u{1FA99} ${_gc}</div>\n"
    "      </div>`\n"
    "    :`<div style=\"display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem .6rem;margin-bottom:.1rem\">\n"
    "        <div style=\"font-size:1.05rem;font-weight:700;color:var(--text)\">Willkommen, Gast \\u{1F30D}</div>\n"
    "        <button onclick=\"S.tab='profil';render()\" style=\"background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border:none;border-radius:20px;padding:.3rem .8rem;font-size:.72rem;font-weight:700;cursor:pointer;white-space:nowrap;box-shadow:0 2px 8px rgba(99,102,241,.35)\">\\u{1F510} Fortschritt sichern</button>\n"
    "      </div>`;\n"
    '  return`${_hdr}${renderDailyHero()}\n'
    '    <div class="pvp-hero" onclick="S.mpModal=true;render()" role="button" aria-label="Live 1vs1 starten">'
)
patch('Home tab: dynamic header Phase 59', _OLD_HOME_HDR, _NEW_HOME_HDR)


print()
print('=== Fix 7 — Phase 60: Ad-container + loadAd() hook on Score Screen ===')

# 7a: insert ad banner before the share-btn
_OLD_AD_SLOT = '      <button class="share-btn" onclick="shareResult()">\\u{1F4CB} Ergebnis teilen</button>'
_NEW_AD_SLOT = (
    '      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);'
    'border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;'
    'color:var(--text3);font-size:.8rem">'
    'Danke, dass du GeoQuest spielst\\! \\u{1F499}</div>\n'
    '      <button class="share-btn" onclick="shareResult()">\\u{1F4CB} Ergebnis teilen</button>'
)
patch('Score screen: ad container slot', _OLD_AD_SLOT, _NEW_AD_SLOT)

# 7b: call loadAd after rendering gameover
_OLD_LOAD_AD_HOOK = '    </div>`;\n    return;\n  }\n\n  /* PLAYING / FEEDBACK */'
_NEW_LOAD_AD_HOOK = '    </div>`;\n    setTimeout(loadAd,100);\n    return;\n  }\n\n  /* PLAYING / FEEDBACK */'
patch('Score screen: setTimeout(loadAd,100)', _OLD_LOAD_AD_HOOK, _NEW_LOAD_AD_HOOK)

# 7c: add loadAd function in JS
_OLD_AFTER_SHARE = '\n}\nfunction updateHdrGuest(){'
_NEW_AFTER_SHARE = (
    '\n}\n'
    '/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */\n'
    'function loadAd(){\n'
    '  /* adsbygoogle.push({}); */\n'
    '}\n'
    'function updateHdrGuest(){'
)
patch('loadAd() stub function', _OLD_AFTER_SHARE, _NEW_AFTER_SHARE)

print()
print('=== Fix 8 — Phase 61: shareGame() viral share button on Score Screen ===')

# 8a: add shareGame button before NOCHMAL
_OLD_NOCHMAL = '      <button class="btn-p" onclick="rngSeed=null;S.challenge=null;S.challengeStarted=false;startGame()">NOCHMAL</button>'
_NEW_NOCHMAL = (
    '      <button class="btn-share-viral" onclick="shareGame()">\\u{1F4E4} Spiel teilen</button>\n'
    '      <button class="btn-p" onclick="rngSeed=null;S.challenge=null;S.challengeStarted=false;startGame()">NOCHMAL</button>'
)
patch('Score screen: shareGame viral button', _OLD_NOCHMAL, _NEW_NOCHMAL)

# 8b: add shareGame() JS function (after loadAd stub)
_OLD_AFTER_LOAD_AD = (
    '/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */\n'
    'function loadAd(){\n'
    '  /* adsbygoogle.push({}); */\n'
    '}\n'
    'function updateHdrGuest(){'
)
_NEW_AFTER_LOAD_AD = (
    '/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */\n'
    'function loadAd(){\n'
    '  /* adsbygoogle.push({}); */\n'
    '}\n'
    '/* Phase 61: Viral share — Web Share API with clipboard fallback */\n'
    'function shareGame(){\n'
    '  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\\! Schaffst du mehr?`;\n'
    '  const url=window.location.href;\n'
    '  if(navigator.share){\n'
    '    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});\n'
    '  }else{\n'
    '    navigator.clipboard.writeText(text+" "+url)\n'
    '      .then(()=>showToast(t("link_copied")||"Link kopiert\\!"))\n'
    '      .catch(()=>showToast("Link kopiert\\!"));\n'
    '  }\n'
    '}\n'
    'function updateHdrGuest(){'
)
patch('shareGame() viral share function', _OLD_AFTER_LOAD_AD, _NEW_AFTER_LOAD_AD)


print()
print('=== Fix 9 — Phase 62a: pop_compare country name text size ===')

_OLD_POP_CSS = '.pop-country{font-weight:900;font-size:.88rem;color:var(--text);margin-bottom:.3rem}'
_NEW_POP_CSS = '.pop-country{font-weight:900;font-size:1.3rem;color:var(--text);margin-bottom:.3rem}'
patch('pop-country font-size bump', _OLD_POP_CSS, _NEW_POP_CSS)

print()
print('=== Fix 10 — Phase 62b: Region filter in question generators ===')

# 10a: inject _regionOk + _rfilt helpers before genRiverQ
_OLD_BEFORE_RIVER = '}\nfunction genRiverQ(){'
_NEW_BEFORE_RIVER = (
    '}\n'
    '/* Phase 62: region filter helpers */\n'
    'function _regionOk(cc,cont){\n'
    '  const f=S.filter;\n'
    '  if(f==="all"||f==="eu_plates")return true;\n'
    '  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";\n'
    '  if(f==="europe")return c==="Europe";\n'
    '  if(f==="africa")return c==="Africa";\n'
    '  if(f==="oceania")return c==="Oceania";\n'
    '  if(f==="asia")return c==="Asia";\n'
    '  if(f==="america")return c.includes("America");\n'
    '  return true;\n'
    '}\n'
    'function _rfilt(pool,minLen){\n'
    '  if(S.filter==="all"||S.filter==="eu_plates")return pool;\n'
    '  const f=pool.filter(x=>_regionOk(x.cc,x.continent));\n'
    '  return f.length>=minLen?f:pool;\n'
    '}\n'
    'function genRiverQ(){'
)
patch('_regionOk + _rfilt helpers', _OLD_BEFORE_RIVER, _NEW_BEFORE_RIVER)

# 10b-10f: pool-based generators (have .name//.cc//.continent fields)
_POOL_PATCHES = [
    ('genRiverQ region filter',
     'const pool=RIVERS.filter(x=>x.name\\!==S.lid);if(pool.length<3)return null;',
     'const pool=_rfilt(RIVERS.filter(x=>x.name\\!==S.lid),3);if(pool.length<3)return null;'),
    ('genLandmarkQ region filter',
     'const pool=LANDMARKS.filter(x=>x.name\\!==S.lid);if(pool.length<3)return null;',
     'const pool=_rfilt(LANDMARKS.filter(x=>x.name\\!==S.lid),3);if(pool.length<3)return null;'),
    ('genParkQ region filter',
     'const pool=NATIONAL_PARKS.filter(x=>x.name\\!==S.lid);if(pool.length<3)return null;',
     'const pool=_rfilt(NATIONAL_PARKS.filter(x=>x.name\\!==S.lid),3);if(pool.length<3)return null;'),
    ('genUnescoQ region filter',
     'const pool=UNESCO_SITES.filter(x=>x.name\\!==S.lid);if(pool.length<3)return null;',
     'const pool=_rfilt(UNESCO_SITES.filter(x=>x.name\\!==S.lid),3);if(pool.length<3)return null;'),
    ('genCitymarkQ region filter',
     'const pool=CITY_LANDMARKS.filter(x=>x.name\\!==S.lid);if(pool.length<3)return null;',
     'const pool=_rfilt(CITY_LANDMARKS.filter(x=>x.name\\!==S.lid),3);if(pool.length<3)return null;'),
    ('genSubwayQ region filter',
     'const pool=SUBWAYS.filter(x=>x.city\\!==S.lid);if(pool.length<3)return null;',
     'const pool=_rfilt(SUBWAYS.filter(x=>x.city\\!==S.lid),3);if(pool.length<3)return null;'),
]
for label, old, new in _POOL_PATCHES:
    patch(label, old, new)

# 10g-10i: index-based generators (food/brand/currency — no pre-filter)
patch('genFoodQ region filter',
    'const idx=~~(rng()*FOOD_DATA.length);const item=FOOD_DATA[idx];',
    'const _fp=_rfilt(FOOD_DATA,3);const item=_fp[~~(rng()*_fp.length)];')

patch('genBrandQ region filter',
    'const idx=~~(rng()*BRANDS_DATA.length);const item=BRANDS_DATA[idx];',
    'const _bp=_rfilt(BRANDS_DATA,3);const item=_bp[~~(rng()*_bp.length)];')

patch('genCurrencyQ region filter',
    'const idx=~~(rng()*CURRENCIES_DATA.length);const item=CURRENCIES_DATA[idx];',
    'const _cp=_rfilt(CURRENCIES_DATA,3);const item=_cp[~~(rng()*_cp.length)];')

# ─── Summary ──────────────────────────────────────────────────────────────────
print()
print('=' * 60)
if applied:
    with open(GEN, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f'gen.py saved  — {len(applied)} patch(es) applied.')
    if skipped:
        print(f'                {len(skipped)} already done, {len(missing)} not found.')
else:
    print(f'No changes needed — {len(skipped)} already applied.')
    if missing:
        print(f'WARNING: {len(missing)} patch(es) not found (already different or gen.py changed):')
        for m in missing:
            print(f'  ! {m}')

if missing:
    print()
    print('Run this script again after checking the NOT FOUND items above.')
    sys.exit(1)

print()
print('All done. Now run:  python gen.py')
