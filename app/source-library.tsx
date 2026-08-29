'use client';

import {
  AlertTriangle,
  BookOpenCheck,
  Check,
  ExternalLink,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

import { Input } from '@/components/ui/input';
import {
  LATEST_SOURCE_FALLBACK,
  SOURCE_API_URL,
  SOURCE_CATEGORY_URL,
  SOURCE_GUIDES,
  type SourceGuideCategory,
} from '@/lib/source-guide-data';

type LatestSourceItem = {
  title: string;
  date: string;
  link: string;
};

type SourceApiPost = {
  date: string;
  link: string;
  title: { rendered: string };
};

const categories: Array<'全部' | SourceGuideCategory> = [
  '全部',
  '最新系統',
  '科技配件',
  '收藏系統',
  '特工寵物',
  '裝備養成',
  '關卡活動',
];

const statusStyles = {
  現行: 'border-primary/25 bg-primary/10 text-primary',
  常駐: 'border-cyan-300/20 bg-cyan-300/10 text-cyan-200',
  需版本核對: 'border-orange-300/25 bg-orange-300/10 text-orange-200',
};

function decodeTitle(value: string) {
  const box = document.createElement('textarea');
  box.innerHTML = value;
  return box.value
    .replace(/^【噠噠特攻】\s*/, '')
    .replace(/^噠噠特攻[：:]?\s*/, '')
    .trim();
}

function formatDate(value: string) {
  return value.slice(0, 10).replaceAll('-', '/');
}

export default function SourceLibrary() {
  const [category, setCategory] = useState<(typeof categories)[number]>('全部');
  const [query, setQuery] = useState('');
  const [latest, setLatest] = useState<LatestSourceItem[]>(LATEST_SOURCE_FALLBACK);
  const [live, setLive] = useState(false);

  useEffect(() => {
    let cancelled = false;

    fetch(SOURCE_API_URL)
      .then((response) => {
        if (!response.ok) throw new Error('來源暫時無法連線');
        return response.json() as Promise<SourceApiPost[]>;
      })
      .then((posts) => {
        if (cancelled || !Array.isArray(posts) || posts.length === 0) return;
        setLatest(
          posts.map((post) => ({
            title: decodeTitle(post.title.rendered),
            date: formatDate(post.date),
            link: post.link,
          })),
        );
        setLive(true);
      })
      .catch(() => {
        if (!cancelled) setLive(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const filteredGuides = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return SOURCE_GUIDES.filter((guide) => {
      const matchesCategory = category === '全部' || guide.category === category;
      const searchable = [
        guide.title,
        guide.summary,
        guide.category,
        guide.status,
        ...guide.actions,
      ]
        .join(' ')
        .toLowerCase();
      return matchesCategory && (!needle || searchable.includes(needle));
    });
  }, [category, query]);

  return (
    <section id="systems" className="scroll-mt-20 border-y border-white/8 bg-[#071719] py-18">
      <div className="mx-auto max-w-7xl px-5 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[1fr_.72fr] lg:items-end">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/8 px-3 py-1 text-xs font-black text-primary">
              <BookOpenCheck className="size-3.5" />
              來源資料補充庫
            </span>
            <h2 className="mt-4 max-w-3xl text-3xl font-black tracking-tight sm:text-4xl">
              不只收錄文章，直接整理成你能照做的系統攻略
            </h2>
            <p className="mt-4 max-w-3xl text-sm font-medium leading-7 text-muted-foreground">
              已盤點「別說筆記」噠噠特攻分類的 195 篇文章，將科技配件、收藏、特工、寵物、裝備、關卡與新系統重新改寫成行動清單。限時活動與舊版本內容會明確標記，不會混進現行配裝結論。
            </p>
          </div>

          <div className="grid grid-cols-3 gap-2">
            {[
              ['195', '來源文章'],
              [String(SOURCE_GUIDES.length), '實用主題'],
              ['6', '最新動態'],
            ].map(([value, label]) => (
              <div key={label} className="rounded-2xl border border-white/8 bg-white/[0.04] p-4 text-center">
                <p className="text-2xl font-black text-primary">{value}</p>
                <p className="mt-1 text-[11px] font-bold text-muted-foreground">{label}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-8 rounded-[26px] border border-white/8 bg-white/[0.035] p-5 sm:p-6">
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-lg font-black">最新來源動態</p>
                <span
                  className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-[10px] font-black ${
                    live ? 'bg-primary/10 text-primary' : 'bg-white/8 text-muted-foreground'
                  }`}
                >
                  <RefreshCw className={`size-3 ${live ? 'animate-spin [animation-duration:4s]' : ''}`} />
                  {live ? '已連接即時文章' : '顯示最近備援資料'}
                </span>
              </div>
              <p className="mt-1 text-xs font-medium text-muted-foreground">
                每次開啟網站都會讀取最新六篇；若來源暫時離線，仍會保留最近資料。
              </p>
            </div>
            <a
              href={SOURCE_CATEGORY_URL}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center gap-1.5 rounded-xl border border-white/10 bg-white/[0.04] px-3 py-2 text-xs font-black transition hover:border-primary/30 hover:text-primary"
            >
              查看完整來源
              <ExternalLink className="size-3.5" />
            </a>
          </div>

          <div className="mt-5 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
            {latest.map((item) => (
              <a
                key={`${item.date}-${item.link}`}
                href={item.link}
                target="_blank"
                rel="noreferrer"
                className="group flex min-h-24 flex-col justify-between rounded-2xl border border-white/8 bg-[#0b2021] p-4 transition hover:-translate-y-0.5 hover:border-primary/25"
              >
                <p className="line-clamp-2 text-sm font-black leading-6 group-hover:text-primary">
                  {item.title}
                </p>
                <div className="mt-3 flex items-center justify-between text-[11px] font-bold text-muted-foreground">
                  <span>{item.date}</span>
                  <span className="inline-flex items-center gap-1">
                    原文
                    <ExternalLink className="size-3" />
                  </span>
                </div>
              </a>
            ))}
          </div>
        </div>

        <div className="mt-8 grid gap-4 lg:grid-cols-[1fr_.72fr]">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3.5 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="搜尋科技配件、收藏、寵物、覺醒……"
              aria-label="搜尋補充攻略"
              className="h-11 rounded-xl border-white/10 bg-white/[0.04] pl-10 text-sm"
            />
          </div>
          <div className="flex flex-wrap gap-2 lg:justify-end">
            {categories.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => setCategory(item)}
                className={`rounded-full border px-3 py-2 text-xs font-black transition ${
                  category === item
                    ? 'border-primary bg-primary text-primary-foreground'
                    : 'border-white/10 bg-white/[0.03] text-muted-foreground hover:border-primary/25 hover:text-foreground'
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <div className="mt-5 flex flex-col justify-between gap-3 rounded-2xl border border-orange-300/15 bg-orange-300/[0.05] p-4 sm:flex-row sm:items-center">
          <div className="flex gap-3">
            <AlertTriangle className="mt-0.5 size-5 shrink-0 text-orange-200" />
            <div>
              <p className="text-sm font-black text-orange-100">版本保護規則</p>
              <p className="mt-1 text-xs font-medium leading-5 text-orange-100/60">
                「現行」可直接採用；「常駐」保留系統機制；「需版本核對」只作查表入口，配裝與強度結論以目前遊戲版本為準。
              </p>
            </div>
          </div>
          <p className="shrink-0 text-xs font-black text-orange-200">
            找到 {filteredGuides.length} 個主題
          </p>
        </div>

        <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filteredGuides.map((guide) => (
            <article
              key={guide.id}
              className="flex flex-col rounded-[22px] border border-white/8 bg-white/[0.035] p-5 transition hover:border-white/15"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-[11px] font-black text-primary">{guide.category}</span>
                <span
                  className={`rounded-full border px-2 py-1 text-[10px] font-black ${statusStyles[guide.status]}`}
                >
                  {guide.status}
                </span>
              </div>
              <h3 className="mt-3 text-lg font-black leading-7">{guide.title}</h3>
              <p className="mt-2 text-xs font-medium leading-6 text-muted-foreground">
                {guide.summary}
              </p>

              <div className="mt-4 rounded-xl bg-black/15 p-3">
                <p className="flex items-center gap-1.5 text-[11px] font-black text-primary">
                  <Sparkles className="size-3.5" />
                  你現在該做什麼
                </p>
                <ul className="mt-2 space-y-2">
                  {guide.actions.map((action) => (
                    <li key={action} className="flex gap-2 text-xs font-semibold leading-5 text-white/70">
                      <Check className="mt-0.5 size-3.5 shrink-0 text-primary" />
                      {action}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-auto flex items-center justify-between gap-3 pt-4 text-[11px] font-bold text-muted-foreground">
                <span>資料更新：{guide.updated}</span>
                <a
                  href={guide.sourceUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-1 text-primary/80 transition hover:text-primary"
                >
                  核對原文
                  <ExternalLink className="size-3" />
                </a>
              </div>
            </article>
          ))}
        </div>

        {filteredGuides.length === 0 && (
          <div className="mt-5 rounded-2xl border border-dashed border-white/10 p-10 text-center">
            <ShieldCheck className="mx-auto size-7 text-muted-foreground" />
            <p className="mt-3 text-sm font-black">沒有符合的主題</p>
            <button
              type="button"
              onClick={() => {
                setCategory('全部');
                setQuery('');
              }}
              className="mt-3 text-xs font-black text-primary"
            >
              清除搜尋條件
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
