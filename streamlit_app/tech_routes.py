"""Selected skill breakpoints from dated source tables, not a global DPS rank."""
TECH_ROUTES = {
    "雙生無人機（無人機態）": {
        "name": "能量制導系統（無人機態）", "date": "2025-05-03",
        "source": "https://notalknote.xyz/【噠噠特攻】雙生配件-能量制導系統（無人機態）/",
        "milestones": [
            (200, "毀滅力場附加15%易傷，持續1秒"),
            (300, "力場施加衰弱，持續1秒；對衰弱傷害＋20%"),
            (600, "飛彈數量＋10%、技能傷害＋25%、對衰弱傷害＋20%"),
            (900, "單發傷害＋30%；力場額外附加15%易傷"),
            (1650, "飛彈數量＋10%、技能傷害＋15%"),
            (2100, "力場易傷持續5秒、易傷效果＋15%"),
            (3000, "單發傷害＋30%、技能傷害＋15%"),
            (4500, "飛彈數量＋5%"),
        ],
    },
    "雙生雷電（雷電態）": {
        "name": "相位輔助器（雷電態）", "date": "2025-11-03",
        "source": "https://notalknote.xyz/twinborn-tech-phase-driver-lightning-mode/",
        "milestones": [
            (200, "暴擊傷害＋40%"),
            (450, "技能傷害＋40%"),
            (600, "8道落雷後，之後4道落雷傷害＋36%"),
            (900, "被旋轉雷暴場傷害過的敵人附加50%易傷"),
            (1650, "技能傷害＋30%"),
            (2550, "暴擊傷害＋30%"),
            (3000, "雙生渦旋狂雷傷害＋5%"),
            (4500, "被旋轉雷暴場傷害過的敵人附加30%易傷"),
        ],
    },
}


def next_tech_effect(part: str | None, energy: int | None, confirmed: bool = False) -> dict:
    """Next selected effect, not the next arbitrary stat or proven best DPS."""
    route = TECH_ROUTES.get(part)
    if route is None or energy is None:
        return {"state": "unknown", "message": "選雙生形態並填目前能量，才會列出對應效果；普通配件不能套用。"}
    if type(energy) is not int or energy < 0:
        return {"state": "invalid", "message": "能量請填非負整數。"}
    next_row = next(((target, effect) for target, effect in route["milestones"] if target > energy), None)
    if next_row is None:
        return {"state": "outside", "message": "已到本表最高收錄門檻，不代表畢業。更高檔請查該形態的遊戲效果，暫不自動推薦。"}
    target, effect = next_row
    return {"state": "candidate" if confirmed else "verify", "target": target, "effect": effect,
            "gap": target-energy, "message": f"下一個已收錄技能效果：{target:,}；還差 {target-energy:,} 能量。",
            "action": (f"在科技配件選「{route['name']}」，預覽支援替換／晶片投入，把能量補至 {target:,}；到這檔先停。"
                       if confirmed else f"先對照遊戲中的「{route['name']}」{target:,}效果；一致後才規劃投入。"),
            "stop": "不得拆掉另一件現役配件的重要門檻；表內增傷不是整場總傷害增幅。"}


TECH_GUIDE = {
    "slug": "twin-tech-milestones", "category": "科技配件", "title": "雙生無人機／雷電諧振：下一檔效果與實際操作",
    "summary": "無人機3000、雷電1600如何安排？查雙生形態的門檻與觸發條件，直接看能量缺口。",
    "audience": "已使用紅品質以上雙生無人機或雙生雷電的玩家", "resource": None,
    "verdict": "若是雙生相位輔助器雷電態，1600→1650還差50能量，來源列技能傷害＋30%；先比較能否保留現役無人機門檻而補到這一檔。這是近距離候選，不是已證明勝過所有其他投入。普通雷電不能套用。",
    "source_date": "2025-11-03", "checked": "2026-10-02", "status": "雙生效果表已讀取 · 版本需對照",
    "sources": [("別說筆記｜雙生無人機（2025-05-03）", TECH_ROUTES["雙生無人機（無人機態）"]["source"]),
                ("別說筆記｜雙生雷電（2025-11-03）", TECH_ROUTES["雙生雷電（雷電態）"]["source"])],
    "editorial_note": "核對日期代表本次讀取來源，不代表遊戲未改版。下表選錄技能／暴傷／易傷節點，未收錄所有面板檔；不是完整上限或固定優先排行。",
    "sections": [
        {"title": "雙生無人機：能量制導系統（無人機態）", "columns": ["能量", "該檔來源效果"],
         "rows": [[str(n), effect] for n, effect in TECH_ROUTES["雙生無人機（無人機態）"]["milestones"]]},
        {"title": "雙生雷電：相位輔助器（雷電態）", "columns": ["能量", "該檔來源效果"],
         "rows": [[str(n), effect] for n, effect in TECH_ROUTES["雙生雷電（雷電態）"]["milestones"]]},
        {"title": "無人機3000、雷電1600：這樣做", "steps": [
            "先確認兩件全名與形態。只有雙生雷電態才用這裡的1650效果。",
            "選雷電的諧振頁，預覽換入支援或增加晶片後的能量；這一個候選只差50，不直接追3000。",
            "若要搬無人機的支援，先看搬出後是否低於3000；會掉現役效果就先取消，不把失去收益算零。",
            "預覽顯示材料可完成、效果文字一致，才選擇投入。達1650後先停，固定首領與時長比較，再安排更高檔。"]},
        {"title": "效果為什麼不一定全程生效", "columns": ["效果", "實際要做"], "rows": [
            ["無人機毀滅力場的易傷／衰弱", "在該配件對應技能生效時，讓目標落在力場範圍；不能把範圍外當作有覆蓋"],
            ["雷電900／4500易傷", "局內使用並進化對應雙生雷電，讓旋轉雷暴場命中目標"],
            ["技能傷害／暴擊傷害詞條", "分開記錄，不將兩個百分比相加成總DPS"]]},
    ],
    "caution": "來源為2025年效果表，需對照目前遊戲。缺支援庫存、晶片成本與傷害占比時，只能給近距離候選，不能證明全帳號最優。合成後的形態、局內超武與條件覆蓋不可省略。",
    "faq": [("無人機3000就不能再升？", "可以再比較；本表下一個選錄技能節點是4500飛彈數量＋5%，不是下一個所有屬性檔。這1500能量是否值得，要算完整成本。"),
            ("雷電1600一定先到1650？", "只有在雙生雷電態、遊戲效果一致、成本可達且不犧牲主力效果時，才列為近距離候選。普通雷電或不同模式需另看。")],
    "related": ["resonance-planning", "twin-drone", "red-choice-box", "survivor-awakening"],
    "keywords": "雙生無人機3000 雙生雷電1600 雷電1650 能量制導系統 相位輔助器 雷暴場 毀滅力場 諧振 門檻 技能傷害 易傷 衰弱",
}
