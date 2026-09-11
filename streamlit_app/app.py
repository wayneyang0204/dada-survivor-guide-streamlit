from __future__ import annotations

import html
import importlib
import json
from datetime import datetime
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import streamlit as st

import data_engine as _data_engine
import next_step as _next_step
import decision_ui as _decision_ui
import ui_theme as _ui_theme
import guide_content as _guide_content
import guide_ui as _guide_ui

_next_step = importlib.reload(_next_step)
_decision_ui = importlib.reload(_decision_ui)
_ui_theme = importlib.reload(_ui_theme)
_guide_content = importlib.reload(_guide_content)
_guide_ui = importlib.reload(_guide_ui)


# Streamlit Cloud can hot-reload app.py before a changed helper module. Reloading
# the helper explicitly prevents a stale module cache from hiding newly deployed
# functions during that short deployment window.
_data_engine = importlib.reload(_data_engine)
assess_event_plan = _data_engine.assess_event_plan
diagnose_account = _data_engine.diagnose_account
fetch_source_posts = _data_engine.fetch_source_posts
load_collectible_catalog = _data_engine.load_collectible_catalog
match_event_playbook = _data_engine.match_event_playbook
optimize_player_plan = _data_engine.optimize_player_plan
rank_rewards = _data_engine.rank_rewards


來源分類網址 = "https://notalknote.xyz/moblegame/survivorio/"
來源介面網址 = (
    "https://notalknote.xyz/wp-json/wp/v2/posts"
    "?categories=624&per_page=6&_fields=link,title,date"
)

