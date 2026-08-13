from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v25','LAME — Howie Lucas Pinball v26',1)
p.write_text(s)
