"""Dated event phases. A card's display window is not proof of a game opening."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def event_phase(model: dict, now: datetime | None = None) -> dict:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() is None:
        raise ValueError("目前時間必須含時區。")
    if not model.get('starts_at') or not model.get('ends_at'):
        return {'state':'unknown','label':'時段待核對','action':'先看遊戲內倒數與本期獎勵表，不沿用歷史數字。','can_spend':False}
    start,end = (datetime.fromisoformat(model[k]) for k in ('starts_at','ends_at'))
    exchange = datetime.fromisoformat(model['exchange_ends_at']) if model.get('exchange_ends_at') else end
    if any(t.tzinfo is None or t.utcoffset() is None for t in (start,end,exchange)) or not start < end <= exchange:
        raise ValueError("活動與兌換截止需含時區，且順序正確。")
    basis = '官方活動卡' if model.get('schedule_source','official')=='official' else '社群表列'
    def stamp(t):return t.astimezone(ZoneInfo('Asia/Taipei')).strftime('%m/%d %H:%M')
    common={'basis':basis,'starts':stamp(start),'ends':stamp(end),'exchange_ends':stamp(exchange)}
    if current < start:
        return {**common,'state':'upcoming','label':'尚未開始','action':f'{basis}預告 {stamp(start)} 起；先保留鑰匙與寶石，開放後再核對遊戲。','can_spend':False}
    if current < end:
        return {**common,'state':'active','label':'活動時段內','action':f'{basis}至 {stamp(end)}；仍以遊戲入口與倒數為準。','can_spend':True}
    if current < exchange:
        return {**common,'state':'exchange','label':'僅剩兌換','action':f'{basis}兌換至 {stamp(exchange)}；只整理已持有代幣，不再補鑽追里程碑。','can_spend':False}
    return {**common,'state':'ended','label':'原期已結束','action':'只供歷史或復刻核對，不再依原期里程碑投入。','can_spend':False}


def preferred_event(models: list[dict], now: datetime | None = None) -> int | None:
    if not models:return None
    score={'active':4,'exchange':3,'upcoming':2,'unknown':1,'ended':0}
    def rank(i):
        phase=event_phase(models[i],now)['state']
        start=datetime.fromisoformat(models[i]['starts_at']).timestamp() if models[i].get('starts_at') else 0
        return score[phase], -start if phase=='upcoming' else start
    return max(range(len(models)),key=rank)


def current_playbook(models: list[dict], now: datetime | None = None) -> dict:
    """Short actions for today's phase; archived spending tips never leak here."""
    dated=[m for m in models if m.get('guide_slug') and event_phase(m,now)['state'] in ('active','exchange','upcoming')]
    if not dated:
        return {'title':'近期活動待核對，先不補鑽','steps':(('先核對名稱與倒數','本站沒有已核對、仍在活動期的本期表；不要把舊活動獎勵當作現行內容。'),
            ('再領確定可領項','只領遊戲內已完成的任務，開箱成本與隨機返還分開記。'),('有明確目標才試算','獎勵、期限與票價都對上本期後，再算剩餘差額。')),
            'stop':'沒有本期資料時先保留寶石與鑰匙。','guides':('event-budget','daily-resource-ledger'),'state':'unknown','label':'待核對','action':'不把歷史活動列為現行投入建議。'}
    model=dated[preferred_event(dated,now)]; phase=event_phase(model,now)
    if phase['state']=='exchange':
        steps=(('先看剩餘代幣','打開本期商店，確認尚未花掉的代幣與未領的兌換獎勵。'),
               ('只換已知缺口','先補現役配置的完整門檻；已滿星的復刻收藏不要重複換。'),
               ('到期前領完','核對遊戲內商店倒數並領取；遊玩期已結束，不補鑽、不再開箱追里程碑。'))
        title=model['name']+'：現在只處理兌換'; stop='只用已有代幣；兌換截止後停止沿用本期商店。'
    elif phase['state']=='upcoming':
        steps=(('先保留資源','現在不為尚未開始的活動開箱或花寶石。'),('開放後先領免費項目','對照本期任務、累計獎勵與商店；官方活動卡沒有公開的數值不預填。'),
               ('再選需要的里程碑','把獎勵對應到目前缺口；沒有完整任務與價格表，不估固定免費量或必需鑽數。'))
        title=model['name']+'：開放前先留鑰匙';stop='看到遊戲本期介面與價格後，才決定是否投入。'
    else:
        steps=tuple((f'第{i}步',text) for i,text in enumerate(model['steps'][:3],1))
        title=model['name']+'：先領任務，再看停點';stop=model['avoid']
    return {**phase,'title':title,'steps':steps,'stop':stop,'guides':(model['guide_slug'],'event-budget','daily-resource-ledger')}
