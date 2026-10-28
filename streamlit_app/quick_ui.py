"""Read first; only enter configuration when it improves the answer."""
from __future__ import annotations

import html
import streamlit as st
import quick_start as quick


def open_article(slug):
    from guide_ui import open_guide
    open_guide(slug)


def decision_desk(prefix="desk"):
    with st.container(key=f"{prefix}_decision_desk"):
        st.markdown('<div class="desk-eyebrow">直接查答案 · 不必填帳號</div><h2 class="desk-heading">你現在卡在哪裡？</h2>', unsafe_allow_html=True)
        question=st.radio("選一個問題",tuple(quick.PLAYBOOKS),label_visibility="collapsed",
                          key=f"{prefix}_question",horizontal=True,index=None)
        if question is None:
            return
        item=quick.PLAYBOOKS[question]
        if question=='現在活動怎麼做':
            from activity_status import current_playbook
            from data_engine import EVENT_PLAYBOOKS
            item=current_playbook(EVENT_PLAYBOOKS)
            st.caption(item['label']+' · '+item['action'])
        st.markdown(f'<h3 class="desk-answer">{html.escape(item["title"])}</h3>',unsafe_allow_html=True)
        rows="".join(f'<li><span class="desk-step">{i:02d}</span><div><b>{html.escape(title)}</b><p>{html.escape(body)}</p></div></li>'
                     for i,(title,body) in enumerate(item['steps'],1))
        st.markdown(f'<ol class="desk-steps">{rows}</ol><p class="desk-stop"><b>先停在哪裡</b>　{html.escape(item["stop"])}</p>',unsafe_allow_html=True)
        with st.expander("看完整門檻與操作表"):
            import guide_content
            for slug in item['guides']:
                guide=guide_content.get_guide(slug,guide_content.all_guides([]))
                if guide:
                    st.button(guide['title']+' →',key=f'{prefix}_read_{slug}',on_click=open_article,args=(slug,),width="stretch",type="tertiary")


def intake(save, prefix="quick"):
    with st.container(key=f"{prefix}_snapshot"):
        st.markdown('<h3 class="snapshot-heading">用一行帶入配置</h3>',unsafe_allow_html=True)
        st.caption('例如：維納托R6、塔洛莎R4、20個覺醒核心。只填目前現況即可。')
        text=st.text_input("目前配置（一行即可）",placeholder="維納托R6、塔洛莎R4、20個覺醒核心、雙生雷電1600",
                           max_chars=1000,key=f'{prefix}_snapshot_text')
        with st.expander('其他填寫範例'):
            st.caption('裝備：雙絕槍E1V2。收藏：暗物質傀儡黃3。寵物：幽暗黃4。科技：雙生雷電1600。')
            st.caption('免費空槽：典藏已開8格、持有紅收藏6件、已擺入紅收藏4件。紅收藏指原生傳奇品質，不是史詩紅星。不要貼帳密。')
        if st.button("辨識這行配置",key=f'{prefix}_parse',disabled=not text.strip(),width="stretch"):
            st.session_state[f'{prefix}_parsed']=dict(text=text,result=quick.parse_snapshot(text))
        parsed=st.session_state.get(f'{prefix}_parsed')
        if not parsed or parsed['text']!=text:
            return
        result=parsed['result']
        for error in result['errors']:st.error(error)
        if result['errors']:return
        if not result['fields']:
            st.info('尚未辨識到配置。可用「維納托R6」或「雙絕槍E1V2」這類寫法。');return
        from next_step import clean_profile
        try:
            clean_profile({**st.session_state.get('player_profile',{}),**quick.apply_fields(st.session_state.get('player_profile',{}),result['fields'])})
        except ValueError as exc:
            st.error(str(exc));return
        chips=''.join(f'<span><small>{html.escape(quick.LABELS.get(key,key))}</small><b>{html.escape(quick.field_value(key,value))}</b></span>'
                      for key,value in result['fields'].items())
        st.markdown(f'<div class="snapshot-chips" aria-label="已辨識配置">{chips}</div>',unsafe_allow_html=True)
        for note in result['notes']:st.caption(note)
        if result['unmatched']:
            st.warning('未套用的文字：'+'、'.join(result['unmatched'])+'。只會儲存上面已辨識的欄位。')
        st.caption('確認後更新已辨識欄位，其餘現況保留。更換主位會清除舊主位碎片／目標；覺醒或神鑄階級改變會重新核對材料，避免沿用舊確認。')
        if st.button('套用這行現況',key=f'{prefix}_apply',type='primary',width="stretch"):
            save(quick.apply_fields(st.session_state.get('player_profile',{}),result['fields']))


