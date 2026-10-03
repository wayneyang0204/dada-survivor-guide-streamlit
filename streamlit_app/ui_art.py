"""Bundled realistic red-kite artwork and original decorative vector icons.

The generated cutout is realistic artwork, not an in-game asset or a wildlife
documentary photo. It is embedded locally, without external image requests.
"""
from base64 import b64encode
from pathlib import Path

KITE_ASSET = Path(__file__).parent / "assets" / "red-kite-realistic-v1.webp"
_KITE_DATA = "data:image/webp;base64," + b64encode(KITE_ASSET.read_bytes()).decode("ascii")
_REAL_KITE = ('<g class="kite-flight"><g class="kite-direction">'
              f'<image class="kite-photo" x="28" y="36" width="184" height="123" href="{_KITE_DATA}"/>'
              '</g></g>')


GUIDE_BUDDY = ('<svg viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg" '
               'data-mascot="red-kite" aria-hidden="true" focusable="false">'
               + _REAL_KITE + '</svg>')


FIELD_BUDDY = ('''<svg viewBox="0 0 240 190" fill="none" xmlns="http://www.w3.org/2000/svg" data-mascot="red-kite" aria-hidden="true" focusable="false">
<g class="kite-cloud cloud-back"><path d="M13 49c-1-7 6-12 13-10 4-13 22-14 26-1 11-2 18 10 12 16H20q-7 0-7-5z" fill="#fff"/></g>
<g class="kite-cloud cloud-front"><path d="M175 151q-1-9 10-10c2-14 21-15 27-2 13-3 19 9 14 15h-44q-7 0-7-3z" fill="#fff"/></g>
<path class="kite-wind" d="M17 130h25m-19 8h12m162-94h23m-18 8h12" stroke="#b6d2df" stroke-width="2.4" stroke-linecap="round"/>
<path class="kite-sparkle" d="m202 18 2 6 6 2-6 2-2 6-2-6-6-2 6-2z" fill="#efc875"/>
''' + _REAL_KITE + '''
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
