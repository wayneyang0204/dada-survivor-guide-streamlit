import re
from collections import Counter
from datetime import date

import pytest
import guide_content as content
from field_content import FIELD_GUIDES, REVIEW_DATE
from test_decision_ui import APP, by_label
from streamlit.testing.v1 import AppTest


def test_expanded_catalog_has_real_articles_in_every_system():
    counts = Counter(g['category'] for g in content.GUIDES)
    assert len(FIELD_GUIDES) >= 18
    assert set(counts) == set(content.CATEGORIES)
    assert all(count >= 2 for count in counts.values())
    stats = content.library_stats(content.GUIDES)
    assert stats['articles'] == len(content.GUIDES) and stats['tables'] >= 60
    assert stats['questions'] >= 40 and stats['review_date'] == max(g['checked'] for g in content.GUIDES if g.get('checked'))
    refs = [{'reference_only': True}]
    assert content.library_stats(content.GUIDES + refs) == stats


@pytest.mark.parametrize('guide', FIELD_GUIDES, ids=lambda g:g['slug'])
def test_new_articles_are_actionable_and_evidence_is_not_faked(guide):
    assert all(guide[key] for key in ('game_entry','stop','next_after','caution','faq','related'))
    assert len(guide['takeaways']) == 3 and len(guide['sections']) >= 3
    for related in guide['related']:
        assert content.get_guide(related, content.GUIDES), related
    for section in guide['sections']:
        assert section['title'] and (section.get('rows') or section.get('steps') or section.get('body'))
        if section.get('rows'):
            assert all(len(row) == len(section['columns']) for row in section['rows'])
    for source in guide['source_details']:
        assert source['url'].startswith(('https://notalknote.xyz/','https://apps.apple.com/','https://play.google.com/','https://garrytools.com/','https://www.facebook.com/','https://sio-tools.exp0.dev/'))
        if source['date']:
            assert date.fromisoformat(source['date']) <= date.fromisoformat(guide['checked'])
        else:
            assert 'apps.apple.com' in source['url']  # No publication date is fabricated for an official event card.
    if not guide['sources']:
        assert guide['checked'] is None and guide['status'] == '本站操作方法'


def test_new_content_is_traditional_chinese_except_search_aliases():
    for guide in FIELD_GUIDES:
        rendered = ' '.join(str(guide[k]) for k in ('title','summary','verdict','sections','takeaways','stop','next_after','faq','caution'))
        assert not re.search('协同|确认|实际|满|装齊|暂|来源|连续|决定|维持|该|与', rendered), guide['slug']


@pytest.mark.parametrize('query,slug', [
    ('毀滅戰甲怎麼準備','version-5-4-0'),
    ('矩陣小隊怎麼準備','matrix-squad-preview'),
    ('伊狑值得換嗎','elaine-build'), ('伊羚','elaine-build'),
    ('協同帶誰','synergy-vs-link'), ('哪吒和洛基','divine-fire-team'),
    ('六星還是五星','survivor-stars'), ('幽暗黃4','umbral-soul'),
    ('載具怎麼升','mount-layout'), ('模組怎麼擺','mount-modules'),
    ('潮汐祕境打叉','tide-haven'), ('解構機','legend-deconstructor'),
    ('混沌融合之力','chaos-fusion-check'), ('打王傷害不夠','boss-testing'),
])
def test_concrete_player_questions_return_relevant_article(query, slug):
    results = content.search_guides(content.GUIDES, query)
    assert results and results[0]['slug'] == slug


def test_partial_suggestions_do_not_relabel_unknown_term_as_exact_match():
    query = '幽暗 外星不存在項目'
    assert not content.search_guides(content.GUIDES, query)
    assert any(g['slug']=='umbral-soul' for g in content.suggested_guides(content.GUIDES, query))


def test_matrix_squad_separates_store_release_from_feature_activation():
    guide = content.get_guide('matrix-squad-preview', content.GUIDES)
    assert '10月29日官方矩陣小隊活動卡已標示現已登場' in guide['summary']
    assert '成本仍須遊戲內核對' in guide['caution']
    assert any('eventid=6827054794' in url for _,url in guide['sources'])


