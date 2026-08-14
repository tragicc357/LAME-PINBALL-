from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace('LAME — Howie Lucas Pinball v56','LAME — Howie Lucas Pinball v57',1)
bad='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJIUzI1NiIsInJlZiI6ImJocG5ocmlrYXVuaW11bW10eXh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY1ODc2MzcsImV4cCI6MjEwMjE2MzYzN30.gwk15JgK8enkjMY-MD9XYvzLfoWv0yYEXq9WRNN26PA'
good='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJocG5ocmlrYXVuaW11bW10eXh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY1ODc2MzcsImV4cCI6MjEwMjE2MzYzN30.gwk15JgK8enkjMY-MD9XYvzLfoWv0yYEXq9WRNN26PA'
if bad not in s:
    raise SystemExit('bad anon key not found')
s=s.replace(bad,good)
# make leaderboard retry message include actual failure state, while retaining periodic retry behavior
s=s.replace('GLOBAL SCORES RECONNECTING…','GLOBAL SCORES RECONNECTING…',1)
for token in ['LAME — Howie Lucas Pinball v57','eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJocG5ocmlrYXVuaW11bW10eXh0']:
    if token not in s: raise SystemExit('missing '+token)
p.write_text(s)