def contextual_brief(p, show_details=True):
    import next_step as engine
    from direction_tools import operating_steps, execution_plan
    plan=engine.priority_brief(p)
    with st.container(key="quick_context_brief"):
        who = f"{p['survivor']} R{p['awakening']} · {p['mode']}" if p.get('survivor') and p.get('awakening') is not None else '依目前已填資料'
        st.markdown(f'<div class="desk-eyebrow">{html.escape(who)}</div>',unsafe_allow_html=True)
        first=plan['primary']
        if first:
            operation=operating_steps(first)
            execution=execution_plan(first)
            action=execution['action']
            unknown = [c for c in first.get('checks', []) if c['state'] == 'unknown']
            if first['status'] == '待核對材料' and first.get('effect'):
                action = first['effect']
            checks=''.join(f'<li>{html.escape(c["label"])}：{html.escape(c["detail"])}</li>' for c in first.get('checks',[]) if c['state']=='short')
            st.markdown(f'''<section id="upgrade-priority" class="priority-main" aria-label="本次第一步"><span class="priority-label">{html.escape(plan['label'])}</span>
                <h3>{html.escape(first['title'])}</h3><p>{html.escape(action)}</p>
                <p class="priority-entry"><b>遊戲入口</b>　{html.escape(operation['entry'])}</p>
                <p><b>升到哪裡：</b>{html.escape(first['target'])}</p>
                <ul class="priority-checks">{checks}</ul></section>''',unsafe_allow_html=True)
            if unknown:
                st.caption('材料尚未核對。先比較升級方向；要算缺額時再填庫存。')
            elif first.get('gap') and not checks:st.caption(first['gap'])
            from decision_ui import render_step_inputs, render_completion, edit_resource, selected_recommendation
            _,comparison=selected_recommendation(p)
            primary_controls = comparison is not None and comparison['id']==first['id']
            left,right=st.columns(2,gap='small')
            with left:
                editable = first.get('quote_kind') or first['id'].startswith('adv') or first['id'] in ('venato','hall_open','lance_e1','twin_drone','pet_umbral','pet_node')
                if first['id'] in ('hall_fill', 'hall_fill_check') or first['id'].endswith('_rearrange'):
                    with st.popover('看擺放步驟', width='stretch'):
                        for i,item in enumerate(operation['steps'],1): st.write(f'{i}. {item}')
                elif not primary_controls:
                    st.button('核對第一優先材料',on_click=open_details,width='stretch')
                elif editable and first['status'] not in ('星數未達','資料未齊'):
                    with st.popover('核對這一步的材料',width='stretch'):
                        render_step_inputs(first,p,compact=True)
                else:
                    st.button('更新這一項配置',on_click=edit_resource,args=(first['resource'],),width='stretch')
            with right:
                if primary_controls:
                    render_completion(p,first)
                else:
                    with st.popover('遊戲內怎麼做',width='stretch'):
                        for i,item in enumerate(operation['steps'],1):
                            st.write(f'{i}. {item}')
                        st.caption(first['stop'])
            if after:=plan['following']:
                st.markdown(f'<p class="priority-after"><b>這步做完再看</b>　{html.escape(after["title"])} · {html.escape(after["status"])}</p>',unsafe_allow_html=True)
        elif hint:=plan['technology_hint']:
            st.markdown(f'''<section class="priority-main" aria-label="科技門檻候選"><span class="priority-label">先查最近的已收錄科技門檻</span>
                <h3>{html.escape(hint['name'])}：{hint['current']:,} → {hint['target']:,}</h3>
                <p><b>還差 {hint['gap']:,} 能量</b> · {html.escape(hint['effect'])}</p><p>{html.escape(hint['action'])}</p>
                <p><b>停手條件：</b>{html.escape(hint['stop'])}</p></section>''',unsafe_allow_html=True)
            st.caption('只按能量距離找候選，不代表最省材料或最高傷害；未核對的收藏與寵物仍須比較。')
            from guide_ui import open_tech_guide
            st.button('查這個諧振效果與調整方式',key='priority_tech_article',on_click=open_tech_guide,args=(hint['part'],),width='stretch')
        else:
            st.write('目前沒有符合已填配置的單一步驟；以下先列已知門檻供你核對。')
        if show_details:
            contextual_details(p, plan)


