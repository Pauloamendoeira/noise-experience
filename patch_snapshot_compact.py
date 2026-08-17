from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Ensure final commercial CTA is present regardless of deploy order.
s=s.replace('QUERO ENTENDER MEUS BLIND SPOTS','QUERO IDENTIFICAR ESSES RUÍDOS NA MINHA EMPRESA')
s=s.replace('Paulo%2C%20fiz%20o%20NOISE%20Experience.%20Quero%20entender%20melhor%20o%20que%20apareceu%20no%20meu%20Snapshot.','Paulo%2C%20fiz%20o%20NOISE%20Experience.%20Quero%20identificar%20onde%20esses%20ru%C3%ADdos%20est%C3%A3o%20aparecendo%20na%20minha%20empresa.')

# Responsive compact layout for the final Snapshot.
style='''\n<style id="noise-snapshot-compact">\n#snapshot .snapshot-inner{padding-top:14px;padding-bottom:14px}\n#snapshot .snapshot-inner>div:first-child{margin-bottom:6px}\n#snapshot .snapshot-inner h1,#snapshot .snapshot-inner h2{margin-top:0}\n.noise-result-grid{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.8fr);gap:10px;align-items:start}\n.noise-result-left,.noise-result-right{display:grid;gap:8px}\n.noise-risk-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}\n.noise-alert{background:#241b1d;border:1px solid #6e3b40;border-radius:10px;padding:10px 11px}\n.noise-card{background:#17222d;border:1px solid #273746;border-radius:9px;padding:9px 10px}\n.noise-card.primary{border-color:#785055}\n.noise-cost{background:#111a22;border:1px solid #354758;border-radius:10px;padding:10px 11px}\n.noise-provoke{background:#17222d;border:1px solid #273746;border-radius:9px;padding:9px 10px}\n#snapshot .question{margin-top:8px;padding:10px 12px}\n#snapshot .question h3{margin:0 0 4px}\n#snapshot .question p{margin:0 0 8px}\n@media(max-width:900px){.noise-result-grid{grid-template-columns:1fr}.noise-risk-grid{grid-template-columns:1fr 1fr}}\n@media(max-width:620px){.noise-risk-grid{grid-template-columns:1fr}}\n</style>\n'''
if 'id="noise-snapshot-compact"' not in s:
    s=s.replace('</head>',style+'</head>',1)

start=s.index('function finish(){')
html_start=s.index(' const html=`',start)
html_end=s.index('\n `;',html_start)+4

compact=r''' const html=`
   <div class="noise-result-grid">
     <div class="noise-result-left">
       <div class="noise-alert">
         <div style="font-size:9px;color:#ff8f96;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Alerta do seu padrão decisório</div>
         <div style="font-size:16px;font-weight:900;line-height:1.15;color:#f4f7fa">Suas decisões estão criando ruído onde você talvez não esteja vendo.</div>
         <div style="font-size:10px;color:#c6d0d9;line-height:1.35;margin-top:5px">Principal risco: <b style="color:#fff">${primary.title}</b>. Em uma empresa real, esse padrão tende a atingir ${consequence}.</div>
       </div>

       <div>
         <div style="font-size:9px;color:#ffc760;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin:1px 0 5px">Onde a má decisão começa a doer</div>
         <div class="noise-risk-grid">
           ${topRisks.map((r,i)=>`<div class="noise-card ${i===0?'primary':''}"><div style="display:flex;gap:6px;align-items:flex-start"><span style="font-size:9px;font-weight:900;color:#ff8f96;margin-top:1px">0${i+1}</span><div><b style="font-size:11px">${r.title}</b><div style="font-size:9.5px;color:#b9c7d3;line-height:1.3;margin-top:3px">${r.text}</div><div style="font-size:9.5px;color:#e2e8ed;line-height:1.3;margin-top:3px"><b>Custo provável:</b> ${r.pain}</div></div></div></div>`).join("")}
         </div>
       </div>
     </div>

     <div class="noise-result-right">
       <div class="noise-cost">
         <div style="font-size:9px;color:#ffc760;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">O custo da decisão ruim</div>
         <div style="font-size:20px;font-weight:900;color:#fff">${fmt(invisibleEstimate)}</div>
         <div style="font-size:9.5px;color:#b9c7d3;line-height:1.3;margin-top:3px">podem estar sendo consumidos pelo jeito como a empresa decide, não necessariamente pelo mercado.</div>
       </div>

       <div class="noise-card">
         <div style="font-size:9px;color:#67e5d1;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">O que hoje protege você</div>
         ${strengths.slice(0,1).map(x=>`<div style="font-size:10px;line-height:1.35">• ${x}</div>`).join("")}
       </div>

       <div class="noise-provoke">
         <div style="font-size:11px;font-weight:850;line-height:1.3;color:#f4f7fa">O problema não parece estar nas decisões isoladas. Está no custo acumulado entre elas.</div>
         <div style="font-size:10px;line-height:1.35;color:#e2e8ed;margin-top:5px"><b>Se esses padrões apareceram em seis decisões, o que pode estar acontecendo na sua empresa sem aparecer no relatório?</b></div>
       </div>

       <div style="font-size:8.5px;color:#8496a6;line-height:1.3">Leitura indicativa baseada nesta simulação. São hipóteses diagnósticas sobre padrões de risco, não afirmações sobre sua empresa real.</div>
     </div>
   </div>
 `;'''

s=s[:html_start]+compact+s[html_end:]
p.write_text(s,encoding='utf-8')
