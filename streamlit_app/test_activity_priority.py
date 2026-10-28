from copy import deepcopy
from datetime import datetime

import pytest
from streamlit.testing.v1 import AppTest

from activity_status import event_phase, preferred_event, current_playbook
from data_engine import EVENT_PLAYBOOKS, match_event_playbook
import next_step as engine
import quick_start as quick
from test_decision_ui import APP, by_label


TIME=next(m for m in EVENT_PLAYBOOKS if m['name']=='時光拼圖')
BEACH=next(m for m in EVENT_PLAYBOOKS if m['name']=='沙灘尋寶')


def at(value):return datetime.fromisoformat(value)


@pytest.mark.parametrize('when,state,can_spend',[
    ('2026-10-16T23:59:59+08:00','upcoming',False),
    ('2026-10-17T00:00:00+08:00','active',True),
    ('2026-10-21T23:59:59+08:00','active',True),
    ('2026-10-22T00:00:00+08:00','exchange',False),
    ('2026-10-22T15:59:59+00:00','exchange',False),
    ('2026-10-23T00:00:00+08:00','ended',False),
])
def test_play_and_exchange_have_separate_exclusive_boundaries(when,state,can_spend):
    actual=event_phase(TIME,at(when))
    assert actual['state']==state and actual['can_spend'] is can_spend
    assert actual['basis']=='社群表列'
    assert actual['exchange_ends']=='10/23 00:00'


@pytest.mark.parametrize('bad',[
    {'starts_at':'2026-10-20','ends_at':'2026-10-21'},
    {'starts_at':'2026-10-22T00:00:00+08:00','ends_at':'2026-10-21T00:00:00+08:00'},
    {**TIME,'exchange_ends_at':'2026-10-21T00:00:00+08:00'},
])
def test_bad_schedule_is_not_silently_active(bad):
    with pytest.raises(ValueError):event_phase(bad)


def test_unknown_schedule_and_naive_now_never_look_active():
    assert event_phase({})['state']=='unknown' and not event_phase({})['can_spend']
    with pytest.raises(ValueError):event_phase(TIME,datetime(2026,10,22))


@pytest.mark.parametrize('when,expected',[
    ('2026-10-16T12:00:00+08:00','時光拼圖'),
    ('2026-10-20T12:00:00+08:00','時光拼圖'),
    ('2026-10-22T12:00:00+08:00','時光拼圖'),
    ('2026-10-23T00:00:00+08:00','沙灘尋寶'),
])
def test_active_then_exchange_then_nearest_upcoming_is_preferred(when,expected):
    models=[BEACH,TIME]
    assert models[preferred_event(models,at(when))]['name']==expected


def test_exchange_answer_does_not_repeat_spending_instructions():
    brief=current_playbook(EVENT_PLAYBOOKS,at('2026-10-22T12:00:00+08:00'))
    assert brief['state']=='exchange' and '只處理兌換' in brief['title']
    assert '850' not in str(brief['steps']) and '700' not in str(brief['steps'])
    assert '不補鑽' in str(brief['steps']) and not brief['can_spend']


def test_beach_schedule_changes_from_official_preview_to_verified_active_guide():
    assert event_phase(BEACH,at('2026-10-22T12:00:00+08:00'))['starts']=='10/23 00:00'
    assert BEACH['target']==820
    brief=current_playbook([BEACH],at('2026-10-22T12:00:00+08:00'))
    assert brief['state']=='upcoming' and '官方活動卡' in brief['action']
    assert not brief['can_spend'] and '固定' in str(brief['steps'])
    active=current_playbook([BEACH],at('2026-10-23T12:00:00+08:00'))
    assert active['state']=='active' and active['can_spend']
    assert '820' in str(BEACH['highlights']) and '1000' in str(BEACH['highlights'])


def test_beach_exchange_extension_is_labelled_as_community_schedule():
    phase=event_phase(BEACH,at('2026-10-28T12:00:00+08:00'))
    assert phase['state']=='exchange' and phase['exchange_basis']=='社群表列'
    assert '社群表列兌換至 10/29 00:00' in phase['action'] and not phase['can_spend']


def test_archived_events_leave_current_answers_instead_of_reusing_old_targets():
    brief=current_playbook(EVENT_PLAYBOOKS,at('2026-11-05T00:00:00+08:00'))
    assert brief['state']=='unknown' and '待核對' in brief['title']
    assert '850' not in str(brief) and '時光拼圖' not in brief['title']


def test_one_line_hall_counts_find_free_action_and_do_not_fabricate_hearts():
    result=quick.parse_snapshot('典藏已開8格、持有紅收藏6件、已擺入紅收藏4件')
    assert not result['errors'] and not result['unmatched']
    assert result['fields']==dict(slots=8,red_owned=6,red_placed=4)
    plan=engine.priority_brief(result['fields'])
    assert plan['primary']['id']=='hall_fill' and plan['label']=='先做這一步'
    assert engine.clean_profile(result['fields'])['hearts'] is None


