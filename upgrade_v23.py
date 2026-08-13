from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v23</title>',s,count=1)

# Add richer contact sounds plus a continuous breakout siren.
anchor='function sfxGameOver(){tone(330,.14,"triangle",.045,-70,.25);tone(247,.16,"triangle",.045,-55,.40);tone(165,.3,"triangle",.05,-50,.57)}'
extra=r'''function sfxGameOver(){tone(330,.14,"triangle",.045,-70,.25);tone(247,.16,"triangle",.045,-55,.40);tone(165,.3,"triangle",.05,-50,.57)}
let lastContactSfx=0;function sfxContact(kind="wall",strength=1){if(!audioCtx)return;const now=performance.now();if(now-lastContactSfx<22)return;lastContactSfx=now;const v=Math.min(.05,.018+strength*.012);if(kind==="metal"){noise(.025,v*.75);tone(820,.035,"triangle",v,160)}else if(kind==="target"){tone(680,.045,"square",v,170);tone(930,.035,"sine",v*.6,80,.025)}else if(kind==="floor"){noise(.03,v);tone(145,.04,"triangle",v*.7,-25)}else{noise(.018,v*.65);tone(260+Math.random()*90,.035,"triangle",v,55)}}
let sirenNodes=null;function startHowieSiren(){if(!audioCtx||sirenNodes)return;const t=audioCtx.currentTime,o=audioCtx.createOscillator(),g=audioCtx.createGain(),lfo=audioCtx.createOscillator(),lfoGain=audioCtx.createGain();o.type="sawtooth";o.frequency.setValueAtTime(620,t);lfo.type="sine";lfo.frequency.setValueAtTime(1.7,t);lfoGain.gain.setValueAtTime(260,t);lfo.connect(lfoGain).connect(o.frequency);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.035,t+.12);o.connect(g).connect(audioCtx.destination);o.start(t);lfo.start(t);sirenNodes={o,g,lfo,lfoGain}}
function stopHowieSiren(){if(!sirenNodes||!audioCtx)return;const n=sirenNodes;sirenNodes=null;const t=audioCtx.currentTime;try{n.g.gain.cancelScheduledValues(t);n.g.gain.setValueAtTime(Math.max(.0001,n.g.gain.value),t);n.g.gain.exponentialRampToValueAtTime(.0001,t+.12);n.o.stop(t+.14);n.lfo.stop(t+.14)}catch(e){}}
function sfxSuperLaunch(p=.5){noise(.07,.055);tone(90+Math.round(p*35),.24,"sawtooth",.075,760,.01);tone(420,.10,"square",.035,260,.08)}'''
if anchor not in s: raise SystemExit('audio anchor not found')
s=s.replace(anchor,extra,1)

# Stronger launch effect replaces the lighter v22 launch call.
s=s.replace('sfxLaunch(power);','sfxSuperLaunch(power);',1)

# Sound every actual segment/rail collision.
s=s.replace('if(dot<0){ball.vx=(ball.vx-2*dot*nx)*boost;ball.vy=(ball.vy-2*dot*ny)*boost-kick;if(pts)addScore(pts,px,py)}',
'''if(dot<0){ball.vx=(ball.vx-2*dot*nx)*boost;ball.vy=(ball.vy-2*dot*ny)*boost-kick;sfxContact("metal",Math.min(2,Math.abs(dot)/5));if(pts)addScore(pts,px,py)}''',1)

# Outer playfield wall collision sounds.
s=s.replace('if(ball.x<24){ball.x=24;ball.vx=Math.abs(ball.vx)*0.92}',
'''if(ball.x<24){ball.x=24;ball.vx=Math.abs(ball.vx)*0.92;sfxContact("wall",Math.abs(ball.vx)/6)}''',1)
s=s.replace('if(ball.x>576){ball.x=576;ball.vx=-Math.abs(ball.vx)*0.92}',
'''if(ball.x>576){ball.x=576;ball.vx=-Math.abs(ball.vx)*0.92;sfxContact("wall",Math.abs(ball.vx)/6)}''',1)
s=s.replace('if(ball.y<25){ball.y=25;ball.vy=Math.abs(ball.vy)*0.92}',
'''if(ball.y<25){ball.y=25;ball.vy=Math.abs(ball.vy)*0.92;sfxContact("metal",Math.abs(ball.vy)/6)}''',1)

