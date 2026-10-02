"""Original handbook illustrations; SVG only, with no external asset requests.

The sprout guide is our own mascot, not an in-game character. All artwork is
decorative: nearby native controls and headings carry the accessible names.
"""

GUIDE_BUDDY = '''<svg viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
<ellipse cx="81" cy="146" rx="49" ry="8" fill="#dbe9d8"/>
<path d="M35 92c-5-38 13-64 46-64s53 28 46 65l-6 34c-2 13-17 20-39 20s-39-8-41-21z" fill="#c7e8bf" stroke="#315d49" stroke-width="3"/>
<path d="M79 29c-7-17-1-24 12-24 2 13-2 21-12 24z" fill="#76b48c" stroke="#315d49" stroke-width="2.5"/>
<path d="M80 28c-1-13-12-19-22-14 1 11 10 17 22 14z" fill="#e6e9a5" stroke="#315d49" stroke-width="2.5"/>
<ellipse cx="58" cy="79" rx="11" ry="7" fill="#f3b7a2"/><ellipse cx="108" cy="79" rx="11" ry="7" fill="#f3b7a2"/>
<ellipse cx="65" cy="69" rx="4" ry="5" fill="#315d49"/><ellipse cx="101" cy="69" rx="4" ry="5" fill="#315d49"/>
<path d="M76 81q7 8 14 0" stroke="#315d49" stroke-width="3" stroke-linecap="round"/>
<path d="M59 108q13-5 24 1 12-6 25-1v27q-13-4-25 1-11-5-24-1z" fill="#fffaf0" stroke="#315d49" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M83 110v25m-17-16h9m16 0h9m-34 6h9m16 0h9" stroke="#b5c9b4" stroke-width="2" stroke-linecap="round"/>
<ellipse cx="53" cy="112" rx="9" ry="7" fill="#c7e8bf" stroke="#315d49" stroke-width="2.5"/><ellipse cx="112" cy="112" rx="9" ry="7" fill="#c7e8bf" stroke="#315d49" stroke-width="2.5"/>
<path d="m133 24 3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="#f1cd7a"/><circle cx="25" cy="51" r="4" fill="#d5c8ed"/>
</svg>'''


FIELD_BUDDY = '''<svg viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
<ellipse cx="124" cy="170" rx="90" ry="12" fill="#eadfd3"/>
<rect x="154" y="38" width="60" height="93" rx="9" transform="rotate(12 154 38)" fill="#fff" stroke="#dfccba" stroke-width="2"/>
<path d="m169 64 18 4m-21 8 29 6m-32 7 18 4" stroke="#dbc7b4" stroke-width="3" stroke-linecap="round"/>
<path d="M164 111h16m-13 9h21" stroke="#93ba9e" stroke-width="3" stroke-linecap="round"/>
<path d="M71 122c-16 0-20-17-12-28l19-14" fill="#a2cdae" stroke="#345c4f" stroke-width="2.5" stroke-linecap="round"/>
<path d="M73 93c-3-38 18-64 54-64 35 0 54 28 48 63l-8 46c-3 20-20 30-45 30s-42-11-46-28z" fill="#cce8c4" stroke="#345c4f" stroke-width="2.8"/>
<path d="M80 67c8-17 23-27 43-27" stroke="#eaf6e4" stroke-width="6" stroke-linecap="round"/>
<path d="M119 30c-12-2-21-12-19-22 15-1 23 7 19 22z" fill="#e8cd85" stroke="#345c4f" stroke-width="2.5"/>
<path d="M119 29c-2-16 8-26 21-23 0 15-7 22-21 23z" fill="#89bc98" stroke="#345c4f" stroke-width="2.5"/>
<ellipse cx="96" cy="87" rx="11" ry="7" fill="#efbba9"/><ellipse cx="156" cy="87" rx="11" ry="7" fill="#efbba9"/>
<ellipse cx="104" cy="75" rx="4" ry="5.5" fill="#345c4f"/><ellipse cx="146" cy="75" rx="4" ry="5.5" fill="#345c4f"/>
<path d="M119 88q7 9 14 0" stroke="#345c4f" stroke-width="2.8" stroke-linecap="round"/>
<path d="M93 118h58l-4 38H97z" fill="#eaf1df"/>
<path d="m86 112 31 5 10 33-30-5z" fill="#fffaf0" stroke="#345c4f" stroke-width="2.5" stroke-linejoin="round"/>
<path d="m117 117 32-13 11 33-33 13z" fill="#fff" stroke="#345c4f" stroke-width="2.5" stroke-linejoin="round"/>
<path d="m95 123 15 3m-12 6 13 2m17-12 15-6m-12 15 14-5" stroke="#c9d6be" stroke-width="2.4" stroke-linecap="round"/>
<ellipse cx="87" cy="120" rx="9" ry="7" transform="rotate(15 87 120)" fill="#cce8c4" stroke="#345c4f" stroke-width="2.5"/>
<ellipse cx="153" cy="118" rx="9" ry="7" transform="rotate(-25 153 118)" fill="#cce8c4" stroke="#345c4f" stroke-width="2.5"/>
<rect x="36" y="139" width="30" height="25" rx="6" fill="#e3d8f2" stroke="#817390" stroke-width="2"/>
<path d="M40 147h22m-11-7v23" stroke="#a695b8" stroke-width="2"/><rect x="47" y="146" width="8" height="6" rx="2" fill="#fff5db"/>
<path d="m198 16 3 9 9 3-9 3-3 9-3-9-9-3 9-3z" fill="#e8cd85"/>
<path d="m42 48 2 7 7 2-7 2-2 7-2-7-7-2 7-2z" fill="#bfaed9"/>
<circle cx="213" cy="153" r="4" fill="#efbba9"/><circle cx="61" cy="29" r="3" fill="#cce8c4"/>
</svg>'''


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
    return ('<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" '
            'aria-hidden="true" focusable="false"><g stroke="#345c4f" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round">' + shape + '</g></svg>')


TOPIC_ART = {
    "特工養成": ("profile", "覺醒、轉主位與協同搭配"),
    "裝備神鑄": ("gear", "SS 裝備、神鑄斷點與材料"),
    "收藏典藏": ("collection", "黃收藏、紅自選與典藏館"),
    "科技配件": ("tech", "雙生配件、諧振與效果門檻"),
    "活動玩法": ("event", "免費進度、玩法與投入停損"),
    "寵物與關卡": ("pet", "寵物搭配與關卡判斷"),
}
