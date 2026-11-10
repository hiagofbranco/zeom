"""Incoerências entre V0 e V1 e as decisões do time, marcadas em comunicacoes-v0-v1.html.

estado:
  aberta      -> ainda precisa de decisão (chip vermelho/amarelo "⚠ Atenção")
  decidida    -> o time decidiu (chip verde "✓ Decidido"; a decisão aparece no balão)
  descartada  -> sem inconsistência (nenhum chip)
`casa(item)` diz quais comunicações (já com as decisões aplicadas) entram no alerta.
Só metadados: nenhum copy é alterado aqui.  Uso: python3 regua-v1/alertas.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'comunicacoes-v0-v1.html'

PRECEDENCIA_D1 = ('Ordem de precedência: ENG-06 (não dispara os outros: o cliente ainda não tem conta ativa) → VAL-16 (saldo em conta, prioridade máxima) '
                  '→ VAL-12 (ativar multiconta) → VAL-04 (ativar cartão). Exclusões: VAL-12 exclui clientes da VAL-16; VAL-04 exclui clientes da VAL-16 e da VAL-12.')
PRECEDENCIA_D3 = ('Ordem de precedência: ENG-07 (não dispara os outros: o cliente ainda não tem conta ativa) → VAL-17 (saldo em conta, prioridade máxima) '
                  '→ VAL-13 (ativar multiconta) → VAL-05 (ativar cartão). Exclusões: VAL-13 exclui clientes da VAL-17; VAL-05 exclui clientes da VAL-17 e da VAL-13.')


def it(ver=None, fase=None, canal=None, dia=None, sub=None, assunto=None):
    def f(x):
        a = (x['campos'][0]['value'] if x['campos'] else '')
        return ((ver is None or x['ver'] == ver) and (fase is None or x['fase'] == fase) and (canal is None or x['canal'] == canal)
                and (dia is None or x['dia'] == dia or x['dia'].startswith(dia + ' '))
                and (sub is None or x.get('sub') == sub) and (assunto is None or a.startswith(assunto)))
    return f


def algum(*fs):
    return lambda x: any(f(x) for f in fs)


def texto_tem(*palavras):
    def f(x):
        t = ((x['campos'][0]['value'] if x['campos'] else '') + ' ' + x['corpo']).lower()
        return any(p.lower() in t for p in palavras)
    return f


ALERTAS = {
    'A01': dict(estado='decidida', nivel='alta', titulo='Inatividade D7 duplicada (V0 + V1)',
                texto='O mesmo gatilho (7 dias sem atividade) existia na V0 e na V1: até 3 comunicações no mesmo dia.',
                sugestao='', decisao='Eliminar ENG-03 (V0 push D7). Ficam 1 push (ENG-09) e 1 e-mail (ENG-10).',
                casa=it('v1', 'engajamento', None, 'D7', 'Inatividade')),
    'A02': dict(estado='decidida', nivel='alta', titulo='Inatividade D14 duplicada (V0 + V1)',
                texto='Dois e-mails no mesmo dia para o mesmo gatilho (14 dias sem atividade).',
                sugestao='', decisao='Remover ENG-04 (V0 e-mail D14). ENG-11 passa a e-mail + push.',
                casa=it('v1', 'engajamento', None, 'D14', 'Inatividade')),
    'A03': dict(estado='decidida', nivel='alta', titulo='Inatividade D21 duplicada (V0 + V1)',
                texto='Push da V0 e e-mail da V1 no mesmo dia (21 dias sem atividade), os dois com a ideia de "só um Pix".',
                sugestao='', decisao='Manter ENG-05 e ENG-12: são canais diferentes.',
                casa=algum(it('v0', 'engajamento', 'push', 'D21', 'Inatividade'), it('v1', 'engajamento', 'email', 'D21', 'Inatividade'))),
    'A04': dict(estado='decidida', nivel='alta', titulo='KYC D1: assunto e pré-header iguais',
                texto='A V0 (D1) e a V1 (D+1, versão A) tinham o mesmo assunto e o mesmo pré-header, no mesmo dia.',
                sugestao='', decisao='Manter KYC-02 (e-mail) e mudar KYC-07 para push.',
                casa=algum(it('v0', 'kyc', 'email', 'D1'), it('v1', 'kyc', 'push', 'D+1'))),
    'A05': dict(estado='decidida', nivel='alta', titulo='KYC: fechamento e pesquisa repetidos entre V0 e V1',
                texto='A V1 reaproveita o conteúdo do D6 (agora D14) e do D15 (agora D21) da V0, com os mesmos assuntos.',
                sugestao='', decisao='Remover KYC-06. Manter KYC-05 e KYC-15 como duas tentativas de chamado para conclusão. KYC-16 passa a ser fechamento com pesquisa.',
                casa=algum(it('v0', 'kyc', 'email', 'D6'), it('v1', 'kyc', 'email', 'D14'), it('v1', 'kyc', 'email', 'D21'))),
    'A06': dict(estado='decidida', nivel='media', titulo='KYC: mesmo texto no push D5 e no e-mail D7',
                texto='O push do D5 e o e-mail do D7 traziam o mesmo texto.',
                sugestao='', decisao='Mudar o texto de KYC-13 (novo texto aplicado: "Aproveite câmbio sem IOF e use cartão internacional").',
                casa=algum(it('v1', 'kyc', 'push', 'D5'), it('v1', 'kyc', 'email', 'D7'))),
    'A07': dict(estado='decidida', nivel='alta', titulo='Oferta de taxa zero em várias comunicações',
                texto='A oferta aparece no KYC (D5 e D7), na Inatividade D21 e no "dólar recuou", sempre "por tempo limitado".',
                sugestao='', decisao='KYC-10/11 e KYC-12/13 são 2 ativações em 2 canais simultâneos. Manter ENG-06, 07, 12 e ONG-03/04 (disparados em momentos específicos). Oferta válida no mês de novembro.',
                casa=lambda x: x['ver'] == 'v1' and texto_tem('taxa zero', 'sem taxa')(x)),
    'A08': dict(estado='decidida', nivel='alta', titulo='Valor: até 4 e-mails no D7 para o mesmo público',
                texto='Quem não ativou o cartão (e a multiconta) recebia no D7 e-mails da V0 e da V1.',
                sugestao='', decisao='Remover VAL-01 e VAL-03 (V0).',
                casa=algum(it('v1', 'valor', 'email', 'D+7', 'Repescagem · Cartão'), it('v1', 'valor', 'email', 'D+7', 'Repescagem · Multiconta'))),
    'A09': dict(estado='decidida', nivel='alta', titulo='D+1: até 4 pushes no mesmo dia',
                texto='Depois de abrir a conta, o cliente poderia receber no D+1 os pushes de 1º depósito, cartão, multiconta e investimento.',
                sugestao='', decisao=PRECEDENCIA_D1,
                casa=algum(it('v1', 'engajamento', 'push', 'D+1', '1º depósito'), it('v1', 'valor', 'push', 'D+1'))),
    'A10': dict(estado='decidida', nivel='alta', titulo='D+3: até 4 pushes no mesmo dia',
                texto='Mesma situação do D+1, no D+3.',
                sugestao='', decisao=PRECEDENCIA_D3,
                casa=algum(it('v1', 'engajamento', 'push', 'D+3', '1º depósito'), it('v1', 'valor', 'push', 'D+3'))),
    'A11': dict(estado='decidida', nivel='alta', titulo='Variação cambial: 4 comunicações para o mesmo evento',
                texto='A V0 ("Câmbio, de forma simples") e a V1 ("O dólar recuou hoje") disparavam no mesmo evento.',
                sugestao='', decisao='Eliminar ONG-01 e ONG-02 (V0). Ficam ONG-03 e ONG-04.',
                casa=it('v1', 'oportunidades', None, 'Evento')),
    'A12': dict(estado='decidida', nivel='media', titulo='1º depósito: duas cadências para o mesmo público',
                texto='A V0 falava com quem não fez o 1º Pix por dia da semana e a V1 por D+1 e D+3.',
                sugestao='', decisao='ENG-01 vira push 1 hora depois do KYC aprovado. Remover ENG-02. Mudar título e conteúdo de ENG-07 (novo texto aplicado).',
                casa=algum(it('v0', 'engajamento', 'push', '+1h', '1º depósito'), it('v1', 'engajamento', 'push', 'D+1', '1º depósito'), it('v1', 'engajamento', 'push', 'D+3', '1º depósito'))),
    'A13': dict(estado='decidida', nivel='media', titulo='Mesmo título em momentos diferentes',
                texto='"Sua conta está pronta" era o assunto do e-mail de aprovação do KYC e o título do push do 1º depósito (D+1).',
                sugestao='', decisao='Mudar título e conteúdo de ENG-06 (novo texto aplicado: "Deposite hoje e desfrute a conta global Zeom").',
                casa=it('v1', 'engajamento', 'push', 'D+1', '1º depósito')),
    'A14': dict(estado='decidida', nivel='media', titulo='D+30: até 3 pushes e 3 e-mails no mesmo dia',
                texto='O Win Back (churn) e as comunicações de investidor disparavam no D+30 e o público poderia se sobrepor.',
                sugestao='', decisao='Churn passa para Ongoing: CHU-01 em D+45 e CHU-02 em D+60. Remover CHU-03.',
                casa=algum(it('v1', 'oportunidades', None, 'D+30'), it('v1', 'oportunidades', None, 'D+45'), it('v1', 'oportunidades', None, 'D+60'))),
    'A15': dict(estado='decidida', nivel='baixa', titulo='KYC aprovado: 3 comunicações no mesmo momento',
                texto='Push "Sua conta está ativa" e dois e-mails (panorama e carta do CEO) saíam juntos quando o KYC é aprovado.',
                sugestao='', decisao='Remover ONB-06; fica só a comunicação do CEO (ONB-07).',
                casa=it('v0', 'onboarding', None, 'KYC ok')),
    'A16': dict(estado='descartada', nivel='media', titulo='Gatilho "fez Pix" em V0 e V1',
                texto='A V0 envia o push de quarta para quem já fez o Pix e a V1 envia "Pix recebido na sua conta" após cada Pix.',
                sugestao='', decisao='Sem inconsistência.',
                casa=algum(it('v0', 'semana1', 'push', 'Qua'), it('v1', 'valor', 'push', 'Após cada Pix'))),
    # --- pontos que continuam em aberto depois das decisões ---
    'A17': dict(estado='aberta', nivel='media', titulo='KYC D6 e D14 com o mesmo assunto e conteúdo',
                texto='KYC-05 e KYC-15 foram mantidos como duas tentativas, mas os dois se chamam "Sua verificação continua disponível" e o KYC-15 reaproveita o conteúdo do KYC-05.',
                sugestao='Diferenciar o assunto ou o texto da 2ª tentativa.',
                casa=algum(it('v0', 'kyc', 'email', 'D6'), it('v1', 'kyc', 'email', 'D14'))),
    'A18': dict(estado='aberta', nivel='media', titulo='Cartão e multiconta: e-mails no mesmo dia, sem precedência',
                texto='A precedência definida cobre só os pushes de D+1 e D+3. Os e-mails de cartão e multiconta continuam no mesmo dia no D+7 (VAL-06 e VAL-14) e no D+21 (VAL-07 e VAL-15).',
                sugestao='Estender a precedência (e as exclusões) aos e-mails D+7 e D+21.',
                casa=algum(it('v1', 'valor', 'email', 'D+7'), it('v1', 'valor', 'email', 'D+21'))),
    'A19': dict(estado='aberta', nivel='media', titulo='Promessa "sem IOF" a validar',
                texto='O novo texto de KYC-13 e ENG-07 afirma "câmbio sem IOF". É uma promessa que não existia no copy anterior.',
                sugestao='Confirmar com jurídico/compliance antes do disparo.',
                casa=texto_tem('sem IOF')),
    'A20': dict(estado='aberta', nivel='baixa', titulo='KYC aprovado: 3 toques na primeira hora',
                texto='Depois da aprovação do KYC saem o push ONB-05 e o e-mail do CEO (ONB-07), e 1 hora depois o push ENG-01.',
                sugestao='Confirmar se a cadência da primeira hora é essa mesma.',
                casa=algum(it('v0', 'onboarding', 'push', 'KYC ok'), it('v0', 'onboarding', 'email', 'KYC ok'), it('v0', 'engajamento', 'push', '+1h'))),
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
        if al['estado'] != 'descartada':
            for d in DATA:
                if al['casa'](d):
                    d.setdefault('alertas', []).append(k); n += 1
        contagem[k] = n
        if al['estado'] == 'aberta':
            assert n >= 2, (k, n)
    a = a[:di] + 'const DATA = ' + json.dumps(DATA, ensure_ascii=False, indent=1) + ';' + a[dj:]
    pub = {k: {c: v for c, v in al.items() if c != 'casa'} for k, al in ALERTAS.items()}
    bloco = 'const ALERTAS = ' + json.dumps(pub, ensure_ascii=False, indent=1) + ';\n'
    i = a.index('const ALERTAS = '); j = a.index('\n};\n', i) + 4
    a = a[:i] + bloco + a[j:]
    PAGE.write_text(a, encoding='utf-8')
    return contagem, DATA


if __name__ == '__main__':
    c, DATA = aplicar()
    print('abertas:', sum(1 for d in DATA if any(ALERTAS[k]['estado'] == 'aberta' for k in d.get('alertas', []))), '· com decisão:', sum(1 for d in DATA if d.get('alertas')))
    print(c)
