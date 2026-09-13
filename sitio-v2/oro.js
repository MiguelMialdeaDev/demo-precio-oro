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
