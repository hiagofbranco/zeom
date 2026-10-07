# Régua V1

Modernização da régua V0 para a V1, montada a partir da planilha
"Revisão Régua CRM para Implementação V1" (aba "Proposta para Régua V1").
São 40 comunicações (20 e-mails e 20 pushes) em 9 etapas: Prevenção · KYC,
Engajamento · 1º depósito, Repescagem · Cartão, Prevenção · Valor,
Repescagem · Multiconta, Repescagem · Investimento, Ongoing,
Engajamento · Inatividade e Churn.

- `regua-v1.html`: fluxograma + comunicações + preview (layout de `comunicacoes-zeom.html`).
- `emails/reguas-v1/`: os 20 e-mails. 17 são novos (`regua-v1/emails.py`) e 3 são
  cópias da V0 que a planilha manda reaproveitar: KYC D14 (era o D6), KYC D21 (era o
  D15) e Inatividade D14 (e-mail 11). Os originais em `emails/reguas/` não mudam.

## Pendências

- **Cupom Taxa Zero** (KYC D5/D7, Inatividade D21): regras, validade e código entram
  como `{{CUPOM_codigo}}`, `{{CUPOM_validade}}` e `{{LINK_regras_cupom}}`.
- **Validar com compliance:** "Dólar recuou" (usa `{{variacao_usd}}` e precisa do limiar
  de disparo) e os pushes de investimento ("resgate 24/7").
- **Leads da calculadora** (KYC D+1/D+3) dependem da calculadora no site.
- **Taxa zero no 1º mês** para quem não depositou: regra a ver com Perillo/Dani.
- **Novas variáveis:** `{{first_name}}`, `{{LINK_download_app}}`, `{{LINK_app_multiconta}}`,
  `{{LINK_app_investimentos}}`, `{{LINK_novo_servico}}`, `{{LINK_pesquisa_churn}}`,
  `{{saldo_disponivel}}`.

## Atualizar

Copy dos e-mails em `regua-v1/emails.py`; pushes, gatilhos e fluxograma em
`regua-v1/build.py`. Depois de editar:

```bash
python3 regua-v1/build.py
```
