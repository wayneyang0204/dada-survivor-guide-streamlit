from __future__ import annotations

import html
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SOURCE_CATEGORY_URL = "https://notalknote.xyz/moblegame/survivorio/"
SOURCE_API_BASE = "https://notalknote.xyz/wp-json/wp/v2/posts"


def strip_html(value: str) -> str:
    value = re.sub(r"<script.*?</script>|<style.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def classify_article(title: str, excerpt: str = "") -> str:
    text = f"{title} {excerpt}"
    if "區域行動" in title:
        return "關卡模式"
    rules = [
        ("活動攻略", ("活動", "慶典", "派對", "扭蛋", "拼圖", "探寶", "尋寶", "格子舖", "礦場", "彩虹礦", "彩虹棋", "彩虹骰", "一番賞", "訂單員", "轉盤", "圓盤", "麥克風")),
        ("角色特工", ("特工", "角色", "覺醒", "同調", "協同", "碎片")),
        ("寵物系統", ("寵物", "異世", "異寵", "助戰")),
        ("科技配件", ("科技配件", "雙生配件", "諧振", "共振", "制導系統", "控制器", "偏振器", "裝置")),
        ("收藏系統", ("收藏", "典藏館", "收藏之心", "解構")),
        ("裝備養成", ("神器", "神鑄", "星鑄", "裝備", "武器", "護手", "腰帶", "戰衣", "項鍊", "戰靴", "融合")),
        ("關卡模式", ("關卡", "區域行動", "末世迴響", "試煉", "遠征", "首領", "Boss", "主線")),
        ("資源工具", ("無課", "兌換碼", "計算", "試算", "資源", "課金")),
    ]
    for category, keywords in rules:
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return category
    return "綜合資料"


def _freshness(date_text: str, category: str) -> str:
    try:
        published = datetime.strptime(date_text[:10], "%Y-%m-%d")
        days = (datetime.now() - published).days
    except ValueError:
        return "日期待核對"
    if category == "活動攻略":
        if days <= 21:
            return "近期活動"
        if days <= 90:
            return "近期機制"
        return "歷史活動"
    if days <= 240:
        return "現行參考"
    if days <= 730:
        return "常駐機制"
    return "需版本核對"


def fetch_source_posts(max_pages: int = 2, per_page: int = 100) -> list[dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    fields = "id,link,title,date,modified,excerpt,slug"
    for page in range(1, max_pages + 1):
        query = urlencode(
            {
                "categories": 624,
                "per_page": per_page,
                "page": page,
                "orderby": "date",
                "order": "desc",
                "_fields": fields,
            }
        )
        request = Request(
            f"{SOURCE_API_BASE}?{query}",
            headers={"User-Agent": "Mozilla/5.0 (compatible; DadaGuide/1.0)"},
        )
        try:
            with urlopen(request, timeout=10) as response:
                import json

                batch = json.loads(response.read().decode("utf-8"))
        except Exception:
            if posts:
                break
            raise
        if not batch:
            break
        for post in batch:
            title = strip_html(post.get("title", {}).get("rendered", ""))
            title = title.replace("【噠噠特攻】", "").strip()
            excerpt = strip_html(post.get("excerpt", {}).get("rendered", ""))
            category = classify_article(title, excerpt)
            date_text = post.get("date", "")
            posts.append(
                {
                    "id": post.get("id"),
                    "title": title,
                    "excerpt": excerpt,
                    "date": date_text[:10].replace("-", "/"),
                    "raw_date": date_text[:10],
                    "modified": post.get("modified", "")[:10].replace("-", "/"),
                    "link": post.get("link", ""),
                    "slug": post.get("slug", ""),
                    "category": category,
                    "freshness": _freshness(date_text, category),
                }
            )
        if len(batch) < per_page:
            break
    return sorted(posts, key=lambda item: item.get("raw_date", ""), reverse=True)


def _edition_for_id(item_id: int) -> int:
    for ceiling, edition in (
        (30, 1),
        (47, 2),
        (78, 3),
        (110, 4),
        (140, 5),
        (170, 6),
        (200, 7),
        (230, 8),
        (260, 9),
    ):
        if item_id <= ceiling:
            return edition
    return 10


def load_collectible_catalog() -> list[dict[str, Any]]:
    source = Path(__file__).resolve().parents[1] / "lib" / "collectibles-data.ts"
    text = source.read_text(encoding="utf-8")
    match = re.search(r"const rawCatalog = `\s*(.*?)\s*`;", text, flags=re.S)
    if not match:
        return []
    quality_names = {11: "傳奇", 7: "史詩", 4: "優秀", 3: "精良", 2: "普通"}
    catalog = []
    for row in match.group(1).splitlines():
        parts = row.strip().split("|")
        if len(parts) != 4:
            continue
        raw_id, raw_quality, slug, name = parts
        item_id = int(raw_id)
        catalog.append(
            {
                "id": item_id,
                "name": name,
                "quality": quality_names.get(int(raw_quality), "未知"),
                "edition": _edition_for_id(item_id),
                "image": f"https://wsrv.nl/?output=webp&url=https://garrytools.com/assets/img/survivor/UITexture/CollectionIcon/{item_id}_{slug}.png&hash=511",
                "link": f"https://garrytools.com/collections/info?collectionId={item_id}",
            }
        )
    return sorted(catalog, key=lambda item: (item["edition"], item["id"]))


EVENT_PLAYBOOKS = [
    {
        "name": "水上樂園大亂鬥",
        "keywords": ("水上樂園", "水槍"),
        "mechanic": "使用水槍參加活動；官方目前只公開可能獲得的主要獎勵，完整玩法、任務總量、機率與里程碑仍待核對。",
        "target": 0,
        "unit": "活動進度",
        "free_hint": "官方尚未公布完整免費水槍總量；先領登入、任務與免費領取，並以遊戲內倒數為準。",
        "verdict": "獎勵表與成本未核實前只做免費進度，不先花寶石或開大量寶箱。",
        "period": "以遊戲內倒數為準",
        "tags": ["官方活動", "免費水槍優先", "轉化核心", "限定收藏品", "異獸碎片"],
        "highlights": [
            ("已確認玩法", "使用水槍參加活動；先領完登入、任務與免費取得量。"),
            ("已確認獎勵", "可能取得轉化核心、限定收藏品與幽冥烈焰追獵者碎片。"),
            ("仍待核對", "結束時間、任務總量、掉落機率與各里程碑成本尚未有完整可靠資料。"),
            ("目前決策", "只做免費進度；完整獎勵表與成本補齊後再設定停損線。"),
        ],
        "steps": ["先領登入、任務與免費水槍", "進遊戲核對倒數、獎勵表與水槍取得量", "記下高價獎勵所在里程碑", "可靠數值補齊前不投入寶石或大量鑰匙"],
        "avoid": "不要把官方列出的『可能取得』當成保底，也不要在任務數與里程碑未核實前預先砸資源。",
    },
    {
        "name": "煲湯廚房",
        "keywords": ("煲湯廚房", "湯勺", "砂鍋"),
        "mechanic": "每輪八個砂鍋會隨烹飪增加一至七點；超過二十四點會破裂，二十二至二十四點的鍋會鎖定為安全狀態。",
        "target": 220,
        "unit": "累計湯勺",
        "free_hint": "本期已於 9 月 9 日結束；社群攻略曾估算完整任務約可取得三百至三百二十二張湯勺，復刻時必須重新核對。",
        "verdict": "本期已結束；以下只保留作復刻核對，不能直接當成現行活動。",
        "period": "9/5 00:00－9/9 23:59（五天）",
        "tags": ["歷史活動", "八個砂鍋", "二十四點上限", "二百二十湯勺停損", "異世寵物養成"],
        "summary_sections": [
            {
                "title": "砂鍋安全線",
                "items": [
                    ("基本規則", "每輪最少烹飪三次，之後可隨時出鍋結算。"),
                    ("安全區間", "二十二至二十四點會鎖定，不再加點也不會破裂。"),
                    ("危險區間", "多數砂鍋在十八至二十一點時應收手，避免下一次加點超標。"),
                    ("操作節奏", "一般四至五次烹飪後出鍋較穩，不為單輪高分承擔大量破鍋。"),
                ],
            },
            {
                "title": "里程碑與鑰匙成本",
                "items": [
                    ("累計一百六十", "史詩寵物自選禮包，約開二百箱可穩定抵達。"),
                    ("累計二百二十", "異世寵物自選箱，約需開三百八十至四百箱，是一般玩家主要停損點。"),
                    ("累計三百", "異世靈藥，約需開五百六十箱；只有鑰匙庫存充足才追。"),
                    ("停損原則", "不要為了三百檔位硬開滿六百箱，也不要把鑰匙消耗視為零成本。"),
                ],
            },
            {
                "title": "商店兌換順序",
                "items": [
                    ("最高優先", "萬能神火特工碎片。"),
                    ("第二優先", "正在培養異世寵物時換特工寵物餅乾。"),
                    ("依缺口兌換", "覺醒水晶與異世寵物水晶。"),
                    ("零頭處理", "最後再換寵物寶箱鑰匙。"),
                ],
            },
        ],
        "highlights": [
            ("砂鍋規則", "超過二十四點會破裂；二十二至二十四點是鎖定安全區間。"),
            ("推薦進度", "累計二百二十湯勺拿異世寵物自選箱；一般玩家先停在這裡。"),
            ("進階目標", "累計三百湯勺拿異世靈藥，約需開五百六十箱且要確認帳號真的缺它。"),
            ("最後一天", "先領完日常與免費湯勺，再依目前缺口決定是否開箱補檔。"),
        ],
        "steps": ["先完成登入與每日免費湯勺", "每輪四至五次烹飪，危險鍋多就立即出鍋", "先補到累計二百二十湯勺", "鑰匙充足且異世靈藥可立即跨斷點時才追三百"],
        "avoid": "不要讓砂鍋超過二十四點，也不要為了三百檔位耗光後續活動需要的鑰匙。",
    },
    {
        "name": "音樂圓盤大作戰",
        "keywords": ("音樂圓盤", "麥克風", "音符"),
        "mechanic": "消耗麥克風轉動圓盤並取得音符；盤面會返還部分麥克風，判斷成本時要把返還率一起算進去。",
        "target": 980,
        "unit": "累計進度",
        "free_hint": "攻略實測免費票券約 900 張，盤面麥克風返還率約 44%～47%，實質進度約可放大 1.5 倍。",
        "verdict": "免費票先跑完，累計 980 是目前獎勵與資源消耗最平衡的停損點。",
        "period": "8/30 00:00－9/3 23:59（5 天）",
        "tags": ["轉盤攻擊機制", "45% 票券返還率", "最佳開箱檔位", "商店兌換優先級"],
        "summary_sections": [
            {
                "title": "票券數量與 45% 返還機制",
                "items": [
                    ("免費票券總量", "任務＋廣告＋登入約可拿 900 張麥克風。"),
                    ("盤面返還機制", "消耗麥克風後盤面會掉落補回，平均返還率約 44%～47%。"),
                    ("實質進度放大", "900 張票券實際可跑約 1,300＋累計進度，約為票券數的 1.5 倍。"),
                    ("自動連打技巧", "長按自動按鈕可連續抽取技能，適合跑完整張圓盤。"),
                ],
            },
            {
                "title": "寶箱任務改動與開箱策略",
                "items": [
                    ("開箱任務改動", "開到 320 箱後，每 20 箱仍會給票券；若只看本次活動，開滿 600 箱的單抽收益最高。"),
                    ("平民最佳檔位", "建議先開 200～300 箱即可，不需要為任務盲目硬開滿 600 箱。"),
                    ("資源長線規劃", "週年活動後鑰匙庫存偏緊，應保留給後續新特工或大型活動。"),
                    ("最終微調原則", "前 4 天正常解任務，最後一天再依進度補開箱或補少量寶石。"),
                ],
            },
            {
                "title": "推薦累計進度檔位選擇",
                "items": [
                    ("累計 780", "S 級裝備自選箱，屬於無課玩家的基本推薦目標。"),
                    ("累計 980", "諧振晶片＋傳奇收藏品自選寶箱，是全體玩家最推薦的甜蜜點。"),
                    ("累計 1,250", "傳奇收藏品解構機，通常需要開 400～600 箱或投入大量寶石。"),
                    ("建議結論", "鎖定 980 檔位性價比最高；除非解構機能立刻補上關鍵斷點，否則不追 1,250。"),
                ],
            },
            {
                "title": "活動商店兌換優先級",
                "items": [
                    ("最高優先", "紅色收藏品自選箱、萬能神火特工碎片，整體戰力提升最高。"),
                    ("次高優先", "高級收藏之心。"),
                    ("依需求兌換", "特工寵物餅乾；正在主力培養異世寵物的玩家再換。"),
                    ("避雷指南", "配件選擇箱沒有折扣時不要換，活動點數應鎖定高階稀有物資。"),
                ],
            },
        ],
        "highlights": [
            ("免費票券", "約 900 張；盤面麥克風返還率約 44%～47%，實質進度約放大 1.5 倍。"),
            ("推薦進度", "累計 980：可拿諧振晶片與傳奇收藏品自選寶箱，無課優先停在這裡。"),
            ("開箱策略", "先開 200～300 箱，最後一天依差額微調；不要為任務盲目開滿 600 箱。"),
            ("商店必換", "紅色收藏品自選箱 ＞ 萬能神火特工碎片 ＞ 高級收藏之心。"),
        ],
        "steps": ["先拿完登入、每日任務與免費麥克風", "先開 200～300 箱，再看最後一天差額", "只補到累計 980，達標後停手", "商店依紅色收藏、萬能神火特工碎片、高級收藏之心順序兌換"],
        "avoid": "不要在活動前期先砸寶石，也不要為了完成 600 箱任務犧牲長期鑰匙庫存。",
    },
    {
        "name": "4週年彩虹骰",
        "keywords": ("彩虹骰",),
        "mechanic": "7×7 棋盤與縱橫十字攻擊；普通、火焰、雷電骰要依高價值格密度使用。",
        "target": 320,
        "unit": "開箱／任務進度",
        "free_hint": "攻略資料顯示開箱 320 次可在不額外花鑽的情況拿核心自選箱。",
        "steps": ["先用普通骰清資訊與低價格", "火焰／雷電骰留給十字能同時命中多個高價格時", "先換派對邀請函，再換 4 折核心自選箱"],
        "avoid": "不要在棋盤資訊不足時連續丟特殊骰，也不要為低價小獎越過下一個核心斷點。",
    },
    {
        "name": "4週年彩虹礦",
        "keywords": ("彩虹礦",),
        "mechanic": "挖礦開圖；中心點與棋盤式探測能用較少十字鎬定位大礦脈。",
        "target": 1000,
        "unit": "十字鎬上限參考",
        "free_hint": "來源攻略以無課約 1000 把十字鎬作極限進度參考。",
        "steps": ["先點中心與交錯格找輪廓", "大礦確認後才集中挖掘", "派對邀請函與 4 折核心自選箱優先"],
        "avoid": "不要從邊角逐格清空，也不要把爆破道具浪費在未確認的大礦區。",
    },
    {
        "name": "4週年陽光彩虹棋",
        "keywords": ("陽光彩虹棋", "400抽", "彩虹棋"),
        "mechanic": "顏色移動與幸運模式；週年禮券可跨週年子活動累積。",
        "target": 400,
        "unit": "陽光券",
        "free_hint": "特殊補償方案曾以 400 張券解鎖 6 倍里程碑與 2400 進度；只適用該次公告。",
        "steps": ["先確認帳號是否符合補償", "幸運模式期間集中操作", "差額不大時再用派對回收的寶石補券"],
        "avoid": "補償數字不是永久規則；新一輪復刻必須先看遊戲內公告。",
    },
    {
        "name": "一番賞／共享獎池",
        "keywords": ("一番賞", "共享抽獎箱"),
        "mechanic": "多人共享剩餘獎池，價值取決於剩餘抽數、剩餘大獎與尾獎。",
        "target": 0,
        "unit": "抽數",
        "free_hint": "只在剩餘獎池期望值明顯高於單抽成本時狙擊。",
        "steps": ["先看剩餘總抽數", "計算大獎＋尾獎總價值", "只狙擊別人已抽掉大量小獎的箱"],
        "avoid": "不要對滿池盲抽，也不要為了沉沒成本追已失去尾獎的池。",
    },
    {
        "name": "幸運扭蛋",
        "keywords": ("幸運扭蛋",),
        "mechanic": "抽獎返還、限時輪換獎池與好友互送；要同時計算返還率和目標池。",
        "target": 350,
        "unit": "活動進度",
        "free_hint": "2026 攻略以 25% 返還、開箱 320/380 次衝 350 進度為參考。",
        "steps": ["只在目標獎池時段抽", "好友互送先提高幸運值", "計入返還後再算實際缺口"],
        "avoid": "不要在非目標獎池消耗，也不要把表面抽數當成實際成本。",
    },
    {
        "name": "航海格子舖",
        "keywords": ("航海格子舖",),
        "mechanic": "高單抽成本的格子商店；重點是里程碑停損，不是清空所有格。",
        "target": 220,
        "unit": "活動進度",
        "free_hint": "2026 攻略以開箱 320 次加少量鑽石達 220 進度拿神器核心為參考。",
        "steps": ["先做免費任務與開箱", "只補到 220 核心里程碑", "達標後立即停手"],
        "avoid": "單抽昂貴，不應為普通格或排名繼續投入。",
    },
    {
        "name": "森林探寶尋真",
        "keywords": ("森林探寶",),
        "mechanic": "左側目標與右側輪盤配對；先鎖定目標再放大鏡。",
        "target": 660,
        "unit": "里程碑",
        "free_hint": "攻略估算約 696 張免費放大鏡可卡 660 里程碑。",
        "steps": ["每輪先確認左側目標", "只把加成用在正確配對", "660 異寵核心後停手"],
        "avoid": "不要在低倍率或錯誤目標時把放大鏡一次用完。",
    },
    {
        "name": "時光拼圖",
        "keywords": ("時光拼圖",),
        "mechanic": "翻牌與自動跳過；可用道具箱減少低價翻牌。",
        "target": 850,
        "unit": "里程碑",
        "free_hint": "2026 復刻攻略以 850 里程碑神話核心自選箱為主要停損點。",
        "steps": ["啟用自動跳過低價過程", "道具箱留給差一點跨里程碑時", "商店先 SP 碎片與載具碎片"],
        "avoid": "不要為了清完一張圖越過 850 後的低效率區。",
    },
    {
        "name": "生日派對",
        "keywords": ("生日派對",),
        "mechanic": "自動輪盤型，主要看免費票券能否跨里程碑。",
        "target": 50,
        "unit": "里程碑",
        "free_hint": "2026 攻略以約 662 張免費票券達 50 里程碑拿異寵核心為參考。",
        "steps": ["先收齊每日免費票券", "最後一天再補差額", "50 核心里程碑後停手"],
        "avoid": "不要前幾天就用寶石，先等免費任務總量確定。",
    },
    {
        "name": "神火特攻／SP 特工",
        "keywords": ("神火特攻", "伏爾甘", "哪吒"),
        "mechanic": "SP 特工保底型高消耗活動；是否投入取決於角色能否直接成為主力。",
        "target": 60000,
        "unit": "寶石保底參考",
        "free_hint": "伏爾甘攻略估算約 6 萬寶石，哪吒約 58,500 寶石；每次復刻仍須重算。",
        "steps": ["先確認能一次拿到角色／關鍵星級", "把免費票與寶石一起算", "資源不足完整保底就不開追"],
        "avoid": "不要只拿半套 SP 角色，導致主力帳號其他系統全部停滯。",
    },
    {
        "name": "王牌訂單員",
        "keywords": ("王牌訂單員", "王牌推銷員"),
        "mechanic": "工廠與訂單營運；前期升工廠、後期挑高報酬訂單。",
        "target": 0,
        "unit": "訂單積分",
        "free_hint": "這類活動的關鍵是每單資源報酬率，而不是完成訂單數。",
        "steps": ["第一天優先升工廠", "利用好友支援與萬能物資", "只做高積分／稀缺資源訂單"],
        "avoid": "跳過吃大量稀缺物資卻只給普通獎勵的地雷訂單。",
    },
    {
        "name": "通用活動模型",
        "keywords": (),
        "mechanic": "以免費進度、目標缺口、單位寶石成本與帳號斷點做停損。",
        "target": 0,
        "unit": "活動進度",
        "free_hint": "先做完免費任務，最後 24 小時再決定是否補寶石。",
        "steps": ["先拿登入與每日免費資源", "把免費進度投影到活動結束", "只為能立即跨過的高價值斷點補差額"],
        "avoid": "不要前幾天就花光鑰匙與寶石，也不要因為已投入而追低價里程碑。",
    },
]


REWARD_CATALOG = [
    {"name": "神器核心自選箱", "base_score": 100, "gem_value": 18000, "goals": ("神器核心", "終局裝備")},
    {"name": "異世寵物核心自選箱", "base_score": 98, "gem_value": 18000, "goals": ("異世寵物", "終局裝備")},
    {"name": "SP 特工碎片／自選箱", "base_score": 94, "gem_value": 60000, "goals": ("SP特工／覺醒",)},
    {"name": "雙生／永恆科技配件自選", "base_score": 90, "gem_value": 15000, "goals": ("科技配件", "終局裝備")},
    {"name": "傳奇收藏品自選箱", "base_score": 84, "gem_value": 12000, "goals": ("收藏品", "終局裝備")},
    {"name": "S 級裝備自選箱", "base_score": 82, "gem_value": 10000, "goals": ("S裝備",)},
    {"name": "特工覺醒核心", "base_score": 78, "gem_value": 10000, "goals": ("SP特工／覺醒",)},
    {"name": "載具核心／碎片", "base_score": 74, "gem_value": 12000, "goals": ("載具", "終局裝備")},
    {"name": "派對邀請函", "base_score": 72, "gem_value": 12000, "goals": ("通用",)},
    {"name": "鑰匙與寶石", "base_score": 50, "gem_value": 3000, "goals": ("通用",)},
    {"name": "一般材料／金幣", "base_score": 25, "gem_value": 500, "goals": ("通用",)},
    {"name": "頭像框／外觀", "base_score": 8, "gem_value": 0, "goals": ("收藏外觀",)},
]


def match_event_playbook(title: str) -> dict[str, Any]:
    lowered = title.lower()
    for playbook in EVENT_PLAYBOOKS[:-1]:
        if any(keyword.lower() in lowered for keyword in playbook["keywords"]):
            return playbook
    return EVENT_PLAYBOOKS[-1]


def rank_rewards(goal: str, stage: str) -> list[dict[str, Any]]:
    ranked = []
    for reward in REWARD_CATALOG:
        multiplier = 1.0
        if goal in reward["goals"]:
            multiplier += 0.45
        if "通用" in reward["goals"] and goal == "不確定，幫我排":
            multiplier += 0.08
        if stage == "尚未紅裝成套":
            if reward["name"] == "S 級裝備自選箱":
                multiplier += 0.55
            if "神器核心" in reward["name"]:
                multiplier -= 0.2
        elif stage == "紅裝成套、神器核心不足":
            if "神器核心" in reward["name"]:
                multiplier += 0.35
        elif stage == "主要裝備斷點已完成":
            if any(word in reward["name"] for word in ("異世寵物", "科技配件", "收藏品")):
                multiplier += 0.25
        item = dict(reward)
        item["score"] = round(reward["base_score"] * multiplier)
        item["adjusted_gem_value"] = round(reward["gem_value"] * max(0.7, multiplier))
        ranked.append(item)
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


def assess_event_plan(
    *,
    current_progress: int,
    days_remaining: int,
    free_progress_per_day: int,
    target_progress: int,
    progress_per_paid_action: float,
    gems_per_paid_action: int,
    gems_owned: int,
    spending_style: str,
    target_reward: dict[str, Any],
) -> dict[str, Any]:
    projected_free = current_progress + days_remaining * free_progress_per_day
    gap = max(0, target_progress - projected_free)
    paid_actions = 0 if gap == 0 else math.ceil(gap / max(progress_per_paid_action, 0.01))
    gem_need = paid_actions * gems_per_paid_action
    reserve = {"無課／只用免費資源": 30000, "微課／可小補寶石": 15000, "課金／只看效率": 5000}.get(spending_style, 20000)
    spendable = max(0, gems_owned - reserve)
    value_cap = target_reward.get("adjusted_gem_value", target_reward.get("gem_value", 0))

    if target_progress <= current_progress:
        verdict = "已達標，立刻停手"
        tone = "success"
        reason = "目前進度已經跨過目標，不要把沉沒成本變成更多消耗。"
    elif gap == 0:
        verdict = "值得追，但不用花寶石"
        tone = "success"
        reason = "依剩餘免費進度可自然達標；每天做完免費任務即可。"
    elif gem_need <= spendable and gem_need <= value_cap:
        verdict = "值得補到目標後停手"
        tone = "success"
        reason = "所需寶石同時低於安全可花額度與該獎勵的帳號價值上限。"
    elif gem_need <= spendable and gem_need <= value_cap * 1.35 and spending_style != "無課／只用免費資源":
        verdict = "邊際可追，只補這一檔"
        tone = "warning"
        reason = "成本略高於理想價值，但仍在你的消費風格與寶石安全線內。"
    else:
        verdict = "不追，拿免費進度就停"
        tone = "error"
        if gem_need > spendable:
            reason = f"補差額後會低於建議保留的 {reserve:,} 寶石安全線。"
        else:
            reason = "所需寶石高於這項獎勵對目前帳號的估算價值。"

    daily_needed = max(0, math.ceil((target_progress - current_progress) / max(days_remaining, 1)))
    return {
        "projected_free": projected_free,
        "gap": gap,
        "paid_actions": paid_actions,
        "gem_need": gem_need,
        "reserve": reserve,
        "spendable": spendable,
        "value_cap": value_cap,
        "verdict": verdict,
        "tone": tone,
        "reason": reason,
        "daily_needed": daily_needed,
    }


def diagnose_account(
    *,
    main_stage: str,
    chaos_stage: str,
    play_mode: str,
    divine_stage: str,
    weapon_stage: str = "雙生槍E4V4＋異界轉化",
) -> dict[str, Any]:
    main = {
        "維納托覺醒7以上": {
            "phase": "現在只做三件事",
            "title": "覺醒核心點維納托到8，神器核心點混沌到36",
            "reason": "一次只追一個數字。角色停在覺醒8、武器停在混沌36、異寵停在幽冥覺醒5。沒到這三個數字以前，不要改裝備，也不要練第二個主位。",
            "action_title": "覺醒核心全部拿去點維納托覺醒8",
            "stop": "維納托覺醒8",
            "action": "打開維納托，把覺醒核心一直點到畫面顯示覺醒8。還沒到8以前：不要點梅塔莉亞、不要點楊大師、不要開第二主位、不要拆塔洛莎覺醒4。",
            "avoid": "不要把覺醒核心分給其他角色，也不要為了同調拆掉塔洛莎覺醒4。",
            "switch": "維納托覺醒8點上後，剩下的覺醒核心才拿去點左協同梅塔莉亞覺醒1、右協同楊大師覺醒1。",
            "score": 100,
        },
        "維納托覺醒5＋塔洛莎覺醒4": {
            "phase": "現在只追一個數字",
            "title": "覺醒核心只點維納托，點到覺醒7停",
            "reason": "覺醒5只代表可以轉主位。現在唯一要做的是把維納托點到覺醒7。",
            "action_title": "覺醒核心全部拿去點維納托覺醒7",
            "stop": "維納托覺醒7",
            "action": "打開維納托，點到覺醒7就停。還沒到7以前：不要點別人、不要拆塔洛莎覺醒4。",
            "avoid": "不要在覺醒7以前改練第二主位，也不要把覺醒核心平均分給不上場角色。",
            "switch": "覺醒7點上後，下一檔才是維納托覺醒8。",
            "score": 90,
        },
        "塔洛莎覺醒5＋暴率70%": {
            "phase": "現在先存，不要轉",
            "title": "繼續用塔洛莎，先存滿維納托覺醒5",
            "reason": "半套轉職會變弱。存到能一次點完維納托覺醒5，並且塔洛莎還留得住覺醒4，再轉。",
            "action_title": "先存轉換包，不要半套轉職",
            "stop": "存滿維納托覺醒5",
            "action": "塔洛莎繼續上場。覺醒核心與通用碎片先囤著，等到「維納托能一次點完覺醒5、塔洛莎還留得住覺醒4」再轉。",
            "avoid": "不要做覺醒1～4維納托過渡，也不要平均分配通用角色資源。",
            "switch": "兩人門檻同時夠了再轉，不要先轉再補。",
            "score": 82,
        },
        "塔洛莎覺醒1～4／暴率未滿70%": {
            "phase": "現在只做塔洛莎",
            "title": "先把暴率補到70%，再點塔洛莎覺醒5",
            "reason": "現在還在第一個主位。分資源給維納托或伏爾坎，只會更慢成形。",
            "action_title": "先補暴率70%，再點塔洛莎覺醒5",
            "stop": "塔洛莎覺醒5",
            "action": "不含場內觸發的基礎暴率先到約70%，然後把塔洛莎點到覺醒5。這兩件事沒好以前不要談轉職。",
            "avoid": "先不投維納托，也不要為伏爾坎延後塔洛莎突破。",
            "switch": "塔洛莎覺醒5完成後，才開始存維納托轉換包。",
            "score": 58,
        },
        "都未達／不確定": {
            "phase": "先對三個數字",
            "title": "先看畫面數字，再花稀缺資源",
            "reason": "主位與暴率沒對上時，大額轉換很容易變弱。",
            "action_title": "先核對三個數字再花資源",
            "stop": "核對完三個數字",
            "action": "打開角色頁與屬性頁，記下塔洛莎覺醒、維納托覺醒、不含場內觸發的基礎暴率。對完再回來改左側選項。",
            "avoid": "不要因新角色推出就開自選箱或消耗通用突破資源。",
            "switch": "三個數字確認後重新診斷，再決定主位轉換。",
            "score": 35,
        },
    }[main_stage]

    chaos = {
        "混沌之力27以上": {
            "label": "現在點武器",
            "title": "神器核心全部拿去堆混沌36",
            "detail": "打開混沌融合之力，用神器核心點到36（能量雙刀）就停。還沒到36以前：項鍊繼續穿破壞者徽記，不要換成審判項鍊，也不要改腰帶、手套。",
            "next": "混沌36",
            "stop": "混沌36",
            "score": 6,
        },
        "混沌之力18～26": {
            "label": "現在點武器",
            "title": "神器核心全部拿去堆混沌27",
            "detail": "打開混沌融合之力，點到27（切月鐮刀）就停。還沒到27以前：項鍊繼續穿破壞者徽記，不要改腰帶。",
            "next": "混沌27",
            "stop": "混沌27",
            "score": 3,
        },
        "混沌之力9～17": {
            "label": "現在點武器",
            "title": "神器核心全部拿去堆混沌18",
            "detail": "打開混沌融合之力，點到18（神罰之斧）就停。還沒到18以前：不要換腰帶項鍊，也不要回頭用苦無。",
            "next": "混沌18",
            "stop": "混沌18",
            "score": 0,
        },
        "混沌之力未滿9／不確定": {
            "label": "現在點武器",
            "title": "神器核心先把混沌之力補到9",
            "detail": "打開混沌融合之力，先點到9（混沌之風）就停。沒到9以前，不要照抄切月鐮刀或永恆4配置。",
            "next": "混沌9",
            "stop": "混沌9",
            "score": -10,
        },
    }
    chaos["混沌之力18以上"] = chaos["混沌之力18～26"]
    chaos = chaos[chaos_stage]

    weapon_options = {
        "雙生槍E4V4＋異界轉化": {
            "title": "神器核心拿去堆下一個混沌檔",
            "detail": "雙生槍已經夠用。神器核心不要再點苦無，全部拿去把混沌之力點到下一檔。",
            "stop": "下一檔混沌",
            "score": 0,
        },
        "雙生槍E3V2以上未滿E4V4": {
            "title": "神器核心先把雙生槍補到永恆4＋虛空4",
            "detail": "打開雙生槍，點到永恆4與虛空4就停，再開異界轉化1。還沒到以前：不要先堆混沌36，也不要換其他主武器。",
            "stop": "雙生槍E4V4",
            "score": -4,
        },
        "雙生槍E1V2骨架": {
            "title": "神器核心先把雙生槍補到永恆3＋虛空2",
            "detail": "打開雙生槍，點到永恆3與虛空2就停。還沒到以前不要換苦無。",
            "stop": "雙生槍E3V2",
            "score": -8,
        },
        "苦無／虛空／未達雙生槍": {
            "title": "先做出雙生槍，當天點永恆1",
            "detail": "苦無與虛空之力現在不要再當主武器。做出雙生槍的當天，用1個神器核心點永恆神鑄1。",
            "stop": "雙生槍＋永恆1",
            "score": -15,
        },
    }
    weapon = weapon_options[weapon_stage]

    divine_options = {
        "哪吒R4＋伏爾坎R4支援鏈": {
            "title": "哪吒與伏爾坎先維持，不要改主位",
            "detail": "這兩人只當神火支援。覺醒核心先給維納托，不要拿去把他們改成主位。",
            "stop": "先不動神火",
            "score": 0,
        },
        "只有哪吒或伏爾坎": {
            "title": "伏爾坎先不要點",
            "detail": "維納托覺醒7以前，覺醒核心不要分給伏爾坎。主位過關後再補伏爾坎覺醒1。",
            "stop": "先不動伏爾坎",
            "score": -5,
        },
        "都沒有／不確定": {
            "title": "神火這條先跳過",
            "detail": "現在的覺醒核心給主位。哪吒、伏爾坎都還沒有就先不要追。",
            "stop": "先跳過神火",
            "score": -10,
        },
    }
    # Preserve older saved selections while moving the visible UI to current R4 support checks.
    divine_options["哪吒覺醒2＋伏爾坎覺醒1"] = divine_options["哪吒R4＋伏爾坎R4支援鏈"]
    divine_options["只有哪吒"] = divine_options["只有哪吒或伏爾坎"]
    divine = divine_options[divine_stage]
    late_support = {
        "title": "連攜槽只給現在這三人",
        "detail": "多出來的連攜槽依序放：塔洛莎、梅塔莉亞、楊大師。不要放不上場的角色。",
        "stop": "三人連攜就好",
    }
    late_systems = {
        "title": "異世核心全部拿去點幽冥之魂覺醒5",
        "detail": "打開異寵幽冥之魂，點到覺醒5就停。還沒到覺醒5以前：晶片不要先給雙生無人機，腰帶、手套、項鍊先別動。",
        "stop": "幽冥之魂覺醒5",
    }
    loadout = chaos if weapon_stage == "雙生槍E4V4＋異界轉化" else weapon
    third = (
        late_systems
        if main_stage == "維納托覺醒7以上"
        and divine_stage in ("哪吒R4＋伏爾坎R4支援鏈", "哪吒覺醒2＋伏爾坎覺醒1")
        and weapon_stage == "雙生槍E4V4＋異界轉化"
        else late_support
        if main_stage == "維納托覺醒7以上"
        and divine_stage in ("哪吒R4＋伏爾坎R4支援鏈", "哪吒覺醒2＋伏爾坎覺醒1")
        else divine
    )

    mode = {
        "短場首領": {
            "build": "短時首領爆發天花板",
            "instruction": "雙生槍已是後期主武器；進化交給 E4 與異界轉化，技能格優先雙生無人機與冷卻，不要再練苦無。",
        },
        "長場首領": {
            "build": "長戰疊層傷害極限",
            "instruction": "讓混沌27、共鳴、燃燒／虛弱／裂傷完整疊滿；項鍊繼續穿破壞者徽記，等混沌36與審判項鍊雙生階成形再 A/B。",
        },
        "區域行動": {
            "build": "新版區域行動路線最優解",
            "instruction": "2026/08/27 新版不帶入局外裝備；先手操小關取得局內 Buff，再以無人機索敵與生存被動挑戰區域首領。",
        },
    }[play_mode]

    gear_by_mode = {
        "短場首領": [
            {"slot": "武器", "wear": "雙生槍 永恆4＋虛空4", "spend": "神器核心堆混沌36", "freeze": "不要換苦無"},
            {"slot": "項鍊", "wear": "破壞者徽記（神鑄3）", "spend": "先不動", "freeze": "繼續穿這件。審判項鍊還沒雙生階、暴率沒堆滿以前不要換，也不要為了做它花神器核心"},
            {"slot": "手套", "wear": "月痕護腕（雙生階）", "spend": "先不動", "freeze": "暴率沒到70%才暫留虛空手套，不要當終點"},
            {"slot": "腰帶", "wear": "星塵腰帶（雙生階）", "spend": "幽冥覺醒5之後才點永恆3", "freeze": "現在不要換扭曲腰帶"},
            {"slot": "鞋子", "wear": "冰川戰靴（雙生階）", "spend": "排最後：永恆1／虛空2／混沌1", "freeze": "不要為了鞋子拆混沌36"},
            {"slot": "衣服", "wear": "永虛戰甲（雙生階、永恆3起）", "spend": "腰帶永恆3之後再補", "freeze": "短場不要穿亡者風衣"},
        ],
        "長場首領": [
            {"slot": "武器", "wear": "雙生槍 永恆4＋虛空4＋異界轉化", "spend": "神器核心堆混沌36／45", "freeze": "不要換苦無"},
            {"slot": "項鍊", "wear": "破壞者徽記（神鑄3）", "spend": "混沌36之後才跟審判項鍊做 A/B", "freeze": "暴率沒堆滿、審判項鍊沒雙生階以前，繼續穿破壞者，不要先換"},
            {"slot": "手套", "wear": "月痕護腕（雙生階、永恆1／虛空2）", "spend": "先不動", "freeze": "不要退回神鑄3虛空手套"},
            {"slot": "腰帶", "wear": "星塵腰帶（雙生階、永恆3）", "spend": "幽冥覺醒5與紅3收藏之後，才跟扭曲腰帶做 A/B", "freeze": "沒到永恆3以前不要換腰帶"},
            {"slot": "鞋子", "wear": "冰川戰靴（雙生階）", "spend": "排最後：永恆1／虛空2／混沌1", "freeze": "不要為了鞋子拆混沌36"},
            {"slot": "衣服", "wear": "永虛戰甲（雙生階、永恆3／虛空2／混沌2）", "spend": "腰帶永恆3之後再補", "freeze": "不要穿短場過渡裝"},
        ],
        "區域行動": [
            {"slot": "武器", "wear": "雙生槍 E4V4＋異界轉化", "spend": "神器核心仍堆混沌36", "freeze": "特殊詞條關才切虛空之力"},
            {"slot": "項鍊", "wear": "破壞者徽記（神鑄3）", "spend": "先不動", "freeze": "新版區域行動不帶入局外裝備；舊章節也繼續穿破壞者，不要先換成審判項鍊"},
            {"slot": "手套", "wear": "月痕護腕（雙生階）", "spend": "先不動", "freeze": "暴率沒到70%才暫留虛空手套"},
            {"slot": "腰帶", "wear": "星塵腰帶（雙生階、永恆3／虛空2）", "spend": "幽冥覺醒5之後才點", "freeze": "現在不要換扭曲腰帶"},
            {"slot": "鞋子", "wear": "冰川戰靴（雙生階）", "spend": "排最後", "freeze": "不要為了鞋子拆混沌36"},
            {"slot": "衣服", "wear": "新版區域行動不帶入局外裝備", "spend": "舊章節／詞條關才切亡者風衣神鑄3", "freeze": "不要套 8/27 以前的局外裝備攻略"},
        ],
    }
    gear = gear_by_mode[play_mode]
    if chaos["next"] != "混沌36":
        for item in gear:
            if item["slot"] == "項鍊":
                item["spend"] = "先不動"
                item["freeze"] = f"繼續穿破壞者徽記。{chaos['next']}以前不要換成審判項鍊"
            elif item["slot"] in ("手套", "腰帶"):
                item["spend"] = "先不動"
                item["freeze"] = f"{chaos['next']}以前不要改這格"

    collectibles = [
        {"spend": "自選箱／收藏之心", "name": "星際躍遷矩陣圖紙", "stop": "紅3", "why": "無人機主力。紅3還加暴擊率10%。缺這件就用自選箱補它。"},
        {"spend": "自選箱／收藏之心", "name": "水動推力腳蹼", "stop": "紅3", "why": "史詩比較便宜，一樣補無人機與暴擊率。圖紙紅3之後立刻點它。"},
        {"spend": "自選箱／收藏之心", "name": "暗物質傀儡", "stop": "黃5", "why": "雙生無人機長期核心。前兩件紅3之後才點它；黃5以前不要追紅星。"},
    ]

    readiness = max(15, min(100, main["score"] + chaos["score"] + divine["score"] + weapon["score"]))
    return {
        "phase": main["phase"],
        "title": main["title"],
        "reason": main["reason"],
        "readiness": readiness,
        "build": mode["build"],
        "mode_instruction": mode["instruction"],
        "priorities": [
            {"label": "現在點角色", "title": main["action_title"], "detail": main["action"], "stop": main["stop"]},
            {"label": "現在點武器", "title": loadout["title"], "detail": loadout["detail"], "stop": loadout.get("stop", chaos["next"])},
            {"label": "現在點異寵", "title": third["title"], "detail": third["detail"], "stop": third.get("stop", "先不動")},
        ],
        "avoid": main["avoid"],
        "switch_condition": main["switch"],
        "next_breakpoint": chaos["next"],
        "gear": gear,
        "collectibles": collectibles,
        "collectible_freeze": "追光者、混亂之劍、平均升星、先開空欄位硬塞，全部先不要。",
    }


OPTIMIZATION_STRATEGIES: list[dict[str, Any]] = [
    {
        "id": "event_roi",
        "name": "活動免費線＋精準補檔",
        "label": "活動 ROI",
        "base": 72,
        "goals": ("活動獎勵效率",),
        "modes": ("綜合養成", "短場首領", "長場首領", "區域行動"),
        "stages": ("尚未紅裝成套", "紅裝成套、神器核心不足", "主要裝備斷點已完成", "接近滿配"),
        "horizons": (7, 30),
        "risk": 1,
        "min_minutes": 15,
        "resource_need": {},
        "impact": 82,
        "efficiency": 96,
        "certainty": 88,
        "summary": "先吃滿登入、任務與免費票，最後 24 小時才計算是否補到下一個高價值里程碑。",
        "steps": ("把剩餘免費進度投影到活動結束", "只選一個能立即跨過的帳號斷點", "補到目標後立即停手"),
        "stop": "補鑽後低於寶石安全線，或成本高於獎勵對帳號的價值上限時停止。",
        "switch": "活動頁顯示免費可達標，或下一檔獎勵價值突然下降時，切回純免費路線。",
    },
    {
        "id": "survivor_breakpoint",
        "name": "主位覺醒單點突破",
        "label": "角色主位",
        "base": 68,
        "goals": ("首領傷害上限", "長期帳號成長"),
        "modes": ("短場首領", "長場首領", "綜合養成"),
        "stages": ("尚未紅裝成套", "紅裝成套、神器核心不足"),
        "horizons": (30, 90),
        "risk": 1,
        "min_minutes": 20,
        "resource_need": {"awakening_cores": 6},
        "impact": 91,
        "efficiency": 78,
        "certainty": 76,
        "summary": "通用角色資源只服務一個完整主位門檻，不做覺醒一半的過渡角色。",
        "steps": ("先確認基礎暴擊率與主位門檻", "存到可一次完成目標覺醒", "保留必要協同角色後再轉主位"),
        "stop": "無法同時保留協同門檻，或只能完成低覺醒過渡時不投入。",
        "switch": "主位門檻完成後，把新增資源轉向神器核心與模式裝備。",
    },
    {
        "id": "relic_breakpoint",
        "name": "雙生之槍與神器核心斷點",
        "label": "核心配置",
        "base": 76,
        "goals": ("首領傷害上限", "長期帳號成長"),
        "modes": ("短場首領", "長場首領", "綜合養成"),
        "stages": ("紅裝成套、神器核心不足", "主要裝備斷點已完成", "接近滿配"),
        "horizons": (30, 90),
        "risk": 1,
        "min_minutes": 20,
        "resource_need": {"relic_cores": 4},
        "impact": 96,
        "efficiency": 90,
        "certainty": 83,
        "summary": "核心不要平均灑在六個欄位；先完成武器與主模式最有感的完整節點。",
        "steps": ("先鎖定雙生之槍與主模式裝備", "比較下一個完整 E／V／C 節點", "只移動能立即提升實戰的核心"),
        "stop": "核心數不足完整節點，或移動後會拆掉現役關鍵效果時先保留。",
        "switch": "主要武器與裝備斷點完成後，再比較異世寵物與科技諧振的邊際收益。",
    },
    {
        "id": "xeno_pet",
        "name": "異世寵物覺醒與共鳴",
        "label": "異寵乘區",
        "base": 71,
        "goals": ("首領傷害上限", "長期帳號成長"),
        "modes": ("短場首領", "長場首領", "綜合養成"),
        "stages": ("主要裝備斷點已完成", "接近滿配"),
        "horizons": (30, 90),
        "risk": 2,
        "min_minutes": 20,
        "resource_need": {"xeno_cores": 10},
        "impact": 94,
        "efficiency": 84,
        "certainty": 74,
        "summary": "裝備骨架成熟後，把異世核心集中到能改變主人乘區的完整覺醒門檻。",
        "steps": ("確認主戰寵物與主人增傷", "先完成一隻主寵的完整覺醒節點", "助戰技能只服務主寵與主模式"),
        "stop": "核心不足完整覺醒門檻，或只能提高寵物面板而無法提高主人輸出時停止。",
        "switch": "主寵門檻完成後，再比較共鳴晶片與下一個神器節點。",
    },
    {
        "id": "tech_resonance",
        "name": "科技配件諧振／雙生突破",
        "label": "科技乘區",
        "base": 70,
        "goals": ("首領傷害上限", "長期帳號成長"),
        "modes": ("短場首領", "長場首領", "綜合養成"),
        "stages": ("主要裝備斷點已完成", "接近滿配"),
        "horizons": (30, 90),
        "risk": 2,
        "min_minutes": 20,
        "resource_need": {"resonance_chips": 8},
        "impact": 89,
        "efficiency": 82,
        "certainty": 76,
        "summary": "用主力技能的下一個諧振／雙生節點衡量收益，不把晶片平均分散。",
        "steps": ("鎖定主力技能與模式", "計算下一級需要的晶片與配件", "一次跨過完整效果再停"),
        "stop": "下一級只增加面板、沒有改變主力技能乘區時，先轉投其他系統。",
        "switch": "主力配件跨過節點後，重新比較異寵與收藏套裝。",
    },
    {
        "id": "zone_stability",
        "name": "區域行動零失誤骨架",
        "label": "通關穩定",
        "base": 74,
        "goals": ("區域行動穩定", "長期帳號成長"),
        "modes": ("區域行動",),
        "stages": ("尚未紅裝成套", "紅裝成套、神器核心不足", "主要裝備斷點已完成", "接近滿配"),
        "horizons": (7, 30),
        "risk": 0,
        "min_minutes": 25,
        "resource_need": {},
        "impact": 86,
        "efficiency": 91,
        "certainty": 90,
        "summary": "依當期詞條切換生存與控制，不用首領最高面板硬闖所有區域。",
        "steps": ("先讀限制與失敗原因", "用生存骨架拿首次通關", "通關後再逐步換回輸出"),
        "stop": "連續兩次失敗原因相同時停止硬闖，改一個變數後再測。",
        "switch": "穩定通關後，把額外時間轉回活動免費線與長期養成。",
    },
    {
        "id": "collection_breakpoint",
        "name": "收藏套裝最近有效斷點",
        "label": "收藏補洞",
        "base": 64,
        "goals": ("長期帳號成長",),
        "modes": ("綜合養成", "短場首領", "長場首領", "區域行動"),
        "stages": ("紅裝成套、神器核心不足", "主要裝備斷點已完成", "接近滿配"),
        "horizons": (30, 90),
        "risk": 1,
        "min_minutes": 15,
        "resource_need": {},
        "impact": 76,
        "efficiency": 86,
        "certainty": 80,
        "summary": "自選箱只補差一件或差一星的有效套裝與主力技能，不依稀有度平均升星。",
        "steps": ("列出所有未啟動的下一效果", "比較距離與乘區收益", "只開能立刻跨線的自選箱"),
        "stop": "沒有任何可立即啟動的效果時保留自選箱。",
        "switch": "最近套裝啟動後，回到神器、異寵與科技三者的邊際比較。",
    },
    {
        "id": "ab_test",
        "name": "固定場景 A/B 重算",
        "label": "實戰驗證",
        "base": 69,
        "goals": ("首領傷害上限", "區域行動穩定", "長期帳號成長"),
        "modes": ("短場首領", "長場首領", "區域行動"),
        "stages": ("主要裝備斷點已完成", "接近滿配"),
        "horizons": (7, 30),
        "risk": 0,
        "min_minutes": 25,
        "resource_need": {},
        "impact": 84,
        "efficiency": 94,
        "certainty": 95,
        "summary": "高端帳號不要再照固定順位；固定首領、時間與技能，只改一項並記錄結果。",
        "steps": ("建立現役配置基準", "每輪只改一個角色／裝備／配件", "至少三輪取中位數再決定"),
        "stop": "測試條件不同、技能進化時間差太大，或樣本不足三輪時不下結論。",
        "switch": "新配置穩定勝出且資源成本可逆時，再正式轉換。",
    },
    {
        "id": "reserve",
        "name": "屯資源等待完整斷點",
        "label": "保留選擇權",
        "base": 60,
        "goals": ("不確定，自動判斷", "長期帳號成長"),
        "modes": ("綜合養成", "短場首領", "長場首領", "區域行動"),
        "stages": ("尚未紅裝成套", "紅裝成套、神器核心不足", "主要裝備斷點已完成", "接近滿配"),
        "horizons": (7, 30, 90),
        "risk": 0,
        "min_minutes": 10,
        "resource_need": {},
        "impact": 58,
        "efficiency": 98,
        "certainty": 94,
        "summary": "目前資源無法跨過完整節點時，保留核心、自選箱與寶石比做半套升級更有效。",
        "steps": ("列出下一個完整斷點", "只拿免費與高效率常駐資源", "達門檻後一次投入"),
        "stop": "一旦可完成高分策略的完整門檻，就停止屯資源並重新最佳化。",
        "switch": "任一稀缺資源達到推薦策略需求，或版本推出新系統時重算。",
    },
]


DAILY_TASKS: list[dict[str, Any]] = [
    {"name": "登入、郵件與活動免費領取", "minutes": 4, "base": 100, "goals": (), "modes": (), "why": "幾乎零風險取得限時資源，永遠先做。"},
    {"name": "每日任務與快速巡邏", "minutes": 8, "base": 96, "goals": ("長期帳號成長",), "modes": ("綜合養成",), "why": "穩定轉換體力、經驗與鑰匙，不需要額外寶石。"},
    {"name": "體力消耗與主線巡邏", "minutes": 5, "base": 82, "goals": ("長期帳號成長",), "modes": ("綜合養成",), "why": "避免體力溢出並提高長期被動收益。"},
    {"name": "當期活動免費任務／免費票", "minutes": 10, "base": 88, "goals": ("活動獎勵效率",), "modes": (), "why": "先拿免費進度，保留最後一天的補鑽選擇權。"},
    {"name": "常規挑戰與週期核心來源", "minutes": 12, "base": 84, "goals": ("長期帳號成長",), "modes": ("綜合養成",), "why": "稀缺核心來源應高於低價排名與重複刷分。"},
    {"name": "末世反響／公會首領有效場次", "minutes": 12, "base": 82, "goals": ("首領傷害上限",), "modes": ("短場首領", "長場首領"), "why": "固定場景同時取得獎勵並驗證配裝。"},
    {"name": "區域行動／高價值首次通關", "minutes": 15, "base": 82, "goals": ("區域行動穩定",), "modes": ("區域行動",), "why": "首次通關價值通常高於已通關內容的重複刷取。"},
    {"name": "主線、試煉與一次性進度", "minutes": 18, "base": 72, "goals": ("長期帳號成長",), "modes": ("綜合養成", "區域行動"), "why": "有餘裕時優先解鎖永久收益與後續資源。"},
    {"name": "固定場景三輪 A/B 實測", "minutes": 24, "base": 68, "goals": ("首領傷害上限", "區域行動穩定"), "modes": ("短場首領", "長場首領", "區域行動"), "why": "高端帳號用實測避免把稀缺核心投到面板幻覺。"},
]


def _resource_label(key: str) -> str:
    return {
        "relic_cores": "神器核心",
        "resonance_chips": "諧振晶片",
        "xeno_cores": "異世核心",
        "awakening_cores": "覺醒核心",
    }[key]


def _optimize_daily_schedule(*, minutes: int, goal: str, play_mode: str) -> dict[str, Any]:
    budget = max(4, min(180, int(minutes)))
    weighted: list[dict[str, Any]] = []
    for task in DAILY_TASKS:
        utility = int(task["base"])
        if goal in task["goals"]:
            utility += 30
        elif not task["goals"]:
            utility += 10
        if play_mode in task["modes"]:
            utility += 20
        elif not task["modes"]:
            utility += 5
        item = dict(task)
        item["utility"] = utility
        item["density"] = utility / max(1, int(task["minutes"]))
        weighted.append(item)

    states: list[tuple[int, list[int]]] = [(0, []) for _ in range(budget + 1)]
    for index, task in enumerate(weighted):
        duration = int(task["minutes"])
        for current in range(budget, duration - 1, -1):
            previous_score, previous_items = states[current - duration]
            candidate = previous_score + int(task["utility"])
            if candidate > states[current][0]:
                states[current] = (candidate, [*previous_items, index])

    best_minutes = max(range(budget + 1), key=lambda value: states[value][0])
    chosen_indices = states[best_minutes][1]
    selected = sorted(
        (weighted[index] for index in chosen_indices),
        key=lambda item: (-item["density"], item["minutes"]),
    )
    omitted = sorted(
        (item for index, item in enumerate(weighted) if index not in chosen_indices),
        key=lambda item: (-item["utility"], item["minutes"]),
    )
    return {
        "budget": budget,
        "minutes_used": sum(int(item["minutes"]) for item in selected),
        "tasks": selected,
        "next_if_more_time": omitted[:2],
    }


def optimize_player_plan(
    *,
    goal: str,
    account_stage: str,
    play_mode: str,
    spending_style: str,
    risk_style: str,
    horizon_days: int,
    gems: int,
    relic_cores: int,
    resonance_chips: int,
    xeno_cores: int,
    awakening_cores: int,
    daily_minutes: int,
) -> dict[str, Any]:
    """Rank account progression paths and build a time-constrained daily plan.

    This is intentionally a transparent rule optimizer rather than a hidden DPS
    simulator. It favors complete breakpoints, reversible choices, and explicit
    resource safety lines.
    """

    reserve = {"無課／只用免費資源": 30000, "微課／可小補寶石": 15000, "課金／只看效率": 5000}.get(spending_style, 20000)
    spendable_gems = max(0, int(gems) - reserve)
    resources = {
        "relic_cores": max(0, int(relic_cores)),
        "resonance_chips": max(0, int(resonance_chips)),
        "xeno_cores": max(0, int(xeno_cores)),
        "awakening_cores": max(0, int(awakening_cores)),
    }
    horizon = min((7, 30, 90), key=lambda value: abs(value - int(horizon_days)))
    ranked: list[dict[str, Any]] = []

    for strategy in OPTIMIZATION_STRATEGIES:
        reasons: list[str] = []

        if goal in strategy["goals"]:
            goal_fit = 96
            reasons.append("直接符合你的核心目標")
        elif goal == "不確定，自動判斷":
            goal_fit = 66
        else:
            goal_fit = 28

        if play_mode in strategy["modes"]:
            mode_fit = 94
            reasons.append("與主要模式一致")
        elif "綜合養成" in strategy["modes"]:
            mode_fit = 64
        else:
            mode_fit = 30

        if account_stage in strategy["stages"]:
            stage_fit = 94
            reasons.append("符合目前帳號階段")
        else:
            stage_fit = 28

        if horizon in strategy["horizons"]:
            horizon_fit = 92
        else:
            horizon_fit = 48

        if daily_minutes >= int(strategy["min_minutes"]):
            time_fit = 94
        else:
            shortage = int(strategy["min_minutes"]) - int(daily_minutes)
            time_fit = max(25, 90 - shortage * 4)

        risk = int(strategy["risk"])
        if risk_style == "穩定優先":
            risk_fit = max(25, 98 - risk * 28)
        elif risk_style == "追求上限":
            risk_fit = min(98, 58 + risk * 20)
        else:
            risk_fit = max(55, 92 - abs(risk - 1) * 20)

        gaps: list[str] = []
        resource_fits: list[int] = []
        for key, need in strategy["resource_need"].items():
            owned = resources[key]
            if owned >= int(need):
                resource_fits.append(96)
                reasons.append(f"{_resource_label(key)}已達可執行量")
            else:
                gap = int(need) - owned
                resource_fits.append(max(8, round(72 * owned / max(1, int(need)))))
                gaps.append(f"{_resource_label(key)}還差 {gap}")
        resource_fit = round(sum(resource_fits) / len(resource_fits)) if resource_fits else 92

        if int(gems) < reserve:
            if strategy["id"] in ("reserve", "event_roi", "ab_test", "zone_stability"):
                resource_fit = min(98, resource_fit + 4)
            else:
                resource_fit = min(resource_fit, 18)
                gaps.append(f"寶石低於 {reserve:,} 安全線")

        stage_bonus = 0
        if account_stage == "尚未紅裝成套":
            stage_bonus = 6 if strategy["id"] == "survivor_breakpoint" else 0
            stage_bonus -= 6 if strategy["id"] in ("xeno_pet", "tech_resonance") else 0
        elif account_stage == "紅裝成套、神器核心不足":
            stage_bonus = 7 if strategy["id"] == "relic_breakpoint" else 0
        elif account_stage == "主要裝備斷點已完成":
            stage_bonus = 5 if strategy["id"] in ("xeno_pet", "tech_resonance", "collection_breakpoint") else 0
        elif account_stage == "接近滿配":
            stage_bonus = 8 if strategy["id"] == "ab_test" else 0

        objective_bonus = 0
        if goal == "活動獎勵效率" and strategy["id"] == "event_roi":
            objective_bonus = 5
        if goal == "區域行動穩定" and strategy["id"] == "zone_stability":
            objective_bonus = 5
        if not gaps:
            reasons.append("目前資源可直接執行")

        score = (
            int(strategy["impact"]) * 0.22
            + goal_fit * 0.20
            + mode_fit * 0.13
            + stage_fit * 0.15
            + resource_fit * 0.15
            + horizon_fit * 0.05
            + time_fit * 0.05
            + risk_fit * 0.05
            + stage_bonus
            + objective_bonus
        )
        final_score = max(0, min(97, round(score)))
        item = dict(strategy)
        item.update(
            {
                "score": final_score,
                "fit": max(0, min(100, round((final_score + int(strategy["certainty"])) / 2))),
                "reasons": reasons[:3],
                "gaps": gaps,
                "feasible": not gaps,
            }
        )
        ranked.append(item)

    ranked.sort(key=lambda item: (item["score"], item["certainty"], item["efficiency"]), reverse=True)
    top = ranked[0]
    schedule = _optimize_daily_schedule(minutes=daily_minutes, goal=goal, play_mode=play_mode)

    confidence = 68
    confidence += 6 if goal != "不確定，自動判斷" else 0
    confidence += 5 if play_mode != "綜合養成" else 0
    confidence += 4 if any(resources.values()) else 0
    confidence += 3 if int(gems) > 0 else 0
    if account_stage == "接近滿配":
        confidence -= 8
    confidence = max(55, min(86, confidence))

    avoided = [item for item in ranked if item["score"] < 55][:3]
    mode_protocols = {
        "綜合養成": {
            "title": "綜合養成：先做不可溢出的免費收益",
            "opening": "登入、郵件、免費票與體力先清零，避免限時與自然回復資源溢出。",
            "mid": "再做能提供稀缺核心或永久解鎖的一次性內容。",
            "finish": "低價排名、重複刷分與外觀追逐放到所有高價值任務之後。",
            "measure": "每週只看三個數：稀缺核心淨增加、下一斷點距離、寶石安全庫存。",
        },
        "短場首領": {
            "title": "短場首領：進化時間本身就是傷害",
            "opening": "優先雙生槍、無人機與冷卻；開局技能格不要塞入太多低優先技能。",
            "mid": "記錄無人機與主武器完成進化的時間，不用滿層理論 DPS 代替短場實戰。",
            "finish": "固定首領與技能選擇，至少三輪取中位數後才移動神器核心。",
            "measure": "比較前 60 秒傷害、首次進化秒數與整場中位數，不只看單次最高值。",
        },
        "長場首領": {
            "title": "長場首領：完整疊層與異常覆蓋率優先",
            "opening": "先確認燃燒、虛弱、冰緩或裂傷有穩定觸發來源，再計算對應增傷。",
            "mid": "讓混沌、共鳴與寵物乘區進入穩定區間，不把短場進化速度權重照搬。",
            "finish": "固定戰鬥階段與減益條件做 A/B，避免遠征階段和對戰階段混算。",
            "measure": "比較穩定段 DPS、異常覆蓋率、同步損失與三輪中位數。",
        },
        "區域行動": {
            "title": "新版區域行動：局內路線比局外面板重要",
            "opening": "先手操 2～3 個高價值小關拿 Buff；不要把時間平均用在所有支線。",
            "mid": "無人機先升到自動索敵節點，再補雷電、火箭、哨箭與足球。",
            "finish": "優先挑戰區域首領取得下方獎勵；清潔戰可跳過，若打則結束時污染必須為 0。",
            "measure": "記錄失敗原因、剩餘血量與路線 Buff；連敗兩次只更改一個變數。",
        },
    }
    return {
        "best": top,
        "ranked": ranked[:5],
        "alternatives": ranked[1:3],
        "confidence": confidence,
        "reserve": reserve,
        "spendable_gems": spendable_gems,
        "schedule": schedule,
        "avoid_now": avoided,
        "mode_protocol": mode_protocols[play_mode],
        "recalculate_when": [
            top["switch"],
            "任何稀缺核心、自選箱或角色門檻改變時重新計算。",
            "版本更新、活動獎勵表或主要遊玩模式改變時重新計算。",
        ],
        "method": "目標適配＋模式適配＋帳號階段＋資源可行性＋時間限制＋風險偏好",
    }
