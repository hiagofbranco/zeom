"""E-mails da Régua V1 — mesmos padrões dos e-mails de emails/reguas/ (header logo simples,
seções 40px, card de intuito, CTA sólido com fallback VML, lista linha-divisória, rodapé dark)."""

G = "font-family:'Geist',Helvetica,Arial,sans-serif"
INK, BROWN, OLIVA, BEGE, MARFIM, BORDER = '#282621', '#3A362C', '#6C664E', '#BFBA99', '#ECEADC', 'rgba(40,38,33,.14)'
A = '../../assets/'


def sp(n):
    return f'<div style="height:{n}px;line-height:{n}px;font-size:0">&nbsp;</div>'


def gap(n=48):
    return f'<tr><td style="height:{n}px;line-height:{n}px;font-size:0">&nbsp;</td></tr>'


def eyebrow(t):
    return f'<div style="{G};font-size:12px;font-weight:600;letter-spacing:0.8px;text-transform:uppercase;color:{OLIVA};mso-line-height-rule:exactly;line-height:16px">{t}</div>'


def h1(t):
    return f'<div style="{G};font-size:24px;font-weight:600;letter-spacing:-0.3px;color:{INK};mso-line-height-rule:exactly;line-height:31px">{t}</div>'


def p(t, sz=15, lh=23):
    return f'<p style="margin:0;{G};font-weight:300;font-size:{sz}px;line-height:{lh}px;color:{BROWN};mso-line-height-rule:exactly">{t}</p>'


def small(t):
    return f'<p style="margin:0;{G};font-weight:300;font-size:11px;line-height:17px;color:{OLIVA};mso-line-height-rule:exactly">{t}</p>'


def intent(icon, title, text):
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="{MARFIM}" style="background-color:{MARFIM};border-radius:12px"><tr><td style="padding:24px"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
<td width="48" valign="top" style="width:48px"><img src="{A}icons/png/{icon}-gold.png" width="40" height="40" alt="" style="display:block;width:40px;height:40px"></td>
<td width="16" style="width:16px">&nbsp;</td>
<td valign="top"><div style="{G};font-weight:600;font-size:15px;color:{INK};line-height:20px">{title}</div><div style="height:4px;line-height:4px;font-size:0">&nbsp;</div><div style="{G};font-weight:300;font-size:13px;color:{BROWN};line-height:19px">{text}</div></td>
</tr></table></td></tr></table>'''


def solid_btn(t, href):
    return f'''<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{href}" style="height:48px;v-text-anchor:middle;width:280px;" arcsize="17%" strokecolor="{BEGE}" strokeweight="0" fillcolor="{BEGE}">
<w:anchorlock/>
<center style="color:{INK};font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:600;">{t}</center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="mso-hide:all"><tr><td align="center" bgcolor="{BEGE}" style="background-color:{BEGE};border-radius:8px">
<a href="{href}" target="_blank" style="display:inline-block;padding:14px 28px;{G};font-size:14px;font-weight:600;letter-spacing:0.1px;color:{INK};text-decoration:none;border-radius:8px;mso-hide:all">{t} &#8594;</a>
</td></tr></table>
<!--<![endif]-->'''


def ghost_btn(t, href):
    return f'''<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{href}" style="height:46px;v-text-anchor:middle;width:260px;" arcsize="17%" strokecolor="#DDD9C5" strokeweight="1px" fillcolor="#FFFFFF">
