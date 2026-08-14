from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v46','LAME — Howie Lucas Pinball v47',1)

# Add a short launch-grace timer used only to keep Level 4 from instantly draining after the shooter exit.
s=s.replace('launchRailActive=false,launchRailStart=0,perfectLaunchPending=false,perfectLaunchAwarded=false,momentumTrailUntil=0,ballTrail=[];',
            'launchRailActive=false,launchRailStart=0,perfectLaunchPending=false,perfectLaunchAwarded=false,momentumTrailUntil=0,ballTrail=[],launchGraceUntil=0;',1)

# Clear grace on reset.
s=s.replace('function resetBall(){launchRailActive=false;perfectLaunchPending=false;',
            'function resetBall(){launchRailActive=false;launchGraceUntil=0;perfectLaunchPending=false;',1)

# Replace launch-rail release with a safer Level 4 release vector and grace period.
old='''if(p>=1){launchRailActive=false;inShooter=false;ball.x=205;ball.y=235;ball.vx=-6.8-level*.35;ball.vy=7.3+level*.25;momentumTrailUntil=now+850;sfxHit(1.2)}return true}'''
new='''if(p>=1){launchRailActive=false;inShooter=false;if(level===4){ball.x=285;ball.y=250;ball.vx=-2.4;ball.vy=5.2;launchGraceUntil=now+2600;setStatus("LEVEL 4 SAFE ENTRY — BALL IN PLAY") }else{ball.x=205;ball.y=235;ball.vx=-6.8-level*.35;ball.vy=7.3+level*.25}momentumTrailUntil=now+850;sfxHit(1.2)}return true}'''
if old not in s:
    raise SystemExit('launch release target not found')
s=s.replace(old,new,1)

# During Level 4 grace, prevent an immediate drain and gently steer the ball back toward playable center lanes.
needle='''if(!inShooter&&ball.x>135&&ball.x<465&&ball.y>1148)drainCommitted=true;'''
replacement='''if(level===4&&performance.now()<launchGraceUntil&&!inShooter){if(ball.y>900){ball.vx+=(300-ball.x)*0.0025;ball.vy=Math.min(ball.vy,5.4)}if(ball.x<72){ball.x=72;ball.vx=Math.abs(ball.vx)*.72+1.2}if(ball.x>528){ball.x=528;ball.vx=-Math.abs(ball.vx)*.72-1.2}}if(!inShooter&&performance.now()>=launchGraceUntil&&ball.x>135&&ball.x<465&&ball.y>1148)drainCommitted=true;'''
if needle not in s:
    raise SystemExit('drain trigger target not found')
s=s.replace(needle,replacement,1)

# Make Level 4's two trick features less likely to sling the ball straight toward the drain.
s=s.replace('{ramp:{name:"SWITCHBACK",s:[482,950],c1:[545,760],c2:[410,540],e:[505,355],entry:[430,550,885,1010],pts:70000,color:"#4fffe5"},spinner:{name:"STAR SPINNER",x:115,y:875,r:44,blades:5,pts:9000,color:"#ffe95c"}}',
'''{ramp:{name:"SWITCHBACK",s:[430,900],c1:[500,700],c2:[390,500],e:[365,340],entry:[360,500,835,955],pts:70000,color:"#4fffe5"},spinner:{name:"STAR SPINNER",x:150,y:790,r:40,blades:5,pts:9000,color:"#ffe95c"}}''',1)

# Safety checks.
if 'LAME — Howie Lucas Pinball v47' not in s:
    raise SystemExit('version bump failed')
if 'launchGraceUntil=now+2600' not in s:
    raise SystemExit('Level 4 launch grace missing')
if 'LEVEL 4 SAFE ENTRY' not in s:
    raise SystemExit('Level 4 safe-entry status missing')

p.write_text(s)
print('v47 patched: Level 4 safe launch entry + less drain-prone feature layout')
