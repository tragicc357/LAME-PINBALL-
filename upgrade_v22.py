from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v22</title>',s,count=1)

# Built-in pinball sound engine using Web Audio API. No external audio assets required.
anchor='const W=600,VIEW_H=900,WORLD_H=1300;'
audio=r'''const W=600,VIEW_H=900,WORLD_H=1300;
let audioCtx=null;function initAudio(){try{if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();if(audioCtx.state==="suspended")audioCtx.resume()}catch(e){}}
function tone(freq=440,dur=.08,type="square",vol=.05,slide=0,delay=0){if(!audioCtx)return;const t=audioCtx.currentTime+delay,o=audioCtx.createOscillator(),g=audioCtx.createGain();o.type=type;o.frequency.setValueAtTime(freq,t);if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(30,freq+slide),t+dur);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(Math.max(.0002,vol),t+.005);g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(g).connect(audioCtx.destination);o.start(t);o.stop(t+dur+.02)}
function noise(dur=.06,vol=.035,delay=0){if(!audioCtx)return;const n=Math.max(1,Math.floor(audioCtx.sampleRate*dur)),b=audioCtx.createBuffer(1,n,audioCtx.sampleRate),d=b.getChannelData(0);for(let i=0;i<n;i++)d[i]=Math.random()*2-1;const src=audioCtx.createBufferSource(),g=audioCtx.createGain(),t=audioCtx.currentTime+delay;src.buffer=b;g.gain.setValueAtTime(vol,t);g.gain.exponentialRampToValueAtTime(.0001,t+dur);src.connect(g).connect(audioCtx.destination);src.start(t)}
function sfxStart(){tone(392,.06,"square",.045,80);tone(523,.07,"square",.05,90,.07);tone(659,.1,"square",.055,80,.14)}
function sfxLaunch(p=.5){noise(.045,.03);tone(115+Math.round(p*45),.16,"sawtooth",.06,520,.015)}
function sfxFlipper(power=.5){noise(.035,.055);tone(125+power*55,.045,"square",.06,70)}
function sfxRest(){tone(95,.025,"triangle",.018,-20)}
function sfxBumper(pts=100){tone(520+Math.min(500,pts*.7),.055,"square",.045,120);tone(760,.035,"sine",.025,80,.025)}
function sfxFlap(free=false){tone(free?659:440,.08,"square",.05,100);tone(free?880:554,.11,"triangle",.045,100,.07);if(free)tone(1046,.16,"sine",.05,120,.15)}
function sfxBonus(){tone(660,.055,"square",.04,100);tone(880,.055,"square",.045,100,.06);tone(1100,.11,"square",.05,140,.12)}
function sfxHowie(){noise(.05,.04);tone(230,.08,"square",.06,380);tone(720,.09,"sine",.035,-100,.035)}
function sfxDrain(){tone(260,.12,"sawtooth",.045,-130);tone(150,.18,"triangle",.05,-70,.09)}
function sfxGameOver(){tone(330,.14,"triangle",.045,-70,.25);tone(247,.16,"triangle",.045,-55,.40);tone(165,.3,"triangle",.05,-50,.57)}'''
if anchor not in s: raise SystemExit('world constants anchor not found')
s=s.replace(anchor,audio,1)

# Initialize sound only after a user gesture and play a short start chime.
s=s.replace('function newGame(){const typed=', 'function newGame(){initAudio();sfxStart();const typed=',1)

# Launch spring/plunger sound.
s=s.replace('function fireBall(power){if(!waiting||!playing)return;', 'function fireBall(power){if(!waiting||!playing)return;sfxLaunch(power);',1)

# Bumper/post collision pop.
s=s.replace('addScore(pts,o.x,o.y-45)}}}', 'addScore(pts,o.x,o.y-45);sfxBumper(pts)}}}',1)

# Moving flippers get a hard mechanical clack. Resting contact gets a quiet tap only.
s=s.replace('if(moving){const dot=', 'if(moving){sfxFlipper(t);const dot=',1)
s=s.replace('}else{const inward=', '}else{sfxRest();const inward=',1)

# Box progression sounds and bigger breakout fanfare on the fourth flap.
s=s.replace('if(boxOpen<4){boxOpen++;updateFlaps();spark(300,720,30);', 'if(boxOpen<4){boxOpen++;updateFlaps();sfxFlap(boxOpen===4);spark(300,720,30);',1)

# Bonus sound when all target lamps are completed.
s=s.replace('combo=5;addScore(5000,300,560);shake=8;', 'combo=5;addScore(5000,300,560);sfxBonus();shake=8;',1)

# Howie collision sound.
s=s.replace('howieHitAt=now;spark(h.x,h.y,18);shake=5;addScore(750,h.x,h.y-55);', 'howieHitAt=now;sfxHowie();spark(h.x,h.y,18);shake=5;addScore(750,h.x,h.y-55);',1)

# Drain and game-over sounds.
s=s.replace('async function loseBall(){boxOpen=0;', 'async function loseBall(){sfxDrain();boxOpen=0;',1)
s=s.replace('if(currentBall>=3){playing=false;', 'if(currentBall>=3){sfxGameOver();playing=false;',1)

p.write_text(s)
print('v22 applied')
