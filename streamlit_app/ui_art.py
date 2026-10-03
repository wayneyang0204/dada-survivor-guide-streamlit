"""Original handbook illustrations; SVG only, with no external asset requests.

The little red kite is our own mascot, not an in-game character. All artwork is
decorative: nearby native controls and headings carry the accessible names.
"""

_RED_KITE = '''<g class="kite-flight"><g class="kite-character" stroke="#744635" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
<g class="kite-tail"><path d="M105 126 96 166l24-15 24 15-9-40z" fill="#c76946"/>
<path d="m112 135-6 18m22-18 6 18" stroke="#efac73" stroke-width="3"/></g>
<g class="kite-wing-left"><path d="M99 101C81 72 57 54 24 48q-10-1-3 11l19 19-17-8q-5 2 3 11l22 15-18-7q-5 3 4 12l24 16q22 12 43 1z" fill="#ad573e"/>
<path d="M24 48q-10-1-3 11l19 19-17-8q-5 2 3 11l22 15-18-7q-5 3 4 12l17 11 12-19-15-24z" fill="#68504a" stroke="none"/>
<path d="m53 72 12 26 17 5-13-26z" fill="#f4dfc1" stroke="none"/>
<path d="m72 78 15 20m-20-6 16 15" stroke="#e89a64" stroke-width="2.5"/></g>
<g class="kite-wing-right"><path d="M141 101c18-29 42-47 75-53q10-1 3 11l-19 19 17-8q5 2-3 11l-22 15 18-7q5 3-4 12l-24 16q-22 12-43 1z" fill="#ad573e"/>
<path d="M216 48q10-1 3 11l-19 19 17-8q5 2-3 11l-22 15 18-7q5 3-4 12l-17 11-12-19 15-24z" fill="#68504a" stroke="none"/>
<path d="m187 72-12 26-17 5 13-26z" fill="#f4dfc1" stroke="none"/>
<path d="m168 78-15 20m20-6-16 15" stroke="#e89a64" stroke-width="2.5"/></g>
<path d="M96 97q24-16 48 0l4 27q-2 25-28 26-26-1-28-26z" fill="#d78051"/>
<path d="M106 105q14-9 28 0l-2 27q-12 12-24 0z" fill="#f2c392" stroke="none"/>
<path d="m113 112 2 8m10-8-2 8m-3 5v7" stroke="#b46945" stroke-width="2"/>
<path d="m108 145 6-3 5 3m8 0 6-3 5 3" stroke="#e4ae50" stroke-width="3"/>
<g class="kite-head"><path d="M84 76c0-21 14-35 34-36l7-7 3 9c20 3 29 17 28 35-1 20-15 33-36 33S84 96 84 76z" fill="#e9e7e0"/>
<path d="M94 60q8-12 19-13m-8 8 5-3" stroke="#fffdf7" stroke-width="3"/>
<path d="m143 64 4 5m-4 5 5 4" stroke="#b6b8b1" stroke-width="2"/>
<ellipse cx="97" cy="91" rx="8" ry="5" fill="#efa89a" stroke="none"/><ellipse cx="143" cy="91" rx="8" ry="5" fill="#efa89a" stroke="none"/>
<g class="kite-eyes"><ellipse cx="106" cy="77" rx="5" ry="7" fill="#49392e" stroke="none"/><ellipse cx="134" cy="77" rx="5" ry="7" fill="#49392e" stroke="none"/>
<circle cx="104.5" cy="75" r="1.8" fill="#fff" stroke="none"/><circle cx="132.5" cy="75" r="1.8" fill="#fff" stroke="none"/></g>
<path d="M114 88q8-6 16-1l9 5q-10-1-12 9l-8-5z" fill="#edbe63"/>
<path d="m129 90 10 2q-6 1-8 6" fill="#68504a" stroke="none"/>
</g></g></g>'''


GUIDE_BUDDY = ('<svg viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg" '
               'data-mascot="red-kite" aria-hidden="true" focusable="false">'
               + _RED_KITE + '</svg>')


