from copy import deepcopy

import pytest
from field_tools import elaine_pet_limit, pet_milestone, reserve_stat, compare_runs
import next_step as engine
from direction_tools import operating_steps, related_guide
from test_decision_ui import boot, by_label
from datetime import datetime
from field_tools import event_window, guild_ticket_budget


@pytest.mark.parametrize("r,cap", [(0,0),(1,2),(2,4),(3,4),(4,6),(5,6),(6,8),(7,8),(8,10)])
def test_elaine_caps_are_not_all_red5(r, cap):
    result = elaine_pet_limit(r, 10)
    assert result['limit'] == cap
    if r:
        assert result['effective'] == cap
    assert elaine_pet_limit(None, None)['state'] == 'unknown'


def test_elaine_unknown_and_unowned_do_not_gain_skills():
    assert elaine_pet_limit(5, None)['state'] == 'unknown_pet'
    assert elaine_pet_limit(5, 0)['state'] == 'unowned'
    with pytest.raises(ValueError):
        elaine_pet_limit(True, 5)


@pytest.mark.parametrize("current,target", [(1,4),(2,4),(3,4),(4,10),(5,10),(9,10)])
def test_pet_selected_nodes(current, target):
    assert pet_milestone('幽暗之靈', current)['target'] == target
    assert pet_milestone('其他', current)['state'] == 'unknown'
    assert pet_milestone('幽暗之靈', 0)['state'] == 'unknown'
    assert pet_milestone('幽暗之靈', 10)['state'] == 'done'


def umbral(**extra):
    return {'pet_kind': '異世寵物', 'pet_name': '幽暗之靈', 'pet_star': 3,
            'pet_skills_ready': True, 'pet_preview_matches': True,
            'pet_materials_ready': True, **extra}


@pytest.mark.parametrize('matches,ready,status', [(None,True,'待核對材料'), (True,None,'待核對材料'),
            (True,False,'先存資源'), (True,True,'材料已足')])
def test_umbral_needs_effect_and_full_materials(matches, ready, status):
    step = engine.recommend(umbral(pet_preview_matches=matches, pet_materials_ready=ready))['primary']
    assert step['id'] == 'pet_umbral' and step['status'] == status
    assert len(step['checks']) == 2


def test_wrong_version_zero_star_or_maxed_never_recommend_duplicate():
    assert engine.recommend(umbral(pet_preview_matches=False))['primary'] is None
    assert engine.recommend(umbral(pet_star=0))['primary'] is None
    result = engine.recommend(umbral(pet_star=10))
    assert result['primary'] is None and any('紅5' in s for s in result['complete'])


def test_named_pet_does_not_request_an_unrelated_manual_target_after_finishing():
    from decision_ui import next_check
    assert next_check(engine.clean_profile(umbral(pet_star=10)), '寵物材料') is None
    assert next_check(engine.clean_profile({'pet_kind':'異世寵物','pet_name':'其他'}), '寵物材料') == '寵物'
    assert next_check(engine.clean_profile(umbral(pet_star=0)), '寵物材料') == '寵物'
    assert any('未持有' in s for s in engine.recommend(umbral(pet_star=0))['missing'])


def test_character_finished_can_move_to_specific_pet_node_and_completion_is_pure():
    p = umbral(survivor='維納托', awakening=6, awakening_goal=6, taloxa=4, awakening_cores=20)
    before = deepcopy(p)
    step = engine.recommend(p)['primary']
    assert step['id'] == 'pet_umbral' and step['target'] == '幽暗之靈覺醒黃4'
    assert related_guide(step) == 'umbral-soul'
    assert len(operating_steps(step)['steps']) == 3
    updated = engine.completion_preview(p, step)['profile']
    assert p == before and updated['pet_star'] == 4 and updated['awakening_cores'] == 20
    assert updated['pet_preview_matches'] is None and updated['pet_materials_ready'] is None
    next_step = engine.recommend(updated)['primary']
    assert next_step['target'] == '幽暗之靈覺醒紅5' and next_step['status'] == '待核對材料'
    with pytest.raises(ValueError):
        engine.completion_preview(updated, step)


