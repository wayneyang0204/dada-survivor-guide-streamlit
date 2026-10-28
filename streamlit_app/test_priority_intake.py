"""Low-input observations must improve direction without inventing inventory."""
from copy import deepcopy

import pytest
import next_step as engine
import priority_intake as intake
from direction_tools import operating_steps
from test_decision_ui import boot, by_label


def test_free_placement_uses_a_confirmation_without_inventing_counts():
    raw = {'survivor': '維納托', 'awakening': 6, 'awakening_cores': 30, 's_shards': 550, 'quantum_ready': True}
    values = intake.answer_values(raw, 'hall', '有，手上就能放')
    p = engine.clean_profile({**raw, **values})
    first = engine.recommend(p)['primary']
    assert first['id'] == 'hall_fill_check' and first['status'] == '現在可做'
    assert p['slots'] is p['red_owned'] is p['red_placed'] is None
    assert '自訂收藏館' in operating_steps(first)['entry']
    after = engine.completion_preview(p, first)['profile']
    assert after['hall_can_fill'] is False and after['red_placed'] is None
    assert after['awakening_cores'] == 30 and after['hearts'] is None
    assert engine.recommend(after)['primary']['id'] == 'venato'
    assert engine.import_profile(engine.export_profile(p).encode()) == p


@pytest.mark.parametrize('confirmation', [True, False, None])
def test_exact_hall_counts_take_precedence_over_shortcut(confirmation):
    p = dict(slots=2, red_owned=2, red_placed=1, hall_can_fill=confirmation)
    assert engine.recommend(p)['primary']['id'] == 'hall_fill'
    assert not any(q['id'] == 'hall' for q in intake.questions(p))
    p['red_placed'] = 2
    assert not any(s['id'] == 'hall_fill_check' for s in engine.roadmap(p)['queue'])


def test_skip_is_not_a_no_and_changes_no_profile_fields():
    p = dict(survivor='維納托', awakening=6)
    before = deepcopy(p)
    first = intake.questions(p)[0]
    pending = intake.remaining(p, {first['id']: first['token']})
    assert pending[0]['id'] == 'weapon' and p == before
    assert engine.clean_profile(p)['hall_can_fill'] is None
    # A relevant state change makes the previously skipped observation useful again.
    assert intake.remaining({**p, 'slots': 3}, {first['id']: first['token']})[0]['id'] == 'hall'


@pytest.mark.parametrize('counts', [{'slots': 0}, {'red_owned': 0}, {'slots': 2, 'red_placed': 2}, {'red_owned': 3, 'red_placed': 3}])
def test_partial_counts_cannot_be_overridden_by_a_free_placement_shortcut(counts):
    p = {**counts, 'hall_can_fill': True}
    assert engine.hall_fill_state(p) is False
    assert not any(q['id'] == 'hall' for q in intake.questions(p))
    assert not any(s['id'] == 'hall_fill_check' for s in engine.roadmap(p)['queue'])


def test_newly_acquired_collection_invalidates_old_no_free_placement_answer():
    p = {'neck': '破壞者徽記', 'memory': 0, 'red_owned': 2, 'hall_can_fill': False}
    first = engine.recommend(p)['primary']
    assert first['id'] == 'memory'
    after = engine.completion_preview(p, first)['profile']
    assert after['red_owned'] == 3 and after['hall_can_fill'] is None


def test_exact_role_and_collection_choices_reorder_without_stock_fields():
    p = dict(survivor='維納托', awakening=6, awakening_goal=6, hall_can_fill=False,
             weapon='雙絕槍', weapon_e=1)
    p.update(intake.answer_values(p, 'drone', '雙生無人機'))
    p.update(intake.answer_values(p, 'taloxa', 'R4'))
    p.update(intake.answer_values(p, 'dark_matter', '黃3'))
    first = engine.recommend(p)['primary']
    assert first['id'] == 'dark_matter' and first['update']['dark_matter'] == 5
    assert first['status'] == '待核對材料'
    cleaned = engine.clean_profile(p)
    assert all(cleaned[k] is None for k in ('red_boxes', 'hearts', 'relic_cores', 's_shards', 'awakening_cores'))
    with pytest.raises(ValueError): intake.answer_values(p, 'dark_matter', '黃3')
    with pytest.raises(ValueError): intake.answer_values({}, 'weapon', '猜一個')


def test_pet_name_and_star_need_no_typed_effect_or_invented_material_readiness():
    p = dict(pet_materials_ready=True, pet_preview_matches=True, pet_target='舊目標')
    p.update(intake.answer_values(p, 'pet', '幽暗之靈'))
    p.update(intake.answer_values(p, 'pet_skills', '已核對並裝好'))
    p.update(intake.answer_values(p, 'pet_star', '黃3'))
    first = engine.recommend(p)['primary']
    assert first['id'] == 'pet_umbral' and first['update']['pet_star'] == 4
    assert p['pet_materials_ready'] is None and p['pet_preview_matches'] is None
    assert p['pet_target'] is None and first['status'] == '待核對材料'


