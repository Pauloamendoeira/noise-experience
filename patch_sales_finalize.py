from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('QUERO ENTENDER MEUS BLIND SPOTS','QUERO IDENTIFICAR ESSES RUÍDOS NA MINHA EMPRESA')
s=s.replace('Paulo%2C%20fiz%20o%20NOISE%20Experience.%20Quero%20entender%20melhor%20o%20que%20apareceu%20no%20meu%20Snapshot.','Paulo%2C%20fiz%20o%20NOISE%20Experience.%20Quero%20identificar%20onde%20esses%20ru%C3%ADdos%20est%C3%A3o%20aparecendo%20na%20minha%20empresa.')
needle='<div style="font-size:14px;font-weight:800;line-height:1.35;color:#f4f7fa;margin:14px 0 7px">O problema não parece estar nas suas decisões isoladas. Está no custo acumulado entre elas.</div>'
insert=needle+'\n   <div style="background:#17222d;border:1px solid #273746;border-radius:10px;padding:11px 12px;margin:10px 0 8px;font-size:12px;line-height:1.5;color:#e2e8ed"><b>Se esses padrões apareceram em seis decisões, o que pode estar acontecendo na sua empresa sem aparecer no relatório?</b></div>'
if needle not in s: raise SystemExit('provocacao base nao encontrada')
s=s.replace(needle,insert,1)
p.write_text(s,encoding='utf-8')
