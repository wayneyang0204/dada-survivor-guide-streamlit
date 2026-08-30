from __future__ import annotations

import html
import json
from datetime import datetime
from urllib.request import Request, urlopen

import streamlit as st

from data_engine import (
    assess_event_plan,
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
        "名稱": "首領極限輸出",
        "適用": "討伐、遠征首領、傷害排行",
        "核心": "用已達斷點的終局武器與腰帶，科技配件全部服務主輸出技能。",
        "檢查": ["先看武器與腰帶核心數", "寵物比較主人總傷而非自身傷害", "收藏先補暴擊與技能傷害斷點"],
    },
    {
        "名稱": "區域行動穩定通關",
        "適用": "高難區域、容易翻車的限制關",
        "核心": "保留一個生存來源，再用區域強化補回輸出；不要直接照抄首領配裝。",
        "檢查": ["先讀限制與異常效果", "防禦配件補當關缺口", "普通關穩定後才換純輸出"],
    },
    {
        "名稱": "高速清怪與推圖",
        "適用": "主線、資源關、活動刷取",
        "核心": "以範圍、持續輸出與移動效率為主，不浪費資源追單體首領數字。",
        "檢查": ["武器先確保清場範圍", "技能保留範圍與冷卻", "只在卡王時補單體傷害"],
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
        st.link_button("核對原始文章", item["來源"], use_container_width=True)


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


def 顯示活動重點(標題: str, 日期: str, 活動模型: dict, 狀態: str = "30 秒攻略") -> None:
    重點項目 = "".join(
        f'<div class="速覽項"><span class="速覽號">{index}</span><div><strong>{html.escape(label)}</strong><p>{html.escape(content)}</p></div></div>'
        for index, (label, content) in enumerate(取得活動重點(活動模型), 1)
    )
    結論 = str(
        活動模型.get("verdict")
        or (f"先把免費進度跑完，只補到 {int(活動模型['target']):,} {活動模型['unit']}。" if int(活動模型.get("target", 0)) > 0 else "先做完免費任務，最後一天再決定是否投入。")
    )
    st.markdown(
        f"""
        <section class="重點速覽">
          <div class="速覽頂列"><span class="速覽徽章">{html.escape(狀態)}</span><span>{html.escape(日期)}</span></div>
          <h3>{html.escape(標題)}</h3>
          <p class="速覽結論"><b>結論</b>{html.escape(結論)}</p>
          <div class="速覽清單">{重點項目}</div>
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

      [data-testid="stRadio"], [data-testid="stRadio"] > div { width:100%; }
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

      .重點速覽 { padding:1.3rem 1.4rem; border:1px solid rgba(115,159,18,.24); border-radius:1.25rem; background:linear-gradient(145deg,#ffffff,#f5faec); box-shadow:0 12px 30px rgba(39,72,61,.06); }
      .速覽頂列 { display:flex; align-items:center; justify-content:space-between; gap:.8rem; color:rgba(23,48,50,.5); font-size:.68rem; font-weight:800; }
      .速覽徽章 { padding:.28rem .55rem; border-radius:999px; background:var(--lime); color:#fff; letter-spacing:.08em; }
      .重點速覽 h3 { margin:.65rem 0 .7rem; font-size:clamp(1.15rem,2.5vw,1.55rem); line-height:1.38; }
      .速覽結論 { display:flex; gap:.65rem; align-items:flex-start; margin:0 0 .9rem; padding:.75rem .85rem; border-radius:.8rem; background:#edf7d8; color:#31530e; font-size:.86rem; line-height:1.55; }
      .速覽結論 b, .速覽停損 b { flex:0 0 auto; color:#557d08; }
      .速覽清單 { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.65rem; }
      .速覽項 { display:grid; grid-template-columns:auto 1fr; gap:.7rem; align-items:flex-start; min-height:5.5rem; padding:.85rem; border:1px solid var(--line); border-radius:.9rem; background:#fff; }
      .速覽號 { display:grid; place-items:center; width:1.55rem; height:1.55rem; border-radius:.5rem; background:#227d82; color:#fff; font-size:.72rem; font-weight:950; box-shadow:0 7px 14px rgba(34,125,130,.16); }
      .速覽項 strong { display:block; margin:.05rem 0 .25rem; color:var(--ink); font-size:.8rem; }
      .速覽項 p { margin:0; color:rgba(23,48,50,.68); font-size:.76rem; line-height:1.55; }
      .速覽停損 { display:flex; gap:.65rem; margin:.8rem 0 0; padding-top:.8rem; border-top:1px solid var(--line); color:#8a510f; font-size:.76rem; line-height:1.5; }
      .速覽停損 b { color:#a65c0b; }
      .快捷格 { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.75rem; margin:.65rem 0 1.2rem; }
      .快捷卡 { min-height:8.4rem; padding:1rem 1.05rem; border:1px solid var(--line); border-radius:1rem; background:#ffffff; box-shadow:0 9px 24px rgba(39,72,61,.045); }
      .快捷卡 strong { display:block; margin:.25rem 0 .45rem; color:var(--ink); font-size:1.02rem; }
      .快捷卡 p { margin:0; font-size:.78rem; line-height:1.55; }
      .快捷編號 { color:var(--lime); font-size:.66rem; font-weight:950; letter-spacing:.1em; }

      h1, h2, h3 { color:var(--ink) !important; letter-spacing:-.025em; }
      h2 { margin-top:1.25rem !important; font-size:clamp(1.65rem, 3vw, 2.35rem) !important; font-weight:950 !important; }
      h3 { font-weight:900 !important; }
      p, li { color:rgba(23,48,50,.75); }
      [data-testid="stCaptionContainer"] p { color:rgba(23,48,50,.56) !important; }

      .活動焦點 { position:relative; overflow:hidden; padding:1.4rem 1.5rem; border:1px solid rgba(115,159,18,.2); border-radius:1.35rem; background:linear-gradient(135deg, #f5faeb, #ffffff); }
      .活動焦點::before { content:"EVENT"; position:absolute; right:1rem; top:-.5rem; font-size:4.5rem; font-weight:950; color:rgba(115,159,18,.055); }
      .活動焦點 h3 { position:relative; margin:.35rem 0 .55rem; font-size:1.28rem; line-height:1.35; }
      .活動焦點 p { position:relative; margin:.55rem 0 0; max-width:920px; line-height:1.65; font-size:.87rem; }
      .資料標籤 { position:relative; color:var(--lime); font-size:.7rem; font-weight:900; letter-spacing:.08em; }
      .策略卡 { display:grid; grid-template-columns:1.1fr 1fr; gap:1rem; margin:1rem 0 .6rem; }
      .策略主體, .停損卡 { padding:1.2rem 1.3rem; border-radius:1.15rem; border:1px solid var(--line); background:#ffffff; box-shadow:0 10px 26px rgba(39,72,61,.05); }
      .策略主體 strong, .停損卡 strong { display:block; margin-bottom:.45rem; color:var(--ink); }
      .策略主體 p, .停損卡 p { margin:0; line-height:1.6; font-size:.84rem; }
      .停損卡 { border-color:rgba(184,105,18,.2); background:#fff9f0; }
      .停損卡 strong { color:#a65c0b; }
      .步驟列 { display:grid; grid-template-columns:repeat(3,1fr); gap:.65rem; margin:.7rem 0 1.4rem; }
      .步驟 { display:flex; gap:.65rem; align-items:flex-start; min-height:4rem; padding:.85rem; border:1px solid var(--line); border-radius:.9rem; background:#ffffff; color:rgba(23,48,50,.75); font-size:.78rem; line-height:1.45; }
      .步驟 b { display:grid; place-items:center; flex:0 0 auto; width:1.25rem; height:1.25rem; border-radius:50%; color:#fff; background:var(--lime); font-size:.65rem; }

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
      .配置卡 { border:1px solid rgba(115,159,18,.22); border-radius:1.15rem; background:#eff8d7; color:#173032; padding:1.2rem; min-height:250px; box-shadow:0 14px 30px rgba(39,72,61,.08); }
      .配置卡 h3 { margin:.35rem 0 .7rem; }
      .配置卡 p, .配置卡 li { font-size:.83rem; line-height:1.6; }
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
        .策略卡 { grid-template-columns:1fr; }
        .步驟列 { grid-template-columns:1fr; }
        .獎勵格 { grid-template-columns:1fr; }
      }
      @media (max-width: 640px) {
        [data-testid="stHeader"] { height:1.4rem; }
        .block-container { padding:.65rem .8rem 2.5rem; }
        .同步徽章 { font-size:0; padding:.45rem; }
        .同步徽章::after { content:"同步"; font-size:.68rem; }
        div[role="radiogroup"] { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); }
        div[role="radiogroup"] label { min-width:0; padding:.55rem .35rem; font-size:.7rem; }
        .主視覺 { margin:1rem 0; }
        .說明 { font-size:.84rem; }
        .重點速覽 { padding:1rem; }
        .速覽項 { min-height:0; }
        .速覽結論, .速覽停損 { display:block; }
        .速覽結論 b, .速覽停損 b { display:block; margin-bottom:.25rem; }
        .快捷格 { grid-template-columns:1fr; }
        .快捷卡 { min-height:0; }
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
    "首頁": ("今日攻略中心", "先看今天該做什麼，<br><span>再進工具查細節。</span>", "活動判斷、養成路線與完整資料集中在三個入口，減少來回尋找。"),
    "活動最佳解": ("活動決策中心", "先算完免費進度，<br><span>再決定要不要補。</span>", "選活動、填進度，直接得到補鑽上限、寶石安全線與兌換優先級。"),
    "帳號診斷": ("個人化養成路線", "先找到最大缺口，<br><span>再集中跨過斷點。</span>", "依模式、裝備階段與稀缺資源，整理現在最該做的三件事。"),
    "終局配裝": ("終局實戰配置", "不是只有一套神裝，<br><span>模式不同，答案就不同。</span>", "把首領、區域行動與高速清怪拆開判斷，避免用錯配置。"),
    "完整攻略庫": ("完整資料中心", "攻略不只收得多，<br><span>還要知道現在能不能用。</span>", "精選決策卡加上全部來源同步，並標記現行、常駐與需核對內容。"),
    "收藏圖鑑": ("290 件完整收藏", "先查缺哪一件，<br><span>再決定自選箱投哪裡。</span>", "依名稱、品質與期數篩選收藏，快速核對圖示與詳細資料。"),
    "收藏優先級": ("收藏養成決策", "不要平均升星，<br><span>先跨真正有效的斷點。</span>", "依套裝、主力技能與乘區收益，排出收藏資源的正確順序。"),
    "最新文章": ("版本情報同步", "新活動、新系統，<br><span>一次掌握真正有用的變化。</span>", "自動彙整最新來源，版本變動時保留原文入口供你快速核對。"),
}
視覺小標, 視覺標題, 視覺說明 = 頁面主視覺[頁面]
st.markdown(
    f"""
    <section class="主視覺">
      <div class="小標">{視覺小標}</div>
      <div class="主標">{視覺標題}</div>
      <p class="說明">{視覺說明}</p>
      <span class="主視覺徽章">繁體中文・終局玩家版・版本狀態已標記</span>
    </section>
    """,
    unsafe_allow_html=True,
)

if 頁面 == "首頁":
    全部文章首頁, 首頁即時 = 取得完整文章庫()
    首頁活動文章 = [item for item in 全部文章首頁 if item["category"] == "活動攻略"]
    首頁收藏圖鑑 = 取得收藏圖鑑()

    st.header("今日重點")
    if 首頁活動文章:
        首頁活動 = 首頁活動文章[0]
        首頁活動模型 = match_event_playbook(首頁活動["title"])
        顯示活動重點(首頁活動["title"], 首頁活動["date"], 首頁活動模型, "目前活動 · 30 秒攻略")
        st.link_button("閱讀目前活動攻略", 首頁活動["link"])
    else:
        st.info("活動來源暫時無法連線；活動試算與既有攻略仍可正常使用。")

    st.markdown("### 快速入口")
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

    數據1, 數據2, 數據3 = st.columns(3)
    數據1.metric("來源攻略", f"{len(全部文章首頁)} 篇" if 首頁即時 else "備援模式")
    數據2.metric("活動攻略", f"{len(首頁活動文章)} 篇")
    數據3.metric("收藏圖鑑", f"{len(首頁收藏圖鑑)} 件")

    st.markdown("### 最新情報")
    首頁最新 = 全部文章首頁[:3]
    if 首頁最新:
        最新欄 = st.columns(3)
        for 欄位, item in zip(最新欄, 首頁最新):
            with 欄位:
                with st.container(border=True):
                    st.caption(f"{item['category']}｜{item['date']}")
                    st.markdown(f"**{item['title']}**")
                    st.link_button("閱讀原文", item["link"], use_container_width=True)
    else:
        st.caption("最新來源暫時無法載入。")

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
            "date": datetime.now().strftime("%Y/%m/%d"),
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

    if st.button("一鍵判斷這次活動", type="primary", use_container_width=True):
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
    st.header("依你現在的帳號給出行動順序")
    col1, col2, col3 = st.columns(3)
    with col1:
        主要模式 = st.selectbox("目前最在意的模式", ["首領傷害", "區域行動", "主線推圖", "活動刷取"])
    with col2:
        裝備階段 = st.selectbox("終局裝備進度", ["尚未成套", "已有套裝但核心不足", "主要斷點已完成", "接近滿配"])
    with col3:
        最大缺口 = st.selectbox("目前最缺的資源", ["裝備核心", "收藏品", "科技配件", "覺醒核心", "寵物與核心"])

    if st.button("產生我的優先順序", type="primary", use_container_width=True):
        st.success(f"目前目標：{主要模式}｜裝備：{裝備階段}｜缺口：{最大缺口}")
        if 裝備階段 in {"尚未成套", "已有套裝但核心不足"}:
            st.markdown("### 第一順位：停止分散，先跨過一個核心斷點")
            st.write("選定目前主要模式，只強化能直接改變實戰效果的武器、腰帶或科技配件。")
        else:
            st.markdown("### 第一順位：用收藏、諧振與覺醒放大已完成的裝備")
            st.write("你的裝備已過主要斷點，下一階段應比較跨系統乘區，而不是繼續追小幅面板。")
        模式建議 = {
            "首領傷害": "先做同一場首領的固定時間測試，科技、寵物與收藏只保留能提高主人總傷的項目。",
            "區域行動": "先讀當區限制，保留一個生存來源，通關普通區後再把首領戰換成純輸出。",
            "主線推圖": "優先範圍與持續輸出；只有卡王時才犧牲清場能力補單體。",
            "活動刷取": "比較每分鐘收益，不必為低難活動更換或重置終局裝備。",
        }
        st.info(模式建議[主要模式])
        st.markdown(f"### 資源建議：{最大缺口}")
        st.write("自選箱與可回退資源保留到差一步就能跨斷點時再使用；不要為了單一面板數字提前消耗。")

elif 頁面 == "終局配裝":
    st.header("三套終局實戰思路")
    cols = st.columns(3)
    for col, build in zip(cols, 終局配置):
        with col:
            items = "".join(f"<li>{x}</li>" for x in build["檢查"])
            st.markdown(
                f'<div class="配置卡"><small>{build["適用"]}</small><h3>{build["名稱"]}</h3><p>{build["核心"]}</p><ul>{items}</ul></div>',
                unsafe_allow_html=True,
            )
    st.warning("不要用同一套裝備同時判斷首領、區域與推圖強度。終局差距通常來自核心斷點、乘區與模式，而不是單件稀有度。")

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
        use_container_width=True,
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
st.caption(f"最後載入：{datetime.now().strftime('%Y/%m/%d %H:%M')}｜攻略僅供遊戲決策參考，版本變動時以官方內容為準。")