# Shooter lane walls and floor now make physical sounds too.
s=s.replace('if(ball.x<507){ball.x=507;ball.vx=Math.abs(ball.vx)*.25}',
'''if(ball.x<507){ball.x=507;ball.vx=Math.abs(ball.vx)*.25;sfxContact("metal",.7)}''',1)
s=s.replace('if(ball.x>568){ball.x=568;ball.vx=-Math.abs(ball.vx)*.25}',
'''if(ball.x>568){ball.x=568;ball.vx=-Math.abs(ball.vx)*.25;sfxContact("metal",.7)}''',1)
s=s.replace('if(ball.y>1200){ball.y=1200;ball.vy=-Math.abs(ball.vy)*.72}',
'''if(ball.y>1200){ball.y=1200;ball.vy=-Math.abs(ball.vy)*.72;sfxContact("floor",1)}''',1)

# Lamp/target hit sound.
s=s.replace('l.on=true;spark(l.x,l.y,10);addScore(500,l.x,l.y-20)',
'''l.on=true;spark(l.x,l.y,10);sfxContact("target",1.25);addScore(500,l.x,l.y-20)''',1)

# Lower solid floor contact gets a sound when it saves the ball outside the drain.
s=s.replace('ball.y=floorY-ball.r-1;ball.vy=-Math.abs(ball.vy)*0.84;',
'''ball.y=floorY-ball.r-1;ball.vy=-Math.abs(ball.vy)*0.84;sfxContact("floor",Math.min(2,Math.abs(ball.vy)/5));''',1)

# Start/stop siren exactly with Howie's fully-free state.
s=s.replace('if(fullyOpen&&!wasFullyOpen){outStartedAt=performance.now()}',
'''if(fullyOpen&&!wasFullyOpen){outStartedAt=performance.now();startHowieSiren()}''',1)
s=s.replace('else if(!fullyOpen&&wasFullyOpen){if(outStartedAt)',
'''else if(!fullyOpen&&wasFullyOpen){stopHowieSiren();if(outStartedAt)''',1)

# Make sure a new game never inherits an old siren.
s=s.replace('function newGame(){initAudio();sfxStart();const typed=',
'''function newGame(){initAudio();stopHowieSiren();sfxStart();const typed=''',1)

# Red emergency beacon/flash across the visible playfield whenever Howie is free.
needle='function drawWorld(){ctx.fillStyle="#071017";ctx.fillRect(0,0,W,WORLD_H);drawFittedGraphic();'
replacement=r'''function drawWorld(){ctx.fillStyle="#071017";ctx.fillRect(0,0,W,WORLD_H);drawFittedGraphic();if(boxOpen===4){const pulse=.08+.16*(.5+.5*Math.sin(performance.now()/90));ctx.save();ctx.fillStyle=`rgba(255,0,0,${pulse})`;ctx.fillRect(0,cameraY,W,VIEW_H);const beacon=.35+.65*(.5+.5*Math.sin(performance.now()/75));ctx.globalAlpha=beacon;ctx.shadowBlur=38;ctx.shadowColor="#ff0000";ctx.fillStyle="#ff1b1b";ctx.beginPath();ctx.arc(70,cameraY+72,25,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.arc(530,cameraY+72,25,0,Math.PI*2);ctx.fill();ctx.restore();}'''
if needle not in s: raise SystemExit('drawWorld anchor not found')
s=s.replace(needle,replacement,1)

# Breakout caption calls out the siren/light state.
s=s.replace('setStatus("HOWIE\'S OUT THE BOX! DOUBLE POINTS ‼️")',
'''setStatus("🚨 HOWIE'S OUT THE BOX! DOUBLE POINTS ‼️ 🚨")''',1)

p.write_text(s)
print('v23 applied')
# trigger workflow
