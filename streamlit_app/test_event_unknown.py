from streamlit.testing.v1 import AppTest
from test_decision_ui import APP, by_label, fill_event_inputs


def test_event_blanks_never_generate_a_fake_budget():
    app = AppTest.from_file(APP)
    app.session_state['主導覽'] = '活動'
    app.run(timeout=15)
    assert not app.exception and not app.metric
    assert by_label(app.button,'計算補鑽成本').disabled
    for label in ('目前活動進度','剩餘天數','每天還可拿的免費進度',
                  '一次票券／抽取增加進度','一次票券／抽取寶石成本','目前寶石'):
        assert by_label(app.number_input,label).value is None
    fill_event_inputs(app)
    assert not by_label(app.button,'計算補鑽成本').disabled
    by_label(app.button,'計算補鑽成本').click().run()
    assert len(app.metric)==4
    by_label(app.number_input,'每天還可拿的免費進度').set_value(None).run()
    assert not app.metric and by_label(app.button,'計算補鑽成本').disabled


def test_archived_event_requires_explicit_historical_confirmation_and_hides_old_result():
    app = AppTest.from_file(APP)
    app.session_state['主導覽'] = '活動'
    app.run(timeout=15)
    selector = by_label(app.selectbox,'來源文章中的近期／歷史活動')
    selector.set_value(next(value for value in selector.options if '戲院' in value)).run()
    fill_event_inputs(app)
    assert by_label(app.button,'計算補鑽成本').disabled
    check = '我正在核對復刻或做歷史試算，不是依原期排程投入'
    by_label(app.checkbox,check).set_value(True).run()
    by_label(app.button,'計算補鑽成本').click().run()
    assert len(app.metric) == 4
    by_label(app.checkbox,check).set_value(False).run()
    assert not app.metric and by_label(app.button,'計算補鑽成本').disabled
    by_label(app.checkbox,check).set_value(True).run()
    selector = by_label(app.selectbox,'來源文章中的近期／歷史活動')
    selector.set_value(next(value for value in selector.options if '雲中塔' in value)).run()
    assert not by_label(app.checkbox,check).value
