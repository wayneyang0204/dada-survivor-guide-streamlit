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
    assert stats['questions'] >= 40 and stats['review_date'] == REVIEW_DATE
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
        assert source['url'].startswith(('https://notalknote.xyz/','https://apps.apple.com/'))
        if source['date']:
            assert date.fromisoformat(source['date']) <= date.fromisoformat(REVIEW_DATE)
        else:
            assert 'apps.apple.com' in source['url']  # No publication date is fabricated for an official event card.
    if not guide['sources']:
        assert guide['checked'] is None and guide['status'] == '本站操作方法'


def test_new_content_is_traditional_chinese_except_search_aliases():
    for guide in FIELD_GUIDES:
        rendered = ' '.join(str(guide[k]) for k in ('title','summary','verdict','sections','takeaways','stop','next_after','faq','caution'))
        assert not re.search('协同|确认|实际|满|装齊|暂|来源|连续|决定|维持|该|与', rendered), guide['slug']


@pytest.mark.parametrize('query,slug', [
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
