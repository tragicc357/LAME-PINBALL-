from pathlib import Path
p=Path('index.html')
s=p.read_text()
anchor='const posts=[{x:135,y:825,r:17},{x:465,y:825,r:17}];\nconst lamps=[{x:120,y:580,label:"G",on:false},{x:175,y:600,label:"E",on:false},{x:425,y:600,label:"T",on:false},{x:480,y:580,label:"OUT",on:false}];let particles=[],popups=[];'
extra=anchor+'\nconst BOARD_LAYOUTS=[{b:[[165,250],[300,225],[435,255],[210,440],[390,460],[300,635]],p:[[135,825],[465,825]],l:[[120,580],[175,600],[425,600],[480,580]]},{b:[[125,220],[300,300],[475,220],[165,505],[435,505],[300,650]],p:[[185,820],[415,820]],l:[[105,615],[235,560],[365,560],[495,615]]},{b:[[300,185],[145,320],[455,320],[245,470],[355,470],[300,680]],p:[[120,790],[480,790]],l:[[150,590],[250,625],[350,625],[450,590]]},{b:[[110,260],[250,210],[490,260],[185,430],[415,430],[300,610]],p:[[205,845],[395,845]],l:[[90,560],[200,615],[400,615],[510,560]]},{b:[[180,195],[420,195],[300,330],[145,485],[455,485],[300,660]],p:[[150,850],[450,850]],l:[[130,610],[225,555],[375,555],[470,610]]}];function applyLevelLayout(){const q=BOARD_LAYOUTS[Math.max(0,Math.min(4,level-1))];q.b.forEach((v,i)=>{bumpers[i].x=v[0];bumpers[i].y=v[1];bumpers[i].flash=0});q.p.forEach((v,i)=>{posts[i].x=v[0];posts[i].y=v[1]});q.l.forEach((v,i)=>{lamps[i].x=v[0];lamps[i].y=v[1];lamps[i].on=false})}'
if anchor not in s: raise SystemExit('layout anchor missing')
s=s.replace(anchor,extra,1)
p.write_text(s)
