from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

if 'LAME — Howie Lucas Pinball v47' not in s:
    raise SystemExit('Expected v47 title not found')
s=s.replace('LAME — Howie Lucas Pinball v47','LAME — Howie Lucas Pinball v48',1)

# Change the physical box wording when Howie is free.
old='''ctx.shadowBlur=lit?24:4;ctx.fillStyle=lit?"#fff36a":"#19100a";ctx.font="900 44px Impact";ctx.textAlign="center";ctx.fillText("LAME",bx+bw/2,by+92);ctx.shadowBlur=0;'''
new='''ctx.shadowBlur=lit?24:4;ctx.textAlign="center";if(boxOpen===4){ctx.fillStyle="#ffffff";ctx.font="900 23px Impact,Arial Black,Arial";ctx.fillText("HOWIE IS",bx+bw/2,by+70);ctx.fillStyle="#6ec8ff";ctx.font="900 22px Impact,Arial Black,Arial";ctx.fillText("OUT THE BOX",bx+bw/2,by+101)}else{ctx.fillStyle=lit?"#fff36a":"#19100a";ctx.font="900 44px Impact";ctx.fillText("LAME",bx+bw/2,by+92)}ctx.shadowBlur=0;'''
if old not in s:
    raise SystemExit('drawRealBox wording target not found')
s=s.replace(old,new,1)

# Add a synchronized visual reaction layer.
marker='''function draw(){ctx.clearRect(0,0,W,VIEW_H);ctx.save();ctx.translate(0,-cameraY);drawWorld();ctx.restore()}'''
if marker not in s:
    raise SystemExit('draw() target not found')
replacement='''let actionPulseUntil=0,actionPulseColor="#ffffff",actionPulseText="";function actionFeedback(text,color="#ffffff",ms=220){actionPulseText=text||"";actionPulseColor=color;actionPulseUntil=performance.now()+ms}function drawActionFeedback(){const now=performance.now();if(now>=actionPulseUntil)return;const left=actionPulseUntil-now,alpha=Math.min(.22,left/700*.22+.04);ctx.save();ctx.globalAlpha=alpha;ctx.fillStyle=actionPulseColor;ctx.fillRect(0,0,W,VIEW_H);ctx.globalAlpha=Math.min(1,left/160);ctx.shadowBlur=22;ctx.shadowColor=actionPulseColor;ctx.fillStyle="#fff";ctx.font="900 28px Impact,Arial Black,Arial";ctx.textAlign="center";ctx.fillText(actionPulseText,W/2,110);ctx.restore()}function draw(){ctx.clearRect(0,0,W,VIEW_H);ctx.save();ctx.translate(0,-cameraY);drawWorld();ctx.restore();drawActionFeedback()}'''
s=s.replace(marker,replacement,1)

# Wrap existing sound functions with richer pinball-style layers and simultaneous visuals.
start_marker='''nicknameInput.value=playerName;applyLayout();updateHud();loadStats();loop();'''
if start_marker not in s:
    raise SystemExit('startup marker not found')
wrappers='''try{const v48Hit=sfxHit;sfxHit=function(strength=1){actionFeedback("CLACK!",strength>1.4?"#fff36a":"#74d9ff",150);const r=v48Hit(strength);noise(.022,.022);tone(1450+Math.min(2,Number(strength)||1)*180,.028,"square",.014,-620);return r}}catch(e){}try{const v48Flip=sfxFlipper;sfxFlipper=function(){actionFeedback("FLIP!","#ffd21f",130);const r=v48Flip();noise(.028,.03);tone(145,.055,"square",.025,95);return r}}catch(e){}try{const v48Launch=sfxLaunch;sfxLaunch=function(power=.85){actionFeedback("LAUNCH!","#ff725c",240);const r=v48Launch(power);noise(.05,.035);tone(72,.11,"sawtooth",.028,240);return r}}catch(e){}try{const v48Drain=sfxDrain;sfxDrain=function(){actionFeedback("DRAIN!","#ff4141",440);const r=v48Drain();tone(230,.10,"sine",.028,-110);setTimeout(()=>tone(125,.16,"sine",.025,-35),75);return r}}catch(e){}try{const v48Bonus=sfxBonus;sfxBonus=function(){actionFeedback("BONUS!","#77ff9a",480);const r=v48Bonus();tone(880,.07,"sine",.026,380);setTimeout(()=>tone(1320,.09,"triangle",.022,240),65);return r}}catch(e){}try{const v48Trick=trickAward;trickAward=function(name,pts){actionFeedback(name.includes("SPINNER")?"SPINNER!":"FEATURE SHOT!",name.includes("SPINNER")?"#ff77eb":"#6fe3ff",420);if(name.includes("SPINNER")){for(let i=0;i<3;i++)setTimeout(()=>{noise(.012,.018);tone(1750+i*120,.018,"square",.011,-400)},i*28)}return v48Trick(name,pts)}}catch(e){}'''
s=s.replace(start_marker,wrappers+start_marker,1)

# Safety checks.
for required in ['LAME — Howie Lucas Pinball v48','HOWIE IS','OUT THE BOX','function drawActionFeedback()','actionFeedback("CLACK!"','actionFeedback("DRAIN!"','const v48Trick=trickAward']:
    if required not in s:
        raise SystemExit('Missing v48 feature: '+required)

p.write_text(s)
print('v48 patched: dynamic box wording + synchronized realistic sound/visual feedback')