攻略資料 = [
    {
        "分類": "最新系統",
        "標題": "5.2.0：洛基、伊蓮與主線 350 章更新判斷",
        "日期": "2026/09/11",
        "狀態": "官方已公布｜繁中分批上架",
        "摘要": "官方商店已公布 5.2.0，新增 346～350 章、神火特工洛基與高階特工伊蓮；特工同調等級 100 與公會活動「潮霧港灣」仍是預告內容。兩名新特工的技能、覺醒與終局排名尚待可靠實測。",
        "行動": ["先確認自己的商店是否已可下載 5.2.0", "完整數值公開前，不先轉換主力或投入萬能碎片", "新主線先沿用已成形後期配置，卡關再依實際詞條調整"],
        "來源": "https://apps.apple.com/us/app/survivor-io/id1528941310",
    },
    {
        "分類": "關卡活動",
        "標題": "水上樂園大亂鬥：先拿免費水槍，等獎勵表再定停損",
        "日期": "2026/09/10",
        "狀態": "官方活動｜資料待補",
        "摘要": "官方繁中活動頁確認可用水槍參加，並有機會取得神煉核心、限定收藏品與幽暗逐影碎片。完整任務數、機率與里程碑尚未核實。",
        "行動": ["先領登入、任務與免費水槍", "進遊戲核對結束時間、獎勵表與水槍取得量", "可靠數值補齊前只做免費進度，不預先投入寶石或鑰匙"],
        "來源": "https://apps.apple.com/tw/app/survivor-io/id1528941310?eventid=6806949373",
    },
    {
        "分類": "關卡活動",
        "標題": "煲湯廚房：先守二十四點，再選二百二十或三百湯勺",
        "日期": "2026/09/05",
        "狀態": "歷史活動｜已於9/9結束",
        "摘要": "本期活動已於 9 月 9 日結束。保留單鍋二十四點上限、二百二十湯勺停損與開箱成本，只供復刻時重新核對。",
        "行動": ["每輪至少煲三次，多數鍋在十八至二十一點時立即出鍋", "二百二十湯勺約需開三百八十至四百箱，鑰匙不足就不要硬追", "三百湯勺只適合可開約五百六十箱且確定需要異世靈藥的帳號"],
        "來源": "https://notalknote.xyz/survivorio-soup-kitchen-event-guide/",
    },
    {
        "分類": "關卡活動",
        "標題": "音樂圓盤大作戰：九百八十進度停損線",
        "日期": "2026/08/30",
        "狀態": "歷史活動｜已於9/3結束",
        "摘要": "活動到 9 月 3 日結束。社群實測約可取得九百張免費麥克風，盤面返還會放大實際進度；先跑免費資源，九百八十進度是目前最平衡的停損點。",
        "行動": ["先完成登入、每日任務與免費麥克風", "寶箱先開二百至三百箱，最後一天再補差額", "商店先換傳奇收藏品自選箱、萬能神火特工碎片與高級收藏之心"],
        "來源": "https://notalknote.xyz/survivor-io-music-disc-clash-guide/",
    },
    {
        "分類": "最新系統",
        "標題": "新版區域行動：四大區域與首領戰",
        "日期": "2026/08/27",
        "狀態": "現行",
        "摘要": "2026/08/27 新版不帶入局外角色與裝備；先手操 2～3 個小關取得局內 Buff，再挑戰區域首領。",
        "行動": ["先走高價值小關拿局內 Buff", "無人機至少升到自動索敵節點", "首領通關後直接領取該區下方獎勵"],
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
        "角色": "維納托覺醒7～8主位｜塔洛莎覺醒4協同保留裂傷觸發｜梅塔莉亞／楊大師覺醒1協同｜哪吒／伏爾坎支援以 R4 有效門檻核對",
        "寵物": "幽冥之魂覺醒5｜共鳴增益＋共鳴傷害",
        "武器": "雙生之槍｜永恆4、虛空4、混沌2以上、異界轉化1起",
        "裝備": ["武器｜雙生槍永恆4＋虛空4，神器核心堆混沌36", "項鍊｜現在穿破壞者徽記神鑄3，不要先換成審判項鍊", "手套｜月痕護腕雙生階，暴率沒70%才暫留虛空手套", "腰帶｜星塵腰帶雙生階，幽冥覺醒5後才點永恆3", "鞋子｜冰川戰靴雙生階，排最後", "衣服｜永虛戰甲雙生階永恆3起，短場不要穿亡者風衣"],
        "技能": ["雙生槍", "雙生無人機", "燃燒瓶", "足球", "鑽頭", "雷電"],
        "核心": "短場用 E4 起手等級與異界轉化壓縮進化；不要再用永恆1或苦無當武器終點。",
        "斷點": "雙生槍 E4V4＋異界轉化、混沌之力27切月鐮刀、基礎暴率70%以上才用月痕護腕。",
        "評分": {"清怪": 84, "首領": 100, "生存": 82},
    },
    {
        "名稱": "長戰疊層傷害極限",
        "適用": "長線首領／完整疊層場景",
        "角色": "維納托覺醒7～8主位｜塔洛莎覺醒4＋梅塔莉亞／楊大師覺醒1協同",
        "寵物": "幽冥之魂覺醒5｜保護＋共鳴增益＋共鳴傷害",
        "武器": "雙生之槍｜永恆4、虛空4、異界轉化；混沌之力27／36／45",
        "裝備": ["武器｜雙生槍永恆4＋虛空4＋異界轉化", "項鍊｜現在穿破壞者徽記神鑄3，混沌36後才 A/B 審判項鍊", "手套｜月痕護腕雙生階，不要退回虛空手套", "腰帶｜星塵腰帶永恆3後才 A/B 扭曲腰帶", "鞋子｜冰川戰靴排最後", "衣服｜永虛戰甲永恆3／虛空2／混沌2"],
        "技能": ["雙生槍", "雙生無人機", "燃油桶", "量子球", "永恆鑽頭", "超級雷暴"],
        "核心": "讓混沌27、寵物共鳴與裂傷／虛弱完整疊滿；不要用短場永恆1配置硬套。",
        "斷點": "混沌27切月鐮刀起跳；18只是神罰之斧。永虛甲至少永恆3，星塵腰帶永恆3後再 A/B 腰帶。",
        "評分": {"清怪": 88, "首領": 99, "生存": 90},
    },
    {
        "名稱": "新版區域行動路線最優解",
        "適用": "2026/08/27 新版四區域／區域首領",
        "角色標籤": "帶入規則",
        "角色": "局外角色、裝備與寵物不帶入；新版勝負取決於手操、局內技能與路線 Buff。",
        "寵物標籤": "操作核心",
        "寵物": "先打 2～3 個高價值小關強化，再挑區域首領；不要把時間平均浪費在所有支線。",
        "武器標籤": "主動優先",
        "武器": "無人機升到自動索敵節點後，依序考慮雷電、火箭、哨箭與足球。",
        "裝備標籤": "被動／路線",
        "裝備": ["移速鞋：提高走位與任務容錯", "回血、護甲、生命：先確保首次通關", "高爆彈頭、冷卻：輸出與技能循環", "區域首領優先：通關後可領取該區下方獎勵", "清潔戰可跳過；若挑戰，倒數結束時污染必須為 0"],
        "技能": ["無人機", "雷電", "火箭", "哨箭", "足球", "高爆彈頭／冷卻"],
        "核心": "新版是局內路線與 Buff 規劃器，不是局外裝備排行；先穩定通關，再追更快路線。",
        "斷點": "無人機至少升到可自動索敵；連續兩次因同一原因失敗時，只改一個技能或路線再測。",
        "評分": {"清怪": 94, "首領": 92, "生存": 100},
    },
]