<w:anchorlock/>
<center style="color:{INK};font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:600;">{t}</center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="mso-hide:all"><tr><td align="center" bgcolor="#FFFFFF" style="background-color:#FFFFFF;border:1px solid {BORDER};border-radius:8px">
<a href="{href}" target="_blank" style="display:inline-block;padding:12px 24px;{G};font-size:13px;font-weight:600;color:{INK};text-decoration:none;border-radius:8px;mso-hide:all">{t} &#8594;</a>
</td></tr></table>
<!--<![endif]-->'''


def item_list(items):
    rows = []
    for i, (icon, title, text) in enumerate(items):
        last = i == len(items) - 1
        pad = '0 0 16px' if i == 0 else ('16px 0 14px' if last else '16px 0 16px')
        border = '' if i == 0 else f'border-top:1px solid {BORDER};'
        rows.append(f'<tr><td style="{border}padding:{pad}"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td width="24" valign="top" style="width:24px;padding-top:1px"><img src="{A}icons/png/{icon}-gold.png" width="22" height="22" alt="" style="display:block;width:22px;height:22px"></td><td width="14" style="width:14px">&nbsp;</td><td valign="top"><div style="{G};font-weight:600;font-size:14px;color:{INK};line-height:20px">{title}</div><div style="{G};font-weight:300;font-size:13px;color:{BROWN};line-height:19px;padding-top:3px">{text}</div></td></tr></table></td></tr>')
    return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">\n' + '\n'.join(rows) + '\n</table>'


def steps(items):
    rows = []
    for i, (title, text) in enumerate(items, 1):
        rows.append(f'<tr><td style="padding:0 0 {0 if i == len(items) else 18}px"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td width="32" valign="top" style="width:32px"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="{MARFIM}" align="center" valign="middle" width="32" height="32" style="width:32px;height:32px;background-color:{MARFIM};border-radius:8px;{G};font-size:14px;font-weight:600;color:{INK};line-height:32px">{i}</td></tr></table></td><td width="14" style="width:14px">&nbsp;</td><td valign="top"><div style="{G};font-weight:600;font-size:14px;color:{INK};line-height:20px;padding-top:6px">{title}</div><div style="{G};font-weight:300;font-size:13px;color:{BROWN};line-height:19px;padding-top:3px">{text}</div></td></tr></table></td></tr>')
    return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">\n' + '\n'.join(rows) + '\n</table>'


def section(comment, inner):
    return f'<!-- {comment} -->\n<tr><td class="px" style="padding:0 40px">\n{inner}\n</td></tr>'


HEADER = f'''<!-- header · logo simples (blocks/header/logo.html) -->
<tr><td class="px" bgcolor="#FFFFFF" style="background-color:#FFFFFF;padding:26px 40px 22px;border-bottom:1px solid {BORDER}"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td valign="middle" style="line-height:0;font-size:0"><img src="{A}zeom-icone-96.png" width="29" height="29" alt="" style="display:block;width:29px;height:29px"></td><td width="12" style="width:12px">&nbsp;</td><td valign="middle" style="{G};font-weight:300;font-size:28px;letter-spacing:.5px;color:{INK};line-height:29px;mso-line-height-rule:exactly">zeom</td></tr></table></td></tr>'''


def footer(reason):
    return f'''<!-- rodapé institucional · dark, full-bleed (blocks/footer/icones-negativo.html) -->
<tr><td bgcolor="#21211C" style="background-color:#21211C"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td align="center" class="px" style="padding:56px 40px 48px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" class="container" style="width:100%;max-width:600px">
<tr><td align="center"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td valign="middle" style="line-height:0;font-size:0"><img src="{A}zeom-esfera-96.png" width="26" height="26" alt="" style="display:block;width:26px;height:26px"></td><td width="10" style="width:10px">&nbsp;</td><td valign="middle" style="{G};font-weight:300;font-size:21px;letter-spacing:.3px;color:#FAFAF9;line-height:26px;mso-line-height-rule:exactly">zeom</td></tr></table></td></tr>
<tr><td align="center" style="padding-top:20px"><table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr>
<td align="center" width="28" style="width:28px;line-height:0;font-size:0"><a href="{{{{LINK_instagram}}}}" target="_blank" style="text-decoration:none"><img src="{A}icons/png/instagram-soc-dark.png" width="28" height="28" alt="Instagram" style="display:block;width:28px;height:28px"></a></td>
<td width="10" style="width:10px">&nbsp;</td>
<td align="center" width="28" style="width:28px;line-height:0;font-size:0"><a href="{{{{LINK_linkedin}}}}" target="_blank" style="text-decoration:none"><img src="{A}icons/png/linkedin-soc-dark.png" width="28" height="28" alt="LinkedIn" style="display:block;width:28px;height:28px"></a></td>
<td width="10" style="width:10px">&nbsp;</td>
<td align="center" width="28" style="width:28px;line-height:0;font-size:0"><a href="{{{{LINK_x}}}}" target="_blank" style="text-decoration:none"><img src="{A}icons/png/x-soc-dark.png" width="28" height="28" alt="X" style="display:block;width:28px;height:28px"></a></td>
</tr></table></td></tr>
<tr><td align="center" style="padding-top:20px;{G};font-weight:300;font-size:11px;line-height:17px;color:#B3B3A8;text-align:center">{reason}<br>{{{{RAZAO_SOCIAL}}}} · {{{{ENDERECO_POSTAL}}}}<br><br><a href="{{{{LINK_privacidade}}}}" style="color:#B3B3A8;text-decoration:underline">Privacidade</a> · <a href="{{{{LINK_termos}}}}" style="color:#B3B3A8;text-decoration:underline">Termos</a> · <a href="{{{{LINK_preferencias}}}}" style="color:#B3B3A8;text-decoration:underline">Preferências</a> · <a href="{{{{LINK_cancelar_inscricao}}}}" style="color:#B3B3A8;text-decoration:underline">Cancelar inscrição</a></td></tr>
</table>
</td></tr></table></td></tr>'''


def page(meta, subject, preheader, rows, reason):
    return f'''<!-- {meta} -->
