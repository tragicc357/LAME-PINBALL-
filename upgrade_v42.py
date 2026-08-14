from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

# Build from the prior v39 feature set, then repair the bad render injection safely.
s=s.replace('LAME — Howie Lucas Pinball v39','LAME — Howie Lucas Pinball v42',1)
s=s.replace('function updateBallTrail();drawBallTrail();drawRealBall(){','function drawRealBall(){',1)

# Insert trail drawing only at the actual render call in drawWorld.
render='ctx.lineCap="butt";drawRealBall()}'
replacement='ctx.lineCap="butt";updateBallTrail();drawBallTrail();drawRealBall()}'
if render not in s:
    raise SystemExit('Ball render hook not found')
s=s.replace(render,replacement,1)

# Sanity checks: startup UI, leaderboards, launcher features, and no malformed declaration.
required=[
    'id="startBtn"',
    'id="watchComputer"',
    'id="topScoresBoard"',
    'id="topTimesBoard"',
    'loadStats();loop();',
    'function drawRealBall(){',
    'function drawLaunchLoopRail(){',
    'PERFECT LAUNCH! +20,000 BONUS',
    'function drawBallTrail(){',
    'LEVEL_GOAL=3000000'
]
for item in required:
    if item not in s:
        raise SystemExit(f'Missing required feature: {item}')
if 'function updateBallTrail();' in s:
    raise SystemExit('Malformed JavaScript declaration still present')

p.write_text(s)
print('v42 ready: v38 gameplay + looping launcher rail + 100% launch bonus + impact speed trail')
