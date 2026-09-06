'use client';

import Image from 'next/image';
import {
  AlertTriangle,
  ArrowDown,
  BadgeCheck,
  CheckCircle2,
  ChevronRight,
  CircleDollarSign,
  Crosshair,
  Flame,
  Gauge,
  LockKeyhole,
  RotateCcw,
  Route,
  ShieldCheck,
  Target,
} from 'lucide-react';
import { useMemo, useState } from 'react';

import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Progress,
  ProgressLabel,
  ProgressValue,
} from '@/components/ui/progress';
import { BUILDS } from '@/lib/guide-data';

type MainStage = 'venato-a7' | 'venato' | 'taloxa-r5' | 'taloxa-building' | 'unsure';
type WeaponStage = 'e4-xt' | 'e3v2' | 'e1v2' | 'pre';
type ChaosStage = '27-plus' | '18-26' | '9-17' | 'below-9';
type PlayMode = 'short' | 'long' | 'zone';
type DivineStage = 'complete' | 'nezha' | 'none';

const DEFAULTS = {
  mainStage: 'venato-a7' as MainStage,
  weaponStage: 'e4-xt' as WeaponStage,
  chaosStage: '27-plus' as ChaosStage,
  playMode: 'short' as PlayMode,
  divineStage: 'complete' as DivineStage,
};

const mainOptions: { value: MainStage; label: string; hint: string }[] = [
  {
    value: 'venato-a7',
    label: '維納托覺醒7階以上＋塔洛莎覺醒4階協同',
    hint: '後期帳號：下一刀是覺醒8與協同',
  },
  {
    value: 'venato',
    label: '維納托覺醒5～6階＋塔洛莎覺醒4階以上',
    hint: '已轉主位，下一刀是覺醒7',
  },
  {
    value: 'taloxa-r5',
    label: '塔洛莎覺醒5階以上、基礎暴率70%以上',
    hint: '還沒轉維納托的成熟帳號',
  },
  {
    value: 'taloxa-building',
    label: '塔洛莎覺醒1至4階／暴率未滿70%',
    hint: '還在建立第一個主位門檻',
  },
  {
    value: 'unsure',
    label: '都未達／我不確定',
    hint: '採用保守投資路線',
  },
];

const weaponOptions: { value: WeaponStage; label: string; hint: string }[] = [
  {
    value: 'e4-xt',
    label: '雙生槍永恆4＋虛空4，已開異界轉化',
    hint: '後期武器骨架',
  },
  {
    value: 'e3v2',
    label: '雙生槍永恆3＋虛空2以上，未滿 E4V4',
    hint: '下一刀是異界轉化',
  },
  {
    value: 'e1v2',
    label: '雙生槍永恆1＋虛空2 骨架',
    hint: '只解決進化速度',
  },
  {
    value: 'pre',
    label: '還在用苦無／虛空之力／未達雙生槍',
    hint: '武器線仍在開荒',
  },
];

const chaosOptions: { value: ChaosStage; label: string; hint: string }[] = [
  { value: '27-plus', label: '27以上（切月鐮刀）', hint: '後期武器進化線' },
  { value: '18-26', label: '18至26（神罰之斧）', hint: '下一刀是27' },
  { value: '9-17', label: '9至17（混沌之風）', hint: '下一站是18' },
  { value: 'below-9', label: '未滿9／不確定', hint: '先補基本門檻' },
];

const modeOptions: { value: PlayMode; label: string; hint: string }[] = [
  { value: 'short', label: '短場頭目', hint: '末世反響、公會遠征' },
  { value: 'long', label: '長場頭目', hint: '疊層與共鳴完整發揮' },
  { value: 'zone', label: '區域行動', hint: '穩定通關優先' },
];

const divineOptions: { value: DivineStage; label: string; hint: string }[] = [
  {
    value: 'complete',
    label: '哪吒覺醒2階以上＋伏爾坎覺醒1階以上',
    hint: '神火支援鏈完整',
  },
  { value: 'nezha', label: '只有哪吒', hint: '伏爾坎排在主位門檻之後' },
  { value: 'none', label: '都沒有／不確定', hint: '先跳過神火投資' },
];

