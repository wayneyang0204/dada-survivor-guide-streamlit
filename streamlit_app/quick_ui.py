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
            from field_tools import event_window
            window=event_window('2026-10-17T00:00:00+08:00','2026-10-22T00:00:00+08:00',source='community')
            st.caption(window['label']+'；本表為10月17日時光拼圖。')
            if window['state']=='ended':
                st.warning('本期已結束，以下僅作復刻核對，不依原期里程碑投入。')
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
    with st.container(key="quick_context_brief"):
        st.markdown('<div class="desk-eyebrow">依已填配置整理 · 不要求先報全部庫存</div><h2 class="desk-heading">目前可以先做什麼</h2>',unsafe_allow_html=True)
        notes=quick.context_notes(p)
        for i,note in enumerate(notes,1):
            st.markdown(f'<div class="context-note"><span>{i:02d}</span><div><h3>{html.escape(note["title"])}</h3><p>{html.escape(note["body"])}</p></div></div>',unsafe_allow_html=True)
            st.button('查門檻與操作 →',key=f'context_read_{i}',on_click=open_article,args=(note['slug'],),type='tertiary')
        st.caption('以上是條件符合的候選，不是已備齊材料或跨系統傷害排名。要計算庫存缺額再展開下方。')


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
@media(max-width:760px) {[class*="_decision_desk"]{padding:1rem;border-radius:17px;}[class*="_decision_desk"] [role="radiogroup"]{grid-template-columns:repeat(2,minmax(0,1fr));}.desk-heading{font-size:1.25rem!important;}.st-key-quick_context_brief{padding:.6rem .9rem;}}
"""
