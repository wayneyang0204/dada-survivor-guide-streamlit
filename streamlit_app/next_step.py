"""Evidence-labelled milestones, not a simulated global DPS optimum.

Unknown inputs remain None. Resource pools are never treated as interchangeable.
Costs that vary by account are supplied from the game's upgrade preview.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json

SCHEMA = 1
CHECKED = "2026-09-07～09-08"
HALL_SOURCE = "https://notalknote.xyz/custom-collection/"
AWAKE_SOURCE = "https://notalknote.xyz/survivor-awakening/"
COLLECT_SOURCE = "https://notalknote.xyz/survivorio-collection-hall/"
SET_SOURCE = "https://notalknote.xyz/collectible-sets/"
CALCULATOR = "https://sio-tools.exp0.dev/"
PET_SOURCE = "https://www.taptap.cn/moment/578920141585124521?group_id=338134"
RESOURCES = ("收藏之心", "高級收藏之心", "傳奇收藏自選", "覺醒核心", "神器核心", "科技配件", "寵物材料")
MODES = ("末世迴響", "遠征／月礦首領", "主線推關", "新版區域行動")
STARS = ("未持有", "黃1", "黃2", "黃3", "黃4", "黃5", "紅1", "紅2", "紅3", "紅4", "紅5")
STOCK_LABELS = {"hearts": "收藏之心", "advanced_hearts": "高級收藏之心", "red_boxes": "傳奇收藏自選箱",
                "awakening_cores": "覺醒核心", "s_shards": "主位S特工碎片", "relic_cores": "神器核心"}
READY_STATES = ("現在可做", "材料已足")
FOCUSES = ("按目前配置補缺口", "首領傷害不足", "技能成形太慢", "生存不足")
FIELDS = {
    "mode": ("末世迴響", MODES),
    "growth_focus": ("按目前配置補缺口", FOCUSES),
    "survivor": (None, ("維納托", "塔洛莎", "楊大師", "其他")),
    "awakening": (None, (0, 8)), "taloxa": (None, (0, 8)),
    "awakening_goal": (None, (0, 8)),
    "awakening_cores": (None, (0, 10000)), "s_shards": (None, (0, 100000)),
    "quantum_ready": (None, (True, False)),
    "slots": (None, (0, 100)), "red_owned": (None, (0, 100)),
    "red_placed": (None, (0, 100)), "hearts": (None, (0, 10000000)),
    "next_slot_cost": (None, (0, 10000000)),
    "adv1": (None, (0, 4)), "adv2": (None, (0, 8)),
    "stars1": ([], "stars4"), "stars2": ([], "stars8"),
    "advanced_hearts": (None, (0, 100000)),
    "advanced_cost": (None, (0, 100000)), "advanced_quote": (None, "text"),
    "neck": (None, ("破壞者徽記", "其他")), "memory": (None, (0, 10)),
    "ss_boots": (None, (True, False)), "boot_stars": ([], "stars4"),
    "ice_armor_ready": (None, (True, False)),
    "crit_more_useful": (None, (True, False)), "crit_mode": (None, MODES),
    "red_boxes": (None, (0, 10000)),
    "dark_matter": (None, (0, 10)),
    "step_quotes": ({}, "quotes"),
    "estimated_balances": ([], "balances"),
    "weapon": (None, ("雙絕槍", "其他")),
    "weapon_e": (None, (0, 5)), "weapon_v": (None, (0, 5)),
    "relic_cores": (None, (0, 10000)), "gear_materials_ready": (None, (True, False)),
    "drone_red": (None, (True, False)), "forcefield_red": (None, (True, False)),
    "twin_drone": (None, (True, False)),
    "pet_kind": (None, ("普通輸出寵", "主人增益寵", "異世寵物", "未持有")),
    "pet_skills_ready": (None, (True, False)),
    "pet_target": (None, "text"),
    "pet_gain": (None, ("主人增傷／有效增益", "寵物自身傷害", "只有面板／尚未確認")),
    "pet_materials_ready": (None, (True, False)),
}


def clean_profile(raw: dict) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("帳號資料必須是物件。")
    result = {}
    for key, (default, rule) in FIELDS.items():
        value = raw.get(key, default)
        if value is None:
            result[key] = default if key in ("mode", "growth_focus") or isinstance(default, (list, dict)) else None
            continue
        if rule == "quotes":
            if not isinstance(value, dict) or len(value) > 32:
                raise ValueError("目標材料紀錄格式錯誤。")
            checked = {}
            for quote_key, quote in value.items():
                if not isinstance(quote_key, str) or len(quote_key) != 24 or any(c not in "0123456789abcdef" for c in quote_key):
                    raise ValueError("目標材料紀錄識別碼錯誤。")
                if not isinstance(quote, dict) or set(quote) != {"cost", "materials_ready"}:
                    raise ValueError("目標材料紀錄欄位不完整。")
                cost, ready = quote["cost"], quote["materials_ready"]
                if cost is not None and (type(cost) is not int or not 0 <= cost <= 10000000):
                    raise ValueError("目標所需材料不可為負數或小數。")
                if ready is not None and type(ready) is not bool:
                    raise ValueError("其他材料是否齊全必須選是或否。")
                checked[quote_key] = dict(quote)
            value = checked
        elif rule == "balances":
            if not isinstance(value, list) or len(value) > len(STOCK_LABELS) or any(not isinstance(k, str) or k not in STOCK_LABELS for k in value):
                raise ValueError("推算庫存欄位不正確。")
            value = list(dict.fromkeys(value))
        elif isinstance(rule, str) and rule.startswith("stars"):
            limit = int(rule[5:])
            if not isinstance(value, list) or len(value) > limit or any(type(n) is not int or not 0 <= n <= 10 for n in value):
                raise ValueError("收藏星數格式錯誤，請用黃1～紅5。")
        elif rule == "text":
            if not isinstance(value, str) or len(value) > 100:
                raise ValueError("欄位文字過長。")
        elif isinstance(rule, tuple) and type(rule[0]) is int:
            if type(value) is not int or not rule[0] <= value <= rule[1]:
                raise ValueError(f"{key} 超出可接受範圍。")
        elif isinstance(rule, tuple) and type(rule[0]) is bool and type(value) is not bool:
            raise ValueError(f"{key} 必須選是或否。")
        elif value not in rule:
            raise ValueError(f"{key} 的選項不正確。")
        result[key] = value
    if result["red_placed"] is not None:
        for key in ("slots", "red_owned"):
            if result[key] is not None and result["red_placed"] > result[key]:
                raise ValueError("已擺入的紅收藏數不可超過已開槽位或已持有紅收藏數。")
    result["estimated_balances"] = [k for k in result["estimated_balances"] if result[k] is not None]
    return result


def export_profile(profile: dict) -> str:
    return json.dumps({"schema": SCHEMA, "profile": clean_profile(profile)}, ensure_ascii=False, indent=2)


def import_profile(content: bytes) -> dict:
    if len(content) > 32768:
        raise ValueError("紀錄檔過大，請選本站匯出的 JSON。")
    try:
        raw = json.loads(content)
        if not isinstance(raw, dict) or raw.get("schema") != SCHEMA:
            raise ValueError("紀錄版本不支援。")
        return clean_profile(raw.get("profile"))
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
        raise ValueError("無法讀取紀錄，請選本站匯出的 JSON。") from exc


def parse_stars(text: str, limit: int) -> list[int]:
    import re
    if not text.strip():
        return []
    values = []
    for token in re.split(r"[\s,，、]+", text.strip()):
        token = token.upper().replace("金", "黃").replace("Y", "黃").replace("R", "紅")
        if token in ("0", "未持有"):
            values.append(0)
        elif token in STARS:
            values.append(STARS.index(token))
        else:
            raise ValueError("請填黃1～黃5、紅1～紅5；未持有填 0，項目以逗號分隔。")
    if len(values) > limit:
        raise ValueError(f"這組最多 {limit} 件。")
    return values


@dataclass
class Step:
    id: str
    resource: str
    title: str
    target: str
    why: str
    stop: str
    source: str
    priority: int = 50
    status: str = "待核對材料"
    cost: str = "依遊戲升級預覽核對"
    gap: str = ""
    caution: str = ""
    current: str = ""
    effect: str = ""
    update: dict | None = None
    quote_kind: str = ""
    quote_key: str = ""
    checks: list[dict] = field(default_factory=list)


def numeric_check(label: str, owned: int | None, needed: int | None) -> dict:
    if needed == 0 and owned is None:
        detail, state = "本目標不需要投入這項資源；庫存仍未填寫", "ready"
    elif owned is None or needed is None:
        detail = ("庫存尚未填寫" if owned is None else f"庫存 {owned:,}") + "；" + ("需求尚未核對" if needed is None else f"需要 {needed:,}")
        state = "unknown"
    elif owned < needed:
        detail, state = f"{owned:,}／{needed:,}，還差 {needed-owned:,}", "short"
    else:
        detail, state = f"{owned:,}／{needed:,}，投入後推算剩 {owned-needed:,}", "ready"
    return {"label": label, "state": state, "detail": detail, "owned": owned, "needed": needed}


def condition_check(label: str, value: bool | None) -> dict:
    return {"label": label, "state": "unknown" if value is None else "ready" if value else "short",
            "detail": "尚未核對" if value is None else "已符合" if value else "尚未符合"}


def assess_checks(step: Step, checks: list[dict]) -> Step:
    """Known shortages remain visible even when another requirement is unknown."""
    step.checks = checks
    shortages = [c for c in checks if c["state"] == "short"]
    unknowns = [c for c in checks if c["state"] == "unknown"]
    step.status = "先存資源" if shortages else "待核對材料" if unknowns or not checks else "材料已足"
    messages = [f"{c['label']}：{c['detail']}。" for c in shortages]
    if unknowns:
        messages.append("還需核對：" + "、".join(c["label"] for c in unknowns) + "。")
    step.gap = ("尚未建立這個目標的必要條件。" if not checks else " ".join(messages)
                if messages else "這個目標的材料條件已齊，完成後再重新排序。")
    return step


def affordability(step: Step, owned: int | None, cost: int | None) -> Step:
    assess_checks(step, [numeric_check(step.resource, owned, cost)])
    if cost is not None:
        step.cost = f"{cost:,} {step.resource}"
    return step


def apply_quote(step: Step, p: dict) -> None:
    """A player-confirmed recipe applies to exactly this account milestone."""
    if not step.quote_kind:
        return
    identity = {k: getattr(step, k) for k in ("id", "resource", "target", "current")}
    identity.update(mode=p["mode"], survivor=p["survivor"])
    step.quote_key = hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:24]
    quote = p["step_quotes"].get(step.quote_key, {})
    stock_key = "red_boxes" if step.quote_kind == "collection" else "awakening_cores"
    unit = "傳奇收藏自選箱" if step.quote_kind == "collection" else "覺醒核心"
    condition = "自選期數與其他升級條件" if step.quote_kind == "collection" else "目標角色碎片與連攜條件"
    assess_checks(step, [numeric_check(unit, p[stock_key], quote.get("cost")),
                        condition_check(condition, quote.get("materials_ready"))])
    if quote.get("cost") is not None:
        step.cost = f"{quote['cost']:,} {unit}（你核對的整段需求）"


def refine_candidates(steps: list[Step], p: dict) -> tuple[list[Step], list[dict]]:
    """Effect prerequisites override recipes. No invented damage/ROI scores."""
    active, deferred = [], []
    for step in steps:
        if (step.id == "memory" and step.update["memory"] in (3, 5)
                and p["crit_mode"] == p["mode"] and p["crit_more_useful"] is False):
            deferred.append({**asdict(step), "reason": "本模式已確認追加暴率沒有收益（含溢出轉換）；先不為暴率門檻花箱子。面板與後續暴傷節點需另比，並非整件收藏無用。"})
            continue
        if step.id == "memory" and step.update["memory"] in (3, 5):
            useful = p["crit_more_useful"] if p["crit_mode"] == p["mode"] else None
            assess_checks(step, [*step.checks, condition_check("本模式追加暴率有收益（含溢出轉換）", useful)])
        if step.id == "boots_set":
            if p["ice_armor_ready"] is False:
                deferred.append({**asdict(step), "reason": "SS鞋冰甲技能尚未啟用；四件黃三星無法兌現這條路線所追的冰甲增益。先核對鞋子技能，不盲拆裝備補神鑄。"})
                continue
            assess_checks(step, [*step.checks, condition_check("SS鞋永恆神鑄的冰甲已啟用", p["ice_armor_ready"])])
        if step.id == "lance_e1" and p["growth_focus"] == "技能成形太慢":
            step.priority = 105
            step.why = "你目前卡在技能成形速度；先比較雙絕槍E1這個已收錄的基礎進化節點，而不是只追高階面板。仍需備妥完整材料。"
        active.append(step)
    # Only compare costs when the SAME stated crit-damage milestone is ready.
    same_bonus = [s for s in active if s.id in ("memory", "dark_matter")
                  and s.effect == "暴擊傷害＋10%" and s.status in READY_STATES]
    costs = {s.id: next((c["needed"] for c in s.checks if c.get("label") == "傳奇收藏自選箱"), None) for s in same_bonus}
    if len(same_bonus) == 2 and all(type(v) is int for v in costs.values()) and len(set(costs.values())) == 2:
        cheaper = min(same_bonus, key=lambda s: costs[s.id])
        other = next(s for s in same_bonus if s != cheaper)
        cheaper.priority = max(s.priority for s in same_bonus) + 1
        cheaper.why = (f"兩個已備妥目標都解鎖暴擊傷害＋10%；本步整段需要 {costs[cheaper.id]} 箱，"
                       f"「{other.title}」需要 {costs[other.id]} 箱，先完成較省箱的同類門檻。不同期箱子須能選各自目標；未比較沿途面板，非總傷害效益排名。")
    return active, deferred


def advanced_options(p: dict) -> list[Step]:
    thresholds = (5, 12, 24, 36, 50, 60, 70, 80)
    effects = ("暴擊傷害＋20%", "技能傷害＋20%", "對衰弱／中毒／冰緩目標傷害各＋10%",
               "暴擊傷害＋40%", "攻擊與生命", "對衰弱／中毒／冰緩目標傷害各＋15%",
               "技能傷害＋40%", "對菁英／BOSS傷害＋20%，另有異常增傷")
    options = []
    for number, limit in ((1, 4), (2, 8)):
        opened, stars = p[f"adv{number}"], p[f"stars{number}"]
        if opened is None or not stars:
            continue
        # Positions are the player's planned assignment, not reusable copies.
        active_total = sum(stars[:opened])
        unmet_opened = next((n for n in range(1, opened + 1)
                             if len(stars) < n or active_total < thresholds[n-1]), None)
        if unmet_opened:
            n = unmet_opened
            rearranged = sorted(stars, reverse=True)
            rearranged_total = sum(rearranged[:opened])
            if rearranged_total >= thresholds[n-1]:
                options.append(Step(f"adv{number}_rearrange", "高級收藏之心",
                    f"先調整第{number}套擺放，不急著升星", f"高星收藏放到已進階的 {opened} 格",
                    "這套已填的收藏中有更高星成員；先把它移入已進階槽，便能補上目前未亮的門檻。",
                    "重新擺好就停，重算下一格是否值得開。", HALL_SOURCE, 118,
                    "現在可做", "0 高級收藏之心",
                    current=f"已進階槽：目前 {active_total} 星 → 調整後 {rearranged_total} 星",
                    effect=effects[n-1],
                    caution="僅在同一套已持有的收藏中調整；不從另一套借用同一件，不改變已開格數。",
                    update={f"stars{number}": rearranged}))
                continue
            options.append(Step(f"adv{number}_stars", "高級收藏之心",
                f"先補第{number}套已開槽的星數", f"已進階槽合計 {thresholds[n-1]} 星",
                "先檢查已進階槽的累計星數；這一檔尚未啟動，先補星或調整擺放，再比較開格。",
                "這個星數門檻亮起後重新比較下一格。", HALL_SOURCE, 90,
                "星數未達", "本步先不花高級收藏之心",
                f"已進階 {opened} 格合計 {active_total}／{thresholds[n-1]} 星，還差 {thresholds[n-1]-active_total} 星。",
                effect=effects[n-1]))
            if len(stars) < opened:
                options[-1].status = "資料未齊"
                options[-1].gap = f"已進階 {opened} 格，但只填了 {len(stars)} 件星數；請補完，不能把未填當成零。"
            continue
        if opened == limit:
            continue
        n = opened + 1
        total = sum(stars[:n])
        ready = len(stars) >= n and total >= thresholds[n-1]
        boss_route = number == 2 and len(stars) == 8 and sum(stars) >= 80 and p["mode"] in MODES[:2]
        step = Step(f"adv{number}_{n}", "高級收藏之心",
            f"進階第{number}套第{n}格", f"第{number}套 {n} 個進階格＋{thresholds[n-1]} 星",
            "已備妥80傳奇星，可把第二套第8格菁英／BOSS加成列為路線目標；這一筆先推進下一格。" if boss_route else "以能立即啟動的門檻比較；開格與收藏星數必須一起達標。",
            "啟動這一檔就停，重新比較下一筆材料。", HALL_SOURCE,
            115 if boss_route else 85 if n in (1, 2, 7) else 65,
            current=f"已開 {opened} 格；預定前{n}格 {total} 星", effect=effects[n-1],
            caution="這是條件式路線，不代表固定增加同等百分比的總輸出。第一套和第二套不可重複使用同一件收藏。",
            update={f"adv{number}": n})
        if not ready:
            if len(stars) < n:
                step.status, step.gap = "資料未齊", f"請先填完這套前 {n} 格的星數；目前只填 {len(stars)} 件，未持有的那件請明確填 0。"
            else:
                step.status, step.gap = "星數未達", f"目前 {total}／{thresholds[n-1]} 星；先補星或調整擺放。"
        else:
            quoted = p["advanced_cost"] if p["advanced_quote"] == step.id else None
            affordability(step, p["advanced_hearts"], quoted)
        options.append(step)
    return options


def recommend(raw: dict, resource: str = "自動排序") -> dict:
    p = clean_profile(raw)
    steps: list[Step] = []
    missing = []
    if p["mode"] == "新版區域行動":
        return {"primary": asdict(Step("zone", "玩法", "先調整局內路線與技能", "先取得局內 Buff，再挑戰區域首領",
                "這個模式需先確認局外養成是否帶入，不能直接拿首領養成順位套用。", "記錄一次失敗原因後，只改一項再試。",
                "https://notalknote.xyz/dadasurvivor-regional-action-update-guide/", status="先做玩法調整",
                cost="不消耗核心")), "alternatives": [], "missing": [], "complete": []}

    if any(p[k] is None for k in ("slots", "red_owned", "red_placed")):
        missing.append("典藏館：已開格數、持有與已擺入的紅收藏數")
    else:
        empty = p["slots"] - p["red_placed"]
        spare = p["red_owned"] - p["red_placed"]
        if empty and spare:
            steps.append(Step("hall_fill", "收藏之心", "把已持有紅收藏放進空槽", "先填滿已開槽位",
                "已解鎖槽位和紅收藏都在手上，先拿到不需再買材料的典藏加成。",
                "可放的紅收藏用完就停。", HALL_SOURCE, 120, "現在可做", "0 收藏之心",
                update={"red_placed": min(p["slots"], p["red_owned"])}))
        elif empty:
            first_new = "記憶編輯器" if p["memory"] == 0 and p["neck"] == "破壞者徽記" else "一件尚未持有的紅收藏"
            steps.append(affordability(Step("red_unlock", "傳奇收藏自選", "先解鎖一件尚未持有的紅收藏", "填上 1 個已開的空槽",
                "普通典藏格看原生品質；黃一星的傳奇收藏即可計入紅品質件數。",
                "補上空槽後重算，不先集中同一件升高星。", HALL_SOURCE, 105,
                caution="自選箱必須能選尚未解鎖的傳奇收藏，且足夠合成一件；不是把黃品質升紅星。",
                current=f"持有 {p['red_owned']} 件；已擺入 {p['red_placed']}／{p['slots']} 格",
                update={"red_owned": p["red_owned"]+1, "red_placed": p["red_placed"]+1,
                        **({"memory": 1} if first_new == "記憶編輯器" else {})}, quote_kind="collection"),
                None, None))
            steps[-1].title = f"先解鎖{first_new}，補上典藏空槽"
        elif spare:
            steps.append(affordability(Step("hall_open", "收藏之心", "開下一個能立刻放紅收藏的槽位", "開 1 格並擺入紅收藏",
                "先比較各套下一格價格；已持有多餘紅收藏時，開格才能立即取得效果。",
                "開一格後重算，避免一次買到昂貴空槽。", HALL_SOURCE, 95,
                current=f"{p['red_placed']}／{p['slots']} 格已放紅收藏；另有 {spare} 件可放",
                update={"slots": p["slots"]+1, "red_placed": p["red_placed"]+1}), p["hearts"], p["next_slot_cost"]))

    steps.extend(advanced_options(p))
    if p["adv2"] is None or not p["stars2"]:
        missing.append("進階典藏：第二套已進階格數與各格傳奇星數")

    if p["neck"] == "破壞者徽記" and p["memory"] is not None and p["memory"] < 10:
        target = next(n for n in (3, 5, 8, 10) if p["memory"] < n)
        effect = "破壞者徽記低血量暴擊率上限＋20%" if target <= 5 else "暴擊傷害＋10%" if target == 8 else "破壞者徽記低血量傷害上限＋20%"
        steps.append(Step("memory", "傳奇收藏自選", f"記憶編輯器升到{STARS[target]}星", f"{STARS[target]}星",
            "你仍使用破壞者徽記；只列下一個有技能或暴傷效果的節點，不停在中間的面板星。",
            "到目標星數就停，再比較SS鞋套裝或其他缺口。", COLLECT_SOURCE, 90,
            current=STARS[p["memory"]], effect=effect,
            caution="徽記專屬效果需要低血量條件；若暴擊率已達需求，黃三星／五星的優先性會下降。未計算你的實際增傷比例。",
            update={"memory": target}, quote_kind="collection"))
    if (p["drone_red"] or p["twin_drone"]) and p["dark_matter"] is not None and p["dark_matter"] < 10:
        target = next(n for n in (3, 5, 8, 10) if p["dark_matter"] < n)
        steps.append(Step("dark_matter", "傳奇收藏自選", f"暗物質傀儡升到{STARS[target]}星", f"{STARS[target]}星",
            "你的配置包含無人機；先追這個配件實際會用到的收藏節點。",
            "到這個節點先停，再看無人機傷害占比與其他收藏缺口。", COLLECT_SOURCE, 92,
            current=STARS[p["dark_matter"]],
            effect="暴擊傷害＋10%" if target == 8 else f"無人機／雙生無人機飛彈單發傷害＋{5 if target == 3 else 10 if target == 5 else 15}%",
            caution="單發飛彈增傷不是全帳號總傷害增幅；未把它與不同乘區硬換成同一分數。",
            update={"dark_matter": target}, quote_kind="collection"))
    if p["ss_boots"] and len(p["boot_stars"]) == 4 and min(p["boot_stars"]) < 3:
        names = ("賽博圖騰柱", "複製寶鏡", "夢境拼圖", "基因編輯器")
        needed = [f"{names[i]} {STARS[n]}→黃3" for i, n in enumerate(p["boot_stars"]) if n < 3]
        step = Step("boots_set", "傳奇收藏自選", "SS鞋套裝：補齊四件黃三星", "四件都至少黃3星，啟動同一個套裝門檻",
            f"這套還缺 {len(needed)} 件達標。先核對整組成本，避免只花到一半卻尚未啟動套裝技能。",
            "四件各到黃三星就停，已超過的成員不降星、不再追加。", SET_SOURCE, 85,
            current="；".join(needed),
            effect="四件達標且已啟用鞋子永恆神鑄冰甲時，每層冰霜血脈增加10%護盾增傷",
            caution="不是整體傷害直接增加10%。必須核對冰甲已啟用；填寫的是所有缺件合計成本，不只一件。",
            quote_kind="collection", update={"boot_stars": [max(3, n) for n in p["boot_stars"]]})
        steps.append(step)
    if p["neck"] is None or p["memory"] is None:
        missing.append("收藏：目前項鍊與記憶編輯器星數")

    role_paused = (p["awakening_goal"] is not None and p["awakening"] is not None
                   and p["awakening"] >= p["awakening_goal"])
    if not role_paused and p["survivor"] == "維納托" and p["awakening"] in (6, 7):
        target = p["awakening"]+1
        shards = 550 if target == 7 else 600
        step = affordability(Step("venato", "覺醒核心", f"維納托 R{p['awakening']} → R{target}", f"維納托覺醒{target}",
            "主位的下一個已查核技能節點；保留現役協同，不預設重置任何角色。",
            "只升這一階，達標後重新比較協同與其他資源。", AWAKE_SOURCE, 88,
            current=f"維納托 R{p['awakening']}",
            effect="猩紅蝙蝠傷害與對菁英／首領增傷強化" if target == 7 else "背水一戰每層暴擊傷害強化",
            caution="這是主位路線建議；尚未計入完整同調、協同和實戰覆蓋率。",
            update={"awakening": target}), p["awakening_cores"], 30)
        step.cost = f"30 覺醒核心＋{shards} 角色碎片＋遊戲預覽所需量子碎片"
        assess_checks(step, [numeric_check("覺醒核心", p["awakening_cores"], 30),
                            numeric_check("角色碎片", p["s_shards"], shards),
                            condition_check("量子碎片", p["quantum_ready"])])
        steps.append(step)
    elif p["survivor"] is None or p["awakening"] is None:
        missing.append("特工：目前主位與精確覺醒等級")

    if not role_paused and p["survivor"] == "維納托" and p["awakening"] == 5:
        steps.append(Step("venato6", "覺醒核心", "維納托下一階先到 R6", "維納托覺醒6",
            "覺醒6強化背水一戰層數，並新增連攜被動槽位。",
            "升到R6後重新比較R7與協同，不一次投入到R8。", AWAKE_SOURCE, 85,
            current="維納托 R5", effect="背水一戰最多疊加層數＋5、連攜被動槽位＋1",
            update={"awakening": 6}, quote_kind="awakening"))
    if p["survivor"] == "維納托" and p["taloxa"] is not None and p["taloxa"] < 4 and (p["drone_red"] or p["twin_drone"]):
        steps.append(Step("taloxa4", "覺醒核心", "補塔洛莎協同到 R4", "塔洛莎覺醒4並裝備連攜被動",
            "你已使用無人機配件；此節點讓無人機命中能施加裂傷，需實際裝入連攜才計入。",
            "R4就停，再比較主位下一階。", AWAKE_SOURCE, 95,
            current=f"塔洛莎 R{p['taloxa']}", effect="無人機觸發裂傷的被動門檻",
            caution="未計算重置其他特工的成本；升級前確認連攜槽與碎片需求。", update={"taloxa": 4}, quote_kind="awakening"))

    if p["weapon"] == "雙絕槍" and p["weapon_e"] == 0:
        steps.append(affordability(Step("lance_e1", "神器核心", "雙絕槍先補永恆神鑄1", "E1",
            "先完成主武器的基礎進化節點，才比較後續高成本神鑄。", "E1完成後停，不自動一路加到E4。",
            "https://notalknote.xyz/ss-twin-lance-starforged-havoc/", 90,
            caution="還需對應S裝、永恆核心與基礎材料；僅神器核心足夠不代表能升。",
            update={"weapon_e": 1}), p["relic_cores"], 1))
        step = steps[-1]
        assess_checks(step, [numeric_check("神器核心", p["relic_cores"], 1),
                            condition_check("E1所需S裝及其他材料", p["gear_materials_ready"])])
    if p["weapon"] is None or p["weapon_e"] is None or p["weapon_v"] is None:
        missing.append("裝備：主武器與永恆／虛空神鑄")

    if p["twin_drone"] is False and p["drone_red"] is True:
        step = Step("twin_drone", "科技配件", "下一個配件目標：雙生無人機", "紅無人機＋紅力場，完成雙生合成",
            "已有紅無人機，先補合成缺口；不要求你同時換整套裝備。", "合成後依戰鬥傷害分布重排。",
            "https://notalknote.xyz/twinborn-parts/", 80,
            "現在可做" if p["forcefield_red"] is True else "先存資源" if p["forcefield_red"] is False else "待核對材料",
            "紅無人機＋紅力場；其他條件依合成頁核對",
            "合成前核對諧振配置" if p["forcefield_red"] is True else "先把力場配件補到紅色" if p["forcefield_red"] is False else "先確認是否已有紅力場，不把未知當成沒有。",
            update={"twin_drone": True})
        assess_checks(step, [condition_check("紅無人機配件", p["drone_red"]),
                            condition_check("紅力場配件", p["forcefield_red"])])
        steps.append(step)
    if p["twin_drone"] is None:
        missing.append("科技：是否已完成雙生無人機")

    if p["pet_kind"] is None:
        missing.append("寵物：主戰類型、技能配置與下一個覺醒效果")
    elif p["pet_kind"] == "未持有":
        missing.append("寵物：尚未持有主戰寵，先確認可取得的寵物，不預設抽取成本")
    elif p["pet_skills_ready"] is not True:
        steps.append(Step("pet_skills", "寵物材料", "先核對寵物出戰／助戰技能", "主戰與助戰技能服務同一個傷害目標",
            "先檢查現有技能是否放對；普通輸出寵強化寵物傷害，主人增益／異世寵優先核對主人有效增益。",
            "只調整已解鎖技能；需要新寵或新材料時先停，不為湊配置盲抽。", PET_SOURCE, 110,
            "待核對材料", "只用已解鎖技能時不花新材料",
            current=p["pet_kind"], effect="先排除技能未裝入或助戰方向不一致的問題",
            caution="社群來源已停止更新；不把歷史寵物排名當成當前版本最優配置。",
            update={"pet_skills_ready": True}))
    elif p["pet_target"] and p["pet_target"].strip() and p["pet_gain"] in ("主人增傷／有效增益", "寵物自身傷害"):
        step = Step("pet_node", "寵物材料", f"寵物：{p['pet_target'].strip()}", p["pet_target"].strip(),
            "已核對下一階有主人有效增益，完成一個節點後再比較其他系統。" if p["pet_gain"] == "主人增傷／有效增益" else
            "這一階只強化寵物自身輸出；先看同模式結算的寵物占比，不能當成主人等比例增傷。",
            "只完成這個節點；重新核對下一階效果與整段需求，不連續追加。", PET_SOURCE,
            82 if p["pet_gain"] == "主人增傷／有效增益" else 55,
            current=p["pet_kind"], effect=p["pet_gain"],
            caution="目標與效果來自你核對的遊戲預覽，不是本站已驗證的寵物階級推薦。異世覺醒／共鳴不套用普通寵物成本。",
            update={"pet_target": None, "pet_gain": None, "pet_materials_ready": None})
        assess_checks(step, [condition_check("本節點所有本體、碎片、核心及其他材料（整段）", p["pet_materials_ready"])])
        steps.append(step)
    else:
        missing.append("寵物：下一個完整節點及其效果；只有面板的升級先保留材料")

    for step in steps:
        apply_quote(step, p)

    steps, deferred = refine_candidates(steps, p)
    if p["growth_focus"] == "生存不足":
        steps.append(Step("survival_check", "玩法", "先找出死亡原因，不急著追加輸出", "同一關卡記錄死亡原因與主力技能成形時間",
            "你指定的問題是生存不足；輸出養成未必解決死亡。先保留付費材料，確認是否需要改技能、走位或現役防護配置。",
            "確認能穩定存活後，把目前問題改成首領傷害或技能成形，再重排。", CALCULATOR, 110,
            "先做玩法調整", "先不花養成材料"))

    if resource != "自動排序":
        steps = [s for s in steps if s.resource == resource]
    # Ready actions first; within the same readiness group use explained rules.
    state = {"先做玩法調整": 4, "現在可做": 3, "材料已足": 3, "先存資源": 2, "待核對材料": 1, "星數未達": 0, "資料未齊": 0}
    steps.sort(key=lambda s: (s.id == "hall_fill" or s.id.endswith("_rearrange"), state.get(s.status, 0), s.priority, s.id), reverse=True)
    complete = []
    if p["awakening"] == 8:
        complete.append("主位覺醒8：不再推薦重複升級")
    elif role_paused:
        complete.append(f"主位階段目標 R{p['awakening_goal']} 已達：暫停主位追加，改比其他系統；協同另算")
    if p["adv2"] == 8 and len(p["stars2"]) == 8 and sum(p["stars2"]) >= 80:
        complete.append("第二套8進階格／80傳奇星：菁英與BOSS門檻已完成")
    return {"primary": asdict(steps[0]) if steps else None,
            "alternatives": [asdict(s) for s in steps[1:]], "missing": missing, "complete": complete,
            "deferred": [s for s in deferred if resource == "自動排序" or s["resource"] == resource]}


SYSTEMS = {"收藏之心": "普通典藏館", "高級收藏之心": "進階典藏館", "傳奇收藏自選": "收藏品",
           "覺醒核心": "特工", "神器核心": "裝備", "科技配件": "科技", "寵物材料": "寵物", "玩法": "玩法"}


def roadmap(raw: dict) -> dict:
    """Visible cross-system queue; readiness precedes documented milestone rules.

    This is an execution order, not an ROI ranking of interchangeable budgets.
    Only the best current candidate per system is promoted to the overview.
    """
    result = recommend(raw)
    candidates = ([result["primary"]] if result["primary"] else []) + result["alternatives"]
    systems, queue = set(), []
    for step in candidates:
        system = SYSTEMS[step["resource"]]
        if system not in systems:
            queue.append({**step, "system": system, "rank": len(queue) + 1})
            systems.add(system)
    return {**result, "queue": queue}


def following_step(raw: dict, step: dict) -> dict | None:
    """Preview exactly one completed milestone without changing profile or game."""
    if not step.get("update"):
        return None
    updated = completion_preview(raw, step)["profile"]
    return recommend(updated)["primary"]


def next_question(raw: dict, result: dict | None = None) -> dict | None:
    """Ask a condition that can change the decision before asking for stock."""
    p = clean_profile(raw)
    result = result or recommend(p)
    first = result["primary"]
    if p["mode"] == "新版區域行動" or first and first["id"] in ("hall_fill", "survival_check") or first and first["id"].endswith("_rearrange"):
        return None
    candidates = ([first] if first else []) + result["alternatives"]
    for step in candidates:
        if step["id"] == "memory" and step["update"]["memory"] in (3, 5) and (p["crit_mode"] != p["mode"] or p["crit_more_useful"] is None):
            return {"resource": "傳奇收藏自選", "section": "收藏品", "field": "crit_more_useful",
                    "title": "本模式繼續加暴擊率，還有實際收益嗎？",
                    "why": "答案會改變記憶編輯器黃三星／五星的順位。先看戰鬥條件與溢出轉換，不只看面板100%。"}
        if step["id"] == "boots_set" and p["ice_armor_ready"] is None:
            return {"resource": "傳奇收藏自選", "section": "收藏品", "field": "ice_armor_ready",
                    "title": "SS鞋的冰甲技能已啟用嗎？", "why": "這個前置條件未確認，不能把四件黃三星當成已可兌現的冰甲增益。"}
    if any(p[k] is None for k in ("slots", "red_owned", "red_placed")):
        return {"resource": "收藏之心", "section": "普通典藏館", "field": "hall_counts",
                "title": "先核對典藏已開槽、紅收藏持有數與擺入數", "why": "這三個數字能先找出是否有不花新材料的空槽加成，不必先填全套帳號。"}
    if first and any(c["state"] == "unknown" for c in first["checks"]):
        labels = "、".join(c["label"] for c in first["checks"] if c["state"] == "unknown")
        return {"resource": first["resource"], "section": SYSTEMS.get(first["resource"], "角色與模式"),
                "field": "recipe", "title": f"只補本步尚未確認的條件：{labels}", "why": "上方材料表保留所有已知缺額；這次不要求重填其他系統。"}
    if p["pet_kind"] is None:
        return {"resource": "寵物材料", "section": "寵物", "field": "pet_kind", "title": "確認主戰寵物的類型與下一階效果",
                "why": "目前尚無寵物候選，不能因此認定收藏一定比寵物優先。"}
    return None


def ranking_reason(result: dict) -> str:
    """Explain the actual comparator, without inventing efficiency or DPS data."""
    first = result["primary"]
    if not first:
        return "尚無足夠資料可比較，先保留資源。"
    if first["id"] == "hall_fill" or first["id"].endswith("_rearrange"):
        return "先使用已經持有、而且不需要新材料的提升；付費材料留到重新排序後再安排。"
    if first["id"] == "survival_check":
        return "先解決你指定的生存問題；材料已足的輸出升級保留為候選，不等於現在就該花。"
    other = next((s for s in result["alternatives"] if s["resource"] == first["resource"]),
                 next(iter(result["alternatives"]), None))
    if not other:
        return "這是目前已填資料中唯一可列出的路線，不代表已證明比未填資料的投資更好。"
    if first["status"] in READY_STATES and other["status"] not in READY_STATES:
        return f"這個目標的材料已齊；「{other['title']}」仍是{other['status']}，所以先列能完成的這一步。"
    if first["status"] == other["status"]:
        separate = "兩者使用不同資源，可以分別安排。" if first["resource"] != other["resource"] else "兩者使用同一種資源，先完成一個門檻再重算。"
        return f"與「{other['title']}」同為{first['status']}。{separate}本次以已收錄的門檻規則排序，並非實測傷害或每份材料效益排名。"
    return f"「{other['title']}」仍是{other['status']}。目前先追蹤資料較明確的目標；不要在未核對成本時直接投入。"


def action_token(raw: dict, step: dict) -> str:
    identity = {"profile": clean_profile(raw), "id": step["id"], "target": step["target"], "update": step.get("update")}
    return hashlib.sha256(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:24]


def completion_preview(raw: dict, step: dict) -> dict:
    """Calculate a guide-record transition; this never changes the game or input."""
    p = clean_profile(raw)
    current = recommend(p)
    candidates = ([current["primary"]] if current["primary"] else []) + current["alternatives"]
    fresh = next((s for s in candidates if all(s.get(k) == step.get(k) for k in ("id", "target", "current", "update"))), None)
    if not fresh or not fresh.get("update"):
        raise ValueError("帳號或目標已變更，請重新查看下一步再記錄完成。")
    values = dict(fresh["update"])
    costs, cleared = {}, []
    sid, resource = fresh["id"], fresh["resource"]
    if sid == "hall_open":
        costs["hearts"] = p["next_slot_cost"]
        values["next_slot_cost"] = None
    elif sid.startswith("adv") and sid.rsplit("_", 1)[-1].isdigit():
        costs["advanced_hearts"] = p["advanced_cost"] if p["advanced_quote"] == sid else None
        values.update(advanced_cost=None, advanced_quote=None)
    elif sid == "venato":
        costs.update(awakening_cores=30, s_shards=550 if values["awakening"] == 7 else 600)
        values["quantum_ready"] = None
    elif resource == "覺醒核心":
        quote = p["step_quotes"].get(fresh["quote_key"], {})
        costs["awakening_cores"] = quote.get("cost") if quote.get("materials_ready") is True else None
        values.update(s_shards=None, quantum_ready=None)
    elif resource == "神器核心":
        costs["relic_cores"] = 1 if sid == "lance_e1" else None
        values["gear_materials_ready"] = None
    elif resource == "傳奇收藏自選":
        quote = p["step_quotes"].get(fresh["quote_key"], {})
        costs["red_boxes"] = quote.get("cost") if quote.get("materials_ready") is True else None
        newly_owned = sum(1 for key in ("memory", "dark_matter") if key in values and p[key] == 0 and values[key] > 0)
        if "boot_stars" in values:
            newly_owned += sum(1 for old, new in zip(p["boot_stars"], values["boot_stars"]) if old == 0 and new > 0)
        if newly_owned and "red_owned" not in values and p["red_owned"] is not None:
            values["red_owned"] = p["red_owned"] + newly_owned
    if resource in ("傳奇收藏自選", "覺醒核心"):
        # Partial fragments and shared selectors may have changed during spending.
        values["step_quotes"] = {}
    estimates = set(p["estimated_balances"])
    changes = []
    for key, cost in costs.items():
        owned = p[key]
        if owned is not None and cost is not None and owned >= cost:
            values[key] = owned - cost
            estimates.add(key)
            changes.append({"resource": STOCK_LABELS[key], "before": owned, "used": cost, "after": owned-cost})
        else:
            values[key] = None
            estimates.discard(key)
            cleared.append(STOCK_LABELS[key])
    values["estimated_balances"] = sorted(estimates)
    updated = clean_profile({**p, **values})
    return {"profile": updated, "balances": changes, "unknown": cleared}