function ChoiceGroup<T extends string>({
  step,
  label,
  value,
  options,
  onChange,
}: {
  step: number;
  label: string;
  value: T;
  options: { value: T; label: string; hint?: string }[];
  onChange: (value: T) => void;
}) {
  return (
    <fieldset className="rounded-2xl border border-white/8 bg-white/[0.035] p-4">
      <legend className="sr-only">{label}</legend>
      <div className="mb-3 flex items-center gap-2">
        <span className="grid size-6 place-items-center rounded-full bg-[#d8ff57] text-[11px] font-black text-[#0b1f1e]">
          {step}
        </span>
        <p className="text-sm font-black text-white">{label}</p>
      </div>
      <div className="grid gap-2 sm:grid-cols-2" role="group" aria-label={label}>
        {options.map((option) => {
          const active = value === option.value;
          return (
            <Button
              key={option.value}
              type="button"
              variant="outline"
              aria-pressed={active}
              onClick={() => onChange(option.value)}
              className={`h-auto min-h-12 justify-start whitespace-normal rounded-xl px-3 py-2.5 text-left ${
                active
                  ? 'border-[#d8ff57] bg-[#d8ff57] text-[#0b1f1e] hover:bg-[#d8ff57]/90'
                  : 'border-white/10 bg-transparent text-white hover:border-white/20 hover:bg-white/[0.06]'
              }`}
            >
              <span>
                <span className="block text-xs font-black leading-5">{option.label}</span>
                {option.hint && (
                  <span className={`block text-[10px] font-semibold leading-4 ${active ? 'opacity-60' : 'text-white/40'}`}>
                    {option.hint}
                  </span>
                )}
              </span>
            </Button>
          );
        })}
      </div>
    </fieldset>
  );
}

