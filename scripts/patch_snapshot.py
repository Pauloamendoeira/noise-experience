from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1. Keep only diagnostic cards in the Snapshot header.
s, n1 = re.subn(
    r'\s*<div class="snap"><small>Tempo simulado</small><b id="snapTime">0</b></div>\n'
    r'\s*<div class="snap"><small>Patrimônio final</small><b id="snapWorth">R\$ 0</b></div>\n'
    r'\s*<div class="snap"><small>Custo provável do ruído</small><b id="snapInvisible">R\$ 0</b></div>',
    '',
    s,
    count=1,
)

# 2. Reframe consequence language away from financial cost.
s, n2 = re.subn(
    r'<b>Custo provável:</b> \$\{r\.pain\}',
    '<b>Pode produzir:</b> ${r.pain}',
    s,
    count=1,
)

# 3. Replace the monetary right-hand card with a systemic consequence card.
old_block = '''       <div class="noise-cost">
         <div style="font-size:9px;color:#ffc760;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">O custo da decisão ruim</div>
         <div style="font-size:20px;font-weight:900;color:#fff">${fmt(invisibleEstimate)}</div>
         <div style="font-size:9.5px;color:#b9c7d3;line-height:1.3;margin-top:3px">podem estar sendo consumidos pelo jeito como a empresa decide, não necessariamente pelo mercado.</div>
       </div>'''
new_block = '''       <div class="noise-cost">
         <div style="font-size:9px;color:#ffc760;font-weight:900;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px">O que este padrão pode produzir</div>
         <div style="font-size:11px;font-weight:850;line-height:1.35;color:#f4f7fa">${topRisks[0]?.pain || "Retrabalho, lentidão decisória e pressão crescente sobre o sistema."}</div>
         <div style="font-size:9.5px;color:#b9c7d3;line-height:1.3;margin-top:3px">O efeito aparece na continuidade, na coordenação e na capacidade de responder antes que o ruído vire problema.</div>
       </div>'''
if old_block not in s:
    raise SystemExit('Monetary consequence block not found')
s = s.replace(old_block, new_block, 1)
n3 = 1

# 4. Remove assignments to deleted DOM elements.
for line in [
    ' document.getElementById("snapTime").textContent=`${state.year-2026} anos e ${state.month} meses`;\n',
    ' document.getElementById("snapWorth").textContent=fmt(state.cash+state.assets-state.debt);\n',
    ' document.getElementById("snapInvisible").textContent=fmt(invisibleEstimate);\n',
]:
    if line not in s:
        raise SystemExit('Expected DOM assignment not found: ' + line.strip())
    s = s.replace(line, '', 1)

if (n1, n2, n3) != (1, 1, 1):
    raise SystemExit(f'Unexpected replacement counts: {(n1, n2, n3)}')

p.write_text(s, encoding='utf-8')
print('Snapshot updated: financial output removed; diagnostic consequences preserved.')
