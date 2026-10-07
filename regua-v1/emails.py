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
  .code-val{{font-size:20px !important;letter-spacing:1px !important}}
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


def coupon(title, note):
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="{MARFIM}" style="background-color:{MARFIM};border-radius:12px;border:1px dashed {BEGE}"><tr><td align="center" class="card-pad" style="padding:28px 24px">
<div style="{G};font-size:12px;font-weight:600;letter-spacing:0.8px;text-transform:uppercase;color:{OLIVA};line-height:16px">{title}</div>
<div style="height:10px;line-height:10px;font-size:0">&nbsp;</div>
<div class="code-val" style="{G};font-size:26px;font-weight:600;letter-spacing:2px;color:{INK};line-height:32px;word-break:break-all">{{{{CUPOM_codigo}}}}</div>
<div style="height:10px;line-height:10px;font-size:0">&nbsp;</div>
<div style="{G};font-size:12px;font-weight:300;color:{BROWN};line-height:18px">{note}</div>
</td></tr></table>"""


def sign(t='Até breve,'):
    return p(f'{t}<br><span style="font-weight:600;color:{INK}">Equipe Zeom</span>', 14, 21)


INVEST_DISCLAIMER = small('Conteúdo informativo. Não constitui oferta, recomendação ou análise individualizada de investimentos. Rentabilidade passada não é garantia de resultado futuro. Investimentos em ativos internacionais estão sujeitos a riscos e à variação cambial.')
COUPON_RULES = small('Cupom de uso único, válido para a primeira conversão até {{CUPOM_validade}}. Condições completas em {{LINK_regras_cupom}}.')
SUPPORT = (eyebrow('Dúvidas e suporte') + sp(16)
           + p('Se algo travou no caminho, nossa equipe de atendimento ajuda pelo WhatsApp.', 13, 19)
           + sp(20) + ghost_btn('Falar com o suporte', '{{LINK_whatsapp_suporte}}'))


def E(file, meta, subject, preheader, reason, *rows):
    return dict(file=file, meta=meta, subject=subject, preheader=preheader, reason=reason, rows=list(rows))


EMAILS = [
    # ---------------- PREVENÇÃO · KYC ----------------
    E('kyc-01-lead-d1.html',
      'V1 · KYC · E-mail D+1 — lead da calculadora do site\nGatilho: e-mail coletado pela calculadora, cadastro sem KYC\nObjetivo: baixar o app e concluir a abertura',
      'Sua simulação de câmbio na Zeom', 'Abra sua conta para converter com a cotação que você viu.',
      'Você recebeu este e-mail porque fez uma simulação no site da Zeom e informou este endereço.',
      section('seção 1 · contexto + CTA',
              eyebrow('Sua simulação') + sp(16) + h1('Do cálculo à conversão, no mesmo app') + sp(16)
              + p('Você simulou uma conversão no site da Zeom. Com a conta aberta, você converte, envia e guarda dólar com a cotação visível antes de confirmar.')
              + sp(24) + intent('transferir', 'Abertura 100% pelo app', 'Seu cadastro já começou. Falta baixar o aplicativo e concluir a verificação de identidade.')
              + sp(24) + solid_btn('Baixar o app', '{{LINK_download_app}}')),
      section('seção 2 · passos',
              eyebrow('Como concluir') + sp(16) + steps([
                  ('Baixe o app Zeom', 'Disponível para iPhone e Android.'),
                  ('Entre com este e-mail', 'Seu cadastro continua de onde parou.'),
                  ('Conclua a verificação de identidade', 'Documento e selfie, direto pelo celular.'),
              ]))),
    E('kyc-02-lead-d3.html',
      'V1 · KYC · E-mail D+3 — lead da calculadora do site\nGatilho: lead sem KYC 3 dias depois\nObjetivo: mostrar o valor da conta e levar ao app',
      'O que você encontra na conta Zeom', 'Câmbio, cartão em dólar e investimentos no exterior em um só app.',
      'Você recebeu este e-mail porque fez uma simulação no site da Zeom e informou este endereço.',
      section('seção 1 · lista + CTA',
              eyebrow('Conta global') + sp(16) + h1('Uma conta para usar seu dinheiro fora do Brasil') + sp(16)
              + p('Depois da simulação, veja o que fica disponível quando você conclui a abertura da conta.')
              + sp(24) + item_list([
                  ('transferir', 'Conversão com cotação visível', 'A taxa e o valor final aparecem antes de você confirmar.'),
                  ('cartao', 'Cartão em Dólar', 'Compras no exterior debitadas do seu saldo em dólar.'),
                  ('investir', 'Investimentos', 'Ativos no exterior, acompanhados no painel do app.'),
                  ('chat', 'Zeom AI', 'Consultas e suporte 24 horas por dia.'),
              ]) + sp(24) + solid_btn('Concluir minha abertura', '{{LINK_download_app}}'))),
    E('kyc-03-cupom-d5.html',
      'V1 · KYC · E-mail D5 — cupom Taxa Zero (PROPOSTA · validar regras do cupom e compliance)\nGatilho: 5 dias sem concluir KYC (junto do push)\nObjetivo: concluir KYC e fazer o primeiro depósito',
      'Seu primeiro câmbio com taxa zero', 'Conclua a verificação e use o cupom na sua primeira conversão.',
      'Você recebeu este e-mail porque a verificação de identidade da sua conta Zeom ainda não foi concluída.',
      section('seção 1 · cupom + CTA',
              eyebrow('Verificação de identidade') + sp(16) + h1('Conclua a verificação e converta sem taxa') + sp(16)
              + p('{{first_name}}, sua conta está a um passo de ser liberada. Ao concluir a verificação de identidade, você pode usar o cupom abaixo na sua primeira conversão para dólar.')
              + sp(24) + coupon('Cupom Taxa Zero', 'Use na sua primeira conversão para dólar.')
              + sp(24) + solid_btn('Concluir verificação', '{{LINK_continuar_verificacao}}') + sp(16) + COUPON_RULES),
      section('seção 2 · passos',
              eyebrow('Como usar o cupom') + sp(16) + steps([
                  ('Conclua a verificação no app', 'Documento e selfie, em poucos minutos.'),
                  ('Faça um Pix para a sua conta', 'O valor entra em reais na sua conta Zeom.'),
                  ('Aplique o cupom na conversão', 'A taxa zero aparece antes de você confirmar.'),
              ]))),
    E('kyc-04-cupom-d7.html',
      'V1 · KYC · E-mail D7 — lembrete do cupom Taxa Zero (PROPOSTA · validar regras do cupom e compliance)\nGatilho: 7 dias sem concluir KYC (junto do push)\nObjetivo: concluir KYC e fazer o primeiro depósito',
      'Seu cupom taxa zero vale até {{CUPOM_validade}}', 'Conclua a verificação para usar na sua primeira conversão.',
      'Você recebeu este e-mail porque a verificação de identidade da sua conta Zeom ainda não foi concluída.',
      section('seção 1 · cupom + CTA',
              eyebrow('Cupom Taxa Zero') + sp(16) + h1('Seu cupom segue reservado') + sp(16)
              + p('{{first_name}}, o cupom de taxa zero para a sua primeira conversão continua disponível. Para usar, basta concluir a verificação de identidade no aplicativo.')
              + sp(24) + coupon('Seu cupom', 'Válido até {{CUPOM_validade}} na primeira conversão.')
              + sp(24) + solid_btn('Concluir verificação', '{{LINK_continuar_verificacao}}') + sp(16) + COUPON_RULES),
      section('seção 2 · suporte', SUPPORT)),
    E('kyc-05-fechamento-d10.html',
      'V1 · KYC · E-mail D10 — fechamento 1 (assinado Equipe Zeom)\nGatilho: 10 dias sem concluir KYC\nObjetivo: destravar quem parou por dificuldade',
      'Continue de onde parou', 'Sua verificação fica salva. Se algo travou, a gente ajuda.',
      'Você recebeu este e-mail porque a verificação de identidade da sua conta Zeom ainda não foi concluída.',
      section('seção 1 · contexto + dicas + CTA',
              eyebrow('Verificação de identidade') + sp(16) + h1('Sua verificação fica salva no app') + sp(16)
              + p('{{first_name}}, os dados que você já enviou continuam guardados. Quando quiser, é só abrir o aplicativo e seguir do ponto em que parou.')
              + sp(24) + eyebrow('Dicas para concluir') + sp(16) + item_list([
                  ('perfil', 'Foto do documento', 'Use boa iluminação e mostre o documento inteiro, sem reflexo.'),
                  ('olho', 'Selfie', 'Retire óculos e acessórios e fique em um lugar claro.'),
                  ('escudo', 'Dados pessoais', 'Confira se nome e CPF estão iguais aos do documento.'),
              ]) + sp(24) + solid_btn('Continuar verificação', '{{LINK_continuar_verificacao}}')),
      section('seção 2 · suporte + assinatura', SUPPORT + sp(32) + sign())),
    E('eng-01-inatividade-d7.html',
      'V1 · ENGAJAMENTO · E-mail D7 — inatividade\nGatilho: 7 dias sem qualquer atividade no app (junto do push)\nObjetivo: reabrir consideração de uso, sem pedir nada específico',
      'Sua conta Zeom, sempre à mão', 'Saldo, cotações e cartão em um só lugar, quando você quiser.',
      'Você recebeu este e-mail porque sua conta Zeom está sem movimentações há 7 dias.',
      section('seção 1 · contexto + CTA',
              eyebrow('Sua conta') + sp(16) + h1('Tudo o que você precisa, no app') + sp(16)
              + p('{{first_name}}, sua conta Zeom segue pronta para quando você precisar converter, enviar ou acompanhar seu saldo em outras moedas.')
              + sp(24) + intent('olho', 'Cotações sempre visíveis', 'Acompanhe dólar, euro e outras moedas direto na tela inicial do app.')
              + sp(24) + solid_btn('Abrir o app', '{{LINK_app_home}}'))),
    E('eng-03-fechamento-d21.html',
      'V1 · ENGAJAMENTO · E-mail D21 — fechamento + cupom no próximo depósito (PROPOSTA · validar regras do cupom)\nGatilho: 21 dias sem qualquer atividade no app\nObjetivo: deixar a porta aberta sem cobrança',
      'Quando quiser voltar, é só um Pix', 'E a conversão do seu próximo depósito vem com taxa zero.',
      'Você recebeu este e-mail porque sua conta Zeom está sem movimentações há 21 dias.',
      section('seção 1 · cupom + CTA',
              eyebrow('Sua conta') + sp(16) + h1('Seu próximo câmbio com taxa zero') + sp(16)
              + p('{{first_name}}, sua conta Zeom continua ativa. Para quando fizer sentido voltar a usar, reservamos um cupom de taxa zero para a conversão do seu próximo depósito.')
              + sp(24) + coupon('Cupom Taxa Zero', 'Válido na conversão do seu próximo depósito.')
              + sp(24) + solid_btn('Fazer um Pix', '{{LINK_fazer_pix}}') + sp(16)
              + small('Cupom de uso único, válido até {{CUPOM_validade}}. Condições completas em {{LINK_regras_cupom}}.'))),
    # ---------------- REPESCAGEM · MULTICONTA ----------------
    E('mc-01-ativar-d7.html',
      'V1 · REPESCAGEM · MULTICONTA · E-mail D+7\nGatilho: abriu a conta e não ativou a multiconta\nObjetivo: ativar as contas virtuais em dólar e euro',
      'Sua multiconta está pronta para ativar', 'Contas em dólar e euro para receber e enviar transferências.',
      'Você recebeu este e-mail porque a multiconta da sua conta Zeom ainda não foi ativada.',
      section('seção 1 · contexto + CTA',
              eyebrow('Multiconta') + sp(16) + h1('Uma conta em cada moeda, no mesmo app') + sp(16)
              + p('{{first_name}}, a multiconta da Zeom cria contas virtuais em dólar e euro. Com elas, você recebe e envia transferências internacionais na moeda de origem.')
              + sp(24) + intent('globo', 'Receba do exterior', 'Use os dados da conta virtual para receber pagamentos e transferências em outras moedas.')
              + sp(24) + solid_btn('Ativar multiconta', '{{LINK_app_multiconta}}')),
      section('seção 2 · passos',
              eyebrow('Como ativar') + sp(16) + steps([
                  ('Acesse Multiconta no app', 'A opção fica na tela inicial da sua conta.'),
                  ('Escolha as moedas', 'Dólar, euro ou as duas.'),
                  ('Compartilhe os dados da conta', 'Para receber transferências de fora do Brasil.'),
              ]))),
    E('mc-02-usos-d21.html',
      'V1 · REPESCAGEM · MULTICONTA · E-mail D+21\nGatilho: 21 dias sem ativar a multiconta\nObjetivo: mostrar usos concretos e levar à ativação',
      'Três usos para a sua multiconta', 'Receber, enviar e guardar em dólar ou euro.',
      'Você recebeu este e-mail porque a multiconta da sua conta Zeom ainda não foi ativada.',
      section('seção 1 · lista + CTA',
              eyebrow('Multiconta') + sp(16) + h1('Para que serve uma conta em outra moeda') + sp(16)
              + p('{{first_name}}, a multiconta segue disponível para ativar no app. Veja como ela costuma ser usada:')
              + sp(24) + item_list([
                  ('depositar', 'Receber do exterior', 'Pagamentos de clientes, salários ou reembolsos em dólar ou euro.'),
                  ('enviar', 'Enviar para fora', 'Transferências internacionais direto da moeda de destino.'),
                  ('globo', 'Guardar em outras moedas', 'Saldo separado por moeda, com conversão quando você quiser.'),
              ]) + sp(24) + solid_btn('Ativar multiconta', '{{LINK_app_multiconta}}'))),
    # ---------------- REPESCAGEM · CARTÃO ----------------
    E('cartao-01-ativar-d7.html',
      'V1 · REPESCAGEM · CARTÃO · E-mail D+7 (régua própria, pedido do André)\nGatilho: abriu a conta e não ativou o cartão\nObjetivo: ativar o cartão internacional',
      'Seu cartão em dólar está pronto', 'Ative quando quiser — sem prazo para isso mudar.',
      'Você recebeu este e-mail porque o cartão internacional da sua conta Zeom ainda não foi ativado.',
      section('seção 1 · contexto + intuito + CTA',
              eyebrow('Cartão internacional') + sp(16) + h1('Compras no exterior com o saldo que você já tem') + sp(16)
              + p('{{first_name}}, o cartão internacional da sua conta Zeom já está disponível. As compras no exterior são debitadas do seu saldo em dólar, com a cotação visível antes de cada recarga.')
              + sp(24) + intent('cartao', 'Ativação em poucos passos', 'Tudo é feito pelo aplicativo, quando fizer sentido para você. Não há prazo para ativar.')
              + sp(24) + solid_btn('Ativar cartão', '{{LINK_app_cartao}}')),
      section('seção 2 · passos',
              eyebrow('Como ativar') + sp(16) + steps([
                  ('Abra o aplicativo e acesse Cartão', 'O cartão aparece na tela inicial da sua conta.'),
                  ('Confirme seus dados e crie a senha', 'A senha é pessoal e fica só com você.'),
                  ('Use em compras internacionais', 'Em lojas físicas e online, onde a bandeira for aceita.'),
              ])),
      section('seção 3 · suporte', SUPPORT)),
    E('cartao-02-usos-d21.html',
      'V1 · REPESCAGEM · CARTÃO · E-mail D+21\nGatilho: 21 dias sem ativar o cartão\nObjetivo: mostrar usos concretos e levar à ativação',
      'Onde usar seu cartão em dólar', 'Viagens, compras online e assinaturas internacionais.',
      'Você recebeu este e-mail porque o cartão internacional da sua conta Zeom ainda não foi ativado.',
      section('seção 1 · lista + CTA',
              eyebrow('Cartão em Dólar') + sp(16) + h1('Um cartão para os gastos em outras moedas') + sp(16)
              + p('{{first_name}}, seu cartão internacional segue disponível para ativar no app. Veja onde ele costuma fazer diferença:')
              + sp(24) + item_list([
                  ('globo', 'Viagens', 'Compras no exterior com o saldo em dólar.'),
                  ('cartao', 'Compras online', 'Lojas internacionais que cobram em dólar.'),
                  ('sino', 'Assinaturas', 'Serviços e aplicativos cobrados em moeda estrangeira.'),
              ]) + sp(24) + solid_btn('Ativar cartão', '{{LINK_app_cartao}}'))),
    # ---------------- ONGOING ----------------
    E('ong-01-dolar-recuou.html',
      'V1 · ONGOING · E-mail — variação cambial (dólar recuou) (PROPOSTA · validar com compliance e definir limiar)\nGatilho: queda relevante do dólar — hoje manual, futuramente automatizado\nObjetivo: levar à tela do Pix ou de investimento, sem tom de campanha',
      'O dólar recuou hoje', 'Cotação atualizada no app, com a taxa visível antes de confirmar.',
      'Você recebeu este e-mail porque sua conta Zeom está ativa.',
      section('seção 1 · contexto + CTA + disclaimer',
              eyebrow('Câmbio') + sp(16) + h1('Dólar com queda de {{variacao_usd}} nas últimas 24 horas') + sp(16)
              + p('{{first_name}}, se você planeja converter, pode acompanhar a cotação em tempo real no app e decidir o melhor momento para você.')
              + sp(24) + intent('olho', 'Sem surpresa na conversão', 'A taxa e o valor final aparecem antes de você confirmar.')
              + sp(24) + solid_btn('Ver cotação no app', '{{LINK_cotacoes_app}}') + sp(16)
              + small('Informação de mercado com caráter informativo. Variações passadas não indicam movimentos futuros da cotação.'))),
    E('ong-02-novo-servico.html',
      'V1 · ONGOING · E-mail — novos serviços e produtos (MODELO · preencher a cada lançamento)\nGatilho: lançamento de um novo serviço da Zeom\nObjetivo: apresentar a novidade e levar ao app',
      'Novidade na Zeom: [nome do serviço]', '[Uma frase sobre o que muda para o cliente]',
      'Você recebeu este e-mail porque sua conta Zeom está ativa.',
      section('seção 1 · novidade + CTA',
              eyebrow('Novidade') + sp(16) + h1('[Título · o benefício em 4 a 7 palavras]') + sp(16)
              + p('{{first_name}}, [o que é o novo serviço e para quem ele é, em até duas frases].')
              + sp(24) + item_list([
                  ('estrela', '[Benefício 1]', '[Uma linha explicando o benefício]'),
                  ('seta', '[Benefício 2]', '[Uma linha explicando o benefício]'),
                  ('escudo', '[Benefício 3]', '[Uma linha explicando o benefício]'),
              ]) + sp(24) + solid_btn('Conhecer no app', '{{LINK_novo_servico}}'))),
    E('ong-03-novos-aportes-d30.html',
      'V1 · ONGOING · E-mail D+30 — investidor com saldo ocioso (junto do push)\nGatilho: investidor com saldo parado em conta há 30 dias\nObjetivo: novo aporte com o saldo disponível',
      'Você tem saldo disponível para investir', 'Veja as opções de investimento no app e decida no seu tempo.',
      'Você recebeu este e-mail porque sua conta Zeom tem saldo disponível e acesso à área de investimentos.',
      section('seção 1 · contexto + CTA + disclaimer',
              eyebrow('Investimentos') + sp(16) + h1('Seu saldo pode ser aplicado') + sp(16)
              + p('{{first_name}}, você tem {{saldo_disponivel}} parado na sua conta. Se fizer sentido, esse valor pode ser aplicado nos investimentos internacionais do app.')
              + sp(24) + intent('resgatar', 'Resgate quando precisar', 'O valor investido pode ser resgatado pelo app, para uso ou saque.')
              + sp(24) + solid_btn('Ver investimentos', '{{LINK_app_investimentos}}') + sp(16) + INVEST_DISCLAIMER)),
    E('ong-04-novos-depositos-d30.html',
      'V1 · ONGOING · E-mail D+30 — investidor sem novos depósitos (junto do push)\nGatilho: investidor sem saldo ocioso e sem depósito há 30 dias\nObjetivo: novo depósito para aporte',
      'Consistência também conta nos investimentos', 'Faça um novo aporte quando fizer sentido para você.',
      'Você recebeu este e-mail porque sua conta Zeom tem investimentos ativos.',
      section('seção 1 · contexto + passos + CTA + disclaimer',
              eyebrow('Investimentos') + sp(16) + h1('Um novo aporte, no seu ritmo') + sp(16)
              + p('{{first_name}}, seus investimentos seguem no painel do app. Para quem constrói patrimônio no longo prazo, aportes regulares costumam pesar mais do que o momento de cada aplicação.')
              + sp(24) + steps([
                  ('Faça um Pix para a sua conta', 'O valor entra em reais na sua conta Zeom.'),
                  ('Converta para dólar', 'Com a cotação visível antes de confirmar.'),
                  ('Escolha onde aplicar', 'Nos investimentos internacionais do app.'),
              ]) + sp(24) + solid_btn('Fazer um aporte', '{{LINK_fazer_pix}}') + sp(16) + INVEST_DISCLAIMER)),
    # ---------------- CHURN ----------------
    E('churn-01-win-back-d30.html',
      'V1 · CHURN · WIN BACK · E-mail D+30 (assinado Equipe Zeom, CEO não participa)\nGatilho: inativo por longo período, sem saldo em conta / esgotou qualquer prevenção\nObjetivo: reativar o cliente',
      'Sua conta Zeom está do jeito que você deixou', 'Quando quiser retomar, é só um Pix.',
      'Você recebeu este e-mail porque sua conta Zeom está sem movimentações há 30 dias.',
      section('seção 1 · contexto + lista + CTA + assinatura',
              eyebrow('Sua conta Zeom') + sp(16) + h1('Quando quiser retomar, é só entrar') + sp(16)
              + p('{{first_name}}, faz um tempo que você não movimenta sua conta Zeom. Ela segue ativa, com seus dados preservados.')
              + sp(24) + eyebrow('O que segue disponível') + sp(16) + item_list([
                  ('enviar', 'Transferências Globais', 'Envio e conversão de moedas de forma direta.'),
                  ('cartao', 'Cartão em Dólar', 'Disponível para uso em compras internacionais.'),
                  ('investir', 'Investimentos', 'Painel para acompanhamento de ativos no exterior.'),
                  ('chat', 'Zeom AI', 'Consultas e suporte 24 horas por dia, no aplicativo.'),
              ]) + sp(24) + solid_btn('Acessar minha conta', '{{LINK_acessar_conta}}') + sp(32) + sign())),
    E('churn-02-pesquisa-d35.html',
      'V1 · CHURN · BATTLE IS LOST · E-mail D+35 — pesquisa (assinado Equipe Zeom)\nGatilho: 5 dias após o Win Back, sem reativação\nObjetivo: capturar feedback qualitativo, não reconverter',
      'O que poderíamos ter feito melhor?', 'Sua opinião ajuda a melhorar a Zeom. São 3 perguntas.',
      'Você recebeu este e-mail porque sua conta Zeom está sem movimentações há mais de 30 dias.',
      section('seção 1 · pesquisa + assinatura',
              eyebrow('Sua opinião') + sp(16) + h1('Conte como foi sua experiência') + sp(16)
              + p('{{first_name}}, percebemos que você deixou de usar a Zeom. Queremos entender o que aconteceu e o que poderia ter sido diferente.')
              + sp(24) + solid_btn('Responder a pesquisa', '{{LINK_pesquisa_churn}}') + sp(24)
              + p('Sua conta segue ativa. Se quiser voltar, é só entrar no app.', 13, 19) + sp(32) + sign('Obrigado,'))),
]


def build():
    return {e['file']: page(e['meta'], e['subject'], e['preheader'], e['rows'], e['reason']) for e in EMAILS}