<!DOCTYPE html>
<html lang="pt-BR" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>Zeom · {subject}</title>
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
<style>
body,table,td{{margin:0;padding:0}}
img{{border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic}}
table{{border-collapse:collapse}}
@media (max-width:600px){{
  .container{{width:100% !important;max-width:100% !important}}
  .px{{padding-left:24px !important;padding-right:24px !important}}
  .card-pad{{padding:24px !important}}
}}
</style>
</head>
<body style="margin:0;padding:0;background-color:#FFFFFF;-webkit-font-smoothing:antialiased">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#FFFFFF;opacity:0">{preheader}{'&nbsp;&#8203;' * 11}</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="#FFFFFF" style="background-color:#FFFFFF">
<tr><td align="center" style="padding:32px 20px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="container" style="width:600px;max-width:600px">
{HEADER}
{gap()}
{(chr(10) + gap() + chr(10)).join(rows)}
{gap()}
{footer(reason)}
</table>
</td></tr></table>
</body>
</html>
'''


EMAILS = [
    dict(
        file='v1-01-repescagem-cartao-d7.html',
        meta='V1 · 01 · PREVENÇÃO · VALOR & REPESCAGEM · E-mail D7 — Repescagem · Cartão\nGatilho: 1 semana sem ativar o cartão\nObjetivo CRM: ativação do cartão internacional, sem prazo nem urgência\nBlocos: header logo simples · card de intuito · CTA sólido · passos numerados · suporte (CTA secundário)',
        subject='Seu cartão internacional está esperando',
        preheader='Ative quando quiser — sem prazo para isso mudar.',
        reason='Você recebeu este e-mail porque o cartão internacional da sua conta Zeom ainda não foi ativado.',
        rows=[
            section('seção 1 · contexto + intuito + CTA',
                    eyebrow('Cartão internacional') + sp(16) + h1('Seu cartão em dólar está pronto para ativar') + sp(16)
                    + p('O cartão internacional da sua conta Zeom já está disponível. A ativação é feita pelo aplicativo, em poucos passos, e pode acontecer quando fizer sentido para você.')
                    + sp(24) + intent('cartao', 'Usa o saldo que você já tem', 'As compras no exterior são debitadas do seu saldo em dólar, com a cotação visível antes de cada recarga.')
                    + sp(24) + solid_btn('Ativar meu cartão', '{{LINK_app_cartao}}')),
            section('seção 2 · passos numerados',
                    eyebrow('Como ativar') + sp(16) + steps([
                        ('Abra o aplicativo e acesse Cartão', 'O cartão aparece na tela inicial da sua conta.'),
                        ('Confirme seus dados e crie a senha', 'A senha é pessoal e fica só com você.'),
                        ('Use em compras internacionais', 'Em lojas físicas e online, onde a bandeira for aceita.'),
                    ])),
            section('seção 3 · suporte (cta secundário)',
                    eyebrow('Dúvidas e suporte') + sp(16)
                    + p('Se precisar de ajuda na ativação, nossa equipe de atendimento está disponível.', 13, 19)
                    + sp(20) + ghost_btn('Falar com o suporte no WhatsApp', '{{LINK_whatsapp_suporte}}')),
        ]),
    dict(
        file='v1-02-repescagem-investimento.html',
        meta='V1 · 02 · PREVENÇÃO · VALOR & REPESCAGEM · E-mail D+X — Repescagem · Investimento\nGatilho: fez Pix mas nunca investiu, X dias depois\nObjetivo CRM: apresentar a área de investimentos, sem recomendação nem urgência\nBlocos: header logo simples · card de intuito · CTA sólido · lista linha-divisória · disclaimer de investimentos',
        subject='Seus investimentos internacionais estão disponíveis',
        preheader='Sem valor mínimo para começar, no seu tempo.',
        reason='Você recebeu este e-mail porque sua conta Zeom tem acesso à área de investimentos internacionais.',
        rows=[
            section('seção 1 · contexto + intuito + CTA',
                    eyebrow('Investimentos') + sp(16) + h1('Seu saldo em dólar também pode ser investido') + sp(16)
                    + p('Com sua conta ativa e o primeiro Pix concluído, a área de investimentos internacionais já está liberada no aplicativo. Você escolhe quando e quanto alocar.')
                    + sp(24) + intent('investir', 'Sem valor mínimo para começar', 'Comece com o valor que fizer sentido para você e acompanhe a evolução dos ativos direto no painel do app.')
                    + sp(24) + solid_btn('Conhecer os investimentos', '{{LINK_app_investimentos}}')),
            section('seção 2 · lista linha-divisória + disclaimer',
                    eyebrow('O que você encontra no app') + sp(16) + item_list([
                        ('globo', 'Ativos no exterior', 'Opções de investimento internacional reunidas em um só lugar.'),
                        ('olho', 'Acompanhamento no painel', 'Evolução, saldo investido e movimentações em tempo real.'),
                        ('chat', 'Consultas com o Zeom AI', 'Tire dúvidas sobre alocação e métricas, 24 horas por dia.'),
                    ]) + sp(24)
                    + small('Conteúdo informativo. Não constitui oferta, recomendação ou análise individualizada de investimentos. Rentabilidade passada não é garantia de resultado futuro. Investimentos em ativos internacionais estão sujeitos a riscos e à variação cambial.')),
        ]),
    dict(
        file='v1-03-prevencao-valor-d7.html',
        meta='V1 · 03 · PREVENÇÃO · VALOR & REPESCAGEM · E-mail D7 — Prevenção · Valor\nGatilho: 1 semana sem ativar cartão ou multiconta\nObjetivo CRM: lembrar o valor dos recursos internacionais já liberados\nBlocos: header logo simples · lista linha-divisória · CTA sólido · Zeom AI (CTA secundário)',
        subject='Seus recursos internacionais continuam por aqui',
        preheader='Cartão e multiconta, prontos para quando você quiser usar.',
        reason='Você recebeu este e-mail porque os recursos internacionais da sua conta Zeom ainda não foram utilizados.',
        rows=[
            section('seção 1 · contexto + lista + CTA',
                    eyebrow('Sua conta') + sp(16) + h1('Cartão e multiconta, prontos para usar') + sp(16)
                    + p('Os recursos internacionais da sua conta Zeom seguem disponíveis no aplicativo, para quando fizer sentido para você.')
                    + sp(24) + item_list([
                        ('cartao', 'Cartão internacional', 'Compras no exterior debitadas do seu saldo em dólar.'),
                        ('globo', 'Multiconta', 'Saldos em diferentes moedas, organizados em um só lugar.'),
                        ('transferir', 'Conversão entre moedas', 'Cotação visível antes de cada operação.'),
                    ]) + sp(24) + solid_btn('Acessar minha conta', '{{LINK_acessar_conta}}')),
            section('seção 2 · zeom ai (cta secundário)',
                    intent('chat', 'Ficou alguma dúvida?', 'O Zeom AI responde sobre cartão, saldos e limites a qualquer hora, direto no aplicativo.')
                    + sp(20) + ghost_btn('Conversar com o Zeom AI', '{{LINK_zeom_ai_chat}}')),
        ]),
    dict(
        file='v1-06-churn-win-back.html',
        meta='V1 · 06 · CHURN · WIN BACK · E-mail — PROPOSTA DE COPY (aguardando aprovação)\nGatilho: inativo por longo período / esgotou qualquer régua de prevenção\nObjetivo CRM: reabrir a porta sem pressão + entender o motivo da inatividade\nAssinatura: Equipe Zeom (CEO não participa)\nBlocos: header logo simples · lista linha-divisória · CTA sólido · pesquisa (CTA secundário) · assinatura',
        subject='Sua conta Zeom continua ativa',
        preheader='Seus recursos seguem disponíveis, para quando fizer sentido retomar.',
        reason='Você recebeu este e-mail porque sua conta Zeom está sem movimentações há um longo período.',
        rows=[
            section('seção 1 · contexto + lista + CTA',
                    eyebrow('Sua conta Zeom') + sp(16) + h1('Sua conta continua aqui, do jeito que você deixou') + sp(16)
                    + p('Faz um tempo que você não movimenta sua conta Zeom. Ela segue ativa, com seus dados e saldos preservados, para quando você quiser retomar.')
                    + sp(24) + eyebrow('O que segue disponível') + sp(16) + item_list([
                        ('enviar', 'Transferências Globais', 'Envio e conversão de moedas de forma direta.'),
                        ('cartao', 'Cartão em Dólar', 'Disponível para uso em compras internacionais.'),
                        ('investir', 'Investimentos', 'Painel para acompanhamento de ativos no exterior.'),
                        ('chat', 'Zeom AI', 'Consultas e suporte 24 horas por dia, no aplicativo.'),
                    ]) + sp(24) + solid_btn('Acessar minha conta', '{{LINK_acessar_conta}}')),
            section('seção 2 · pesquisa (cta secundário) + assinatura',
                    eyebrow('Conte para a gente') + sp(16)
                    + p('Se algo não funcionou como você esperava, queremos saber. A pesquisa leva menos de 2 minutos e ajuda a melhorar a Zeom.', 13, 19)
                    + sp(20) + ghost_btn('Responder a pesquisa', '{{LINK_pesquisa_win_back}}')
                    + sp(32) + p('Até breve,<br><span style="font-weight:600;color:#282621">Equipe Zeom</span>', 14, 21)),
        ]),
]


def build():
    return {e['file']: page(e['meta'], e['subject'], e['preheader'], e['rows'], e['reason']) for e in EMAILS}
