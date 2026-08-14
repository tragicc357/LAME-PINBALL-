from pathlib import Path
p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v42','LAME — Howie Lucas Pinball v43',1)

# Fix runtime freeze: never call sfxLaunch without a finite power value.
s=s.replace('function sfxLaunch(p){noise(.05,.04);tone(95+p*35,.2,"sawtooth",.065,650)}',
'''function sfxLaunch(p=.85){p=Number.isFinite(p)?p:.85;noise(.05,.04);tone(95+p*35,.2,"sawtooth",.065,650)}''',1)
s=s.replace('ball.vx=0;ball.vy=0;sfxLaunch();if(perfectLaunchPending',
            'ball.vx=0;ball.vy=0;sfxLaunch(.9);if(perfectLaunchPending',1)

# Replace rail geometry with a clearly visible loop attached to the top of the shooter lane.
old='''function launchRailPoint(t){const p=Math.max(0,Math.min(1,t));if(p<.38){const q=p/.38,a=Math.PI*.04-Math.PI*1.12*q;return{x:512+112*Math.cos(a),y:290+112*Math.sin(a)}}const q=(p-.38)/.62,u=1-q;return{x:u*u*405+2*u*q*315+q*q*205,y:u*u*188+2*u*q*120+q*q*235}}'''
new='''function launchRailPoint(t){const p=Math.max(0,Math.min(1,t));if(p<.58){const q=p/.58,a=.55-Math.PI*1.72*q;return{x:488+92*Math.cos(a),y:430+145*Math.sin(a)}}const q=(p-.58)/.42,u=1-q;return{x:u*u*410+2*u*q*325+q*q*235,y:u*u*312+2*u*q*245+q*q*225}}'''
if old not in s:
    raise SystemExit('launchRailPoint target not found')
s=s.replace(old,new,1)

# Enter the rail a little lower so the transition is visible and reliable.
s=s.replace('ball.vy<-3&&ball.y<325','ball.vy<-3&&ball.y<430',1)

# Make the rail visually stronger and label it near the shooter entrance.
s=s.replace('ctx.fillText("LOOP LAUNCH RAIL",410,105)', 'ctx.fillText("LOOP LAUNCH RAIL",420,255)',1)

# Keep camera following the rail animation smoothly rather than snapping to the top.
s=s.replace('cameraY=Math.max(0,Math.min(400,ball.y-430));',
            'cameraY+=(Math.max(0,Math.min(400,ball.y-430))-cameraY)*.28;',1)

# Safety checks.
if 'function sfxLaunch(p=.85)' not in s:
    raise SystemExit('safe sfxLaunch default missing')
if 'sfxLaunch();if(perfectLaunchPending' in s:
    raise SystemExit('unsafe rail sound call still present')
if 'ball.y<430' not in s:
    raise SystemExit('rail entry threshold missing')

p.write_text(s)
print('v43 patched: launch freeze fixed and visible launch loop rail installed')
