from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v56','LAME — Howie Lucas Pinball v58',1)
old='async function api(method,body){const o={method,headers:{"Authorization":"Bearer "+GAME_ANON_KEY,"apikey":GAME_ANON_KEY,"Content-Type":"application/json"}};if(body)o.body=JSON.stringify(body);const r=await fetch(GAME_API,o);if(!r.ok)throw new Error(r.status);return r.json()}'
new='async function api(method,body){const base="https://bhpnhrikaunimummtyxt.supabase.co/rest/v1/rpc/";const h={"Authorization":"Bearer "+GAME_ANON_KEY,"apikey":GAME_ANON_KEY,"Content-Type":"application/json"};let fn,args={};if(method==="GET"){fn="lame_game_get_stats"}else if(body?.action==="start"){fn="lame_game_record_start";args={p_player_id:String(body.playerId||"")}}else if(body?.action==="finish"){fn="lame_game_record_finish";args={p_player_id:String(body.playerId||""),p_player_name:String(body.playerName||""),p_score:Math.floor(Number(body.score)||0),p_howie_out_ms:Math.floor(Number(body.howieOutMs)||0)}}else throw new Error("unknown api action");const r=await fetch(base+fn,{method:"POST",headers:h,body:JSON.stringify(args)});if(!r.ok)throw new Error(r.status+" "+await r.text());return r.json()}'
if old not in s: raise SystemExit('old api function not found')
s=s.replace(old,new,1)
for token in ['LAME — Howie Lucas Pinball v58','lame_game_get_stats','lame_game_record_start','lame_game_record_finish']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
