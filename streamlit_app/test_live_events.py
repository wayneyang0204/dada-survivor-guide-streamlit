import json
from datetime import datetime
from pathlib import Path
from live_events import parse_card, discover, unlisted_cards, BASE
from activity_status import current_playbook, event_phase
from data_engine import EVENT_PLAYBOOKS


def body(title='新的活動', kind='特別活動'):
    node=dict(title=title,kind=kind,startDate='2026-10-28T16:00:00Z',endDate='2026-11-03T16:00:00Z')
    return '<script type="application/json">'+json.dumps({'data':[node]})+'</script>'


def test_discovery_is_independent_of_editorial_articles_and_fixed_host_only():
    requests=[]
    def read(url):
        requests.append(url)
        return '<a href="?eventid=6821273114">card</a>' if url==BASE else body()
    result=discover(read)
    assert result['state']=='ok' and result['cards'][0]['title']=='新的活動'
    assert len(requests)==2 and all(u.startswith(BASE) for u in requests)
    assert unlisted_cards(result,[],datetime.fromisoformat('2026-10-29T12:00:00+08:00'))
    assert not unlisted_cards(result,[{'official_event_id':'6821273114'}],datetime.fromisoformat('2026-10-29T12:00:00+08:00'))


def test_failure_and_changed_markup_are_not_reported_as_up_to_date():
    assert discover(lambda u:'broken')['state']=='unavailable'
    def fail(u):raise OSError('offline')
    assert discover(fail)['state']=='unavailable'
    assert parse_card(body(kind='重磅更新'),'12345678') is None
    assert parse_card('<script type="application/json">bad</script>','12345678') is None


def test_castle_is_current_and_old_beach_is_not_the_default():
    now=datetime.fromisoformat('2026-10-29T12:00:00+08:00')
    brief=current_playbook(EVENT_PLAYBOOKS,now)
    assert brief['guides'][0]=='castle-cards' and brief['state']=='active'
    castle=next(m for m in EVENT_PLAYBOOKS if m['name']=='古堡卡牌')
    assert castle['target']==0 and '820' not in str(castle['steps'])
    assert event_phase(castle,datetime.fromisoformat('2026-11-03T00:00:00+08:00'))['state']=='ended'


def test_current_button_overrides_a_stale_historical_selection():
    from test_decision_ui import boot, by_label
    app=boot('攻略首頁')
    app.session_state['activity_selection']='old historical selection'
    app.button(key='start_event').click().run()
    assert '古堡卡牌' in by_label(app.selectbox,'來源文章中的近期／歷史活動').value
    assert not app.exception


def test_actual_official_snapshot_can_be_parsed_when_available():
    path=Path('work/halloween-1029.txt')
    if path.exists():
        card=parse_card(path.read_text(encoding='utf-8'),'6821273114')
        assert card and '古堡' in card['title'] and card['starts_at']=='2026-10-28T16:00:00+00:00'
