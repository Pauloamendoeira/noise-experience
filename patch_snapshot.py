from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Reframe the summary cards when these labels exist in the current markup.
s = s.replace('<small>Maior acerto</small>', '<small>Recurso de proteção</small>')
s = s.replace('<small>Maior risco</small>', '<small>Principal risco decisório</small>')
s = s.replace('<small>Custo invisível estimado</small>', '<small>Custo provável do ruído</small>')

start = s.index('function finish(){')
end = s.index('function restartGame(){', start)

new_finish = r'''function finish(){
 const p=state.patterns;
 const choices=state.history.map(h=>h.choice);
 const strengthPairs=[
   ["Planejamento",p.planning],["Estrutura",p.structureFirst],["Pessoas",p.people],["Liquidez",p.liquidity],["Tecnologia",p.tech],["Compliance",p.compliance]
 ].sort((a,b)=>b[1]-a[1]);
 const strength=strengthPairs[0][0];

 const strengths=[];
 if(p.planning>=3)strengths.push("Planejamento aparece como mecanismo de proteção contra urgência e improviso.");
 if(p.structureFirst>=3)strengths.push("Você tende a proteger capacidade e sustentação antes de acelerar crescimento.");
 if(p.people>=3)strengths.push("Pessoas entram como capacidade crítica do sistema, não apenas como custo.");
 if(p.liquidity>=2)strengths.push("Liquidez funciona como proteção de opcionalidade quando a pressão aumenta.");
 if(p.tech>=1 && p.planning>=2)strengths.push("Tecnologia tende a entrar com teste e algum grau de governança.");
 if(!strengths.length)strengths.push("Você mantém capacidade de decidir mesmo sob informação incompleta e pressão crescente.");

 const risks=[];
 const addRisk=(title,text,pain,score)=>risks.push({title,text,pain,score});

 if(choices.includes("Cobrir a proposta")) addRisk(
   "Dependência de pessoas-chave",
   "A pessoa foi preservada, mas a concentração de conhecimento permaneceu.",
   "Na prática, decisões, clientes e operação podem continuar dependentes de poucos indivíduos. Quando um deles sai, o custo aparece em atraso, retrabalho e perda de contexto.",
   9
 );
 if(choices.includes("Deixar sair e contratar no mercado")) addRisk(
   "Perda de conhecimento crítico",
   "Você aceitou ruptura em uma posição que concentrava conhecimento operacional.",
   "O custo provável vai além do recrutamento: erros repetidos, decisões mais lentas, perda de memória operacional e clientes sentindo a descontinuidade.",
   10
 );
 if(p.people<=0 && (p.planning>=2 || p.structureFirst>=2)) addRisk(
   "Centralização invisível",
   "Seu padrão protege estrutura, mas distribui pouca capacidade decisória.",
   "Sob pressão, decisões voltam para o líder. A empresa parece organizada, mas começa a depender de uma pessoa para destravar exceções, prioridades e conflitos.",
   9
 );
 if(p.shortTerm>=2 || state.pressure>=38) addRisk(
   "Custo invisível de coordenação",
   "Urgência e correções sucessivas estão consumindo atenção para manter as partes funcionando juntas.",
   "Esse custo raramente aparece no DRE. Ele aparece em reuniões, alinhamentos, retrabalho, exceções, energia perdida e decisões que demoram mais do que deveriam.",
   10
 );
 if(p.structureFirst<2 && (p.riskTaking>=1 || state.revenue>30000)) addRisk(
   "Crescimento que consome capacidade",
   "Há sinais de aceleração mais rápida do que a estrutura consegue absorver.",
   "Receita pode crescer enquanto margem, qualidade e velocidade deterioram. O crescimento passa a financiar a própria desorganização.",
   10
 );
 if(choices.includes("Implantar em toda a operação") || (p.tech>=2 && p.planning<2)) addRisk(
   "Tecnologia como atalho",
   "A tecnologia entrou antes de uma validação suficiente da arquitetura operacional.",
   "IA e automação podem reduzir custo local enquanto multiplicam um processo errado, criando dependência, retrabalho e velocidade no lugar errado.",
   9
 );
 if(choices.includes("Esperar para ver o que acontece") || p.compliance<0) addRisk(
   "Governança reativa",
   "Governança e compliance ganham atenção depois que o risco já virou pressão.",
   "O efeito costuma chegar tarde e caro: correção emergencial, perda de margem, atraso comercial e energia executiva desviada para apagar incêndios evitáveis.",
   9
 );
 if(p.planning<1 && p.compliance<=0 && state.pressure>=32) addRisk(
   "Política organizacional",
   "Com poucos critérios explícitos e pressão crescente, a decisão fica mais vulnerável à negociação interna.",
   "Prioridades podem passar a refletir poder, urgência local e capacidade de influência, não o que gera mais valor para o sistema.",
   8
 );
 if(state.debt>70000 || state.cash<50000 || p.liquidity<0) addRisk(
   "Liquidez vulnerável",
   "Seu espaço financeiro de manobra ficou estreito.",
   "Quando a folga desaparece, o horizonte encurta. A urgência passa a decidir pela estratégia e opções boas deixam de existir justamente quando mais seriam necessárias.",
   10
 );
 if(state.noise>=45) addRisk(
   "Ruído sistêmico acumulado",
   "As decisões isoladas podem parecer defensáveis, mas o conjunto está gerando fricção entre caixa, capacidade, pressão e execução.",
   "O risco não é uma decisão errada. É repetir um padrão caro sem perceber até ele aparecer como queda de margem, exaustão ou perda de velocidade.",
   10
 );

 if(!risks.length) addRisk(
   "Excesso de controle",
   "Seu padrão está relativamente coerente, mas protege estrutura e previsibilidade com força.",
   "O risco é transformar prudência em lentidão: oportunidades passam a exigir validação demais, decisões sobem na hierarquia e a organização perde velocidade sem perceber.",
   6
 );

 risks.sort((a,b)=>b.score-a.score);
 const topRisks=risks.slice(0,3);
 const risk=topRisks[0].title;
 const primary=topRisks[0];

 const systemicBase = Math.max(0,state.noise-18)*900 + Math.max(0,state.pressure-25)*650 + Math.max(0,55-state.capacity)*500;
 const patternCost = topRisks.reduce((sum,r)=>sum + r.score*1800,0);
 const invisibleEstimate = Math.max(state.invisibleCost, Math.round(systemicBase + patternCost));

 const consequenceMap={
   "Dependência de pessoas-chave":"velocidade, continuidade e capacidade de escala",
   "Perda de conhecimento crítico":"retrabalho, continuidade e experiência do cliente",
   "Centralização invisível":"velocidade, autonomia e tempo executivo",
   "Custo invisível de coordenação":"margem, foco e velocidade de execução",
   "Crescimento que consome capacidade":"margem, qualidade e sustentabilidade do crescimento",
   "Tecnologia como atalho":"eficiência real, integração e governança",
   "Governança reativa":"margem, previsibilidade e tempo executivo",
   "Política organizacional":"qualidade da decisão, prioridade e velocidade",
   "Liquidez vulnerável":"opcionalidade, horizonte estratégico e poder de reação",
   "Ruído sistêmico acumulado":"margem, pessoas, caixa e execução",
   "Excesso de controle":"velocidade, autonomia e aproveitamento de oportunidades"
 };
 const consequence=consequenceMap[primary.title] || "margem, velocidade e capacidade de execução";

 const html=`
   <div style="background:#241b1d;border:1px solid #6e3b40;border-radius:12px;padding:14px 15px;margin-bottom:14px">
     <div style="font-size:10px;color:#ff8f96;font-weight:900;text-transform:uppercase;letter-spacing:1.1px;margin-bottom:7px">Alerta do seu padrão decisório</div>
     <div style="font-size:18px;font-weight:900;line-height:1.2;color:#f4f7fa">Suas decisões estão criando ruído onde você talvez não esteja vendo.</div>
     <div style="font-size:12px;color:#c6d0d9;line-height:1.5;margin-top:8px">O principal risco observado foi <b style="color:#fff">${primary.title}</b>. Em uma empresa real, esse padrão tende a atingir ${consequence}.</div>
   </div>

   <div style="margin-bottom:15px">
     <div style="font-size:10px;color:#ffc760;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-bottom:7px">Onde a má decisão começa a doer</div>
     ${topRisks.map((r,i)=>`<div style="background:#17222d;border:1px solid ${i===0?'#785055':'#273746'};border-radius:10px;padding:11px 12px;margin:7px 0"><div style="display:flex;gap:8px;align-items:flex-start"><span style="font-size:10px;font-weight:900;color:#ff8f96;margin-top:2px">0${i+1}</span><div><b>${r.title}</b><div style="font-size:11px;color:#b9c7d3;line-height:1.45;margin-top:4px">${r.text}</div><div style="font-size:11px;color:#e2e8ed;line-height:1.45;margin-top:5px"><b>O que isso pode custar:</b> ${r.pain}</div></div></div></div>`).join("")}
   </div>

   <div style="background:#111a22;border:1px solid #354758;border-radius:12px;padding:13px 14px;margin-bottom:14px">
     <div style="font-size:10px;color:#ffc760;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px">O custo da decisão ruim</div>
     <div style="font-size:21px;font-weight:900;color:#fff">${fmt(invisibleEstimate)}</div>
     <div style="font-size:11px;color:#b9c7d3;line-height:1.5;margin-top:5px">podem estar sendo consumidos pelo jeito como a empresa decide, não necessariamente pelo mercado.</div>
   </div>

   <div style="margin-bottom:13px">
     <div style="font-size:10px;color:#67e5d1;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:7px">O que hoje protege você</div>
     ${strengths.slice(0,1).map(x=>`<div style="margin:5px 0">• ${x}</div>`).join("")}
   </div>

   <div style="font-size:14px;font-weight:800;line-height:1.35;color:#f4f7fa;margin:14px 0 7px">O problema não parece estar nas suas decisões isoladas. Está no custo acumulado entre elas.</div>
   <div style="font-size:11px;color:#8496a6;line-height:1.45">Leitura indicativa baseada nas decisões desta simulação. São hipóteses diagnósticas sobre padrões de risco, não afirmações sobre sua empresa real.</div>
 `;

 document.getElementById("snapNoise").textContent=Math.round(state.noise);
 document.getElementById("snapTime").textContent=`${state.year-2026} anos e ${state.month} meses`;
 document.getElementById("snapWorth").textContent=fmt(state.cash+state.assets-state.debt);
 document.getElementById("snapInvisible").textContent=fmt(invisibleEstimate);
 document.getElementById("snapStrength").textContent=strength;
 document.getElementById("snapRisk").textContent=risk;
 document.getElementById("patternText").innerHTML=html;
 document.getElementById("snapshot").style.display="block";
}
'''

s = s[:start] + new_finish + s[end:]
p.write_text(s, encoding='utf-8')
