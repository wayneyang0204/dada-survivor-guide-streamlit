'use client';

import Image from 'next/image';
import {
  ArrowRight,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  ExternalLink,
  Heart,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Swords,
  Target,
  Trophy,
  Zap,
} from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

import AccountAdvisor from '@/app/account-advisor';
import {
  BUILDS,
  CHARACTER_GLOSSARY,
  GUIDES,
  OFFICIAL_UPDATE,
  STARTER_TASKS,
  type GuideCategory,
} from '@/lib/guide-data';

const characterIndex = new Map(
  CHARACTER_GLOSSARY.map((profile) => [profile.id, profile]),
);

const categories = ['全部', '武器', '技能', '角色', '關卡', '收藏'] as const;
type Category = (typeof categories)[number];

const quickGuides: {
  icon: typeof Swords;
  label: GuideCategory;
  hint: string;
}[] = [
  { icon: Swords, label: '武器', hint: '武器排行與養成' },
  { icon: Sparkles, label: '技能', hint: '進化組合圖鑑' },
  { icon: BookOpen, label: '關卡', hint: '更新至 345 章' },
  { icon: Trophy, label: '角色', hint: '角色投資指南' },
];

const categoryStyles: Record<GuideCategory, string> = {
  武器: 'border-orange-300/20 bg-orange-300/10 text-orange-200',
  技能: 'border-cyan-300/20 bg-cyan-300/10 text-cyan-200',
  角色: 'border-violet-300/20 bg-violet-300/10 text-violet-200',
  關卡: 'border-primary/20 bg-primary/10 text-primary',
};

const buildUseWhen = [
  '你要打 EE／公會遠征，重點是最短時間爆發',
  '你要打 LME 等長場頭目，能讓 Chaos 與共鳴疊滿',
  '你要穩過區域行動或 341–345 章，不想因詞條翻車',
];

