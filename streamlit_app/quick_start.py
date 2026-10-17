"""Explicit-text intake and source-based recipes, without inferred inventory."""
from __future__ import annotations

import re
import unicodedata

SS_SOURCE = "https://notalknote.xyz/【噠噠特攻】神鑄消耗/"
SS_ROWS = ((1,1,1,10,500), (2,1,2,20,500), (3,2,3,40,500), (4,2,5,60,500), (5,1,8,80,1000))


def ss_recipe(current: int, target: int) -> dict:
    """A single E/V path. Equipment quality and other-path prerequisites remain explicit."""
    if type(current) is not int or type(target) is not int or not 0 <= current < target <= 5:
        raise ValueError("神鑄需為0～5，目標必須高於目前。")
    rows = [row for row in SS_ROWS if current < row[0] <= target]
    return {"cores":sum(r[2] for r in rows), "stones":sum(r[3] for r in rows),
            "base":sum(r[4] for r in rows), "epic":sum(r[1] for r in rows if r[0] < 5),
            "legendary":sum(r[1] for r in rows if r[0] == 5),
            "other_path_min":3 if target >= 4 else None, "source":SS_SOURCE}


HERO_ALIASES = {"維納托":"維納托", "維托爾":"維納托", "塔洛莎":"塔洛莎", "塔洛西婭":"塔洛莎",
                "楊大師":"楊大師", "金":"金"}
LABELS = {"survivor":"主位", "awakening":"主位覺醒", "taloxa":"塔洛莎覺醒", "yang":"楊大師覺醒", "king":"金覺醒",
          "awakening_cores":"覺醒核心", "s_shards":"主位S碎片", "relic_cores":"神器核心", "red_boxes":"傳奇收藏自選箱",
          "hearts":"收藏之心", "advanced_hearts":"高級收藏之心", "weapon":"武器", "weapon_e":"永恆神鑄 E",
          "weapon_v":"虛空神鑄 V", "memory":"記憶編輯器", "dark_matter":"暗物質傀儡",
          "pet_kind":"寵物類型", "pet_name":"主戰寵物", "pet_star":"寵物覺醒", "mode":"模式",
          "drone_energy":"無人機諧振", "lightning_energy":"雷電諧振", "drone_form":"無人機形態", "lightning_form":"雷電形態",
          "neck":"項鍊", "ss_boots":"SS鞋", "twin_drone":"雙生無人機", "drone_red":"紅無人機"}