def test_free_pet_check_precedes_named_paid_node():
    assert engine.recommend(umbral(pet_skills_ready=False))['primary']['id'] == 'pet_skills'


def test_reserve_stat_keeps_unknown_and_no_total_damage_claim():
    assert reserve_stat(None,60)['state'] == 'unknown'
    assert reserve_stat(10,60)['value'] == 6
    assert reserve_stat(10,0)['value'] == 0
    for value, sync in ((-1,60),(1,101),(float('nan'),60),(True,60)):
        with pytest.raises(ValueError):
            reserve_stat(value,sync)


@pytest.mark.parametrize('coins,reserve,price,requested,safe,maximum,cost,shortfall', [
    (20000, 8000, 3000, 4, True, 4, 12000, 0),
    (20000, 8000, 3000, 5, False, 4, 15000, 3000),
    (100, 200, 30, 0, True, 0, 0, 0),
    (0, 0, 30, 1, False, 0, 30, 30),
    (100, 1, 30, 3, True, 3, 90, 0),
])
def test_guild_budget_is_only_exact_coin_arithmetic(coins,reserve,price,requested,safe,maximum,cost,shortfall):
    result = guild_ticket_budget(coins,reserve,price,requested)
    assert result['safe'] == safe and result['max_tickets'] == maximum
    assert result['cost'] == cost and result['shortfall'] == shortfall
    assert 'gem_need' not in result and 'projected_free' not in result


@pytest.mark.parametrize('values', [(None,0,30,1), (10,None,30,1), (10,0,None,1), (10,0,30,None)])
def test_unknown_guild_budget_never_assumes_a_price_or_reserve(values):
    assert guild_ticket_budget(*values)['state'] == 'unknown'


@pytest.mark.parametrize('values', [(-1,0,30,1), (10,-1,30,1), (10,0,0,1),
                                    (10,0,30,-1), (True,0,30,1), (10.5,0,30,1)])
def test_guild_budget_rejects_invalid_coin_units(values):
    with pytest.raises(ValueError):
        guild_ticket_budget(*values)


def test_guild_activity_replaces_diamond_formula_and_readback_does_not_touch_profile():
    app = boot('活動')
    profile = {'survivor':'維納托', 'awakening':6, 'awakening_cores':20}
    app.session_state['player_profile'] = deepcopy(profile)
    selector = by_label(app.selectbox, '來源文章中的近期／歷史活動')
    selector.set_value(next(value for value in selector.options if '潮汐' in value)).run()
    assert not app.exception and not any(x.label == '目前寶石' for x in app.number_input)
    assert not any(x.label == '計算補鑽成本' for x in app.button)
    assert [x.value for x in app.number_input] == [None] * 4
    for label, value in [('目前公會幣',20000),('本期每張探索券公會幣價格',3000),
                         ('保留給公會商店固定物資的公會幣',8000),('這次想買的探索券張數',5)]:
        by_label(app.number_input,label).set_value(value)
    app.run()
    assert not app.exception
    assert by_label(app.metric,'本次買券成本（公會幣）').value == '15,000'
    assert by_label(app.metric,'扣除保留額後最多可買（張）').value == '4'
    assert any('還差 3,000 公會幣' in x.value for x in app.warning)
    assert app.session_state['player_profile'] == profile


def test_ab_medians_ranges_and_bad_inputs():
    assert compare_runs('100,101', '100,101,102')['state'] == 'unknown'
    result = compare_runs('100,101,102','110,111,112')
    assert result['median_a'] == 101 and result['median_b'] == 111
    assert result['min_a'] == 100 and not result['range_overlap']
    assert compare_runs('0,0,0','1,1,1')['change'] is None
    assert compare_runs('100,110,90','105,115,95')['range_overlap']
    for value in ('NaN,1,1','Infinity,1,1','-1,1,1','abc,1,1',','.join(['1']*31)):
        with pytest.raises(ValueError):
            compare_runs(value,'1,1,1')


