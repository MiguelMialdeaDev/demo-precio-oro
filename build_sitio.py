"""Genera el sitio demo de Ariel Joyerías en sitio/ a partir de su contenido real.

Todo el texto de negocio sale de sus propias paginas (quienes somos, financiacion,
tiendas, contacto, embajadores) y las piezas de su catalogo. Lo que la demo
anade es estructura, claridad y la herramienta del oro: no inventa cifras.

    python build_sitio.py      # escribe sitio/*.html, sitio/sitio.css, sitio/oro.js

Forge · macrostructure por pagina (inicio: Marquee + Stat, coleccion: Catalogue,
producto: Split, tasa: Stat-Led, resto: Long Document corto) · theme: studied-DNA
(arielsjewelry.com) · nav: N12 · footer: Ft1 mast-headed con tiendas.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
OUT = AQUI / "sitio"
ASSETS = AQUI / "assets-ariel"

TEL = "(305) 418-9188"
TEL_HREF = "tel:+13054189188"
TEL_FIN = "786-953-2651"
EMAIL = "arielsjewelry.online@gmail.com"

TIENDAS = [
    ("Tienda 1", "13220 SW 8th St, Miami, FL 33184", "(305) 223-0437"),
    ("Tienda 2", "8334 SW 8th St, Miami, FL 33144", "(305) 264-1466"),
    ("Tienda 3", "13637 SW 26th St, Miami, FL 33175", "(305) 226-0313"),
    ("Tienda 4", "285 NW 27th Ave, Miami, FL 33125", "(305) 642-1475"),
    ("Tienda 5", "2476 W 60th St, Hialeah, FL 33016", "(305) 826-1475"),
    ("Tienda 6", "7273 NW 36th St, Doral, FL 33166", "(305) 418-9188"),
    ("Tienda 7", "13150 Biscayne Blvd, North Miami, FL 33181", "(305) 893-7937"),
]

NAV = [("index.html", "Inicio"), ("coleccion.html", "Colección"), ("tasa-tu-oro.html", "Tasa tu oro"),
       ("financiacion.html", "Financiación"), ("tiendas.html", "Tiendas"), ("nosotros.html", "Nosotros"),
       ("contacto.html", "Contacto")]


def tel_href(t: str) -> str:
    return "tel:+1" + re.sub(r"\D", "", t)


def maps(direccion: str) -> str:
    return "https://www.google.com/maps/search/?api=1&query=" + direccion.replace(" ", "+")


def shell(titulo: str, cuerpo: str, activa: str, extra_head: str = "", oro: bool = False) -> str:
    def item(h: str, t: str) -> str:
        actual = ' aria-current="page"' if h == activa else ""
        return f'<li><a href="{h}"{actual}>{t}</a></li>'
    nav = "".join(item(h, t) for h, t in NAV)
    tiendas_pie = " · ".join(f'<a href="{tel_href(t)}">{n} {t}</a>' for n, _, t in TIENDAS)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{titulo} · Ariel Joyerías (demo)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Michroma&family=EB+Garamond:wght@400;500;600&display=swap">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="sitio.css">
{extra_head}
</head>
<body>
<p class="utility">Bienvenido a nuestra tienda · siete joyerías en Miami</p>
<div class="announce"><div class="wrap">
  <span class="msg">Cuban Link hecho a mano · precios al día con el oro</span>
  <span><a href="{TEL_HREF}">☎ {TEL}</a> &nbsp;|&nbsp; <a href="mailto:{EMAIL}">✉ {EMAIL}</a></span>
</div></div>
<header class="head">
  <a href="index.html" class="logo"><img src="assets-ariel/logo.jpg" alt="Ariel Joyerías"></a>
  <nav aria-label="Principal"><ul>{nav}</ul></nav>
</header>
<main>
{cuerpo}
</main>
<footer class="foot">
  <div class="wrap">
    <p class="foot-mast"><img src="assets-ariel/logo.jpg" alt="" aria-hidden="true"></p>
    <p class="foot-tiendas">{tiendas_pie}</p>
    <p class="foot-meta"><span>Ariel Joyerías · demo para enseñar, no es su tienda · oro de gold-api.com</span> <a href="https://mialdeastudio.com/" rel="noopener">Hecha por Mialdea Studio</a></p>
  </div>
</footer>
{'<script src="oro.js"></script>' if oro else ''}
</body>
</html>
"""


