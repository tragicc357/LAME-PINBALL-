from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('<meta property="og:image:width" content="120">','<meta property="og:image:width" content="200">')
s=s.replace('<meta property="og:image:height" content="180">','<meta property="og:image:height" content="200">')
p.write_text(s)
print('v12 social preview metadata updated')
