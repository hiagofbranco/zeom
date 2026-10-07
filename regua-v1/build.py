#!/usr/bin/env python3
"""Gera a Régua V1 separada:
  - emails/reguas-v1/*.html  (4 e-mails novos + cópias dos e-mails V1 que já existiam)
  - regua-v1.html            (fluxograma + comunicações + preview, no layout de comunicacoes-zeom.html)

Uso: python3 regua-v1/build.py
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import emails  # noqa: E402

SITE_ASSETS = 'https://hiagofbranco.github.io/zeom/assets/'
OUT_DIR = ROOT / 'emails/reguas-v1'

# e-mails V1 que já tinham layout pronto em emails/reguas/
REUSED = {
    'v1-04-engajamento-d14.html': '11-prevencao-engajamento-d14.html',
    'v1-05-oportunidades-cambio.html': '15-ongoing-oportunidades-cambio.html',
}

# ajustes de copy aplicados só na cópia V1
COPY_EDITS = {
    'v1-04-engajamento-d14.html': [
        ('<title>Zeom · Seus recursos continuam disponíveis</title>', '<title>Zeom · Por onde começar na sua conta Zeom</title>'),
        ('>A sua conta Zeom permanece ativa', '>{{first_name}}, a sua conta Zeom permanece ativa'),
        ('porque sua conta Zeom está inativa há 14 dias', 'porque sua conta Zeom está sem movimentações há 14 dias'),
    ],
}

FASES = {
    'ativacao': dict(nome='Prevenção · Valor & Repescagem', classe='pre',
                     desc='Cartão, investimento e multiconta parados. Espaço reservado para uma trilha de conteúdo educacional futura, no tom do Zeom AI.'),
    'engajamento': dict(nome='Prevenção · Engajamento', classe='pre',
                        desc='Cliente já ativado e sem transação · 21 dias · fecha no push D21'),
    'oportunidades': dict(nome='Ongoing · Oportunidades', classe='ong',
                          desc='Gatilho de mercado (variação cambial) · versão neutra, sem urgência'),
    'churn': dict(nome='Churn · Win Back', classe='churn',
                  desc='Inativo por longo período · assinado pela Equipe Zeom · copy em proposta, aguardando aprovação'),
}

PROPOSTA = 'Proposta de copy'
DATA = [
    dict(fase='ativacao', canal='email', dia='D7', trigger='1 semana sem ativar o cartão — Repescagem · Cartão',
         campos=[dict(label='Assunto', value='Seu cartão em dólar está pronto')],
         corpo='Ative quando quiser — sem prazo para isso mudar.', emailId='v1-01-repescagem-cartao-d7'),
    dict(fase='ativacao', canal='email', dia='D+X', trigger='Fez Pix mas nunca investiu, X dias depois — Repescagem · Investimento',
         campos=[dict(label='Assunto', value='Seus investimentos internacionais estão disponíveis')],
         corpo='Sem valor mínimo para começar, no seu tempo.', emailId='v1-02-repescagem-investimento'),
    dict(fase='ativacao', canal='email', dia='D7', trigger='1 semana sem ativar cartão ou multiconta — Prevenção · Valor',
         campos=[dict(label='Assunto', value='Cartão e multiconta, prontos para usar')],
         corpo='Compras, saldos e conversões em outras moedas, direto do app.', emailId='v1-03-prevencao-valor-d7'),
    dict(fase='engajamento', canal='push', dia='D7', trigger='7 dias sem transação (cliente já ativado)',
         campos=[dict(label='Título', value='Sua conta segue disponível')], corpo='Converta, envie ou use o cartão quando quiser.'),
    dict(fase='engajamento', canal='email', dia='D14', trigger='14 dias sem transação',
         campos=[dict(label='Assunto', value='Por onde começar na sua conta Zeom')],
         corpo='Sua conta permanece pronta para acompanhar suas movimentações.', emailId='v1-04-engajamento-d14'),
    dict(fase='engajamento', canal='push', dia='D21', trigger='21 dias sem transação — fechamento da régua',
         campos=[dict(label='Título', value='No seu ritmo')], corpo='Um Pix é suficiente para voltar a movimentar sua conta.'),
    dict(fase='oportunidades', canal='push', dia='Evento', trigger='Variação cambial — hoje manual, futuramente automatizado',
         campos=[dict(label='Título', value='Cotações atualizadas no app')],
         corpo='Dólar, euro e outras moedas, sempre visíveis na sua conta.'),
    dict(fase='oportunidades', canal='email', dia='Evento', trigger='Variação cambial — versão neutra, sem gatilho de urgência',
         campos=[dict(label='Assunto', value='Câmbio, de forma simples')],
         corpo='Consulte cotações de diferentes moedas e acompanhe o mercado pela sua conta.', emailId='v1-05-oportunidades-cambio'),
    dict(fase='churn', canal='push', dia='A detalhar', trigger='Inativo por longo período / esgotou qualquer régua de prevenção',
         campos=[dict(label='Título', value='Tudo pronto quando você voltar')],
         corpo='Sua conta segue ativa, com seus dados e saldos preservados.', status=PROPOSTA),
    dict(fase='churn', canal='email', dia='A detalhar', trigger='Inativo por longo período / esgotou qualquer régua de prevenção · assinado Equipe Zeom',
         campos=[dict(label='Assunto', value='Sua conta Zeom está do jeito que você deixou')],
         corpo='Veja o que segue disponível e conte como podemos melhorar.', emailId='v1-06-churn-win-back', status=PROPOSTA),
]

# fluxograma (viewBox 900 × H) — espinha em x=260, desvios em x=650
H = 740
FLOW_LINES = '''
  <defs>
    <marker id="arGray" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#8A97A8"/></marker>
    <marker id="arAmber" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#C98A00"/></marker>
  </defs>
  <line x1="260" y1="63"  x2="260" y2="100" stroke="#8A97A8" stroke-width="1.6" marker-end="url(#arGray)"/>
  <line x1="260" y1="195" x2="260" y2="240" stroke="#8A97A8" stroke-width="1.6" marker-end="url(#arGray)"/>
  <line x1="260" y1="335" x2="260" y2="383" stroke="#8A97A8" stroke-width="1.6" marker-end="url(#arGray)"/>
  <line x1="260" y1="452" x2="260" y2="500" stroke="#8A97A8" stroke-width="1.6" marker-end="url(#arGray)"/>
  <line x1="260" y1="595" x2="260" y2="650" stroke="#8A97A8" stroke-width="1.6" marker-end="url(#arGray)"/>
  <line x1="305" y1="150" x2="505" y2="150" stroke="#D9A420" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#arAmber)"/>
  <line x1="305" y1="290" x2="515" y2="290" stroke="#D9A420" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#arAmber)"/>
  <line x1="305" y1="550" x2="515" y2="550" stroke="#B3AD98" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#arGray)"/>
'''
FLOW_NODES = '''
addNode({x:260, y:40,  w:240, h:46, cls:'hex', label:'Início · cliente com conta ativa'});
addNode({x:260, y:150, w:90,  h:90, cls:'diamond', label:'Usou cartão, multiconta e investimentos?'});
addNode({x:260, y:290, w:90,  h:90, cls:'diamond', label:'Transacionou nos últimos 7 dias?'});
addNode({x:260, y:420, w:360, h:64, cls:'n-ong', label:FASES.oportunidades.nome, faseKey:'oportunidades', extraLabel:'Gatilho de mercado'});
addNode({x:260, y:550, w:90,  h:90, cls:'diamond', label:'Continua engajado?'});
addNode({x:260, y:680, w:220, h:50, cls:'end-node', label:'✓ Cliente ativo'});
addNode({x:650, y:150, w:290, h:100, cls:'n-pre', label:FASES.ativacao.nome, faseKey:'ativacao', sequence:true});
addNode({x:650, y:290, w:270, h:92,  cls:'n-pre', label:FASES.engajamento.nome, faseKey:'engajamento', sequence:true});
addNode({x:650, y:550, w:270, h:64,  cls:'n-churn', label:FASES.churn.nome, faseKey:'churn'});
[[405,138],[405,278],[405,538]].forEach(([lx,ly]) => {
  const lbl = document.createElement('div');
  lbl.className = 'flabel-not';
  lbl.style.left = (lx/900*100)+'%';
  lbl.style.top = (ly/H*100)+'%';
  lbl.textContent = 'não';
  flowWrap.appendChild(lbl);
});

'''

EXTRA_CSS = f'''
  .flow-wrap{{padding-bottom:{H / 900 * 100:.2f}%;}}
  .fnode.n-churn{{background:var(--churn-bg); color:#6B6656; border-color:#BFBA99;}}
  .status-pill{{font-size:10px; font-weight:800; letter-spacing:.4px; color:#8A5A00; background:#FFF4DB; border:1px solid #F2D58A; padding:2px 8px; border-radius:20px; white-space:nowrap;}}
  .back-link{{display:inline-block; margin-bottom:18px; font-size:12.5px; font-weight:600; color:var(--muted); text-decoration:none;}}
  .back-link:hover{{color:var(--ink);}}
'''


def sub(pattern, repl, text, count=1, flags=re.S):
    out, n = re.subn(pattern, lambda m: repl, text, count=count, flags=flags)
    assert n, f'padrão não encontrado: {pattern[:60]}'
    return out


def replace_between(text, start, end, repl):
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + repl + text[b:]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = emails.build()
    for new, old in REUSED.items():
        src = (ROOT / 'emails/reguas' / old).read_text()
        for before, after in COPY_EDITS.get(new, []):
            assert before in src, before
            src = src.replace(before, after)
        files[new] = f'<!-- Régua V1 · cópia de emails/reguas/{old} (com os ajustes de COPY_EDITS) -->\n' + src
    for name, html in files.items():
        (OUT_DIR / name).write_text(html)

    templates = {name[:-5]: html.replace('../../assets/', SITE_ASSETS) for name, html in files.items()}
    subjects = {d['campos'][0]['value']: d['emailId'] for d in DATA if d.get('emailId')}
    for d in DATA:
        assert not d.get('emailId') or d['emailId'] in templates, d['emailId']

    s = (ROOT / 'comunicacoes-zeom.html').read_text()

    # head
    s = sub(r'<title>[^<]*</title>', '<title>Régua V1 · Zeom</title>', s)
    s = s.replace('</style>', EXTRA_CSS + '</style>', 1)

    # cabeçalho, legenda, rodapé
    s = sub(r'<h1>Comunicações <span class="z">Zeom</span></h1>', '<h1>Régua <span class="z">V1</span></h1>', s)
    s = sub(r'<p class="sub">.*?</p>',
            '<p class="sub">Comunicações da V1, separadas da régua atual: valor &amp; repescagem, engajamento de clientes já ativados, '
            'oportunidades de mercado e win back. Clique numa etapa e em "Ver mais" para ver o texto e o e-mail montado.</p>', s)
    assert '<header>' in s
    s = s.replace('<header>', '<header>\n    <a class="back-link" href="index-projeto.html">← Índice do projeto</a>', 1)
    s = sub(r'<div class="flow-legend">.*?</div>',
            '<div class="flow-legend">\n'
            '      <span><span class="sw" style="background:#5B6B7A;"></span>Início</span>\n'
            '      <span><span class="sw" style="background:var(--pre);"></span>Prevenção</span>\n'
            '      <span><span class="sw" style="background:var(--ong);"></span>Ongoing</span>\n'
            '      <span><span class="sw" style="background:var(--churn);"></span>Churn</span>\n'
            '      <span><span class="sw" style="background:#F6C244; border:1px solid #D9A420;"></span>Decisão</span>\n'
            '    </div>', s)
    s = sub(r'<footer>.*?</footer>', '<footer>Zeom · Régua V1 · Momento Zero</footer>', s)

    # dados embutidos
    s = sub(r'(<script type="application/json" id="email-templates-data">).*?(</script>)',
            '<script type="application/json" id="email-templates-data">' + json.dumps(templates, ensure_ascii=False).replace('</', '<\\/') + '</script>', s)
    s = sub(r'(<script type="application/json" id="email-subjects-data">).*?(</script>)',
            '<script type="application/json" id="email-subjects-data">' + json.dumps(subjects, ensure_ascii=False) + '</script>', s)

    # script principal
    s = replace_between(s, 'const FASES = {', '\n};', 'const FASES = ' + json.dumps(FASES, ensure_ascii=False, indent=2)[:-1])
    s = replace_between(s, 'const DATA = [', '\n];', 'const DATA = ' + json.dumps(DATA, ensure_ascii=False, indent=1)[:-2])
    s = s.replace('\n// ---------- render stage 1 (flowchart) ----------', f'\nconst H = {H};\n// ---------- render stage 1 (flowchart) ----------', 1)
    s = replace_between(s, '\n  <defs>', '\n`;\nflowWrap.innerHTML', FLOW_LINES.rstrip('\n'))
    s = s.replace('viewBox 0 0 900 1370', 'viewBox 0 0 900 H')
    s = s.replace('<svg viewBox="0 0 900 1370"', '<svg viewBox="0 0 900 ${H}"')
    s = s.replace('(y/1370*100)', '(y/H*100)').replace('(h/1370*100)', '(h/H*100)')
    s = replace_between(s, '// main spine', '// ---------- stage navigation', FLOW_NODES)
    s = s.replace("const isV1 = item.prioridade === 'V1';", 'const isV1 = false;')
    s = s.replace("${isV1 ? '<span class=\"v1-pill\">V1 · futuro</span>' : ''}",
                  "${item.status ? '<span class=\"status-pill\">' + item.status + '</span>' : ''}")
    s = s.replace("({onb:'#2B6EF5',pre:'#9A6B00',exp:'#7C4DFF',ong:'#0A7A6C'})", "({onb:'#2B6EF5',pre:'#9A6B00',exp:'#7C4DFF',ong:'#0A7A6C',churn:'#6B6656'})")
    main_js = s[s.rindex('<script>'):]
    for leftover in ['/1370', '0 900 1370', 'V1 · futuro', "prioridade === 'V1'", 'e01-onboarding']:
        assert leftover not in main_js, leftover

    (ROOT / 'regua-v1.html').write_text(s)
    print(f'{len(files)} e-mails → {OUT_DIR.relative_to(ROOT)}/ · regua-v1.html {len(s) // 1024} KB')


if __name__ == '__main__':
    main()
