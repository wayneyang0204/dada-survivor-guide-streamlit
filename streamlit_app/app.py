from __future__ import annotations

import html
import json
from datetime import datetime
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import streamlit as st

from data_engine import (
    assess_event_plan,
    diagnose_account,
    fetch_source_posts,
    load_collectible_catalog,
    match_event_playbook,
    rank_rewards,
)


st.set_page_config(
    page_title="噠噠特攻終局攻略",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

來源分類網址 = "https://notalknote.xyz/moblegame/survivorio/"
來源介面網址 = (
    "https://notalknote.xyz/wp-json/wp/v2/posts"
    "?categories=624&per_page=6&_fields=link,title,date"
)

攻略資料 = [
    {
        "分類": "最新系統",
        "標題": "新版區域行動：四大區域與首領戰",
        "日期": "2026/08/27",
        "狀態": "現行",
        "摘要": "先看區域限制，再決定裝備與技能；通關後強化區域效果，最後投入首領戰。",
        "行動": ["先讀區域限制", "普通關卡優先拿強化", "首領戰再換純輸出配置"],
        "來源": "https://notalknote.xyz/dadasurvivor-regional-action-update-guide/",
    },
    {
        "分類": "特工寵物",
        "標題": "幽暗之靈：終局主戰寵物判斷",
        "日期": "2026/08/22",
        "狀態": "現行",
        "摘要": "核心是增傷效果與主人輸出，不要只比較寵物自己的面板傷害。",
        "行動": ["確認核心數量", "比較整體輸出", "轉換前保留回復配置"],
        "來源": "https://notalknote.xyz/survivor-io-umbral-soul-pet-guide-2026/",
    },
    {
        "分類": "收藏系統",
        "標題": "第十期收藏品：升星與選擇箱順序",
        "日期": "2026/03/07",
        "狀態": "現行",
        "摘要": "選擇箱應先補套裝啟動缺口，再補高價值三星收藏，最後追主力技能五星。",
        "行動": ["先啟動套裝", "再補三星效果", "最後集中主力技能"],
        "來源": "https://notalknote.xyz/10th-edition-collectibles/",
    },
    {
        "分類": "收藏系統",
        "標題": "傳奇收藏解構機：重置前檢查",
        "日期": "2026/04/08",
        "狀態": "現行",
        "摘要": "解構是重新分配稀缺資源的工具，使用前必須核對套裝、共鳴與自訂典藏館。",
        "行動": ["盤點目前套裝", "算出目標斷點", "確認收益後再解構"],
        "來源": "https://notalknote.xyz/survivor-io-legend-deconstructor-explained/",
    },
    {
        "分類": "收藏系統",
        "標題": "自訂典藏館：槽位、星數與終局收益",
        "日期": "2026/03/08",
        "狀態": "現行",
        "摘要": "傳奇收藏可提供暴擊傷害、技能傷害與異常增傷；先開有效槽位再追高星。",
        "行動": ["至少放入可計分收藏", "優先傳奇星數斷點", "不要為提早開槽大量分解"],
        "來源": "https://notalknote.xyz/custom-collection/",
    },
    {
        "分類": "收藏系統",
        "標題": "收藏套裝：先看下一個效果",
        "日期": "2025/05/23",
        "狀態": "常駐",
        "摘要": "選擇箱應投給最接近啟動下一個高價值套裝效果的收藏，而不是只看稀有度。",
        "行動": ["標出未啟動套裝", "計算差幾件", "優先最近的有效斷點"],
        "來源": "https://notalknote.xyz/collectible-sets/",
    },
    {
        "分類": "科技配件",
        "標題": "科技配件總覽：三攻三防與升級路線",
        "日期": "2025/02/21",
        "狀態": "常駐",
        "摘要": "一次配置三個攻擊與三個防禦配件，資源應集中在主力配件與下一個合成斷點。",
        "行動": ["攻擊欄服務主輸出", "防禦欄補生存缺口", "不要平均升級"],
        "來源": "https://notalknote.xyz/techparts/",
    },
    {
        "分類": "科技配件",
        "標題": "科技諧振：主配件與輔助配件",
        "日期": "2024/10/31",
        "狀態": "需版本核對",
        "摘要": "保留主配件搭配低稀有度輔助配件的機制，但實際開放順序需以目前遊戲為準。",
        "行動": ["確認已開啟諧振", "輔助配件先看諧振量", "逐一比較實戰傷害"],
        "來源": "https://notalknote.xyz/tech-parts-resonance/",
    },
    {
        "分類": "科技配件",
        "標題": "雙生配件：合成前先決定模式",
        "日期": "2025/02/21",
        "狀態": "常駐",
        "摘要": "傳奇配件可進入雙生系統，合成前先確定首領、清怪或生存用途。",
        "行動": ["先選主要模式", "確認不會拆掉現役配件", "同步調整收藏與套裝"],
        "來源": "https://notalknote.xyz/twinborn-parts/",
    },
    {
        "分類": "最新系統",
        "標題": "載具系統：屬性、技能與投資順序",
        "日期": "2026/04/25",
        "狀態": "現行",
        "摘要": "載具是獨立養成線，先投資能跨模式生效的核心與技能斷點。",
        "行動": ["確認適用模式", "先升泛用斷點", "與角色及寵物一起比較"],
        "來源": "https://notalknote.xyz/survivorio-mount-system-ultimate-guide/",
    },
    {
        "分類": "裝備養成",
        "標題": "星鑄腰帶與扭曲腰帶：何時更換",
        "日期": "2026/03/09",
        "狀態": "現行",
        "摘要": "裝備價值取決於核心與模式；新腰帶未達斷點時，成熟舊腰帶可能更穩定。",
        "行動": ["按核心數比較", "分開測首領與區域", "達斷點前保留舊裝"],
        "來源": "https://notalknote.xyz/survivor-io-twisting-belt-vs-ss-belt-meta-guide/",
    },
    {
        "分類": "裝備養成",
        "標題": "混沌融合：終局裝備資源分配",
        "日期": "2025/04/13",
        "狀態": "常駐",
        "摘要": "把融合材料集中在能立刻跨過斷點的核心裝備，不要平均分配。",
        "行動": ["列出下一斷點", "優先主模式裝備", "保留轉換材料"],
        "來源": "https://notalknote.xyz/chaos-fusion/",
    },
    {
        "分類": "裝備養成",
        "標題": "星鑄消耗：升級前材料清單",
        "日期": "2025/04/13",
        "狀態": "常駐",
        "摘要": "先列出每階核心與材料來源，只投資能直接取得實戰效果的節點。",
        "行動": ["盤點核心存量", "記錄下一個有效節點", "保留自選箱與回退資源"],
        "來源": "https://notalknote.xyz/%e3%80%90%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e3%80%91%e7%a5%9e%e9%91%84%e6%b6%88%e8%80%97/",
    },
    {
        "分類": "特工寵物",
        "標題": "特工覺醒：核心、碎片與連攜技能",
        "日期": "2026/01/24",
        "狀態": "常駐",
        "摘要": "覺醒需要角色碎片、量子碎片與覺醒核心，先完成主力再補連攜角色。",
        "行動": ["先覺醒主力", "第二順位看連攜收益", "不要把核心平均分散"],
        "來源": "https://notalknote.xyz/survivor-awakening/",
    },
    {
        "分類": "特工寵物",
        "標題": "特工同調與協同作戰",
        "日期": "2025/08/01",
        "狀態": "需版本核對",
        "摘要": "同調會統一部分基礎等級並開放協同位，解鎖條件與配置需依現行版本核對。",
        "行動": ["確認同調門檻", "按被動技能選協同", "升級前盤點精華與核心"],
        "來源": "https://notalknote.xyz/survivor-synergy-system/",
    },
    {
        "分類": "特工寵物",
        "標題": "寵物技能、覺醒與助戰配置",
        "日期": "2025/08/20",
        "狀態": "需版本核對",
        "摘要": "舊寵物排行只能當過渡參考，終局需重新比較主人增傷、助戰與新寵物。",
        "行動": ["分清主戰與助戰", "助戰技能服務主寵", "用整體傷害決定"],
        "來源": "https://notalknote.xyz/survivoriopet-system/",
    },
    {
        "分類": "特工寵物",
        "標題": "全部角色能力與取得方式",
        "日期": "2026/01/24",
        "狀態": "需版本核對",
        "摘要": "角色強度會隨覺醒與同調改變，舊排行只適合查取得與技能，不直接當終局答案。",
        "行動": ["查取得與碎片", "再看覺醒及同調", "以現行模式實測"],
        "來源": "https://notalknote.xyz/%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e6%96%b0%e8%a7%92%e8%89%b2/",
    },
    {
        "分類": "關卡活動",
        "標題": "技能等級與突破合成速查",
        "日期": "2024/08/20",
        "狀態": "需版本核對",
        "摘要": "用來查主動與被動技能的突破組合；新技能仍要以當期版本確認。",
        "行動": ["開局前記住主力被動", "保留一格給必要輔助", "新技能以當期圖鑑為準"],
        "來源": "https://notalknote.xyz/%e3%80%90%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e3%80%91%e6%8a%80%e8%83%bd%e7%ad%89%e7%b4%9a%e5%8f%8a%e7%aa%81%e7%a0%b4%e5%90%88%e6%88%90%e8%a1%a8/",
    },
    {
        "分類": "關卡活動",
        "標題": "第一百二十六關以後的關卡入口",
        "日期": "2024/05/18",
        "狀態": "需版本核對",
        "摘要": "舊文章適合查特定關卡地圖與怪物，裝備及技能建議應套用現行系統。",
        "行動": ["先按關卡編號搜尋", "只採地圖與怪物資訊", "配裝使用目前終局配置"],
        "來源": "https://notalknote.xyz/%e3%80%90%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e3%80%91%e9%80%9a%e9%97%9c%e6%94%bb%e7%95%a5%e7%ac%ac126%e9%97%9c/",
    },
]

終局配置 = [
    {
        "名稱": "短時首領爆發天花板",
        "適用": "末世反響／公會遠征／短場首領",
        "角色": "維納托覺醒5以上主位｜塔洛莎覺醒4協同｜哪吒覺醒2 → 伏爾坎覺醒1支援鏈",
        "寵物": "幽冥之魂覺醒3以上｜共鳴增益＋共鳴傷害",
        "武器": "雙生之槍｜永恆4、虛空4、混沌2以上、異界轉化",
        "裝備": ["虛空項鍊神鑄3／審判項鍊雙生階", "月痕護腕雙生階｜基礎暴率至少70%", "星塵腰帶雙生階 E3／V2", "冰川戰靴雙生階 E1／V2／C1", "永虛戰甲雙生階 E3起"],
        "技能": ["雙生槍", "雙生無人機", "燃燒瓶", "足球", "鑽頭", "雷電"],
        "核心": "以最快進化與首領增傷為核心；短場先確保雙生槍永恆1，技能格優先無人機與冷卻。",
        "斷點": "基礎暴率70～100%、雙生槍至少永恆1＋虛空2；未達時神鑄3虛空手套通常更強。",
        "評分": {"清怪": 84, "首領": 100, "生存": 82},
    },
    {
        "名稱": "長戰疊層傷害極限",
        "適用": "長線首領／完整疊層場景",
        "角色": "維納托覺醒5～7主位｜塔洛莎覺醒4＋梅塔莉亞／楊大師覺醒1協同",
        "寵物": "幽冥之魂｜保護＋共鳴增益＋共鳴傷害",
        "武器": "雙生之槍｜永恆4、虛空4；混沌之力9／18為重算點",
        "裝備": ["審判項鍊雙生階／虛空項鍊神鑄3", "月痕護腕雙生階 E1／V2以上", "星塵腰帶雙生階；收藏滿門檻才測扭曲腰帶", "冰川戰靴雙生階 E1／V2／C1", "永虛戰甲雙生階 E3／V2／C2"],
        "技能": ["雙生槍", "雙生無人機", "燃油桶", "量子球", "永恆鑽頭", "超級雷暴"],
        "核心": "讓混沌之力與寵物共鳴完整疊滿；燃燒、虛弱與冰凍觸發需配合異界轉化詞條。",
        "斷點": "混沌之力9起跳、永虛甲至少永恆3；混沌之力18後再重算腰帶與項鍊。",
        "評分": {"清怪": 88, "首領": 99, "生存": 90},
    },
    {
        "名稱": "區域行動零失誤配置",
        "適用": "區域行動／341～345章／極端詞條",
        "角色": "塔洛莎覺醒5穩定主位／維納托覺醒5高投入；詞條關再調整梅塔莉亞協同",
        "寵物": "幽冥之魂／高星控制型異獸",
        "武器": "雙生之槍 E4／V4；特殊詞條關可切虛空之力",
        "裝備": ["虛空項鍊神鑄3", "月痕護腕雙生階／虛空手套神鑄3", "星塵腰帶雙生階 E3／V2", "冰川戰靴雙生階 E1／V2／C1", "亡者風衣神鑄3／永虛甲雙生階 E3"],
        "技能": ["雙生無人機", "燃油桶", "守衛者", "量子球", "力場", "高爆燃料"],
        "核心": "不是堆面板，而是針對詞條保證通關；極端怪潮用死神流，禁復活關改永虛甲。",
        "斷點": "亡者風衣必須神鑄3才值得當核心；禁復活或限制護盾時必須依詞條切換。",
        "評分": {"清怪": 100, "首領": 90, "生存": 98},
    },
]

收藏優先順序 = [
    "先啟動能立即生效的收藏套裝",
    "再補主力技能與終局裝備對應收藏",
    "傳奇收藏優先暴擊傷害、技能傷害與異常增傷斷點",
    "自選箱留給差一件或差一星就能跨過的斷點",
    "解構前確認套裝、共鳴與自訂典藏館不會退級",
]


@st.cache_data(ttl=900, show_spinner=False)
def 取得最新文章() -> tuple[list[dict[str, str]], bool]:
    try:
        request = Request(來源介面網址, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=8) as response:
            posts = json.loads(response.read().decode("utf-8"))
        items = []
        for post in posts:
            title = html.unescape(post["title"]["rendered"])
            title = title.replace("【噠噠特攻】", "").strip()
            items.append(
                {
                    "標題": title,
                    "日期": post["date"][:10].replace("-", "/"),
                    "網址": post["link"],
                }
            )
        return items, True
    except Exception:
        return [
            {
                "標題": "四週年活動總結與資源投入心得",
                "日期": "2026/08/28",
                "網址": "https://notalknote.xyz/dadasurvivor-4th-anniversary-event-review/",
            },
            {
                "標題": "區域行動全新改版攻略",
                "日期": "2026/08/27",
                "網址": "https://notalknote.xyz/dadasurvivor-regional-action-update-guide/",
            },
            {
                "標題": "幽暗之靈完整解析",
                "日期": "2026/08/22",
                "網址": "https://notalknote.xyz/survivor-io-umbral-soul-pet-guide-2026/",
            },
        ], False


@st.cache_data(ttl=900, show_spinner=False)
def 取得完整文章庫() -> tuple[list[dict], bool]:
    try:
        return fetch_source_posts(), True
    except Exception:
        return [], False


@st.cache_data(show_spinner=False)
def 取得收藏圖鑑() -> list[dict]:
    return load_collectible_catalog()


官方版本資訊 = {
    "版本": "5.1.0",
    "查核": "2026/08/31",
    "標題": "四週年慶典與主線 341～345 章",
    "重點": ["主線 341～345 章與挑戰章節", "音樂圓盤與彩虹骰活動", "足球模式共鳴超載預告", "料理主題活動預告"],
}


def 切換主頁面(主要: str, 次要: str | None = None) -> None:
    st.session_state["主導覽"] = 主要
    if 主要 == "養成" and 次要:
        st.session_state["養成分類"] = 次要
    if 主要 == "資料庫" and 次要:
        st.session_state["資料分類"] = 次要


def 顯示攻略卡片(item: dict) -> None:
    狀態色 = {"現行": "#5f860b", "常駐": "#187178", "需版本核對": "#a85a08"}[item["狀態"]]
    st.markdown(
        f"""
        <div class="攻略卡">
          <div class="卡片頂列">
            <span class="分類">{item['分類']}</span>
            <span class="狀態" style="color:{狀態色};border-color:{狀態色}55;background:{狀態色}12">{item['狀態']}</span>
          </div>
          <h3>{item['標題']}</h3>
          <p>{item['摘要']}</p>
          <div class="更新日">資料更新：{item['日期']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("你現在該做什麼"):
        for action in item["行動"]:
            st.markdown(f"- {action}")
        st.link_button("核對原始文章", item["來源"], width="stretch")


def 取得活動重點(活動模型: dict) -> list[tuple[str, str]]:
    if 活動模型.get("highlights"):
        return [(str(label), str(content)) for label, content in 活動模型["highlights"]]

    目標 = int(活動模型.get("target", 0))
    單位 = str(活動模型.get("unit", "活動進度"))
    推薦進度 = f"先以 {目標:,} {單位}作為主要停損點，達標後先停手。" if 目標 > 0 else "先做完免費任務，最後一天再依獎勵價值決定是否補差額。"
    步驟 = [str(step) for step in 活動模型.get("steps", [])]
    操作順序 = " → ".join(步驟[:2]) if 步驟 else "先拿免費資源，再比較目標缺口。"
    收尾策略 = 步驟[-1] if 步驟 else str(活動模型.get("avoid", "達標後停手。"))
    return [
        ("免費資源", str(活動模型.get("free_hint", "先完成所有免費任務。"))),
        ("推薦進度", 推薦進度),
        ("操作順序", 操作順序),
        ("收尾策略", 收尾策略),
    ]


def 取得活動重點區塊(活動模型: dict) -> list[dict]:
    if 活動模型.get("summary_sections"):
        return list(活動模型["summary_sections"])
    return [
        {"title": label, "items": [("重點", content)]}
        for label, content in 取得活動重點(活動模型)
    ]


def 顯示活動重點(標題: str, 日期: str, 活動模型: dict, 狀態: str = "30 秒攻略") -> None:
    重點區塊 = ""
    for index, section in enumerate(取得活動重點區塊(活動模型), 1):
        條目 = "".join(
            f'<li><b>{html.escape(str(label))}：</b>{html.escape(str(content))}</li>'
            for label, content in section["items"]
        )
        重點區塊 += (
            f'<article class="速覽區塊"><div class="速覽區塊標題"><span class="速覽號">{index}</span>'
            f'<strong>{html.escape(str(section["title"]))}</strong></div><ul>{條目}</ul></article>'
        )
    標籤列 = "".join(f"<span>{html.escape(str(tag))}</span>" for tag in 活動模型.get("tags", []))
    時間文字 = f"活動時間：{活動模型['period']}" if 活動模型.get("period") else f"攻略更新：{日期}"
    結論 = str(
        活動模型.get("verdict")
        or (f"先把免費進度跑完，只補到 {int(活動模型['target']):,} {活動模型['unit']}。" if int(活動模型.get("target", 0)) > 0 else "先做完免費任務，最後一天再決定是否投入。")
    )
    st.markdown(
        f"""
        <section class="重點速覽">
          <div class="速覽頂列"><span class="速覽徽章">{html.escape(狀態)}</span><span>{html.escape(時間文字)}</span></div>
          <h3>{html.escape(標題)}</h3>
          <div class="速覽標籤列">{標籤列}</div>
          <p class="速覽結論"><b>結論</b>{html.escape(結論)}</p>
          <div class="速覽清單">{重點區塊}</div>
          <p class="速覽停損"><b>停損提醒</b>{html.escape(str(活動模型['avoid']))}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
      :root {
        color-scheme: light;
        --bg: #f7f9f5;
        --panel: #ffffff;
        --panel-2: #f0f6ee;
        --lime: #87b91c;
        --lime-strong: #739f12;
        --lime-soft: #e8f6c8;
        --ink: #173032;
        --muted: rgba(23, 48, 50, .68);
        --line: rgba(29, 73, 63, .14);
        --cyan: #227d82;
        --orange: #b86912;
      }
      html, body, [class*="css"] { font-family: Inter, "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif; }
      .stApp {
        color: var(--ink);
        background:
          radial-gradient(900px 520px at 8% 10%, rgba(151, 201, 61, .11), transparent 62%),
          radial-gradient(700px 420px at 92% 30%, rgba(73, 187, 181, .08), transparent 60%),
          var(--bg);
      }
      [data-testid="stHeader"] { height: 1.2rem; background: transparent; }
      [data-testid="stToolbar"], [data-testid="stDecoration"] { display:none; }
      [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
      [data-testid="stAppViewContainer"] > .main { overflow: visible; }
      .block-container { max-width: 1220px; padding: 1.1rem 2rem 4rem; }
      footer { display: none; }

      .頂導 { min-height: 3.2rem; display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:.25rem 0 .65rem; }
      .品牌 { display:flex; align-items:center; gap:.7rem; font-size:1rem; font-weight:950; letter-spacing:-.02em; }
      .品牌記號 { display:grid; place-items:center; width:2.2rem; height:2.2rem; border-radius:.8rem; color:#fff; background:var(--lime); box-shadow:0 10px 24px rgba(115,159,18,.22); }
      .同步徽章 { display:inline-flex; align-items:center; gap:.45rem; padding:.35rem .65rem; border:1px solid rgba(34,125,130,.18); border-radius:999px; background:#eef8f5; color:#246d70; font-size:.72rem; font-weight:850; }
      .同步點 { width:.42rem; height:.42rem; border-radius:50%; background:#2fb678; box-shadow:0 0 10px rgba(47,182,120,.35); }

      [data-testid="stRadio"] { position:sticky; top:.45rem; z-index:999; width:100%; }
      [data-testid="stRadio"] > div { width:100%; }
      div[role="radiogroup"] { display:flex; flex-wrap:wrap; gap:.35rem; width:100%; padding:.35rem; border:1px solid var(--line); border-radius:1rem; background:rgba(255,255,255,.92); box-shadow:0 12px 32px rgba(39,72,61,.08); }
      div[role="radiogroup"] label { flex:1 1 auto; min-width:max-content; justify-content:center; padding:.62rem .78rem; border-radius:.72rem; color:rgba(23,48,50,.65); font-size:.78rem; font-weight:850; cursor:pointer; transition:all .18s ease; }
      div[role="radiogroup"] label p { color:inherit !important; }
      div[role="radiogroup"] label:hover { color:var(--ink); background:#f0f5ee; }
      div[role="radiogroup"] label:has(input:checked) { color:#173032; background:#dff49e; box-shadow:0 8px 20px rgba(115,159,18,.12); }
      label[data-testid="stRadioOption"] > div > div > div:first-child { display:none; }

      .主視覺 { position:relative; overflow:hidden; margin:1rem 0 1.25rem; padding:1.45rem 1.7rem; border:1px solid rgba(83,131,63,.18); border-radius:1.4rem; background:linear-gradient(135deg, #ffffff, #f2f8e8 58%, #e9f4e1); box-shadow:0 16px 38px rgba(45,79,58,.08); }
      .主視覺::after { content:""; position:absolute; width:20rem; height:20rem; right:-7rem; top:-10rem; border-radius:50%; background:rgba(151,201,61,.16); filter:blur(24px); pointer-events:none; }
      .主標 { position:relative; z-index:1; font-size:clamp(1.85rem, 4vw, 3rem); line-height:1.06; font-weight:950; letter-spacing:-.05em; max-width:920px; margin:.25rem 0 .65rem; text-wrap:balance; }
      .主標 span { color:var(--lime); }
      .說明 { position:relative; z-index:1; margin:0; color:var(--muted); max-width:820px; line-height:1.75; font-size:.95rem; font-weight:560; }
      .小標 { position:relative; z-index:1; color:var(--lime); font-size:.72rem; font-weight:950; letter-spacing:.16em; text-transform:uppercase; }
      .主視覺徽章 { display:inline-flex; margin-top:.8rem; padding:.34rem .62rem; border:1px solid rgba(115,159,18,.22); border-radius:999px; background:#edf7d8; color:#557d08; font-size:.68rem; font-weight:850; }
      [data-testid="stImage"] { height:100%; margin:1rem 0 1.25rem; }
      [data-testid="stImage"] img { width:100%; height:100%; min-height:220px; max-height:245px; object-fit:cover; object-position:68% center; border:1px solid rgba(29,73,63,.14); border-radius:1.4rem; box-shadow:0 16px 38px rgba(45,79,58,.1); }
      .信任列 { display:flex; flex-wrap:wrap; gap:.45rem; margin:-.35rem 0 1.1rem; }
      .信任列 span { display:inline-flex; align-items:center; gap:.35rem; padding:.38rem .62rem; border:1px solid var(--line); border-radius:999px; background:#fff; color:rgba(23,48,50,.64); font-size:.68rem; font-weight:820; }
      .信任列 b { color:#557d08; }

      .重點速覽 { padding:1.3rem 1.4rem; border:1px solid rgba(115,159,18,.24); border-radius:1.25rem; background:linear-gradient(145deg,#ffffff,#f5faec); box-shadow:0 12px 30px rgba(39,72,61,.06); }
      .速覽頂列 { display:flex; align-items:center; justify-content:space-between; gap:.8rem; color:rgba(23,48,50,.5); font-size:.68rem; font-weight:800; }
      .速覽徽章 { padding:.28rem .55rem; border-radius:999px; background:var(--lime); color:#fff; letter-spacing:.08em; }
      .重點速覽 h3 { margin:.65rem 0 .7rem; font-size:clamp(1.15rem,2.5vw,1.55rem); line-height:1.38; }
      .速覽標籤列 { display:flex; flex-wrap:wrap; gap:.35rem; margin:-.2rem 0 .8rem; }
      .速覽標籤列 span { padding:.28rem .5rem; border-radius:999px; background:#eef8f5; color:#227d82; font-size:.66rem; font-weight:850; }
      .速覽結論 { display:flex; gap:.65rem; align-items:flex-start; margin:0 0 .9rem; padding:.75rem .85rem; border-radius:.8rem; background:#edf7d8; color:#31530e; font-size:.86rem; line-height:1.55; }
      .速覽結論 b, .速覽停損 b { flex:0 0 auto; color:#557d08; }
      .速覽清單 { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.65rem; }
      .速覽區塊 { min-height:12rem; padding:.95rem 1rem; border:1px solid rgba(34,125,130,.2); border-radius:.95rem; background:#fff; box-shadow:0 8px 20px rgba(39,72,61,.035); }
      .速覽區塊:nth-child(2) { border-color:rgba(184,105,18,.24); }
      .速覽區塊:nth-child(3) { border-color:rgba(115,159,18,.28); }
      .速覽區塊:nth-child(4) { border-color:rgba(164,68,127,.22); }
      .速覽區塊標題 { display:flex; gap:.6rem; align-items:center; margin-bottom:.55rem; }
      .速覽區塊標題 strong { color:var(--ink); font-size:.88rem; }
      .速覽號 { display:grid; place-items:center; width:1.55rem; height:1.55rem; border-radius:.5rem; background:#227d82; color:#fff; font-size:.72rem; font-weight:950; box-shadow:0 7px 14px rgba(34,125,130,.16); }
      .速覽區塊:nth-child(2) .速覽號 { background:#b86912; }
      .速覽區塊:nth-child(3) .速覽號 { background:#739f12; }
      .速覽區塊:nth-child(4) .速覽號 { background:#9e467e; }
      .速覽區塊 ul { margin:0; padding-left:1.1rem; }
      .速覽區塊 li { margin:.36rem 0; color:rgba(23,48,50,.69); font-size:.78rem; line-height:1.58; }
      .速覽區塊 li::marker { color:var(--lime); }
      .速覽區塊 li b { color:var(--ink); font-weight:900; }
      .速覽停損 { display:flex; gap:.65rem; margin:.8rem 0 0; padding-top:.8rem; border-top:1px solid var(--line); color:#8a510f; font-size:.76rem; line-height:1.5; }
      .速覽停損 b { color:#a65c0b; }
      .快捷格 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.75rem; margin:.65rem 0 1.2rem; }
      .快捷卡 { min-height:8.4rem; padding:1rem 1.05rem; border:1px solid var(--line); border-radius:1rem; background:#ffffff; box-shadow:0 9px 24px rgba(39,72,61,.045); }
      .快捷卡 strong { display:block; margin:.25rem 0 .45rem; color:var(--ink); font-size:1.02rem; }
      .快捷卡 p { margin:0; font-size:.78rem; line-height:1.55; }
      .快捷編號 { color:var(--lime); font-size:.66rem; font-weight:950; letter-spacing:.1em; }

      .診斷結論 { padding:1.3rem 1.4rem; border:1px solid rgba(34,125,130,.22); border-radius:1.2rem; background:linear-gradient(135deg,#eef8f5,#ffffff); box-shadow:0 12px 30px rgba(39,72,61,.06); }
      .診斷標籤 { color:#227d82; font-size:.68rem; font-weight:950; letter-spacing:.11em; }
      .診斷結論 h3 { margin:.4rem 0 .45rem; font-size:1.45rem; }
      .診斷結論 p { margin:0; max-width:900px; font-size:.86rem; line-height:1.65; }
      .優先格 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.65rem; margin:.8rem 0; }
      .優先項 { padding:1rem; border:1px solid var(--line); border-radius:1rem; background:#fff; box-shadow:0 8px 20px rgba(39,72,61,.04); }
      .優先項 small { color:var(--lime); font-size:.65rem; font-weight:950; letter-spacing:.08em; }
      .優先項 strong { display:block; margin:.32rem 0 .38rem; color:var(--ink); font-size:.92rem; }
      .優先項 p { margin:0; font-size:.76rem; line-height:1.55; }
      .建議框 { display:grid; grid-template-columns:1fr 1fr; gap:.65rem; margin:.7rem 0 1rem; }
      .建議框 > div { padding:.9rem 1rem; border-radius:.9rem; background:#f3f8ed; color:rgba(23,48,50,.74); font-size:.78rem; line-height:1.55; }
      .建議框 > div:last-child { background:#fff5e8; color:#7c470f; }
      .建議框 b { display:block; margin-bottom:.25rem; color:var(--ink); }

      .配置總覽 { min-height:14rem; padding:1.05rem; border:1px solid var(--line); border-radius:1rem; background:#fff; box-shadow:0 9px 24px rgba(39,72,61,.045); }
      .配置總覽 small { color:#227d82; font-weight:850; }
      .配置總覽 h3 { margin:.45rem 0 .55rem; font-size:1rem; }
      .配置總覽 p { font-size:.76rem; line-height:1.55; }
      .評分列 { display:grid; grid-template-columns:repeat(3,1fr); gap:.35rem; margin-top:.8rem; }
      .評分 { padding:.5rem .35rem; border-radius:.65rem; background:#f2f7ef; text-align:center; }
      .評分 b { display:block; color:var(--ink); font-size:.92rem; }
      .評分 span { color:rgba(23,48,50,.5); font-size:.62rem; font-weight:800; }
      .配置詳情 { padding:1.15rem 1.25rem; border:1px solid rgba(115,159,18,.22); border-radius:1rem; background:#f7fbea; }
      .配置詳情 p, .配置詳情 li { font-size:.8rem; line-height:1.6; }
      .配置詳情 b { color:var(--ink); }
      .版本卡 { padding:1.1rem 1.2rem; border:1px solid rgba(34,125,130,.18); border-radius:1rem; background:linear-gradient(135deg,#eef8f5,#fff); }
      .版本卡 h3 { margin:.35rem 0 .55rem; font-size:1.02rem; }
      .版本卡 ul { margin:.4rem 0 0; padding-left:1.15rem; }
      .版本卡 li { margin:.25rem 0; font-size:.76rem; line-height:1.5; }

      h1, h2, h3 { color:var(--ink) !important; letter-spacing:-.025em; }
      h2 { margin-top:1.25rem !important; font-size:clamp(1.65rem, 3vw, 2.35rem) !important; font-weight:950 !important; }
      h3 { font-weight:900 !important; }
      p, li { color:rgba(23,48,50,.75); }
      [data-testid="stCaptionContainer"] p { color:rgba(23,48,50,.56) !important; }

      .資料標籤 { position:relative; color:var(--lime); font-size:.7rem; font-weight:900; letter-spacing:.08em; }

      div[data-testid="stVerticalBlockBorderWrapper"] { border:1px solid var(--line) !important; border-radius:1.35rem !important; background:#ffffff !important; box-shadow:0 14px 34px rgba(39,72,61,.07); }
      div[data-testid="stMetric"] { min-height:6.1rem; border:1px solid var(--line); border-radius:1.05rem; padding:1rem 1.05rem; background:linear-gradient(145deg, #ffffff, #f5f8f3); box-shadow:0 8px 22px rgba(39,72,61,.045); }
      div[data-testid="stMetric"] [data-testid="stMetricLabel"] p { color:rgba(23,48,50,.56) !important; font-size:.72rem; font-weight:800; }
      div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:var(--ink); font-size:1.65rem; font-weight:950; letter-spacing:-.04em; }

      [data-baseweb="select"] > div, [data-baseweb="input"] > div, .stTextInput input, .stNumberInput input { min-height:2.85rem; color:var(--ink) !important; border:1px solid rgba(29,73,63,.18) !important; border-radius:.78rem !important; background:#ffffff !important; box-shadow:none !important; }
      [data-baseweb="select"] > div:hover, [data-baseweb="input"] > div:hover, .stTextInput input:hover { border-color:rgba(115,159,18,.48) !important; }
      [data-baseweb="select"] span, [data-baseweb="select"] svg, .stNumberInput button svg { color:rgba(23,48,50,.72) !important; fill:currentColor !important; }
      .react-aria-ComboBox > div[role="group"], .react-aria-NumberField > div[role="group"] { min-height:2.85rem; overflow:hidden; border:1px solid rgba(29,73,63,.18) !important; border-radius:.78rem !important; background:#ffffff !important; box-shadow:none !important; }
      .react-aria-ComboBox > div[role="group"]:focus-within, .react-aria-NumberField > div[role="group"]:focus-within { border-color:rgba(115,159,18,.58) !important; box-shadow:0 0 0 2px rgba(115,159,18,.1) !important; }
      .react-aria-ComboBox input[role="combobox"], .react-aria-NumberField input { color:var(--ink) !important; background:transparent !important; }
      input::placeholder { color:rgba(23,48,50,.42) !important; opacity:1 !important; }
      .react-aria-ComboBox button, .react-aria-NumberField button { color:rgba(23,48,50,.68) !important; background:transparent !important; }
      label[data-testid="stWidgetLabel"] p { color:rgba(23,48,50,.78) !important; font-size:.76rem; font-weight:800; }
      [data-baseweb="popover"], [role="listbox"] { color:var(--ink) !important; background:#ffffff !important; }

      .stButton > button, .stLinkButton > a { min-height:2.65rem; border-radius:.78rem; border-color:rgba(29,73,63,.18); background:#ffffff; color:var(--ink); font-weight:900; transition:transform .16s ease, border-color .16s ease, background .16s ease; }
      .stButton > button:hover, .stLinkButton > a:hover { transform:translateY(-1px); border-color:rgba(115,159,18,.5); color:#5d850a; }
      .stButton > button[kind="primary"] { border-color:var(--lime) !important; background:var(--lime) !important; color:#ffffff !important; box-shadow:0 12px 28px rgba(115,159,18,.18); }
      .stButton > button[kind="primary"]:hover { background:var(--lime-strong) !important; color:#ffffff !important; }

      [data-baseweb="tab-list"] { gap:.3rem; padding:.3rem; border:1px solid var(--line); border-radius:.9rem; background:#ffffff; }
      [data-baseweb="tab"] { height:2.7rem; border-radius:.65rem; color:rgba(23,48,50,.62); font-weight:850; }
      [aria-selected="true"][data-baseweb="tab"] { color:#173032 !important; background:#dff49e !important; }
      [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display:none; }

      [data-testid="stAlert"] { border:1px solid var(--line); border-radius:1rem; background:#ffffff; }
      [data-testid="stExpander"] { overflow:hidden; border:1px solid var(--line); border-radius:.9rem; background:#ffffff; }
      [data-testid="stDataFrame"] { overflow:hidden; border:1px solid var(--line); border-radius:1rem; }
      hr { border-color:var(--line) !important; }

      .攻略卡 { min-height:225px; padding:1.2rem; border:1px solid var(--line); border-radius:1.2rem; background:linear-gradient(145deg, #ffffff, #f7faf5); box-shadow:0 12px 28px rgba(39,72,61,.07); }
      .攻略卡 h3 { font-size:1.1rem; margin:.85rem 0 .55rem; }
      .攻略卡 p { color:var(--muted); line-height:1.65; font-size:.88rem; }
      .卡片頂列 { display:flex; justify-content:space-between; gap:.7rem; align-items:center; }
      .分類 { color:var(--lime); font-size:.72rem; font-weight:900; }
      .狀態 { border:1px solid; border-radius:999px; padding:.2rem .55rem; font-size:.65rem; font-weight:900; }
      .更新日 { color:rgba(23,48,50,.48); font-size:.68rem; margin-top:.7rem; }
      .提醒 { border-left:4px solid var(--orange); padding:.9rem 1rem; background:#fff6e8; border-radius:.8rem; color:#77410b; }
      .獎勵格 { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.65rem; margin:.5rem 0 1rem; }
      .獎勵項 { display:grid; grid-template-columns:auto 1fr auto; align-items:center; gap:.8rem; padding:.9rem 1rem; border:1px solid var(--line); border-radius:.95rem; background:#ffffff; box-shadow:0 8px 20px rgba(39,72,61,.045); }
      .獎勵序 { display:grid; place-items:center; width:1.6rem; height:1.6rem; border-radius:.55rem; background:#edf7d8; color:#5d850a; font-size:.72rem; font-weight:950; }
      .獎勵名稱 { color:var(--ink); font-size:.82rem; font-weight:900; }
      .獎勵數據 { color:rgba(23,48,50,.55); font-size:.68rem; text-align:right; }

      @media (max-width: 900px) {
        .block-container { padding:1rem 1rem 3rem; }
        .主視覺 { padding:1.3rem 1.25rem; border-radius:1.2rem; }
        .主標 { font-size:clamp(1.8rem, 7vw, 2.6rem); }
        .速覽清單 { grid-template-columns:1fr; }
        .獎勵格 { grid-template-columns:1fr; }
        .優先格 { grid-template-columns:1fr; }
      }
      @media (max-width: 640px) {
        [data-testid="stHeader"] { height:1.4rem; }
        .block-container { padding:.65rem .8rem 6.5rem; }
        .同步徽章 { font-size:0; padding:.45rem; }
        .同步徽章::after { content:"同步"; font-size:.68rem; }
        [data-testid="stRadio"] { position:fixed; left:.6rem; right:.6rem; bottom:max(.55rem, env(safe-area-inset-bottom)); top:auto; width:auto; z-index:9999; filter:drop-shadow(0 12px 26px rgba(29,73,63,.2)); }
        div[role="radiogroup"] { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); }
        div[role="radiogroup"] label { min-width:0; padding:.55rem .35rem; font-size:.7rem; }
        .主視覺 { margin:1rem 0; }
        .說明 { font-size:.84rem; }
        .重點速覽 { padding:1rem; }
        .速覽區塊 { min-height:0; }
        .速覽區塊 li { font-size:.82rem; }
        .速覽結論, .速覽停損 { display:block; }
        .速覽結論 b, .速覽停損 b { display:block; margin-bottom:.25rem; }
        .快捷格 { grid-template-columns:1fr; }
        .快捷卡 { min-height:0; }
        [data-testid="stImage"] { display:none; }
        .建議框 { grid-template-columns:1fr; }
        .配置總覽 { min-height:0; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="頂導">
      <div class="品牌"><span class="品牌記號">噠</span><span>噠噠攻略站</span></div>
      <div class="同步徽章"><span class="同步點"></span>資料每 15 分鐘自動同步</div>
    </div>
    """,
    unsafe_allow_html=True,
)

主頁面 = st.radio(
    "選擇功能",
    ["首頁", "活動", "養成", "資料庫"],
    horizontal=True,
    label_visibility="collapsed",
    key="主導覽",
)

if 主頁面 == "活動":
    頁面 = "活動最佳解"
elif 主頁面 == "養成":
    頁面 = st.selectbox("選擇養成工具", ["帳號診斷", "終局配裝", "收藏優先級"], key="養成分類")
elif 主頁面 == "資料庫":
    頁面 = st.selectbox("選擇資料內容", ["完整攻略庫", "收藏圖鑑", "最新文章"], key="資料分類")
else:
    頁面 = "首頁"

頁面主視覺 = {
    "首頁": ("PRO DECISION HUB", "今天該做什麼，<br><span>三十秒做對決定。</span>", "即時活動、終局養成與完整資料庫集中在同一套決策流程；先看結論，再查完整依據。"),
    "活動最佳解": ("活動決策中心", "先算完免費進度，<br><span>再決定要不要補。</span>", "選活動、填進度，直接得到補鑽上限、寶石安全線與兌換優先級。"),
    "帳號診斷": ("個人化養成路線", "先找到最大缺口，<br><span>再集中跨過斷點。</span>", "依模式、裝備階段與稀缺資源，整理現在最該做的三件事。"),
    "終局配裝": ("終局實戰配置", "不是只有一套神裝，<br><span>模式不同，答案就不同。</span>", "把首領、區域行動與高速清怪拆開判斷，避免用錯配置。"),
    "完整攻略庫": ("完整資料中心", "攻略不只收得多，<br><span>還要知道現在能不能用。</span>", "精選決策卡加上全部來源同步，並標記現行、常駐與需核對內容。"),
    "收藏圖鑑": ("290 件完整收藏", "先查缺哪一件，<br><span>再決定自選箱投哪裡。</span>", "依名稱、品質與期數篩選收藏，快速核對圖示與詳細資料。"),
    "收藏優先級": ("收藏養成決策", "不要平均升星，<br><span>先跨真正有效的斷點。</span>", "依套裝、主力技能與乘區收益，排出收藏資源的正確順序。"),
    "最新文章": ("版本情報同步", "新活動、新系統，<br><span>一次掌握真正有用的變化。</span>", "自動彙整最新來源，版本變動時保留原文入口供你快速核對。"),
}
視覺小標, 視覺標題, 視覺說明 = 頁面主視覺[頁面]
主視覺內容 = f"""
    <section class="主視覺">
      <div class="小標">{視覺小標}</div>
      <div class="主標">{視覺標題}</div>
      <p class="說明">{視覺說明}</p>
      <span class="主視覺徽章">繁體中文・終局玩家版・每筆資料標記狀態</span>
    </section>
    """
if 頁面 == "首頁":
    主視覺左, 主視覺右 = st.columns([1.25, 0.75])
    with 主視覺左:
        st.markdown(主視覺內容, unsafe_allow_html=True)
    with 主視覺右:
        st.image("public/dada-guide-hero.png", width="stretch")
else:
    st.markdown(主視覺內容, unsafe_allow_html=True)

if 頁面 == "首頁":
    全部文章首頁, 首頁即時 = 取得完整文章庫()
    首頁活動文章 = [item for item in 全部文章首頁 if item["category"] == "活動攻略"]
    首頁收藏圖鑑 = 取得收藏圖鑑()

    st.markdown(
        f'<div class="信任列"><span><b>{官方版本資訊["版本"]}</b> 版本追蹤</span>'
        f'<span><b>{len(全部文章首頁)}</b> 篇來源攻略</span><span><b>{len(首頁活動文章)}</b> 篇活動資料</span>'
        f'<span><b>{len(首頁收藏圖鑑)}</b> 件收藏圖鑑</span><span><b>{"即時" if 首頁即時 else "備援"}</b> 資料模式</span></div>',
        unsafe_allow_html=True,
    )

    st.header("今天只看這裡")
    if 首頁活動文章:
        首頁活動 = 首頁活動文章[0]
        首頁活動模型 = match_event_playbook(首頁活動["title"])
        顯示活動重點(首頁活動["title"], 首頁活動["date"], 首頁活動模型, "目前活動 · 30 秒攻略")
        活動操作, 原文操作 = st.columns(2)
        with 活動操作:
            st.button("用我的帳號精算這次活動", type="primary", width="stretch", on_click=切換主頁面, args=("活動",))
        with 原文操作:
            st.link_button("核對完整原始攻略 ↗", 首頁活動["link"], width="stretch")
    else:
        st.info("活動來源暫時無法連線；活動試算與既有攻略仍可正常使用。")

    st.markdown("### 三個專業決策入口")
    st.markdown(
        f"""
        <div class="快捷格">
          <div class="快捷卡"><span class="快捷編號">01 · 活動</span><strong>這次活動值不值得追？</strong><p>先算免費進度，再看補鑽上限、寶石安全線與獎勵兌換順序。</p></div>
          <div class="快捷卡"><span class="快捷編號">02 · 養成</span><strong>下一份資源投在哪？</strong><p>集中帳號診斷、終局配裝與收藏優先級，依模式判斷下一個斷點。</p></div>
          <div class="快捷卡"><span class="快捷編號">03 · 資料庫</span><strong>需要查完整資料？</strong><p>搜尋 {len(全部文章首頁)} 篇來源文章與 {len(首頁收藏圖鑑)} 件收藏，另有人工整理的精選攻略。</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    入口一, 入口二, 入口三 = st.columns(3)
    with 入口一:
        st.button("開啟活動判斷", width="stretch", on_click=切換主頁面, args=("活動",))
    with 入口二:
        st.button("進行帳號診斷", width="stretch", on_click=切換主頁面, args=("養成", "帳號診斷"))
    with 入口三:
        st.button("搜尋完整資料", width="stretch", on_click=切換主頁面, args=("資料庫", "完整攻略庫"))

    最新區, 版本區 = st.columns([1.35, 0.65])
    with 最新區:
        st.markdown("### 最新情報")
        首頁最新 = 全部文章首頁[:3]
        if 首頁最新:
            for item in 首頁最新:
                with st.container(border=True):
                    st.caption(f"{item['category']}｜{item['date']}")
                    st.markdown(f"**{item['title']}**")
                    摘要 = item.get("excerpt") or "開啟原文查看完整內容。"
                    st.write(摘要[:120] + ("…" if len(摘要) > 120 else ""))
                    st.link_button("閱讀原文", item["link"], width="stretch")
        else:
            st.caption("最新來源暫時無法載入。")
    with 版本區:
        st.markdown("### 版本雷達")
        版本項目 = "".join(f"<li>{html.escape(item)}</li>" for item in 官方版本資訊["重點"])
        st.markdown(
            f'<div class="版本卡"><span class="資料標籤">官方商店版本 {官方版本資訊["版本"]}</span>'
            f'<h3>{官方版本資訊["標題"]}</h3><p>最後查核：{官方版本資訊["查核"]}</p><ul>{版本項目}</ul></div>',
            unsafe_allow_html=True,
        )
        官方一, 官方二 = st.columns(2)
        with 官方一:
            st.link_button("Apple 官方", "https://apps.apple.com/us/app/survivor-io/id1528941310", width="stretch")
        with 官方二:
            st.link_button("Google 官方", "https://play.google.com/store/apps/details?id=com.dxx.firenow", width="stretch")

elif 頁面 == "活動最佳解":
    st.header("活動最佳解：先算免費進度，再決定要不要補")
    全部文章, 文章即時 = 取得完整文章庫()
    活動文章 = [item for item in 全部文章 if item["category"] == "活動攻略"]
    if 活動文章:
        預設活動索引 = next(
            (index for index, item in enumerate(活動文章) if match_event_playbook(item["title"])["name"] != "通用活動模型"),
            0,
        )
        活動選項 = [f"{item['date']}｜{item['title']}" for item in 活動文章[:40]]
        活動標籤 = st.selectbox("自動偵測到的近期／歷史活動", 活動選項, index=min(預設活動索引, len(活動選項) - 1))
        已選活動 = 活動文章[活動選項.index(活動標籤)]
    else:
        已選活動 = {
            "title": "目前活動（手動輸入）",
            "date": datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y/%m/%d"),
            "excerpt": "來源暫時無法連線，仍可使用下方通用試算。",
            "link": 來源分類網址,
            "freshness": "待核對",
        }
    活動模型 = match_event_playbook(已選活動["title"])

    顯示活動重點(
        str(已選活動["title"]),
        str(已選活動["date"]),
        活動模型,
        f"{已選活動.get('freshness', '待核對')} · 30 秒攻略",
    )
    st.caption(
        f"已同步 {len(全部文章)} 篇來源攻略｜其中 {len(活動文章)} 篇活動攻略｜自動套用：{活動模型['name']}"
        if 文章即時
        else f"來源目前使用備援模式｜自動套用：{活動模型['name']}"
    )
    st.link_button("核對原始活動攻略 ↗", 已選活動["link"])

    with st.expander("展開詳細玩法與判斷依據"):
        st.markdown(f"**核心機制：** {活動模型['mechanic']}")
        for index, step in enumerate(活動模型["steps"], 1):
            st.markdown(f"{index}. {step}")
        st.markdown(f"**免費資源依據：** {活動模型['free_hint']}")
        st.markdown(f"**停損提醒：** {活動模型['avoid']}")

    st.markdown("### 用你的帳號數字精算")
    a1, a2, a3 = st.columns(3)
    with a1:
        帳號目標 = st.selectbox(
            "帳號最大缺口",
            ["不確定，幫我排", "神器核心", "異世寵物", "科技配件", "收藏品", "SP特工／覺醒", "S裝備", "載具"],
        )
    with a2:
        帳號階段 = st.selectbox("帳號階段", ["尚未紅裝成套", "紅裝成套、神器核心不足", "主要裝備斷點已完成", "接近滿配"])
    with a3:
        消費風格 = st.selectbox("消費風格", ["無課／只用免費資源", "微課／可小補寶石", "課金／只看效率"])

    獎勵排序 = rank_rewards(帳號目標, 帳號階段)
    目標獎勵名稱 = st.selectbox("想追的里程碑獎勵", [item["name"] for item in 獎勵排序])
    目標獎勵 = next(item for item in 獎勵排序 if item["name"] == 目標獎勵名稱)

    模型目標 = int(活動模型["target"])
    預設目標 = 模型目標 if 0 < 模型目標 <= 10000 else 100
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        目前進度 = int(st.number_input("目前活動進度", min_value=0, value=0, step=1))
    with p2:
        剩餘天數 = int(st.number_input("剩餘天數", min_value=0, max_value=30, value=3, step=1))
    with p3:
        每日免費進度 = int(st.number_input("每天還可拿的免費進度", min_value=0, value=max(1, 預設目標 // 6), step=1))
    with p4:
        目標進度 = int(st.number_input("目標里程碑", min_value=1, value=預設目標, step=1))

    c1, c2, c3 = st.columns(3)
    with c1:
        每次付費進度 = float(st.number_input("一次票券／抽取增加進度", min_value=0.01, value=1.0, step=0.1))
    with c2:
        每次寶石成本 = int(st.number_input("一次票券／抽取寶石成本", min_value=0, value=100, step=10))
    with c3:
        現有寶石 = int(st.number_input("目前寶石", min_value=0, value=30000, step=500))

    with st.expander("這些數字怎麼填？"):
        st.write("免費進度包含剩餘登入、每日任務、廣告、免費票與預計開箱任務；付費進度只填需要用寶石補的部分。若遊戲顯示每次十連抽，請把進度與成本都換算成單次或都用十連，兩邊單位一致即可。")

    if st.button("一鍵判斷這次活動", type="primary", width="stretch"):
        判斷 = assess_event_plan(
            current_progress=目前進度,
            days_remaining=剩餘天數,
            free_progress_per_day=每日免費進度,
            target_progress=目標進度,
            progress_per_paid_action=每次付費進度,
            gems_per_paid_action=每次寶石成本,
            gems_owned=現有寶石,
            spending_style=消費風格,
            target_reward=目標獎勵,
        )
        getattr(st, 判斷["tone"])(f"{判斷['verdict']}｜{判斷['reason']}")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("免費期末進度", f"{判斷['projected_free']:,}")
        r2.metric("仍缺進度", f"{判斷['gap']:,}")
        r3.metric("估計補鑽", f"{判斷['gem_need']:,}")
        r4.metric("每天至少要拿", f"{判斷['daily_needed']:,}")
        免費達成率 = min(1.0, 判斷["projected_free"] / max(目標進度, 1))
        st.progress(免費達成率, text=f"免費進度可完成目標的 {免費達成率 * 100:.0f}%")
        st.write(f"建議保留寶石安全線：**{判斷['reserve']:,}**；目前可安全動用：**{判斷['spendable']:,}**；此獎勵對你帳號的估算補鑽上限：**{判斷['value_cap']:,}**。")
        st.caption("價值上限是用帳號缺口與長期稀缺度估算的決策門檻，不是官方定價；活動結束時間與實際機率仍以遊戲內公告為準。")

    st.markdown("### 兌換商店優先級")
    獎勵卡片 = "".join(
        f'<div class="獎勵項"><span class="獎勵序">{index:02d}</span>'
        f'<span class="獎勵名稱">{html.escape(str(reward["name"]))}</span>'
        f'<span class="獎勵數據">適配 {reward["score"]}<br>上限 {reward["adjusted_gem_value"]:,} 鑽</span></div>'
        for index, reward in enumerate(獎勵排序[:8], 1)
    )
    st.markdown(f'<div class="獎勵格">{獎勵卡片}</div>', unsafe_allow_html=True)

elif 頁面 == "帳號診斷":
    st.header("終局帳號診斷：四個狀態，直接決定下一步")
    st.caption("選項變更後會自動重算；先確認不含場內觸發的基礎暴率，以及角色實際覺醒階級。")
    col1, col2 = st.columns(2)
    with col1:
        主位階段 = st.selectbox(
            "① 主位與暴率門檻",
            ["塔洛莎覺醒5＋暴率70%", "維納托覺醒5＋塔洛莎覺醒4", "塔洛莎覺醒1～4／暴率未滿70%", "都未達／不確定"],
        )
        遊玩模式 = st.selectbox("③ 目前主要模式", ["短場首領", "長場首領", "區域行動"])
    with col2:
        混沌階段 = st.selectbox("② 混沌之力", ["混沌之力9～17", "混沌之力18以上", "混沌之力未滿9／不確定"])
        神火階段 = st.selectbox("④ 神火支援鏈", ["都沒有／不確定", "只有哪吒", "哪吒覺醒2＋伏爾坎覺醒1"])

    診斷 = diagnose_account(main_stage=主位階段, chaos_stage=混沌階段, play_mode=遊玩模式, divine_stage=神火階段)
    st.markdown(
        f'<section class="診斷結論"><span class="診斷標籤">{診斷["phase"]} · 即時判斷</span>'
        f'<h3>{診斷["title"]}</h3><p>{診斷["reason"]}</p></section>',
        unsafe_allow_html=True,
    )
    st.progress(診斷["readiness"] / 100, text=f"終局準備度 {診斷['readiness']}%｜下一個斷點：{診斷['next_breakpoint']}")

    優先卡片 = "".join(
        f'<article class="優先項"><small>0{index} · {html.escape(item["label"])}</small><strong>{html.escape(item["title"])}</strong><p>{html.escape(item["detail"])}</p></article>'
        for index, item in enumerate(診斷["priorities"], 1)
    )
    st.markdown(f'<div class="優先格">{優先卡片}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="建議框"><div><b>模式配置｜{診斷["build"]}</b>{診斷["mode_instruction"]}</div>'
        f'<div><b>現在不要做</b>{診斷["avoid"]}</div></div>',
        unsafe_allow_html=True,
    )
    st.info(f"轉換條件：{診斷['switch_condition']}")
    st.button("依這個結果查看完整配裝", type="primary", width="stretch", on_click=切換主頁面, args=("養成", "終局配裝"))

elif 頁面 == "終局配裝":
    st.header("三套終局配置：先選模式，再核對斷點")
    cols = st.columns(3)
    for col, build in zip(cols, 終局配置):
        with col:
            評分 = "".join(f'<div class="評分"><b>{score}</b><span>{label}</span></div>' for label, score in build["評分"].items())
            st.markdown(
                f'<article class="配置總覽"><small>{build["適用"]}</small><h3>{build["名稱"]}</h3><p>{build["核心"]}</p><div class="評分列">{評分}</div></article>',
                unsafe_allow_html=True,
            )
    選擇配置名稱 = st.selectbox("展開完整配置", [build["名稱"] for build in 終局配置])
    選擇配置 = next(build for build in 終局配置 if build["名稱"] == 選擇配置名稱)
    詳情左, 詳情右 = st.columns(2)
    with 詳情左:
        st.markdown(
            f'<div class="配置詳情"><p><b>角色：</b>{選擇配置["角色"]}</p><p><b>異獸：</b>{選擇配置["寵物"]}</p>'
            f'<p><b>武器：</b>{選擇配置["武器"]}</p><p><b>關鍵斷點：</b>{選擇配置["斷點"]}</p></div>',
            unsafe_allow_html=True,
        )
    with 詳情右:
        裝備清單 = "".join(f"<li>{html.escape(item)}</li>" for item in 選擇配置["裝備"])
        技能文字 = "、".join(選擇配置["技能"])
        st.markdown(
            f'<div class="配置詳情"><p><b>裝備：</b></p><ul>{裝備清單}</ul><p><b>技能：</b>{技能文字}</p></div>',
            unsafe_allow_html=True,
        )
    st.warning("縮寫 E／V／C 分別代表永恆／虛空／混沌神鑄。不要用同一套配置同時評估短場、長場與區域行動；跨過門檻後仍需固定場景 A/B 實測。")

elif 頁面 == "完整攻略庫":
    st.header("完整攻略庫：精選決策＋全部來源自動同步")
    精選頁, 全部頁 = st.tabs(["精選決策卡", "全部來源文章"])
    with 精選頁:
        c1, c2 = st.columns([1.35, 1])
        with c1:
            查詢 = st.text_input("搜尋精選攻略", placeholder="搜尋科技配件、收藏、寵物、覺醒……", key="curated_search")
        with c2:
            分類 = st.selectbox("精選分類", ["全部", "最新系統", "科技配件", "收藏系統", "特工寵物", "裝備養成", "關卡活動"], key="curated_category")

        結果 = [
            item
            for item in 攻略資料
            if (分類 == "全部" or item["分類"] == 分類)
            and (not 查詢 or 查詢.lower() in " ".join([item["標題"], item["摘要"], *item["行動"]]).lower())
        ]
        st.caption(f"找到 {len(結果)} 個人工核對的決策主題")
        for row_start in range(0, len(結果), 3):
            cols = st.columns(3)
            for col, item in zip(cols, 結果[row_start : row_start + 3]):
                with col:
                    顯示攻略卡片(item)
        if not 結果:
            st.info("沒有符合的精選主題，請改到『全部來源文章』搜尋。")

    with 全部頁:
        全部文章, 即時 = 取得完整文章庫()
        if not 即時:
            st.warning("來源目前無法連線；精選決策卡與收藏圖鑑仍可正常使用。")
        else:
            m1, m2, m3 = st.columns(3)
            m1.metric("來源文章", len(全部文章))
            m2.metric("活動攻略", sum(1 for item in 全部文章 if item["category"] == "活動攻略"))
            m3.metric("資料分類", len({item["category"] for item in 全部文章}))
            f1, f2 = st.columns([1.4, 1])
            with f1:
                全文查詢 = st.text_input("搜尋全部文章", placeholder="輸入活動、角色、裝備、配件或資源名稱", key="live_search")
            with f2:
                全部分類 = st.selectbox("文章分類", ["全部", *sorted({item["category"] for item in 全部文章})], key="live_category")
            全文結果 = [
                item
                for item in 全部文章
                if (全部分類 == "全部" or item["category"] == 全部分類)
                and (not 全文查詢 or 全文查詢.lower() in f"{item['title']} {item['excerpt']}".lower())
            ]
            每頁數量 = 12
            總頁數 = max(1, (len(全文結果) + 每頁數量 - 1) // 每頁數量)
            頁碼 = st.selectbox("文章頁碼", list(range(1, 總頁數 + 1)), key=f"article_page_{len(全文結果)}")
            st.caption(f"找到 {len(全文結果)} 篇｜第 {頁碼}/{總頁數} 頁")
            當頁 = 全文結果[(頁碼 - 1) * 每頁數量 : 頁碼 * 每頁數量]
            for row_start in range(0, len(當頁), 2):
                cols = st.columns(2)
                for col, item in zip(cols, 當頁[row_start : row_start + 2]):
                    with col:
                        with st.container(border=True):
                            st.markdown(f"**{item['title']}**")
                            st.caption(f"{item['category']}｜{item['freshness']}｜{item['date']}")
                            摘要 = item["excerpt"] or "來源未提供摘要，請開啟原文核對。"
                            st.write(摘要[:280] + ("…" if len(摘要) > 280 else ""))
                            st.link_button("閱讀原文", item["link"])

elif 頁面 == "收藏圖鑑":
    st.header("完整收藏品圖鑑")
    收藏圖鑑 = 取得收藏圖鑑()
    d1, d2, d3 = st.columns(3)
    d1.metric("收藏品總數", len(收藏圖鑑))
    d2.metric("收錄期數", len({item["edition"] for item in 收藏圖鑑}))
    d3.metric("傳奇收藏", sum(1 for item in 收藏圖鑑 if item["quality"] == "傳奇"))
    q1, q2, q3 = st.columns([1.4, 1, 1])
    with q1:
        收藏查詢 = st.text_input("搜尋收藏品", placeholder="輸入名稱或編號")
    with q2:
        收藏品質 = st.selectbox("品質", ["全部", "傳奇", "史詩", "優秀", "精良", "普通"])
    with q3:
        收藏期數 = st.selectbox("期數", ["全部", *range(1, 11)])
    收藏結果 = [
        item
        for item in 收藏圖鑑
        if (收藏品質 == "全部" or item["quality"] == 收藏品質)
        and (收藏期數 == "全部" or item["edition"] == 收藏期數)
        and (not 收藏查詢 or 收藏查詢.lower() in f"{item['id']} {item['name']}".lower())
    ]
    收藏每頁 = 25
    收藏總頁 = max(1, (len(收藏結果) + 收藏每頁 - 1) // 收藏每頁)
    收藏頁碼 = st.selectbox("圖鑑頁碼", list(range(1, 收藏總頁 + 1)), key=f"collectible_page_{len(收藏結果)}")
    收藏當頁 = 收藏結果[(收藏頁碼 - 1) * 收藏每頁 : 收藏頁碼 * 收藏每頁]
    st.caption(f"找到 {len(收藏結果)} 件｜第 {收藏頁碼}/{收藏總頁} 頁")
    st.dataframe(
        [
            {
                "圖片": item["image"],
                "編號": item["id"],
                "名稱": item["name"],
                "品質": item["quality"],
                "期數": item["edition"],
                "詳細資料": item["link"],
            }
            for item in 收藏當頁
        ],
        hide_index=True,
        width="stretch",
        column_config={
            "圖片": st.column_config.ImageColumn("圖示", width="small"),
            "詳細資料": st.column_config.LinkColumn("詳細資料", display_text="開啟"),
        },
    )

elif 頁面 == "收藏優先級":
    st.header("收藏品不是全收，先跨有效斷點")
    left, right = st.columns([1.1, 1])
    with left:
        for index, item in enumerate(收藏優先順序, 1):
            st.markdown(f"### {index:02d}　{item}")
    with right:
        st.markdown(
            '<div class="提醒"><b>最常見的錯誤</b><br>平均升星、只看稀有度、為了開槽過早分解，以及沒有先確認套裝下一個效果。</div>',
            unsafe_allow_html=True,
        )
        st.divider()
        st.metric("已整理收藏主題", "4 類")
        st.metric("收藏決策核心", "套裝＋技能＋乘區")

elif 頁面 == "最新文章":
    st.header("最新來源動態")
    全部文章, 全部即時 = 取得完整文章庫()
    if 全部即時:
        最新 = [{"標題": item["title"], "日期": item["date"], "網址": item["link"], "分類": item["category"]} for item in 全部文章[:15]]
    else:
        最新, _ = 取得最新文章()
    st.caption(f"已同步完整來源，共 {len(全部文章)} 篇" if 全部即時 else "來源暫時無法連線，顯示最近備援資料")
    for item in 最新:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{item['標題']}**")
            col2.caption(item["日期"])
            if item.get("分類"):
                st.caption(item["分類"])
            st.link_button("閱讀原始文章", item["網址"])
    st.link_button("查看完整文章分類", 來源分類網址)

st.divider()
台北現在 = datetime.now(ZoneInfo("Asia/Taipei"))
st.caption(f"最後載入：{台北現在.strftime('%Y/%m/%d %H:%M')}（台北）｜攻略僅供遊戲決策參考，版本變動時以遊戲內公告與官方商店為準。")