def parse_snapshot(text: str) -> dict:
    """Recognise a small explicit grammar; never treat a goal, question or blank as ownership."""
    if not isinstance(text,str) or len(text)>1000:
        raise ValueError("現況最多1000字。")
    value = unicodedata.normalize('NFKC',text).strip()
    number = r'[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
    def numeric(raw):
        return float(raw.replace(',',''))
    if re.search(r'密碼|password|cookie|token|api.?key|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',value,re.I):
        return {"fields":{},"errors":["請移除帳密、信箱或金鑰；這裡只需要遊戲配置。"],"unmatched":[],"notes":[]}
    fields, errors, notes, spans = {}, [], [], []
    def put(key, val):
        if key in fields and fields[key] != val:
            errors.append(f"{LABELS.get(key,key)}有兩個不同數值，請只留目前狀態。")
        else:
            fields[key] = val
    def accept(match):
        spans.append(match.span())
    if re.search(r'→|->|打算|準備|想升|想要|升到|要升|目標|預計|計畫|\?',value):
        return {"fields":{},"errors":["請只貼目前配置，不貼升級目標或問句，例如「維納托R6、塔洛莎R4」。"],"unmatched":[],"notes":[]}
    if re.search(r'沒有|沒|未持有|不是|不使用|不用|尚未|不確定|可能|好像|未解鎖|缺|還差',value):
        return {"fields":{},"errors":["這行包含否定或不確定敘述，先不套用。請只列已確認的現況；沒有的項目可省略，庫存為零請填0。"],"unmatched":[],"notes":[]}
    if re.search(r'\d(?:\.\d+)?[eE][+-]?\d',value):
        return {"fields":{},"errors":["數量請寫一般整數，不使用科學記號。"],"unmatched":[],"notes":[]}
    heroes=[]; hero_levels={}
    hero_pattern='|'.join(sorted(HERO_ALIASES,key=len,reverse=True))
    for m in re.finditer(rf'(?P<main>主位\s*[:：]?\s*)?(?P<hero>{hero_pattern})\s*(?:R|覺醒)\s*(?P<n>[+-]?\d+(?:\.\d+)?)\s*(?:星)?',value,re.I):
        n=float(m['n'])
        if not n.is_integer() or not 0<=n<=8:
            errors.append('特工覺醒請填R0～R8整數。');continue
        hero=HERO_ALIASES[m['hero']];n=int(n)
        if hero in hero_levels and hero_levels[hero] != n:
            errors.append(hero+'有兩個不同覺醒等級，請只留目前狀態。')
        hero_levels[hero]=n
        heroes.append((hero,n,bool(m['main'])))
        if hero in ('塔洛莎','楊大師','金'):
            put({'塔洛莎':'taloxa','楊大師':'yang','金':'king'}[hero],n)
        accept(m)
    if heroes:
        explicit=[h for h in heroes if h[2]]
        chosen=explicit[0] if explicit else heroes[0]
        if len({(h[0],h[1]) for h in explicit})>1:
            errors.append('只能指定一位主位特工。')
        put('survivor',chosen[0]);put('awakening',chosen[1])
        if len(heroes)>1 and not explicit:
            notes.append('第一位角色暫列主位；若不是，請在該角色前加「主位」。')
    stocks = (('覺醒核心','awakening_cores',10000),('神器核心','relic_cores',10000),
              ('(?:主位)?S(?:特工)?碎片','s_shards',100000),('(?:傳奇|紅色)收藏自選箱','red_boxes',10000),
              ('高級收藏之心','advanced_hearts',100000),('收藏之心','hearts',10000000))
    for term,key,maximum in stocks:
        patterns=(rf'(?:^|[\s,，、;；])(?P<label>{term})\s*[:：=]?\s*(?P<n>{number})\s*(?:個|顆|箱)?',
                  rf'(?:^|[\s,，、;；])(?P<n>{number})\s*(?:個|顆|箱)\s*(?P<label>{term})')
        for m in (m for pattern in patterns for m in re.finditer(pattern,value,re.I)):
            n=numeric(m['n'])
            if not n.is_integer() or not 0<=n<=maximum:
                errors.append(f'{LABELS[key]}數量超出範圍或不是整數。');continue
            put(key,int(n));accept(m)
    for m in re.finditer(r'(?:雙絕槍|雙生槍)\s*E\s*([+-]?\d+(?:\.\d+)?)\s*[/／,，、 ]*V\s*([+-]?\d+(?:\.\d+)?)',value,re.I):
        e,v=map(float,m.groups())
        if not e.is_integer() or not v.is_integer() or not 0<=e<=5 or not 0<=v<=5:
            errors.append('雙絕槍E/V請填0～5。');continue
        put('weapon','雙絕槍');put('weapon_e',int(e));put('weapon_v',int(v));accept(m)
    for m in re.finditer(r'(記憶編輯器|暗物質[傀魁]儡|幽暗之靈|幽暗)\s*(?:覺醒)?\s*([黃金紅YR])\s*([+-]?\d+(?:\.\d+)?)',value,re.I):
        name,colour,n=m.groups();n=float(n)
        if not n.is_integer() or not 1<=n<=5:
            errors.append('收藏或寵物星級請填黃1～黃5／紅1～紅5。');continue
        n=int(n)
        star=n+(5 if colour.upper() in ('紅','R') else 0)
        if name.startswith('幽暗'):
            put('pet_kind','異世寵物');put('pet_name','幽暗之靈');put('pet_star',star)
        else:
            put('memory' if name=='記憶編輯器' else 'dark_matter',star)
        accept(m)
    for m in re.finditer(rf'(?P<form>雙生|普通)?(?P<part>無人機|雷電)\s*(?:諧振|能量)?\s*[:：=]?\s*(?P<n>{number})',value):
        n=numeric(m['n']);prefix='drone' if m['part']=='無人機' else 'lightning'
        if not n.is_integer() or not 0<=n<=1000000:
            errors.append('諧振能量請填0～1000000整數。');continue
        put(prefix+'_energy',int(n))
        if m['form']:
            put(prefix+'_form',m['form'])
            if prefix=='drone':put('twin_drone',m['form']=='雙生')
        else:
            notes.append(m['part']+'未註明普通／雙生，先不套用雙生效果。')
        accept(m)
    for term,key,val in (('破壞者徽記','neck','破壞者徽記'),('SS鞋','ss_boots',True),('紅無人機','drone_red',True)):
        for m in re.finditer(rf'(?:^|[\s,，、;；])(?:穿|使用|有)?{term}(?=$|[\s,，、;；])',value,re.I):
            put(key,val);accept(m)
    for term,mode in (('末世迴響','末世迴響'),('末世','末世迴響'),('月礦','遠征／月礦首領'),
                      ('遠征','遠征／月礦首領'),('主線','主線推關'),('區域行動','新版區域行動')):
        for m in re.finditer(term,value):put('mode',mode);accept(m)
    remaining=list(value)
    for start,end in spans:remaining[start:end]=' '*(end-start)
    unmatched=[s.strip() for s in re.split(r'[\n,，、;；]+',''.join(remaining)) if s.strip()]
    if any(re.fullmatch(r'[+-]?\d+(?:\.\d+)?',s) for s in unmatched):
        errors.append('有數字沒有對應到物品，先不套用。請將物品名稱和數量寫在一起。')
    return {"fields":fields,"errors":list(dict.fromkeys(errors)),"unmatched":unmatched,
            "notes":list(dict.fromkeys(notes))}