export default function AccountAdvisor() {
  const [mainStage, setMainStage] = useState<MainStage>(DEFAULTS.mainStage);
  const [weaponStage, setWeaponStage] = useState<WeaponStage>(DEFAULTS.weaponStage);
  const [chaosStage, setChaosStage] = useState<ChaosStage>(DEFAULTS.chaosStage);
  const [playMode, setPlayMode] = useState<PlayMode>(DEFAULTS.playMode);
  const [divineStage, setDivineStage] = useState<DivineStage>(DEFAULTS.divineStage);
  const [completed, setCompleted] = useState<string[]>([]);

  const recommendation = useMemo(() => {
    const buildIndex = playMode === 'short' ? 0 : playMode === 'long' ? 1 : 2;
    const build = BUILDS[buildIndex];

    const main = {
      'venato-a7': {
        phase: '覺醒8與協同成形期',
        title: '維納托已過覺醒7，改推覺醒8與協同乘區',
        reason: '首領傷害+60%已經到手。角色計畫若還停在覺醒5轉職或塔洛莎養成，會把後期帳號拉回前期。',
        actionTitle: '推維納托覺醒8，並補滿現役協同',
        action: '覺醒8解鎖第四連攜槽與每層額外6%傷害。左協同優先梅塔莉亞覺醒1以上，右協同楊大師覺醒1以上；塔洛莎維持覺醒4以上提供裂傷。',
        avoid: '不要把通用覺醒核心再砸進第二個主位，也不要為了同調等級拆掉塔洛莎裂傷門檻。',
        switchCondition: '覺醒8完成後，角色主線改比協同紅星與連攜被動，不再回頭練過渡主位。',
      },
      venato: {
        phase: '轉主位後的覺醒7斷點',
        title: '維納托主位已成立，下一刀是覺醒7',
        reason: '覺醒5只是轉換門檻，還不是後期天花板。覺醒7才會拿到首領+60%，並把強化腎上腺素初始等級拉到5。',
        actionTitle: '先把維納托推到覺醒7',
        action: '通用角色資源只服務維納托覺醒7；塔洛莎維持覺醒4以上，不要拆掉裂傷協同。',
        avoid: '不要在覺醒7以前改練第二主位，也不要把覺醒核心平均分給不上場角色。',
        switchCondition: '覺醒7完成後，角色計畫改成覺醒8、左協同梅塔莉亞與右協同楊大師。',
      },
      'taloxa-r5': {
        phase: '轉職準備期',
        title: '塔洛莎繼續主位，暫時不要轉維納托',
        reason: '低覺醒維納托不會自動更強；現在轉換會同時失去成熟主位與高階協同。',
        actionTitle: '維持塔洛莎主位',
        action: '先存到能一次完成覺醒5階維納托，並同時保留覺醒4階塔洛莎，再一次轉換。',
        avoid: '不要做覺醒1至4階維納托過渡，也不要把通用角色資源平均分配。',
        switchCondition: '覺醒5階維納托＋覺醒4階塔洛莎同時成立後再轉。',
      },
      'taloxa-building': {
        phase: '主位養成期',
        title: '塔洛莎主位，第一目標是覺醒5階',
        reason: '目前還沒跨過塔洛莎的主要爆發門檻，分資源給其他主位只會延後成形。',
        actionTitle: '先完成塔洛莎門檻',
        action: '基礎暴率補到70%左右，接著把塔洛莎推到覺醒5階。',
        avoid: '先不投維納托，也不要為伏爾坎延後塔洛莎突破。',
        switchCondition: '先完成塔洛莎覺醒5階；維納托轉換仍是更後面的階段。',
      },
      unsure: {
        phase: '資料確認期',
        title: '維持現有最強主位，資源先不要分散',
        reason: '主位與暴率資料不完整時，任何大額轉換都可能讓帳號實際變弱。',
        actionTitle: '先完成帳號盤點',
        action: '確認塔洛莎、維納托突破與不含場內觸發的基礎暴率，再決定轉換。',
        avoid: '不要因新角色推出就開選擇箱或消耗通用突破資源。',
        switchCondition: '確認角色突破與基礎暴率後，再依上方選項重新診斷。',
      },
    }[mainStage];

    const weapon = {
      'e4-xt': {
        title: '雙生槍改追混沌27與異界觸發',
        detail: 'E4V4與異界轉化已是後期骨架，不是終點。下一刀把混沌之力堆到27切月鐮刀，異界轉發條件用固定首領做 A/B。',
      },
      e3v2: {
        title: '雙生槍先推到 E4V4',
        detail: 'E3V2 只能開混沌融合，還解不了異界轉化。神器核心先補永恆4與虛空4，再開異界轉化1。',
      },
      e1v2: {
        title: '雙生槍先補到 E3V2',
        detail: '永恆1只解決進化速度，不是後期武器計畫。接著把永恆與虛空補到 E3V2，再開混沌融合。',
      },
      pre: {
        title: '先換成雙生槍並立刻永恆1',
        detail: '苦無與虛空之力不再當後期主武器。做出雙生槍當天就把永恆神鑄1點上，不要繼續練開荒武器。',
      },
    }[weaponStage];

    const chaos = {
      '27-plus': {
        label: '武器進化線',
        title: '比較混沌36／45與 SS 裝',
        detail: '切月鐮刀已解。下一刀比較混沌36能量雙刀、45終極聖劍，以及審判項鍊／星塵腰帶雙生階；不要退回神鑄3虛空手套。',
        next: '混沌36／45',
      },
      '18-26': {
        label: '下一進化',
        title: '混沌之力推到27切月鐮刀',
        detail: '神罰之斧已解，這不是武器終點。先把全體 SS 混沌星堆到27，再微調項鍊與腰帶。',
        next: '混沌之力27',
      },
      '9-17': {
        label: '下一斷點',
        title: '混沌之力推到18神罰之斧',
        detail: '混沌之風已能用；18以前不要頻繁更換腰帶與項鍊，也不要回頭用苦無。',
        next: '混沌之力18',
      },
      'below-9': {
        label: '第一斷點',
        title: '混沌之力先補到9',
        detail: '未滿9時先完成混沌之風門檻，不要直接照抄混沌27的切月鐮刀配置。',
        next: '混沌之力9',
      },
    }[chaosStage];

    const divine = {
      complete: {
        title: '維持完整神火支援鏈',
        detail: '哪吒放協同被動並獲得伏爾坎加成；兩者都不改成主位。',
      },
      nezha: {
        title: '先保留哪吒，再補伏爾坎',
        detail: '主位覺醒7以前不要為伏爾坎延後維納托；達標後再把伏爾坎補到覺醒1階。',
      },
      none: {
        title: '暫時跳過神火投資',
        detail: '通用資源先放主位覺醒與協同裂傷，伏爾坎不是現在的優先項。',
      },
    }[divineStage];

    const lateSupport = {
      title: '連攜被動只服務現役三人',
      detail: '覺醒6／8多出來的連攜槽，優先放塔洛莎裂傷、梅塔莉亞異常或楊大師易傷；不要塞不上場角色。',
    };

    const lateSystems = {
      title: '異寵、科技與 SS 裝一起補',
      detail: '幽冥之魂優先覺醒5；科技先雙生無人機諧振。星塵腰帶至少永恆3，月痕護腕要基礎暴率70%以上才當後期手套，不要退回神鑄3虛空手套。',
    };

    const mode = {
      short: {
        label: '短場頭目',
        instruction: '雙生槍已是後期主武器；進化交給 E4 與異界轉化，技能格優先雙生無人機與冷卻，不要再練苦無。',
      },
      long: {
        label: '長場頭目',
        instruction: '讓混沌27、共鳴、燃燒／虛弱／裂傷完整疊滿；項鍊腰帶只做雙生階 A/B，不退回神鑄3單系。',
      },
      zone: {
        label: '區域行動',
        instruction: '新版不帶入局外裝備；先手操小關拿 Buff。舊章節或詞條關才切亡者風衣或永虛戰甲。',
      },
    }[playMode];

    const completeness =
      100 -
      (mainStage === 'unsure' ? 20 : 0) -
      (weaponStage === 'pre' ? 15 : weaponStage === 'e1v2' ? 8 : 0) -
      (chaosStage === 'below-9' ? 10 : chaosStage === '9-17' ? 5 : 0) -
      (divineStage === 'none' ? 8 : 0);

    const loadout = weaponStage === 'e4-xt' ? chaos : weapon;
    const third =
      mainStage === 'venato-a7' && divineStage === 'complete'
        ? weaponStage === 'e4-xt'
          ? lateSystems
          : lateSupport
        : divine;
    const priorities = [
      { id: 'main', title: main.actionTitle, detail: main.action },
      { id: 'loadout', title: loadout.title, detail: loadout.detail },
      { id: 'support', title: third.title, detail: third.detail },
    ];

    return { build, main, chaos, support: third, mode, completeness, priorities };
  }, [chaosStage, divineStage, mainStage, playMode, weaponStage]);

  function clearProgress() {
    setCompleted([]);
  }

  function reset() {
    setMainStage(DEFAULTS.mainStage);
    setWeaponStage(DEFAULTS.weaponStage);
    setChaosStage(DEFAULTS.chaosStage);
    setPlayMode(DEFAULTS.playMode);
    setDivineStage(DEFAULTS.divineStage);
    clearProgress();
  }

  function toggleCompleted(id: string, checked: boolean) {
    setCompleted((current) =>
      checked
        ? [...current.filter((item) => item !== id), id]
        : current.filter((item) => item !== id),
    );
  }

  const progress = Math.round((completed.length / recommendation.priorities.length) * 100);

  return (
    <section
      id="advisor"
      className="scroll-mt-24 overflow-hidden rounded-[30px] border border-white/10 bg-[#0b1f1e] shadow-[0_30px_90px_rgba(0,0,0,.35)]"
      aria-labelledby="advisor-title"
    >
      <div className="border-b border-white/10 bg-gradient-to-r from-[#173c39] to-[#0b1f1e] px-5 py-5 sm:px-7">
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
          <div className="flex items-center gap-3">
            <div className="flex -space-x-2">
              {[
                ['/characters/taloxa-guide.jpg', '塔洛莎'],
                ['/characters/venato-guide.jpg', '維納托'],
              ].map(([src, alt]) => (
                <span key={src} className="relative size-11 overflow-hidden rounded-full border-2 border-[#173c39] bg-white/10">
                  <Image src={src} alt={alt} fill className="object-cover" sizes="44px" />
                </span>
              ))}
            </div>
            <div>
              <p className="text-[10px] font-black tracking-[.18em] text-[#d8ff57]">
                高端帳號決策中心
              </p>
              <h2 id="advisor-title" className="text-xl font-black text-white sm:text-2xl">
                先診斷，再照優先順序執行
              </h2>
            </div>
          </div>
          <div className="flex items-center gap-2 text-[11px] font-bold text-white/50">
            <span className="rounded-full border border-white/10 px-2.5 py-1">版本 5.1.0</span>
            <span className="rounded-full border border-white/10 px-2.5 py-1">最後查核 9月7日</span>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={reset}
              aria-label="恢復後期帳號預設值"
              className="text-white/55 hover:bg-white/10 hover:text-white"
            >
              <RotateCcw />
            </Button>
          </div>
        </div>
      </div>

      <div className="grid xl:grid-cols-[.88fr_1.12fr]">
        <div className="space-y-3 border-b border-white/10 p-4 sm:p-6 xl:border-b-0 xl:border-r">
          <div className="mb-4 flex items-start gap-3 rounded-xl border border-[#d8ff57]/15 bg-[#d8ff57]/8 p-3">
            <Gauge className="mt-0.5 size-4 shrink-0 text-[#d8ff57]" />
            <p className="text-xs font-semibold leading-5 text-white/55">
              已套用後期常見狀態：維納托覺醒7以上、雙生槍 E4V4＋異界轉化、混沌之力27、神火支援鏈完整。若還沒到這裡，改左側選項後會立刻重算。
            </p>
          </div>

          <ChoiceGroup step={1} label="目前主位與突破" value={mainStage} options={mainOptions} onChange={(value) => { setMainStage(value); clearProgress(); }} />
          <ChoiceGroup step={2} label="主武器與神鑄" value={weaponStage} options={weaponOptions} onChange={(value) => { setWeaponStage(value); clearProgress(); }} />
          <ChoiceGroup step={3} label="混沌之力" value={chaosStage} options={chaosOptions} onChange={(value) => { setChaosStage(value); clearProgress(); }} />
          <ChoiceGroup step={4} label="最重要的遊戲模式" value={playMode} options={modeOptions} onChange={(value) => { setPlayMode(value); clearProgress(); }} />
          <ChoiceGroup step={5} label="神火支援進度" value={divineStage} options={divineOptions} onChange={(value) => { setDivineStage(value); clearProgress(); }} />
        </div>

        <article aria-live="polite" className="bg-[#f8ffe1] p-4 text-[#0b1f1e] sm:p-6 lg:p-7">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-[11px] font-black tracking-[.12em] opacity-55">
              <BadgeCheck className="size-4" /> 專屬診斷結果
            </div>
            <span className="rounded-full bg-[#0b1f1e] px-3 py-1 text-[11px] font-black text-[#d8ff57]">
              {recommendation.main.phase}
            </span>
          </div>

          <h3 className="mt-4 max-w-2xl text-3xl font-black leading-[1.12] tracking-tight sm:text-4xl">
            {recommendation.main.title}
          </h3>
          <p className="mt-3 max-w-2xl text-sm font-semibold leading-6 opacity-65">
            {recommendation.main.reason}
          </p>

          <div className="mt-5 grid gap-2 sm:grid-cols-3">
            {[
              ['主要模式', recommendation.mode.label],
              [recommendation.chaos.label, recommendation.chaos.next],
              ['資料完整度', `${recommendation.completeness}%`],
            ].map(([label, value]) => (
              <div key={label} className="rounded-xl border border-[#0b1f1e]/10 bg-white/55 p-3">
                <p className="text-[10px] font-black tracking-wider opacity-45">{label}</p>
                <p className="mt-1 text-sm font-black">{value}</p>
              </div>
            ))}
          </div>

          <div id="action-plan" className="mt-6 scroll-mt-24 rounded-2xl border border-[#0b1f1e]/12 bg-white/60 p-4 sm:p-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="flex items-center gap-2 text-sm font-black">
                  <Target className="size-4" /> 你的三步行動清單
                </p>
                <p className="mt-1 text-xs font-semibold opacity-50">依序完成，不要同時分散資源。</p>
              </div>
              <span className="text-xs font-black opacity-55">{completed.length}／3</span>
            </div>
            <Progress value={progress} className="mt-3 gap-2 [&_[data-slot=progress-indicator]]:bg-[#0b1f1e] [&_[data-slot=progress-track]]:bg-[#0b1f1e]/10">
              <ProgressLabel className="sr-only">行動清單完成度</ProgressLabel>
              <ProgressValue className="sr-only" />
            </Progress>

            <div className="mt-4 space-y-2.5">
              {recommendation.priorities.map((item, index) => {
                const checked = completed.includes(item.id);
                return (
                  <label key={item.id} className={`flex cursor-pointer gap-3 rounded-xl border p-3.5 transition ${checked ? 'border-emerald-700/15 bg-emerald-700/8 opacity-60' : 'border-[#0b1f1e]/10 bg-[#f8ffe1] hover:border-[#0b1f1e]/25'}`}>
                    <Checkbox checked={checked} onCheckedChange={(next) => toggleCompleted(item.id, Boolean(next))} aria-label={`完成第${index + 1}項：${item.title}`} className="mt-0.5 border-[#0b1f1e]/25 data-checked:border-[#0b1f1e] data-checked:bg-[#0b1f1e]" />
                    <span className="min-w-0">
                      <span className="flex items-center gap-2 text-xs font-black">
                        <span className="grid size-5 place-items-center rounded-full bg-[#0b1f1e] text-[10px] text-[#d8ff57]">{index + 1}</span>
                        {item.title}
                      </span>
                      <span className="mt-1.5 block text-xs font-semibold leading-5 opacity-60">{item.detail}</span>
                    </span>
                  </label>
                );
              })}
            </div>
          </div>

          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl border border-red-950/10 bg-red-950/[0.06] p-4">
              <p className="flex items-center gap-2 text-xs font-black text-red-950/80"><LockKeyhole className="size-4" /> 資源凍結清單</p>
              <p className="mt-2 text-xs font-bold leading-5 text-red-950/60">{recommendation.main.avoid}</p>
            </div>
            <div className="rounded-xl border border-[#0b1f1e]/10 bg-[#d8ff57]/55 p-4">
              <p className="flex items-center gap-2 text-xs font-black"><Route className="size-4" /> 何時才能切換</p>
              <p className="mt-2 text-xs font-bold leading-5 opacity-65">{recommendation.main.switchCondition}</p>
            </div>
          </div>

          <div className="mt-4 rounded-2xl bg-[#0b1f1e] p-4 text-[#f8ffe1] sm:p-5">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <p className="flex items-center gap-2 text-[11px] font-black text-[#d8ff57]"><Crosshair className="size-4" /> 目前直接採用</p>
                <p className="mt-2 text-lg font-black">{recommendation.build.name}</p>
              </div>
              <span className="rounded-full border border-white/15 px-2.5 py-1 text-[10px] font-bold text-white/55">{recommendation.build.mode}</span>
            </div>
            <p className="mt-3 text-xs font-semibold leading-5 text-white/60">{recommendation.mode.instruction}</p>
            <div className="mt-3 grid gap-2 sm:grid-cols-2">
              <p className="rounded-lg bg-white/[0.06] p-3 text-xs font-bold leading-5"><ShieldCheck className="mr-1.5 inline size-3.5 text-[#d8ff57]" />{recommendation.build.weapon}</p>
              <p className="rounded-lg bg-white/[0.06] p-3 text-xs font-bold leading-5"><Flame className="mr-1.5 inline size-3.5 text-[#d8ff57]" />{recommendation.support.detail}</p>
            </div>
            <a href="#builds" className="mt-4 inline-flex items-center gap-1.5 rounded-lg bg-[#d8ff57] px-3 py-2 text-xs font-black text-[#0b1f1e] transition hover:bg-[#d8ff57]/85">
              查看完整裝備與技能 <ArrowDown className="size-3.5" />
            </a>
          </div>

          <details className="guide-details mt-4 rounded-xl border border-[#0b1f1e]/10 bg-white/40">
            <summary className="flex cursor-pointer list-none items-center justify-between px-4 py-3 text-xs font-black">
              查看判斷依據與限制 <ChevronRight className="size-4 transition-transform" />
            </summary>
            <div className="space-y-2 border-t border-[#0b1f1e]/10 px-4 py-3 text-xs font-semibold leading-5 opacity-60">
              <p className="flex gap-2"><CheckCircle2 className="mt-0.5 size-4 shrink-0" />覺醒5只是轉職線；覺醒7拿首領+60%，覺醒8才解第四連攜槽。</p>
              <p className="flex gap-2"><CircleDollarSign className="mt-0.5 size-4 shrink-0" />武器以雙生槍 E4V4、異界轉化與混沌27／36／45為後期斷點；永恆1與苦無只是開荒線。</p>
              <p className="flex gap-2"><AlertTriangle className="mt-0.5 size-4 shrink-0" />實際最優解仍會受收藏加成、遺物核心與特殊詞條影響。</p>
            </div>
          </details>
        </article>
      </div>
    </section>
  );
}
