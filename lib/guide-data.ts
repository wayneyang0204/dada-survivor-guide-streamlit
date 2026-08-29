export type GuideCategory = '武器' | '技能' | '角色' | '關卡';

export type Guide = {
  id: string;
  category: GuideCategory;
  title: string;
  description: string;
  level: '新手' | '進階' | '高難';
  readTime: string;
  updated: string;
  tags: string[];
  takeaways: string[];
};

export const OFFICIAL_UPDATE = {
  version: '5.1.0',
  checkedAt: '2026-08-29 09:00',
  headline: '四週年慶典持續進行中',
  summary:
    '官方商店版本資訊已加入主線 341–345 章與挑戰章節，足球模式「量子奈米機器人」共鳴超載即將登場。',
  bullets: [
    '新增主線 341–345 章與對應挑戰章節',
    '週年限定「彩虹骰子」與「音樂唱片爭奪」活動',
    '足球模式共鳴超載即將推出',
    '全新活動「Soup Kitchen」預告',
  ],
  sources: [
    {
      name: 'App Store｜HABBY',
      url: 'https://apps.apple.com/us/app/survivor-io/id1528941310',
    },
    {
      name: 'Google Play｜HABBY',
      url: 'https://play.google.com/store/apps/details?id=com.dxx.firenow&hl=en_US',
    },
  ],
};

export const GUIDES: Guide[] = [
  {
    id: 'drone-evolution',
    category: '技能',
    title: '無人機合成：毀滅者的正確養成順序',
    description: 'A、B 型無人機何時拿？如何避免前期卡格，兼顧清怪與頭目輸出。',
    level: '新手',
    readTime: '4 分鐘',
    updated: '8/29',
    tags: ['無人機', '技能合成', '頭目'],
    takeaways: ['前期先確保一項穩定清怪技能', 'A、B 型皆滿級後可合成毀滅者', '合成後空出一格，可補單體輸出'],
  },
  {
    id: 'kunai-build',
    category: '武器',
    title: '苦無推圖流：低操作也能穩定過關',
    description: '自動追蹤、容錯高，整理苦無從開荒到紅裝的技能優先級。',
    level: '新手',
    readTime: '6 分鐘',
    updated: '8/29',
    tags: ['苦無', '推圖', '無課'],
    takeaways: ['苦無搭配甲賀忍法帖進化', '優先補足範圍清怪技能', '頭目戰保持距離，讓自動追蹤全程命中'],
  },
  {
    id: 'soccer-overload',
    category: '技能',
    title: '足球模式共鳴超載：更新前準備清單',
    description: '依官方 5.1.0 預告，先整理量子球與相關科技零件的養成資源。',
    level: '進階',
    readTime: '5 分鐘',
    updated: '8/29',
    tags: ['足球', '量子球', '5.1.0'],
    takeaways: ['保留足球相關科技零件與晶片', '正式數值公開前不要盲目拆解舊配置', '上線後優先在頭目模式測試單體增益'],
  },
  {
    id: 'chapter-341',
    category: '關卡',
    title: '341–345 章：生存壓力與技能選擇',
    description: '新章節開荒先看：清怪、續航與頭目輸出的三階段配置思路。',
    level: '高難',
    readTime: '8 分鐘',
    updated: '8/29',
    tags: ['341章', '345章', '推圖'],
    takeaways: ['前五分鐘優先成形範圍技能', '中段保留磁鐵與補給品控場', '最後一格留給高倍率單體輸出'],
  },
  {
    id: 'vulcan-overview',
    category: '角色',
    title: 'SP 神火角色 Vulcan：資源投資觀察',
    description: '整理官方已公開資訊與目前仍待實測部分，避免新角色推出就一次梭哈。',
    level: '進階',
    readTime: '5 分鐘',
    updated: '8/28',
    tags: ['Vulcan', 'SP角色', '資源規劃'],
    takeaways: ['先看既有隊伍是否已成形', '保留重置與升星資源直到完整測試', '活動兌換以通用資源優先'],
  },
  {
    id: 'guardian-combo',
    category: '技能',
    title: '守衛者＋外骨骼：新手最穩控場組',
    description: '擊退、擋飛行物與持續旋轉，適合怪潮密集的直線與小型地圖。',
    level: '新手',
    readTime: '3 分鐘',
    updated: '8/27',
    tags: ['守衛者', '控場', '新手'],
    takeaways: ['搭配外骨骼裝甲完成進化', '怪物免疫擊退時需補傷害', '守衛者不是主要頭目輸出'],
  },
  {
    id: 'boss-burst',
    category: '武器',
    title: '頭目爆發流：輸出窗口怎麼抓',
    description: '把追蹤技能、冷卻縮減與走位節奏排在一起，減少空轉傷害。',
    level: '進階',
    readTime: '7 分鐘',
    updated: '8/26',
    tags: ['頭目', '爆發', '冷卻'],
    takeaways: ['以無人機與追蹤類技能作主軸', '冷卻與攻擊被動優先升級', '先躲招再貪輸出，死亡就是零傷害'],
  },
  {
    id: 'anniversary-plan',
    category: '關卡',
    title: '四週年回鍋：7 天資源規劃',
    description: '從登入獎勵、彩虹活動到裝備整理，安排每天最划算的行動。',
    level: '新手',
    readTime: '6 分鐘',
    updated: '8/29',
    tags: ['四週年', '回鍋', '活動'],
    takeaways: ['先完成每日免費與可累積任務', '不要為低階獎池提早花完寶石', '通用選擇箱保留到確認缺口再開'],
  },
];

