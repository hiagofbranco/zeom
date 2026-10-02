#!/usr/bin/env python3
"""Gera editor-emails.html (raiz do repositório) a partir da biblioteca blocks/.

Uso: python3 editor-emails/build.py
"""
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ZEOM = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent
OUT = ZEOM / 'editor-emails.html'
ASSET_BASE = 'https://hiagofbranco.github.io/zeom/assets/'


def parse_css(css):
    """Lista de (prelude, corpo); corpo é str (declarações) ou lista (regras aninhadas)."""
    out, i = [], 0
    while i < len(css):
        j = css.find('{', i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        depth, k = 1, j + 1
        while depth:
            depth += {'{': 1, '}': -1}.get(css[k], 0)
            k += 1
        body = css[j + 1:k - 1]
        out.append((prelude, parse_css(body) if prelude.startswith('@') else body))
        i = k
    return out


def dump_css(rules):
    return ''.join(f"{p}{{{dump_css(b) if isinstance(b, list) else b}}}" for p, b in rules)


def diff_css(rules, base):
    """Regras de `rules` que não existem em `base` (comparando dentro de cada @media)."""
    base_flat = {p: b for p, b in base if not isinstance(b, list)}
    base_at = {p: b for p, b in base if isinstance(b, list)}
    out = []
    for p, b in rules:
        if isinstance(b, list):
            inner = diff_css(b, base_at.get(p, []))
            if inner:
                out.append((p, inner))
        elif base_flat.get(p) != b:
            out.append((p, b))
    return out


def classes_in(css):
    return set(re.findall(r'\.([A-Za-z][\w-]*)', re.sub(r'url\([^)]*\)', '', css)))


def main():
    index = json.loads((ZEOM / 'blocks/_index.json').read_text())
    pages = {}
    for b in index:
        pages[(b['dir'], b['slug'])] = (ZEOM / 'blocks' / b['dir'] / f"{b['slug']}.html").read_text()

    style_of = lambda s: re.search(r'<style>(.*?)</style>', s, re.S).group(1)
    base_css = style_of(pages[('header', 'logo')])
    base_rules = parse_css(base_css)
    base_classes = classes_in(base_css)

    blocks = []
    for b in index:
        page = pages[(b['dir'], b['slug'])]
        bid = f"{b['dir']}-{b['slug']}"
        extra = dump_css(diff_css(parse_css(style_of(page)), base_rules))

        body = page.split('<body', 1)[1]
        start = re.search(r'<table[^>]*class="container[^"]*"[^>]*>', body)
        # conteúdo = linhas da tabela container (fecha no penúltimo </table>; o último é o .desk)
        end = body.rfind('</table>', 0, body.rfind('</table>'))
        inner = body[start.end():end]
        inner = re.sub(r'<!--.*?-->', '', inner, flags=re.S)

        # isola classes próprias do bloco (.col, .gut, .g-t...) para não colidirem entre blocos
        for c in sorted(classes_in(extra) - base_classes, key=len, reverse=True):
            new = f"{c}--{bid}"
            extra = re.sub(rf'url\([^)]*\)|\.{re.escape(c)}(?![\w-])', lambda m: m.group(0) if m.group(0).startswith('url(') else '.' + new, extra)
            inner = re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(new if t == c else t for t in m.group(1).split()) + '"', inner)

        inner = inner.replace('../../assets/', ASSET_BASE)
        extra = extra.replace('../../assets/', ASSET_BASE)
        blocks.append({'id': bid, 'cat': b['cat'], 'name': b['name'], 'note': b.get('note', ''),
                       'html': inner.strip(), 'css': extra})

    base_css = base_css.replace('../../assets/', ASSET_BASE)
    icons = sorted(p.name for p in (ZEOM / 'assets/icons/png').glob('*.png'))
    official = json.loads((ZEOM / 'assets/icons/_index.json').read_text())
    tpl = (HERE / 'editor.template.html').read_text()
    out = tpl.replace('/*__BASE_CSS__*/""', json.dumps(base_css, ensure_ascii=False)) \
             .replace('/*__BLOCKS__*/[]', json.dumps(blocks, ensure_ascii=False).replace('</', '<\\/')) \
             .replace('/*__ICONS__*/{}', json.dumps({'files': icons, 'official': official, 'base': ASSET_BASE + 'icons/png/'}))
    OUT.write_text(out)
    print(f"{len(blocks)} blocos · {len(out)//1024} KB → {OUT}")


if __name__ == '__main__':
    main()
