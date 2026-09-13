# Precio al día

Demo de una tienda de joyería cuyos precios se recalculan solos con el oro en vivo, sellados con hora y con aviso de que se confirman en tienda. Marca neutra a propósito: esta demo no lleva la marca de ningún cliente real.

## Qué hay

| Fichero | Qué hace |
|---|---|
| `motor_oro.py` | El software. Mira el oro en gold-api.com, recalcula cada pieza por peso y kilate, escribe `precios.json` con hora y próxima revisión. Corre una vez o cada N minutos. |
| `catalogo.json` | Ocho piezas de muestra con kilate, gramos y mano de obra fija. |
| `precios.json` | Salida del motor. Es lo que leería la tienda. |
| `index.html` | La página. Enseña el oro ahora mismo, el catálogo repreciado y una tasadora para el cliente que trae oro. |

## Arrancar

```
python motor_oro.py --una-vez        # calcula y sale
python motor_oro.py --cada 60        # vivo, revisa cada hora
python motor_oro.py --titulo "Chain Cuban link 14kt , 22.9 dwt"
```

Abrir `index.html` en el navegador. La página también consulta el oro por su cuenta, así que se ve en vivo aunque el motor no esté corriendo.

## La fórmula, en una línea

`precio = (gramos × pureza × oro_por_gramo) × 1,35 + mano de obra`, redondeado a 10.

La pureza por kilate es la real (14k = 0,585, 18k = 0,750). Solo se recalcula el metal: la mano de obra es un número fijo por pieza y no se toca. La tasación paga entre el 78 % y el 90 % del valor del metal según el kilate.

## Cómo iría en Shopify

El motor ya lee kilate y peso de títulos tal como están escritos en la tienda (`14kt`, `22.9 dwt`, `81.7g`). En producción, en vez de escribir `precios.json`, escribiría el precio por la Admin API en cada producto que tenga esos dos datos, y el aviso con la hora iría en un metafield que el tema pinta debajo del precio. Las piezas sin peso no se tocan: mejor un precio viejo que uno inventado.

Fuente del oro: `https://api.gold-api.com/price/XAU`, gratuita y sin clave. En producción conviene una segunda fuente de respaldo.

## El sitio completo (sitio/)

`python build_sitio.py` genera nueve páginas en `sitio/` con el contenido real de arielsjewelry.com: inicio, colección (12 cubanas reales), ficha de producto, tasa tu oro, financiación, nosotros, tiendas (las siete, con llamar y cómo llegar), contacto y embajadores. Comparten `sitio.css`, `tokens.css` y `oro.js` (el oro en vivo y la tasadora). Las fotos y el logo están en `assets-ariel/` y son suyos: solo para enseñárselo a ellos.

## La segunda versión (sitio-v2/)

`python build_sitio_v2.py` genera las mismas nueve páginas con otro diseño: misma paleta, titulares en Cormorant Garamond, cuerpo en Jost, portada partida, colección con filtros laterales y la tasadora sobre azul. Reutiliza los datos y las fotos del v1.

## Versiones

`index.html` lleva el logo y seis piezas reales de Ariel Joyerías, publicado solo para enseñárselo a ellos (va con `noindex`). `demo-neutra.html` es la misma demo sin marca.
