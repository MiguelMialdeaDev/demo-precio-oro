"""Version 2 del sitio demo de Ariel Joyerias: misma paleta, otro diseno.

Lo que cambia respecto a build_sitio.py (que imita su tema Dawn): asimetria
en vez de todo centrado, una serif de alto contraste para los titulares, el
azul como color de seccion y no solo de boton, y una jerarquia clara en cada
pagina. Los datos (tiendas, telefonos, financiacion, piezas) se reutilizan
tal cual del v1: no se inventa nada nuevo.

    python build_sitio_v2.py     # escribe sitio-v2/

Forge · redesign · theme: studied-DNA (paleta arielsjewelry.com) con tipografia
propia: Cormorant Garamond (display) + Jost (cuerpo y UI)
· inicio: Split Studio + Bento de coleccion · coleccion: Catalogue con filtros
· producto: Split · tasa: Stat-Led sobre azul · resto: Long Document
· nav: N9 edge-aligned · footer: Ft1 mast-headed · motion: 2 primitivas
· pre-emit critique: P5 H5 E4 S5 R4 V5
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import build_sitio as v1

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "sitio-v2"
ASSETS = "../assets-ariel"   # las fotos y el logo ya viven en la raiz del repo

TEL, TEL_HREF, TEL_FIN, EMAIL, TIENDAS, NAV = v1.TEL, v1.TEL_HREF, v1.TEL_FIN, v1.EMAIL, v1.TIENDAS, v1.NAV
PUREZA, USD_G = v1.PUREZA, v1.USD_G
esc, usd, fmtg, tel_href, maps, nombre_es = v1.esc, v1.usd, v1.fmtg, v1.tel_href, v1.maps, v1.nombre_es


def img(p: str) -> str:
    return p.replace("assets-ariel/", ASSETS + "/")


def shell(titulo: str, cuerpo: str, activa: str, oro: bool = False, claro: bool = True) -> str:
    def item(h: str, t: str) -> str:
        actual = ' aria-current="page"' if h == activa else ""
        return f'<li><a href="{h}"{actual}>{t}</a></li>'
    nav = "".join(item(h, t) for h, t in NAV if h != "index.html")
    tiendas = "".join(f'<li><a href="{tel_href(t)}"><span>{n}</span> {t}</a></li>' for n, _, t in TIENDAS)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{titulo} · Ariel Joyerías (demo v2)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Jost:wght@400;500;600&display=swap">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="sitio.css">
</head>
<body>
<div class="announce"><div class="wrap">
  <span>Cuban Link hecho a mano en Miami · precios al día con el oro</span>
  <a href="{TEL_HREF}">{TEL}</a>
</div></div>
<header class="head wrap">
  <a href="index.html" class="logo"><img src="{ASSETS}/logo.jpg" alt="Ariel Joyerías"></a>
  <nav aria-label="Principal"><ul>{nav}</ul></nav>
  <a class="btn small" href="{TEL_HREF}">Llamar</a>
</header>
<main>
{cuerpo}
</main>
<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <img src="{ASSETS}/logo.jpg" alt="" aria-hidden="true" class="foot-logo">
      <p class="foot-claim">Un anillo y un bolsillo lleno de sueños. Hoy, siete tiendas.</p>
    </div>
    <div>
      <p class="foot-h">Tiendas</p>
      <ul class="foot-list">{tiendas}</ul>
    </div>
    <div>
      <p class="foot-h">Contacto</p>
      <ul class="foot-list">
        <li><a href="{TEL_HREF}">{TEL}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="financiacion.html">Financiación</a></li>
        <li><a href="embajadores.html">Embajadores</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-meta"><span>Ariel Joyerías · demo para enseñar, no es su tienda · oro de gold-api.com</span><a href="https://mialdeastudio.com/" rel="noopener">Hecha por Mialdea Studio</a></div>
</footer>
{'<script src="oro.js"></script>' if oro else ''}
</body>
</html>
"""