def test_version_540_separates_live_features_from_coming_soon_and_platform_rollout():
    guide = content.get_guide('version-5-4-0', content.GUIDES)
    rendered = str(guide)
    for term in ('356～360', '毀滅戰甲', '異寵化形', '冰霜戰靴', '區域行動', '月礦遠征'):
        assert term in rendered
    assert '安卓5.4.0已上線' in rendered
    assert '蘋果仍為5.3.1' in rendered
    assert '即將上線' in rendered and '即將開啟' in rendered
    assert any('play.google.com/store/apps/details' in url for _, url in guide['sources'])
    assert '精確效果、解鎖條件、材料消耗' in guide['caution']


def test_boots_guide_does_not_reuse_old_routes_as_alien_forge_data():
    guide = content.get_guide('ss-boots-check', content.GUIDES)
    rendered = str(guide)
    assert '5.4.0' in rendered and '異星神煉即將開啟' in rendered
    assert '舊E／V效果' in rendered
    assert '沒有精確效果、解鎖條件或成本' in guide['caution']


def test_castle_cards_separates_no_chest_tickets_from_chest_costs():
    guide = content.get_guide('castle-cards', content.GUIDES)
    rendered = str(guide)
    assert '456' in rendered and '629' in rendered and '1085' in rendered
    assert '500／600／700／800／950逐檔重算' in rendered
    assert '不是官方保證' in guide['caution']


def test_flower_workshop_separates_free_tasks_from_chest_costs():
    guide = content.get_guide('flower-workshop', content.GUIDES)
    rendered = str(guide)
    assert '11月10日00:00' in rendered and '11月16日00:00' in rendered
    assert '6827046270' in rendered and '2256' in rendered
    assert '801' in rendered and '1455' in rendered
    assert '400張' in rendered and '1211' in rendered and '2666' in rendered
    assert '50箱' in rendered and '140箱' in rendered and '250箱' in rendered and '360箱' in rendered and '540箱' in rendered
    assert '705／795／1065' in rendered
    assert 'garrytools.com/event/details/42508884' in rendered
    assert 'notalknote.xyz/survivor-io-flower-workshop' in rendered
    assert '花束出現率與約1%花束狂歡不是官方保底' in guide['caution']


def test_supreme_collectibles_keep_official_launch_separate_from_community_thresholds():
    guide = content.get_guide('supreme-collectibles', content.GUIDES)
    rendered = str(guide)
    assert '6832413409' in rendered and '官方活動卡' in rendered
    assert '失重奇點' in rendered and '終極無限源' in rendered
    assert '18件傳奇收藏品' in rendered and '第三方' in guide['caution']
    assert '3650' in rendered and '39360' in rendered


def test_dessert_pinball_separates_no_chest_tickets_from_chest_costs():
    guide = content.get_guide('dessert-pinball', content.GUIDES)
    rendered = str(guide)
    assert '11月4日00:00' in rendered and '11月10日00:00' in rendered
    assert '6827040277' in rendered and '2250' in rendered
    assert '870' in rendered and '1380' in rendered and '380箱' in rendered
    assert '1600' in rendered and '2200' in rendered and '3100' in rendered
    assert 'garrytools.com/event/details/72537364' in rendered
    assert '不把2250張任務券全算成零成本免費量' in guide['caution']


def test_home_quick_search_callback_does_not_mutate_profile():
    app = AppTest.from_file(APP).run()
    raw = {'survivor':'維納托','awakening':6,'awakening_cores':20}
    app.session_state['player_profile'] = raw.copy()
    app.button(key='quick_query_2').click().run()
    assert not app.exception and by_label(app.text_input,'搜尋攻略').value == '協同作戰'
    assert app.button(key='home_search_synergy-vs-link')
    assert app.session_state['player_profile'] == raw


def test_article_body_is_visible_and_does_not_require_section_expansion():
    app = AppTest.from_file(APP)
    app.query_params['guide'] = 'elaine-build'
    app.run()
    text='\n'.join(m.value for m in app.markdown)
    assert '<ol class="article-steps">' in text and 'R2／R3' in text
    assert '實際操作與停止點' in text
    titles={s['title'] for s in content.get_guide('elaine-build',content.GUIDES)['sections']}
    assert not any(e.label in titles for e in app.expander)
