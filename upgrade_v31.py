from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'LAME — Howie Lucas Pinball v30' in s:
    s=s.replace('LAME — Howie Lucas Pinball v30','LAME — Howie Lucas Pinball v31',1)
old='sfxHit(2.4);tone(880,.08,"sine",.045,180);addScore(750,h.x,h.y);setStatus("HOWIE BUMPER! BALL KICKED WITH HIS MOMENTUM")'
new='sfxHit(2.4);tone(880,.08,"sine",.045,180);score+=100000;updateHud();openFlapsAndLevels();setStatus("HOWIE BUMPER! +100,000 POINTS • BALL KICKED WITH HIS MOMENTUM")'
if old not in s:
    raise SystemExit('Howie hit scoring target not found')
s=s.replace(old,new,1)
p.write_text(s)
print('v31 patched: Howie hit = 100,000 points')
