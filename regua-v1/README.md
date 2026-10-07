# Régua V1

Régua separada da régua atual (`comunicacoes-zeom.html`), com as comunicações
marcadas como "V1 · futuro": 10 comunicações (6 e-mails, 4 pushes).

| Etapa | Canal · dia | Assunto / título | E-mail |
|---|---|---|---|
| Valor & Repescagem | E-mail D7 | Seu cartão internacional está esperando | `emails/reguas-v1/v1-01-repescagem-cartao-d7.html` (novo) |
| Valor & Repescagem | E-mail D+X | Seus investimentos internacionais estão disponíveis | `v1-02-repescagem-investimento.html` (novo) |
| Valor & Repescagem | E-mail D7 | Seus recursos internacionais continuam por aqui | `v1-03-prevencao-valor-d7.html` (novo) |
| Engajamento | Push D7 | Sua conta segue disponível | — |
| Engajamento | E-mail D14 | Seus recursos continuam disponíveis | `v1-04-engajamento-d14.html` (cópia do 11) |
| Engajamento | Push D21 | No seu ritmo | — |
| Oportunidades | Push · evento | Acompanhe as moedas que você usa | — |
| Oportunidades | E-mail · evento | Câmbio, de forma simples | `v1-05-oportunidades-cambio.html` (cópia do 15) |
| Churn · Win Back | Push | Sua conta Zeom continua ativa — **proposta** | — |
| Churn · Win Back | E-mail | Sua conta Zeom continua ativa — **proposta** | `v1-06-churn-win-back.html` (novo) |

Os e-mails seguem os mesmos padrões de `emails/reguas/` (header logo simples, card de
intuito, CTA sólido com fallback VML para Outlook, lista linha-divisória, rodapé dark).

Variáveis novas, a cadastrar na ferramenta de disparo: `{{LINK_app_investimentos}}`
(v1-02) e `{{LINK_pesquisa_win_back}}` (v1-06).

## Atualizar

Copy e e-mails ficam em `regua-v1/emails.py`; dados da régua e fluxograma em
`regua-v1/build.py`. Depois de editar:

```bash
python3 regua-v1/build.py
```

Isso regera `emails/reguas-v1/*.html` e `regua-v1.html` (a página reaproveita o layout de
`comunicacoes-zeom.html`).