def contextual_details(p, plan):
    from direction_tools import operating_steps
    if first := plan['primary']:
        with st.expander('怎麼操作／為什麼排這一步'):
            for i,item in enumerate(operating_steps(first)['steps'],1): st.write(f'{i}. {item}')
            st.caption(plan['reason'])
            st.caption('按已填配置與已收錄門檻排序，未填的系統仍待比較。')
    if plan['queue']:
        with st.expander('後續候選 · 先不一起升'):
            for item in plan['queue']: st.write(f'{item["system"]} · {item["title"]}（{item["status"]}）')
    notes=quick.context_notes(p)
    with st.expander('依配置補充門檻',expanded=not bool(plan['primary'] or plan['technology_hint'])):
        for i,note in enumerate(notes,1):
            st.markdown(f'<div class="context-note"><span>{i:02d}</span><div><h3>{html.escape(note["title"])}</h3><p>{html.escape(note["body"])}</p></div></div>',unsafe_allow_html=True)
            st.button('查門檻與操作 →',key=f'context_read_{i}',on_click=open_article,args=(note['slug'],),type='tertiary')
        st.caption('以上為條件式候選，未代表已備齊材料。')


def open_details():
    # The top card is the global priority, not the last filtered comparison.
    st.session_state['decision_resource']='自動排序'
    st.session_state.pop('route_selected_id',None)
    st.session_state['route_details_revision']=st.session_state.get('route_details_revision',0)+1


def apply_priority_answer(question, label):
    import priority_intake as intake
    from decision_ui import profile, save
    before = profile()
    values = intake.answer_values(before, question['id'], label)
    st.session_state['quick_answer_undo'] = {'before': before, 'title': label,
        'revision': st.session_state.get('editor_revision', 0) + 1}
    branches = {'weapon': ('weapon_e',), 'drone': ('taloxa', 'dark_matter'),
                'taloxa': ('dark_matter',), 'pet': ('pet_skills', 'pet_star'),
                'pet_skills': ('pet_star',), 'neck': ('memory',)}
    next_ids = {q['id'] for q in intake.questions({**before, **values})}
    st.session_state['quick_requested'] = next((key for key in branches.get(question['id'], ()) if key in next_ids), None)
    st.session_state['decision_resource'] = '自動排序'
    save(values)


def priority_questions(p):
    """One useful question in place, with no inventory or full-profile form."""
    import priority_intake as intake
    from decision_ui import save
    if p['mode'] == '新版區域行動' or p['growth_focus'] == '生存不足':
        return
    questions = intake.questions(p)
    skipped = st.session_state.get('quick_skipped', {})
    pending = intake.remaining(p, skipped)
    requested = st.session_state.get('quick_requested')
    question = next((q for q in pending if q['id'] == requested), next(iter(pending), None))
    with st.container(key='priority_intake'):
        st.markdown('<div id="priority-questions"></div>', unsafe_allow_html=True)
        known = intake.context_labels(p)
        st.caption('已帶入：' + '、'.join(known) if known else '只選目前現況，不用先填材料數量。')
        previous = st.session_state.get('quick_answer_undo')
        if previous and previous['revision'] == st.session_state.get('editor_revision', 0):
            import next_step as engine
            if first := engine.recommend(p)['primary']:
                st.markdown(f'<div class="intake-result" role="status"><span>更新後的第一步 · {html.escape(first["status"])}</span>'
                    f'<b>{html.escape(first["title"])}</b><a href="#upgrade-priority" target="_self">查看操作 ↑</a></div>', unsafe_allow_html=True)
            if st.button('撤回回答：' + previous['title'], key='undo_quick_answer', type='tertiary'):
                st.session_state.pop('quick_answer_undo', None)
                st.session_state.pop('quick_requested', None)
                st.session_state['decision_resource'] = '自動排序'
                save(previous['before'], restoring=True)
        if question:
            st.markdown('<span class="intake-label">補一項現況，立即重排</span>'
                        f'<h3 class="intake-question">{html.escape(question["title"])}</h3>'
                        f'<p class="intake-reason">{html.escape(question["why"])}</p>', unsafe_allow_html=True)
            options = question['options']
            if len(options) <= 3:
                # One tap per observation. No default answer and no Save button.
                for i, (label, values) in enumerate(options):
                    if st.button(label, key=f'answer_{question["id"]}_{i}', width='stretch'):
                        apply_priority_answer(question, label)
            else:
                count = 2 if question['id'] == 'pet' else 3
                for start in range(0, len(options), count):
                    cells = st.columns(count, gap='small')
                    for i, (label, _) in enumerate(options[start:start+count], start):
                        with cells[i-start]:
                            if st.button(label, key=f'answer_{question["id"]}_{i}', width='stretch'):
                                apply_priority_answer(question, label)
            st.caption(question['entry'])
            later, other = st.columns(2, gap='small')
            with later:
                if st.button('不確定，先跳過', key='skip_priority_question', type='tertiary', width='stretch'):
                    st.session_state['quick_skipped'] = {**skipped, question['id']: question['token']}
                    st.session_state.pop('quick_requested', None)
                    st.rerun()
            with other:
                with st.popover('換個項目', width='stretch'):
                    for item in pending:
                        if item['id'] != question['id'] and st.button(item['title'], key=f'ask_{item["id"]}', width='stretch'):
                            st.session_state['quick_requested'] = item['id']
                            st.rerun()
        elif questions:
            st.write('其餘問題已先跳過。現有建議只比較已知配置。')
        elif p['mode'] != '新版區域行動' and p['growth_focus'] != '生存不足':
            st.write('快速核對已完成。材料不必全填，想算哪一步的缺額再展開那一步。')
            st.caption('SS套裝、進階典藏與其他寵物的完整節點，仍可在「我的配置」補充。')
        if len(pending) < len(questions):
            if st.button(f'回頭看略過的 {len(questions)-len(pending)} 項', key='restore_quick_questions', type='tertiary'):
                st.session_state.pop('quick_skipped', None)
                st.rerun()


