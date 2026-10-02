# Editor de e-mails (drag & drop)

`editor-emails.html`, na raiz do repositório, é um editor visual autocontido
montado sobre a biblioteca `blocks/` (127 blocos, 24 categorias).

- Arrastar blocos da biblioteca (miniaturas, busca, filtro por categoria) ou clicar em **+**.
- Reordenar, duplicar e excluir blocos.
- Editar textos direto no e-mail; negrito, itálico, link e variáveis (`{{nome}}`…).
- Trocar links de botões (sugestões `{{LINK_*}}`), imagens, ícones e fundos.
- Pré-visualizar Desktop/Celular e Claro/Escuro; assunto, pré-header e modelos iniciais.
- Desfazer/refazer, salvamento automático, rascunhos e projeto `.json`.
- Exportar/copiar o HTML no formato dos e-mails da régua (600px, CSS do design
  system, pré-header oculto, condicional MSO).

As imagens apontam para `https://hiagofbranco.github.io/zeom/assets/…`, então o
HTML exportado funciona em qualquer ferramenta de disparo.

## Atualizar quando a biblioteca mudar

```bash
python3 editor-emails/build.py
```

O script lê `blocks/_index.json` e cada bloco, extrai as linhas da tabela
`.container`, separa o CSS próprio de cada bloco (isolando `.col`, `.gut`, `.g-t`
para não colidirem) e regenera `editor-emails.html` a partir de
`editor-emails/editor.template.html`.
