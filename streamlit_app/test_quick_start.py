import pytest
import quick_start as quick
import next_step as engine
from test_decision_ui import boot, by_label, APP
from streamlit.testing.v1 import AppTest


@pytest.mark.parametrize('text,expected',[
    ('維納托R6、塔洛莎R4、楊大師R1、20個覺醒核心',{'survivor':'維納托','awakening':6,'taloxa':4,'yang':1,'awakening_cores':20}),
    ('塔洛莎R4、主位維納托R6、雙絕槍E1V2',{'survivor':'維納托','awakening':6,'weapon_e':1,'weapon_v':2}),
    ('雙生雷電1600、普通無人機3000',{'lightning_form':'雙生','lightning_energy':1600,'drone_form':'普通','drone_energy':3000}),
    ('幽暗黃4、暗物質魁儡黃3、記憶編輯器紅1',{'pet_star':4,'dark_matter':3,'memory':6}),
    ('金Ｒ３、神器核心0、S碎片550',{'survivor':'金','awakening':3,'king':3,'relic_cores':0,'s_shards':550}),
    ('雙生雷電1,600、覺醒核心1,000',{'lightning_form':'雙生','lightning_energy':1600,'awakening_cores':1000}),
])
def test_explicit_parser_recognises_current_state_only(text,expected):
    result=quick.parse_snapshot(text)
    assert not result['errors'] and not result['unmatched']
    assert all(result['fields'][k]==v for k,v in expected.items())
    assert set(result['fields']).issubset(engine.FIELDS)
    p=engine.clean_profile(result['fields'])
    assert p['quantum_ready'] is None and p['pet_materials_ready'] is None
    assert p['gear_materials_ready'] is None


@pytest.mark.parametrize('text',[
    '維納托R6→R7','維納托要升R7','幽暗黃4？','沒有幽暗黃4','沒幽暗黃4','目標維納托R7','缺幽暗黃4',
    '維納托R6、維納托R7','主位維納托R6、主位塔洛莎R4',
    '維納托R9','維納托R6.5','雙絕槍E1V2.5','幽暗黃3.5',
    '覺醒核心-1','覺醒核心10001','雷電1.5','password:1234','abc@example.com','覺醒核心1e3','雷電1,50',
])
def test_invalid_conflicting_goals_or_secrets_cannot_be_applied(text):
    assert quick.parse_snapshot(text)['errors']


def test_unknown_fields_are_visible_not_guessed():
    r=quick.parse_snapshot('維納托R6、神秘材料18、無人機3000')
    assert '神秘材料18' in r['unmatched']
    assert 'drone_form' not in r['fields'] and 'twin_drone' not in r['fields']
    assert r['notes']


def test_retargeting_clears_only_stale_target_confirmations():
    fields=quick.parse_snapshot('主位維納托R6、普通無人機3000、雙絕槍E2V1')['fields']
    updated=quick.apply_fields({'survivor':'塔洛莎','s_shards':500,'awakening_goal':4,
                               'quantum_ready':True,'gear_materials_ready':True},fields)
    assert updated['s_shards'] is None and updated['awakening_goal'] is None
    assert updated['quantum_ready'] is None and updated['gear_materials_ready'] is None
    assert updated['twin_drone'] is False
    assert quick.apply_fields({'survivor':'維納托','awakening':6,'quantum_ready':True}, {'awakening_cores':20})=={'awakening_cores':20}


def test_recipe_single_path_totals_and_other_path_not_silently_charged():
    assert quick.ss_recipe(0,3)==dict(cores=6,stones=70,base=1500,epic=4,legendary=0,other_path_min=None,source=quick.SS_SOURCE)
    assert quick.ss_recipe(3,5)==dict(cores=13,stones=140,base=1500,epic=2,legendary=1,other_path_min=3,source=quick.SS_SOURCE)
    assert quick.ss_recipe(0,5)['cores']==19


@pytest.mark.parametrize('current,target',[(3,3),(4,2),(-1,1),(0,6),(False,1),(0,1.5)])
def test_invalid_recipe_ranges_rejected(current,target):
    with pytest.raises(ValueError):quick.ss_recipe(current,target)


def test_brief_honours_pause_and_never_awakens_unowned_pet():
    notes=quick.context_notes({'survivor':'維納托','awakening':6,'awakening_goal':6,'pet_name':'幽暗之靈','pet_star':0})
    assert not any('R7' in n['title'] or n['slug']=='umbral-soul' for n in notes)
    assert '暫停' in notes[0]['body']


def test_brief_uses_known_stocks_without_asking_for_known_recipe():
    notes=quick.context_notes({'survivor':'維納托','awakening':6,'awakening_cores':20,'s_shards':400,
                              'lightning_form':'雙生','lightning_energy':1600})
    text=str(notes)
    assert '核心差10' in text and '碎片差150' in text and '1,650' in text and '50' in text
    p=engine.clean_profile(quick.parse_snapshot('雙生雷電1600')['fields'])
    assert engine.import_profile(engine.export_profile(p))['lightning_energy']==1600