CSS = r"""
/* Forge · redesign v2 · paleta arielsjewelry.com · Cormorant Garamond + Jost · P5 H5 E4 S5 R4 V5 */
*, *::before, *::after { box-sizing: border-box; }
html, body { overflow-x: clip; }
body { margin: 0; background: var(--color-paper); color: var(--color-ink); font-family: var(--font-body); font-size: var(--text-md); line-height: 1.55; -webkit-font-smoothing: antialiased; }
h1, h2, h3 { margin: 0; font-style: normal; overflow-wrap: anywhere; min-width: 0; }
h1, h2 { font-family: var(--font-display); font-weight: 600; line-height: 1.05; letter-spacing: -.01em; }
h1 { font-size: clamp(2.4rem, 6vw, 4.4rem); }
h2 { font-size: clamp(1.9rem, 4vw, 3rem); }
h3 { font-weight: 500; font-size: var(--text-lg); }
p { margin: 0; }
a { color: inherit; }
img { max-width: 100%; height: auto; display: block; }
.tnum { font-variant-numeric: tabular-nums lining-nums; }
:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
.wrap { max-width: 1240px; margin-inline: auto; padding-inline: var(--page-gutter); }
.kick { font-size: var(--text-xs); letter-spacing: .2em; text-transform: uppercase; color: var(--color-accent); font-weight: 500; }
.kick::before { content: ""; display: inline-block; width: 22px; height: 1px; background: var(--color-gold); vertical-align: middle; margin-right: 10px; }
.lead { font-size: var(--text-lg); color: var(--color-ink-2); max-width: 52ch; }
.aviso { display: block; font-size: var(--text-sm); color: var(--color-muted); max-width: 60ch; }
.muted { color: var(--color-muted); }
section { padding-block: var(--space-3xl); }
.on-blue { background: var(--color-accent); color: var(--color-paper); }
.on-blue .kick { color: var(--color-gold); }
.on-blue .lead, .on-blue .aviso, .on-blue .muted { color: rgba(255,255,255,.78); }
.on-warm { background: var(--color-paper-warm); }
.rule { border: 0; border-top: 1px solid var(--color-rule); margin: 0; }
.rule-gold { border: 0; border-top: 2px solid var(--color-gold); width: 56px; margin: var(--space-md) 0 0; }

/* cabecera N9 */
.announce { background: var(--color-accent); color: var(--color-paper); font-size: var(--text-sm); }
.announce .wrap { display: flex; justify-content: space-between; gap: var(--space-md); align-items: center; min-height: 40px; }
.announce a { color: inherit; text-decoration: none; white-space: nowrap; font-weight: 500; }
.announce a:hover { text-decoration: underline; }
.head { display: flex; align-items: center; justify-content: space-between; gap: var(--space-lg); padding-block: var(--space-md); border-bottom: 1px solid var(--color-rule); }
.head .logo img { height: 52px; width: auto; }
.head nav ul { display: flex; flex-wrap: wrap; gap: var(--space-xs) var(--space-lg); list-style: none; margin: 0; padding: 0; }
.head nav a { font-size: var(--text-sm); font-weight: 500; letter-spacing: .04em; text-decoration: none; white-space: nowrap; padding: var(--space-2xs) 0; border-bottom: 2px solid transparent; transition: border-color var(--dur-fast) var(--ease-out); }
.head nav a:hover, .head nav a[aria-current="page"] { border-bottom-color: var(--color-gold); }
@media (max-width: 900px) { .head { flex-wrap: wrap; } .head nav { order: 3; width: 100%; } .head nav ul { justify-content: flex-start; } }

/* botones */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: .5em; min-height: 46px; padding: .7rem 1.6rem; background: var(--color-accent); color: var(--color-paper); border: 1px solid var(--color-accent); border-radius: var(--radius); font: inherit; font-size: var(--text-sm); font-weight: 500; letter-spacing: .04em; text-decoration: none; white-space: nowrap; cursor: pointer; transition: background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out), transform var(--dur-fast) var(--ease-out); }
.btn:hover { background: var(--color-accent-hover); }
.btn:active { transform: translateY(1px); }
.btn[disabled], .btn[aria-busy="true"] { opacity: .55; cursor: progress; }
.btn.ghost { background: transparent; color: var(--color-accent); }
.btn.ghost:hover { background: var(--color-accent); color: var(--color-paper); }
.btn.gold { background: var(--color-gold); border-color: var(--color-gold); color: var(--color-ink); }
.btn.gold:hover { background: var(--color-gold-pale); border-color: var(--color-gold-pale); }
.btn.white { background: var(--color-paper); border-color: var(--color-paper); color: var(--color-accent); }
.btn.white:hover { background: var(--color-gold-pale); border-color: var(--color-gold-pale); color: var(--color-ink); }
.btn.small { min-height: 40px; padding: .5rem 1.1rem; }
.acciones { display: flex; flex-wrap: wrap; gap: var(--space-sm); margin-top: var(--space-lg); }

/* portada split */
.hero { display: grid; gap: var(--space-xl); align-items: end; padding-block: var(--space-2xl) var(--space-3xl); }
@media (min-width: 900px) { .hero { grid-template-columns: 7fr 5fr; gap: var(--space-2xl); } }
.hero h1 { margin-top: var(--space-md); max-width: 16ch; }
.hero .lead { margin-top: var(--space-lg); }
.hero figure { margin: 0; position: relative; aspect-ratio: 4 / 5; overflow: hidden; }
.hero figure img { width: 100%; height: 100%; object-fit: cover; }
.hero .chip { position: absolute; left: var(--space-md); bottom: var(--space-md); background: var(--color-paper); padding: var(--space-sm) var(--space-md); border-left: 3px solid var(--color-gold); display: grid; gap: 2px; }
.hero .chip .k { font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--color-muted); }
.hero .chip .v { font-weight: 600; font-size: var(--text-lg); }
.figure.is-live::after { content: ""; display: inline-block; width: 10px; height: 10px; margin-left: .35em; border-radius: 50%; background: var(--color-ok); vertical-align: middle; }
.unit { font-size: .5em; color: var(--color-muted); }

/* ventajas como lista con regla */
.ventajas { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); border-top: 1px solid var(--color-rule); border-bottom: 1px solid var(--color-rule); }
.ventajas > div { padding: var(--space-lg) var(--space-md) var(--space-lg) 0; border-top: 1px solid var(--color-rule); }
.ventajas > div:first-child { border-top: 0; }
@media (min-width: 720px) { .ventajas > div { border-top: 0; border-left: 1px solid var(--color-rule); padding-left: var(--space-md); } .ventajas > div:first-child { border-left: 0; padding-left: 0; } }
.ventajas h3 { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 600; }
.ventajas p { margin-top: var(--space-xs); color: var(--color-ink-2); }

/* bento de colección */
.sec-head { display: flex; flex-wrap: wrap; align-items: end; justify-content: space-between; gap: var(--space-md); margin-bottom: var(--space-xl); }
.sec-head .lead { margin-top: var(--space-sm); }
.bento { display: grid; gap: var(--space-md); grid-template-columns: repeat(auto-fill, minmax(min(240px, 100%), 1fr)); }
@media (min-width: 900px) { .bento { grid-template-columns: repeat(4, minmax(0, 1fr)); } .bento .pieza:first-child { grid-column: span 2; grid-row: span 2; } }
.pieza { display: grid; grid-template-rows: auto 1fr; gap: var(--space-sm); text-decoration: none; min-width: 0; }
.pieza figure { margin: 0; aspect-ratio: 1; overflow: hidden; background: var(--color-paper-2); }
.bento .pieza:first-child figure { aspect-ratio: auto; height: 100%; min-height: 320px; }
.pieza figure img { width: 100%; height: 100%; object-fit: cover; transition: transform var(--dur-base) var(--ease-out); }
.pieza:hover figure img { transform: scale(1.03); }
.pieza .txt { display: grid; grid-template-columns: 1fr auto; gap: var(--space-2xs) var(--space-md); align-items: baseline; }
.pieza h3 { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 600; }
.pieza .spec { grid-column: 1; font-size: var(--text-sm); color: var(--color-muted); }
.pieza .precio { grid-column: 2; grid-row: 1; font-weight: 600; font-size: var(--text-lg); white-space: nowrap; }
.pieza .tag { grid-column: 1 / -1; font-size: var(--text-xs); letter-spacing: .12em; text-transform: uppercase; color: var(--color-accent); }

/* colección con filtros laterales */
.cat { display: grid; gap: var(--space-xl); }
@media (min-width: 900px) { .cat { grid-template-columns: 220px minmax(0, 1fr); align-items: start; } .cat aside { position: sticky; top: var(--space-lg); } }
.filtros { display: grid; gap: var(--space-2xs); }
.filtros button { font: inherit; font-size: var(--text-sm); text-align: left; padding: .55rem .75rem; min-height: 40px; background: transparent; border: 0; border-left: 2px solid var(--color-rule); color: var(--color-ink-2); cursor: pointer; transition: border-color var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out); }
.filtros button:hover { color: var(--color-ink); }
.filtros button[aria-pressed="true"] { border-left-color: var(--color-gold); color: var(--color-ink); font-weight: 500; }
.grid { display: grid; gap: var(--space-xl) var(--space-md); grid-template-columns: repeat(auto-fill, minmax(min(240px, 100%), 1fr)); }

/* producto */
.producto { display: grid; gap: var(--space-xl); padding-block: var(--space-2xl); }
@media (min-width: 900px) { .producto { grid-template-columns: 7fr 5fr; align-items: start; } .producto figure { position: sticky; top: var(--space-lg); } }
.producto figure { margin: 0; aspect-ratio: 4 / 5; overflow: hidden; background: var(--color-paper-2); }
.producto figure img { width: 100%; height: 100%; object-fit: cover; }
.producto h1 { margin-top: var(--space-sm); font-size: clamp(2rem, 4.5vw, 3.2rem); }
.precio-card { margin-top: var(--space-lg); padding: var(--space-lg); border: 1px solid var(--color-rule); border-top: 3px solid var(--color-gold); background: var(--color-paper-warm); }
.precio-card .precio { font-family: var(--font-display); font-weight: 600; font-size: clamp(2rem, 5vw, 3rem); line-height: 1; }
.precio-card .aviso { margin-top: var(--space-xs); }
.producto dl { display: grid; grid-template-columns: max-content 1fr; gap: var(--space-xs) var(--space-lg); margin: var(--space-lg) 0 0; }
.producto dt { color: var(--color-muted); font-size: var(--text-sm); }
.producto dd { margin: 0; }
.producto dl > * { padding-bottom: var(--space-xs); border-bottom: 1px solid var(--color-rule); }

/* tasadora sobre azul */
.tasa-hero { padding-block: var(--space-2xl) calc(var(--space-3xl) + 80px); }
.tasa-hero .figure { font-family: var(--font-display); font-weight: 600; font-size: clamp(3rem, 9vw, 7rem); line-height: 1; white-space: nowrap; margin-top: var(--space-sm); }
.tasa-hero .unit { color: rgba(255,255,255,.6); }
.tasa-hero h1 { margin-top: var(--space-md); max-width: 24ch; font-size: clamp(1.8rem, 4vw, 3rem); }
.tasa-card { margin-top: -80px; padding-bottom: var(--space-2xl); }
.tasa { display: grid; gap: var(--space-lg); background: var(--color-paper); border: 1px solid var(--color-rule); padding: var(--space-lg); }
@media (min-width: 800px) { .tasa { grid-template-columns: 1fr 1fr; padding: var(--space-xl); } }
.campo { display: grid; gap: var(--space-2xs); }
.campo + .campo { margin-top: var(--space-md); }
.campo label { font-size: var(--text-xs); letter-spacing: .14em; text-transform: uppercase; color: var(--color-ink-2); }
.campo input, .campo select, .campo textarea { font: inherit; font-size: var(--text-md); padding: .7rem .9rem; min-height: 46px; width: 100%; border: 0; border-bottom: 2px solid var(--color-ink); background: var(--color-paper-2); color: var(--color-ink); transition: border-color var(--dur-fast) var(--ease-out); }
.campo input:hover, .campo select:hover, .campo textarea:hover { border-color: var(--color-accent); }
.campo input:focus-visible, .campo select:focus-visible, .campo textarea:focus-visible { border-color: var(--color-accent); outline-offset: 2px; }
.campo input[aria-invalid="true"] { border-color: var(--color-danger); }
.campo .err { font-size: var(--text-sm); color: var(--color-danger); min-height: 1.3em; }
.resultado { border-left: 3px solid var(--color-gold); padding-left: var(--space-lg); }
.resultado .lbl { font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--color-muted); }
.resultado .hasta { font-family: var(--font-display); font-weight: 600; font-size: clamp(2.4rem, 6vw, 4rem); line-height: 1; margin-top: var(--space-xs); }
.resultado .hasta.ok { color: var(--color-accent); }
.resultado .detalle { margin-top: var(--space-sm); color: var(--color-ink-2); max-width: 40ch; }
.resultado .btn { margin-top: var(--space-md); }
.pasos { display: grid; gap: 0; margin-top: var(--space-xl); border-top: 1px solid var(--color-rule); }
.pasos > div { display: grid; grid-template-columns: 3.5rem 1fr; gap: var(--space-md); padding: var(--space-lg) 0; border-bottom: 1px solid var(--color-rule); }
.pasos .n { font-family: var(--font-display); font-size: var(--text-2xl); color: var(--color-gold); line-height: 1; }
.pasos h3 { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 600; }
.pasos p { margin-top: var(--space-2xs); color: var(--color-ink-2); max-width: 60ch; }

/* documento */
.doc { max-width: 64ch; }
.doc p + p { margin-top: var(--space-md); }
.doc h2 { margin-top: var(--space-xl); font-size: clamp(1.5rem, 3vw, 2.2rem); }
.doc .lead { margin-top: var(--space-lg); }
.cita { font-family: var(--font-display); font-size: clamp(1.6rem, 3.6vw, 2.6rem); font-weight: 500; line-height: 1.2; max-width: 22ch; border-left: 3px solid var(--color-gold); padding-left: var(--space-lg); margin: var(--space-2xl) 0; }
.dos { display: grid; gap: var(--space-lg); grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); margin-top: var(--space-xl); }
.tarjeta { padding: var(--space-lg) 0 0; border-top: 3px solid var(--color-gold); }
.tarjeta h3 { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 600; }
.tarjeta p { margin-top: var(--space-sm); color: var(--color-ink-2); }
.tarjeta .cifra { font-family: var(--font-display); font-size: clamp(1.6rem, 3vw, 2.2rem); font-weight: 600; color: var(--color-ink); margin-top: var(--space-md); }
.tarjeta .btn { margin-top: var(--space-md); }

/* tiendas */
.tiendas { display: grid; gap: 0; margin-top: var(--space-xl); border-top: 1px solid var(--color-rule); }
.tienda { display: grid; grid-template-columns: 3.5rem 1fr auto; gap: var(--space-md); align-items: center; padding: var(--space-lg) 0; border-bottom: 1px solid var(--color-rule); }
.tienda .n { font-family: var(--font-display); font-size: var(--text-2xl); color: var(--color-gold); line-height: 1; }
.tienda .dir { color: var(--color-ink-2); }
.tienda .tel { font-weight: 500; }
.tienda .enlaces { display: flex; gap: var(--space-sm); }
@media (max-width: 640px) { .tienda { grid-template-columns: 3.5rem 1fr; } .tienda .enlaces { grid-column: 2; } }

/* formulario */
.form { display: grid; gap: var(--space-md); max-width: 560px; margin-top: var(--space-xl); }
.split-doc { display: grid; gap: var(--space-xl); }
@media (min-width: 900px) { .split-doc { grid-template-columns: 5fr 7fr; align-items: start; } }

/* pie Ft1 */
.foot { background: var(--color-paper-warm); border-top: 1px solid var(--color-rule); padding-block: var(--space-2xl) var(--space-lg); font-size: var(--text-sm); }
.foot-grid { display: grid; gap: var(--space-xl); grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); }
.foot-logo { height: 44px; width: auto; }
.foot-claim { margin-top: var(--space-md); font-family: var(--font-display); font-size: var(--text-xl); max-width: 22ch; line-height: 1.2; }
.foot-h { font-size: var(--text-xs); letter-spacing: .16em; text-transform: uppercase; color: var(--color-muted); }
.foot-list { list-style: none; margin: var(--space-sm) 0 0; padding: 0; display: grid; gap: var(--space-2xs); }
.foot-list a { text-decoration: none; white-space: nowrap; }
.foot-list a:hover { text-decoration: underline; }
.foot-list span { color: var(--color-muted); margin-right: .35em; }
.foot-meta { display: flex; flex-wrap: wrap; gap: var(--space-xs) var(--space-lg); justify-content: space-between; margin-top: var(--space-xl); padding-top: var(--space-md); border-top: 1px solid var(--color-rule); color: var(--color-muted); }
.foot-meta a { text-decoration: underline; text-underline-offset: 3px; white-space: nowrap; }

@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 1ms !important; animation-duration: 1ms !important; } .btn:active { transform: none; } }
"""


