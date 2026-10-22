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
                          key=f"{prefix}_question",horizontal=True)
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
        st.caption('只填你知道的，其他不用補。依下列固定格式辨識，不會登入遊戲或自動讀取帳號。')
        text=st.text_input("目前配置（一行即可）",placeholder="維納托R6、塔洛莎R4、20個覺醒核心、雙生雷電1600",
                           max_chars=1000,key=f'{prefix}_snapshot_text')
        st.caption('可辨識：特工R級、核心／碎片庫存、雙絕槍E1V2、收藏黃3／紅1、幽暗黃4、普通／雙生諧振。不要貼帳密。')
        st.caption('找免費提升也可貼：典藏已開8格、持有紅收藏6件、已擺入紅收藏4件。紅收藏指原生傳奇品質，不是史詩紅星。')
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


def contextual_brief(p):
    import next_step as engine
    from direction_tools import operating_steps
    plan=engine.priority_brief(p)
    with st.container(key="quick_context_brief"):
        st.markdown('<div class="desk-eyebrow">依已填配置整理 · 不要求先報全部庫存</div><h2 class="desk-heading">目前可以先做什麼</h2>',unsafe_allow_html=True)
        first=plan['primary']
        if first:
            operation=operating_steps(first)
            unknown=[c['label'] for c in first.get('checks',[]) if c['state']=='unknown']
            action=('先存到下列需求；目前仍有已知缺額，這一步先不投入。' if first['status']=='先存資源' else
                    '先確認'+ '、'.join(unknown)+'；已填的數量不用重填。' if unknown else operation['steps'][0])
            checks=''.join(f'<li>{html.escape(c["label"])}：{html.escape(c["detail"])}</li>' for c in first.get('checks',[]) if c['state']!='ready')
            st.markdown(f'''<section class="priority-main" aria-label="本次第一步"><span class="priority-label">{html.escape(plan['label'])}</span>
                <h3>{html.escape(first['title'])}</h3><p>{html.escape(action)}</p>
                <p><b>本次停點：</b>{html.escape(first['target'])}</p>
                <ul class="priority-checks">{checks}</ul></section>''',unsafe_allow_html=True)
            if first.get('gap') and not checks:st.caption(first['gap'])
            st.caption(plan['reason'])
            if after:=plan['following']:
                st.markdown(f'<p class="priority-after"><b>這步做完再看</b>　{html.escape(after["title"])} · {html.escape(after["status"])}</p>',unsafe_allow_html=True)
            st.button('看這一步操作與材料',key='priority_open_details',on_click=open_details,width='stretch')
            if plan['queue']:
                with st.expander('後續候選 · 先不一起升'):
                    for item in plan['queue']:
                        st.write(f'{item["system"]} · {item["title"]}（{item["status"]}）')
            st.caption('不同資源分開存。尚未填的系統不等於低優先，這不是帳號總傷害效益排名。')
        elif hint:=plan['technology_hint']:
            st.markdown(f'''<section class="priority-main" aria-label="科技門檻候選"><span class="priority-label">先查最近的已收錄科技門檻</span>
                <h3>{html.escape(hint['name'])}：{hint['current']:,} → {hint['target']:,}</h3>
                <p><b>還差 {hint['gap']:,} 能量</b> · {html.escape(hint['effect'])}</p><p>{html.escape(hint['action'])}</p>
                <p><b>停手條件：</b>{html.escape(hint['stop'])}</p></section>''',unsafe_allow_html=True)
            st.caption('只按能量距離找候選，不代表最省材料或最高傷害；未核對的收藏與寵物仍須比較。')
            st.button('查這個諧振效果與調整方式',key='priority_tech_article',on_click=open_article,args=(hint['slug'],),width='stretch')
        else:
            st.write('還沒有可確認的單一步驟。先從下方已知配置找門檻，不必補齊整份帳號。')
        notes=quick.context_notes(p)
        with st.expander('依配置補充門檻',expanded=not bool(first or plan['technology_hint'])):
            for i,note in enumerate(notes,1):
                st.markdown(f'<div class="context-note"><span>{i:02d}</span><div><h3>{html.escape(note["title"])}</h3><p>{html.escape(note["body"])}</p></div></div>',unsafe_allow_html=True)
                st.button('查門檻與操作 →',key=f'context_read_{i}',on_click=open_article,args=(note['slug'],),type='tertiary')
            st.caption('以上為條件式候選，未代表已備齊材料。')


def open_details():
    st.session_state['route_details_revision']=st.session_state.get('route_details_revision',0)+1


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
