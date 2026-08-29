'use client';

import {
  Check,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  Filter,
  Gem,
  LibraryBig,
  Search,
  Sparkles,
  Target,
} from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  COLLECTIBLES,
  COLLECTIBLE_SOURCES,
  COLLECTION_SET_GUIDE,
  PRIORITY_COLLECTIBLES,
  type CollectibleQuality,
} from '@/lib/collectibles-data';

const views = ['投資順序', '完整圖鑑', '套組決策'] as const;
type View = (typeof views)[number];

const qualities = ['全部品質', '傳奇', '史詩', '優秀', '精良', '普通'] as const;
const qualityStyles: Record<CollectibleQuality, string> = {
  傳奇: 'border-red-300/25 bg-red-300/10 text-red-200',
  史詩: 'border-amber-300/25 bg-amber-300/10 text-amber-200',
  優秀: 'border-violet-300/25 bg-violet-300/10 text-violet-200',
  精良: 'border-sky-300/25 bg-sky-300/10 text-sky-200',
  普通: 'border-emerald-300/25 bg-emerald-300/10 text-emerald-200',
};

const PAGE_SIZE = 24;

const actionOrder = [
  {
    number: '01',
    title: '先盤點暴擊率',
    detail: '把所有能在紅3提供暴擊率的史詩收藏列出，缺哪一件就集中換哪一件。',
  },
  {
    number: '02',
    title: '無人機先到關鍵星級',
    detail: '星際躍遷矩陣圖紙與水動推力腳蹼優先；雙生無人機成形後再追暗物質傀儡。',
  },
  {
    number: '03',
    title: '自訂收藏先開欄位',
    detail: '欄位數量至少要能放下現有高星傳奇收藏品，再把收藏之心用於碎片。',
  },
  {
    number: '04',
    title: '最後補模式專精',
    detail: '足球、雷電、燃燒、特定武器，只投資你每週實際會用的模式。',
  },
];

