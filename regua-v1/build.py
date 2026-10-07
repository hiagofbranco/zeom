#!/usr/bin/env python3
"""Gera a Régua V1 separada, a partir da planilha "Revisão Régua CRM para Implementação V1":
  - emails/reguas-v1/*.html  (e-mails novos de emails.py + cópias dos e-mails da V0 que a planilha reaproveita)
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

# e-mails V0 que a planilha manda reaproveitar (cópia em emails/reguas-v1/, original intacto)
REUSED = {
    'kyc-06-fechamento-d14.html': '07-prevencao-kyc-d6-fechamento.html',
    'kyc-07-pesquisa-d21.html': '08-prevencao-kyc-d15-pesquisa.html',
    'eng-02-inatividade-d14.html': '11-prevencao-engajamento-d14.html',
}

# ajustes de copy aplicados só na cópia V1
COPY_EDITS = {
    'kyc-07-pesquisa-d21.html': [
        ('h%C3%A1%2015%20dias', 'h%C3%A1%2021%20dias'),
    ],
    'eng-02-inatividade-d14.html': [
        ('<title>Zeom · Seus recursos continuam disponíveis</title>', '<title>Zeom · Por onde começar na sua conta Zeom</title>'),
        ('>A sua conta Zeom permanece ativa', '>{{first_name}}, a sua conta Zeom permanece ativa'),
        ('porque sua conta Zeom está inativa há 14 dias', 'porque sua conta Zeom está sem movimentações há 14 dias'),
    ],
}

FASES = {
    'kyc': dict(nome='Prevenção · KYC', classe='pre',
                desc='Leads da calculadora do site + cadastro sem KYC concluído · cupom Taxa Zero no D5/D7 · fechamento D10/D14 · pesquisa D21'),
    'deposito': dict(nome='Engajamento · 1º depósito', classe='pre',
                     desc='Abriu a conta e não depositou · reforço por push e Pix gerado sem pagamento'),
    'cartao': dict(nome='Repescagem · Cartão', classe='exp',
                   desc='Régua própria, priorizada (pedido do André) · abriu a conta e não ativou o cartão'),
    'valor': dict(nome='Prevenção · Valor', classe='onb',
                  desc='Cartão ativado sem saldo na conta cartão e incentivo após cada Pix'),
    'multiconta': dict(nome='Repescagem · Multiconta', classe='exp',
                       desc='Abriu a conta e não ativou as contas virtuais em dólar e euro'),
    'investimento': dict(nome='Repescagem · Investimento', classe='exp',
                         desc='Régua própria, priorizada (pedido do André) · dinheiro parado em conta corrente'),
    'ongoing': dict(nome='Ongoing', classe='ong',
                    desc='Variação cambial, novos serviços e novos aportes ou depósitos de investidores'),
    'inatividade': dict(nome='Engajamento · Inatividade', classe='pre',
                        desc='Cliente ativado sem qualquer atividade no app · 7, 14 e 21 dias'),
    'churn': dict(nome='Churn', classe='churn',
                  desc='Win Back no D+30 (sem saldo em conta) e pesquisa "Battle is lost" no D+35 · assinados pela Equipe Zeom'),
}

CUPOM = 'Cupom · validar regras'
COMPLIANCE = 'Validar com compliance'


def push(fase, dia, trigger, titulo, texto, status=None):
    d = dict(fase=fase, canal='push', dia=dia, trigger=trigger, campos=[dict(label='Título', value=titulo)], corpo=texto)
    if status:
        d['status'] = status
    return d


def mail(fase, dia, trigger, file, status=None):
    d = dict(fase=fase, canal='email', dia=dia, trigger=trigger, emailId=file[:-5])
    if status:
        d['status'] = status
    return d


DATA = [
    mail('kyc', 'D+1', 'Lead da calculadora do site · cadastro já existe, falta baixar o app e fazer o KYC', 'kyc-01-lead-d1.html', 'Depende da calculadora'),
    mail('kyc', 'D+3', 'Lead da calculadora do site · 3 dias depois, ainda sem KYC', 'kyc-02-lead-d3.html', 'Depende da calculadora'),
    push('kyc', 'D5', '5 dias sem concluir o KYC', 'Taxa zero no primeiro câmbio', 'Conclua sua verificação e use o cupom na primeira conversão.', CUPOM),
    mail('kyc', 'D5', '5 dias sem concluir o KYC (junto do push)', 'kyc-03-cupom-d5.html', CUPOM),
    push('kyc', 'D7', '7 dias sem concluir o KYC · lembrete do cupom', 'Cupom taxa zero até {{CUPOM_validade}}', 'Conclua a verificação para usar na primeira conversão.', CUPOM),
    mail('kyc', 'D7', '7 dias sem concluir o KYC (junto do push)', 'kyc-04-cupom-d7.html', CUPOM),
    mail('kyc', 'D10', '10 dias sem concluir o KYC · fechamento 1, assinado Equipe Zeom', 'kyc-05-fechamento-d10.html'),
    mail('kyc', 'D14', '14 dias sem concluir o KYC · fechamento final (conteúdo do D6 da V0)', 'kyc-06-fechamento-d14.html'),
    mail('kyc', 'D21', 'Fora da régua ativa · pesquisa de abandono (era o D15 da V0)', 'kyc-07-pesquisa-d21.html'),

    push('deposito', 'D+1', 'Abriu a conta e não fez depósito', 'Sua conta está pronta', 'Faça um Pix para começar a usar sua conta em dólar.'),
    push('deposito', 'D+3', 'Abriu a conta e não fez depósito · 3 dias', 'Comece com um Pix', 'Adicione saldo e converta para dólar com a cotação visível.', 'Taxa zero no 1º mês · ver com Perillo/Dani'),
    push('deposito', '+2 min', 'Gerou um Pix para depositar e não pagou', 'Seu Pix está aguardando', 'Conclua o pagamento antes de o QR Code expirar.'),

    push('cartao', 'D+1', 'Abriu a conta e não ativou o cartão', 'Ative seu cartão em dólar', 'Ative pelo app e use o saldo em dólar nas compras no exterior.'),
    push('cartao', 'D+3', 'Abriu a conta e não ativou o cartão · 3 dias', 'Cartão ativo em poucos passos', 'Abra o app, confirme seus dados e crie a senha.'),
    mail('cartao', 'D+7', 'Abriu a conta e não ativou o cartão · 7 dias', 'cartao-01-ativar-d7.html'),
    mail('cartao', 'D+21', 'Abriu a conta e não ativou o cartão · 21 dias', 'cartao-02-usos-d21.html'),

    push('valor', 'D+0', 'Cartão ativado, sem saldo na conta cartão', 'Cartão ativado', 'Adicione saldo à conta do cartão para começar a usar.'),
    push('valor', 'D+7', 'Conta cartão sem saldo · 7 dias', 'Saldo para o seu cartão', 'Transfira do seu saldo em dólar para a conta do cartão.'),
    push('valor', 'D+14', 'Conta cartão sem saldo · 14 dias', 'Cartão pronto para a próxima compra', 'Recarregue a conta do cartão pelo app, com a cotação visível.'),
    push('valor', 'Após cada Pix', 'Pix concluído · no máximo 1 por semana', 'Pix recebido na sua conta', 'Agora você pode converter, investir ou usar no cartão.'),

    push('multiconta', 'D+1', 'Abriu a conta e não ativou a multiconta', 'Dólar e euro na mesma conta', 'Ative suas contas em moedas para receber e transferir no exterior.'),
    push('multiconta', 'D+3', 'Abriu a conta e não ativou a multiconta · 3 dias', 'Receba em dólar ou euro', 'Com a multiconta, você tem uma conta virtual em cada moeda.'),
    mail('multiconta', 'D+7', 'Sem ativar a multiconta · 7 dias', 'mc-01-ativar-d7.html'),
    mail('multiconta', 'D+21', 'Sem ativar a multiconta · 21 dias', 'mc-02-usos-d21.html'),

    push('investimento', 'D+1', 'Dinheiro parado em conta corrente', 'Seu saldo pode ser investido', 'O valor investido fica disponível para resgate quando você precisar.', COMPLIANCE),
    push('investimento', 'D+3', 'Dinheiro parado em conta corrente · 3 dias', 'Investir sem travar seu dinheiro', 'Resgate quando precisar, 24 horas por dia, direto no app.', COMPLIANCE),

    push('ongoing', 'Evento', 'Queda relevante do dólar (limiar a definir) — hoje manual, futuramente automatizado', 'O dólar recuou hoje', 'Veja a cotação atualizada no app antes de converter.', COMPLIANCE),
    mail('ongoing', 'Evento', 'Queda relevante do dólar (limiar a definir)', 'ong-01-dolar-recuou.html', COMPLIANCE),
    mail('ongoing', 'Lançamento', 'Novo serviço ou produto da Zeom', 'ong-02-novo-servico.html', 'Modelo'),
    push('ongoing', 'D+30', 'Investidor com saldo ocioso em conta', 'Saldo disponível para investir', 'Você tem saldo parado na conta. Veja as opções no app.'),
    mail('ongoing', 'D+30', 'Investidor com saldo ocioso em conta (junto do push)', 'ong-03-novos-aportes-d30.html'),
    push('ongoing', 'D+30', 'Investidor sem novos depósitos', 'Novo aporte, no seu ritmo', 'Adicione saldo e invista o valor que fizer sentido para você.'),
    mail('ongoing', 'D+30', 'Investidor sem novos depósitos (junto do push)', 'ong-04-novos-depositos-d30.html'),

    push('inatividade', 'D7', '7 dias sem qualquer atividade no app', 'Tudo certo na sua conta', 'Saldo, cartão e cotações a um toque, no app.'),
    mail('inatividade', 'D7', '7 dias sem qualquer atividade no app (junto do push)', 'eng-01-inatividade-d7.html'),
    mail('inatividade', 'D14', '14 dias sem qualquer atividade no app', 'eng-02-inatividade-d14.html'),
    mail('inatividade', 'D21', '21 dias sem atividade · fechamento + cupom no próximo depósito', 'eng-03-fechamento-d21.html', CUPOM),

    push('churn', 'D+30', 'Inativo há 30 dias, sem saldo em conta / esgotou qualquer prevenção', 'Tudo pronto quando você voltar', 'Sua conta segue ativa, com seus dados preservados.'),
    mail('churn', 'D+30', 'Win Back · inativo há 30 dias, sem saldo em conta (junto do push)', 'churn-01-win-back-d30.html'),
    mail('churn', 'D+35', 'Battle is lost · não tenta reconverter, só entender o que houve', 'churn-02-pesquisa-d35.html'),
]

# fluxograma: espinha em x=260, desvios em x=650 · (tipo, rótulo, fase ligada, rótulo da seta)
FLOW = [
    ('hex', 'Início · cadastro ou lead do site', None, None),
    ('diamond', 'Concluiu o KYC?', 'kyc', 'não'),
    ('diamond', 'Fez o 1º depósito?', 'deposito', 'não'),
    ('diamond', 'Ativou o cartão?', 'cartao', 'não'),
    ('node', None, 'valor', None),
    ('diamond', 'Ativou a multiconta?', 'multiconta', 'não'),
    ('diamond', 'Tem dinheiro parado?', 'investimento', 'sim'),
    ('node', None, 'ongoing', None),
    ('diamond', 'Ativo nos últimos 7 dias?', 'inatividade', 'não'),
    ('diamond', 'Voltou a usar?', 'churn', 'não'),
    ('end', '✓ Cliente ativo', None, None),
]
SIZES = {'hex': (260, 46), 'diamond': (90, 90), 'node': (360, 64), 'end': (220, 50)}
HALF = {'hex': 23, 'diamond': 64, 'node': 32, 'end': 25}
GAP = 34
LABELS_JS = """
%s.forEach(([lx, ly, t]) => {
  const lbl = document.createElement('div');
  lbl.className = 'flabel-not';
  lbl.style.left = (lx/900*100)+'%%';
  lbl.style.top = (ly/H*100)+'%%';
  lbl.textContent = t;
  flowWrap.appendChild(lbl);
});

