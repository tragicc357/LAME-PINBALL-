from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

s=s.replace('LAME — Howie Lucas Pinball v49','LAME — Howie Lucas Pinball v50',1)

# Facebook/OG: use the actual static JPG, not a screenshot service.
share_url='https://tragicc357.github.io/LAME-PINBALL-/?share=v50'
img_url='https://tragicc357.github.io/LAME-PINBALL-/pinball-table.jpg?v=50'

s=re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{share_url}">', s, count=1)
s=re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{img_url}">', s, count=1)
s=re.sub(r'<meta property="og:image:secure_url" content="[^"]*">', f'<meta property="og:image:secure_url" content="{img_url}">', s, count=1)
s=re.sub(r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="LAME — Howie Lucas Break Out The Box pinball table">', s, count=1)
s=re.sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{img_url}">', s, count=1)

# Add explicit image metadata once.
if 'property="og:image:type"' not in s:
    anchor=f'<meta property="og:image:secure_url" content="{img_url}">'
    extra='\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1024">\n<meta property="og:image:height" content="1536">'
    s=s.replace(anchor,anchor+extra,1)
else:
    s=re.sub(r'<meta property="og:image:type" content="[^"]*">','<meta property="og:image:type" content="image/jpeg">',s,count=1)
    s=re.sub(r'<meta property="og:image:width" content="[^"]*">','<meta property="og:image:width" content="1024">',s,count=1)
    s=re.sub(r'<meta property="og:image:height" content="[^"]*">','<meta property="og:image:height" content="1536">',s,count=1)

# SHARE button uses a fresh versioned URL so Facebook cannot reuse the old base-URL scrape.
s=s.replace('const url="https://tragicc357.github.io/LAME-PINBALL-/";', f'const url="{share_url}";', 1)

# Safety checks.
assert 'pinball-table.jpg?v=50' in s
assert '?share=v50' in s
assert 'image.thum.io/get/ogImage' not in '\n'.join(re.findall(r'<meta[^>]+(?:og:image|twitter:image)[^>]*>',s))

p.write_text(s)
print('v50: direct static Facebook image + fresh share URL')