def card(p: dict) -> str:
    spec = f"{p['kilates']}k" + (f" · {fmtg(p['gramos'])} g" if p.get("gramos") else "")
    factor = round(p["precio"] / (p["gramos"] * PUREZA[p["kilates"]] * USD_G), 4) if p.get("gramos") and p.get("kilates") else 0
    data = f' data-pieza data-gramos="{p["gramos"]}" data-kilates="{p["kilates"]}" data-factor="{factor}"' if factor else ""
    return f"""<a class="pieza" href="producto.html" data-tipo="{p.get('tipo','cadena')}"{data}>
  <figure><img src="{img(p['img'])}" alt="{esc(p['nombre'])}, oro de {p['kilates']} kilates" loading="lazy"></figure>
  <div class="txt"><h3>{esc(p['nombre'])}</h3><p class="precio tnum" data-precio>{usd(p['precio'])}</p><p class="spec">{spec}</p><p class="tag">Orientativo · confirmar en tienda</p></div>
</a>"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "sitio.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (OUT / "oro.js").write_text(v1.JS.strip() + "\n", encoding="utf-8")
    tokens = (AQUI / "tokens.css").read_text(encoding="utf-8")
    tokens = tokens.replace('--font-display: "Michroma", "Arial Black", sans-serif;', '--font-display: "Cormorant Garamond", Georgia, serif;')
    tokens = tokens.replace('--font-body: "EB Garamond", Garamond, "Times New Roman", serif;', '--font-body: "Jost", "Segoe UI", system-ui, sans-serif;')
    (OUT / "tokens.css").write_text(tokens, encoding="utf-8")

    piezas = json.loads((AQUI / "assets-ariel" / "piezas.json").read_text(encoding="utf-8"))["piezas"]
    col = json.loads((AQUI / "assets-ariel" / "coleccion.json").read_text(encoding="utf-8"))
    nombres = {1: "Pulsera cubana", 2: "Pulsera oro amarillo", 3: "Anillo con diamante", 4: "Charm 3,25 pulgadas", 6: "Cadena cubana", 7: "Cadena con cruz"}
    destacadas = [{"nombre": nombres[i], "kilates": p["kilates"], "gramos": p["gramos"], "precio": p["precio_web"], "img": p["img_local"],
                   "tipo": "pulsera" if "Pulsera" in nombres[i] else ("anillo" if "Anillo" in nombres[i] else "cadena")}
                  for i, p in enumerate(piezas, 1) if i in nombres]
    # la cubana grande primero: es la que manda en el bento
    destacadas.sort(key=lambda p: -p["precio"])
    coleccion = [{"nombre": nombre_es(c["titulo"]), "kilates": c["kilates"] or 14, "gramos": c["gramos"], "precio": c["precio"], "img": c["img"],
                  "tipo": "pulsera" if re.search(r"bracelet|pulsera", c["titulo"], re.I) else "cadena"} for c in col]

    ventajas = [("Hecho a mano", "Cuban Link fabricado por nosotros, en Miami."), ("Envío asegurado", "Ultraseguro y asegurado hasta tu puerta."),
                ("Cientos de reseñas", "Cinco estrellas de clientes de todo el sur de Florida."), ("A plazos", "3, 6 o 12 meses con Affirm, o en 4 sin intereses.")]

    inicio = f"""
