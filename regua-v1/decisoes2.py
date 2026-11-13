"""Segunda rodada de decisões do time (Pendências 13 a 17 da planilha v2, 12-13/11/2026).

- A17: KYC-05 e KYC-15 seguem como estão (mesmo assunto).
- A18: D+7 e D+21 de cartão/multiconta viram 3 e-mails por segmento; cria VAL-18 (D+7) e VAL-19 (D+21)
       para quem não ativou nem o cartão nem a multiconta.
- A19: "sem IOF" confirmado pelo time.
- A20: ONB-05/ONB-07 imediatos; ENG-01 1 h depois do KYC, só se não houve depósito.
- ONB-07: André Bastos, CEO e Fundador da Zeom (retrato provisório com iniciais até chegar a foto).
Uso: python3 regua-v1/decisoes2.py [saida.json]
"""
import json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import alertas  # noqa: E402
import decisoes  # noqa: E402
from alertas import it  # noqa: E402

PAGE = ROOT / 'comunicacoes-v0-v1.html'
OUT_JSON = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
CEO_KEY = 'emails/reguas/v0/02-onboarding-boas-vindas-ceo.html'
VAL18 = 'emails/reguas/v1/VAL-18-d7-cartao-multiconta.html'
VAL19 = 'emails/reguas/v1/VAL-19-d21-cartao-multiconta.html'


def trocar(html, velho, novo, n=1):
    assert html.count(velho) == n, (velho[:70], html.count(velho))
    return html.replace(velho, novo)


def val19(base):
    h = base
    h = trocar(h, '<title>Onde usar seu cartão em dólar</title>', '<title>Dois jeitos de usar sua conta fora do Brasil</title>')
    h = trocar(h, '<!-- V1 · CAR-04 (D+21). -->', '<!-- V1 · VAL-19 (D+21): não ativou nem o cartão nem a multiconta. -->')
    h = trocar(h, 'Viagens, compras online e assinaturas internacionais.', 'Cartão em dólar e multiconta, para ativar quando quiser.', 2)
    h = trocar(h, '>Cartão</td>', '>Cartão e multiconta</td>')
    h = trocar(h, 'Onde usar seu cartão em dólar</h1>', 'Cartão e multiconta, no seu tempo</h1>')
    h = trocar(h, '>Viagens</p>', '>Cartão em dólar</p>')
    h = trocar(h, 'Use o saldo em dólar em compras presenciais no exterior.', 'Compras no exterior e em lojas virtuais internacionais, com o saldo em dólar.')
    h = trocar(h, '>Compras online</p>', '>Multiconta</p>')
    h = trocar(h, 'Pague em dólar em lojas virtuais internacionais.', 'Contas em dólar e euro para receber, enviar e guardar.')
    h = trocar(h, '>Assinaturas internacionais</p>', '>Sem prazo</p>')
    h = trocar(h, 'Serviços e assinaturas cobrados em dólar.', 'Ative cada um quando fizer sentido para você.')
    h = trocar(h, 'Ver meu cartão</a>', 'Ativar no app</a>')
    return h


def ceo(h):
    h = trocar(h, '[ imagem — retrato de André ]</p></td>',
               '</p><table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0"><tr>'
               '<td width="96" height="96" align="center" valign="middle" bgcolor="#21211C" '
               'style="width:96px;height:96px;border-radius:48px;background:#21211C;font-family:\'Instrument Sans\',Helvetica,Arial,sans-serif;'
               'font-weight:300;font-size:32px;letter-spacing:.06em;color:#CCC290;">AB</td></tr></table></td>')
    h = trocar(h, '>André</p>', '>André Bastos</p>')
    h = trocar(h, '[sobrenome e cargo — confirmar]', 'CEO e Fundador da Zeom')
    return h


