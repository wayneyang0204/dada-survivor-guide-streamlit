export type GuideCategory = '武器' | '技能' | '角色' | '關卡';

export type CharacterId =
  | 'venato'
  | 'taloxa'
  | 'nezha'
  | 'vulcan'
  | 'metallia'
  | 'umbral-soul';

export type CharacterProfile = {
  id: CharacterId;
  nameZh: string;
  nameEn: string;
  kind: '生存者' | '神火生存者' | '異獸';
  role: string;
  summary: string;
  image: string;
  imageAlt: string;
  sourceName: string;
  sourceUrl: string;
};

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
    '全新料理主題活動預告',
  ],
  sources: [
    {
      name: '蘋果商店｜官方',
      url: 'https://apps.apple.com/us/app/survivor-io/id1528941310',
    },
    {
      name: '安卓商店｜官方',
      url: 'https://play.google.com/store/apps/details?id=com.dxx.firenow&hl=en_US',
    },
  ],
};

export const GUIDES: Guide[] = [
  {
    id: 'drone-evolution',
    category: '技能',
    title: '無人機合成：毀滅者的正確養成順序',
    description: '兩種無人機何時拿？如何避免前期卡格，兼顧清怪與頭目輸出。',
    level: '新手',
    readTime: '4 分鐘',
    updated: '8/29',
    tags: ['無人機', '技能合成', '頭目'],
    takeaways: ['前期先確保一項穩定清怪技能', '兩種無人機皆滿級後可合成毀滅者', '合成後空出一格，可補單體輸出'],
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
    title: '伏爾坎：他不是終局主位',
    description: '整理官方已公開資訊與目前仍待實測部分，避免新角色推出就一次梭哈。',
    level: '進階',
    readTime: '5 分鐘',
    updated: '8/28',
    tags: ['伏爾坎', '神火角色', '神火支援'],
    takeaways: ['伏爾坎主要強化哪吒的神火被動', '先把哪吒推到覺醒1階以上，伏爾坎才開始有價值', '終局配裝中的主位通常是維納托或塔洛莎，不是伏爾坎'],
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

export const CHARACTER_GLOSSARY: CharacterProfile[] = [
  {
    id: 'venato',
    nameZh: '維納托',
    nameEn: '維納托',
    kind: '生存者',
    role: '真終局主位',
    summary: '資源與覺醒門檻都很高；通常要能組出覺醒5階維納托＋覺醒4階塔洛莎，再考慮從塔洛莎轉主位。',
    image: '/characters/venato-guide.jpg',
    imageAlt: '《噠噠特攻》生存者維納托的角色畫面',
    sourceName: '玩家角色實測影片',
    sourceUrl: 'https://www.youtube.com/watch?v=B-lmUhtuH3g',
  },
  {
    id: 'taloxa',
    nameZh: '塔洛莎',
    nameEn: '塔洛莎',
    kind: '生存者',
    role: '後期主位／終局協同',
    summary: '基礎暴率約 70% 以上開始發力；覺醒5階前後是多數高端帳號的核心，轉維納托後仍可當強力協同。',
    image: '/characters/taloxa-guide.jpg',
    imageAlt: '《噠噠特攻》生存者塔洛莎的角色畫面',
    sourceName: '玩家角色介紹影片',
    sourceUrl: 'https://www.youtube.com/watch?v=SPWy0pNX5YQ',
  },
  {
    id: 'nezha',
    nameZh: '哪吒',
    nameEn: '哪吒',
    kind: '神火生存者',
    role: '協同被動',
    summary: '提供神火傷害的起點，主要放在協同被動欄位；這條神火鏈先投資哪吒，再考慮伏爾坎。',
    image: '/characters/nezha-guide.jpg',
    imageAlt: '《噠噠特攻》神火生存者哪吒的角色畫面',
    sourceName: '玩家角色介紹影片',
    sourceUrl: 'https://www.youtube.com/watch?v=qB49TkoZuXE',
  },
  {
    id: 'vulcan',
    nameZh: '伏爾坎',
    nameEn: '伏爾坎',
    kind: '神火生存者',
    role: '全域被動支援',
    summary: '不是上場主位，也不必佔協同欄位；覺醒1階起主要強化哪吒的神火效果，沒有哪吒覺醒1階時先不要投。',
    image: '/characters/vulcan-guide.jpg',
    imageAlt: '《噠噠特攻》神火生存者伏爾坎的角色畫面',
    sourceName: '玩家角色介紹影片',
    sourceUrl: 'https://www.youtube.com/watch?v=r8LE32kgQ1c',
  },
  {
    id: 'metallia',
    nameZh: '梅塔莉亞',
    nameEn: '梅塔莉亞',
    kind: '生存者',
    role: '異常狀態／協同支援',
    summary: '搖滾歌手造型的 S 級生存者；終局更常拿來補毒、冰、虛弱等異常狀態與協同，而非固定主位。',
    image: '/characters/metallia-guide.jpg',
    imageAlt: '《噠噠特攻》生存者梅塔莉亞的角色宣傳畫面',
    sourceName: '玩家角色攻略站',
    sourceUrl: 'https://www.allclash.com/best-build-for-metallia-in-survivor-io-gear-weapon-skill-choices/',
  },
  {
    id: 'umbral-soul',
    nameZh: '幽冥之魂',
    nameEn: '幽冥之魂',
    kind: '異獸',
    role: '共鳴／傷害支援',
    summary: '牠是異獸，不是角色。配裝裡看到牠時，要到異獸與共鳴欄位處理。',
    image: '/characters/umbral-soul-official.webp',
    imageAlt: '《噠噠特攻》異獸幽冥之魂的官方活動圖',
    sourceName: '官方活動圖',
    sourceUrl: 'https://apps.apple.com/us/app/survivor-io/id1528941310?eventid=6799857083',
  },
];

export const BUILDS = [
  {
    name: '短時頭目爆發天花板',
    mode: '短場頭目／公會遠征',
    hero: '維納托覺醒5階以上主位｜塔洛莎覺醒4階協同；神火：哪吒覺醒2階以上 → 伏爾坎覺醒1階以上',
    pet: '幽冥之魂覺醒3階以上｜共鳴增益＋共鳴傷害',
    characterIds: ['venato', 'taloxa', 'nezha', 'vulcan', 'umbral-soul'] as CharacterId[],
    weapon: '雙生之槍｜永恆神鑄4、虛空神鑄4、混沌神鑄2以上、異界轉化',
    gear: [
      '虛空項鍊（神鑄3）／審判項鍊（雙生階，依計算器）',
      '月痕護腕（雙生階）｜基礎暴率至少 70%',
      '星塵腰帶（雙生階、永恆神鑄3、虛空神鑄2）',
      '冰川戰靴（雙生階、永恆神鑄1、虛空神鑄2、混沌神鑄1）',
      '永虛戰甲（雙生階、永恆神鑄3起）',
    ],
    skills: ['雙生槍', '雙生無人機', '燃燒瓶', '足球', '鑽頭', '雷電'],
    stats: { clear: 84, boss: 100, safety: 82 },
    note: '以最快進化與首領增傷為核心；短場先確保雙生槍永恆神鑄1，技能格優先無人機與冷卻。',
    breakpoint: '門檻：基礎暴率 70–100%、雙生槍至少永恆神鑄1＋虛空神鑄2；未達門檻時神鑄3虛空手套通常更強。',
  },
  {
    name: '長戰疊層傷害極限',
    mode: '長線首領',
    hero: '維納托覺醒5至7階主位｜塔洛莎覺醒4階＋梅塔莉亞／楊大師覺醒1階協同',
    pet: '幽冥之魂｜保護＋共鳴增益＋共鳴傷害',
    characterIds: ['venato', 'taloxa', 'metallia', 'nezha', 'vulcan', 'umbral-soul'] as CharacterId[],
    weapon: '雙生之槍｜永恆神鑄4、虛空神鑄4；混沌之力9／18門檻',
    gear: [
      '審判項鍊（雙生階、高暴率）／虛空項鍊（神鑄3）',
      '月痕護腕（雙生階、永恆神鑄1、虛空神鑄2以上）',
      '星塵腰帶（雙生階）；收藏滿門檻才測神鑄3扭曲腰帶',
      '冰川戰靴（雙生階、永恆神鑄1、虛空神鑄2、混沌神鑄1）',
      '永虛戰甲（雙生階、永恆神鑄3、虛空神鑄2、混沌神鑄2）',
    ],
    skills: ['雙生槍', '雙生無人機', '燃油桶', '量子球', '永恆鑽頭', '超級雷暴'],
    stats: { clear: 88, boss: 99, safety: 90 },
    note: '長場讓混沌之力與寵物共鳴完整疊滿；燃燒、虛弱與冰凍觸發要配合你的異界轉化詞條。',
    breakpoint: '門檻：混沌之力9起跳、永虛甲至少永恆神鑄3；混沌之力18後再重算腰帶與項鍊。',
  },
  {
    name: '區域行動零失誤配置',
    mode: '區域行動／341–345章',
    hero: '塔洛莎覺醒5階穩定主位／維納托覺醒5階高投入；詞條關再調整梅塔莉亞協同',
    pet: '幽冥之魂／高星控制型異獸',
    characterIds: ['taloxa', 'venato', 'metallia', 'umbral-soul'] as CharacterId[],
    weapon: '雙生之槍（永恆神鑄4、虛空神鑄4）；特殊詞條關可切虛空之力',
    gear: [
      '虛空項鍊（神鑄3）',
      '月痕護腕（雙生階）／虛空手套（神鑄3）',
      '星塵腰帶（雙生階、永恆神鑄3、虛空神鑄2）',
      '冰川戰靴（雙生階、永恆神鑄1、虛空神鑄2、混沌神鑄1）',
      '亡者風衣（神鑄3、死神流）／永虛甲（雙生階、永恆神鑄3）',
    ],
    skills: ['雙生無人機', '燃油桶', '守衛者', '量子球', '力場', '高爆燃料'],
    stats: { clear: 100, boss: 90, safety: 98 },
    note: '不是堆面板，而是針對詞條保證通關；極端怪潮用死神流，禁復活關改永虛甲。',
    breakpoint: '門檻：亡者風衣必須神鑄3才值得當核心；若關卡禁復活或限制護盾，依詞條切換。',
  },
];

export const STARTER_TASKS = [
  '確認基礎暴率（不含戰鬥觸發）是否達 70%',
  '記下雙生槍的永恆、虛空、混沌神鑄與混沌之力',
  '確認塔洛莎／維納托的實際突破等級',
  '確認哪吒與伏爾坎是否達神火支援門檻',
];