QUICK_STYLE = """
[class*="_decision_desk"] {border:1px solid #e6ddcf;border-radius:22px;padding:1.5rem;background:#fffefa;}
.desk-eyebrow {color:#94633f;font-size:.875rem;font-weight:700;letter-spacing:.05em;}
.desk-heading {font-size:1.45rem!important;margin:.35rem 0 1rem!important;}
.desk-answer {font-size:1.1rem!important;line-height:1.6!important;margin:.8rem 0!important;}
.desk-steps {list-style:none;margin:0;padding:0;}
.desk-steps li {display:grid;grid-template-columns:2rem 1fr;gap:.6rem;padding:.9rem 0;border-bottom:1px solid #eee6dc;}
.desk-step {color:#8e542f;font-size:.875rem;font-weight:800;background:#fff0d8;border-radius:10px;height:2rem;display:grid;place-items:center;}
.desk-steps p,.context-note p {font-size:.94rem;line-height:1.85;margin:.25rem 0 0;}
.desk-stop {font-size:.88rem!important;line-height:1.8!important;color:#685d4c;background:#f4f5eb;padding:.8rem 1rem;border-radius:12px;}
[class*="_decision_desk"] [role="radiogroup"] {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.5rem;}
[class*="_decision_desk"] [data-testid="stRadioOption"] {min-height:52px;width:100%;box-sizing:border-box;border:1px solid #e9dfcf;border-radius:12px;padding:.45rem .65rem;margin:0;background:white;}
[class*="_decision_desk"] [data-testid="stRadio"] label:has(input:checked) {border-color:#a66b42;background:#fff1db;}
.snapshot-heading {font-size:1.15rem!important;margin:.4rem 0!important;}
.snapshot-chips {display:flex;flex-wrap:wrap;gap:.5rem;margin:.5rem 0;}
.snapshot-chips span {display:flex;flex-direction:column;border:1px solid #e7ddcb;border-radius:12px;padding:.55rem .75rem;background:#fff9ec;min-width:7rem;}
.snapshot-chips small {font-size:.875rem;color:#766448;}.snapshot-chips b {color:#3c4035;font-size:.95rem;}
.st-key-quick_context_brief {border-left:3px solid #d89a59;padding:.4rem 1.3rem;background:#fffdf7;border-radius:0 20px 20px 0;}
.context-note {display:grid;grid-template-columns:1.8rem 1fr;gap:.7rem;margin:.9rem 0 .1rem;}
.context-note>span {font-size:.875rem;font-weight:800;color:#94633f;line-height:1.8;}.context-note h3 {font-size:1rem!important;line-height:1.6!important;margin:0!important;}
.priority-main {padding:1rem;border:1px solid #e6ddcf;border-radius:16px;background:#fffefa;}
.priority-label {display:inline-block;color:#593c2c;background:#fff0d8;padding:.3rem .65rem;border-radius:8px;font-size:.875rem;font-weight:700;}
.priority-main h3 {font-size:1.25rem!important;line-height:1.55!important;margin:.65rem 0!important;}
.priority-main p {margin:.5rem 0!important;}.priority-checks {padding-left:1.3rem;margin:.6rem 0 0;}
.priority-checks li {font-size:.94rem!important;}.priority-after {padding:.75rem 1rem;background:#f4f5eb;border-radius:12px;}
@media(max-width:760px) {[class*="_decision_desk"]{padding:1rem;border-radius:17px;}[class*="_decision_desk"] [role="radiogroup"]{grid-template-columns:repeat(2,minmax(0,1fr));}.desk-heading{font-size:1.25rem!important;}.st-key-quick_context_brief{padding:.6rem .9rem;}}
"""