收藏優先順序 = [
    "自選箱／收藏之心先把星際躍遷矩陣圖紙點到紅3就停",
    "接著把水動推力腳蹼點到紅3就停",
    "第三件才是暗物質傀儡，點到黃5就停",
    "追光者、混亂之劍、平均升星、先開空欄位硬塞，全部先不要",
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
                "標題": "煲湯廚房攻略",
                "日期": "2026/09/05",
                "網址": "https://notalknote.xyz/survivorio-soup-kitchen-event-guide/",
            },
            {
                "標題": "音樂圓盤大作戰攻略",
                "日期": "2026/08/30",
                "網址": "https://notalknote.xyz/survivor-io-music-disc-clash-guide/",
            },
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
    "版本": "5.2.0",
    "查核": "2026/09/11",
    "標題": "洛基、伊蓮與主線 346～350 章",
    "重點": ["新增主線 346～350 章與對應挑戰章節", "新增神火特工洛基與高階特工伊蓮，終局排名待實測", "特工同調等級 100 與公會活動潮霧港灣仍是預告", "新增雲端高塔與秋日海底探索等活動", "繁中版本仍在分批上架，請以自己的商店為準"],
}


def 切換主頁面(主要: str, 次要: str | None = None) -> None:
    st.session_state["主導覽"] = 主要
    if 主要 == "養成" and 次要:
        st.session_state["養成分類"] = 次要
    if 主要 == "資料庫" and 次要:
        st.session_state["資料分類"] = 次要


