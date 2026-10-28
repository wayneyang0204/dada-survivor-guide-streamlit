"""Small, explicit observations that expose existing upgrade routes.

No inventory defaults, inferred levels, or new damage rankings. A skipped
question is session-only and remains unknown in the saved profile.
"""
from __future__ import annotations

import hashlib
import json
import next_step as engine


def questions(raw: dict) -> list[dict]:
    p = engine.clean_profile(raw)
    if p['mode'] == '新版區域行動' or p['growth_focus'] == '生存不足':
        return []
    result = []

    def add(key, title, why, entry, options, dependencies=()):
        scope = {k: p[k] for k in dependencies}
        token = hashlib.sha256(json.dumps([key, scope], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
        result.append(dict(id=key, title=title, why=why, entry=entry, options=options, token=token))

    if engine.hall_fill_state(p) is None:
        add('hall', '典藏館有空槽，而且有紅收藏能放進去嗎？',
            '有的話先放進去，這一步不用買材料，也不用先算收藏數量。',
            '收藏館 → 自訂收藏館；紅收藏指原生傳奇品質。',
            [('有，手上就能放', {'hall_can_fill': True}), ('沒有可直接放的', {'hall_can_fill': False})],
            ('slots', 'red_owned', 'red_placed'))
    if p['weapon'] is None:
        add('weapon', '目前用雙絕槍嗎？', '先查主武器有沒有漏掉 E1；不用填六件裝備。',
            '裝備 → 目前主武器', [('用雙絕槍', {'weapon': '雙絕槍'}), ('用其他武器', {'weapon': '其他'})])
    elif p['weapon'] == '雙絕槍' and p['weapon_e'] is None:
        add('weapon_e', '雙絕槍的永恆神鑄是幾階？', 'E0 才列入補 E1；已有的階級不會叫你重升。',
            '雙絕槍 → 神鑄 → 永恆；未神鑄選 E0。',
            [(f'E{n}', {'weapon_e': n}) for n in range(6)], ('weapon',))
    if p['twin_drone'] is None or p['twin_drone'] is False and p['drone_red'] is None:
        add('drone', '無人機配件目前是哪一種？', '這會決定先補雙生、塔洛莎協同，還是比較暗物質傀儡。',
            '科技配件 → 無人機配件',
            [('雙生無人機', {'twin_drone': True, 'drone_form': '雙生'}),
             ('普通紅無人機', {'twin_drone': False, 'drone_red': True, 'drone_form': '普通'}),
             ('普通，還沒紅', {'twin_drone': False, 'drone_red': False, 'drone_form': '普通'})])
    if p['twin_drone'] or p['drone_red']:
        if p['survivor'] == '維納托' and p['taloxa'] is None:
            add('taloxa', '塔洛莎目前覺醒幾階？', '協同還沒到 R4 時，會和主位下一階一起比較。',
                '特工 → 塔洛莎 → 覺醒；未覺醒選 R0。',
                [(f'R{n}', {'taloxa': n}) for n in range(9)], ('survivor', 'twin_drone', 'drone_red'))
        if p['dark_matter'] is None:
            add('dark_matter', '暗物質傀儡現在幾星？', '直接找下一個已收錄的無人機增傷節點，先不用填箱數。',
                '收藏館 → 暗物質傀儡',
                [(engine.STARS[n], {'dark_matter': n}) for n in range(11)], ('twin_drone', 'drone_red'))
    if p['pet_kind'] is None or p['pet_kind'] == '異世寵物' and p['pet_name'] is None:
        add('pet', '目前帶哪一類主戰寵？', '幽暗之靈只需選星級，就能帶出已收錄的節點與效果。',
            '寵物 → 目前出戰寵物',
            [('幽暗之靈', {'pet_kind': '異世寵物', 'pet_name': '幽暗之靈'}),
             ('其他異世寵物', {'pet_kind': '異世寵物', 'pet_name': '其他'}),
             ('普通輸出寵', {'pet_kind': '普通輸出寵', 'pet_name': '其他'}),
             ('主人增益寵', {'pet_kind': '主人增益寵', 'pet_name': '其他'}),
             ('還沒有主戰寵', {'pet_kind': '未持有', 'pet_name': None})])
    if p['pet_kind'] not in (None, '未持有'):
        if p['pet_skills_ready'] is None:
            add('pet_skills', '出戰、助戰技能已核對並裝好了嗎？', '先排除技能沒裝入的情況，再比較花材料的覺醒。',
                '寵物 → 主戰與助戰技能槽',
                [('已核對並裝好', {'pet_skills_ready': True}), ('還沒核對', {'pet_skills_ready': False})],
                ('pet_kind', 'pet_name'))
        if p['pet_kind'] == '異世寵物' and p['pet_name'] == '幽暗之靈' and p['pet_star'] is None:
            add('pet_star', '幽暗之靈目前覺醒幾星？', '黃4以前查黃4節點；已達黃4再比較紅5，不會直接叫你追滿。',
                '寵物 → 幽暗之靈 → 覺醒',
                [('尚未覺醒' if n == 0 else engine.STARS[n], {'pet_star': n}) for n in range(11)],
                ('pet_kind', 'pet_name'))
    if p['neck'] is None:
        add('neck', '目前用破壞者徽記嗎？', '仍用徽記才比較它對應的記憶編輯器節點。',
            '裝備 → 項鍊', [('用破壞者徽記', {'neck': '破壞者徽記'}), ('用其他項鍊', {'neck': '其他'})])
    elif p['neck'] == '破壞者徽記' and p['memory'] is None:
        add('memory', '記憶編輯器現在幾星？', '依現有星級找下一個效果門檻；暴率是否仍有收益會另外核對。',
            '收藏館 → 記憶編輯器', [(engine.STARS[n], {'memory': n}) for n in range(11)], ('neck',))
    return result


def answer_values(raw: dict, question_id: str, option: str) -> dict:
    """Accept only an answer to a currently applicable question."""
    p = engine.clean_profile(raw)
    question = next((q for q in questions(p) if q['id'] == question_id), None)
    if not question:
        raise ValueError('這項現況已經改變，請查看目前問題。')
    values = next((dict(v) for label, v in question['options'] if label == option), None)
    if values is None:
        raise ValueError('請選擇畫面上的現況。')
    if question_id == 'weapon' and values['weapon'] != p['weapon']:
        values.update(weapon_e=None, weapon_v=None, gear_materials_ready=None)
    if question_id == 'weapon_e':
        values['gear_materials_ready'] = None
    if question_id == 'drone' and values['drone_form'] != p['drone_form']:
        values['drone_energy'] = None
    if question_id == 'pet':
        values.update(pet_star=None, pet_target=None, pet_gain=None, pet_skills_ready=None,
                      pet_preview_matches=None, pet_materials_ready=None)
    return values


def remaining(raw: dict, skipped: dict) -> list[dict]:
    return [q for q in questions(raw) if skipped.get(q['id']) != q['token']]


def context_labels(raw: dict) -> list[str]:
    """Observed systems, not a claim that every route in a system is covered."""
    p = engine.clean_profile(raw)
    items = []
    if p['survivor'] is not None and p['awakening'] is not None: items.append('角色')
    if p['weapon'] is not None: items.append('武器')
    if p['twin_drone'] is not None: items.append('無人機')
    if p['dark_matter'] is not None or p['memory'] is not None: items.append('收藏品')
    if p['pet_kind'] is not None: items.append('寵物')
    if p['hall_can_fill'] is not None or all(p[k] is not None for k in ('slots','red_owned','red_placed')): items.append('典藏空槽')
    return items
