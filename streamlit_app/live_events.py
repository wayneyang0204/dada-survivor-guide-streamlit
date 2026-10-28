"""Public official-card discovery, independent of editorial publishing.

Only fixed Apple URLs are requested. Card display windows never become game
recipes, reward amounts, or spending advice. No player data leaves the app.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
import json
import re
from urllib.request import Request, urlopen

import streamlit as st

BASE = 'https://apps.apple.com/tw/app/survivor-io/id1528941310'


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(); self.inside=False; self.parts=[]
    def handle_starttag(self, tag, attrs):
        self.inside=tag=='script' and dict(attrs).get('type')=='application/json'
    def handle_endtag(self, tag):
        if tag=='script': self.inside=False
    def handle_data(self, data):
        if self.inside: self.parts.append(data)


def parse_card(body, event_id):
    parser=Scripts(); parser.feed(body)
    def walk(node):
        if isinstance(node, dict):
            if all(k in node for k in ('title','startDate','endDate')) and node.get('kind')=='特別活動':
                start=datetime.fromisoformat(node['startDate'].replace('Z','+00:00'))
                end=datetime.fromisoformat(node['endDate'].replace('Z','+00:00'))
                if start.tzinfo and end.tzinfo and start<end:
                    yield dict(id=event_id, title=str(node['title'])[:150], starts_at=start.isoformat(), ends_at=end.isoformat(), url=BASE+'?eventid='+event_id)
            for value in node.values(): yield from walk(value)
        elif isinstance(node,list):
            for value in node: yield from walk(value)
    for part in parser.parts:
        try:
            found=next(walk(json.loads(part)),None)
            if found: return found
        except (ValueError,TypeError): continue
    return None


def read_public(url):
    with urlopen(Request(url,headers={'User-Agent':'SurvivorGuide/1.0 public-event-check'}),timeout=3) as response:
        return response.read(2_000_001).decode('utf-8')


def discover(reader=read_public):
    checked=datetime.now(timezone.utc).isoformat()
    try:
        body=reader(BASE)
        ids=list(dict.fromkeys(re.findall(r'eventid=(\d{8,12})',unescape(body))))[:4]
        if not ids: return dict(checked=checked, state='unavailable', cards=[])
        def fetch(eid):
            try:return parse_card(reader(BASE+'?eventid='+eid),eid)
            except Exception:return None
        with ThreadPoolExecutor(max_workers=4) as pool: cards=[c for c in pool.map(fetch,ids) if c]
        # Empty/changed markup is not proof that there are no new events.
        return dict(checked=checked,state='ok' if cards else 'unavailable',cards=cards)
    except Exception:
        return dict(checked=checked,state='unavailable',cards=[])


@st.cache_data(ttl=900,show_spinner=False)
def latest_cards():
    return discover()


def unlisted_cards(result, models, now=None):
    now=now or datetime.now(timezone.utc)
    known={m.get('official_event_id') for m in models}
    return [c for c in result['cards'] if c['id'] not in known and datetime.fromisoformat(c['starts_at'])<=now<datetime.fromisoformat(c['ends_at'])]


@st.fragment(run_every='15m')
def render_updates():
    from data_engine import EVENT_PLAYBOOKS
    from zoneinfo import ZoneInfo
    result=latest_cards()
    stamp=datetime.fromisoformat(result['checked']).astimezone(ZoneInfo('Asia/Taipei')).strftime('%m/%d %H:%M')
    with st.expander('官方活動查核 · '+stamp):
        st.caption('開啟此頁時查核，連線期間每15分鐘重查。官方活動卡的展示期限不當作遊戲遊玩或兌換截止。')
        if st.button('立即重查官方活動',key='refresh_official_events'):
            latest_cards.clear(); st.rerun()
        if result['state']!='ok':
            st.warning('本次官方連線或格式核對未成功；下方為已收錄資料，未確認沒有新活動。')
        else:
            for card in result['cards']:
                st.link_button(card['title'], card['url'])
    for card in unlisted_cards(result,EVENT_PLAYBOOKS):
        st.info('官方已出現新活動：'+card['title']+'。完整攻略數值尚未收錄，請先核對官方卡與遊戲畫面。')
        st.link_button('查看新活動官方卡 ↗',card['url'])