def field_value(key, value):
    if key in ('awakening','taloxa','yang','king'):return f'R{value}'
    if key in ('memory','dark_matter','pet_star'):return ('黃' if value<=5 else '紅')+str(value if value<=5 else value-5)
    return '是' if value is True else '否' if value is False else str(value)


def apply_fields(before: dict, fields: dict) -> dict:
    """Retargeted upgrades must not inherit another target's confirmations."""
    updates=dict(fields)
    if 'survivor' in fields and before.get('survivor') and fields['survivor']!=before['survivor']:
        for key in ('s_shards','quantum_ready','awakening_goal'):
            if key not in fields:updates[key]=None
    if 'awakening' in fields and fields['awakening']!=before.get('awakening'):
        updates['quantum_ready']=None
    if any(k in fields and fields[k]!=before.get(k) for k in ('weapon','weapon_e','weapon_v')):
        updates['gear_materials_ready']=None
    return updates


PLAYBOOKS = {
 '角色升完，接著升什麼': {
  'title':'先把角色資源停住，找收藏、寵物和科技的近端門檻',
  'steps':(('先做，不花新材料','填滿已開的典藏空槽，裝好已解鎖連攜／助戰；先取得已持有配置的效果。'),
           ('再比，分開材料池','有幽暗之靈但未黃4：列黃4易傷候選；已黃4就別直接假設要衝紅5。同時看主力收藏下一個技能星級。'),
           ('最後才加碼','雙生雷電1600可先查1650（差50）；不要為此拆掉無人機3000。只有有用的完整門檻才投入。')),
  'stop':'角色、寵物、收藏和科技不是同一種貨幣，不強行排一條通用付費榜。先完成已持有的免費調整，再按距離與材料比較。',
  'guides':('upgrade-roadmap','umbral-soul','twin-tech-milestones','collectible-breakpoints')},
 '紅色自選箱怎麼選': {
  'title':'先辨認箱種，再選能一次啟動的效果',
  'steps':(('收藏自選','仍穿破壞者徽記才補記憶編輯器的專屬暴率；用無人機才比較暗物質傀儡黃3／黃5。'),
           ('科技／諧振自選','雷電要看普通還是雙生；雙生雷電1600→1650是差50的候選，無人機3000不是所有形態的通用上限。'),
           ('套裝差一件','SS鞋冰甲已開時，比四件黃3整組缺口；別把一件升好當作套裝已啟動。')),
  'stop':'不同箱種、期數與每箱碎片量不能混算。沒有需要的完整節點，就先不開箱。',
  'guides':('red-choice-box','collectible-sets','epic-collectibles','twin-tech-milestones')},
 '維納托R6／連攜怎麼排': {
  'title':'維納托R6後，先分清塔洛莎裂傷和主位R7',
  'steps':(('塔洛莎未R4且主力是無人機','下一個連攜門檻是塔洛莎R4的無人機裂傷；要真的放入連攜槽。'),
           ('塔洛莎已R4','主位R7列30覺醒核心＋550角色碎片，量子另計。只有20核心時，核心差10，不用自己填需求。'),
           ('楊大師／金','楊大師R1武魂列暴率與暴傷各5%；金R3是主動無敵期間回復，不能直接當成同一種常駐連攜收益。')),
  'stop':'R7後再比較其他系統，不因核心到30就省略550碎片與量子，也不自動重置金或楊大師。',
  'guides':('survivor-awakening','link-passives','synergy-vs-link')},
 'SS裝備需要多少材料': {
  'title':'E／V材料可以直接查，不必自己合計',
  'steps':(('單路線核心','0→1要1、0→2要3、0→3要6、0→4要11、0→5要19顆神器核心。'),
           ('核心以外','各階另有材料裝備、陣營之石與基礎科技素材；完整表與區間試算已收錄。'),
           ('高階前置','來源表列升E4前要V3、升V4前要E3；混沌與異星不套用E／V的19核心累計。')),
  'stop':'先選有用的技能，再查這一段材料；不是核心夠就一定能按升級。',
  'guides':('ss-material-recipes','lance-starforge','ss-glove-crit','ss-boots-check')},
 '寵物怎麼養': {
  'title':'先把現有寵物技能放對，再決定追哪一階',
  'steps':(('普通輸出寵','主戰技能服務寵物自身輸出，助戰按寵物種類搭配；普通覺醒不等於異世覺醒。'),
           ('幽暗之靈未黃4','黃4是本表收錄的60%易傷20秒門檻；先比這一段，不直接追滿紅5。'),
           ('幽暗黃4以後／伊狑','紅5是遠端候選而非立即必追；伊狑R5第二寵技能仍上限紅1，R8才到紅5。')),
  'stop':'沒有使用的寵物不平均投。未測量主人輸出前，寵物面板提升不等於帳號總傷害提升。',
  'guides':('ordinary-pet-skills','umbral-soul','elaine-build','xeno-assist')},
 '現在活動怎麼做': {
  'title':'時光拼圖：先拿確定里程碑，隨機核心別當保底',
  'steps':(('日常操作','長按自動移動；右上道具箱可中途領影集，不必等一整張完成。'),
           ('先看目標','10月17日社群表列700影集S裝、850神器核心自選、1000動態頭像；以遊戲本期獎勵表對照。'),
           ('最後一天再補差額','開300箱任務有鑰匙成本；約30%返還是估計，拼圖隨機核心不構成第二顆保底。')),
  'stop':'已拿需要的里程碑就停；不為猜測1000～1200會出核心而強補鑽。',
  'guides':('time-jigsaw','event-budget','matrix-squad-preview')},
}