def test_umbral_small_recipe_form_and_completed_node_do_not_touch_other_stock():
    app = boot()
    app.session_state['player_profile'] = umbral(pet_preview_matches=None, awakening_cores=20)
    app.run()
    assert not app.exception
    by_label(app.selectbox,'幽暗之靈目標效果與遊戲預覽一致').set_value(True)
    by_label(app.button,'更新這一步的材料').click().run()
    by_label(app.button,'我已在遊戲完成，排下一步').click().run()
    assert not app.exception and app.session_state['player_profile']['pet_star'] == 4
    assert app.session_state['player_profile']['awakening_cores'] == 20


def test_edited_existing_pet_cannot_reuse_previous_recipe_confirmation():
    before = umbral()
    after = {**before, 'pet_star':4}
    clean = engine.invalidate_pet_verification(before, after)
    assert clean['pet_preview_matches'] is None and clean['pet_materials_ready'] is None
    assert before['pet_materials_ready'] is True
    assert engine.invalidate_pet_verification(before,before)['pet_materials_ready'] is True
    assert engine.invalidate_pet_verification({},before)['pet_materials_ready'] is True
    assert engine.import_profile(engine.export_profile(before).encode())['pet_name']=='幽暗之靈'


def test_pet_editor_draft_switch_does_not_change_profile_and_save_invalidates_recipe():
    app = boot()
    original = umbral(awakening_cores=20)
    app.session_state['player_profile'] = deepcopy(original)
    app.radio[0].set_value('我的帳號').run()
    by_label(app.radio, '這次更新哪一項').set_value('寵物').run()
    assert by_label(app.radio, '寵物目標怎麼填').value == '來源節點：幽暗之靈'
    by_label(app.radio, '寵物目標怎麼填').set_value('其他寵物：遊戲預覽').run()
    assert app.session_state['player_profile'] == original
    assert not any(x.label == '現役異寵覺醒星級' for x in app.selectbox)
    target = '測試寵覺醒黃4'
    by_label(app.text_input, '遊戲預覽的下一個完整節點（含寵物名稱與等級）').set_value(target)
    by_label(app.selectbox, '這個節點實際解鎖的效果').set_value('主人增傷／有效增益')
    by_label(app.button, '儲存並重新排序').click().run()
    saved = app.session_state['player_profile']
    assert not app.exception and saved['pet_name'] == '其他'
    assert saved['pet_target'] == target and saved['pet_star'] is None
    assert saved['pet_materials_ready'] is None and saved['pet_preview_matches'] is None
    assert saved['awakening_cores'] == 20


def test_all_guide_articles_and_activity_render_without_any_network_request(monkeypatch):
    import urllib.request
    from streamlit.testing.v1 import AppTest
    from test_decision_ui import APP
    from guide_content import GUIDES

    calls = []
    def forbidden(*args, **kwargs):
        calls.append(args)
        raise AssertionError('Reading a core guide must not require the source server')
    monkeypatch.setattr(urllib.request, 'urlopen', forbidden)
    for guide in GUIDES:
        app = AppTest.from_file(APP)
        app.query_params['guide'] = guide['slug']
        app.run(timeout=15)
        assert not app.exception, guide['slug']
    assert not boot('活動').exception
    assert calls == []


@pytest.mark.parametrize('now,state', [('2026-10-10T23:59:59+08:00','scheduled'),
    ('2026-10-11T00:00:00+08:00','within'), ('2026-10-15T23:59:59+08:00','within'),
    ('2026-10-16T00:00:00+08:00','ended')])
def test_event_schedule_edges_are_timezone_aware(now,state):
    result = event_window('2026-10-11T00:00:00+08:00','2026-10-16T00:00:00+08:00',datetime.fromisoformat(now))
    assert result['state']==state
    assert event_window(None,None)['state']=='unknown'
    with pytest.raises(ValueError):
        event_window('2026-10-11T00:00:00','2026-10-16T00:00:00+08:00')