export const BUILDS = [
  {
    name: '短時頭目爆發天花板',
    mode: 'EE／公會遠征',
    hero: '哪吒高覺醒主位＋Vulcan R1–R4 被動',
    pet: 'Umbral Soul R3+｜共鳴增益＋共鳴傷害',
    weapon: '雙生之槍 E4V4・C2+・Xeno Transmute',
    gear: [
      'AF3 虛空項鍊／SS 審判項鍊（依計算器）',
      'SS 月痕護腕｜基礎暴率至少 70%',
      'SS 星塵腰帶 E3V2',
      'SS 冰川戰靴 E1V2C1',
      'SS 永虛戰甲 E3 起',
    ],
    skills: ['雙生槍', '雙生無人機', '燃燒瓶', '足球', '鑽頭', '雷電'],
    stats: { clear: 84, boss: 100, safety: 82 },
    note: '以最快進化與首領增傷為核心；短場先確保雙生槍 E1，技能格優先無人機與冷卻。',
    breakpoint: '門檻：基礎暴率 70–100%、雙生槍至少 E1V2；未達門檻時 AF3 虛空手套通常更強。',
  },
  {
    name: '長戰疊層傷害極限',
    mode: 'LME／長線首領',
    hero: '哪吒覺醒矩陣＋神火支援位',
    pet: 'Umbral Soul｜保護＋共鳴增益＋共鳴傷害',
    weapon: '雙生之槍 E4V4・Chaos 9／18 門檻',
    gear: [
      'SS 審判項鍊（高暴率）／AF3 虛空項鍊',
      'SS 月痕護腕 E1V2 以上',
      'SS 星塵腰帶；收藏滿門檻才測 AF3 扭曲腰帶',
      'SS 冰川戰靴 E1V2C1',
      'SS 永虛戰甲 E3V2C2',
    ],
    skills: ['雙生槍', '雙生無人機', '燃油桶', '量子球', '永恆鑽頭', '超級雷暴'],
    stats: { clear: 88, boss: 99, safety: 90 },
    note: '長場讓 Chaos 與寵物共鳴完整疊滿；燃燒、虛弱與冰凍觸發要配合你的 XT 詞條。',
    breakpoint: '門檻：Chaos Power 9 起跳、永虛甲至少 E3；Chaos 18 後再重算腰帶與項鍊。',
  },
  {
    name: '區域行動零失誤配置',
    mode: 'Zone Ops／341–345',
    hero: '高覺醒主力｜哪吒優先，弱點關再切 Metallia',
    pet: 'Umbral Soul／高星控制型異獸',
    weapon: '雙生之槍 E4V4；特殊詞條關可切虛空之力',
    gear: [
      'AF3 虛空項鍊',
      'SS 月痕護腕／AF3 虛空手套',
      'SS 星塵腰帶 E3V2',
      'SS 冰川戰靴 E1V2C1',
      'AF3 亡者風衣（死神流）／SS 永虛甲 E3',
    ],
    skills: ['雙生無人機', '燃油桶', '守衛者', '量子球', '力場', '高爆燃料'],
    stats: { clear: 100, boss: 90, safety: 98 },
    note: '不是堆面板，而是針對詞條保證通關；極端怪潮用死神流，禁復活關改永虛甲。',
    breakpoint: '門檻：亡者風衣必須 AF3 才值得當核心；若關卡禁復活或限制護盾，依詞條切換。',
  },
];

export const STARTER_TASKS = [
  '把主武器升到優良品質',
  '完成一組技能進化組合',
  '每日巡邏收益領滿',
  '保留選擇箱，確認缺口再開',
];