def test_explicit_ordinary_tech_is_not_asked_to_confirm_its_form_again():
    p=quick.parse_snapshot('普通無人機3000')['fields']
    notes=quick.context_notes(p)
    assert any('普通無人機' in n['title'] and '不需要重填' in n['body'] for n in notes)
    assert not any('形態尚未確認' in n['title'] for n in notes)


def test_priority_preview_is_pure_and_unknown_materials_are_not_completed():
    p={'survivor':'維納托','awakening':6,'awakening_cores':20}
    before=deepcopy(p)
    plan=engine.priority_brief(p)
    assert plan['primary']['id']=='venato' and plan['following'] is None
    assert plan['label']=='先存材料，不急著升' and p==before
    assert any(c['state']=='unknown' for c in plan['primary']['checks'])


def test_ready_action_preview_exposes_a_new_step_without_applying_it():
    p={'survivor':'維納托','awakening':6,'awakening_cores':30,'s_shards':550,'quantum_ready':True}
    before=deepcopy(p)
    plan=engine.priority_brief(p)
    assert plan['label']=='先做這一步' and plan['following']['target']!=plan['primary']['target']
    assert p==before and len(plan['queue'])<=2


def test_paused_survivor_with_known_tech_shows_a_concrete_conditional_hint():
    p={'survivor':'維納托','awakening':6,'awakening_goal':6,'lightning_form':'雙生','lightning_energy':1600}
    before=deepcopy(p)
    plan=engine.priority_brief(p)
    assert plan['primary'] is None and plan['technology_hint']['target']==1650
    assert plan['technology_hint']['gap']==50 and plan['technology_hint']['state']=='verify'
    assert p==before


def test_technology_hint_does_not_steal_priority_from_confirmed_free_action():
    plan=engine.priority_brief({'slots':8,'red_owned':6,'red_placed':4,'lightning_form':'雙生','lightning_energy':1600})
    assert plan['primary']['id']=='hall_fill' and plan['technology_hint'] is None


def test_ordinary_tech_is_not_offered_a_twin_milestone_hint():
    plan=engine.priority_brief({'lightning_form':'普通','lightning_energy':1600})
    assert plan['primary'] is None and plan['technology_hint'] is None


def test_invalid_merged_hall_counts_block_apply_preview_and_preserve_state():
    app=AppTest.from_file(APP);app.session_state['主導覽']='下一步';app.run()
    by_label(app.text_input,'目前配置（一行即可）').set_value('典藏已開4格、持有紅收藏3件、已擺入紅收藏6件').run()
    by_label(app.button,'辨識這行配置').click().run()
    assert app.error and not any(b.label=='套用這行現況' for b in app.button)
    assert not app.exception


def test_primary_action_opens_materials_and_never_records_completion():
    app=AppTest.from_file(APP)
    app.session_state['主導覽']='下一步'
    p={'survivor':'維納托','awakening':6,'awakening_cores':20}
    app.session_state['player_profile']=p.copy();app.run()
    assert any('本次第一步' in m.value for m in app.markdown)
    assert not by_label(app.expander,'依配置補充門檻').proto.expanded
    assert not by_label(app.expander,'材料缺額與詳細排序').proto.expanded
    by_label(app.button,'回到第一優先').click().run()
    assert by_label(app.expander,'材料缺額與詳細排序').proto.expanded
    assert app.session_state['player_profile']==p


def test_article_activity_entry_preserves_selected_event_on_subsequent_rerun():
    app=AppTest.from_file(APP);app.query_params['guide']='beach-treasure';app.run()
    by_label(app.button,'查看本期階段與活動步驟').click().run()
    selected=by_label(app.selectbox,'來源文章中的近期／歷史活動')
    assert '沙灘尋寶' in selected.value
    app.run()
    assert '沙灘尋寶' in by_label(app.selectbox,'來源文章中的近期／歷史活動').value
    phase=event_phase(match_event_playbook(selected.value))
    if phase['state'] in ('upcoming','exchange','ended'):
        assert not app.number_input and not any(b.label=='計算補鑽成本' for b in app.button)
    assert not app.exception


def test_different_events_do_not_inherit_progress_or_ticket_prices():
    from test_decision_ui import fill_event_inputs, open_event_calculator
    app=AppTest.from_file(APP);app.session_state['主導覽']='活動';app.run()
    selector=by_label(app.selectbox,'來源文章中的近期／歷史活動')
    selector.set_value(next(s for s in selector.options if '時光拼圖' in s)).run()
    fill_event_inputs(app)
    assert by_label(app.number_input,'目前活動進度').value==0
    selector=by_label(app.selectbox,'來源文章中的近期／歷史活動')
    selector.set_value(next(s for s in selector.options if '沙灘尋寶' in s)).run()
    assert not app.number_input
    open_event_calculator(app)
    assert by_label(app.number_input,'目前活動進度').value is None
    assert by_label(app.number_input,'一次票券／抽取寶石成本').value is None
    assert by_label(app.number_input,'目標里程碑').value==820
    assert not app.exception