export default function GuideApp() {
  const [category, setCategory] = useState<Category>('全部');
  const [query, setQuery] = useState('');
  const [favorites, setFavorites] = useState<string[]>([]);
  const [checkedTasks, setCheckedTasks] = useState<string[]>([]);

  useEffect(() => {
    try {
      setFavorites(JSON.parse(localStorage.getItem('dada-favorites') ?? '[]'));
      setCheckedTasks(JSON.parse(localStorage.getItem('dada-starter-tasks') ?? '[]'));
    } catch {
      setFavorites([]);
      setCheckedTasks([]);
    }
  }, []);

  const filteredGuides = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return GUIDES.filter((guide) => {
      const matchesCategory =
        category === '全部' ||
        (category === '收藏'
          ? favorites.includes(guide.id)
          : guide.category === category);
      const searchable = [
        guide.title,
        guide.description,
        guide.category,
        ...guide.tags,
      ]
        .join(' ')
        .toLowerCase();
      return matchesCategory && (!needle || searchable.includes(needle));
    });
  }, [category, favorites, query]);

  function toggleFavorite(id: string) {
    setFavorites((current) => {
      const next = current.includes(id)
        ? current.filter((favorite) => favorite !== id)
        : [...current, id];
      localStorage.setItem('dada-favorites', JSON.stringify(next));
      return next;
    });
  }

  function toggleTask(task: string) {
    setCheckedTasks((current) => {
      const next = current.includes(task)
        ? current.filter((item) => item !== task)
        : [...current, task];
      localStorage.setItem('dada-starter-tasks', JSON.stringify(next));
      return next;
    });
  }

  function jumpToGuides(nextCategory: Category = '全部') {
    setCategory(nextCategory);
    document
      .getElementById('guide-library')
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  return (
    <main className="min-h-screen overflow-hidden bg-background text-foreground">
      <header className="sticky top-0 z-50 border-b border-white/8 bg-[#071719]/90 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 lg:px-8">
          <a
            className="flex items-center gap-2.5"
            href="#top"
            aria-label="噠噠特攻攻略站首頁"
          >
            <span className="grid size-9 place-items-center rounded-xl bg-primary text-lg font-black text-primary-foreground shadow-[0_0_30px_var(--primary-glow)]">
              噠
            </span>
            <span className="text-base font-black tracking-tight">噠噠攻略站</span>
          </a>
          <nav
            className="hidden items-center gap-7 text-sm font-semibold text-muted-foreground md:flex"
            aria-label="主要導覽"
          >
            <a className="transition-colors hover:text-foreground" href="#advisor">
              配裝診斷
            </a>
            <a className="transition-colors hover:text-foreground" href="#guide-library">
              攻略庫
            </a>
            <a className="transition-colors hover:text-foreground" href="#latest">
              最新情報
            </a>
            <a className="transition-colors hover:text-foreground" href="#characters">
              角色圖鑑
            </a>
            <a className="transition-colors hover:text-foreground" href="#builds">
              流派配裝
            </a>
          </nav>
          <span className="inline-flex h-5 items-center justify-center gap-1 rounded-full border border-emerald-300/20 bg-emerald-300/10 px-2 text-xs font-medium text-emerald-200">
            <span className="size-1.5 rounded-full bg-emerald-300" />
            <span className="hidden sm:inline">每日自動更新</span>
            <span className="sm:hidden">每日更新</span>
          </span>
        </div>
      </header>

      <section
        id="top"
        className="relative mx-auto max-w-7xl px-5 pb-12 pt-8 lg:px-8 lg:pb-16 lg:pt-12"
      >
        <div className="pointer-events-none absolute -left-40 top-4 size-[480px] rounded-full bg-primary/8 blur-[120px]" />
        <div className="relative z-10 mb-7 grid gap-5 lg:grid-cols-[1fr_auto] lg:items-end">
          <div>
            <span className="mb-4 inline-flex h-6 w-fit items-center rounded-full border border-primary/30 bg-primary/10 px-2.5 text-xs font-semibold text-primary">
              {OFFICIAL_UPDATE.version} 終局版 · 2026/08/29 更新
            </span>
            <h1 className="max-w-3xl text-4xl font-black leading-[1.08] tracking-[-0.04em] sm:text-5xl">
              別照抄榜單，先算出
              <span className="text-primary">你現在最強的解。</span>
            </h1>
            <p className="mt-4 max-w-2xl text-sm font-medium leading-6 text-muted-foreground sm:text-base">
              選四個帳號狀態，直接得到主位、模式配裝與下一個投資目標。看不懂英文角色名也沒關係，後面都有照片。
            </p>
          </div>
          <div className="grid grid-cols-3 gap-2 text-center text-[11px] font-black sm:min-w-[360px]">
            {[
              ['1', '選目前門檻'],
              ['2', '立刻看答案'],
              ['3', '照順序升級'],
            ].map(([step, label]) => (
              <div key={step} className="rounded-xl border border-white/8 bg-white/[0.04] px-3 py-3">
                <span className="mx-auto grid size-5 place-items-center rounded-full bg-primary text-[10px] text-primary-foreground">
                  {step}
                </span>
                <span className="mt-1.5 block text-muted-foreground">{label}</span>
              </div>
            ))}
          </div>
        </div>

        <AccountAdvisor />
      </section>

      <section className="mx-auto max-w-7xl px-5 pb-18 lg:px-8">
        <div className="mb-5 flex items-end justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.18em] text-primary">
              快速入口
            </p>
            <h2 className="mt-1 text-2xl font-black">你現在想查什麼？</h2>
          </div>
          <button
            className="hidden items-center gap-1 text-sm font-bold text-primary sm:flex"
            onClick={() => jumpToGuides()}
            type="button"
          >
            瀏覽全部 <ArrowRight className="size-4" />
          </button>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {quickGuides.map(({ icon: Icon, label, hint }) => (
            <button
              key={label}
              type="button"
              onClick={() => jumpToGuides(label)}
              className="group flex items-center gap-4 rounded-2xl border border-white/8 bg-card p-5 text-left transition-all hover:-translate-y-1 hover:border-primary/35 hover:bg-card/80"
            >
              <span className="grid size-12 place-items-center rounded-2xl bg-primary/10 text-primary">
                <Icon className="size-5" />
              </span>
              <span className="flex-1">
                <strong className="block text-base">{label}攻略</strong>
                <span className="mt-1 block text-xs text-muted-foreground">
                  {hint}
                </span>
              </span>
              <ChevronRight className="size-4 text-muted-foreground transition-transform group-hover:translate-x-1 group-hover:text-primary" />
            </button>
          ))}
        </div>
      </section>

      <section
        id="latest"
        className="border-y border-white/8 bg-[#0a1c1d] py-18"
      >
        <div className="mx-auto grid max-w-7xl gap-8 px-5 lg:grid-cols-[.8fr_1.2fr] lg:px-8">
          <div>
            <div className="flex items-center gap-2 text-primary">
              <RefreshCw className="size-4" />
              <p className="text-xs font-bold uppercase tracking-[.18em]">
                官方情報同步
              </p>
            </div>
            <h2 className="mt-3 text-3xl font-black tracking-tight">
              最新版本，
              <br />
              我們每天替你追。
            </h2>
            <p className="mt-4 max-w-md text-sm leading-6 text-muted-foreground">
              每天上午 9:00 比對 HABBY 的官方商店版本與公告；只有可核實的內容才會放進攻略。
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              {OFFICIAL_UPDATE.sources.map((source) => (
                <a
                  key={source.name}
                  href={source.url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1.5 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1.5 text-xs font-semibold text-muted-foreground transition hover:border-primary/30 hover:text-primary"
                >
                  {source.name}
                  <ExternalLink className="size-3" />
                </a>
              ))}
            </div>
          </div>

          <article className="relative overflow-hidden rounded-[28px] border border-primary/20 bg-gradient-to-br from-primary/[0.12] via-card to-card p-6 sm:p-8">
            <div className="absolute -right-16 -top-16 size-52 rounded-full bg-primary/10 blur-3xl" />
            <div className="relative flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className="grid size-11 place-items-center rounded-2xl bg-primary font-black text-primary-foreground">
                  {OFFICIAL_UPDATE.version.split('.')[0]}
                </span>
                <div>
                  <p className="font-black">版本 {OFFICIAL_UPDATE.version}</p>
                  <p className="text-xs text-muted-foreground">
                    最後查核：{OFFICIAL_UPDATE.checkedAt}
                  </p>
                </div>
              </div>
              <span className="inline-flex h-5 items-center rounded-full bg-primary px-2 text-xs font-semibold text-primary-foreground">
                官方已確認
              </span>
            </div>
            <h3 className="relative mt-7 text-2xl font-black">
              {OFFICIAL_UPDATE.headline}
            </h3>
            <p className="relative mt-2 text-sm leading-6 text-muted-foreground">
              {OFFICIAL_UPDATE.summary}
            </p>
            <ul className="relative mt-6 grid gap-3 sm:grid-cols-2">
              {OFFICIAL_UPDATE.bullets.map((bullet) => (
                <li
                  key={bullet}
                  className="flex gap-2 rounded-xl border border-white/8 bg-black/10 p-3 text-sm"
                >
                  <Check className="mt-0.5 size-4 shrink-0 text-primary" />
                  {bullet}
                </li>
              ))}
            </ul>
          </article>
        </div>
      </section>

      <section
        id="guide-library"
        className="mx-auto max-w-7xl scroll-mt-20 px-5 py-18 lg:px-8"
      >
        <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
          <div>
            <p className="text-xs font-bold uppercase tracking-[.18em] text-primary">
              攻略資料庫
            </p>
            <h2 className="mt-2 text-3xl font-black tracking-tight">
              找到你的下一步
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">
              共 {GUIDES.length} 篇實用攻略，收藏會保存在這台裝置。
            </p>
          </div>
          <div className="flex w-full max-w-sm items-center rounded-xl border border-white/10 bg-card px-3 focus-within:border-primary/40">
            <Search className="size-4 text-muted-foreground" />
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="h-10 w-full min-w-0 border-0 bg-transparent px-2.5 text-sm outline-none placeholder:text-muted-foreground"
              aria-label="篩選攻略"
              placeholder="在攻略庫內搜尋"
            />
            {query && (
              <button
                className="text-xs font-bold text-primary"
                type="button"
                onClick={() => setQuery('')}
              >
                清除
              </button>
            )}
          </div>
        </div>

        <div className="mt-7 flex w-full justify-start overflow-x-auto rounded-xl bg-card p-1 sm:w-fit" role="tablist" aria-label="攻略分類">
            {categories.map((item) => (
              <button
                key={item}
                type="button"
                role="tab"
                aria-selected={category === item}
                onClick={() => setCategory(item)}
                className={`inline-flex h-8 min-w-16 items-center justify-center gap-1.5 rounded-lg px-3 text-sm font-medium transition ${
                  category === item
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                {item}
                {item === '收藏' && favorites.length > 0 && (
                  <span className="rounded-full bg-black/20 px-1.5 text-[10px]">
                    {favorites.length}
                  </span>
                )}
              </button>
            ))}
        </div>

        {filteredGuides.length > 0 ? (
          <div className="mt-7 grid gap-4 md:grid-cols-2">
            {filteredGuides.map((guide) => {
              const isFavorite = favorites.includes(guide.id);
              return (
                <article
                  key={guide.id}
                  className="group flex flex-col rounded-2xl border border-white/8 bg-card p-5 transition hover:-translate-y-0.5 hover:border-primary/25"
                >
                  <div className="flex items-start justify-between gap-3">
                    <span className={`inline-flex h-5 items-center rounded-full border px-2 text-xs font-semibold ${categoryStyles[guide.category]}`}>
                      {guide.category}
                    </span>
                    <button
                      type="button"
                      onClick={() => toggleFavorite(guide.id)}
                      className="grid size-9 place-items-center rounded-full border border-white/8 text-muted-foreground transition hover:border-primary/30 hover:text-primary"
                      aria-label={isFavorite ? `取消收藏${guide.title}` : `收藏${guide.title}`}
                    >
                      <Heart
                        className={`size-4 ${isFavorite ? 'fill-primary text-primary' : ''}`}
                      />
                    </button>
                  </div>
                  <h3 className="mt-4 text-lg font-black leading-snug">
                    {guide.title}
                  </h3>
                  <p className="mt-2 flex-1 text-sm leading-6 text-muted-foreground">
                    {guide.description}
                  </p>
                  <div className="mt-4 flex flex-wrap gap-1.5">
                    {guide.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-full bg-white/[0.05] px-2 py-1 text-[11px] text-muted-foreground"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                  <details className="guide-details mt-4 border-t border-white/8 pt-4">
                    <summary className="flex cursor-pointer list-none items-center justify-between text-sm font-bold text-primary">
                      查看攻略重點
                      <ChevronRight className="size-4 transition-transform" />
                    </summary>
                    <ul className="mt-3 space-y-2">
                      {guide.takeaways.map((takeaway) => (
                        <li
                          key={takeaway}
                          className="flex gap-2 text-sm leading-5 text-muted-foreground"
                        >
                          <Check className="mt-0.5 size-3.5 shrink-0 text-primary" />
                          {takeaway}
                        </li>
                      ))}
                    </ul>
                  </details>
                  <div className="mt-4 flex items-center gap-3 text-[11px] text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Clock3 className="size-3" />
                      {guide.readTime}
                    </span>
                    <span>{guide.level}</span>
                    <span className="ml-auto">更新 {guide.updated}</span>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="mt-7 rounded-2xl border border-dashed border-white/12 bg-card/50 px-6 py-16 text-center">
            <Search className="mx-auto size-8 text-muted-foreground" />
            <h3 className="mt-4 font-black">沒有找到相符攻略</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              試試「苦無」、「無人機」或清除篩選條件。
            </p>
            <button
              type="button"
              className="mt-5 h-9 rounded-lg border border-white/12 bg-transparent px-3 text-sm font-semibold transition hover:bg-white/5"
              onClick={() => {
                setQuery('');
                setCategory('全部');
              }}
            >
              清除篩選
            </button>
          </div>
        )}
      </section>

      <section id="meta" className="bg-[#d8ff57] py-18 text-[#0b1f1e]">
        <div className="mx-auto max-w-7xl px-5 lg:px-8">
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <p className="text-xs font-black uppercase tracking-[.18em] opacity-60">
                5.1.0 · ENDGAME META
              </p>
              <h2 className="mt-2 text-3xl font-black tracking-tight sm:text-4xl">
                診斷結果對應這三套
              </h2>
            </div>
            <p className="max-w-md text-sm font-semibold leading-6 opacity-65">
              先看卡片上方的「適合你，如果」，符合再展開完整裝備。終局沒有一套通吃，模式與門檻不同就要切換。
            </p>
          </div>

          <div
            id="characters"
            className="mt-8 scroll-mt-24 overflow-hidden rounded-[28px] bg-[#0b1f1e] p-5 text-[#f8ffe1] sm:p-7"
          >
            <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
              <div>
                <p className="text-xs font-black uppercase tracking-[.18em] text-[#d8ff57]">
                  先認人，再看配裝
                </p>
                <h3 className="mt-2 text-2xl font-black">終局配裝角色圖鑑</h3>
              </div>
              <p className="max-w-lg text-sm font-semibold leading-6 text-white/55">
                「主位、協同、Teamwork 被動、異獸」是四種不同位置。下方每張卡都附中英文名與用途，英文不再只丟一串給你猜。
              </p>
            </div>

            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {CHARACTER_GLOSSARY.map((profile) => (
                <article
                  id={`character-${profile.id}`}
                  key={profile.id}
                  className="scroll-mt-24 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.06]"
                >
                  <div className="relative aspect-[16/9] overflow-hidden bg-white/5">
                    <Image
                      src={profile.image}
                      alt={profile.imageAlt}
                      fill
                      className="object-cover transition duration-500 hover:scale-[1.03]"
                      sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-[#0b1f1e] via-transparent to-transparent" />
                    <span className="absolute left-3 top-3 inline-flex h-6 items-center rounded-full border border-white/15 bg-[#0b1f1e]/80 px-2.5 text-[11px] font-black text-[#d8ff57] backdrop-blur">
                      {profile.kind}
                    </span>
                  </div>
                  <div className="p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h4 className="text-lg font-black">{profile.nameZh}</h4>
                        <p className="text-xs font-bold uppercase tracking-wider text-white/45">
                          {profile.nameEn}
                        </p>
                      </div>
                      <span className="rounded-full bg-[#d8ff57] px-2.5 py-1 text-[11px] font-black text-[#0b1f1e]">
                        {profile.role}
                      </span>
                    </div>
                    <p className="mt-3 text-sm font-medium leading-6 text-white/65">
                      {profile.summary}
                    </p>
                    <a
                      href={profile.sourceUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="mt-3 inline-flex items-center gap-1 text-[11px] font-bold text-[#d8ff57]/75 transition hover:text-[#d8ff57]"
                    >
                      圖片／資料：{profile.sourceName}
                      <ExternalLink className="size-3" />
                    </a>
                  </div>
                </article>
              ))}
            </div>

            <div className="mt-5 grid gap-3 text-xs font-bold sm:grid-cols-3">
              <p className="rounded-xl bg-white/[0.06] p-3 text-white/65">
                <span className="text-[#d8ff57]">真正主位：</span>Venato／Taloxa
              </p>
              <p className="rounded-xl bg-white/[0.06] p-3 text-white/65">
                <span className="text-[#d8ff57]">神火支援鏈：</span>哪吒 → 伏爾坎
              </p>
              <p className="rounded-xl bg-white/[0.06] p-3 text-white/65">
                <span className="text-[#d8ff57]">不是角色：</span>幽冥之魂是異獸
              </p>
            </div>
          </div>

          <div id="builds" className="mt-8 grid scroll-mt-24 gap-4 lg:grid-cols-3">
            {BUILDS.map((build, index) => (
              <article
                key={build.name}
                className="rounded-[24px] border-2 border-[#0b1f1e]/10 bg-[#f8ffe1] p-5 shadow-[0_8px_0_rgba(11,31,30,.12)]"
              >
                <div className="flex items-center justify-between">
                  <span className="grid size-9 place-items-center rounded-xl bg-[#0b1f1e] text-sm font-black text-[#d8ff57]">
                    0{index + 1}
                  </span>
                  <span className="inline-flex h-5 items-center rounded-full bg-[#0b1f1e]/8 px-2 text-xs font-semibold text-[#0b1f1e]">
                    {build.mode}
                  </span>
                </div>
                <h3 className="mt-5 text-xl font-black">{build.name}</h3>
                <p className="mt-2 rounded-lg bg-[#0b1f1e]/7 px-3 py-2 text-xs font-black leading-5">
                  適合你，如果：{buildUseWhen[index]}
                </p>
                <div className="mt-5 rounded-2xl bg-[#0b1f1e]/6 p-4">
                  <div className="mb-4 flex flex-wrap gap-2">
                    {build.characterIds.map((characterId) => {
                      const profile = characterIndex.get(characterId);
                      if (!profile) return null;

                      return (
                        <a
                          key={profile.id}
                          href={`#character-${profile.id}`}
                          title={`${profile.nameZh}（${profile.nameEn}）｜${profile.role}`}
                          className="group inline-flex items-center gap-2 rounded-full border border-[#0b1f1e]/10 bg-[#f8ffe1] py-1 pl-1 pr-2.5 text-[11px] font-black transition hover:-translate-y-0.5 hover:border-[#0b1f1e]/30"
                        >
                          <span className="relative size-7 overflow-hidden rounded-full bg-[#0b1f1e]/10">
                            <Image
                              src={profile.image}
                              alt=""
                              fill
                              className="object-cover"
                              sizes="28px"
                            />
                          </span>
                          {profile.nameZh}
                        </a>
                      );
                    })}
                  </div>
                  <p className="text-xs font-black uppercase tracking-wider opacity-50">
                    終局核心
                  </p>
                  <p className="mt-2 text-sm font-black">角色 · {build.hero}</p>
                  <p className="mt-2 text-sm font-black">異獸 · {build.pet}</p>
                  <p className="mt-2 text-sm font-black">武器 · {build.weapon}</p>
                </div>
                <p className="mt-5 rounded-xl border border-[#0b1f1e]/12 bg-[#0b1f1e] px-3 py-2.5 text-xs font-bold leading-5 text-[#d8ff57]">
                  {build.breakpoint}
                </p>
                <details className="guide-details mt-4 rounded-xl border border-[#0b1f1e]/15 bg-white/35">
                  <summary className="flex cursor-pointer list-none items-center justify-between gap-3 px-3 py-3 text-xs font-black">
                    完整裝備、技能與評分
                    <ChevronRight className="size-4 transition-transform" />
                  </summary>
                  <div className="border-t border-[#0b1f1e]/10 px-3 pb-4 pt-3">
                    <p className="text-xs font-black uppercase tracking-wider opacity-50">
                      裝備槽位
                    </p>
                    <ul className="mt-2 space-y-2">
                      {build.gear.map((gear) => (
                        <li key={gear} className="flex gap-2 text-xs font-bold leading-5">
                          <Check className="mt-0.5 size-3.5 shrink-0" />
                          {gear}
                        </li>
                      ))}
                    </ul>
                    <p className="mt-4 text-xs font-black uppercase tracking-wider opacity-50">
                      場內技能
                    </p>
                    <p className="mt-1 text-xs font-semibold leading-5 opacity-70">
                      {build.skills.join(' ／ ')}
                    </p>
                    <p className="mt-4 text-xs font-semibold leading-5 opacity-70">
                      {build.note}
                    </p>
                    <div className="mt-4 space-y-3">
                      {[
                        ['清怪', build.stats.clear],
                        ['頭目', build.stats.boss],
                        ['生存', build.stats.safety],
                      ].map(([label, value]) => (
                        <div key={label}>
                          <div className="mb-1 flex items-center justify-between text-xs font-black">
                            <span>{label}</span>
                            <span className="text-[#0b1f1e]/55">{value}</span>
                          </div>
                          <div
                            className="h-1.5 overflow-hidden rounded-full bg-[#0b1f1e]/10"
                            role="progressbar"
                            aria-label={String(label)}
                            aria-valuenow={value as number}
                            aria-valuemin={0}
                            aria-valuemax={100}
                          >
                            <div
                              className="h-full rounded-full bg-[#0b1f1e]"
                              style={{ width: `${value}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </details>
              </article>
            ))}
          </div>
          <div className="mt-7 flex flex-col gap-3 rounded-2xl border-2 border-[#0b1f1e]/10 bg-[#f8ffe1]/70 p-4 text-xs font-semibold sm:flex-row sm:items-center sm:justify-between">
            <p className="max-w-2xl leading-5 opacity-70">
              終局玩家請把自己的基礎暴率、Relic Cores、Chaos Power 與收藏加成丟進計算器；同一件 SS 裝在未達門檻時，可能輸給 AF3 S 裝。
            </p>
            <div className="flex flex-wrap gap-2">
              <a
                href="https://www.reddit.com/r/Survivorio/comments/1ca5t70/random_build_questions_mega_thread/"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 rounded-full bg-[#0b1f1e] px-3 py-1.5 text-[#d8ff57]"
              >
                近期社群實測 <ExternalLink className="size-3" />
              </a>
              <a
                href="https://survivoriocalc.com/survivor-io-build-calculator/"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 rounded-full border border-[#0b1f1e]/20 px-3 py-1.5"
              >
                配裝計算器 <ExternalLink className="size-3" />
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-5 px-5 py-18 lg:grid-cols-[1fr_.72fr] lg:px-8">
        <div className="rounded-[28px] border border-white/8 bg-card p-6 sm:p-8">
          <div className="flex items-center gap-3">
            <span className="grid size-11 place-items-center rounded-2xl bg-primary/10 text-primary">
              <ShieldCheck className="size-5" />
            </span>
            <div>
              <p className="text-xs font-bold uppercase tracking-[.16em] text-primary">
                終局帳號檢查
              </p>
              <h2 className="text-xl font-black">給建議前，先確認這四項</h2>
            </div>
          </div>
          <div className="mt-6 grid gap-3 sm:grid-cols-2">
            {STARTER_TASKS.map((task) => {
              const checked = checkedTasks.includes(task);
              return (
                <label
                  key={task}
                  className={`flex cursor-pointer items-center gap-3 rounded-xl border p-4 transition ${
                    checked
                      ? 'border-primary/25 bg-primary/8 text-muted-foreground'
                      : 'border-white/8 bg-black/10 hover:border-primary/20'
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => toggleTask(task)}
                    aria-label={task}
                    className="size-4 shrink-0 accent-[var(--primary)]"
                  />
                  <span className={`text-sm font-semibold ${checked ? 'line-through' : ''}`}>
                    {task}
                  </span>
                </label>
              );
            })}
          </div>
          <div className="mt-5 flex items-center justify-between text-xs font-bold text-muted-foreground">
            <span>帳號資料完整度</span>
            <span className="text-primary">
              {checkedTasks.length} / {STARTER_TASKS.length}
            </span>
          </div>
          <div className="mt-2 h-2 overflow-hidden rounded-full bg-black/20">
            <div
              className="h-full rounded-full bg-primary transition-all duration-500"
              style={{
                width: `${(checkedTasks.length / STARTER_TASKS.length) * 100}%`,
              }}
            />
          </div>
        </div>

        <aside className="relative overflow-hidden rounded-[28px] border border-white/8 bg-gradient-to-br from-[#143b3b] to-[#0a2020] p-6 sm:p-8">
          <Zap className="absolute -bottom-5 -right-4 size-36 rotate-12 text-primary/8" />
          <div className="relative">
            <span className="grid size-11 place-items-center rounded-2xl bg-orange-300/10 text-orange-200">
              <Target className="size-5" />
            </span>
            <h2 className="mt-5 text-xl font-black">攻略可信度原則</h2>
            <ul className="mt-4 space-y-3 text-sm leading-6 text-muted-foreground">
              <li className="flex gap-2">
                <Check className="mt-1 size-4 shrink-0 text-primary" />
                版本與活動資訊優先採官方來源
              </li>
              <li className="flex gap-2">
                <Check className="mt-1 size-4 shrink-0 text-primary" />
                尚未實測的內容會明確標示「觀察」
              </li>
              <li className="flex gap-2">
                <Check className="mt-1 size-4 shrink-0 text-primary" />
                每篇攻略保留最後更新日期
              </li>
            </ul>
          </div>
        </aside>
      </section>

      <footer className="border-t border-white/8 bg-[#071719]">
        <div className="mx-auto flex max-w-7xl flex-col gap-5 px-5 py-8 text-xs text-muted-foreground sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <div className="flex items-center gap-2">
            <span className="grid size-8 place-items-center rounded-lg bg-primary font-black text-primary-foreground">
              噠
            </span>
            <div>
              <p className="font-black text-foreground">噠噠攻略站</p>
              <p>非官方玩家攻略站，遊戲商標與內容歸原權利人所有。</p>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <span>每日 09:00 自動查核</span>
            <a className="hover:text-primary" href="#latest">
              資料來源
            </a>
            <a className="hover:text-primary" href="#top">
              回到頂端 ↑
            </a>
          </div>
        </div>
      </footer>

      <nav className="fixed inset-x-4 bottom-4 z-40 flex items-center justify-around rounded-2xl border border-white/10 bg-[#0a1d1e]/92 p-2 shadow-2xl backdrop-blur-xl md:hidden" aria-label="行動版導覽">
        {[
          { label: '診斷', icon: Target, href: '#advisor' },
          { label: '情報', icon: RefreshCw, href: '#latest' },
          { label: '配裝', icon: Swords, href: '#builds' },
          { label: '收藏', icon: Heart, action: () => jumpToGuides('收藏') },
        ].map((item) => {
          const Icon = item.icon;
          const content = (
            <>
              <Icon className="size-4" />
              <span>{item.label}</span>
            </>
          );
          return item.action ? (
            <button
              key={item.label}
              type="button"
              onClick={item.action}
              className="flex min-w-14 flex-col items-center gap-1 rounded-xl px-3 py-1.5 text-[10px] font-bold text-muted-foreground hover:bg-white/[0.05] hover:text-primary"
            >
              {content}
            </button>
          ) : (
            <a
              key={item.label}
              href={item.href}
              className="flex min-w-14 flex-col items-center gap-1 rounded-xl px-3 py-1.5 text-[10px] font-bold text-muted-foreground hover:bg-white/[0.05] hover:text-primary"
            >
              {content}
            </a>
          );
        })}
      </nav>
    </main>
  );
}
