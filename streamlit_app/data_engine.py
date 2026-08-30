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
                    ("自動連打技巧", "長按 Auto 可自動抽取技能，適合跑完整張圓盤。"),
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
                    ("T0 必換核心", "紅色收藏品自選箱、萬能 SP 碎片，整體戰力提升最高。"),
                    ("T1 極推兌換", "高級收藏之心。"),
                    ("T2 選擇兌換", "特工寵物餅乾；正在主力培養異世寵物的玩家再換。"),
                    ("避雷指南", "配件選擇箱沒有折扣時不要換，活動點數應鎖定高階稀有物資。"),
                ],
            },
        ],
        "highlights": [
            ("免費票券", "約 900 張；盤面麥克風返還率約 44%～47%，實質進度約放大 1.5 倍。"),
            ("推薦進度", "累計 980：可拿諧振晶片與傳奇收藏品自選寶箱，無課優先停在這裡。"),
            ("開箱策略", "先開 200～300 箱，最後一天依差額微調；不要為任務盲目開滿 600 箱。"),
            ("商店必換", "紅色收藏品自選箱 ＞ 萬能 SP 碎片 ＞ 高級收藏之心。"),
        ],
        "steps": ["先拿完登入、每日任務與免費麥克風", "先開 200～300 箱，再看最後一天差額", "只補到累計 980，達標後停手", "商店依紅色收藏、萬能 SP 碎片、高級收藏之心順序兌換"],
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
) -> dict[str, Any]:
    main = {
        "維納托覺醒5＋塔洛莎覺醒4": {
            "phase": "真終局主位期",
            "title": "維納托主位，塔洛莎保留協同",
            "reason": "角色組合已跨過主位轉換門檻，維納托現在才有條件穩定超過塔洛莎。",
            "action": "維納托由覺醒5繼續升到7；塔洛莎維持覺醒4以上，不要拆掉協同。",
            "avoid": "不要分解塔洛莎，也不要為短期面板把她降出協同門檻。",
            "switch": "已達主位轉換條件，後續集中強化維納托與終局裝備。",
            "score": 95,
        },
        "塔洛莎覺醒5＋暴率70%": {
            "phase": "高端成熟期",
            "title": "塔洛莎繼續主位，暫時不要轉維納托",
            "reason": "低覺醒維納托不會自動更強；現在轉換會同時失去成熟主位與高階協同。",
            "action": "存到能一次完成維納托覺醒5，並同時保留塔洛莎覺醒4，再一次轉換。",
            "avoid": "不要做覺醒1～4維納托過渡，也不要平均分配通用角色資源。",
            "switch": "維納托覺醒5＋塔洛莎覺醒4同時成立後再轉主位。",
            "score": 82,
        },
        "塔洛莎覺醒1～4／暴率未滿70%": {
            "phase": "主位養成期",
            "title": "塔洛莎主位，第一目標是覺醒5",
            "reason": "目前還沒跨過塔洛莎的主要爆發門檻，分資源給其他主位只會延後成形。",
            "action": "先把基礎暴率補到約70%，接著把塔洛莎推到覺醒5。",
            "avoid": "先不投維納托，也不要為伏爾坎延後塔洛莎突破。",
            "switch": "先完成塔洛莎覺醒5；維納托轉換是更後面的階段。",
            "score": 58,
        },
        "都未達／不確定": {
            "phase": "資料確認期",
            "title": "維持現有最強主位，資源先不要分散",
            "reason": "主位與暴率資料不完整時，任何大額轉換都可能讓帳號實際變弱。",
            "action": "確認塔洛莎、維納托突破，以及不含場內觸發的基礎暴率。",
            "avoid": "不要因新角色推出就開自選箱或消耗通用突破資源。",
            "switch": "資料確認後重新診斷，再決定主位轉換。",
            "score": 35,
        },
    }[main_stage]

    chaos = {
        "混沌之力18以上": {
            "label": "高階重算",
            "title": "重新比較項鍊與腰帶",
            "detail": "混沌之力18已達重算點；長場可開始比較雙生階與神鑄3單系裝備。",
            "next": "固定首領、固定時間做 A/B 實測",
            "score": 5,
        },
        "混沌之力9～17": {
            "label": "下一斷點",
            "title": "混沌之力推到18",
            "detail": "目前已能使用終局骨架；在18以前，不要頻繁更換腰帶與項鍊。",
            "next": "混沌之力18",
            "score": 0,
        },
        "混沌之力未滿9／不確定": {
            "label": "第一斷點",
            "title": "混沌之力先補到9",
            "detail": "未滿9時先完成基本門檻，不要直接照抄混沌之力18的長場配置。",
            "next": "混沌之力9",
            "score": -10,
        },
    }[chaos_stage]

    divine = {
        "哪吒覺醒2＋伏爾坎覺醒1": {
            "title": "維持完整神火支援鏈",
            "detail": "哪吒放協同被動並獲得伏爾坎加成；兩者都不改成主位。",
            "score": 0,
        },
        "只有哪吒": {
            "title": "先保留哪吒，再補伏爾坎",
            "detail": "等主位與混沌之力門檻完成後，再把伏爾坎補到覺醒1。",
            "score": -5,
        },
        "都沒有／不確定": {
            "title": "暫時跳過神火投資",
            "detail": "通用資源先給主位、雙生之槍與裝備門檻，伏爾坎不是現在的優先項。",
            "score": -10,
        },
    }[divine_stage]

    mode = {
        "短場首領": {
            "build": "短時首領爆發天花板",
            "instruction": "先讓雙生之槍進化，技能優先無人機與冷卻，追求最短時間爆發。",
        },
        "長場首領": {
            "build": "長戰疊層傷害極限",
            "instruction": "讓混沌之力、共鳴、燃燒與虛弱完整疊滿，不用短場配裝硬套。",
        },
        "區域行動": {
            "build": "區域行動零失誤配置",
            "instruction": "依詞條切換亡者風衣或永虛戰甲，穩定通關優先於面板數字。",
        },
    }[play_mode]

    readiness = max(15, min(100, main["score"] + chaos["score"] + divine["score"]))
    return {
        "phase": main["phase"],
        "title": main["title"],
        "reason": main["reason"],
        "readiness": readiness,
        "build": mode["build"],
        "mode_instruction": mode["instruction"],
        "priorities": [
            {"label": "主位第一順位", "title": main["title"], "detail": main["action"]},
            {"label": chaos["label"], "title": chaos["title"], "detail": chaos["detail"]},
            {"label": "支援鏈", "title": divine["title"], "detail": divine["detail"]},
        ],
        "avoid": main["avoid"],
        "switch_condition": main["switch"],
        "next_breakpoint": chaos["next"],
    }
