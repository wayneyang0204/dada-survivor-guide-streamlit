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
import { BUILDS, COLLECTIBLE_ADVICE, COLLECTIBLE_FREEZE, GEAR_ADVICE } from '@/lib/guide-data';

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
    hint: '現在該點：維納托覺醒8',
  },
  {
    value: 'venato',
    label: '維納托覺醒5～6階＋塔洛莎覺醒4階以上',
    hint: '現在該點：維納托覺醒7',
  },
  {
    value: 'taloxa-r5',
    label: '塔洛莎覺醒5階以上、基礎暴率70%以上',
    hint: '現在先存，不要半套轉職',
  },
  {
    value: 'taloxa-building',
    label: '塔洛莎覺醒1至4階／暴率未滿70%',
    hint: '現在該點：塔洛莎覺醒5',
  },
  {
    value: 'unsure',
    label: '都未達／我不確定',
    hint: '先對三個數字再花資源',
  },
];

const weaponOptions: { value: WeaponStage; label: string; hint: string }[] = [
  {
    value: 'e4-xt',
    label: '雙生槍永恆4＋虛空4，已開異界轉化',
    hint: '雙生槍夠了，神器核心改堆混沌',
  },
  {
    value: 'e3v2',
    label: '雙生槍永恆3＋虛空2以上，未滿 E4V4',
    hint: '現在該點：永恆4＋虛空4',
  },
  {
    value: 'e1v2',
    label: '雙生槍永恆1＋虛空2 骨架',
    hint: '現在該點：永恆3＋虛空2',
  },
  {
    value: 'pre',
    label: '還在用苦無／虛空之力／未達雙生槍',
    hint: '現在先做出雙生槍',
  },
];