def test_switching_drone_form_does_not_keep_another_forms_energy():
    values = intake.answer_values({'drone_energy': 3000, 'drone_form': '普通'}, 'drone', '雙生無人機')
    assert values['drone_energy'] is None
    assert 'drone_red' not in values  # A consumed component is not current inventory.
    values = intake.answer_values({'drone_energy': 3000, 'drone_form': '雙生'}, 'drone', '雙生無人機')
    assert 'drone_energy' not in values


def test_paused_character_has_a_direct_question_and_can_resume_without_editor():
    a = boot()
    a.session_state['player_profile'] = {'survivor': '維納托', 'awakening': 6}
    a.run()
    by_label(a.button, '角色先停在 R6，比較其他系統').click().run()
    assert a.button(key='answer_hall_0') and not a.exception
    assert not by_label(a.expander, '已知配置與參考門檻').proto.expanded
    by_label(a.button, '沒有可直接放的').click().run()
    assert a.button(key='answer_weapon_0')
    by_label(a.button, '重新比較主位下一階').click().run()
    assert a.session_state['player_profile']['awakening_goal'] is None
    assert a.session_state['player_profile']['hall_can_fill'] is False
    assert any('維納托 R6 → R7' in m.value for m in a.markdown)


def test_start_without_character_preserves_selected_mode_and_unknown_levels():
    a = boot()
    by_label(a.selectbox, '主要模式').set_value('遠征／月礦首領')
    by_label(a.button, '角色稍後填，先看其他升級').click().run()
    p = a.session_state['player_profile']
    assert p['mode'] == '遠征／月礦首領'
    assert p['survivor'] is None and p['awakening'] is None and p['awakening_cores'] is None
    assert a.button(key='answer_hall_0') and not a.exception


def test_known_observations_are_not_asked_again_after_navigation():
    a = boot()
    a.session_state['player_profile'] = {'survivor': '維納托', 'awakening': 6, 'twin_drone': True,
        'taloxa': 4, 'dark_matter': 3, 'weapon': '雙絕槍', 'weapon_e': 1, 'hall_can_fill': False}
    a.run()
    a.radio[0].set_value('攻略首頁').run()
    a.radio[0].set_value('下一步').run()
    assert a.button(key='answer_pet_0')
    assert not any(b.key == 'answer_drone_0' for b in a.button)
    assert not any(b.key and b.key.startswith('answer_dark_matter_') for b in a.button)


def test_editing_hall_counts_invalidates_the_shortcut():
    a = boot()
    a.session_state['player_profile'] = {'hall_can_fill': False}
    a.run()
    a.radio[0].set_value('我的帳號').run()
    by_label(a.radio, '這次更新哪一項').set_value('普通典藏館').run()
    by_label(a.number_input, '全部已開槽位').set_value(3)
    by_label(a.button, '儲存並重新排序').click().run()
    assert a.session_state['player_profile']['hall_can_fill'] is None
    assert a.button(key='answer_hall_0') and not a.exception


def test_inline_answers_undo_skip_and_targeted_branch_stay_on_route():
    a = boot()
    a.session_state['player_profile'] = {'survivor': '維納托', 'awakening': 6, 'awakening_goal': 6}
    a.run()
    by_label(a.button, '不確定，先跳過').click().run()
    assert a.button(key='answer_weapon_0')
    assert a.session_state['player_profile'].get('hall_can_fill') is None
    a.button(key='ask_pet').click().run()
    by_label(a.button, '幽暗之靈').click().run()
    assert a.button(key='answer_pet_skills_0') and a.radio[0].value == '下一步'
    by_label(a.button, '已核對並裝好').click().run()
    by_label(a.button, '黃3').click().run()
    p = a.session_state['player_profile']
    assert p['pet_star'] == 3 and p['pet_materials_ready'] is None
    card = next(m.value for m in a.markdown if 'aria-label="本次第一步"' in m.value)
    assert '幽暗之靈覺醒黃4' in card
    a.button(key='undo_quick_answer').click().run()
    assert a.session_state['player_profile']['pet_star'] is None
    assert a.session_state['player_profile']['pet_skills_ready'] is True
    assert not a.exception


def test_undo_answer_disappears_after_unrelated_manual_edit():
    a = boot()
    a.session_state['player_profile'] = {'survivor': '維納托', 'awakening': 6}
    a.run()
    by_label(a.button, '沒有可直接放的').click().run()
    assert a.button(key='undo_quick_answer')
    by_label(a.button, '角色先停在 R6，比較其他系統').click().run()
    assert not any(b.key == 'undo_quick_answer' for b in a.button)


def test_known_shortage_stays_on_card_when_other_materials_are_unknown():
    a = boot()
    a.session_state['player_profile'] = {'survivor': '維納托', 'awakening': 6, 'awakening_cores': 20}
    a.run()
    card = next(m.value for m in a.markdown if 'aria-label="本次第一步"' in m.value)
    assert '還差 10' in card and '庫存尚未填寫' not in card
    assert any('材料尚未核對' in c.value for c in a.caption)
