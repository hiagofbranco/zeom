"""Incoerências entre V0 e V1 (e dentro de cada versão), marcadas em comunicacoes-v0-v1.html.

Cada alerta tem nível, título, o que é e o que decidir. `casa(item)` diz quais comunicações
entram nele. Só metadados: nenhum copy é alterado.
Uso: python3 regua-v1/alertas.py   (aplica em comunicacoes-v0-v1.html)
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'comunicacoes-v0-v1.html'


def it(ver=None, fase=None, canal=None, dia=None, sub=None, assunto=None):
    def f(x):
        a = (x['campos'][0]['value'] if x['campos'] else '')
        return ((ver is None or x['ver'] == ver) and (fase is None or x['fase'] == fase) and (canal is None or x['canal'] == canal)
                and (dia is None or x['dia'] == dia or x['dia'].startswith(dia + ' ')) and (sub is None or x.get('sub') == sub)
                and (assunto is None or a.startswith(assunto)))
    return f


def algum(*fs):
    return lambda x: any(f(x) for f in fs)


def taxa_zero(x):
    t = ((x['campos'][0]['value'] if x['campos'] else '') + ' ' + x['corpo']).lower()
    return 'taxa zero' in t or 'sem taxa' in t


ALERTAS = {
    'A01': dict(nivel='alta', titulo='Inatividade D7 duplicada (V0 + V1)',
                texto='O mesmo gatilho (7 dias sem atividade) existe na V0 e na V1: até 3 comunicações no mesmo dia, 2 pushes e 1 e-mail.',
                sugestao='Manter só uma versão; a V1 substitui a V0.',
                casa=algum(it('v0', 'engajamento', 'push', 'D7', 'Inatividade'), it('v1', 'engajamento', None, 'D7', 'Inatividade'))),
    'A02': dict(nivel='alta', titulo='Inatividade D14 duplicada (V0 + V1)',
                texto='Dois e-mails no mesmo dia para o mesmo gatilho (14 dias sem atividade), um da V0 e um da V1.',
                sugestao='Manter só um e-mail D14.',
                casa=algum(it('v0', 'engajamento', 'email', 'D14', 'Inatividade'), it('v1', 'engajamento', 'email', 'D14', 'Inatividade'))),
    'A03': dict(nivel='alta', titulo='Inatividade D21 duplicada (V0 + V1)',
                texto='Push da V0 e e-mail da V1 no mesmo dia (21 dias sem atividade), os dois com a ideia de "só um Pix".',
                sugestao='Escolher um fechamento (push ou e-mail) ou assumir os dois como par e retirar o da V0.',
                casa=algum(it('v0', 'engajamento', 'push', 'D21', 'Inatividade'), it('v1', 'engajamento', 'email', 'D21', 'Inatividade'))),
    'A04': dict(nivel='alta', titulo='KYC D1: assunto e pré-header iguais',
                texto='A V0 (D1) e a V1 (D+1, versão A) têm o mesmo assunto, "Sua verificação de identidade", e o mesmo pré-header, no mesmo dia.',
                sugestao='Manter só uma. A V1 versão A substitui a V0 D1.',
                casa=algum(it('v0', 'kyc', 'email', 'D1'), it('v1', 'kyc', 'email', 'D+1 (A'))),
    'A05': dict(nivel='alta', titulo='KYC: fechamento e pesquisa repetidos entre V0 e V1',
                texto='A V1 reaproveita o conteúdo do D6 (agora D14) e do D15 (agora D21) da V0, com os mesmos assuntos. Se a V0 continuar ativa, o cliente recebe os dois.',
                sugestao='Desativar o D6 e o D15 da V0 quando a V1 entrar.',
                casa=algum(it('v0', 'kyc', 'email', 'D6'), it('v1', 'kyc', 'email', 'D14'), it('v0', 'kyc', 'email', 'D15'), it('v1', 'kyc', 'email', 'D21'))),
    'A06': dict(nivel='media', titulo='KYC: mesmo texto no push D5 e no e-mail D7',
                texto='O push do D5 e o e-mail do D7 trazem o mesmo texto ("Conclua sua verificação e tenha acesso ao câmbio com taxa zero, por tempo limitado.*").',
                sugestao='Diferenciar os textos ou rever a cadência D5/D7.',
                casa=algum(it('v1', 'kyc', 'push', 'D5'), it('v1', 'kyc', 'email', 'D7'))),
    'A07': dict(nivel='alta', titulo='Oferta de taxa zero em 9 comunicações',
                texto='A oferta aparece no KYC (D5 e D7), no 1º depósito (D+1 e D+3), no "dólar recuou" e na Inatividade D21, sempre "por tempo limitado". Sem regra única de quem recebe e por quanto tempo, o cliente pode ver ofertas diferentes ao mesmo tempo.',
                sugestao='Definir uma regra única: elegibilidade, prazo, quantas vezes e como o cupom é resgatado.',
                casa=lambda x: x['ver'] == 'v1' and taxa_zero(x)),
    'A08': dict(nivel='alta', titulo='Valor: até 4 e-mails no D7 para o mesmo público',
                texto='Quem não ativou o cartão (e a multiconta) recebe no D7 e-mails da V0 (cartão e valor) e da V1 (cartão e multiconta).',
                sugestao='Reduzir a um e-mail por público e dia; a V1 substitui os da V0.',
                casa=algum(it('v0', 'valor', 'email', 'D7'), it('v1', 'valor', 'email', 'D+7', 'Repescagem · Cartão'), it('v1', 'valor', 'email', 'D+7', 'Repescagem · Multiconta'))),
    'A09': dict(nivel='alta', titulo='D+1: até 4 pushes no mesmo dia',
                texto='Depois de abrir a conta, o cliente pode receber no D+1 os pushes de 1º depósito, cartão, multiconta e investimento. Não há limite de envios por cliente definido.',
                sugestao='Definir limite e prioridade entre as réguas (por exemplo, 1 push por dia).',
                casa=algum(it('v1', 'engajamento', 'push', 'D+1', '1º depósito'), it('v1', 'valor', 'push', 'D+1'))),
    'A10': dict(nivel='alta', titulo='D+3: até 4 pushes no mesmo dia',
                texto='Mesma situação do D+1: 1º depósito, cartão, multiconta e investimento no D+3.',
                sugestao='Escalonar as réguas ou aplicar limite diário.',
                casa=algum(it('v1', 'engajamento', 'push', 'D+3', '1º depósito'), it('v1', 'valor', 'push', 'D+3'))),
    'A11': dict(nivel='alta', titulo='Variação cambial: 4 comunicações para o mesmo evento',
                texto='A V0 ("Câmbio, de forma simples", manual) e a V1 ("O dólar recuou hoje", por limiar) disparam no mesmo evento, cada uma com push e e-mail.',
                sugestao='Definir qual versão vale e se o disparo é manual ou por limiar.',
                casa=it(None, 'oportunidades', None, 'Evento')),
    'A12': dict(nivel='media', titulo='1º depósito: duas cadências para o mesmo público',
                texto='A V0 fala com quem não fez o 1º Pix por dia da semana (quarta e sexta) e a V1 por D+1 e D+3. O mesmo cliente pode receber as duas.',
                sugestao='Escolher uma cadência e retirar a outra.',
                casa=algum(it('v0', 'engajamento', None, None, '1º depósito'), it('v1', 'engajamento', 'push', 'D+1', '1º depósito'), it('v1', 'engajamento', 'push', 'D+3', '1º depósito'))),
    'A13': dict(nivel='media', titulo='Mesmo título em momentos diferentes',
                texto='"Sua conta está pronta" é o assunto do e-mail de aprovação do KYC (onboarding) e o título do push do 1º depósito (D+1).',
                sugestao='Trocar um dos dois para não confundir os momentos.',
                casa=algum(it('v0', 'onboarding', 'email', 'KYC ok', None, 'Sua conta está pronta'), it('v1', 'engajamento', 'push', 'D+1', '1º depósito'))),
    'A14': dict(nivel='media', titulo='D+30: até 3 pushes e 3 e-mails no mesmo dia',
                texto='O Win Back (churn) e as comunicações de investidor (saldo ocioso e novos aportes) disparam no D+30 e o público pode se sobrepor.',
                sugestao='Definir prioridade entre Churn e Ongoing no D+30.',
                casa=algum(it('v1', 'churn', None, 'D+30'), it('v1', 'oportunidades', None, 'D+30'))),
    'A15': dict(nivel='baixa', titulo='KYC aprovado: 3 comunicações no mesmo momento',
                texto='Push "Sua conta está ativa" e dois e-mails (panorama e carta do CEO) saem juntos quando o KYC é aprovado. O e-mail de panorama já está marcado para confirmar se mantém.',
                sugestao='Confirmar se os dois e-mails precisam sair juntos.',
                casa=it('v0', 'onboarding', None, 'KYC ok')),
    'A16': dict(nivel='media', titulo='Gatilho "fez Pix" em V0 e V1',
                texto='A V0 envia o push de quarta ("Mais para o seu saldo") para quem já fez o Pix, e a V1 envia "Pix recebido na sua conta" após cada Pix.',
                sugestao='Escolher um dos dois ou diferenciar o público.',
                casa=algum(it('v0', 'semana1', 'push', 'Qua'), it('v1', 'valor', 'push', 'Após cada Pix'))),
}


def aplicar():
    a = PAGE.read_text(encoding='utf-8')
    di = a.index('const DATA = ['); dj = a.index('\n];', di) + 3
    DATA = json.loads(a[di + len('const DATA = '):dj].rstrip().rstrip(';'))
    for d in DATA:
        d.pop('alertas', None)
    contagem = {}
    for k, al in ALERTAS.items():
        n = 0
        for d in DATA:
            if al['casa'](d):
                d.setdefault('alertas', []).append(k); n += 1
        contagem[k] = n
        assert n >= 2, (k, n)
    a = a[:di] + 'const DATA = ' + json.dumps(DATA, ensure_ascii=False, indent=1) + ';' + a[dj:]
    pub = {k: {c: v for c, v in al.items() if c != 'casa'} for k, al in ALERTAS.items()}
    bloco = 'const ALERTAS = ' + json.dumps(pub, ensure_ascii=False, indent=1) + ';\n'
    if 'const ALERTAS = ' in a:
        i = a.index('const ALERTAS = '); j = a.index('\n};\n', i) + 4
        a = a[:i] + bloco + a[j:]
    else:
        a = a.replace('const BASE = \'\';', bloco + 'const BASE = \'\';', 1)
    PAGE.write_text(a, encoding='utf-8')
    return contagem, sum(1 for d in DATA if d.get('alertas'))


if __name__ == '__main__':
    c, n = aplicar()
    print('comunicações com atenção:', n)
    print(c)