FIELD_BUDDY = ('''<svg viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg" data-mascot="red-kite" aria-hidden="true" focusable="false">
<g class="kite-cloud cloud-back"><path d="M13 49c-1-7 6-12 13-10 4-13 22-14 26-1 11-2 18 10 12 16H20q-7 0-7-5z" fill="#fff"/></g>
<g class="kite-cloud cloud-front"><path d="M175 151q-1-9 10-10c2-14 21-15 27-2 13-3 19 9 14 15h-44q-7 0-7-3z" fill="#fff"/></g>
<path class="kite-wind" d="M17 130h25m-19 8h12m162-94h23m-18 8h12" stroke="#b6d2df" stroke-width="2.4" stroke-linecap="round"/>
<path class="kite-sparkle" d="m202 18 2 6 6 2-6 2-2 6-2-6-6-2 6-2z" fill="#efc875"/>
''' + _RED_KITE + '''
</svg>''')


_SHAPES = {
    "home": '<path d="m7 16 17-12 17 12v23H7z" fill="#d7eccc"/><path d="M19 39V25h10v14" fill="#fff8ec"/><path d="m4 18 20-14 20 14"/>',
    "upgrade": '<path d="M8 36h9V26h10V16h13"/><path d="m32 8 8 8-8 8"/><circle cx="12" cy="11" r="5" fill="#e8cd85" stroke="none"/>',
    "profile": '<circle cx="24" cy="16" r="8" fill="#d7eccc"/><path d="M9 40c0-10 6-15 15-15s15 5 15 15z" fill="#fff8ec"/>',
    "event": '<rect x="7" y="11" width="34" height="30" rx="7" fill="#fff8ec"/><path d="M7 21h34M16 6v10M32 6v10"/><path d="m24 26 2 4 5 1-4 3 1 5-4-3-4 3 1-5-4-3 5-1z" fill="#efbba9" stroke="none"/>',
    "book": '<path d="M5 10q9-5 19 1 10-6 19-1v28q-9-5-19 1-10-6-19-1z" fill="#fff8ec"/><path d="M24 11v28M11 18h7M11 25h7M30 18h7M30 25h7"/>',
    "collection": '<path d="M8 18h32v23H8z" fill="#e3d8f2"/><path d="M6 11h36v10H6z" fill="#fff8ec"/><path d="M24 11v30M8 29h32"/><rect x="20" y="24" width="8" height="7" rx="2" fill="#e8cd85"/>',
    "gear": '<path d="m15 7 9 5 9-5 11 12-8 7-3-5v21H15V21l-3 5-8-7z" fill="#dbe8f2"/><path d="m20 21 4 5 4-5M19 33h10"/>',
    "tech": '<rect x="12" y="12" width="24" height="24" rx="7" fill="#e3d8f2"/><path d="M18 5v7M30 5v7M18 36v7M30 36v7M5 18h7M5 30h7M36 18h7M36 30h7"/><path d="m25 17-6 8h7l-3 6" stroke="#817390"/>',
    "pet": '<path d="M9 20 7 7l13 9m19 4 2-13-13 9" fill="#efbba9"/><path d="M8 27c0-10 7-15 16-15s16 5 16 15-7 16-16 16S8 37 8 27z" fill="#fff8ec"/><circle cx="18" cy="26" r="2" fill="#345c4f" stroke="none"/><circle cx="30" cy="26" r="2" fill="#345c4f" stroke="none"/><path d="m21 33 3 2 3-2"/>',
}


def guide_icon(name: str) -> str:
    """An allowlisted decorative icon; never interpolate user-authored SVG."""
    shape = _SHAPES.get(name, _SHAPES["book"])
    icon = ('<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" '
            'aria-hidden="true" focusable="false"><g stroke="#674936" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round">' + shape + '</g></svg>')
    # Keep the established icon vocabulary, adapted to the eagle's nest/sky palette.
    for old, new in (("#345c4f", "#674936"), ("#d7eccc", "#f0dfba"),
                     ("#e3d8f2", "#dceaf2"), ("#817390", "#638198")):
        icon = icon.replace(old, new)
    return icon


TOPIC_ART = {
    "特工養成": ("profile", "覺醒、轉主位與協同搭配"),
    "裝備神鑄": ("gear", "SS 裝備、神鑄斷點與材料"),
    "收藏典藏": ("collection", "黃收藏、紅自選與典藏館"),
    "科技配件": ("tech", "雙生配件、諧振與效果門檻"),
    "活動玩法": ("event", "免費進度、玩法與投入停損"),
    "寵物與關卡": ("pet", "寵物搭配與關卡判斷"),
}