def 顯示攻略卡片(item: dict) -> None:
    狀態色 = {"現行": "#176446", "常駐": "#2449d8", "需版本核對": "#805510"}.get(item["狀態"], "#606873")
    st.markdown(
        f"""
        <div class="攻略卡">
          <div class="卡片頂列">
            <span class="分類">{item['分類']}</span>
            <span class="狀態" style="color:{狀態色}">{item['狀態']}</span>
          </div>
          <h3>{item['標題']}</h3>
          <p>{item['摘要']}</p>
          <div class="更新日">資料更新：{item['日期']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("查看這篇攻略的重點"):
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


標題攻略 = _guide_content.get_guide(st.query_params.get("guide", ""), _guide_content.all_guides(攻略資料))
st.set_page_config(
    page_title=f"{標題攻略['title']}｜噠噠攻略站" if 標題攻略 else "噠噠特攻攻略站 · 養成與活動攻略",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(_ui_theme.STYLE, unsafe_allow_html=True)

_guide_ui.sync_query()
st.session_state.setdefault("主導覽", "攻略首頁")
# Migrate older navigation state without carrying its conflicting recommendation pages.
if st.session_state.get("主導覽") in ("首頁", "養成"):
    st.session_state["主導覽"] = "下一步"
if pending := st.session_state.pop("pending_navigation", None):
    st.session_state["主導覽"] = pending
if st.session_state.get("資料分類") == "終局配裝":
    st.session_state["資料分類"] = "配裝參考"

st.markdown(
    """
    <div class="masthead">
      <div class="masthead-brand">
        <span class="brand-mark" aria-hidden="true">噠</span>
        <div><span class="brand-title">噠噠攻略站</span><span class="brand-subtitle">Survivor.io 攻略與養成指南</span></div>
      </div>
      <div class="masthead-edition">升級路線 / 活動試算 / 攻略索引</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(key="main_nav"):
    主頁面 = st.radio(
        "選擇功能",
        ["攻略首頁", "下一步", "我的帳號", "活動", "資料庫"],
        horizontal=True,
        label_visibility="collapsed",
        key="主導覽",
        on_change=_guide_ui.clear_article,
    )

if 主頁面 == "活動":
    頁面 = "活動最佳解"
elif 主頁面 == "資料庫":
    if st.session_state.get("article_slug"):
        頁面 = "閱讀攻略"
    else:
        _decision_ui.page_heading("攻略索引", "按系統或關鍵字查找；升級路線、機制門檻與來源分開標示。")
        頁面 = st.selectbox("要查什麼", ["本站攻略", "完整攻略庫", "收藏圖鑑", "最新文章", "配裝參考"], key="資料分類")
    if 頁面 == "配裝參考":
        頁面 = "終局配裝"
else:
    頁面 = 主頁面

if 頁面 == "攻略首頁":
    _guide_ui.render_home(攻略資料)
elif 頁面 == "本站攻略":
    _guide_ui.render_index(攻略資料)
elif 頁面 == "閱讀攻略":
    _guide_ui.render_article(st.session_state["article_slug"], 攻略資料)
elif 頁面 == "下一步":
    _decision_ui.render_home()
elif 頁面 == "我的帳號":
    _decision_ui.render_profile()
elif 頁面 == "活動最佳解":
    _decision_ui.page_heading("活動試算", "免費進度、里程碑與補鑽成本，一起核對。")
    全部文章, 文章即時 = 取得完整文章庫()
    官方活動文章 = {
        "title": "水上樂園大亂鬥",
        "date": "2026/09/10",
        "excerpt": "官方已確認可使用水槍參加；完整時間、任務數與里程碑仍待核對。",
        "link": "https://apps.apple.com/tw/app/survivor-io/id1528941310?eventid=6806949373",
        "category": "活動攻略",
        "freshness": "官方現行活動｜資料待補",
    }
    活動文章 = [官方活動文章, *[item for item in 全部文章 if item["category"] == "活動攻略"]]
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

    st.info("文章日期不等於活動仍開放。請先核對遊戲內名稱、截止時間與獎勵表；下方可試算歷史活動。")
    with st.expander("查看這篇活動的30秒重點", expanded=True):
        顯示活動重點(
            str(已選活動["title"]),
            str(已選活動["date"]),
            活動模型,
            f"{已選活動.get('freshness', '待核對')} · 參考攻略",
        )
    st.caption(
        f"已同步 {len(全部文章)} 篇來源攻略｜其中 {len(活動文章)} 篇活動攻略｜自動套用：{活動模型['name']}"
        if 文章即時
        else f"來源目前使用備援模式｜自動套用：{活動模型['name']}"
    )
    st.link_button("核對活動來源 ↗", 已選活動["link"])

    with st.expander("展開詳細玩法與判斷依據"):
        st.markdown(f"**核心機制：** {活動模型['mechanic']}")
        for index, step in enumerate(活動模型["steps"], 1):
            st.markdown(f"{index}. {step}")
        st.markdown(f"**免費資源依據：** {活動模型['free_hint']}")
        st.markdown(f"**停損提醒：** {活動模型['avoid']}")

    st.markdown("### 01 / 活動目標")
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
    st.markdown("### 02 / 免費進度")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        目前進度 = int(st.number_input("目前活動進度", min_value=0, value=0, step=1))
    with p2:
        剩餘天數 = int(st.number_input("剩餘天數", min_value=0, max_value=30, value=3, step=1))
    with p3:
        每日免費進度 = int(st.number_input("每天還可拿的免費進度", min_value=0, value=max(1, 預設目標 // 6), step=1))
    with p4:
        目標進度 = int(st.number_input("目標里程碑", min_value=1, value=預設目標, step=1))

    st.markdown("### 03 / 寶石成本")
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

    st.markdown("### 兌換優先項")
    st.write(f"**{獎勵排序[0]['name']}**")
    st.caption("依上方帳號缺口排出的參考順位；先確認這次商店確實有提供。")
    獎勵卡片 = "".join(
        f'<div class="獎勵項"><span class="獎勵序">{index:02d}</span>'
        f'<span class="獎勵名稱">{html.escape(str(reward["name"]))}</span>'
        f'<span class="獎勵數據">試算上限 {reward["adjusted_gem_value"]:,} 鑽</span></div>'
        for index, reward in enumerate(獎勵排序[:8], 1)
    )
    with st.expander("比較其他獎勵與試算上限"):
        st.markdown(f'<div class="獎勵格">{獎勵卡片}</div>', unsafe_allow_html=True)

elif 頁面 == "終局配裝":
    st.subheader("配裝參考")
    st.warning("以下為舊版整理的配裝範例，不是你的升級順位；名稱、神鑄與版本可能需重新核對。個人下一步請回首頁，高階六件配置請用情境計算器比較。")
    st.link_button("開啟完整傷害配置比較", "https://sio-tools.exp0.dev/")
    選擇配置名稱 = st.selectbox("展開完整配置", [build["名稱"] for build in 終局配置])
    選擇配置 = next(build for build in 終局配置 if build["名稱"] == 選擇配置名稱)
    詳情左, 詳情右 = st.columns(2)
    with 詳情左:
        角色標籤 = 選擇配置.get("角色標籤", "角色")
        寵物標籤 = 選擇配置.get("寵物標籤", "異獸")
        武器標籤 = 選擇配置.get("武器標籤", "武器")
        st.markdown(
            f'<div class="配置詳情"><p><b>{角色標籤}：</b>{選擇配置["角色"]}</p><p><b>{寵物標籤}：</b>{選擇配置["寵物"]}</p>'
            f'<p><b>{武器標籤}：</b>{選擇配置["武器"]}</p><p><b>關鍵斷點：</b>{選擇配置["斷點"]}</p></div>',
            unsafe_allow_html=True,
        )
    with 詳情右:
        裝備清單 = "".join(f"<li>{html.escape(item)}</li>" for item in 選擇配置["裝備"])
        技能文字 = "、".join(選擇配置["技能"])
        裝備標籤 = 選擇配置.get("裝備標籤", "裝備")
        st.markdown(
            f'<div class="配置詳情"><p><b>{裝備標籤}：</b></p><ul>{裝備清單}</ul><p><b>技能：</b>{技能文字}</p></div>',
            unsafe_allow_html=True,
        )
    if 選擇配置.get("角色標籤") == "帶入規則":
        st.info("新版區域行動不帶入局外裝備，請以局內技能、Buff 路線與實際失敗原因調整；不要套用 2026/08/27 以前的 AoQ／局外裝備攻略。")
    else:
        st.warning("縮寫 E／V／C 分別代表永恆／虛空／混沌神鑄。不要用同一套配置同時評估短場與長場；跨過門檻後仍需固定場景 A/B 實測。")

elif 頁面 == "完整攻略庫":
    精選頁, 全部頁 = st.tabs(["主題摘要", "來源文章"])
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
        st.caption(f"找到 {len(結果)} 個參考主題；請留意各篇資料日期。")
        精選頁數 = max(1, (len(結果) + 5) // 6)
        精選頁碼 = st.selectbox("主題頁碼", range(1, 精選頁數 + 1), key=f"curated_page_{分類}_{查詢}")
        當頁精選 = 結果[(精選頁碼 - 1)*6:精選頁碼*6]
        for item in 當頁精選:
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
            for index, item in enumerate(當頁):
                with st.container(key=f"source_article_{index}"):
                    st.caption(f"{item['category']} / {item['freshness']} / {item['date']}")
                    st.markdown(f"### {item['title']}")
                    摘要 = item["excerpt"] or "來源未提供摘要，請開啟原文核對。"
                    st.write(摘要[:280] + ("…" if len(摘要) > 280 else ""))
                    st.link_button("閱讀原文", item["link"])

elif 頁面 == "收藏圖鑑":
    st.subheader("收藏品圖鑑")
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

elif 頁面 == "最新文章":
    st.subheader("最新來源動態")
    全部文章, 全部即時 = 取得完整文章庫()
    if 全部即時:
        最新 = [{"標題": item["title"], "日期": item["date"], "網址": item["link"], "分類": item["category"]} for item in 全部文章[:15]]
    else:
        最新, _ = 取得最新文章()
    st.caption(f"已同步完整來源，共 {len(全部文章)} 篇" if 全部即時 else "來源暫時無法連線，顯示最近備援資料")
    for index, item in enumerate(最新):
        with st.container(key=f"latest_article_{index}"):
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{item['標題']}**")
            col2.caption(item["日期"])
            if item.get("分類"):
                st.caption(item["分類"])
            st.link_button("閱讀原始文章", item["網址"])
    st.link_button("查看完整文章分類", 來源分類網址)

st.markdown('<div class="site-footer">噠噠攻略站 · 2026.09.08 · 攻略網站版<br>社群攻略整理，非官方網站；本站不會登入或操作你的遊戲。</div>', unsafe_allow_html=True)
台北現在 = datetime.now(ZoneInfo("Asia/Taipei"))
st.caption(f"頁面時間（不是資料查核日期）：{台北現在.strftime('%Y/%m/%d %H:%M')}（台北）｜攻略僅供遊戲決策參考，版本變動時以遊戲內公告與官方商店為準。")