# ───────────────────────── CSS compartido ─────────────────────────
CSS = r"""
/* Forge · sitio demo Ariel Joyerías · theme: studied-DNA (arielsjewelry.com) · P4 H5 E4 S5 R4 V4 */
*, *::before, *::after { box-sizing: border-box; }
html, body { overflow-x: clip; }
body { margin: 0; background: var(--color-paper); color: var(--color-ink); font-family: var(--font-body); font-size: var(--text-md); line-height: 1.5; -webkit-font-smoothing: antialiased; }
h1, h2, h3 { margin: 0; font-style: normal; overflow-wrap: anywhere; min-width: 0; }
h1, h2 { font-family: var(--font-display); font-weight: 400; text-transform: uppercase; letter-spacing: .04em; line-height: 1.2; }
h1 { font-size: clamp(1.3rem, 3.4vw, 2.1rem); }
h2 { font-size: clamp(1.15rem, 2.8vw, 1.7rem); }
h3 { font-weight: 500; font-size: var(--text-lg); }
p { margin: 0; }
a { color: inherit; }
img { max-width: 100%; height: auto; display: block; }
.tnum { font-variant-numeric: tabular-nums lining-nums; }
:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 3px; }
.wrap { max-width: 1200px; margin: 0 auto; padding-inline: var(--page-gutter); }
.center { text-align: center; }
.aviso { display: block; font-size: var(--text-sm); color: var(--color-muted); max-width: var(--measure); margin-inline: auto; }
.intro { text-align: center; max-width: var(--measure); margin: var(--space-sm) auto 0; font-size: var(--text-lg); color: var(--color-ink-2); }
section.bloque { padding-block: var(--space-2xl); }
.band { background: var(--color-paper-2); }
.band-warm { background: var(--color-paper-warm); }

.utility { border-bottom: var(--rule-hair) solid var(--color-rule); font-size: var(--text-xs); padding: var(--space-2xs) var(--page-gutter); color: var(--color-ink-2); }
.announce { background: var(--color-accent); color: var(--color-paper); font-size: var(--text-sm); }
.announce .wrap { display: flex; flex-wrap: wrap; gap: var(--space-xs) var(--space-lg); justify-content: space-between; align-items: center; min-height: 44px; }
.announce a { color: inherit; text-decoration: none; white-space: nowrap; }
.announce a:hover { text-decoration: underline; }
.announce .msg { font-weight: 500; }
.head { padding: var(--space-lg) var(--page-gutter) var(--space-md); text-align: center; }
.head .logo img { height: clamp(52px, 8vw, 96px); width: auto; margin: 0 auto; }
.head nav ul { display: flex; flex-wrap: wrap; justify-content: center; gap: var(--space-sm) var(--space-md); list-style: none; margin: var(--space-md) 0 0; padding: 0; }
@media (min-width: 720px) { .head nav ul { gap: var(--space-lg); } }
.head nav a { font-size: var(--text-sm); letter-spacing: .1em; text-transform: uppercase; text-decoration: none; white-space: nowrap; padding: var(--space-2xs) 0; border-bottom: 2px solid transparent; transition: border-color var(--dur-fast) var(--ease-out); }
.head nav a:hover, .head nav a[aria-current="page"] { border-bottom-color: var(--color-accent); }

.btn { display: inline-flex; align-items: center; justify-content: center; gap: .5em; min-height: 46px; padding: .75rem 1.9rem; background: var(--color-accent); color: var(--color-paper); border: 1px solid var(--color-accent); border-radius: var(--radius); font: inherit; font-size: var(--text-md); font-weight: 500; text-decoration: none; white-space: nowrap; cursor: pointer; transition: background var(--dur-fast) var(--ease-out), transform var(--dur-fast) var(--ease-out); }
.btn:hover { background: var(--color-accent-hover); }
.btn:active { transform: translateY(1px); }
.btn[disabled], .btn[aria-busy="true"] { opacity: .55; cursor: progress; }
.btn.ghost { background: transparent; color: var(--color-accent); }
.btn.ghost:hover { background: var(--color-accent); color: var(--color-paper); }
.acciones { display: flex; flex-wrap: wrap; gap: var(--space-sm); justify-content: center; margin-top: var(--space-lg); }

/* inicio */
.hero { display: grid; gap: var(--space-xl); align-items: center; padding-block: var(--space-2xl); }
@media (min-width: 900px) { .hero { grid-template-columns: 1.1fr 1fr; } }
.hero .kick { font-size: var(--text-sm); letter-spacing: .18em; text-transform: uppercase; color: var(--color-ink-2); }
.hero h1 { font-size: clamp(1.5rem, 4vw, 2.6rem); margin-top: var(--space-sm); }
.hero .lead { font-size: var(--text-lg); color: var(--color-ink-2); margin-top: var(--space-md); max-width: 46ch; }
.hero figure { margin: 0; border: var(--rule-hair) solid var(--color-rule); aspect-ratio: 1; overflow: hidden; }
.hero figure img { width: 100%; height: 100%; object-fit: cover; }
.oro-band { background: var(--color-paper-warm); text-align: center; padding: var(--space-xl) var(--page-gutter); }
.oro-band .figure { font-family: var(--font-display); font-size: clamp(1.8rem, 6vw, 4rem); line-height: 1.05; white-space: nowrap; }
.figure .unit { font-size: .32em; color: var(--color-muted); letter-spacing: .08em; margin-left: .2em; }
.figure.is-live::after { content: ""; display: inline-block; width: .13em; height: .13em; margin-left: .3em; border-radius: 50%; background: var(--color-ok); vertical-align: middle; }
.oro-band p { margin-top: var(--space-xs); color: var(--color-ink-2); }
.ventajas { display: grid; gap: var(--space-lg); grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); text-align: center; padding: var(--space-xl) 0; }
.ventajas h3 { letter-spacing: .06em; text-transform: uppercase; font-size: var(--text-sm); }
.ventajas p { margin: var(--space-xs) auto 0; max-width: 32ch; color: var(--color-ink-2); }

/* catálogo */
.grid { display: grid; gap: var(--space-xl) var(--space-md); grid-template-columns: repeat(auto-fill, minmax(min(240px, 100%), 1fr)); margin-top: var(--space-xl); }
.pieza { display: grid; gap: var(--space-2xs); text-align: center; min-width: 0; text-decoration: none; }
.pieza figure { margin: 0 0 var(--space-xs); aspect-ratio: 1; border: var(--rule-hair) solid var(--color-rule); overflow: hidden; }
.pieza figure img { width: 100%; height: 100%; object-fit: cover; transition: transform var(--dur-base) var(--ease-out); }
.pieza:hover figure img { transform: scale(1.03); }
.pieza .spec { font-size: var(--text-sm); letter-spacing: .06em; text-transform: uppercase; color: var(--color-muted); }
.pieza .precio { font-size: var(--text-xl); font-weight: 600; margin-top: var(--space-2xs); }
.pieza .tag { font-size: var(--text-xs); letter-spacing: .08em; text-transform: uppercase; color: var(--color-accent); }
.filtros { display: flex; flex-wrap: wrap; gap: var(--space-xs); justify-content: center; margin-top: var(--space-lg); }
.filtros button { font: inherit; font-size: var(--text-sm); letter-spacing: .06em; text-transform: uppercase; padding: .5rem 1rem; min-height: 40px; background: transparent; border: 1px solid var(--color-rule); color: var(--color-ink); cursor: pointer; }
.filtros button[aria-pressed="true"] { border-color: var(--color-accent); color: var(--color-accent); }

/* producto */
.producto { display: grid; gap: var(--space-xl); padding-block: var(--space-2xl); }
@media (min-width: 900px) { .producto { grid-template-columns: 1fr 1fr; align-items: start; } }
.producto figure { margin: 0; border: var(--rule-hair) solid var(--color-rule); aspect-ratio: 1; overflow: hidden; }
.producto figure img { width: 100%; height: 100%; object-fit: cover; }
.producto .kick { font-size: var(--text-sm); letter-spacing: .18em; text-transform: uppercase; color: var(--color-ink-2); }
.producto h1 { margin-top: var(--space-xs); }
.producto .precio { font-family: var(--font-display); font-size: clamp(1.6rem, 4vw, 2.4rem); margin-top: var(--space-md); }
.producto dl { display: grid; grid-template-columns: max-content 1fr; gap: var(--space-2xs) var(--space-md); margin: var(--space-lg) 0 0; }
.producto dt { color: var(--color-muted); font-size: var(--text-sm); letter-spacing: .06em; text-transform: uppercase; }
.producto dd { margin: 0; }
.producto .btn { margin-top: var(--space-lg); }

/* tasadora */
.tasa { display: grid; gap: var(--space-xl); grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); align-items: start; margin-top: var(--space-xl); }
.campo { display: grid; gap: var(--space-2xs); }
.campo label { font-size: var(--text-sm); letter-spacing: .08em; text-transform: uppercase; }
.campo input, .campo select, .campo textarea { font: inherit; font-size: var(--text-md); padding: .7rem .9rem; min-height: 46px; width: 100%; border: 1px solid var(--color-ink); border-radius: var(--radius); background: var(--color-paper); color: var(--color-ink); transition: border-color var(--dur-fast) var(--ease-out); }
.campo input:hover, .campo select:hover, .campo textarea:hover { border-color: var(--color-accent); }
.campo input:focus-visible, .campo select:focus-visible, .campo textarea:focus-visible { border-color: var(--color-accent); outline-offset: 0; }
.campo input[aria-invalid="true"] { border-color: var(--color-danger); }
.campo .err { font-size: var(--text-sm); color: var(--color-danger); min-height: 1.3em; }
.resultado { text-align: center; border: var(--rule-hair) solid var(--color-rule); background: var(--color-paper); padding: var(--space-lg); }
.resultado .lbl { font-size: var(--text-sm); letter-spacing: .18em; text-transform: uppercase; color: var(--color-ink-2); }
.resultado .hasta { font-family: var(--font-display); font-size: clamp(1.9rem, 5.5vw, 3.2rem); line-height: 1.1; margin-top: var(--space-xs); }
.resultado .hasta.ok { color: var(--color-accent); }
.resultado .detalle { margin: var(--space-sm) auto 0; color: var(--color-ink-2); max-width: 40ch; }
.resultado .btn { margin-top: var(--space-md); }
.pasos { display: grid; gap: var(--space-xl) var(--space-lg); grid-template-columns: repeat(auto-fit, minmax(min(240px, 100%), 1fr)); margin-top: var(--space-xl); text-align: center; }
.pasos .n { font-family: var(--font-display); color: var(--color-gold); font-size: var(--text-lg); }
.pasos h3 { margin-top: var(--space-xs); letter-spacing: .06em; text-transform: uppercase; font-size: var(--text-sm); }
.pasos p { margin: var(--space-xs) auto 0; max-width: 34ch; color: var(--color-ink-2); }

/* documento (nosotros, financiación) */
.doc { max-width: var(--measure); margin: 0 auto; }
.doc p + p { margin-top: var(--space-md); }
.doc h2 { margin-top: var(--space-xl); }
.dos { display: grid; gap: var(--space-lg); grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); margin-top: var(--space-xl); }
.tarjeta { border: var(--rule-hair) solid var(--color-rule); padding: var(--space-lg); background: var(--color-paper); }
.tarjeta h3 { letter-spacing: .06em; text-transform: uppercase; font-size: var(--text-sm); }
.tarjeta p { margin-top: var(--space-xs); color: var(--color-ink-2); }
.tarjeta .btn { margin-top: var(--space-md); }
.cifra { font-family: var(--font-display); font-size: var(--text-xl); margin-top: var(--space-sm); }

/* tiendas */
.tiendas { display: grid; gap: var(--space-md); grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr)); margin-top: var(--space-xl); }
.tienda { border: var(--rule-hair) solid var(--color-rule); padding: var(--space-lg); display: grid; gap: var(--space-xs); }
.tienda h3 { font-family: var(--font-display); font-size: var(--text-sm); letter-spacing: .1em; text-transform: uppercase; color: var(--color-accent); }
.tienda .dir { color: var(--color-ink-2); }
.tienda .enlaces { display: flex; flex-wrap: wrap; gap: var(--space-sm); margin-top: var(--space-xs); }
.tienda .enlaces a { font-size: var(--text-sm); letter-spacing: .06em; text-transform: uppercase; text-decoration: none; border-bottom: 1px solid var(--color-accent); white-space: nowrap; }

/* formularios */
.form { display: grid; gap: var(--space-md); max-width: 560px; margin: var(--space-xl) auto 0; }

/* pie */
.foot { background: var(--color-accent); color: var(--color-paper); padding: var(--space-xl) var(--page-gutter); font-size: var(--text-sm); }
.foot .wrap { display: grid; gap: var(--space-md); text-align: center; }
.foot-mast img { height: 44px; width: auto; margin: 0 auto; background: var(--color-paper); padding: 4px; }
.foot-tiendas { line-height: 1.9; }
.foot a { color: inherit; text-decoration: none; white-space: nowrap; }
.foot a:hover { text-decoration: underline; }
.foot-meta { display: flex; flex-wrap: wrap; gap: var(--space-xs) var(--space-lg); justify-content: space-between; padding-top: var(--space-md); border-top: 1px solid rgba(255,255,255,.25); }
.foot-meta a { text-decoration: underline; text-underline-offset: 3px; }

@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 1ms !important; animation-duration: 1ms !important; } .btn:active { transform: none; } }
"""