def test_owned_link_adjustments_precede_paid_survivor_candidate():
    notes=quick.context_notes({'survivor':'維納托','awakening':6,'yang':1,'taloxa':4,'twin_drone':True})
    assert '武魂' in notes[0]['title'] and '裂傷連攜' in notes[1]['title']
    assert '維納托R7' in notes[2]['title']


def test_zero_input_desk_and_one_line_apply_preserve_unknowns_and_existing_fields():
    app=boot()
    assert not app.exception and len(app.number_input)==0
    by_label(app.text_input,'目前配置（一行即可）').set_value('維納托R6、塔洛莎R4、20個覺醒核心、雙生雷電1600').run()
    by_label(app.button,'辨識這行配置').click().run()
    assert not app.exception
    with pytest.raises(KeyError):app.session_state['player_profile']
    by_label(app.button,'套用這行現況').click().run()
    assert not app.exception
    p=app.session_state['player_profile']
    assert p['awakening']==6 and p['awakening_cores']==20 and p['s_shards'] is None
    assert any('核心差10' in m.value for m in app.markdown)
    assert next(e for e in app.expander if e.label=='材料缺額與詳細排序').proto.expanded is False
    by_label(app.text_input,'目前配置（一行即可）').set_value('神器核心3').run()
    by_label(app.button,'辨識這行配置').click().run()
    by_label(app.button,'套用這行現況').click().run()
    p=app.session_state['player_profile']
    assert p['awakening']==6 and p['relic_cores']==3 and p['awakening_cores']==20


def test_editing_text_invalidates_stale_preview_and_blocked_input_has_no_apply():
    app=boot()
    by_label(app.text_input,'目前配置（一行即可）').set_value('維納托R6').run()
    by_label(app.button,'辨識這行配置').click().run()
    assert by_label(app.button,'套用這行現況')
    by_label(app.text_input,'目前配置（一行即可）').set_value('沒有幽暗黃4').run()
    assert not any(b.label=='套用這行現況' for b in app.button)
    by_label(app.button,'辨識這行配置').click().run()
    assert app.error and not any(b.label=='套用這行現況' for b in app.button)


def test_all_decision_desk_links_resolve_and_do_not_change_profile():
    import guide_content as content
    for item in quick.PLAYBOOKS.values():
        assert len(item['steps'])==3
        assert all(content.get_guide(slug,content.GUIDES) for slug in item['guides'])
    app=AppTest.from_file(APP).run()
    by_label(app.radio,'選一個問題').set_value('SS裝備需要多少材料').run()
    assert not app.exception and any('19顆' in m.value for m in app.markdown)
    app.button(key='home_read_ss-material-recipes').click().run()
    assert not app.exception and app.query_params['guide']==['ss-material-recipes']


def test_activity_gives_steps_before_any_calculator_inputs():
    app=boot('活動')
    assert not app.exception and len(app.number_input)==0
    assert '時光拼圖' in by_label(app.selectbox,'來源文章中的近期／歷史活動').value
    assert any('現在照這個順序做' in m.value for m in app.markdown)
    by_label(app.toggle,'展開寶石成本試算').set_value(True).run()
    assert len(app.number_input)==7 and by_label(app.number_input,'目前活動進度').value is None


def test_ss_recipe_article_calculates_without_number_inputs():
    app=AppTest.from_file(APP);app.query_params['guide']='ss-material-recipes';app.run()
    by_label(app.selectbox,'目前階級').set_value(3).run()
    by_label(app.selectbox,'目標階級').set_value(5).run()
    assert not app.exception and len(app.number_input)==0
    text='\n'.join(m.value for m in app.markdown)
    assert '<td>13</td>' in text and '<td>140</td>' in text


def test_community_event_schedule_never_becomes_official_and_expires():
    from datetime import datetime
    from field_tools import event_window
    from guide_content import GUIDES, get_guide
    guide=get_guide('time-jigsaw',GUIDES)
    before=event_window(guide['starts_at'],guide['ends_at'],datetime.fromisoformat('2026-10-18T12:00:00+08:00'),source=guide['schedule_source'])
    after=event_window(guide['starts_at'],guide['ends_at'],datetime.fromisoformat('2026-10-22T00:00:00+08:00'),source=guide['schedule_source'])
    assert before['state']=='within' and '社群表列' in before['label'] and '官方' not in before['label']
    assert after['state']=='ended' and '社群表列' in after['label']


def test_intake_limits_and_literal_zero_are_explicit():
    with pytest.raises(ValueError):quick.parse_snapshot('a'*1001)
    assert quick.parse_snapshot('覺醒核心0')['fields']=={'awakening_cores':0}
    assert quick.parse_snapshot('')['fields']=={}