export default function CollectiblesDatabase() {
  const [view, setView] = useState<View>('投資順序');
  const [query, setQuery] = useState('');
  const [quality, setQuality] = useState<(typeof qualities)[number]>('全部品質');
  const [edition, setEdition] = useState('全部期數');
  const [page, setPage] = useState(1);

  const collectibleById = useMemo(
    () => new Map(COLLECTIBLES.map((item) => [item.id, item])),
    [],
  );

  const filtered = useMemo(() => {
    const needle = query.trim();
    return COLLECTIBLES.filter((item) => {
      const matchesQuery =
        !needle || item.name.includes(needle) || String(item.id).includes(needle);
      const matchesQuality = quality === '全部品質' || item.quality === quality;
      const matchesEdition =
        edition === '全部期數' || item.edition === Number(edition.replace('第', '').replace('期', ''));
      return matchesQuery && matchesQuality && matchesEdition;
    });
  }, [edition, quality, query]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const visible = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  useEffect(() => {
    setPage(1);
  }, [query, quality, edition]);

  return (
    <section
      id="collectibles"
      className="scroll-mt-20 border-y border-white/8 bg-[#08191a] py-18"
    >
      <div className="mx-auto max-w-7xl px-5 lg:px-8">
        <div className="grid gap-7 lg:grid-cols-[1fr_auto] lg:items-end">
          <div className="max-w-3xl">
            <div className="flex items-center gap-2 text-primary">
              <LibraryBig className="size-4" />
              <p className="text-xs font-bold tracking-[.18em]">收藏品資料中心</p>
            </div>
            <h2 className="mt-3 text-3xl font-black tracking-tight sm:text-4xl">
              不只告訴你有什麼，
              <span className="text-primary">直接告訴你下一件升誰。</span>
            </h2>
            <p className="mt-4 max-w-2xl text-sm font-medium leading-6 text-muted-foreground">
              已建立目前 290 件收藏品的完整中文索引，涵蓋第 1～10 期、5 種品質、圖片與逐件數值入口；另外整理高階帳號真正需要的黃3、黃5、紅3與紅5斷點。
            </p>
          </div>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:min-w-[440px]">
            {[
              ['290', '件收藏品'],
              ['116', '套收藏組合'],
              ['10', '期完整索引'],
              ['08/30', '最新查核'],
            ].map(([value, label]) => (
              <div key={label} className="rounded-2xl border border-white/8 bg-card p-3 text-center">
                <strong className="block text-xl font-black text-primary">{value}</strong>
                <span className="mt-1 block text-[11px] font-bold text-muted-foreground">{label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-7 flex w-full gap-1 overflow-x-auto rounded-xl border border-white/8 bg-black/15 p-1 sm:w-fit" role="tablist" aria-label="收藏品資料分類">
          {views.map((item) => (
            <button
              key={item}
              type="button"
              role="tab"
              aria-selected={view === item}
              onClick={() => setView(item)}
              className={`h-9 min-w-24 rounded-lg px-4 text-sm font-black transition ${
                view === item
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-white/5 hover:text-foreground'
              }`}
            >
              {item}
            </button>
          ))}
        </div>

        {view === '投資順序' && (
          <div className="mt-7">
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
              {actionOrder.map((action) => (
                <article key={action.number} className="rounded-2xl border border-primary/15 bg-primary/[0.055] p-5">
                  <span className="text-xs font-black tracking-widest text-primary">{action.number}</span>
                  <h3 className="mt-3 text-base font-black">{action.title}</h3>
                  <p className="mt-2 text-xs font-semibold leading-5 text-muted-foreground">{action.detail}</p>
                </article>
              ))}
            </div>

            <div className="mt-8 flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
              <div>
                <p className="text-xs font-bold tracking-[.16em] text-primary">終局優先表</p>
                <h3 className="mt-2 text-2xl font-black">先看斷點，再決定要不要換碎片</h3>
              </div>
              <p className="max-w-xl text-xs font-semibold leading-5 text-muted-foreground">
                核心原則：全域暴擊與主力科技零件優先；只強化舊武器或冷門技能的收藏品延後。
              </p>
            </div>

            <div className="mt-5 grid gap-4 lg:grid-cols-2">
              {PRIORITY_COLLECTIBLES.map((guide) => {
                const item = collectibleById.get(guide.id);
                if (!item) return null;
                return (
                  <article key={guide.id} className="rounded-2xl border border-white/8 bg-card p-5">
                    <div className="flex items-start gap-4">
                      <div className="grid size-16 shrink-0 place-items-center overflow-hidden rounded-2xl border border-white/10 bg-black/20 p-1.5">
                        <img src={item.imageUrl} alt={item.name} className="size-full object-contain" loading="lazy" />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="rounded-full bg-primary px-2 py-1 text-[10px] font-black text-primary-foreground">{guide.priority}</span>
                          <span className={`rounded-full border px-2 py-1 text-[10px] font-black ${qualityStyles[item.quality]}`}>{item.quality}</span>
                          <span className="text-[11px] font-bold text-muted-foreground">第{item.edition}期</span>
                        </div>
                        <h4 className="mt-2 text-lg font-black">{item.name}</h4>
                        <p className="mt-0.5 text-xs font-bold text-primary">強化：{guide.target}</p>
                      </div>
                    </div>
                    <p className="mt-4 rounded-xl bg-black/15 px-3 py-2.5 text-xs font-semibold leading-5 text-muted-foreground">{guide.reason}</p>
                    <div className="mt-4 grid gap-2 sm:grid-cols-2">
                      {guide.milestones.map((milestone) => (
                        <p key={milestone} className="flex gap-2 text-xs font-semibold leading-5">
                          <Check className="mt-0.5 size-3.5 shrink-0 text-primary" />
                          {milestone}
                        </p>
                      ))}
                    </div>
                    <a href={item.detailUrl} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-1 text-xs font-black text-primary hover:underline">
                      查看逐星完整數值 <ExternalLink className="size-3" />
                    </a>
                  </article>
                );
              })}
            </div>
          </div>
        )}

        {view === '完整圖鑑' && (
          <div className="mt-7">
            <div className="rounded-2xl border border-white/8 bg-card p-4 sm:p-5">
              <div className="grid gap-3 lg:grid-cols-[1fr_180px_180px_auto]">
                <label className="relative block">
                  <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    placeholder="搜尋收藏品名稱或編號"
                    aria-label="搜尋收藏品"
                    className="h-10 rounded-xl bg-black/15 pl-9"
                  />
                </label>
                <Select value={quality} onValueChange={(value) => setQuality(value as (typeof qualities)[number])}>
                  <SelectTrigger className="h-10 w-full rounded-xl bg-black/15" aria-label="依品質篩選">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {qualities.map((item) => <SelectItem key={item} value={item}>{item}</SelectItem>)}
                  </SelectContent>
                </Select>
                <Select value={edition} onValueChange={setEdition}>
                  <SelectTrigger className="h-10 w-full rounded-xl bg-black/15" aria-label="依期數篩選">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="全部期數">全部期數</SelectItem>
                    {Array.from({ length: 10 }, (_, index) => `第${index + 1}期`).map((item) => (
                      <SelectItem key={item} value={item}>{item}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <button
                  type="button"
                  onClick={() => { setQuery(''); setQuality('全部品質'); setEdition('全部期數'); }}
                  className="inline-flex h-10 items-center justify-center gap-2 rounded-xl border border-white/10 px-4 text-sm font-black text-muted-foreground transition hover:border-primary/30 hover:text-primary"
                >
                  <Filter className="size-4" /> 清除篩選
                </button>
              </div>
              <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-white/8 pt-4 text-xs font-semibold text-muted-foreground">
                <span>找到 <strong className="text-foreground">{filtered.length}</strong> 件；站內索引共 {COLLECTIBLES.length} 件</span>
                <span>每件皆可開啟原始逐星數值頁</span>
              </div>
            </div>

            {visible.length > 0 ? (
              <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
                {visible.map((item) => (
                  <article key={item.id} className="group overflow-hidden rounded-2xl border border-white/8 bg-card transition hover:-translate-y-0.5 hover:border-primary/25">
                    <div className="relative grid aspect-square place-items-center bg-black/15 p-5">
                      <img src={item.imageUrl} alt={item.name} className="size-full object-contain transition duration-300 group-hover:scale-105" loading="lazy" />
                      <span className={`absolute left-2.5 top-2.5 rounded-full border px-2 py-1 text-[10px] font-black ${qualityStyles[item.quality]}`}>{item.quality}</span>
                      <span className="absolute right-2.5 top-2.5 rounded-full bg-black/45 px-2 py-1 text-[10px] font-black text-white/70">第{item.edition}期</span>
                    </div>
                    <div className="p-3.5">
                      <p className="text-[10px] font-bold text-muted-foreground">收藏編號 {item.id}</p>
                      <h3 className="mt-1 min-h-10 text-sm font-black leading-5">{item.name}</h3>
                      <a href={item.detailUrl} target="_blank" rel="noreferrer" className="mt-3 inline-flex items-center gap-1 text-[11px] font-black text-primary hover:underline">
                        完整數值 <ExternalLink className="size-3" />
                      </a>
                    </div>
                  </article>
                ))}
              </div>
            ) : (
              <div className="mt-5 rounded-2xl border border-dashed border-white/12 bg-card/50 px-6 py-16 text-center">
                <Search className="mx-auto size-8 text-muted-foreground" />
                <h3 className="mt-4 font-black">沒有符合的收藏品</h3>
                <p className="mt-2 text-sm text-muted-foreground">請清除篩選，或改用收藏編號搜尋。</p>
              </div>
            )}

            {filtered.length > PAGE_SIZE && (
              <div className="mt-6 flex items-center justify-center gap-3">
                <button
                  type="button"
                  disabled={page === 1}
                  onClick={() => setPage((current) => Math.max(1, current - 1))}
                  className="grid size-9 place-items-center rounded-xl border border-white/10 text-muted-foreground transition hover:border-primary/30 hover:text-primary disabled:cursor-not-allowed disabled:opacity-30"
                  aria-label="上一頁"
                >
                  <ChevronLeft className="size-4" />
                </button>
                <span className="min-w-24 text-center text-sm font-black">第 {page} / {pageCount} 頁</span>
                <button
                  type="button"
                  disabled={page === pageCount}
                  onClick={() => setPage((current) => Math.min(pageCount, current + 1))}
                  className="grid size-9 place-items-center rounded-xl border border-white/10 text-muted-foreground transition hover:border-primary/30 hover:text-primary disabled:cursor-not-allowed disabled:opacity-30"
                  aria-label="下一頁"
                >
                  <ChevronRight className="size-4" />
                </button>
              </div>
            )}
          </div>
        )}

        {view === '套組決策' && (
          <div className="mt-7">
            <div className="grid gap-4 md:grid-cols-2">
              {COLLECTION_SET_GUIDE.map((item, index) => (
                <article key={item.title} className="rounded-2xl border border-white/8 bg-card p-5 sm:p-6">
                  <div className="flex items-center justify-between gap-3">
                    <span className="grid size-10 place-items-center rounded-xl bg-primary/10 text-primary">
                      {index === 0 ? <Gem className="size-4" /> : index === 1 ? <Target className="size-4" /> : <Sparkles className="size-4" />}
                    </span>
                    <span className="rounded-full border border-primary/20 bg-primary/10 px-2.5 py-1 text-[10px] font-black text-primary">{item.label}</span>
                  </div>
                  <h3 className="mt-5 text-lg font-black">{item.title}</h3>
                  <p className="mt-2 text-sm font-semibold leading-6 text-muted-foreground">{item.detail}</p>
                </article>
              ))}
            </div>

            <div className="mt-5 grid gap-5 rounded-[24px] border border-primary/20 bg-gradient-to-br from-primary/[0.1] to-card p-6 lg:grid-cols-[1fr_auto] lg:items-center">
              <div>
                <p className="text-xs font-bold tracking-[.16em] text-primary">116 套完整資料</p>
                <h3 className="mt-2 text-xl font-black">套組先看總星數門檻，不要只看單件名稱</h3>
                <p className="mt-2 max-w-2xl text-sm font-semibold leading-6 text-muted-foreground">
                  套組效果會要求持有件數、單件紅星數或總紅星數。打開完整套組庫後，先找你的主力科技與自訂收藏，再決定選擇箱要投哪一期。
                </p>
              </div>
              <a href={COLLECTIBLE_SOURCES.sets} target="_blank" rel="noreferrer" className="inline-flex h-10 items-center justify-center gap-2 rounded-xl bg-primary px-4 text-sm font-black text-primary-foreground transition hover:brightness-110">
                查看 116 套完整數值 <ExternalLink className="size-4" />
              </a>
            </div>
          </div>
        )}

        <div className="mt-8 flex flex-col gap-4 rounded-2xl border border-white/8 bg-black/15 p-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-black text-foreground">資料查核說明</p>
            <p className="mt-1 max-w-2xl text-[11px] font-semibold leading-5 text-muted-foreground">
              290 件與 116 套以目前完整資料庫為基準；中文名稱與高階星級效果交叉比對中文版效果表。版本出現衝突時，以遊戲內數值與官方更新為最高優先。
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href={COLLECTIBLE_SOURCES.database} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-1.5 text-[11px] font-black text-muted-foreground hover:border-primary/30 hover:text-primary">完整收藏資料庫 <ExternalLink className="size-3" /></a>
            <a href={COLLECTIBLE_SOURCES.chineseEffects} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-1.5 text-[11px] font-black text-muted-foreground hover:border-primary/30 hover:text-primary">中文效果表 <ExternalLink className="size-3" /></a>
            <a href={COLLECTIBLE_SOURCES.official} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1.5 rounded-full border border-white/10 px-3 py-1.5 text-[11px] font-black text-muted-foreground hover:border-primary/30 hover:text-primary">官方版本紀錄 <ExternalLink className="size-3" /></a>
          </div>
        </div>
      </div>
    </section>
  );
}
