from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
preview='https://image.thum.io/get/ogImage/https://tragicc357.github.io/LAME-PINBALL-/facebook-preview-v29.html'
s=re.sub(r'<title>.*?</title>','<title>LAME — Howie Lucas Pinball v29</title>',s,count=1)
s=re.sub(r'<meta property="og:image" content="[^"]+">',f'<meta property="og:image" content="{preview}">',s,count=1)
s=re.sub(r'<meta name="twitter:image" content="[^"]+">',f'<meta name="twitter:image" content="{preview}">',s,count=1)
if 'og:image:alt' not in s:
    anchor=f'<meta property="og:image" content="{preview}">'
    s=s.replace(anchor,anchor+'\n<meta property="og:image:secure_url" content="'+preview+'">\n<meta property="og:image:alt" content="LAME — Howie Lucas Pinball global leaderboard preview">',1)
p.write_text(s)
print('v29 social preview applied')
