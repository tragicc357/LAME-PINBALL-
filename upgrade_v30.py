from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v30','LAME — Howie Lucas Pinball v31',1)
s=s.replace('addScore(750,h.x,h.y);setStatus("HOWIE BUMPER! BALL KICKED WITH HIS MOMENTUM")','score+=100000;updateHud();openFlapsAndLevels();setStatus("HOWIE BUMPER! +100,000 POINTS • BALL KICKED WITH HIS MOMENTUM")',1)
p.write_text(s)