"""


def flow():
    lines, nodes, labels = [], [], []
    y = 40
    for i, (kind, label, fase, arrow) in enumerate(FLOW):
        w, h = SIZES[kind]
        if i:
            pk = FLOW[i - 1][0]
            lines.append(f'<line x1="260" y1="{prev_y + HALF[pk]}" x2="260" y2="{y - HALF[kind] - 4}" stroke="#8A97A8" stroke-width="1.6" marker-end="url(#arGray)"/>')
        if kind == 'node':
            nodes.append(f"addNode({{x:260, y:{y}, w:{w}, h:{h}, cls:'n-{FASES[fase]['classe']}', label:FASES.{fase}.nome, faseKey:'{fase}'}});")
        else:
            cls = {'hex': 'hex', 'diamond': 'diamond', 'end': 'end-node'}[kind]
            nodes.append(f"addNode({{x:260, y:{y}, w:{w}, h:{h}, cls:'{cls}', label:{json.dumps(label, ensure_ascii=False)}}});")
        if kind == 'diamond':
            sw = 290
            color, marker = ('#B3AD98', 'arGray') if FASES[fase]['classe'] == 'churn' else ('#D9A420', 'arAmber')
            lines.append(f'<line x1="324" y1="{y}" x2="{650 - sw // 2 - 5}" y2="{y}" stroke="{color}" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#{marker})"/>')
            nodes.append(f"addNode({{x:650, y:{y}, w:{sw}, h:72, cls:'n-{FASES[fase]['classe']}', label:FASES.{fase}.nome, faseKey:'{fase}'}});")
            labels.append([415, y - 12, arrow])
        prev_y = y
        if i + 1 < len(FLOW):
            y += HALF[kind] + GAP + HALF[FLOW[i + 1][0]]
    height = y + HALF[FLOW[-1][0]] + 30
    svg = ('\n  <defs>\n'
           '    <marker id="arGray" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#8A97A8"/></marker>\n'
           '    <marker id="arAmber" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#C98A00"/></marker>\n'
           '  </defs>\n  ' + '\n  '.join(lines))
    js = '\n' + '\n'.join(nodes) + LABELS_JS % json.dumps(labels, ensure_ascii=False)
    return svg, js, height


FLOW_LINES, FLOW_NODES, H = flow()

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


def meta_of(html):
    subject = re.search(r'<title>Zeom · (.*?)</title>', html).group(1)
    pre = re.search(r'<div style="display:none[^>]*>(.*?)(?:&nbsp;|</div>)', html, re.S).group(1).strip()
    return subject, pre


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = emails.build()
    for new, old in REUSED.items():
        src = (ROOT / 'emails/reguas' / old).read_text()
        for before, after in COPY_EDITS.get(new, []):
            assert before in src, before
            src = src.replace(before, after)
        files[new] = f'<!-- Régua V1 · cópia de emails/reguas/{old} (com os ajustes de COPY_EDITS) -->\n' + src
    for stale in OUT_DIR.glob('*.html'):
        if stale.name not in files:
            stale.unlink()
    for name, html in files.items():
        (OUT_DIR / name).write_text(html)

    templates = {name[:-5]: html.replace('../../assets/', SITE_ASSETS) for name, html in files.items()}
    for d in DATA:
        if d['canal'] == 'email':
            subject, pre = meta_of(templates[d['emailId']])
            d['campos'] = [dict(label='Assunto', value=subject)]
            d['corpo'] = pre
    assert {d['emailId'] for d in DATA if d.get('emailId')} == set(templates), 'e-mail sem comunicação ou vice-versa'
    subjects = {}

    s = (ROOT / 'comunicacoes-zeom.html').read_text()

    # head
    s = sub(r'<title>[^<]*</title>', '<title>Régua V1 · Zeom</title>', s)
    s = s.replace('</style>', EXTRA_CSS + '</style>', 1)

    # cabeçalho, legenda, rodapé
    s = sub(r'<h1>Comunicações <span class="z">Zeom</span></h1>', '<h1>Régua <span class="z">V1</span></h1>', s)
    s = sub(r'<p class="sub">.*?</p>',
            '<p class="sub">Modernização da régua V0 para a V1, a partir da planilha de revisão: KYC com cupom, primeiro depósito, '
            'repescagens de cartão, multiconta e investimento, valor, ongoing, inatividade e churn. Clique numa etapa e em "Ver mais" '
            'para ver o texto e o e-mail montado.</p>', s)
    assert '<header>' in s
    s = s.replace('<header>', '<header>\n    <a class="back-link" href="index-projeto.html">← Índice do projeto</a>', 1)
    s = sub(r'<div class="flow-legend">.*?</div>',
            '<div class="flow-legend">\n'
            '      <span><span class="sw" style="background:#5B6B7A;"></span>Início</span>\n'
            '      <span><span class="sw" style="background:var(--pre);"></span>Prevenção · Engajamento</span>\n'
            '      <span><span class="sw" style="background:var(--exp);"></span>Repescagem</span>\n'
            '      <span><span class="sw" style="background:var(--onb);"></span>Valor</span>\n'
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