<section class="wrap hero">
  <div>
    <p class="kick">Siete joyerías en Miami</p>
    <h1>Cuban Link hecho a mano, al precio del oro de hoy</h1>
    <p class="lead">Cadenas, pulseras, anillos y charms en oro de 14 y 18 kilates. El precio de cada pieza se ajusta con el oro cada hora y se confirma en tienda con la pieza en la báscula.</p>
    <div class="acciones"><a class="btn" href="coleccion.html">Ver la colección</a><a class="btn ghost" href="tasa-tu-oro.html">Tasa tu oro</a></div>
  </div>
  <figure>
    <img src="{img(destacadas[0]['img'])}" alt="{esc(destacadas[0]['nombre'])} de oro de 14 kilates" fetchpriority="high">
    <div class="chip"><span class="k">El oro ahora mismo</span><span class="v figure tnum" data-oro>$4,349.70<span class="unit">/oz</span></span><span class="k">actualizado a las <span data-hora>21:12</span></span></div>
  </figure>
</section>
<div class="wrap"><div class="ventajas">{''.join(f'<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in ventajas)}</div></div>
<section class="wrap">
  <div class="sec-head"><div><p class="kick">Piezas reales de la tienda</p><h2>Nuestra colección de cubanas</h2></div><a class="btn ghost" href="coleccion.html">Ver todo</a></div>
  <div class="bento">{''.join(card(p) for p in destacadas)}</div>
</section>
<section class="on-warm"><div class="wrap split-doc">
  <div>
    <p class="kick">La historia</p>
    <h2>Un anillo y un bolsillo lleno de sueños</h2>
    <p class="cita" style="margin:var(--space-lg) 0 0">Todo el mundo merece acceso a joyas de calidad.</p>
  </div>
  <div class="doc">
    <p class="lead" style="margin-top:0">Ariel trabajaba de cajero en Publix y se gastó el sueldo de una semana en un anillo. Un cliente se fijó en él en la caja, Ariel se lo vendió por el doble, y aquellos cien dólares plantaron la semilla de todo lo que vino después.</p>
    <p>Empezó vendiendo joyas en la calle. Hoy son siete tiendas en Miami, un negocio de familia con su esposa Yuliet y su cuñada Yulimar, y un canal de YouTube con cerca de 800.000 personas viendo cómo se compra y se vende el oro cada semana.</p>
    <div class="acciones"><a class="btn" href="nosotros.html">Leer la historia</a><a class="btn ghost" href="https://www.youtube.com/@arielsjoyeria" rel="noopener" target="_blank">Ver el canal</a></div>
  </div>
</div></section>
<section class="on-blue"><div class="wrap" style="display:grid;gap:var(--space-lg);grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));align-items:center">
  <div><p class="kick">Compramos oro</p><h2>¿Tienes oro? Te decimos cuánto</h2><p class="lead">Dos datos y sale un número. En cualquiera de las siete tiendas lo confirmamos con la pieza en la mano.</p></div>
  <div class="acciones" style="margin:0;justify-content:flex-start"><a class="btn white" href="tasa-tu-oro.html">Tasar mi oro</a><a class="btn gold" href="tiendas.html">Ver tiendas</a></div>
</div></section>
"""

    coleccion_html = f"""
<section class="wrap">
  <p class="kick">Colección</p>
  <h1>Cadenas y pulseras cubanas</h1>
  <p class="lead">Hechas a mano en oro de 14 kilates. {len(coleccion)} piezas reales de la web, con el precio ajustado al oro de hoy.</p>
  <div class="cat" style="margin-top:var(--space-xl)">
    <aside><p class="kick" style="margin-bottom:var(--space-sm)">Filtrar</p><div class="filtros" role="group" aria-label="Filtrar"><button type="button" data-f="todo" aria-pressed="true">Todo</button><button type="button" data-f="cadena" aria-pressed="false">Cadenas</button><button type="button" data-f="pulsera" aria-pressed="false">Pulseras</button></div>
      <small class="aviso" style="margin-top:var(--space-lg)">Precios orientativos con el oro de hoy. El final se confirma en tienda al ver la pieza.</small></aside>
    <div class="grid">{''.join(card(p) for p in coleccion)}</div>
  </div>
</section>
"""

    prod = next(p for p in destacadas if p["nombre"] == "Cadena cubana")
    factor = round(prod["precio"] / (prod["gramos"] * PUREZA[prod["kilates"]] * USD_G), 4)
    producto = f"""
<section class="wrap producto" data-pieza data-gramos="{prod['gramos']}" data-kilates="{prod['kilates']}" data-factor="{factor}">
  <figure><img src="{img(prod['img'])}" alt="Cadena cubana de oro de 14 kilates, 22,9 dwt" fetchpriority="high"></figure>
  <div>
    <p class="kick">Cuban Link · hecha a mano</p>
    <h1>Cadena cubana 14k, 22,9 dwt</h1>
    <div class="precio-card">
      <p class="precio tnum" data-precio>{usd(prod['precio'])}</p>
      <small class="aviso">Orientativo con el oro de las <span data-hora class="tnum">21:12</span>. Se confirma en tienda al ver la pieza.</small>
    </div>
    <dl>
      <dt>Oro</dt><dd>14 kilates (585 milésimas)</dd>
      <dt>Peso</dt><dd>22,9 dwt · 35,6 g</dd>
      <dt>Metal hoy</dt><dd class="tnum" data-metal>$2,913</dd>
      <dt>Financiación</dt><dd>3, 6 o 12 meses con Affirm, o Paga en 4</dd>
      <dt>Recogida</dt><dd>En cualquiera de las siete tiendas de Miami</dd>
    </dl>
    <div class="acciones"><a class="btn" href="{TEL_HREF}">Reservar por teléfono</a><a class="btn ghost" href="financiacion.html">Ver financiación</a></div>
  </div>
</section>
<section class="on-warm"><div class="wrap">
  <p class="kick">Cómo se calcula este precio</p>
  <div class="pasos">
    <div><p class="n">1</p><div><h3>Metal</h3><p>Gramos, por pureza del kilate, por precio del gramo de hoy.</p></div></div>
    <div><p class="n">2</p><div><h3>Lo demás no cambia</h3><p>Mano de obra y margen quedan fijos: se calibraron con el precio de la web.</p></div></div>
    <div><p class="n">3</p><div><h3>Se confirma en tienda</h3><p>Con la pieza en la báscula. El precio online es orientativo.</p></div></div>
  </div>
</div></section>
"""

    tasa = f"""
<section class="on-blue tasa-hero"><div class="wrap">
  <p class="kick">El oro ahora mismo</p>
  <p class="figure tnum" data-oro>$4,349.70<span class="unit">/oz</span></p>
  <h1>¿Tienes oro? Te decimos cuánto te pagamos hoy</h1>
  <p class="lead">Dos datos y sale un número. El definitivo, con la pieza en la báscula en cualquiera de las siete tiendas.</p>
</div></section>
<div class="wrap tasa-card">
  <form class="tasa" id="form-tasa" novalidate>
    <div>
      <div class="campo"><label for="gramos">Gramos</label><input id="gramos" name="gramos" type="number" inputmode="decimal" min="0.1" step="0.1" placeholder="35,6" autocomplete="off"><p class="err" id="err-gramos" aria-live="polite"></p></div>
      <div class="campo"><label for="kilates">Kilates</label><select id="kilates" name="kilates"><option value="10">10k</option><option value="14" selected>14k</option><option value="18">18k</option><option value="22">22k</option><option value="24">24k</option></select><p class="err"></p></div>
    </div>
    <div class="resultado" aria-live="polite">
      <p class="lbl">Te pagamos hoy</p>
      <p class="hasta tnum" id="hasta">Hasta $0</p>
      <p class="detalle" id="detalle">Escribe los gramos y te lo calculamos con el oro de ahora.</p>
      <small class="aviso">Se confirma en tienda con la pieza en la báscula.</small>
      <p><a class="btn" href="{TEL_HREF}">Reservar cita en tienda</a></p>
    </div>
  </form>
</div>
<section class="wrap" style="padding-top:0">
  <p class="kick">Así funciona</p>
  <div class="pasos">
    <div><p class="n">1</p><div><h3>Miramos el oro</h3><p>Cada hora, en una fuente pública. El número de arriba es el de ahora.</p></div></div>
    <div><p class="n">2</p><div><h3>Calculamos el metal</h3><p>Gramos, por pureza del kilate, por precio del gramo. Pagamos del 78 al 90 % según el kilate.</p></div></div>
    <div><p class="n">3</p><div><h3>Lo confirmamos contigo</h3><p>Trae la pieza a cualquier tienda. La pesamos delante de ti y cerramos el precio.</p></div></div>
  </div>
</section>
"""

    financiacion = f"""
<section class="wrap">
  <p class="kick">Financiación</p>
  <h1>Paga tu joya a plazos</h1>
  <p class="lead">Dos formas de llevártela hoy y pagarla con calma. Sin letra pequeña: lo que ves al pagar es lo que pagas.</p>
  <div class="dos">
    <div class="tarjeta">
      <h3>Con Affirm, en 3, 6 o 12 meses</h3>
      <p>Sin intereses diferidos ni comisiones ocultas. Tasas desde el 0 % o del 10 al 36 % APR según tu crédito; la tuya la ves antes de confirmar.</p>
      <p class="cifra tnum">$950 → $88.15 al mes</p>
      <p>Ejemplo real de su web: 12 meses al 20 % APR.</p>
      <a class="btn" href="https://www.affirm.com/" rel="noopener">Precalificar con Affirm</a>
    </div>
    <div class="tarjeta">
      <h3>Sin crédito, alquiler con opción a compra</h3>
      <p>Con Progressive puedes llevarte oro y diamantes aunque no tengas crédito o lo tengas malo. Pagas la primera cuota al comprar y tienes 90 días para comprarla anticipadamente.</p>
      <p class="cifra">Cuatro pasos</p>
      <p>Te aprueban, eliges la pieza, llamas al {TEL_FIN} para cerrar el pedido y pagas a plazos.</p>
      <a class="btn ghost" href="tel:+1{TEL_FIN.replace('-', '')}">Llamar al {TEL_FIN}</a>
    </div>
  </div>
  <small class="aviso" style="margin-top:var(--space-xl)">Las condiciones las fija cada entidad al aprobar. La joyería no cobra nada por financiar.</small>
</section>
"""

    nosotros = """
<section class="wrap split-doc">
  <div>
    <p class="kick">Nosotros</p>
    <h1>Un anillo y un bolsillo lleno de sueños</h1>
    <p class="cita">Todo el mundo merece acceso a joyas de calidad.</p>
  </div>
  <div class="doc">
    <p class="lead" style="margin-top:0">El viaje de Ariel empezó modestamente: un anillo y un bolsillo lleno de sueños.</p>
    <p>Trabajaba de cajero en Publix y le gustaban tanto las joyas que se gastó el sueldo de una semana en un anillo. Lo llevaba todos los días, también en el trabajo, y un cliente se fijó en él en la caja. Ariel se lo ofreció por el doble de lo que le había costado. El cliente pagó cien dólares. Aquella venta duplicó su sueldo semanal y plantó la semilla de todo lo que vino después.</p>
    <p>Empezó vendiendo joyas en la calle, ganando experiencia y clientes poco a poco, hasta abrir su primera joyería. Hoy son siete sucursales en todo Miami.</p>
    <h2>Un negocio de familia</h2>
    <p>Ariel's Jewelry lo dirigen Ariel, su esposa Yuliet y su cuñada Yulimar, con un equipo leal que lleva más de diez años a bordo. Trato personal y las mejores joyas al precio más competitivo, especializados en Cuban Link hecho a mano.</p>
    <div class="acciones"><a class="btn" href="coleccion.html">Ver la colección</a><a class="btn ghost" href="tiendas.html">Las siete tiendas</a></div>
  </div>
</section>
"""

    tiendas = f"""
<section class="wrap">
  <p class="kick">Tiendas</p>
  <h1>Siete tiendas en el sur de Florida</h1>
  <p class="lead">Elige la más cercana. Llama con un toque o abre la ruta en el mapa.</p>
  <div class="tiendas">{''.join(f'<div class="tienda"><p class="n">{i}</p><div><p class="dir">{esc(d)}</p><p class="tel tnum">{t}</p></div><div class="enlaces"><a class="btn small" href="{tel_href(t)}">Llamar</a><a class="btn small ghost" href="{maps(d)}" rel="noopener" target="_blank">Cómo llegar</a></div></div>' for i, (n, d, t) in enumerate(TIENDAS, 1))}</div>
</section>
"""

    contacto = f"""
<section class="wrap split-doc">
  <div>
    <p class="kick">Contacto</p>
    <h1>Ponte en contacto</h1>
    <p class="lead">Por teléfono es lo más rápido. Si prefieres escribir, te contestamos al correo.</p>
    <div class="acciones"><a class="btn" href="{TEL_HREF}">{TEL}</a><a class="btn ghost" href="mailto:{EMAIL}">Escribir un correo</a></div>
    <small class="aviso" style="margin-top:var(--space-xl)">13200 Biscayne Blvd, North Miami, FL 33181<br>{EMAIL}</small>
  </div>
  <form class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain" style="margin-top:0">
    <div class="campo"><label for="c-nombre">Nombre</label><input id="c-nombre" name="nombre" type="text" autocomplete="name"></div>
    <div class="campo"><label for="c-tel">Teléfono</label><input id="c-tel" name="telefono" type="tel" inputmode="tel" autocomplete="tel"></div>
    <div class="campo"><label for="c-msg">Qué necesitas</label><textarea id="c-msg" name="mensaje" rows="4"></textarea></div>
    <div><button class="btn" type="submit">Enviar</button></div>
  </form>
</section>
"""

    embajadores = f"""
<section class="wrap split-doc">
  <div>
    <p class="kick">Embajadores</p>
    <h1>Embajadores y patrocinios</h1>
    <p class="lead">¿Quieres ser embajador de la marca o buscas patrocinio para tu contenido? Déjanos tus datos y hablamos.</p>
  </div>
  <form class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain" style="margin-top:0">
    <div class="campo"><label for="e-nombre">Nombre</label><input id="e-nombre" name="nombre" type="text" autocomplete="name"></div>
    <div class="campo"><label for="e-email">Correo</label><input id="e-email" name="correo" type="email" autocomplete="email" required></div>
    <div class="campo"><label for="e-redes">Tus redes</label><input id="e-redes" name="redes" type="text" placeholder="@usuario en Instagram, TikTok, YouTube"></div>
    <div><button class="btn" type="submit">Enviar</button></div>
  </form>
</section>
"""

    paginas = {
        "index.html": ("Inicio", inicio, True), "coleccion.html": ("Colección de cubanas", coleccion_html, True),
        "producto.html": ("Cadena cubana 14k", producto, True), "tasa-tu-oro.html": ("Tasa tu oro", tasa, True),
        "financiacion.html": ("Financiación", financiacion, False), "nosotros.html": ("Nosotros", nosotros, False),
        "tiendas.html": ("Tiendas", tiendas, False), "contacto.html": ("Contacto", contacto, False), "embajadores.html": ("Embajadores", embajadores, False),
    }
    for f, (t, cuerpo, oro) in paginas.items():
        (OUT / f).write_text(shell(t, cuerpo, f, oro=oro), encoding="utf-8")
    print(f"sitio v2 generado en {OUT} ({len(paginas)} paginas)")


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