# ───────────────────────── JS del oro (compartido) ─────────────────────────
JS = r"""
// Espejo de motor_oro.py. Pinta el oro en vivo donde haya [data-oro] y calcula precios por factor calibrado.
const FUENTE = "https://api.gold-api.com/price/XAU";
const GRAMOS_POR_ONZA = 31.1035;
const PUREZA = { 10: 0.417, 14: 0.585, 18: 0.750, 22: 0.916, 24: 0.999 };
const PAGO_TASACION = { 24: 0.90, 22: 0.88, 18: 0.85, 14: 0.82, 10: 0.78 };
const RESPALDO = { spot: 4349.70, actualizado: "2026-09-12T21:12:17+02:00" };
const usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
const usd2 = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", minimumFractionDigits: 2 });
const fmtG = (g) => Number(g).toLocaleString("es-ES", { maximumFractionDigits: 2 });
let estado = { spot: RESPALDO.spot, actualizado: new Date(RESPALDO.actualizado), vivo: false };
const usdGramo = () => estado.spot / GRAMOS_POR_ONZA;
function metalDe(gramos, kilates) { return gramos * PUREZA[kilates] * usdGramo(); }

function pintarOro() {
  document.querySelectorAll("[data-oro]").forEach(el => {
    el.innerHTML = `${usd2.format(estado.spot)}<span class="unit">/OZ</span>`;
    el.classList.toggle("is-live", estado.vivo);
  });
  document.querySelectorAll("[data-hora]").forEach(el => el.textContent = estado.actualizado.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }));
  document.querySelectorAll("[data-g14]").forEach(el => el.textContent = usd2.format(usdGramo() * PUREZA[14]));
  document.querySelectorAll("[data-g18]").forEach(el => el.textContent = usd2.format(usdGramo() * PUREZA[18]));
  // piezas con factor calibrado: hoy clavan el precio de la web, y el metal flota
  document.querySelectorAll("[data-pieza]").forEach(el => {
    const g = Number(el.dataset.gramos), k = Number(el.dataset.kilates), f = Number(el.dataset.factor);
    if (!(g > 0) || !PUREZA[k] || !(f > 0)) return;
    const metal = metalDe(g, k);
    const p = el.querySelector("[data-precio]"); if (p) p.textContent = usd.format(Math.round(metal * f / 10) * 10);
    const m = el.querySelector("[data-metal]"); if (m) m.textContent = usd.format(metal);
  });
  if (typeof window.calcularTasa === "function") window.calcularTasa();
}
async function consultarOro() {
  try {
    const r = await fetch(FUENTE, { cache: "no-store" });
    if (!r.ok) throw new Error(r.status);
    const d = await r.json();
    estado = { spot: Number(d.price), actualizado: new Date(), vivo: true };
  } catch (e) { estado.vivo = false; }
  pintarOro();
}
pintarOro(); consultarOro(); setInterval(consultarOro, 60 * 60 * 1000);

// Tasadora (solo si la pagina la tiene)
const inpG = document.getElementById("gramos");
if (inpG) {
  window.calcularTasa = function () {
    const err = document.getElementById("err-gramos"), hasta = document.getElementById("hasta"), det = document.getElementById("detalle");
    const g = parseFloat(String(inpG.value).replace(",", ".")); const k = Number(document.getElementById("kilates").value);
    if (!inpG.value) { inpG.setAttribute("aria-invalid", "false"); err.textContent = ""; hasta.textContent = "Hasta $0"; hasta.classList.remove("ok"); det.textContent = "Escribe los gramos y te lo calculamos con el oro de ahora."; return; }
    if (!(g > 0) || g > 5000) { inpG.setAttribute("aria-invalid", "true"); err.textContent = "Pon un peso en gramos, por ejemplo 35,6."; hasta.textContent = "Hasta $0"; hasta.classList.remove("ok"); det.textContent = "Con el peso correcto sale el número."; return; }
    inpG.setAttribute("aria-invalid", "false"); err.textContent = "";
    const metal = metalDe(g, k); const pagamos = Math.round(metal * PAGO_TASACION[k] / 5) * 5;
    hasta.textContent = `Hasta ${usd.format(pagamos)}`; hasta.classList.add("ok");
    det.textContent = `Por ${fmtG(g)} g de ${k}k con el oro a ${usd2.format(estado.spot)} la onza. El metal vale ${usd.format(metal)} y pagamos el ${Math.round(PAGO_TASACION[k] * 100)} %.`;
  };
  inpG.addEventListener("input", window.calcularTasa);
  document.getElementById("kilates").addEventListener("change", window.calcularTasa);
  document.getElementById("form-tasa").addEventListener("submit", e => { e.preventDefault(); window.calcularTasa(); });
}

// Filtros de la colección (solo si hay)
document.querySelectorAll(".filtros button").forEach(b => b.addEventListener("click", () => {
  document.querySelectorAll(".filtros button").forEach(x => x.setAttribute("aria-pressed", "false"));
  b.setAttribute("aria-pressed", "true");
  const f = b.dataset.f;
  document.querySelectorAll(".grid .pieza").forEach(p => { p.hidden = f !== "todo" && p.dataset.tipo !== f; });
}));
"""


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def card(p: dict, href: str = "producto.html") -> str:
    spec = f"{p['kilates']}k" + (f" · {fmtg(p['gramos'])} g" if p.get("gramos") else "")
    factor = round(p["precio"] / (p["gramos"] * PUREZA[p["kilates"]] * USD_G), 4) if p.get("gramos") and p.get("kilates") else 0
    data = f' data-pieza data-gramos="{p["gramos"]}" data-kilates="{p["kilates"]}" data-factor="{factor}"' if factor else ""
    return f"""<a class="pieza" href="{href}" data-tipo="{p.get('tipo','cadena')}"{data}>
  <figure><img src="{p['img']}" alt="{esc(p['nombre'])}, oro de {p['kilates']} kilates" loading="lazy"></figure>
  <h3>{esc(p['nombre'])}</h3>
  <p class="spec">{spec}</p>
  <p class="precio tnum" data-precio>{usd(p['precio'])}</p>
  <p class="tag">Orientativo · confirmar en tienda</p>
</a>"""


