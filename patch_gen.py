#!/usr/bin/env python3
"""
patch_gen.py — GeoQuest Phases 54/55/56 source patches
Idempotent: safe to run multiple times.
Usage:  python patch_gen.py
Then:   python gen.py
"""
import os, sys, re

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

# Buttons use double-quotes in ternary expressions (gen.py raw string style)
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

# Old: truncated gen.py ending (no with-open / print)
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
