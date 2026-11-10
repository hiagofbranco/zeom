"""Aplica em comunicacoes-v0-v1.html as decisões do time (planilha de feedback, 10/11/2026).

Roda uma vez sobre a página com as 76 comunicações originais:
  - dá a cada comunicação o ID usado na planilha (ONB-01, ENG-06…) e mostra na página;
  - remove, move e altera comunicações conforme a coluna Decisão/Observações;
  - atualiza os e-mails embutidos e os arquivos em emails/reguas/v1;
  - recalcula as marcas de atenção (regua-v1/alertas.py).
Uso: python3 regua-v1/decisoes.py
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import alertas  # noqa: E402
from alertas import it, algum  # noqa: E402

PAGE = ROOT / 'comunicacoes-v0-v1.html'
OUT_JSON = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None

PREFIX = {'onboarding': 'ONB', 'aquisicao': 'AQU', 'kyc': 'KYC', 'semana1': 'SM1', 'engajamento': 'ENG', 'semana2': 'SM2',
          'semana3': 'SM3', 'valor': 'VAL', 'oportunidades': 'ONG', 'churn': 'CHU'}

PROMO_VELHO = '* Promoção por tempo limitado. Consulte as condições no app. [TEXTO PROVISÓRIO — definir o rodapé oficial da taxa zero]'
PROMO_NOVO = '* Promoção válida até 30/11/2026. Consulte as condições no app.'

# textos entregues pelo time (Observações da planilha)
KYC13_TITULO = 'Aproveite câmbio sem IOF e use cartão internacional'
KYC13_TEXTO = 'Em sua conta Zeom aproveite o dólar sem IOF e use seu cartão já em dólar para efetuar compras internacionais.'
ENG06_TITULO = 'Deposite hoje e desfrute a conta global Zeom'
ENG06_TEXTO = 'Faça seu depósito e comece a viver o novo jeito de pensar, investir e usar o dinheiro globalmente.'


def carregar(a):
    di = a.index('const DATA = ['); dj = a.index('\n];', di) + 3
    fi = a.index('const FASES = {'); fj = a.index('\n};', fi) + 3
    ei = a.index('const EMAILS = {'); ej = a.index('};', ei) + 2
    DATA = json.loads(a[di + len('const DATA = '):dj].rstrip().rstrip(';'))
    FASES = json.loads(a[fi + len('const FASES = '):fj].rstrip().rstrip(';'))
    EMAILS = json.loads(a[ei + len('const EMAILS = '):ej].rstrip().rstrip(';'))
    return DATA, FASES, EMAILS


def achar(DATA, fn, n=1):
    r = [x for x in DATA if fn(x)]
    assert len(r) == n, (n, len(r), [(x['id'], x['ver'], x['canal'], x['dia']) for x in r])
    return r


def main():
    a = PAGE.read_text(encoding='utf-8')
    assert 'idchip' not in a, 'decisões já aplicadas'
    DATA, FASES, EMAILS = carregar(a)
    assert len(DATA) == 76, len(DATA)

    # 1) IDs da planilha (ordem original)
    cont = {}
    for x in DATA:
        p = PREFIX[x['fase']]; cont[p] = cont.get(p, 0) + 1
        x['id'] = f'{p}-{cont[p]:02d}'
    original = {x['id']: json.loads(json.dumps(x)) for x in DATA}

    removidas, alteracoes = [], {}

    def remover(fn, n, motivo):
        for x in achar(DATA, fn, n):
            removidas.append(dict(id=x['id'], motivo=motivo))
            DATA.remove(x)

    def alterar(x, texto):
        alteracoes.setdefault(x['id'], []).append(texto)

    # 2) remoções
    remover(it('v0', 'onboarding', 'email', 'KYC ok', assunto='Sua conta está pronta'), 1, 'A15 · fica só a comunicação do CEO')
    remover(it('v0', 'engajamento', 'email', 'Sex (imediata)'), 1, 'A12 · remover ENG-02')
    remover(it('v0', 'engajamento', 'push', 'D7', 'Inatividade'), 1, 'A01 · ficam 1 push e 1 e-mail (V1)')
    remover(it('v0', 'engajamento', 'email', 'D14', 'Inatividade'), 1, 'A02 · ENG-11 passa a e-mail + push')
    remover(it('v0', 'kyc', 'email', 'D15'), 1, 'A05 · remover KYC-06')
    remover(it('v1', 'kyc', 'email', 'D+1 (B'), 1, 'Pendência 9 · sem ativações da calculadora')
    remover(it('v1', 'kyc', 'email', 'D+3'), 1, 'Pendência 9 · sem ativações da calculadora')
    remover(it('v0', 'valor', 'email', 'D7', 'Repescagem · Cartão'), 1, 'A08 · remover VAL-01')
    remover(it('v0', 'valor', 'email', 'D7', 'Prevenção · Valor'), 1, 'A08 · remover VAL-03')
    remover(it('v0', 'oportunidades', None, 'Evento'), 2, 'A11 · eliminar ONG-01 e ONG-02')
    remover(it('v1', 'churn', 'email', 'D+35'), 1, 'A14 · remover CHU-03')
    assert len(removidas) == 12

    # 3) alterações
    x = achar(DATA, it('v0', 'engajamento', 'push', 'Qua (imediata)'))[0]
    x['dia'] = '+1h'; x['trigger'] = '+1h — 1 hora depois do KYC aprovado, ainda sem depósito'
    alterar(x, 'A12 · passa a push 1 hora depois do KYC aprovado')

    x = achar(DATA, it('v1', 'kyc', 'email', 'D+1 (A'))[0]
    arquivo_kyc07 = x.pop('file')
    x['canal'] = 'push'; x['dia'] = 'D+1'
    x['trigger'] = 'D+1 · cadastro existe, falta concluir o KYC (sign up do app)'
    x['campos'] = [{'label': 'Título', 'value': 'Sua verificação de identidade'}]
    x['corpo'] = 'A etapa de verificação continua disponível para concluir sua abertura de conta.'
    alterar(x, 'A04 · muda de e-mail para push (título e texto reaproveitados do e-mail)')

    x = achar(DATA, it('v1', 'kyc', 'email', 'D7'))[0]
    arquivo_kyc13 = x['file']
    x['campos'] = [{'label': 'Assunto', 'value': KYC13_TITULO}]; x['corpo'] = KYC13_TEXTO
    alterar(x, 'A06 · texto novo entregue pelo time')

    x = achar(DATA, it('v1', 'engajamento', 'push', 'D+1', '1º depósito'))[0]
    x['campos'] = [{'label': 'Título', 'value': ENG06_TITULO}]; x['corpo'] = ENG06_TEXTO
    alterar(x, 'A13 · título e conteúdo novos entregues pelo time (corrigido "começe" para "comece")')

    x = achar(DATA, it('v1', 'engajamento', 'push', 'D+3', '1º depósito'))[0]
    x['campos'] = [{'label': 'Título', 'value': KYC13_TITULO}]; x['corpo'] = KYC13_TEXTO
    alterar(x, 'A12 · título e conteúdo novos entregues pelo time (mesmo texto da A06)')

    x = achar(DATA, it('v0', 'kyc', 'email', 'D6'))[0]
    x['trigger'] = x['trigger'] + ' — 1ª tentativa de conclusão'; alterar(x, 'A05 · mantido como 1ª tentativa')
    x = achar(DATA, it('v1', 'kyc', 'email', 'D14'))[0]
    x['trigger'] = 'D14 · 2ª tentativa de conclusão (conteúdo do D6 da V0)'; alterar(x, 'A05 · mantido como 2ª tentativa')
    x = achar(DATA, it('v1', 'kyc', 'email', 'D21'))[0]
    x['trigger'] = 'D21 · fechamento da régua com pesquisa de abandono (era o D15 da V0)'; alterar(x, 'A05 · passa a fechamento com pesquisa')

    x = achar(DATA, it('v1', 'churn', 'push', 'D+30'))[0]
    x['fase'] = 'oportunidades'; x['sub'] = 'Win back'; x['dia'] = 'D+45'
    x['trigger'] = 'D+45 · inativo, sem saldo · win back · status Zeom: Pendente'; alterar(x, 'A14 · Churn → Ongoing em D+45')
    x = achar(DATA, it('v1', 'churn', 'email', 'D+30'))[0]
    x['fase'] = 'oportunidades'; x['sub'] = 'Win back'; x['dia'] = 'D+60'
    x['trigger'] = 'D+60 · inativo, sem saldo · win back · status Zeom: Pendente'; alterar(x, 'A14 · Churn → Ongoing em D+60')

    # ENG-11 passa a e-mail + push
    e11 = achar(DATA, it('v1', 'engajamento', 'email', 'D14', 'Inatividade'))[0]
    push11 = dict(fase='engajamento', canal='push', dia='D14', sub='Inatividade', ver='v1', id='ENG-13',
                  trigger='D14 · sem atividade no app (junto do e-mail) · status Zeom: Pendente',
                  campos=[{'label': 'Título', 'value': 'Por onde começar na sua conta Zeom'}],
                  corpo='Acesse sua conta e acompanhe as opções para a gestão dos seus recursos.')
    DATA.insert(DATA.index(e11) + 1, push11)
    alterar(e11, 'A02 · passa a e-mail + push (novo push ENG-13)')
    alterar(push11, 'A02 · push novo (título e texto reaproveitados do e-mail)')

    # 4) e-mails (HTML)
    def promo(html):
        assert PROMO_VELHO in html
        return html.replace(PROMO_VELHO, PROMO_NOVO)

    def kyc13(html):
        old = 'Conclua sua verificação e tenha acesso ao câmbio com taxa zero, por tempo limitado.*'
        assert html.count(old) == 2 and 'Câmbio com taxa zero na Zeom' in html
        html = html.replace(old, KYC13_TEXTO).replace('Câmbio com taxa zero na Zeom', KYC13_TITULO)
        html, n = re.subn(r'<tr><td[^>]*><p[^>]*>\* Promoção por tempo limitado\.[^<]*</p></td></tr>', '', html)
        assert n == 1, n
        return html

    editar = {arquivo_kyc13: kyc13}
    for x in DATA:
        if x.get('file') and PROMO_VELHO in EMAILS.get(x['file'], '') and x['file'] != arquivo_kyc13:
            editar[x['file']] = promo
    for f, fn in editar.items():
        EMAILS[f] = fn(EMAILS[f])
        p = ROOT / f
        if p.exists():
            p.write_text(fn(p.read_text(encoding='utf-8')), encoding='utf-8')

    # arquivos de e-mails que deixaram de existir
    sem_uso = {arquivo_kyc07}
    for r in removidas:
        o = original[r['id']]
        if o.get('file'):
            sem_uso.add(o['file'])
    usados = {x['file'] for x in DATA if x.get('file')}
    for f in sorted(sem_uso - usados):
        EMAILS.pop(f, None)
        p = ROOT / f
        # os e-mails originais da régua V0 (usados por outras páginas) ficam no repositório
        if p.exists() and f.startswith('emails/reguas/v1/') or f in ('emails/reguas/v0/13-repescagem-cartao.html', 'emails/reguas/v0/15-prevencao-valor.html'):
            if p.exists():
                p.unlink()

    # 5) etapas e fluxograma
    del FASES['churn']
    FASES['oportunidades']['desc'] = 'Variação cambial, novos serviços, investidores e win back · V0 + V1'
    assert 'churn' not in {x['fase'] for x in DATA}

    def sub1(s, old, new):
        assert old in s, old[:60]
        return s.replace(old, new, 1)
    a = sub1(a, "addNode({x:650, y:845, w:260, h:64, cls:'n-churn', label:FASES.churn.nome, faseKey:'churn'});\n", '')
    a = sub1(a, '  <line x1="305" y1="845" x2="520" y2="845" stroke="#B3AD98" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#arGray)"/>\n', '')
    a = sub1(a, "['não','não','não','parou','não'].forEach", "['não','não','não','parou'].forEach")
    a = sub1(a, '[[420,197],[420,275],[420,432],[480,640],[420,832]]', '[[420,197],[420,275],[420,432],[480,640]]') if '[[420,197],[420,275],[420,432],[480,640],[420,832]]' in a else a

    # 6) grava
    def bloco(a, ini, fim, novo):
        i = a.index(ini); j = a.index(fim, i) + len(fim)
        return a[:i] + novo + a[j:]
    a = bloco(a, 'const FASES = {', '\n};', 'const FASES = ' + json.dumps(FASES, ensure_ascii=False, indent=1) + ';')
    a = bloco(a, 'const DATA = [', '\n];', 'const DATA = ' + json.dumps(DATA, ensure_ascii=False, indent=1) + ';')
    ei = a.index('const EMAILS = {'); ej = a.index('};', ei) + 2
    a = a[:ei] + 'const EMAILS = ' + json.dumps(EMAILS, ensure_ascii=False) + ';' + a[ej:]
    PAGE.write_text(a, encoding='utf-8')
    alertas.aplicar()
    if OUT_JSON:
        OUT_JSON.write_text(json.dumps(dict(removidas=removidas, alteracoes=alteracoes, original=original), ensure_ascii=False), encoding='utf-8')
    print('comunicações:', len(DATA), '· removidas:', len(removidas), '· e-mails embutidos:', len(EMAILS))


if __name__ == '__main__':
    main()
