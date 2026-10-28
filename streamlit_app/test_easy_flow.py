"""Task-first entry and one-target editing, without assuming player inventory."""
from copy import deepcopy

from streamlit.testing.v1 import AppTest
from test_decision_ui import APP, boot, by_label


def test_home_starts_with_three_tasks_and_no_unsolicited_answer():
    app=AppTest.from_file(APP).run()
    assert all(app.button(key=k) for k in ('start_upgrade','start_box','start_event'))
    assert by_label(app.radio,'選一個問題').value is None
    for label in ('常見養成問題','近期更新','完整攻略目錄'):
        assert not by_label(app.expander,label).proto.expanded
    assert not any('class="desk-answer"' in m.value for m in app.markdown)
    assert 'player_profile' not in app.session_state
    app.button(key='start_box').click().run()
    assert app.query_params['guide']==['red-choice-box']
    by_label(app.button,'← 攻略首頁').click().run()
    app.button(key='start_upgrade').click().run()
    assert app.radio[0].value=='下一步' and not app.exception


def test_click_setup_requires_actual_selections_and_preserves_zero_awakening():
    app=boot()
    assert not app.number_input
    assert by_label(app.selectbox,'主位特工').value is None
    assert by_label(app.selectbox,'覺醒等級').value is None
    by_label(app.button,'建立我的升級路線').click().run()
    assert app.error and 'player_profile' not in app.session_state
    by_label(app.selectbox,'主位特工').set_value('維納托')
    by_label(app.selectbox,'覺醒等級').set_value(0)
    by_label(app.button,'建立我的升級路線').click().run()
    p=app.session_state['player_profile']
    assert p['awakening']==0 and p['awakening_cores'] is None and p['s_shards'] is None
    assert p['pet_materials_ready'] is None and not app.exception


def test_main_card_materials_update_in_place_without_full_profile_editor():
    app=boot()
    raw={'survivor':'維納托','awakening':6,'taloxa':4,'awakening_cores':20}
    app.session_state['player_profile']=deepcopy(raw);app.run()
    controls=next(x for x in app.get('popover') if x.proto.popover.label=='核對這一步的材料')
    assert len(controls.get('form'))==1
    assert len(app.get('form'))==1
    assert not by_label(app.expander,'材料缺額與詳細排序').proto.expanded
    assert by_label(app.number_input,'現有覺醒核心').value==20
    by_label(app.number_input,'可用於主位的S特工碎片').set_value(550)
    by_label(app.selectbox,'量子碎片是否足夠升主位下一階').set_value(True)
    by_label(app.button,'更新這一步的材料').click().run()
    assert app.radio[0].value=='下一步'
    assert app.session_state['player_profile']['s_shards']==550
    assert app.session_state['player_profile']['awakening_cores']==20
    card=next(m.value for m in app.markdown if 'aria-label="本次第一步"' in m.value)
    assert '還差 10' in card and '遊戲入口' in card
    assert len(app.get('form'))==1 and not app.exception


def test_clearing_a_category_search_restores_three_home_tasks():
    app=AppTest.from_file(APP).run()
    by_label(app.radio,'攻略分類').set_value('收藏典藏').run()
    by_label(app.text_input,'搜尋攻略').set_value('暗物質黃五星').run()
    assert not any(b.key=='start_upgrade' for b in app.button)
    by_label(app.button,'清除搜尋').click().run()
    by_label(app.radio,'攻略分類').set_value('全部').run()
    assert all(app.button(key=k) for k in ('start_upgrade','start_box','start_event'))
    assert not app.exception and 'player_profile' not in app.session_state
