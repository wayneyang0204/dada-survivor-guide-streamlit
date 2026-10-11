"""Small, bounded tools: no network, game actions, or profile side effects."""
from __future__ import annotations

from math import isfinite
from datetime import datetime, timezone

UMBRAL_SOURCE = "https://notalknote.xyz/survivor-io-umbral-soul-pet-guide-2026/"
ELAINE_LIMITS = {0: 0, 1: 2, 2: 4, 3: 4, 4: 6, 5: 6, 6: 8, 7: 8, 8: 10}


def guild_ticket_budget(coins: int | None, reserve: int | None,
                        price: int | None, requested: int | None) -> dict:
    """Exact purchase arithmetic only; never predicts random gems on the board."""
    if any(value is None for value in (coins, reserve, price, requested)):
        return {"state": "unknown", "message": "填本期票價、公會幣與保留額；不把寶石當公會幣。"}
    if any(type(value) is not int or value < 0 for value in (coins, reserve, price, requested)) or price == 0:
        raise ValueError("公會幣、保留額與張數需為非負整數，單券價格需大於0。")
    available = max(0, coins - reserve)
    cost = price * requested
    return {"state": "quoted", "available": available, "max_tickets": available // price,
            "cost": cost, "shortfall": max(0, cost - available),
            "safe": cost <= available,
            "message": "這只計買券成本；不預測每券寶鑽，不保證公會跨檔，也不超過遊戲本期購買上限。"}


def event_window(start: str | None, end: str | None, now: datetime | None = None) -> dict:
    """Status of the published schedule; never claims an observed game opening."""
    if not start or not end:
        return {"state": "unknown", "label": "時間未完整核對，查看遊戲倒數"}
    begins, ends = datetime.fromisoformat(start), datetime.fromisoformat(end)
    current = now or datetime.now(timezone.utc)
    if any(value.tzinfo is None or value.utcoffset() is None for value in (begins, ends, current)) or ends <= begins:
        raise ValueError("活動時間需含時區，且結束晚於開始。")
    if current < begins:
        return {"state": "scheduled", "label": "官方預告期間，先保留資源"}
    if current >= ends:
        return {"state": "ended", "label": "原期官方排程已結束，只供復刻核對"}
    return {"state": "within", "label": "官方排程內，仍須核對遊戲入口與倒數"}


def pet_milestone(name: str | None, star: int | None) -> dict:
    """Selected effect milestones, not a full pet tier list or recipe table."""
    if name != "幽暗之靈" or star is None:
        return {"state": "unknown", "message": "先填寵物名稱與目前覺醒星級；其他寵物請照遊戲預覽填目標。"}
    if type(star) is not int or not 0 <= star <= 10:
        raise ValueError("覺醒星級不正確。")
    if star == 0:
        return {"state": "unknown", "message": "未持有寵物，不列覺醒投入。先核對本體取得方式，不預設抽取成本。"}
    if star == 10:
        return {"state": "done", "message": "幽暗之靈紅5已達本表最高效果節點；先重查助戰、科技與收藏，不再重複追加。"}
    target = 4 if star < 4 else 10
    return {"state": "listed", "target": target,
            "label": "幽暗之靈覺醒黃4" if target == 4 else "幽暗之靈覺醒紅5",
            "effect": "永夜冠冕60%易傷20秒與首領／菁英加成" if target == 4 else "再加60%易傷及其他紅5增益",
            "message": "先核對黃4易傷技能，計算目前到黃4的全部材料。" if target == 4 else
                       "黃4已達。紅5是下一個本表收錄的效果，不代表中途各階都無用；只有整段材料與實測值得時才列入。",
            "source": UMBRAL_SOURCE}


def elaine_pet_limit(awakening: int | None, pet_star: int | None) -> dict:
    if awakening is None:
        return {"state": "unknown", "message": "先填伊狑目前覺醒等級。"}
    if type(awakening) is not int or awakening not in ELAINE_LIMITS:
        raise ValueError("伊狑覺醒範圍為R0～R8。")
    limit = ELAINE_LIMITS[awakening]
    if not limit:
        return {"state": "locked", "limit": 0, "message": "R0尚未解鎖第二隻異寵；R1開啟，仍須不同種類。"}
    text = f"R{awakening}的第二寵技能上限：{'黃' + str(limit) if limit <= 5 else '紅' + str(limit - 5)}。"
    if pet_star is None:
        return {"state": "unknown_pet", "limit": limit, "message": text + " 再填協同寵實際星級，確認超出的技能。"}
    if type(pet_star) is not int or not 0 <= pet_star <= 10:
        raise ValueError("寵物覺醒星級不正確。")
    if pet_star == 0:
        return {"state": "unowned", "limit": limit, "message": text + " 尚未持有第二寵，不能算入協同效果。"}
    effective = min(limit, pet_star)
    return {"state": "capped" if pet_star > limit else "within", "limit": limit,
            "effective": effective, "message": text + (" 超出上限的技能不可算入。" if pet_star > limit else " 尚未超過上限。") +
            " 此處只算技能上限，不換算寵物總傷害；協同同步率需另核對。"}


def reserve_stat(value: float | None, sync: float | None) -> dict:
    if value is None or sync is None:
        return {"state": "unknown", "message": "填單件模組的該項屬性與本車同步率；留白不當作0。"}
    if any(type(n) not in (int, float) or not isfinite(n) or n < 0 for n in (value, sync)) or sync > 100:
        raise ValueError("屬性需為非負數，同步率需在0～100%。")
    amount = value * (sync / 100)
    return {"state": "calculated", "value": amount,
            "message": f"後備傳遞該項屬性 {amount:g}%。只計這一項模組屬性，不含後備連線技能，也不是總傷害增幅。"}


def compare_runs(a: str, b: str) -> dict:
    """Descriptive A/B record, not a significance test or purchasing advice."""
    import re

    def parse(text):
        tokens = [n for n in re.split(r"[\s,，、]+", text.strip()) if n]
        if not tokens:
            return []
        if len(tokens) > 30:
            raise ValueError("每組最多30場。")
        try:
            values = [float(n) for n in tokens]
        except ValueError as exc:
            raise ValueError("請填同單位純數字，以逗號分隔。") from exc
        if any(not isfinite(n) or n < 0 for n in values):
            raise ValueError("成績不可為負值、NaN或無限大。")
        return values

    first, second = parse(a), parse(b)
    if len(first) < 3 or len(second) < 3:
        return {"state": "unknown", "message": "每組至少填3場同條件成績，使用相同單位。"}
    def finite_median(values):
        ordered = sorted(values)
        count = len(ordered)
        return ordered[count // 2] if count % 2 else ordered[count // 2 - 1] / 2 + ordered[count // 2] / 2

    ma, mb = finite_median(first), finite_median(second)
    overlap = max(min(first), min(second)) <= min(max(first), max(second))
    change = (mb / ma - 1) * 100 if ma else None
    if change is not None and not isfinite(change):
        change = None
    return {"state": "descriptive", "median_a": ma, "median_b": mb,
            "min_a": min(first), "min_b": min(second), "range_overlap": overlap,
            "change": change,
            "message": "兩組範圍有重疊；不能只靠中位數差判定值得升級。" if overlap else
                       "樣本範圍未重疊，但有限場次仍不能證明統計顯著或全局最優。"}
