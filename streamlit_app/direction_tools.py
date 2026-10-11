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
    if step.get("id") in ("zone", "survival_check"):
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
    if step.get("id") == "pet_umbral":
        return "umbral-soul"
    if step.get("id") == "zone":
        return "upgrade-roadmap"
    return {"收藏之心": "collection-hall", "高級收藏之心": "collection-hall",
            "傳奇收藏自選": "red-choice-box", "覺醒核心": "survivor-awakening",
            "神器核心": "gear-forging", "科技配件": "twin-drone",
            "寵物材料": "xeno-assist" if step.get("id") == "pet_skills" else "ordinary-pet-skills"}.get(step.get("resource"), "upgrade-roadmap")


def operating_steps(step: dict) -> dict:
    """Concrete, conditional game actions for every currently supported rule."""
    sid, status = step["id"], step["status"]
    ready = status in ("現在可做", "材料已足")
    entry, steps = "", []
    if sid in ("venato", "venato6", "taloxa4"):
        hero = "塔洛莎" if sid == "taloxa4" else "維納托"
        entry = f"遊戲內「{hero}」角色的覺醒頁"
        steps = [
            f"先選{hero}，查看從目前階級到「{step['target']}」的需求；跨階需合計，不使用其他角色的報價。",
            (f"完整材料已足：只完成「{step['target']}」。" if ready else
             "先保留現役角色。活動若有覺醒核心／適用角色碎片，按上方缺額選；不要分解本次目標或現役連攜仍需的碎片。"),
            ("升到R4後，在主位可用連攜槽裝入塔洛莎「戰術協議」，才算完成這條路線。" if sid == "taloxa4" else
             "升級後檢查可用連攜槽並保留現役配置；回本站記錄這一階，不連續升下一階。"),
        ]
    elif sid in ("hall_fill", "hall_open", "red_unlock"):
        entry = "收藏館標籤 → 下方「自訂收藏館」"
        if sid == "hall_fill":
            steps = ["打開已解鎖的空格，選尚未擺入且已持有的傳奇收藏。",
                     "按確認擺入；不要先按購買新格，也不用先把這件升高星。",
                     "檢查放入件數和亮起詞條；可放收藏用完／空槽填滿就停。"]
        elif sid == "hall_open":
            steps = ["比較各套下一個未開格的遊戲顯示價格，選已有收藏能立即放入的那一格。",
                     "收藏之心不足就先存；來源列滿等收藏的多餘碎片分解、試煉之路排名戰獎勵。先看目前獎勵，別分解尚需升星的碎片。",
                     "材料足才開一格並擺入一件；不先連買數格，完成後更新下一格價格。"]
        else:
            steps = ["在自選箱清單找這次目標，確認原生傳奇品質、期數與解鎖碎片需求。",
                     "只統計能選到這件的箱子；需求未齊就保留箱子，不先拿替代品。",
                     "解鎖一件後放進已開空槽；不把史詩紅星當成傳奇，再回本站更新持有與擺入數。"]
    elif sid.startswith("adv"):
        number = sid[3]
        entry = f"自訂收藏館 → 第{number}套的進階欄位"
        if sid.endswith("_rearrange"):
            steps = [f"只使用第{number}套已持有、已填入的收藏，查看哪幾格已進階。",
                     "把這套較高星收藏移入已進階格，不增加開格數，也不借另一套的同一件。",
                     "確認對應星數詞條亮起；重新擺好就停，回本站更新擺放順序。"]
        elif sid.endswith("_stars") or status in ("星數未達", "資料未齊"):
            steps = [f"逐件記錄第{number}套的收藏星級；黃5記5，紅5記10，未持有明確記0。",
                     "先把高星收藏放入已進階格。若仍不足，再補適用收藏的下一個星數缺口；未填資料先補資料。",
                     "這一步先不買進階格；顯示目標星數與件數一起達標後再比較。"]
        else:
            steps = ["查看這一個目標格的遊戲報價，不用另一套或上一格的價格。",
                     "確認目標格數、放入收藏累計星數和高級收藏之心三項都達標，才進階這一格。",
                     "詞條亮起就停；回本站更新格數，下一格價格重新核對。普通收藏之心不能代替高級。"]
    elif sid in ("memory", "dark_matter", "boots_set"):
        entry = "收藏館 → 目標收藏／套裝成員的升星預覽"
        if sid == "boots_set":
            steps = [f"只補這些未黃3成員：{step.get('current') or '先查看四件星級'}。",
                     "逐件合計到黃3的缺額與可選期數；已黃3或更高的成員不追加。",
                     "四件都黃3且鞋子對應冰甲技能已啟用才算生效；部分完成只更新實際星級，不記整組完成。"]
        else:
            name = "記憶編輯器" if sid == "memory" else "暗物質傀儡"
            steps = [f"選「{name}」，把升星預覽切到本次目標「{step['target']}」，合計從目前星級到這一檔的缺額。",
                     "打開自選清單，只用能選到這件的期數與碎片；材料不足先保留，不平均分給多件。",
                     ("確認仍使用破壞者徽記及所需血量條件；目標星級達到就停。" if sid == "memory" else
                      "確認使用普通／雙生無人機；目標星級達到就停，另查四件套是否生效。")]
    elif sid == "lance_e1":
        entry = "雙絕槍裝備的神鑄頁 → 永恆路線"
        steps = ["選永恆1階，不把虛空／混沌／異星路線當成E1。",
                 "核對1神器核心、對應S裝及其他材料；未齊先保留，別拆仍在使用的裝備硬湊。",
                 "完整材料齊才完成E1；回本站更新永恆神鑄，不連續投入E2。"]
    elif sid == "twin_drone":
        entry = "科技配件 → 配件合成 → 雙生配件 → 雙生合體"
        steps = ["在配方選精確制導系統（無人機）＋能量收集器（力場），先看兩件實際品質。",
                 "紅力場不足先補紅力場；已有兩件仍需核對合成預覽和投入後諧振是否受影響。",
                 "完整配方齊才合成，使用無人機態並在局內進化對應技能；回本站記錄雙生已完成。"]
    elif sid == "zone":
        entry = "目前區域行動的局內路線／技能選擇"
        steps = ["先讀本期規則，確認哪些局外養成會帶入，不先套用末世材料順位。",
                 "記錄失敗原因：生存不足、首領傷害不足或技能未成形；下一次只改一項。",
                 "先取得本局可用Buff與技能，再試首領；這條路線不推薦花覺醒核心。"]
    elif sid == "survival_check":
        entry = "目前卡住的同一關卡 → 戰鬥過程與結算"
        steps = ["保持同一關卡與現役配置，記錄死亡時間、死因及主力技能何時成形；不要同時改多個系統。",
                 "分辨瞬間受傷、持續受傷或技能尚未成形；先比較已持有的技能、走位與防護配置，不拆裝備硬湊。",
                 "只改一項再試，能穩定存活後更新目前問題；尚未確認死因前保留輸出養成材料。"]
    elif sid == "pet_skills":
        entry = "寵物 → 主戰寵出戰技能 → 助戰寵技能"
        steps = ["先查看已解鎖技能：普通輸出寵比較寵物傷害，主人增益／異世寵核對主人有效增益。",
                 "把符合主戰方向的已解鎖技能裝入可用槽位；沒有解鎖的技能先記缺項，不購買、不盲抽補齊。",
                 "用同模式結算確認主戰效果，再記錄配置已核對；這是配置檢查，不是完成覺醒。"]
    elif sid in ("pet_node", "pet_umbral"):
        entry = "寵物 → 本次主戰寵的覺醒／共鳴預覽"
        steps = [f"選你核對的「{step['target']}」，核對本階解鎖效果；只有面板時先不追加。",
                 "合計本節點全部本體、碎片、核心與其他材料；普通與異世寵物不可套用同一配方。",
                 "材料整段備妥才完成這一階，確認技能／共鳴已生效；回本站更新下一個節點，不連續追加。"]
    else:
        entry = "本次目標的遊戲升級預覽"
        steps = ["查看本次目標與完整需求，不套用另一條路線的價格。",
                 "只補上方已知缺額；未知條件保持未確認。",
                 "完整條件齊才操作，完成後重新排序。"]
    return {"entry": entry, "steps": steps}
