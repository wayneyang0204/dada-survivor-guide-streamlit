export type SourceGuideCategory =
  | '最新系統'
  | '科技配件'
  | '收藏系統'
  | '特工寵物'
  | '裝備養成'
  | '關卡活動';

export type SourceGuide = {
  id: string;
  category: SourceGuideCategory;
  title: string;
  updated: string;
  status: '現行' | '常駐' | '需版本核對';
  summary: string;
  actions: string[];
  sourceUrl: string;
};

export const SOURCE_CATEGORY_URL =
  'https://notalknote.xyz/moblegame/survivorio/';

export const SOURCE_API_URL =
  'https://notalknote.xyz/wp-json/wp/v2/posts?categories=624&per_page=6&_fields=link,title,date,excerpt';

export const SOURCE_GUIDES: SourceGuide[] = [
  {
    id: 'regional-action-rework',
    category: '最新系統',
    title: '新版區域行動：四大區域與首領戰',
    updated: '2026/08/27',
    status: '現行',
    summary: '新版區域行動拆成四個區域，包含普通關卡、區域強化與區域首領；先完成能放大整區效率的強化，再投入首領戰。',
    actions: ['先看區域限制，再換裝備與技能', '普通關卡先拿強化，不急著硬壓首領', '高戰帳號以首領時間與獎勵上限為目標'],
    sourceUrl: 'https://notalknote.xyz/dadasurvivor-regional-action-update-guide/',
  },
  {
    id: 'umbral-soul',
    category: '特工寵物',
    title: '幽暗之靈：終局異世寵物判斷',
    updated: '2026/08/22',
    status: '現行',
    summary: '幽暗之靈以脆弱效果與主人增傷為核心，不應只看寵物自己的輸出占比；終局帳號要比較的是整體傷害提升。',
    actions: ['先確認異世寵物功能與核心數量', '比較整體傷害，不只看寵物傷害', '轉換前保留能回復配置的資源'],
    sourceUrl: 'https://notalknote.xyz/survivor-io-umbral-soul-pet-guide-2026/',
  },
  {
    id: 'edition-ten-collectibles',
    category: '收藏系統',
    title: '第10期收藏品：升級與選擇箱策略',
    updated: '2026/03/07',
    status: '現行',
    summary: '第10期已納入完整圖鑑。選擇箱不要平均分散，先看暴擊門檻、自訂典藏館與主力套組缺口。',
    actions: ['先補能啟動套組的缺件', '再補紅3暴擊門檻', '最後才追單件紅5技能'],
    sourceUrl: 'https://notalknote.xyz/10th-edition-collectibles/',
  },
  {
    id: 'legend-deconstructor',
    category: '收藏系統',
    title: '傳奇收藏品解構機：換流派前先算回收',
    updated: '2026/04/08',
    status: '現行',
    summary: '解構功能讓高階帳號能重新分配稀缺收藏資源；使用前要先確認回收內容、目標收藏與自訂典藏館是否會掉檔。',
    actions: ['先截圖目前典藏館與套組門檻', '計算回收後能否直達目標斷點', '確認完成後再拆，不做半套轉換'],
    sourceUrl: 'https://notalknote.xyz/survivor-io-legend-deconstructor-explained/',
  },
  {
    id: 'custom-collection',
    category: '收藏系統',
    title: '自訂典藏館：欄位、星數與終局收益',
    updated: '2026/03/08',
    status: '現行',
    summary: '自訂典藏館的欄位成本會快速上升，傳奇收藏品能帶來暴擊傷害、技能傷害與異常增傷；先開能填滿的欄位最有效率。',
    actions: ['欄位數至少等於可放入的高星收藏品', '優先達成傳奇件數與總星數門檻', '不要為空欄位提前消耗大量收藏之心'],
    sourceUrl: 'https://notalknote.xyz/custom-collection/',
  },
  {
    id: 'collection-sets',
    category: '收藏系統',
    title: '收藏品套組：先看門檻再選期數',
    updated: '2025/05/23',
    status: '常駐',
    summary: '套組可能要求持有件數、單件紅星或總紅星。選擇箱應該投給最接近啟動下一階效果的期數，而不是只看單件評分。',
    actions: ['盤點缺件與總紅星', '比較下一階效果所需碎片', '只集中一個最近能完成的套組'],
    sourceUrl: 'https://notalknote.xyz/collectible-sets/',
  },
  {
    id: 'tech-parts',
    category: '科技配件',
    title: '科技配件總表：三攻三防與取得路線',
    updated: '2025/02/21',
    status: '常駐',
    summary: '科技配件一次配置三個攻擊與三個防禦配件，會直接改變主動技能。終局資源仍應集中在主力配件與下一個合成斷點。',
    actions: ['攻擊配件先完成無人機主線', '防禦配件依關卡生存需求配置', '自選箱集中，不平均升級'],
    sourceUrl: 'https://notalknote.xyz/techparts/',
  },
  {
    id: 'tech-resonance',
    category: '科技配件',
    title: '科技諧振：主配件與輔助配件配置',
    updated: '2024/10/31',
    status: '需版本核對',
    summary: '諧振以傳奇主配件搭配至少史詩品質的輔助配件，依能量門檻解鎖增益。舊文章可查基本規則，實際開放配件以遊戲內為準。',
    actions: ['先確認主配件已開啟諧振', '用閒置高品質配件補能量', '每跨一個門檻再比較傷害提升'],
    sourceUrl: 'https://notalknote.xyz/tech-parts-resonance/',
  },
  {
    id: 'twinborn-parts',
    category: '科技配件',
    title: '雙生配件：合成條件與模式切換',
    updated: '2025/02/21',
    status: '常駐',
    summary: '取得傳奇科技配件後可解鎖雙生系統，由攻擊與生命配件組合。合成前先決定主模式，避免收藏品與諧振資源投錯形態。',
    actions: ['先選無人機、足球或其他主形態', '確認兩個素材不會破壞現有配裝', '同步調整對應收藏品與套組'],
    sourceUrl: 'https://notalknote.xyz/twinborn-parts/',
  },
  {
    id: 'mount-system',
    category: '最新系統',
    title: '載具系統：屬性、技能與投資順序',
    updated: '2026/04/25',
    status: '現行',
    summary: '載具是獨立養成線，會提供屬性與戰鬥效果。高階帳號可投入，但不應犧牲神器核心、主力科技與角色斷點。',
    actions: ['先確認載具效果適用的模式', '只升能跨越技能斷點的階段', '與神器核心、異寵核心一起比較成本'],
    sourceUrl: 'https://notalknote.xyz/survivorio-mount-system-ultimate-guide/',
  },
  {
    id: 'ss-belt-comparison',
    category: '裝備養成',
    title: '星鑄腰帶與扭曲腰帶：何時才該換',
    updated: '2026/03/09',
    status: '現行',
    summary: '裝備排名不能脫離神器核心與模式。星鑄腰帶未達必要神鑄節點時，已成形的扭曲腰帶仍可能提供更穩定的實戰收益。',
    actions: ['用目前核心數比較，不看滿配結論', '分別測試首領與關卡模式', '新腰帶未過斷點前保留舊裝'],
    sourceUrl: 'https://notalknote.xyz/survivor-io-twisting-belt-vs-ss-belt-meta-guide/',
  },
  {
    id: 'chaos-fusion',
    category: '裝備養成',
    title: '混沌融合：終局裝備的核心分配',
    updated: '2025/04/13',
    status: '常駐',
    summary: '混沌融合屬於終局裝備投資，應該以完整配裝的下一個有效斷點分配核心，不要為了單件面板拆散整套。',
    actions: ['列出每件裝備下一個有效節點', '優先主武器與全域乘區', '保留可讓整套同時跨檔的核心'],
    sourceUrl: 'https://notalknote.xyz/chaos-fusion/',
  },
  {
    id: 'astral-forge-cost',
    category: '裝備養成',
    title: '神鑄消耗：升級前的材料清單',
    updated: '2025/04/13',
    status: '常駐',
    summary: '神鑄前先查每階消耗與素材來源，確定投入後能直接取得有用效果；只增加面板、沒有改變實戰的節點可以延後。',
    actions: ['先列神器核心與三系核心存量', '標記下一個能改變玩法的節點', '保留活動自選箱直到升級當天'],
    sourceUrl: 'https://notalknote.xyz/%e3%80%90%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e3%80%91%e7%a5%9e%e9%91%84%e6%b6%88%e8%80%97/',
  },
  {
    id: 'survivor-awakening',
    category: '特工寵物',
    title: '特工覺醒：核心、碎片與連攜技能',
    updated: '2026/01/24',
    status: '常駐',
    summary: '覺醒需要角色碎片、量子碎片與覺醒核心，並會開啟連攜被動。高階帳號要以主角色與可共用的連攜技能安排順序。',
    actions: ['主角色先完成必要覺醒', '第二順位選能提供連攜技能的角色', '不要分散覺醒核心到不上場角色'],
    sourceUrl: 'https://notalknote.xyz/survivor-awakening/',
  },
  {
    id: 'survivor-synergy',
    category: '特工寵物',
    title: '特工同調與協同作戰',
    updated: '2025/08/01',
    status: '需版本核對',
    summary: '同調系統會統一角色基礎等級並開放協同作戰；啟動與升級材料昂貴，應先確認主角色與兩個協同位置的長期配置。',
    actions: ['先確認同調解鎖條件', '協同角色看技能，不只看稀有度', '升級前比較角色碎片與覺醒核心缺口'],
    sourceUrl: 'https://notalknote.xyz/survivor-synergy-system/',
  },
  {
    id: 'pet-system',
    category: '特工寵物',
    title: '寵物技能、覺醒與助戰配置',
    updated: '2025/08/20',
    status: '需版本核對',
    summary: '舊寵物養成可查出戰、助戰、性格與覺醒規則；異世寵物推出後，舊強度排行只能作過渡參考，不能直接當終局答案。',
    actions: ['過渡期看鷹鴿鴿與皮皮德', '助戰技能依主寵需求選擇', '終局改用異世寵物與整體增傷比較'],
    sourceUrl: 'https://notalknote.xyz/survivoriopet-system/',
  },
  {
    id: 'characters',
    category: '特工寵物',
    title: '完整角色資料與取得方式',
    updated: '2026/01/24',
    status: '需版本核對',
    summary: '角色總表適合查取得、升星與技能，但角色強度會隨新特工與協同系統改變；本站配裝結論仍以目前版本實戰為準。',
    actions: ['先查角色取得與碎片需求', '再看覺醒與協同價值', '過期排行只當歷史資料'],
    sourceUrl: 'https://notalknote.xyz/%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e6%96%b0%e8%a7%92%e8%89%b2/',
  },
  {
    id: 'skill-evolution',
    category: '關卡活動',
    title: '技能等級與突破合成速查',
    updated: '2024/08/20',
    status: '需版本核對',
    summary: '可用來快速查主動技能與被動技能的突破組合；雙生科技與新技能加入後，仍需以遊戲內顯示確認最新合成條件。',
    actions: ['開局前記住主力技能的被動需求', '保留一格給模式必要輔助', '新技能以遊戲內突破提示為準'],
    sourceUrl: 'https://notalknote.xyz/%e3%80%90%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e3%80%91%e6%8a%80%e8%83%bd%e7%ad%89%e7%b4%9a%e5%8f%8a%e7%aa%81%e7%a0%b4%e5%90%88%e6%88%90%e8%a1%a8/',
  },
  {
    id: 'chapter-126-plus',
    category: '關卡活動',
    title: '第126關以後的關卡資料入口',
    updated: '2024/05/18',
    status: '需版本核對',
    summary: '舊關卡文章可查地圖與怪物機制；目前主線已大幅超過該範圍，建議只用來查特定舊關卡，不作全版本通關結論。',
    actions: ['先用關卡編號搜尋', '只取地圖與怪物機制', '裝備與角色建議改用本站目前配裝'],
    sourceUrl: 'https://notalknote.xyz/%e3%80%90%e5%99%a0%e5%99%a0%e7%89%b9%e6%94%bb%e3%80%91%e9%80%9a%e9%97%9c%e6%94%bb%e7%95%a5%e7%ac%ac126%e9%97%9c/',
  },
];

export const LATEST_SOURCE_FALLBACK = [
  {
    title: '4週年活動總結與資源投入心得',
    date: '2026/08/28',
    link: 'https://notalknote.xyz/dadasurvivor-4th-anniversary-event-review/',
  },
  {
    title: '區域行動全面改版攻略',
    date: '2026/08/27',
    link: 'https://notalknote.xyz/dadasurvivor-regional-action-update-guide/',
  },
  {
    title: '4週年彩虹骰攻略',
    date: '2026/08/24',
    link: 'https://notalknote.xyz/survivor-io-4th-anniversary-rainbow-dice-ultimate-guide/',
  },
  {
    title: '幽暗之靈完整解析',
    date: '2026/08/22',
    link: 'https://notalknote.xyz/survivor-io-umbral-soul-pet-guide-2026/',
  },
  {
    title: '4週年彩虹礦攻略',
    date: '2026/08/18',
    link: 'https://notalknote.xyz/survivor-io-4th-anniversary-rainbow-mine-event-guide/',
  },
  {
    title: '4週年彩虹棋補償解析',
    date: '2026/08/16',
    link: 'https://notalknote.xyz/survivor-io-4th-anniversary-rainbow-chess-400-tickets-pity-compensation-guide/',
  },
];
