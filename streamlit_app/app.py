from __future__ import annotations

import html
import json
from datetime import datetime
from urllib.request import Request, urlopen

import streamlit as st


st.set_page_config(
    page_title="噠噠特攻終局攻略",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
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


def 顯示攻略卡片(item: dict) -> None:
    狀態色 = {"現行": "#d8ff57", "常駐": "#7ee7f2", "需版本核對": "#ffb86b"}[item["狀態"]]
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


st.markdown(
    """
    <style>
      :root { color-scheme: dark; }
      .stApp { background: #071719; color: #f7ffe7; }
      [data-testid="stSidebar"] { background: #0b2021; border-right: 1px solid rgba(255,255,255,.08); }
      [data-testid="stHeader"] { background: rgba(7,23,25,.82); }
      .主標 { font-size: clamp(2.1rem, 5vw, 4.4rem); line-height: 1.02; font-weight: 950; letter-spacing: -.05em; max-width: 900px; margin: .2rem 0 1rem; }
      .主標 span { color: #d8ff57; }
      .說明 { color: rgba(247,255,231,.65); max-width: 820px; line-height: 1.8; }
      .小標 { color: #d8ff57; font-size: .78rem; font-weight: 900; letter-spacing: .12em; }
      .攻略卡 { min-height: 225px; padding: 1.2rem; border: 1px solid rgba(255,255,255,.08); border-radius: 1.2rem; background: rgba(255,255,255,.035); }
      .攻略卡 h3 { font-size: 1.1rem; margin: .85rem 0 .55rem; }
      .攻略卡 p { color: rgba(247,255,231,.62); line-height: 1.65; font-size: .88rem; }
      .卡片頂列 { display:flex; justify-content:space-between; gap:.7rem; align-items:center; }
      .分類 { color:#d8ff57; font-size:.72rem; font-weight:900; }
      .狀態 { border:1px solid; border-radius:999px; padding:.2rem .55rem; font-size:.65rem; font-weight:900; }
      .更新日 { color:rgba(247,255,231,.38); font-size:.68rem; margin-top:.7rem; }
      .提醒 { border-left: 4px solid #ffb86b; padding: .8rem 1rem; background: rgba(255,184,107,.07); border-radius: .7rem; color: rgba(255,235,210,.78); }
      .配置卡 { border-radius: 1.1rem; background:#d8ff57; color:#0b1f1e; padding:1.15rem; min-height:250px; }
      .配置卡 h3 { margin:.35rem 0 .7rem; }
      .配置卡 p, .配置卡 li { font-size:.83rem; line-height:1.6; }
      div[data-testid="stMetric"] { border:1px solid rgba(255,255,255,.08); border-radius:1rem; padding:.8rem; background:rgba(255,255,255,.03); }
      .stButton button, .stLinkButton a { font-weight: 800; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## ⚡ 噠噠特攻攻略")
    st.caption("繁體中文・終局玩家版")
    頁面 = st.radio(
        "選擇功能",
        ["帳號診斷", "終局配裝", "系統資料庫", "收藏優先級", "最新文章"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**版本判讀**")
    st.caption("現行：可直接採用")
    st.caption("常駐：機制仍可參考")
    st.caption("需版本核對：只當查表入口")
    st.link_button("開啟完整攻略網站", "https://dada-survivor-guide.wayne111wrtfc.chatgpt.site", use_container_width=True)

st.markdown('<div class="小標">終局玩家決策中心</div>', unsafe_allow_html=True)
st.markdown('<div class="主標">不用再看新手排行，<br><span>直接決定下一步。</span></div>', unsafe_allow_html=True)
st.markdown(
    '<p class="說明">依模式、裝備斷點、科技配件、收藏與寵物整體收益做判斷。所有社群資料都標記版本狀態，官方資料優先。</p>',
    unsafe_allow_html=True,
)

if 頁面 == "帳號診斷":
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

elif 頁面 == "系統資料庫":
    st.header("完整系統攻略庫")
    c1, c2 = st.columns([1.35, 1])
    with c1:
        查詢 = st.text_input("搜尋", placeholder="搜尋科技配件、收藏、寵物、覺醒……")
    with c2:
        分類 = st.selectbox("分類", ["全部", "最新系統", "科技配件", "收藏系統", "特工寵物", "裝備養成", "關卡活動"])

    結果 = [
        item
        for item in 攻略資料
        if (分類 == "全部" or item["分類"] == 分類)
        and (not 查詢 or 查詢.lower() in " ".join([item["標題"], item["摘要"], *item["行動"]]).lower())
    ]
    st.caption(f"找到 {len(結果)} 個主題")
    for row_start in range(0, len(結果), 3):
        cols = st.columns(3)
        for col, item in zip(cols, 結果[row_start : row_start + 3]):
            with col:
                顯示攻略卡片(item)
    if not 結果:
        st.info("沒有符合的主題，請換一個關鍵字。")

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
    最新, 即時 = 取得最新文章()
    st.caption("已連接即時文章" if 即時 else "來源暫時無法連線，顯示最近備援資料")
    for item in 最新:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{item['標題']}**")
            col2.caption(item["日期"])
            st.link_button("閱讀原始文章", item["網址"])
    st.link_button("查看完整文章分類", 來源分類網址)

st.divider()
st.caption(f"最後載入：{datetime.now().strftime('%Y/%m/%d %H:%M')}｜攻略僅供遊戲決策參考，版本變動時以官方內容為準。")
