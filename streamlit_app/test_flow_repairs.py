"""Regression journeys for search recovery and consistent planner handoffs."""
from copy import deepcopy

import pytest
from streamlit.testing.v1 import AppTest

import guide_content as content
from test_decision_ui import APP, by_label


@pytest.mark.parametrize("query,slug", [
    ("暗物質傀儡黃五星", "collectible-breakpoints"),
    ("諧振要達到什麼程度", "resonance-planning"),
    ("雙絕槍異星神練怎麼選擇", "lance-starforge"),
    ("無人機已經3000了，雷電1600", "twin-tech-milestones"),
])
def test_existing_answers_are_found_by_player_wording(query, slug):
    results = content.search_guides(content.GUIDES, query)
    assert results and slug in [g['slug'] for g in results[:3]]


def test_unknown_term_is_not_silently_discarded():
    assert not content.search_guides(content.GUIDES, '雙絕槍不存在的效果123456')
    assert not content.search_guides(content.GUIDES, '消融')
    assert content.query_terms('維納托 R 6') == ['維納托', 'r6']
    rows = content.answer_rows(content.get_guide('collectible-breakpoints', content.GUIDES), '暗物質傀儡黃五星')
    assert len(rows) == 1 and rows[0][:2] == ['暗物質傀儡', '黃5']


@pytest.mark.parametrize('page,search_label,category_kind', [
    ('攻略首頁', '搜尋攻略', 'radio'), ('資料庫', '搜尋本站攻略', 'selectbox'),
])
def test_wrong_category_can_expand_search_and_return_to_same_query(page, search_label, category_kind):
    app = AppTest.from_file(APP)
    app.session_state['主導覽'] = page
    app.run()
    by_label(getattr(app, category_kind), '攻略分類').set_value('裝備神鑄')
    by_label(app.text_input, search_label).set_value('暗物質黃五星').run()
    expand = next(b for b in app.button if b.label.startswith('搜尋所有分類（'))
    expand.click().run()
    assert by_label(getattr(app, category_kind), '攻略分類').value == '全部'
    assert by_label(app.text_input, search_label).value == '暗物質黃五星'
    prefix = 'home_search' if page == '攻略首頁' else 'index'
    app.button(key=prefix + '_collectible-breakpoints').click().run()
    by_label(app.button, '← 搜尋結果').click().run()
    assert by_label(app.text_input, search_label).value == '暗物質黃五星'
    by_label(app.button, '清除搜尋').click().run()
    assert by_label(app.text_input, search_label).value == ''
    assert not app.exception


def test_primary_button_discards_previous_resource_filter_and_comparison():
    app = AppTest.from_file(APP)
    p = {'survivor': '維納托', 'awakening': 6, 'awakening_cores': 20,
         'weapon': '雙絕槍', 'weapon_e': 0, 'weapon_v': 0}
    app.session_state['player_profile'] = deepcopy(p)
    app.session_state['主導覽'] = '下一步'
    app.session_state['decision_resource'] = '神器核心'
    app.session_state['route_selected_id'] = 'weapon_e1'
    app.run()
    primary = next(m.value for m in app.markdown if 'aria-label="本次第一步"' in m.value)
    assert '維納托' in primary
    by_label(app.button, '回到第一優先').click().run()
    detail = next(m.value for m in app.markdown if 'aria-label="優先升級目標"' in m.value)
    assert '維納托 R6 → R7' in detail
    assert by_label(app.selectbox, '這次要安排的資源').value == '自動排序'
    assert 'route_selected_id' not in app.session_state
    assert app.session_state['player_profile'] == p and not app.exception


def test_catalog_only_match_can_escape_wrong_category():
    app = AppTest.from_file(APP).run()
    by_label(app.radio, '攻略分類').set_value('裝備神鑄')
    by_label(app.text_input, '搜尋攻略').set_value('231').run()
    button = next(b for b in app.button if b.label.startswith('搜尋所有分類（'))
    assert '件收藏' in button.label
    button.click().run()
    assert '暗物質傀儡' in ' '.join(m.value for m in app.markdown)
    assert by_label(app.text_input, '搜尋攻略').value == '231' and not app.exception


def test_single_saved_twin_tech_accepts_zero_and_changed_readings_reset_verification():
    app = AppTest.from_file(APP)
    app.session_state['player_profile'] = {'lightning_form': '雙生', 'lightning_energy': 0}
    app.query_params['guide'] = 'twin-tech-milestones'
    app.run()
    assert by_label(app.selectbox, '目前使用的雙生形態').value == '雙生雷電（雷電態）'
    assert by_label(app.number_input, '這件目前的諧振能量').value == 0
    by_label(app.checkbox, '我已對照遊戲，下一檔效果與來源表一致').check().run()
    app.session_state['player_profile'] = {'lightning_form': '雙生', 'lightning_energy': 1600}
    app.run()
    assert by_label(app.number_input, '這件目前的諧振能量').value == 1600
    assert not by_label(app.checkbox, '我已對照遊戲，下一檔效果與來源表一致').value
    assert not app.exception


def test_tech_hint_carries_exact_part_and_energy_without_editing_profile():
    app = AppTest.from_file(APP)
    p = {'survivor': '維納托', 'awakening': 6, 'awakening_goal': 6,
         'drone_form': '雙生', 'drone_energy': 3000,
         'lightning_form': '雙生', 'lightning_energy': 1600}
    app.session_state['player_profile'] = deepcopy(p)
    app.session_state['主導覽'] = '下一步'
    app.run()
    app.button(key='priority_tech_article').click().run()
    assert by_label(app.selectbox, '目前使用的雙生形態').value == '雙生雷電（雷電態）'
    assert by_label(app.number_input, '這件目前的諧振能量').value == 1600
    by_label(app.checkbox, '我已對照遊戲，下一檔效果與來源表一致').check().run()
    by_label(app.selectbox, '目前使用的雙生形態').select('雙生無人機（無人機態）').run()
    assert by_label(app.number_input, '這件目前的諧振能量').value == 3000
    assert not by_label(app.checkbox, '我已對照遊戲，下一檔效果與來源表一致').value
    by_label(app.number_input, '這件目前的諧振能量').set_value(3100).run()
    assert app.session_state['player_profile'] == p
    by_label(app.button, '← 升級路線').click().run()
    assert app.session_state['player_profile'] == p and not app.exception


def test_ordinary_or_unknown_form_never_supplies_twin_tool_energy():
    app = AppTest.from_file(APP)
    p = {'drone_form': '普通', 'drone_energy': 3000, 'lightning_energy': 1600}
    app.session_state['player_profile'] = deepcopy(p)
    app.query_params['guide'] = 'twin-tech-milestones'
    app.run()
    assert by_label(app.selectbox, '目前使用的雙生形態').value is None
    by_label(app.selectbox, '目前使用的雙生形態').select('雙生雷電（雷電態）').run()
    assert by_label(app.number_input, '這件目前的諧振能量').value is None
    assert app.session_state['player_profile'] == p and not app.exception
