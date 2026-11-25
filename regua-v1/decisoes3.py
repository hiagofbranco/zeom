"""Terceira rodada: notas de 17/11/2026 na aba Incoerências (planilha v2), que valem mais que as respostas
anteriores da aba Pendências.

- A17: mesma comunicação nas duas tentativas (já é assim).
- A18: e-mails de cartão e multiconta seguem a mesma regra de precedência dos pushes; VAL-18 e VAL-19 saem.
- A19: remover a promessa "sem IOF" (KYC-13 e ENG-07).
- A20: ONB-05 e ONB-07 como estão; ENG-01 passa para D1, só se não houver depósito nas primeiras 24 horas.
Uso: python3 regua-v1/decisoes3.py [saida.json]
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import alertas  # noqa: E402
import decisoes  # noqa: E402

PAGE = ROOT / 'comunicacoes-v0-v1.html'
OUT_JSON = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None

TITULO_NOVO = 'Aproveite câmbio e use cartão internacional'
TEXTO_NOVO = 'Em sua conta Zeom aproveite o dólar e use seu cartão já em dólar para efetuar compras internacionais.'


def trocar(html, velho, novo):
    assert velho in html, velho[:60]
    return html.replace(velho, novo)


def main():
    a = PAGE.read_text(encoding='utf-8')
    DATA, FASES, EMAILS = decisoes.carregar(a)
    assert any(x['id'] == 'VAL-18' for x in DATA), 'terceira rodada já aplicada'
    por_id = {x['id']: x for x in DATA}
    n0 = len(DATA)
    alteracoes = {}

    def alt(i, t):
        alteracoes.setdefault(i, []).append(t)

    # A18: VAL-18 e VAL-19 saem; precedência como nos pushes
    for i in ('VAL-18', 'VAL-19'):
        x = por_id[i]
        DATA.remove(x)
        EMAILS.pop(x['file'], None)
        p = ROOT / x['file']
        if p.exists():
            p.unlink()
    regras = [('VAL-14', 'D+7 · não ativou a multiconta (prioridade sobre o e-mail de cartão)', 'prioridade sobre o e-mail de cartão (VAL-06)'),
              ('VAL-06', 'D+7 · não ativou o cartão (não recebe quem recebe o e-mail de multiconta)', 'exclui quem recebe o e-mail de multiconta (VAL-14)'),
              ('VAL-15', 'D+21 · não ativou a multiconta (prioridade sobre o e-mail de cartão)', 'prioridade sobre o e-mail de cartão (VAL-07)'),
              ('VAL-07', 'D+21 · não ativou o cartão (não recebe quem recebe o e-mail de multiconta)', 'exclui quem recebe o e-mail de multiconta (VAL-15)')]
    for i, trig, nota in regras:
        por_id[i]['trigger'] = trig
        alt(i, 'A18 · mesma regra de precedência dos pushes: ' + nota)

    # A19: sem a promessa "sem IOF"
    k13 = por_id['KYC-13']
    antigo_t, antigo_c = k13['campos'][0]['value'], k13['corpo']
    k13['campos'] = [{'label': 'Assunto', 'value': TITULO_NOVO}]; k13['corpo'] = TEXTO_NOVO
    h = EMAILS[k13['file']]
    h = trocar(h, antigo_t, TITULO_NOVO); h = trocar(h, antigo_c, TEXTO_NOVO)
    EMAILS[k13['file']] = h
    (ROOT / k13['file']).write_text(trocar((ROOT / k13['file']).read_text(encoding='utf-8'), antigo_t, TITULO_NOVO).replace(antigo_c, TEXTO_NOVO), encoding='utf-8')
    alt('KYC-13', 'A19 · promessa "sem IOF" removida do assunto e do texto')
    e07 = por_id['ENG-07']
    e07['campos'] = [{'label': 'Título', 'value': TITULO_NOVO}]; e07['corpo'] = TEXTO_NOVO
    alt('ENG-07', 'A19 · promessa "sem IOF" removida do título e do texto')

    # A20: ENG-01 em D1
    e01 = por_id['ENG-01']
    e01['dia'] = 'D1'
    e01['trigger'] = 'D1 — 1 dia depois do KYC aprovado, só se não houve depósito nas primeiras 24 horas'
    alt('ENG-01', 'A20 · passa para D1, só para quem não depositou nas primeiras 24 horas')

    def bloco(a, ini, fim, novo):
        i = a.index(ini); j = a.index(fim, i) + len(fim)
        return a[:i] + novo + a[j:]
    a = bloco(a, 'const DATA = [', '\n];', 'const DATA = ' + json.dumps(DATA, ensure_ascii=False, indent=1) + ';')
    ei = a.index('const EMAILS = {'); ej = a.index('};', ei) + 2
    a = a[:ei] + 'const EMAILS = ' + json.dumps(EMAILS, ensure_ascii=False) + ';' + a[ej:]
    PAGE.write_text(a, encoding='utf-8')
    alertas.aplicar()
    if OUT_JSON:
        OUT_JSON.write_text(json.dumps(dict(alteracoes=alteracoes, removidas_na_rodada=['VAL-18', 'VAL-19']), ensure_ascii=False), encoding='utf-8')
    print('comunicações:', n0, '->', len(DATA))


if __name__ == '__main__':
    main()
