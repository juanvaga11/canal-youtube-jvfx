"""Pop-ups animados (fondo transparente) para poner en una esquina del video:
'suscribete' (botón + campanita) y 'instagram' (sígueme @julianval.fx). 5 s a 30 fps."""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from escenas import JV, ORO, ROJO
from playwright.sync_api import sync_playwright

W, H, FPS, DUR = 640, 190, 30, 5.0
CLICK = 1.8  # segundo del clic (para el sonido)


def _ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def frame(tipo, t):
    entra = _ease(t / 0.45); sale = _ease((t - 4.4) / 0.5)
    dx = (1 - entra) * 700 + sale * 700
    clic = t >= CLICK
    camp = math.sin((t - CLICK) * 28) * 18 * math.exp(-(t - CLICK) * 2.2) if clic else 0
    # cursor que llega al botón
    cx = 560 - 140 * _ease((t - 0.9) / 0.8); cy = 175 - 60 * _ease((t - 0.9) / 0.8)
    cur_op = 1 if 0.9 < t < 3.2 else 0
    escala_clic = 0.92 if CLICK <= t < CLICK + 0.12 else 1
    if tipo == "suscribete":
        boton = (f'<div style="background:#3a3a3a;color:#ddd">SUSCRITO ✓</div>' if clic else
                 f'<div style="background:{ROJO};color:#fff">SUSCRÍBETE</div>')
        texto = '¿Te está sirviendo?'
        sub = 'Suscríbete para más contenido'
        icono = f'<div style="font-size:52px;transform:rotate({camp}deg);transform-origin:50% 10%">🔔</div>'
    else:
        boton = (f'<div style="background:#3a3a3a;color:#ddd">SIGUIENDO ✓</div>' if clic else
                 f'<div style="background:linear-gradient(90deg,#f58529,#dd2a7b,#8134af);color:#fff">SÍGUEME</div>')
        texto = '@julianval.fx'
        sub = 'Contenido diario en Instagram'
        icono = f'<div style="font-size:52px;transform:scale({1 + abs(camp) / 60})">📲</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{W}px;height:{H}px;background:transparent;font-family:'Inter',sans-serif;overflow:hidden}}
.c{{position:absolute;right:20px;top:20px;transform:translateX({dx}px);display:flex;align-items:center;gap:18px;padding:18px 22px;border-radius:24px;
background:rgba(12,11,8,.92);border:2px solid {ORO};box-shadow:0 12px 40px rgba(0,0,0,.6)}}
.c img{{height:74px}} .t{{color:#fff;font-weight:800;font-size:26px}} .s{{color:#bfae7a;font-size:18px;font-weight:600;margin-top:4px}}
.b div{{font-weight:900;font-size:22px;letter-spacing:1px;padding:12px 20px;border-radius:12px;transform:scale({escala_clic});white-space:nowrap}}
.cur{{position:absolute;left:{cx}px;top:{cy}px;opacity:{cur_op};font-size:40px;filter:drop-shadow(0 2px 4px #000)}}
</style></head><body><div class="c"><img src="{JV}"><div><div class="t">{texto}</div><div class="s">{sub}</div></div><div class="b">{boton}</div>{icono}</div>
<div class="cur">👆</div></body></html>"""


def generar(destino="/tmp/popups"):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
        for tipo in ("suscribete", "instagram"):
            d = f"{destino}/{tipo}"; os.makedirs(d, exist_ok=True)
            for i in range(int(DUR * FPS)):
                pg.set_content(frame(tipo, i / FPS))
                pg.screenshot(path=f"{d}/{i:03d}.png", omit_background=True)
        b.close()
    return destino


if __name__ == "__main__":
    generar()
