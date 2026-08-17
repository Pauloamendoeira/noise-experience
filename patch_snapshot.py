from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
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
 if(p.planning>=3)strengths.push("Você tende a criar estrutura antes que a urgência assuma o controle da decisão.");
 if(p.structureFirst>=3)strengths.push("Você protege capacidade e sustentação antes de acelerar crescimento.");
 if(p.people>=3)strengths.push("Você trata pessoas como capacidade crítica do sistema, não apenas como custo.");
 if(p.liquidity>=2)strengths.push("Liquidez aparece como critério real de segurança e opcionalidade.");
 if(p.tech>=1 && p.planning>=2)strengths.push("Tecnologia tende a entrar com algum grau de teste e governança, em vez de apenas como promessa de eficiência.");
 if(!strengths.length)strengths.push("Seu padrão mostra adaptação rápida e disposição para decidir mesmo com informação incompleta.");

 const risks=[];
 const addRisk=(title,text,score)=>risks.push({title,text,score});

 if(choices.includes("Cobrir a proposta")) addRisk(
   "Dependência de pessoas-chave",
   "A resposta preservou a pessoa, mas não reduziu a concentração de conhecimento. Em uma empresa real, isso pode manter decisões, clientes e operação dependentes de poucos indivíduos.",
   9
 );
 if(choices.includes("Deixar sair e contratar no mercado")) addRisk(
   "Perda de conhecimento crítico",
   "Você aceitou ruptura de uma posição que concentrava conhecimento operacional. O custo provável não é apenas recrutamento, mas atraso, retrabalho e perda de contexto.",
   10
 );
 if(p.people<=0 && (p.planning>=2 || p.structureFirst>=2)) addRisk(
   "Centralização operacional",
   "Seu padrão protege estrutura, mas investe pouco em distribuir capacidade decisória. Sob pressão, isso pode concentrar decisões no líder e transformar coordenação em gargalo.",
   8
 );
 if(p.shortTerm>=2 || state.pressure>=38) addRisk(
   "Custo invisível de coordenação",
   "A combinação de urgência, pressão e decisões corretivas tende a consumir atenção em alinhamentos, exceções e retrabalho que não aparecem diretamente no DRE.",
   9
 );
 if(p.structureFirst<2 && (p.riskTaking>=1 || state.revenue>30000)) addRisk(
   "Crescimento antes da estrutura",
   "Há sinais de aceleração mais rápida que a capacidade de sustentação. O risco é transformar crescimento em pressão operacional, queda de qualidade e dívida organizacional.",
   10
 );
 if(choices.includes("Implantar em toda a operação") || (p.tech>=2 && p.planning<2)) addRisk(
   "Tecnologia como atalho",
   "A adoção tecnológica aparece antes de uma validação suficiente da arquitetura operacional. IA pode acelerar eficiência, mas também automatizar ruído, dependência e retrabalho.",
   9
 );
 if(choices.includes("Esperar para ver o que acontece") || p.compliance<0) addRisk(
   "Governança reativa",
   "Governança e compliance tendem a ganhar atenção depois que o risco já virou pressão. Em ambientes regulados, o custo costuma aparecer tarde e de forma desproporcional.",
   9
 );
 if(p.planning<1 && p.compliance<=0 && state.pressure>=32) addRisk(
   "Política organizacional",
   "Com poucos critérios explícitos e pressão crescente, decisões podem migrar do mérito estratégico para negociação entre áreas, interesses e urgências locais.",
   7
 );
 if(state.debt>70000 || state.cash<50000 || p.liquidity<0) addRisk(
   "Liquidez vulnerável",
   "Seu espaço de manobra financeiro ficou estreito. Isso tende a encurtar o horizonte das decisões e aumentar o poder das urgências sobre a estratégia.",
   10
 );
 if(state.noise>=45) addRisk(
   "Ruído sistêmico acumulado",
   "As decisões isoladas podem parecer defensáveis, mas o conjunto está produzindo fricção entre caixa, capacidade, pressão e execução.",
   10
 );

 if(!risks.length) addRisk(
   "Excesso de controle",
   "Seu padrão está relativamente coerente. O principal risco provável é proteger tanto estrutura, liquidez e previsibilidade que oportunidades passem a exigir validação demais antes de avançar.",
   5
 );

 risks.sort((a,b)=>b.score-a.score);
 const topRisks=risks.slice(0,3);
 const risk=topRisks[0].title;

 const systemicBase = Math.max(0,state.noise-18)*900 + Math.max(0,state.pressure-25)*650 + Math.max(0,55-state.capacity)*500;
 const patternCost = topRisks.reduce((sum,r)=>sum + r.score*1800,0);
 const invisibleEstimate = Math.max(state.invisibleCost, Math.round(systemicBase + patternCost));

 const html=`
   <div style="margin-bottom:15px">
     <div style="font-size:10px;color:#67e5d1;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:7px">Onde seu modelo funciona bem</div>
     ${strengths.slice(0,2).map(x=>`<div style="margin:5px 0">• ${x}</div>`).join("")}
   </div>
   <div style="margin-bottom:15px">
     <div style="font-size:10px;color:#ffc760;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-bottom:7px">Ruídos prováveis que você pode não estar vendo</div>
     ${topRisks.map(r=>`<div style="background:#17222d;border:1px solid #273746;border-radius:10px;padding:10px 11px;margin:7px 0"><b>${r.title}</b><div style="font-size:11px;color:#b9c7d3;line-height:1.45;margin-top:4px">${r.text}</div></div>`).join("")}
   </div>
   <div style="font-size:10px;color:#8496a6;line-height:1.45">Leitura indicativa baseada nas decisões desta simulação. Os itens acima são hipóteses diagnósticas, não afirmações sobre sua empresa real.</div>
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