const chaosOptions: { value: ChaosStage; label: string; hint: string }[] = [
  { value: '27-plus', label: '27以上（切月鐮刀）', hint: '現在該點：混沌36' },
  { value: '18-26', label: '18至26（神罰之斧）', hint: '現在該點：混沌27' },
  { value: '9-17', label: '9至17（混沌之風）', hint: '現在該點：混沌18' },
  { value: 'below-9', label: '未滿9／不確定', hint: '現在該點：混沌9' },
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
    hint: '神火先維持，核心不要改投',
  },
  { value: 'nezha', label: '只有哪吒', hint: '伏爾坎先不要點' },
  { value: 'none', label: '都沒有／不確定', hint: '神火這條先跳過' },
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
    <fieldset className="rounded-xl border border-white/8 bg-white/[0.035] p-3">
      <legend className="sr-only">{label}</legend>
      <div className="mb-2 flex items-center gap-2">
        <span className="grid size-5 place-items-center rounded-full bg-[#d8ff57] text-[10px] font-black text-[#0b1f1e]">
          {step}
        </span>
        <p className="text-xs font-black text-white">{label}</p>
      </div>
      <div className="grid gap-1.5 sm:grid-cols-2" role="group" aria-label={label}>
        {options.map((option) => {
          const active = value === option.value;
          return (
            <Button
              key={option.value}
              type="button"
              variant="outline"
              aria-pressed={active}
              onClick={() => onChange(option.value)}
              className={`h-auto min-h-10 justify-start whitespace-normal rounded-lg px-2.5 py-2 text-left ${
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
        phase: '現在只做三件事',
        title: '覺醒核心點維納托到8，神器核心點混沌到36',
        reason: '一次只追一個數字。角色停在覺醒8、武器停在混沌36、異寵停在幽冥覺醒5。沒到這三個數字以前，不要改裝備，也不要練第二個主位。',
        actionTitle: '覺醒核心全部拿去點維納托覺醒8',
        stop: '維納托覺醒8',
        action: '打開維納托，把覺醒核心一直點到畫面顯示覺醒8。還沒到8以前：不要點梅塔莉亞、不要點楊大師、不要開第二主位、不要拆塔洛莎覺醒4。',
        avoid: '不要把覺醒核心分給其他角色，也不要為了同調拆掉塔洛莎覺醒4。',
        switchCondition: '維納托覺醒8點上後，剩下的覺醒核心才拿去點左協同梅塔莉亞覺醒1、右協同楊大師覺醒1。',
      },
      venato: {
        phase: '現在只追一個數字',
        title: '覺醒核心只點維納托，點到覺醒7停',
        reason: '覺醒5只代表可以轉主位。現在唯一要做的是把維納托點到覺醒7。',
        actionTitle: '覺醒核心全部拿去點維納托覺醒7',
        stop: '維納托覺醒7',
        action: '打開維納托，點到覺醒7就停。還沒到7以前：不要點別人、不要拆塔洛莎覺醒4。',
        avoid: '不要在覺醒7以前改練第二主位，也不要把覺醒核心平均分給不上場角色。',
        switchCondition: '覺醒7點上後，下一檔才是維納托覺醒8。',
      },
      'taloxa-r5': {
        phase: '現在先存，不要轉',
        title: '繼續用塔洛莎，先存滿維納托覺醒5',
        reason: '半套轉職會變弱。存到能一次點完維納托覺醒5，並且塔洛莎還留得住覺醒4，再轉。',
        actionTitle: '先存轉換包，不要半套轉職',
        stop: '存滿維納托覺醒5',
        action: '塔洛莎繼續上場。覺醒核心與通用碎片先囤著，等到「維納托能一次點完覺醒5、塔洛莎還留得住覺醒4」再轉。',
        avoid: '不要做覺醒1至4階維納托過渡，也不要把通用角色資源平均分配。',
        switchCondition: '兩人門檻同時夠了再轉，不要先轉再補。',
      },
      'taloxa-building': {
        phase: '現在只做塔洛莎',
        title: '先把暴率補到70%，再點塔洛莎覺醒5',
        reason: '現在還在第一個主位。分資源給維納托或伏爾坎，只會更慢成形。',
        actionTitle: '先補暴率70%，再點塔洛莎覺醒5',
        stop: '塔洛莎覺醒5',
        action: '不含場內觸發的基礎暴率先到約70%，然後把塔洛莎點到覺醒5。這兩件事沒好以前不要談轉職。',
        avoid: '先不投維納托，也不要為伏爾坎延後塔洛莎。',
        switchCondition: '塔洛莎覺醒5完成後，才開始存維納托轉換包。',
      },
      unsure: {
        phase: '先對三個數字',
        title: '先看畫面數字，再花稀缺資源',
        reason: '主位與暴率沒對上時，大額轉換很容易變弱。',
        actionTitle: '先核對三個數字再花資源',
        stop: '核對完三個數字',
        action: '打開角色頁與屬性頁，記下塔洛莎覺醒、維納托覺醒、不含場內觸發的基礎暴率。對完再回來改左側選項。',
        avoid: '不要因新角色推出就開選擇箱或消耗通用突破資源。',
        switchCondition: '三個數字確認後，改左側選項，清單會重算。',
      },
    }[mainStage];

    const weapon = {
      'e4-xt': {
        title: '神器核心拿去堆下一個混沌檔',
        detail: '雙生槍已經夠用。神器核心不要再點苦無，全部拿去把混沌之力點到下一檔。',
        spend: '神器核心',
        stop: '下一檔混沌',
      },
      e3v2: {
        title: '神器核心先把雙生槍補到永恆4＋虛空4',
        detail: '打開雙生槍，點到永恆4與虛空4就停，再開異界轉化1。還沒到以前：不要先堆混沌36，也不要換其他主武器。',
        spend: '神器核心',
        stop: '雙生槍E4V4',
      },
      e1v2: {
        title: '神器核心先把雙生槍補到永恆3＋虛空2',
        detail: '打開雙生槍，點到永恆3與虛空2就停。還沒到以前不要換苦無。',
        spend: '神器核心',
        stop: '雙生槍E3V2',
      },
      pre: {
        title: '先做出雙生槍，當天點永恆1',
        detail: '苦無與虛空之力現在不要再當主武器。做出雙生槍的當天，用1個神器核心點永恆神鑄1。',
        spend: '神器核心',
        stop: '雙生槍＋永恆1',
      },
    }[weaponStage];

    const chaos = {
      '27-plus': {
        label: '現在點武器',
        title: '神器核心全部拿去堆混沌36',
        detail: '打開混沌融合之力，用神器核心點到36（能量雙刀）就停。還沒到36以前：項鍊繼續穿破壞者徽記，不要換成審判項鍊，也不要改腰帶、手套。',
        next: '混沌36',
        spend: '神器核心',
        stop: '混沌36',
      },
      '18-26': {
        label: '現在點武器',
        title: '神器核心全部拿去堆混沌27',
        detail: '打開混沌融合之力，點到27（切月鐮刀）就停。還沒到27以前：項鍊繼續穿破壞者徽記，不要改腰帶。',
        next: '混沌27',
        spend: '神器核心',
        stop: '混沌27',
      },
      '9-17': {
        label: '現在點武器',
        title: '神器核心全部拿去堆混沌18',
        detail: '打開混沌融合之力，點到18（神罰之斧）就停。還沒到18以前：不要換腰帶項鍊，也不要回頭用苦無。',
        next: '混沌18',
        spend: '神器核心',
        stop: '混沌18',
      },
      'below-9': {
        label: '現在點武器',
        title: '神器核心先把混沌之力補到9',
        detail: '打開混沌融合之力，先點到9（混沌之風）就停。沒到9以前，不要照抄切月鐮刀或永恆4配置。',
        next: '混沌9',
        spend: '神器核心',
        stop: '混沌9',
      },
    }[chaosStage];

    const lateSupport = {
      title: '連攜槽只給現在這三人',
      detail: '多出來的連攜槽依序放：塔洛莎、梅塔莉亞、楊大師。不要放不上場的角色。',
      spend: '連攜槽',
      stop: '三人連攜就好',
    };

    const lateSystems = {
      title: '異世核心全部拿去點幽冥之魂覺醒5',
      detail: '打開異寵幽冥之魂，點到覺醒5就停。還沒到覺醒5以前：晶片不要先給雙生無人機，腰帶、手套、項鍊先別動。',
      spend: '異世核心',
      stop: '幽冥之魂覺醒5',
    };

    const divine = {
      complete: {
        title: '哪吒與伏爾坎先維持，不要改主位',
        detail: '這兩人只當神火支援。覺醒核心先給維納托，不要拿去把他們改成主位。',
        spend: '先不動',
        stop: '先不動神火',
      },
      nezha: {
        title: '伏爾坎先不要點',
        detail: '維納托覺醒7以前，覺醒核心不要分給伏爾坎。主位過關後再補伏爾坎覺醒1。',
        spend: '先不動',
        stop: '先不動伏爾坎',
      },
      none: {
        title: '神火這條先跳過',
        detail: '現在的覺醒核心給主位。哪吒、伏爾坎都還沒有就先不要追。',
        spend: '先不動',
        stop: '先跳過神火',
      },
    }[divineStage];

    const mode = {
      short: {
        label: '短場頭目',
        instruction: '雙生槍已是後期主武器；進化交給 E4 與異界轉化，技能格優先雙生無人機與冷卻，不要再練苦無。',
      },
      long: {
        label: '長場頭目',
        instruction: '讓混沌27、共鳴、燃燒／虛弱／裂傷完整疊滿；項鍊繼續穿破壞者徽記，等混沌36與審判項鍊雙生階成形再 A/B。',
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
      { id: 'main', spend: '覺醒核心', stop: main.stop, title: main.actionTitle, detail: main.action },
      { id: 'loadout', spend: loadout.spend ?? '神器核心', stop: loadout.stop, title: loadout.title, detail: loadout.detail },
      { id: 'support', spend: third.spend ?? '其餘資源', stop: third.stop, title: third.title, detail: third.detail },
    ];

    const gear = GEAR_ADVICE[playMode].map((item) => {
      if (chaosStage === '27-plus') return item;
      if (item.slot === '項鍊') {
        return { ...item, spend: '先不動', freeze: `繼續穿破壞者徽記。混沌${chaos.next}以前不要換成審判項鍊` };
      }
      if (item.slot === '手套' || item.slot === '腰帶') {
        return { ...item, spend: '先不動', freeze: `混沌${chaos.next}以前不要改這格` };
      }
      return item;
    });
    const collectibles = COLLECTIBLE_ADVICE;

    return { build, main, chaos, support: third, mode, completeness, priorities, gear, collectibles };
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
                現在該點哪個數字
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
              右側先看四個停點，再往下看六格裝備與三件收藏。沒點到以前，不要改裝備、不要練第二主位。若還沒到這裡，改左側選項後會立刻重算。
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

          <div className="mt-5 grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
            {[
              ['現在點角色', recommendation.priorities[0].stop],
              ['現在點武器', recommendation.priorities[1].stop],
              ['現在點異寵', recommendation.priorities[2].stop],
              ['現在升收藏', `${recommendation.collectibles[0].name} ${recommendation.collectibles[0].stop}`],
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
                  <Target className="size-4" /> 照這個順序做，點到數字就停
                </p>
                <p className="mt-1 text-xs font-semibold opacity-50">每條線只用一種核心。沒點到停點以前，不要開始下一項。</p>
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
                      <span className="flex flex-wrap items-center gap-2 text-xs font-black">
                        <span className="grid size-5 place-items-center rounded-full bg-[#0b1f1e] text-[10px] text-[#d8ff57]">{index + 1}</span>
                        <span className="rounded-full bg-[#0b1f1e] px-2 py-0.5 text-[10px] font-black text-[#d8ff57]">{item.spend}</span>
                        {item.title}
                      </span>
                      <span className="mt-1.5 inline-flex rounded-full bg-[#d8ff57] px-2 py-0.5 text-[10px] font-black text-[#0b1f1e]">
                        做到這裡就停：{item.stop}
                      </span>
                      <span className="mt-1.5 block text-xs font-semibold leading-5 opacity-60">{item.detail}</span>
                    </span>
                  </label>
                );
              })}
            </div>
          </div>

          <div id="gear-plan" className="mt-4 scroll-mt-24 rounded-2xl border border-[#0b1f1e]/12 bg-white/60 p-4 sm:p-5">
            <p className="text-sm font-black">現在穿這六格</p>
            <p className="mt-1 text-xs font-semibold opacity-50">項鍊現在穿破壞者徽記就對了。審判項鍊是之後才拿來比的，不是現在該換的。</p>
            <div className="mt-3 overflow-x-auto">
              <table className="w-full min-w-[520px] text-left text-xs">
                <thead>
                  <tr className="border-b border-[#0b1f1e]/10 text-[10px] font-black tracking-wider opacity-45">
                    <th className="py-2 pr-3">槽位</th>
                    <th className="py-2 pr-3">現在穿</th>
                    <th className="py-2 pr-3">核心拿去</th>
                    <th className="py-2">沒好以前不要</th>
                  </tr>
                </thead>
                <tbody>
                  {recommendation.gear.map((item) => (
                    <tr key={item.slot} className="border-b border-[#0b1f1e]/8 align-top">
                      <td className="py-2.5 pr-3 font-black">{item.slot}</td>
                      <td className="py-2.5 pr-3 font-bold leading-5">{item.wear}</td>
                      <td className="py-2.5 pr-3 font-black text-[#0b1f1e]">{item.spend}</td>
                      <td className="py-2.5 font-semibold leading-5 opacity-60">{item.freeze}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div id="collectible-plan" className="mt-4 scroll-mt-24 rounded-2xl border border-[#0b1f1e]/12 bg-white/60 p-4 sm:p-5">
            <p className="text-sm font-black">現在只升這三件收藏</p>
            <p className="mt-1 text-xs font-semibold opacity-50">用自選箱或收藏之心。缺哪件補哪件，不要平均升星。</p>
            <div className="mt-3 space-y-2">
              {recommendation.collectibles.map((item, index) => (
                <div key={item.name} className="rounded-xl border border-[#0b1f1e]/10 bg-[#f8ffe1] p-3">
                  <p className="flex flex-wrap items-center gap-2 text-xs font-black">
                    <span className="grid size-5 place-items-center rounded-full bg-[#0b1f1e] text-[10px] text-[#d8ff57]">{index + 1}</span>
                    <span className="rounded-full bg-[#0b1f1e] px-2 py-0.5 text-[10px] font-black text-[#d8ff57]">{item.spend}</span>
                    {item.name}
                  </p>
                  <span className="mt-1.5 inline-flex rounded-full bg-[#d8ff57] px-2 py-0.5 text-[10px] font-black text-[#0b1f1e]">
                    做到這裡就停：{item.stop}
                  </span>
                  <p className="mt-1.5 text-xs font-semibold leading-5 opacity-60">{item.why}</p>
                </div>
              ))}
            </div>
            <p className="mt-3 text-xs font-bold leading-5 text-red-950/70">{COLLECTIBLE_FREEZE}</p>
          </div>

          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl border border-red-950/10 bg-red-950/[0.06] p-4">
              <p className="flex items-center gap-2 text-xs font-black text-red-950/80"><LockKeyhole className="size-4" /> 還沒點到以前，不要做這些</p>
              <p className="mt-2 text-xs font-bold leading-5 text-red-950/60">{recommendation.main.avoid}</p>
            </div>
            <div className="rounded-xl border border-[#0b1f1e]/10 bg-[#d8ff57]/55 p-4">
              <p className="flex items-center gap-2 text-xs font-black"><Route className="size-4" /> 點到以後才可以做</p>
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
              三套模式的完整技能 <ArrowDown className="size-3.5" />
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
