"""Precio al dia: el motor que mira el oro cada hora y repone los precios.

Demo para Ariel's Jewelry (Miami). Marca neutra a proposito: la demo no se
publica con marca real de nadie. En produccion esto mismo correria como job
cada hora y escribiria los precios en Shopify por la Admin API; aqui escribe
precios.json, que es lo que lee la pagina.

Por que existe: una joyeria con 2.566 piezas y el oro moviendose a diario
tiene dos opciones malas, o precios viejos que pierden margen, o retocar a
mano cada semana. La tercera es esta: el precio del metal se recalcula solo
por peso y kilate, la mano de obra se queda fija, y cada precio sale sellado
con su hora y con el aviso de que se confirma en tienda.

Uso:
    python motor_oro.py --una-vez          # calcula y sale (para cron / Task Scheduler)
    python motor_oro.py --cada 60          # se queda vivo y repite cada 60 minutos
    python motor_oro.py --titulo "Chain Cuban link 14kt , 22.9 dwt"   # prueba el parser

Sin dependencias: stdlib y ya.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CATALOGO = AQUI / "catalogo.json"
SALIDA = AQUI / "precios.json"

# gold-api.com: gratuita, sin clave y con CORS abierto. Precio de la onza troy en USD.
FUENTE = "https://api.gold-api.com/price/XAU"
GRAMOS_POR_ONZA_TROY = 31.1035
GRAMOS_POR_DWT = 1.55517          # pennyweight, la unidad que usan en EE. UU.

# Pureza real de cada aleacion. 24k no es 1.0 porque el oro comercial no lo es.
PUREZA = {10: 0.417, 14: 0.585, 18: 0.750, 22: 0.916, 24: 0.999}

# Factor de venta sobre el valor del metal. Es la unica cifra de negocio y va
# aparte de la mano de obra para que el joyero la toque sin tocar codigo.
MARGEN_VENTA = 1.35

# Lo que se paga al cliente que trae oro, como fraccion del valor del metal.
# Baja con el kilate porque refinar aleaciones pobres cuesta mas.
PAGO_TASACION = {24: 0.90, 22: 0.88, 18: 0.85, 14: 0.82, 10: 0.78}

AVISO = ("Precio orientativo calculado con el oro de hoy. "
         "El precio final se confirma en tienda al ver la pieza.")

_KILATES = re.compile(r"\b(10|14|18|22|24)\s*(?:k|kt|kts|karat|kilates|quilates)\b", re.I)
_GRAMOS = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:g|gr|grs|grams?|gramos)\b", re.I)
_DWT = re.compile(r"(\d+(?:[.,]\d+)?)\s*dwt\b", re.I)


def _log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def fetch_spot() -> tuple[float, str]:
    """Onza troy en USD y la hora de la fuente. Si la red falla, reutiliza el
    ultimo precio guardado antes que dejar la tienda sin numeros."""
    try:
        with urllib.request.urlopen(FUENTE, timeout=15) as r:
            d = json.load(r)
        return float(d["price"]), d.get("updatedAt", "")
    except Exception as e:  # noqa: BLE001 - aqui queremos degradar, no morir
        _log(f"sin red ({e}); uso el ultimo precio guardado")
        if SALIDA.exists():
            viejo = json.loads(SALIDA.read_text(encoding="utf-8"))
            return float(viejo["spot_usd_oz"]), viejo.get("fuente_hora", "")
        raise SystemExit("no hay precio del oro ni cache: no se puede repreciar")


def parse_titulo(titulo: str) -> dict:
    """Saca kilate y peso de un titulo tal como estan en Shopify.

    Sirve para no reescribir el catalogo: en la tienda real, 1.909 de 2.566
    titulos llevan el kilate y 451 llevan el peso en g o dwt.
    """
    k = _KILATES.search(titulo)
    g = _GRAMOS.search(titulo)
    d = _DWT.search(titulo)
    gramos = None
    if g:
        gramos = float(g.group(1).replace(",", "."))
    elif d:
        gramos = round(float(d.group(1).replace(",", ".")) * GRAMOS_POR_DWT, 2)
    return {"kilates": int(k.group(1)) if k else None, "gramos": gramos}


def precio(pieza: dict, usd_gramo: float) -> dict:
    """Valor del metal por peso y pureza; mano de obra fija; venta redondeada a 10."""
    k = int(pieza["kilates"])
    gramos = float(pieza["gramos"])
    metal = gramos * PUREZA[k] * usd_gramo
    venta = round((metal * MARGEN_VENTA + float(pieza.get("mano_obra", 0))) / 10) * 10
    pagamos = round(metal * PAGO_TASACION[k] / 5) * 5
    return {
        **pieza,
        "valor_metal_usd": round(metal, 2),
        "precio_usd": int(venta),
        "tasacion_hasta_usd": int(pagamos),
    }


def calcular(cada_min: int) -> dict:
    spot, fuente_hora = fetch_spot()
    usd_gramo = spot / GRAMOS_POR_ONZA_TROY
    ahora = datetime.now(timezone.utc).astimezone()
    piezas = json.loads(CATALOGO.read_text(encoding="utf-8"))["piezas"]
    salida = {
        "spot_usd_oz": round(spot, 2),
        "usd_gramo_puro": round(usd_gramo, 4),
        "usd_gramo": {str(k): round(usd_gramo * p, 2) for k, p in PUREZA.items()},
        "fuente": FUENTE,
        "fuente_hora": fuente_hora,
        "actualizado": ahora.isoformat(timespec="seconds"),
        "proxima_revision": (ahora + timedelta(minutes=cada_min)).isoformat(timespec="seconds"),
        "cada_minutos": cada_min,
        "margen_venta": MARGEN_VENTA,
        "pago_tasacion": PAGO_TASACION,
        "aviso": AVISO,
        "piezas": [precio(p, usd_gramo) for p in piezas],
    }
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    _log(f"oro {spot:,.2f} $/oz  ->  {len(piezas)} piezas repreciadas  ->  {SALIDA.name}")
    return salida


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--una-vez", action="store_true", help="calcula una vez y sale")
    ap.add_argument("--cada", type=int, default=60, metavar="MIN", help="minutos entre revisiones (60)")
    ap.add_argument("--titulo", help="prueba el parser con un titulo de Shopify y sale")
    a = ap.parse_args()

    if a.titulo:
        print(json.dumps(parse_titulo(a.titulo), ensure_ascii=False))
        return
    if a.una_vez:
        calcular(a.cada)
        return
    _log(f"motor vivo: reviso el oro cada {a.cada} min (Ctrl+C para parar)")
    while True:
        try:
            calcular(a.cada)
        except SystemExit as e:
            _log(str(e))
        time.sleep(a.cada * 60)


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
