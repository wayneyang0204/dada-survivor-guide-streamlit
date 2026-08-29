import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  metadataBase: new URL('https://dada-survivor-guide.wayne111wrtfc.chatgpt.site'),
  title: '噠噠攻略站｜噠噠特攻最新攻略與配裝',
  description: '每日比對官方版本的噠噠特攻攻略站：武器排行、技能合成、角色配裝與關卡打法。',
  openGraph: {
    title: '噠噠攻略站',
    description: '每日更新・快速配裝・輕鬆過關',
    type: 'website',
    locale: 'zh_TW',
    images: [
      {
        url: '/og.png',
        width: 1731,
        height: 909,
        alt: '噠噠攻略站－每日更新、快速配裝、輕鬆過關',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: '噠噠攻略站',
    description: '每日更新・快速配裝・輕鬆過關',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
