"""Original handbook illustrations; SVG only, with no external asset requests.

The little eagle guide is our own mascot, not an in-game character. All artwork is
decorative: nearby native controls and headings carry the accessible names.
"""

_EAGLE = '''<g class="eagle-character" stroke="#674936" stroke-width="2.7" stroke-linecap="round" stroke-linejoin="round">
<path d="m64 132-7 16 12-5 12 7 7-17" fill="#c08b5e"/>
<path d="M42 92c-4-29 13-46 39-46s43 18 40 47l-3 28c-2 18-16 28-37 28s-35-10-37-28z" fill="#af7c54"/>
<path d="M64 96q17-10 34 0l-2 33q-15 15-30 0z" fill="#f5dfb7" stroke="none"/>
<g class="eagle-wings"><g class="eagle-wing-left"><path d="M45 85c-20 6-23 31-11 43l18-21" fill="#af7c54"/>
<path d="m32 112 11-9" stroke="#8c603f"/></g><g class="eagle-wing-right"><path d="M117 85c20 6 23 31 11 43l-18-21" fill="#af7c54"/>
<path d="m130 112-11-9" stroke="#8c603f"/></g></g>
<g class="eagle-head"><path d="M29 70c-1-24 15-43 38-47l-2-8 14 6 10-9 4 11c24 4 40 23 39 47-1 17-11 28-25 30l-9-5-9 8-9-6-9 6-10-8-9 5c-15-3-23-14-23-30z" fill="#fffdf7"/>
<path d="M40 48c6-11 16-17 27-19" stroke="#fff" stroke-width="4"/>
<ellipse cx="51" cy="80" rx="9" ry="6" fill="#efbea7" stroke="none"/><ellipse cx="111" cy="80" rx="9" ry="6" fill="#efbea7" stroke="none"/>
<g class="eagle-eyes"><ellipse cx="62" cy="65" rx="5" ry="6.5" fill="#40342c" stroke="none"/><ellipse cx="102" cy="65" rx="5" ry="6.5" fill="#40342c" stroke="none"/>
<circle cx="60.5" cy="63" r="1.7" fill="#fff" stroke="none"/><circle cx="100.5" cy="63" r="1.7" fill="#fff" stroke="none"/></g>
<path d="M75 76c4-5 14-6 21-2l10 7c-8 0-11 3-11 10l-10-4-6-4z" fill="#efbd59"/>
<path d="m87 78 7 3" stroke="#d29a3d" stroke-width="1.6"/></g>
<g class="eagle-book"><path d="M56 109q13-5 25 1 12-6 25-1v26q-13-4-25 1-12-5-25-1z" fill="#fffdf7"/>
<path d="M81 111v24m-17-16h9m16 0h9m-34 6h9m16 0h9" stroke="#b9cbd1" stroke-width="2"/>
<path class="eagle-page-leaf" d="M82 111q12-6 24-2v26q-13-4-24 1z" fill="#fff7e2" stroke="#d9c5ac" stroke-width="1.4"/></g>
<path d="M50 114c1-8 12-7 15 0l-9 9c-5 1-9-4-6-9zm62 0c-1-8-12-7-15 0l9 9c5 1 9-4 6-9z" fill="#af7c54"/>
<path d="M62 145v6m-5 0h12m28-6v6m-5 0h12" stroke="#d69c42" stroke-width="3.5"/>
</g>'''


GUIDE_BUDDY = ('<svg viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" '
               'data-mascot="eagle" aria-hidden="true" focusable="false">'
               '<ellipse class="eagle-shadow" cx="81" cy="153" rx="48" ry="5" fill="#e9dac1"/>' + _EAGLE + '</svg>')


FIELD_BUDDY = ('''<svg viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg" data-mascot="eagle" aria-hidden="true" focusable="false">
<ellipse class="eagle-shadow" cx="125" cy="176" rx="70" ry="7" fill="#eadbc7"/>
<path d="M17 49c0-7 6-12 13-11 4-12 21-12 25-1 11-2 17 11 11 16H23c-4 0-6-1-6-4z" fill="#fff"/>
<rect x="171" y="47" width="51" height="78" rx="8" transform="rotate(12 171 47)" fill="#fff" stroke="#d9c5ac" stroke-width="2"/>
<path d="m184 70 18 4m-20 8 23 5m-26 6 16 3" stroke="#d9c5ac" stroke-width="2.5" stroke-linecap="round"/>
<path d="m182 106 5 5 10-10" stroke="#86a5b7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<path class="eagle-sparkle" d="m206 20 3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="#efc875"/>
<circle class="eagle-sparkle sparkle-late" cx="24" cy="113" r="4" fill="#abc4d1"/><circle cx="223" cy="149" r="3" fill="#efbea7"/>
<g class="eagle-sleep-marks" stroke="#86a5b7" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M161 40h10l-10 10h10m7-26h13l-13 13h13"/></g>
<g transform="translate(36 9) scale(1.08)">''' + _EAGLE + '''</g>
<path d="M26 156q7-12 14-5-1 11-14 13m14-13q8-9 14-1-3 9-14 9" fill="#c8d7df" stroke="#86a5b7" stroke-width="2" stroke-linejoin="round"/>
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