def main():
    a = PAGE.read_text(encoding='utf-8')
    DATA, FASES, EMAILS = decisoes.carregar(a)
    assert not any(x['id'] == 'VAL-18' for x in DATA), 'segunda rodada já aplicada'
    n0 = len(DATA)
    alteracoes = {}

    def alt(x, t):
        alteracoes.setdefault(x['id'], []).append(t)

    # A18: segmentação do D+7 e do D+21
    seg = [('VAL-06', 'D+7 · não ativou o cartão', ' (já tem a multiconta ativa)'),
           ('VAL-14', 'D+7 · não ativou a multiconta', ' (já tem o cartão ativo)'),
           ('VAL-07', 'D+21 · não ativou o cartão', ' (já tem a multiconta ativa)'),
           ('VAL-15', 'D+21 · não ativou a multiconta', ' (já tem o cartão ativo)')]
    por_id = {x['id']: x for x in DATA}
    for i, base, suf in seg:
        x = por_id[i]; assert x['trigger'] == base, x['trigger']
        x['trigger'] = base + suf; alt(x, 'A18 · passa a valer só para quem já tem o outro recurso ativo')

    base_val18 = subprocess.run(['git', '-C', str(ROOT), 'show', '2c3ad79^:emails/reguas/v0/15-prevencao-valor.html'],
                                capture_output=True, text=True, check=True).stdout
    assert 'Seus recursos' in base_val18 and 'Acessar aplicativo' in base_val18
    v18 = dict(id='VAL-18', fase='valor', canal='email', dia='D+7', sub='Repescagem · Cartão + Multiconta', ver='v1',
               trigger='D+7 · não ativou nem o cartão nem a multiconta',
               campos=[{'label': 'Assunto', 'value': 'Seus recursos internacionais continuam por aqui'}],
               corpo='Cartão e multiconta, prontos para quando você quiser usar.', file=VAL18)
    v19 = dict(id='VAL-19', fase='valor', canal='email', dia='D+21', sub='Repescagem · Cartão + Multiconta', ver='v1',
               trigger='D+21 · não ativou nem o cartão nem a multiconta',
               campos=[{'label': 'Assunto', 'value': 'Dois jeitos de usar sua conta fora do Brasil'}],
               corpo='Cartão em dólar e multiconta, para ativar quando quiser.', file=VAL19)
    pos = DATA.index(por_id['VAL-15']) + 1
    DATA[pos:pos] = [v18, v19]
    alt(v18, 'A18 · e-mail novo (reaproveita o texto do antigo VAL-03, que era para este mesmo público)')
    alt(v19, 'A18 · e-mail novo, texto escrito para este público (baseado no layout do VAL-07/VAL-15)')

    cartao21 = (ROOT / 'emails/reguas/v1/CAR-04-d21-email.html').read_text(encoding='utf-8')
    EMAILS[VAL18] = base_val18
    EMAILS[VAL19] = val19(cartao21)
    (ROOT / VAL18).write_text(EMAILS[VAL18], encoding='utf-8')
    (ROOT / VAL19).write_text(EMAILS[VAL19], encoding='utf-8')

    # A20: ENG-01
    x = por_id['ENG-01']
    x['trigger'] = '+1h — 1 hora depois do KYC aprovado, só se ainda não fez o 1º depósito (se depositar antes, não recebe)'
    alt(x, 'A20 · só dispara se não houve depósito na primeira hora')

    # ONB-07: André Bastos
    EMAILS[CEO_KEY] = ceo(EMAILS[CEO_KEY])
    alt(por_id['ONB-07'], 'Pendência 17 · André Bastos, CEO e Fundador da Zeom (retrato provisório com iniciais)')

    def bloco(a, ini, fim, novo):
        i = a.index(ini); j = a.index(fim, i) + len(fim)
        return a[:i] + novo + a[j:]
    a = bloco(a, 'const DATA = [', '\n];', 'const DATA = ' + json.dumps(DATA, ensure_ascii=False, indent=1) + ';')
    ei = a.index('const EMAILS = {'); ej = a.index('};', ei) + 2
    a = a[:ei] + 'const EMAILS = ' + json.dumps(EMAILS, ensure_ascii=False) + ';' + a[ej:]
    PAGE.write_text(a, encoding='utf-8')
    alertas.aplicar()
    if OUT_JSON:
        OUT_JSON.write_text(json.dumps(dict(alteracoes=alteracoes), ensure_ascii=False), encoding='utf-8')
    print('comunicações:', n0, '->', len(DATA))


if __name__ == '__main__':
    main()
