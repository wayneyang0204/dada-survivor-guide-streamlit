'use client';

import Image from 'next/image';
import {
  AlertTriangle,
  ArrowDown,
  CheckCircle2,
  CircleDollarSign,
  Crosshair,
  Flame,
  Gauge,
  RotateCcw,
  Sparkles,
} from 'lucide-react';
import { useMemo, useState } from 'react';

import { Button } from '@/components/ui/button';
import { BUILDS } from '@/lib/guide-data';

type MainStage = 'venato' | 'taloxa-r5' | 'taloxa-building' | 'unsure';
type ChaosStage = '18-plus' | '9-17' | 'below-9';
type PlayMode = 'short' | 'long' | 'zone';
type DivineStage = 'complete' | 'nezha' | 'none';

const DEFAULTS = {
  mainStage: 'taloxa-r5' as MainStage,
  chaosStage: '9-17' as ChaosStage,
  playMode: 'short' as PlayMode,
  divineStage: 'none' as DivineStage,
};

const mainOptions: { value: MainStage; label: string; hint: string }[] = [
  {
    value: 'venato',
    label: 'Venato R5+ ＋塔洛莎 R4+',
    hint: '已達真正轉主位門檻',
  },
  {
    value: 'taloxa-r5',
    label: '塔洛莎 R5+、基礎暴率 70%+',
    hint: '多數高端帳號在這裡',
  },
  {
    value: 'taloxa-building',
    label: '塔洛莎 R1–R4／暴率未滿 70%',
    hint: '還在建立主位門檻',
  },
  {
    value: 'unsure',
    label: '都未達／我不確定',
    hint: '先給你安全投資順序',
  },
];

const chaosOptions: { value: ChaosStage; label: string }[] = [
  { value: '18-plus', label: '18 以上' },
  { value: '9-17', label: '9–17' },
  { value: 'below-9', label: '未滿 9／不確定' },
];

const modeOptions: { value: PlayMode; label: string }[] = [
  { value: 'short', label: '短場頭目' },
  { value: 'long', label: '長場頭目' },
  { value: 'zone', label: '區域行動' },
];

const divineOptions: { value: DivineStage; label: string }[] = [
  { value: 'complete', label: '哪吒 R2+ ＋ 伏爾坎 R1+' },
  { value: 'nezha', label: '只有哪吒' },
  { value: 'none', label: '都沒有／不確定' },
];