PUREZA = {10: .417, 14: .585, 18: .75, 22: .916, 24: .999}
SPOT = 4349.70
USD_G = SPOT / 31.1035


def usd(v: float) -> str:
    return "${:,.0f}".format(v)


def fmtg(g: float) -> str:
    return ("{:,.2f}".format(g)).rstrip("0").rstrip(".").replace(",", "X").replace(".", ",").replace("X", ".")


def nombre_es(titulo: str) -> str:
    """Nombre limpio en español a partir de sus títulos, que son notas de mostrador.

    'Chain cuban link 188.2gr 14k 24"'      -> 'Cadena cubana 24 pulgadas'
    '8 mm Cuban Link Chain In 14K ..., 20”' -> 'Cadena cubana 8 mm · 20 pulgadas'
    'Bracelet cuban link solid 14k'         -> 'Pulsera cubana maciza'
    """
    t = titulo
    base = "Pulsera cubana" if re.search(r"bracelet|pulsera", t, re.I) else "Cadena cubana"
    detalles = []
    mm = re.search(r"(\d+(?:[.,]\d+)?)\s*mm\b", t, re.I)
    if mm:
        detalles.append(f"{mm.group(1).replace('.', ',')} mm")
    pulg = re.search(r"(\d{1,2})\s*(?:\"|”|''|inch|in\b)", t, re.I)
    if pulg:
        detalles.append(f"{pulg.group(1)} pulgadas")
    if re.search(r"\bsolid\b", t, re.I):
        base += " maciza"
    if re.search(r"pendant|charm", t, re.I):
        base += " con colgante"
    return base + (" " + " · ".join(detalles) if detalles else "")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "sitio.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (OUT / "oro.js").write_text(JS.strip() + "\n", encoding="utf-8")
    shutil.copy(AQUI / "tokens.css", OUT / "tokens.css")
    if (OUT / "assets-ariel").exists():
        shutil.rmtree(OUT / "assets-ariel")
    shutil.copytree(ASSETS, OUT / "assets-ariel")

    piezas = json.loads((ASSETS / "piezas.json").read_text(encoding="utf-8"))["piezas"]
    col = json.loads((ASSETS / "coleccion.json").read_text(encoding="utf-8"))
    nombres = {1: "Pulsera cubana", 2: "Pulsera oro amarillo", 3: "Anillo con diamante", 4: "Charm 3,25 pulgadas", 6: "Cadena cubana", 7: "Cadena con cruz"}
    destacadas = []
    for i, p in enumerate(piezas, 1):
        if i in nombres:
            destacadas.append({"nombre": nombres[i], "kilates": p["kilates"], "gramos": p["gramos"], "precio": p["precio_web"], "img": p["img_local"], "tipo": "pulsera" if "Pulsera" in nombres[i] else ("anillo" if "Anillo" in nombres[i] else "cadena")})
    coleccion = [{"nombre": nombre_es(c["titulo"]), "kilates": c["kilates"] or 14, "gramos": c["gramos"], "precio": c["precio"], "img": c["img"], "tipo": "pulsera" if re.search(r"bracelet|pulsera", c["titulo"], re.I) else "cadena"} for c in col]

    # ── inicio ──
    ventajas = [("Descuentos", "Ofertas exclusivas en tienda y en la web."), ("Envío seguro", "Envío ultraseguro y asegurado."),
                ("Reseñas de cinco estrellas", "Cientos de testimonios de clientes de Miami."), ("Financiación", "Paga en 3, 6 o 12 meses, o en 4 sin intereses.")]
    inicio = f"""
<section class="wrap hero">
  <div>
    <p class="kick">Siete joyerías en Miami · desde un anillo y un bolsillo de sueños</p>
    <h1>Cuban Link hecho a mano, al precio del oro de hoy</h1>
    <p class="lead">Cadenas, pulseras, anillos y charms en oro de 14 y 18 kilates. Cada precio se ajusta con el oro cada hora y se confirma en tienda al ver la pieza.</p>
    <div class="acciones" style="justify-content:flex-start"><a class="btn" href="coleccion.html">Ver la colección</a><a class="btn ghost" href="tasa-tu-oro.html">Tasa tu oro</a></div>
  </div>
  <figure><img src="{destacadas[0]['img']}" alt="{esc(destacadas[0]['nombre'])} de oro de 14 kilates" fetchpriority="high"></figure>
</section>
<div class="oro-band">
  <p class="kick" style="font-size:var(--text-sm);letter-spacing:.18em;text-transform:uppercase;color:var(--color-ink-2)">El oro ahora mismo</p>
  <p class="figure tnum" data-oro>$4,349.70<span class="unit">/OZ</span></p>
  <p>Actualizado a las <span data-hora class="tnum">21:12</span> · el gramo de 14k a <span data-g14 class="tnum">$81.81</span> · se revisa cada hora</p>
  <small class="aviso">Precio orientativo. El definitivo, en tienda con la pieza en la báscula.</small>
</div>
<section class="wrap"><div class="ventajas">{''.join(f'<div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in ventajas)}</div></section>
<section class="wrap bloque">
  <h2 class="center">Nuestra colección de cubanas</h2>
  <p class="intro">Piezas reales de la tienda. El precio de cada una lleva dentro el oro de hoy.</p>
  <div class="grid">{''.join(card(p) for p in destacadas)}</div>
  <div class="acciones"><a class="btn" href="coleccion.html">Compra ahora</a></div>
</section>
<section class="band"><div class="wrap bloque">
  <h2 class="center">¿Tienes oro? Te decimos cuánto</h2>
  <p class="intro">Dos datos y sale un número. Y en cualquiera de las siete tiendas lo confirmamos con la pieza en la mano.</p>
  <div class="acciones"><a class="btn" href="tasa-tu-oro.html">Tasar mi oro</a><a class="btn ghost" href="tiendas.html">Ver tiendas</a></div>
</div></section>
"""

    # ── colección ──
    coleccion_html = f"""
<section class="wrap bloque">
  <h1 class="center">Cadenas y pulseras cubanas</h1>
  <p class="intro">Hechas a mano en oro de 14 kilates. {len(coleccion)} piezas reales de la web, con el precio ajustado al oro de hoy.</p>
  <div class="filtros" role="group" aria-label="Filtrar"><button type="button" data-f="todo" aria-pressed="true">Todo</button><button type="button" data-f="cadena" aria-pressed="false">Cadenas</button><button type="button" data-f="pulsera" aria-pressed="false">Pulseras</button></div>
  <div class="grid">{''.join(card(p) for p in coleccion)}</div>
  <small class="aviso center" style="margin-top:var(--space-xl)">Precios orientativos calculados con el oro de hoy. El precio final se confirma en tienda al ver la pieza.</small>
</section>
"""

    # ── producto (la cadena cubana 22,9 dwt) ──
    prod = next(p for p in destacadas if p["nombre"] == "Cadena cubana")
    factor = round(prod["precio"] / (prod["gramos"] * PUREZA[prod["kilates"]] * USD_G), 4)
    producto = f"""
<section class="wrap producto" data-pieza data-gramos="{prod['gramos']}" data-kilates="{prod['kilates']}" data-factor="{factor}">
  <figure><img src="{prod['img']}" alt="Cadena cubana de oro de 14 kilates, 22,9 dwt" fetchpriority="high"></figure>
  <div>
    <p class="kick">Cuban Link · hecha a mano</p>
    <h1>Cadena cubana 14k · 22,9 dwt</h1>
    <p class="precio tnum" data-precio>{usd(prod['precio'])}</p>
    <small class="aviso" style="margin:var(--space-xs) 0 0;max-width:none">Orientativo con el oro a <span data-oro-txt></span> las <span data-hora class="tnum">21:12</span>. Se confirma en tienda al ver la pieza.</small>
    <dl>
      <dt>Oro</dt><dd>14 kilates (585 milésimas)</dd>
      <dt>Peso</dt><dd>22,9 dwt · 35,6 g</dd>
      <dt>Metal hoy</dt><dd class="tnum" data-metal>$2,913</dd>
      <dt>Financiación</dt><dd>3, 6 o 12 meses con Affirm, o Paga en 4</dd>
      <dt>Recogida</dt><dd>En cualquiera de las siete tiendas de Miami</dd>
    </dl>
    <div class="acciones" style="justify-content:flex-start"><a class="btn" href="{TEL_HREF}">Reservar por teléfono</a><a class="btn ghost" href="financiacion.html">Ver financiación</a></div>
  </div>
</section>
<section class="band"><div class="wrap bloque">
  <h2 class="center">Cómo se calcula este precio</h2>
  <div class="pasos">
    <div><p class="n">01</p><h3>Metal</h3><p>Gramos, por pureza del kilate, por precio del gramo de hoy.</p></div>
    <div><p class="n">02</p><h3>Lo demás no cambia</h3><p>Mano de obra y margen quedan fijos: se calibraron con el precio de la web.</p></div>
    <div><p class="n">03</p><h3>Se confirma en tienda</h3><p>Con la pieza en la báscula. El precio online es orientativo.</p></div>
  </div>
</div></section>
"""

    # ── tasa tu oro ──
    tasa = f"""
<section class="wrap bloque">
  <p class="kick center" style="font-size:var(--text-sm);letter-spacing:.18em;text-transform:uppercase;color:var(--color-ink-2)">El oro ahora mismo</p>
  <p class="figure tnum center" data-oro style="font-family:var(--font-display);font-size:clamp(1.8rem,6vw,4rem);line-height:1.05;white-space:nowrap;margin-top:var(--space-sm)">$4,349.70<span class="unit">/OZ</span></p>
  <h1 class="center" style="margin-top:var(--space-lg)">¿Tienes oro? Te decimos cuánto te pagamos hoy</h1>
  <p class="intro">Dos datos y sale un número. El definitivo, con la pieza en la báscula en cualquiera de las siete tiendas.</p>
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
</section>
<section class="band"><div class="wrap bloque">
  <h2 class="center">Así funciona</h2>
  <div class="pasos">
    <div><p class="n">01</p><h3>Miramos el oro</h3><p>Cada hora, en una fuente pública. El número de arriba es el de ahora.</p></div>
    <div><p class="n">02</p><h3>Calculamos el metal</h3><p>Gramos, por pureza del kilate, por precio del gramo. Pagamos del 78 al 90 % según el kilate.</p></div>
    <div><p class="n">03</p><h3>Lo confirmamos contigo</h3><p>Trae la pieza a cualquier tienda. La pesamos delante de ti y cerramos el precio.</p></div>
  </div>
</div></section>
"""

    # ── financiación ──
    financiacion = f"""
<section class="wrap bloque">
  <h1 class="center">Paga tu joya a plazos</h1>
  <p class="intro">Dos formas de llevártela hoy y pagarla con calma. Sin letra pequeña: lo que ves al pagar es lo que pagas.</p>
  <div class="dos">
    <div class="tarjeta">
      <h3>Con Affirm · 3, 6 o 12 meses</h3>
      <p>Sin intereses diferidos ni comisiones ocultas. Tasas desde el 0 % o del 10 al 36 % APR según tu crédito; la tuya la ves antes de confirmar.</p>
      <p class="cifra tnum">$950 → $88.15 al mes</p>
      <p>Ejemplo real de su web: 12 meses al 20 % APR.</p>
      <a class="btn" href="https://www.affirm.com/" rel="noopener">Precalificar con Affirm</a>
    </div>
    <div class="tarjeta">
      <h3>Sin crédito · alquiler con opción a compra</h3>
      <p>Con Progressive puedes llevarte oro y diamantes aunque no tengas crédito o lo tengas malo. Pagas la primera cuota al comprar y tienes 90 días para comprarla anticipadamente.</p>
      <p class="cifra">4 pasos</p>
      <p>1. Te aprueban · 2. Eliges la pieza · 3. Llamas al {TEL_FIN} para cerrar el pedido · 4. Pagas a plazos.</p>
      <a class="btn" href="tel:+1{TEL_FIN.replace('-', '')}">Llamar al {TEL_FIN}</a>
    </div>
  </div>
  <small class="aviso center" style="margin-top:var(--space-xl)">Las condiciones las fija cada entidad al aprobar. La joyería no cobra nada por financiar.</small>
</section>
"""

    # ── nosotros ──
    nosotros = """
<section class="wrap bloque">
  <h1 class="center">Un anillo y un bolsillo lleno de sueños</h1>
  <div class="doc" style="margin-top:var(--space-xl)">
    <p>El viaje de Ariel empezó modestamente: un anillo y un bolsillo lleno de sueños. Trabajaba de cajero en Publix y le gustaban tanto las joyas que se gastó el sueldo de una semana en un anillo. Lo llevaba todos los días, también en el trabajo, y un cliente se fijó en él en la caja.</p>
    <p>Ariel se lo ofreció por el doble de lo que le había costado. El cliente pagó cien dólares. Aquella venta duplicó su sueldo semanal y plantó la semilla de todo lo que vino después.</p>
    <p>Empezó vendiendo joyas en la calle, ganando experiencia y clientes poco a poco, hasta abrir su primera joyería. Hoy son siete sucursales en todo Miami.</p>
    <h2>Un negocio de familia</h2>
    <p>Ariel's Jewelry lo dirigen Ariel, su esposa Yuliet y su cuñada Yulimar, con un equipo leal que lleva más de diez años a bordo. Ofrecen un trato personal y las mejores joyas al precio más competitivo, especializados en Cuban Link hecho a mano.</p>
    <p>La filosofía es sencilla: todo el mundo merece acceso a joyas de calidad.</p>
  </div>
  <div class="acciones"><a class="btn" href="coleccion.html">Ver la colección</a><a class="btn ghost" href="tiendas.html">Nuestras siete tiendas</a></div>
</section>
"""

    # ── tiendas ──
    tiendas = f"""
<section class="wrap bloque">
  <h1 class="center">Siete tiendas en el sur de Florida</h1>
  <p class="intro">Elige la más cercana. Llama con un toque o abre la ruta en el mapa.</p>
  <div class="tiendas">{''.join(f'<div class="tienda"><h3>{n}</h3><p class="dir">{esc(d)}</p><p class="tnum">{t}</p><p class="enlaces"><a href="{tel_href(t)}">Llamar</a><a href="{maps(d)}" rel="noopener" target="_blank">Cómo llegar</a></p></div>' for n, d, t in TIENDAS)}</div>
</section>
"""

    # ── contacto ──
    contacto = f"""
<section class="wrap bloque">
  <h1 class="center">Ponte en contacto</h1>
  <p class="intro">Por teléfono es lo más rápido. Si prefieres escribir, te contestamos al correo.</p>
  <div class="acciones"><a class="btn" href="{TEL_HREF}">☎ {TEL}</a><a class="btn ghost" href="mailto:{EMAIL}">✉ Escribir un correo</a></div>
  <form class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
    <div class="campo"><label for="c-nombre">Nombre</label><input id="c-nombre" name="nombre" type="text" autocomplete="name"></div>
    <div class="campo"><label for="c-tel">Teléfono</label><input id="c-tel" name="telefono" type="tel" inputmode="tel" autocomplete="tel"></div>
    <div class="campo"><label for="c-msg">Qué necesitas</label><textarea id="c-msg" name="mensaje" rows="4"></textarea></div>
    <button class="btn" type="submit">Enviar</button>
  </form>
  <small class="aviso center" style="margin-top:var(--space-xl)">13200 Biscayne Blvd, North Miami, FL 33181 · {EMAIL} · {TEL}</small>
</section>
"""

    # ── embajadores ──
    embajadores = f"""
<section class="wrap bloque">
  <h1 class="center">Embajadores y patrocinios</h1>
  <p class="intro">¿Quieres ser embajador de la marca o buscas patrocinio para tu contenido? Déjanos tus datos y hablamos.</p>
  <form class="form" action="mailto:{EMAIL}" method="post" enctype="text/plain">
    <div class="campo"><label for="e-nombre">Nombre</label><input id="e-nombre" name="nombre" type="text" autocomplete="name"></div>
    <div class="campo"><label for="e-email">Correo</label><input id="e-email" name="correo" type="email" autocomplete="email" required></div>
    <div class="campo"><label for="e-redes">Tus redes</label><input id="e-redes" name="redes" type="text" placeholder="@usuario en Instagram, TikTok, YouTube"></div>
    <button class="btn" type="submit">Enviar</button>
  </form>
</section>
"""

    paginas = {
        "index.html": ("Inicio", inicio, True),
        "coleccion.html": ("Colección de cubanas", coleccion_html, True),
        "producto.html": ("Cadena cubana 14k", producto, True),
        "tasa-tu-oro.html": ("Tasa tu oro", tasa, True),
        "financiacion.html": ("Financiación", financiacion, False),
        "nosotros.html": ("Nosotros", nosotros, False),
        "tiendas.html": ("Tiendas", tiendas, False),
        "contacto.html": ("Contacto", contacto, False),
        "embajadores.html": ("Embajadores", embajadores, False),
    }
    for f, (t, cuerpo, oro) in paginas.items():
        (OUT / f).write_text(shell(t, cuerpo, f, oro=oro), encoding="utf-8")
        print("  ok", f)
    print(f"sitio generado en {OUT} ({len(paginas)} paginas)")


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