def context_notes(p: dict) -> list[dict]:
    """Concrete candidates from supplied facts, not a claim of affordability or global ROI."""
    notes=[]
    if all(p.get(k) is not None for k in ('slots','red_owned','red_placed')) and min(p['slots'],p['red_owned'])>p['red_placed']:
        free=min(p['slots'],p['red_owned'])-p['red_placed']
        notes.append({'title':f'先放入已有紅收藏：還可補{free}個槽','body':'這一步不開新槽、不升星，先用已持有收藏填滿可用空槽，再花新材料。','slug':'collection-hall'})
    if p.get('yang') is not None and p['yang']>=1 and p.get('survivor')!='楊大師':
        notes.append({'title':'先用已解鎖的楊大師武魂','body':'有已解鎖連攜空位時，先核對並裝入武魂；R1表列暴率與暴傷各5%。這是現有配置調整，不要求重置金或繼續投核心。','slug':'link-passives'})
    if p.get('taloxa') is not None and p['taloxa']>=4 and (p.get('twin_drone') or p.get('drone_red')):
        notes.append({'title':'塔洛莎R4已達：先確認裂傷連攜裝入','body':'無人機命中才會觸發這個裂傷候選；已有R4就先把現有連攜用上，不為看見R6／R8而直接追加。','slug':'link-passives'})
    paused=p.get('awakening_goal') is not None and p.get('awakening') is not None and p['awakening']>=p['awakening_goal']
    if paused:
        notes.append({'title':f'角色停在R{p["awakening"]}，先比較其他系統','body':'已依你的階段目標暫停追加主位核心；收藏、寵物、科技材料分開存，協同仍獨立比較。','slug':'upgrade-roadmap'})
    if not paused and p.get('survivor')=='維納托' and p.get('awakening') in (6,7):
        target=p['awakening']+1;shards=550 if target==7 else 600
        gaps=[]
        for label,key,need in (('核心','awakening_cores',30),('碎片','s_shards',shards)):
            if p.get(key) is not None:gaps.append(f'{label}差{max(0,need-p[key])}')
        notes.append({'title':f'主位下一階：維納托R{target}', 'body':f'30覺醒核心＋{shards}角色碎片，量子另計。'+('；'.join(gaps)+'。' if gaps else '不必手填這一階需求。'), 'slug':'survivor-awakening'})
    if p.get('taloxa') is not None and p['taloxa']<4:
        notes.append({'title':'無人機主力才補塔洛莎R4','body':f'目前R{p["taloxa"]}，下一個收錄的無人機裂傷門檻是R4；主力不是無人機時不直接排第一。','slug':'link-passives'})
    if p.get('weapon')=='雙絕槍' and p.get('weapon_e')==0:
        r=ss_recipe(0,1)
        notes.append({'title':'雙絕槍永恆0→1：完整材料已列','body':f'{r["cores"]}神器核心、{r["epic"]}件史詩材料裝備、{r["stones"]}永恆之石、{r["base"]}基礎科技素材。','slug':'ss-material-recipes'})
    if p.get('dark_matter') is not None and p['dark_matter']<5 and (p.get('drone_red') or p.get('twin_drone')):
        target='黃3' if p['dark_matter']<3 else '黃5'
        notes.append({'title':'無人機收藏候選：暗物質傀儡'+target,'body':'先把這一個技能星級補完整，不平均升所有收藏；自選箱期數與整段碎片缺額另核對。','slug':'collectible-breakpoints'})
    if p.get('pet_name')=='幽暗之靈' and p.get('pet_star') is not None and p['pet_star']>0:
        star=p['pet_star'];target='黃4' if star<4 else '紅5'
        notes.append({'title':'幽暗之靈：'+('已到本表最高節點' if star==10 else '下一個收錄節點'+target),
          'body':'黃4易傷門檻已知；紅5不是立即必追。先保留目前配置，比較整段成本與主人輸出。' if star>=4 else '先比較黃4的60%易傷20秒；不要求你手打技能名稱或下一階效果。','slug':'umbral-soul'})
    for prefix,part in (('drone','無人機'),('lightning','雷電')):
        if p.get(prefix+'_energy') is not None:
            if p.get(prefix+'_form')!='雙生':
                notes.append({'title':part+'形態尚未確認','body':'能量已記下；加上「普通」或「雙生」即可辨識，不把普通門檻套成雙生。','slug':'twin-tech-milestones'})
            else:
                from tech_routes import next_tech_effect
                result=next_tech_effect('雙生無人機（無人機態）' if prefix=='drone' else '雙生雷電（雷電態）',p[prefix+'_energy'])
                notes.append({'title':part+'諧振下一檔','body':result['message']+' '+result.get('effect',''),'slug':'twin-tech-milestones'})
    if not notes:
        notes.append({'title':'先做已持有的免費調整','body':'填滿已開典藏槽、裝滿已解鎖連攜與助戰；再從下方問題選擇要投入的系統，不需要先填全部庫存。','slug':'upgrade-roadmap'})
    return notes