function ChoiceGroup<T extends string>({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: T;
  options: { value: T; label: string; hint?: string }[];
  onChange: (value: T) => void;
}) {
  return (
    <fieldset>
      <legend className="mb-2 text-xs font-black uppercase tracking-[.12em] text-white/55">
        {label}
      </legend>
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
              className={`h-auto min-h-11 justify-start whitespace-normal px-3 py-2 text-left ${
                active
                  ? 'border-[#d8ff57] bg-[#d8ff57] text-[#0b1f1e] hover:bg-[#d8ff57]/90'
                  : 'border-white/10 bg-white/[0.05] text-white hover:bg-white/10'
              }`}
            >
              <span>
                <span className="block text-xs font-black leading-5">{option.label}</span>
                {option.hint && (
                  <span className={`block text-[10px] font-semibold ${active ? 'opacity-65' : 'text-white/45'}`}>
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
  const [chaosStage, setChaosStage] = useState<ChaosStage>(DEFAULTS.chaosStage);
  const [playMode, setPlayMode] = useState<PlayMode>(DEFAULTS.playMode);
  const [divineStage, setDivineStage] = useState<DivineStage>(DEFAULTS.divineStage);

  const recommendation = useMemo(() => {
    const buildIndex = playMode === 'short' ? 0 : playMode === 'long' ? 1 : 2;
    const build = BUILDS[buildIndex];

    const main = {
      venato: {
        title: 'Venato 主位，塔洛莎放協同',
        reason: '你已達轉換門檻，現在才是 Venato 真正超過塔洛莎的區間。',
        action: '資源集中 Venato R5→R7，塔洛莎保留 R4 以上做協同。',
        avoid: '不要把塔洛莎吃掉或降到無法當協同。',
      },
      'taloxa-r5': {
        title: '繼續塔洛莎主位，先別硬轉 Venato',
        reason: '低星 Venato 不會自動贏；必須能直接做出 R5 Venato＋R4 塔洛莎才值得換。',
        action: '先存好一次到位的轉換資源，裝備與異獸繼續服務塔洛莎。',
        avoid: '不要做 R1–R4 Venato 當過渡，會同時削弱主位與協同。',
      },
      'taloxa-building': {
        title: '塔洛莎主位，第一優先推到 R5',
        reason: '你還沒跨過塔洛莎的主要爆發門檻，現在分資源給 Venato 會更慢。',
        action: '先補基礎暴率到 70% 左右，再完成塔洛莎 R5。',
        avoid: '先不投 Venato，也不要為伏爾坎延後主位突破。',
      },
      unsure: {
        title: '維持你現有最強主位，先建立塔洛莎',
        reason: '資訊不足時，最安全路線是完成塔洛莎的暴率與 R5 門檻。',
        action: '先查角色突破與基礎暴率；達標前保留轉換箱與通用資源。',
        avoid: '不要因新角色上線就把資源平均分散。',
      },
    }[mainStage];

    const chaos = {
      '18-plus': 'Chaos 18 已達高階重算點：長場可重新比較腰帶與項鍊。',
      '9-17': 'Chaos 9 已能用終局骨架；下一個明確目標是 18。',
      'below-9': 'Chaos 未滿 9：先補到 9，不要直接照抄 Chaos 18 的長場配置。',
    }[chaosStage];

    const divine = {
      complete: '神火鏈已完成：哪吒放 Teamwork，被動吃伏爾坎加成；兩者都不是主位。',
      nezha: '先保留哪吒；主位與裝備門檻完成後，再補伏爾坎 R1。',
      none: '先跳過伏爾坎；資源優先放在主位、雙生槍與裝備門檻。',
    }[divineStage];

    return { build, main, chaos, divine };
  }, [chaosStage, divineStage, mainStage, playMode]);

  function reset() {
    setMainStage(DEFAULTS.mainStage);
    setChaosStage(DEFAULTS.chaosStage);
    setPlayMode(DEFAULTS.playMode);
    setDivineStage(DEFAULTS.divineStage);
  }

  return (
    <section
      id="advisor"
      className="scroll-mt-24 overflow-hidden rounded-[28px] border border-white/10 bg-[#0b1f1e] shadow-[0_30px_90px_rgba(0,0,0,.35)]"
      aria-labelledby="advisor-title"
    >
      <div className="border-b border-white/10 bg-gradient-to-r from-[#173c39] to-[#0b1f1e] p-5 sm:p-6">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex -space-x-2">
              {[
                ['/characters/taloxa-guide.jpg', '塔洛莎'],
                ['/characters/venato-guide.jpg', '維納托'],
              ].map(([src, alt]) => (
                <span key={src} className="relative size-10 overflow-hidden rounded-full border-2 border-[#173c39] bg-white/10">
                  <Image src={src} alt={alt} fill className="object-cover" sizes="40px" />
                </span>
              ))}
            </div>
            <div>
              <p className="text-[10px] font-black uppercase tracking-[.18em] text-[#d8ff57]">
                30 秒配裝診斷
              </p>
              <h2 id="advisor-title" className="text-lg font-black text-white sm:text-xl">
                依你現在的帳號給答案
              </h2>
            </div>
          </div>
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={reset}
            aria-label="恢復高端帳號預設值"
            className="text-white/55 hover:bg-white/10 hover:text-white"
          >
            <RotateCcw />
          </Button>
        </div>
        <p className="mt-3 text-xs font-semibold leading-5 text-white/55">
          已先套用「塔洛莎 R5＋Chaos 9–17」高端常見狀態。把不符合的選項改掉，答案會立即更新。
        </p>
      </div>

      <div className="grid gap-5 p-5 sm:p-6 xl:grid-cols-[1fr_.94fr]">
        <div className="space-y-5">
          <ChoiceGroup
            label="1｜你的主位門檻"
            value={mainStage}
            options={mainOptions}
            onChange={setMainStage}
          />
          <div className="grid gap-5 sm:grid-cols-2">
            <ChoiceGroup
              label="2｜Chaos Power"
              value={chaosStage}
              options={chaosOptions}
              onChange={setChaosStage}
            />
            <ChoiceGroup
              label="3｜你最在意的模式"
              value={playMode}
              options={modeOptions}
              onChange={setPlayMode}
            />
          </div>
          <ChoiceGroup
            label="4｜神火支援進度"
            value={divineStage}
            options={divineOptions}
            onChange={setDivineStage}
          />
          <div className="flex items-center gap-2 text-[11px] font-semibold text-white/40">
            <Gauge className="size-3.5" />
            不知道 Chaos 或基礎暴率，就選「不確定」，不會叫你亂花資源。
          </div>
        </div>

        <div aria-live="polite" className="rounded-2xl bg-[#d8ff57] p-5 text-[#0b1f1e] sm:p-6">
          <div className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[.16em] opacity-55">
            <Sparkles className="size-4" />
            你的最佳建議
          </div>
          <h3 className="mt-3 text-2xl font-black leading-tight">
            {recommendation.main.title}
          </h3>
          <p className="mt-2 text-sm font-semibold leading-6 opacity-70">
            {recommendation.main.reason}
          </p>

          <div className="mt-5 space-y-3">
            <div className="rounded-xl bg-[#0b1f1e] p-3.5 text-[#f8ffe1]">
              <p className="flex items-center gap-2 text-xs font-black text-[#d8ff57]">
                <Crosshair className="size-4" /> 目前直接用
              </p>
              <p className="mt-1.5 text-sm font-black">{recommendation.build.name}</p>
              <p className="mt-1 text-xs font-semibold leading-5 text-white/60">
                {recommendation.build.weapon}
              </p>
            </div>

            <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
              <div className="rounded-xl bg-[#0b1f1e]/8 p-3">
                <p className="flex items-center gap-1.5 text-xs font-black">
                  <CheckCircle2 className="size-4" /> 下一步
                </p>
                <p className="mt-1 text-xs font-bold leading-5 opacity-70">
                  {recommendation.main.action}
                </p>
              </div>
              <div className="rounded-xl bg-[#0b1f1e]/8 p-3">
                <p className="flex items-center gap-1.5 text-xs font-black">
                  <AlertTriangle className="size-4" /> 先不要
                </p>
                <p className="mt-1 text-xs font-bold leading-5 opacity-70">
                  {recommendation.main.avoid}
                </p>
              </div>
            </div>

            <div className="space-y-2 border-t border-[#0b1f1e]/15 pt-3 text-xs font-bold leading-5">
              <p className="flex gap-2">
                <CircleDollarSign className="mt-0.5 size-4 shrink-0" />
                {recommendation.chaos}
              </p>
              <p className="flex gap-2">
                <Flame className="mt-0.5 size-4 shrink-0" />
                {recommendation.divine}
              </p>
            </div>
          </div>

          <a
            href="#builds"
            className="mt-5 inline-flex items-center gap-1.5 text-xs font-black underline decoration-2 underline-offset-4"
          >
            看這套的完整裝備 <ArrowDown className="size-3.5" />
          </a>
        </div>
      </div>
    </section>
  );
}
