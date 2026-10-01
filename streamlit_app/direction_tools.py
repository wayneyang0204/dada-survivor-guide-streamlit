"""Small, deterministic action summaries. No account mutation or DPS estimates."""
from __future__ import annotations


def execution_plan(step: dict) -> dict[str, str]:
    checks = step.get("checks", [])
    short, unknown = [], []
    for check in checks:
        if check["state"] == "short":
            owned, needed = check.get("owned"), check.get("needed")
            short.append(f"{check['label']}缺 {needed-owned:,}" if owned is not None and needed is not None
                         else f"{check['label']}尚未符合")
        elif check["state"] == "unknown":
            unknown.append(check["label"])
    if step.get("id") == "zone":
        action = step["target"] + "；先不花局外養成材料。"
    elif short:
        action = "先補：" + "、".join(short) + "。目前不要按升級。"
    elif unknown:
        action = "先打開遊戲升級預覽，核對：" + "、".join(unknown) + "。"
    elif step["status"] in ("現在可做", "材料已足"):
        action = "先完成：" + step["target"] + "。"
    else:
        action = step.get("gap") or "先核對完整條件，暫不投入。"
    verify = "仍待確認：" + "、".join(unknown) + "。" if short and unknown else ""
    return {"action": action, "verify": verify, "stop": step["stop"],
            "after": "完成後更新本站紀錄，重新排序；不是照候選清單一路花完。"}


def resonance_gap(current: int | None, target: int | None) -> dict[str, str]:
    """The next effect threshold must come from the player's in-game preview."""
    if current is None or target is None:
        return {"state": "unknown", "message": "填目前能量與遊戲顯示的下一個效果門檻；空白不當作 0。"}
    if current < 0 or target <= 0:
        return {"state": "invalid", "message": "目前能量不能小於 0；目標門檻需大於 0。"}
    if target <= current:
        return {"state": "reached", "message": "這個能量門檻已達到。先確認效果生效，再選下一個尚未達到的門檻。"}
    return {"state": "short", "message": f"還差 {target-current:,} 諧振能量。先比較補這段能量的完整成本，不必直接追最高數字。"}


def related_guide(step: dict) -> str:
    if step.get("id") == "zone":
        return "upgrade-roadmap"
    return {"收藏之心": "collection-hall", "高級收藏之心": "collection-hall",
            "傳奇收藏自選": "red-choice-box", "覺醒核心": "survivor-awakening",
            "神器核心": "gear-forging", "科技配件": "twin-drone"}.get(step.get("resource"), "upgrade-roadmap")
