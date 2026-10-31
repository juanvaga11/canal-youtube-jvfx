"""Plantillas visuales (HTML) de cada escena. Marca JulianVal.fx: negro y dorado.
Los elementos con data-s="n" aparecen cuando la voz llega a la frase n de la escena."""
import random

ORO = "#D4AF37"
ORO2 = "#F5D97A"
VERDE = "#22C55E"
ROJO = "#EF4444"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:var(--w);height:var(--h);overflow:hidden;background:#07070a;font-family:'Inter',sans-serif;color:#fff}}
body{{background:radial-gradient(ellipse at 50% 35%,#1b1708 0%,#0b0a07 45%,#050505 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(212,175,55,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(212,175,55,.05) 1px,transparent 1px);background-size:80px 80px}}
.logo{{position:absolute;top:44px;left:56px;font-family:'Inter Display';font-weight:900;font-size:34px;letter-spacing:1px;color:{ORO}}}
.logo span{{color:#fff;font-weight:600}}
.tag{{position:absolute;top:50px;right:56px;font-size:22px;color:#bfae7a;font-weight:600;letter-spacing:3px;text-transform:uppercase}}
.stage{{position:absolute;left:0;right:0;top:120px;bottom:210px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;padding:0 120px}}
.h1{{font-family:'Inter Display';font-weight:900;font-size:96px;line-height:1.02;text-align:center;letter-spacing:-1px}}
.h2{{font-family:'Inter Display';font-weight:800;font-size:64px;line-height:1.08;text-align:center}}
.p{{font-size:38px;color:#d9d3c0;text-align:center;line-height:1.35;font-weight:500}}
.oro{{color:{ORO};background:linear-gradient(180deg,{ORO2},{ORO});-webkit-background-clip:text;background-clip:text;color:transparent}}
.verde{{color:{VERDE}}} .rojo{{color:{ROJO}}}
.card{{background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));border:2px solid rgba(212,175,55,.35);border-radius:28px;padding:34px 38px;text-align:center}}
.row{{display:flex;gap:34px;align-items:stretch;justify-content:center}}
.big{{font-family:'Inter Display';font-weight:900;font-size:220px;line-height:.9}}
.pill{{display:inline-block;padding:12px 30px;border-radius:999px;border:2px solid {ORO};color:{ORO};font-weight:700;font-size:30px;letter-spacing:2px}}
.ico{{font-size:84px;line-height:1}}
.lbl{{font-size:24px;color:#bfae7a;letter-spacing:3px;text-transform:uppercase;font-weight:700;margin-top:10px}}
.val{{font-family:'Inter Display';font-weight:800;font-size:54px;margin-top:8px}}
.arrow{{font-size:70px;color:{ORO};align-self:center}}
.chk{{display:flex;align-items:center;gap:22px;font-size:40px;font-weight:600;text-align:left}}
.chk b{{color:#07070a;background:{ORO};border-radius:50%;width:54px;height:54px;flex:none;display:flex;align-items:center;justify-content:center;font-size:32px}}
[data-s]{{transition:none}}
.hide{{opacity:0}}
.dim{{opacity:.28}}
"""


def velas_svg(w=1300, h=520, n=46, seed=7, tendencia=0.35, marcar=False):
    rnd = random.Random(seed)
    p, vs = 100.0, []
    for _ in range(n):
        o = p
        c = o + rnd.gauss(tendencia, 2.2)
        hi = max(o, c) + abs(rnd.gauss(0, 1.1))
        lo = min(o, c) - abs(rnd.gauss(0, 1.1))
        vs.append((o, hi, lo, c)); p = c
    mn = min(v[2] for v in vs); mx = max(v[1] for v in vs)
    y = lambda v: 20 + (mx - v) / (mx - mn) * (h - 40)
    cw = w / n
    out = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    for i, (o, hi, lo, c) in enumerate(vs):
        x = i * cw + cw / 2
        col = VERDE if c >= o else ROJO
        out.append(f'<line x1="{x}" x2="{x}" y1="{y(hi)}" y2="{y(lo)}" stroke="{col}" stroke-width="3"/>')
        top, bot = y(max(o, c)), y(min(o, c))
        out.append(f'<rect x="{x - cw * .32}" y="{top}" width="{cw * .64}" height="{max(bot - top, 3)}" fill="{col}" rx="2"/>')
    out.append("</svg>")
    return "".join(out)


def mini_tendencia(sube=True, w=380, h=200):
    pts = [(0, 160), (60, 120), (110, 140), (180, 80), (230, 105), (300, 40), (380, 20)]
    if not sube:
        pts = [(x, h - yy) for x, yy in pts]
    col = VERDE if sube else ROJO
    d = " ".join(f"{x},{yy}" for x, yy in pts)
    return f'<svg width="{w}" height="{h}"><polyline points="{d}" fill="none" stroke="{col}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/></svg>'


# ---------- Escenas del video horizontal ----------

def gancho():
    return f"""<div class="stage">
<div class="big rojo" data-s="0">7 de 10</div>
<div class="h2" data-s="0">traders principiantes <span class="rojo">pierden dinero</span></div>
<div class="p" data-s="1">No es mala suerte: empiezan sin entender qué hacen</div>
<div class="pill" data-s="3">TRADING DESDE CERO · SIN ENREDOS</div>
<div class="p" data-s="4">⚠️ Al final: <b class="oro">el error #1</b> de los principiantes</div>
</div>"""


def marca():
    return f"""<div class="stage">
<div class="h1"><span class="oro">JulianVal</span>.fx</div>
<div class="p" data-s="1">Trading paso a paso · <b class="oro">de cero a experto</b></div>
<div class="row" data-s="2"><div class="card"><div class="lbl">Serie</div><div class="val">Fundamentos</div></div><div class="card"><div class="lbl">Video</div><div class="val oro">#1</div></div></div>
</div>"""


def definicion():
    return f"""<div class="stage">
<div class="pill" data-s="0">¿QUÉ ES EL TRADING?</div>
<div class="h2" data-s="1">Comprar y vender activos para <span class="oro">ganar con la diferencia de precio</span></div>
<div class="row" data-s="3"><div class="card"><div class="ico">🎩</div><div class="val rojo">No es magia</div></div><div class="card"><div class="ico">🎲</div><div class="val rojo">No es azar</div></div><div class="card"><div class="ico">⏳</div><div class="val rojo">No es rápido</div></div></div>
<div class="h2" data-s="4">Es una <span class="oro">habilidad</span> que se aprende</div>
</div>"""


def cafe():
    return f"""<div class="stage">
<div class="pill" data-s="0">EJEMPLO REAL · EL CAFÉ</div>
<div class="row">
<div class="card" data-s="1"><div class="ico">☕</div><div class="lbl">Compras</div><div class="val">$100.000</div></div>
<div class="arrow" data-s="2">➜</div>
<div class="card" data-s="2"><div class="ico">📈</div><div class="lbl">Vendes</div><div class="val">$120.000</div></div>
<div class="arrow" data-s="3">=</div>
<div class="card" data-s="3" style="border-color:{VERDE}"><div class="ico">💰</div><div class="lbl">Ganancia</div><div class="val verde">+$20.000</div></div>
</div>
<div class="p" data-s="5">En trading no tocas el café: <b class="oro">operas el precio</b> desde tu celular o PC</div>
</div>"""


def mercados():
    c = lambda s, i, n, e: f'<div class="card" data-s="{s}" style="width:330px"><div class="ico">{i}</div><div class="val" style="font-size:42px">{n}</div><div class="lbl">{e}</div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">¿QUÉ SE PUEDE OPERAR?</div>
<div class="row">{c(2,'💱','Divisas','EUR/USD')}{c(3,'🥇','Oro','XAU/USD')}{c(4,'🏛️','Índices','Bolsa')}{c(5,'⚡','Sintéticos','24/7')}</div>
<div class="p" data-s="6">En este canal: <b class="oro">oro · forex · sintéticos</b></div>
</div>"""


def direccion():
    return f"""<div class="stage">
<div class="h2" data-s="0">Ganas cuando <span class="verde">sube</span> y cuando <span class="rojo">baja</span></div>
<div class="row">
<div class="card" data-s="2" style="border-color:{VERDE}">{mini_tendencia(True)}<div class="val verde">COMPRA</div><div class="lbl">Crees que sube</div></div>
<div class="card" data-s="3" style="border-color:{ROJO}">{mini_tendencia(False)}<div class="val rojo">VENTA</div><div class="lbl">Crees que baja</div></div>
</div>
<div class="p" data-s="4">La clave: <b class="oro">buen análisis + control del riesgo</b></div>
</div>"""


def oferta():
    return f"""<div class="stage">
<div class="pill" data-s="0">¿POR QUÉ SE MUEVE EL PRECIO?</div>
<div class="h2" data-s="1">Oferta <span class="oro">vs</span> Demanda</div>
<div class="row">
<div class="card" data-s="2" style="border-color:{VERDE}"><div class="ico">🙋‍♂️🙋‍♀️🙋</div><div class="val verde">Más compradores</div><div class="lbl">El precio sube ▲</div></div>
<div class="card" data-s="3" style="border-color:{ROJO}"><div class="ico">🏃‍♂️🏃‍♀️🏃</div><div class="val rojo">Más vendedores</div><div class="lbl">El precio baja ▼</div></div>
</div>
<div class="p" data-s="4">🏦 Bancos e instituciones = <b class="oro">Dinero Inteligente (SMC)</b></div>
</div>"""


def herramientas():
    c = lambda s, n, i, t, e: f'<div class="card" data-s="{s}" style="width:420px"><div class="lbl">Paso {n}</div><div class="ico" style="margin:14px 0">{i}</div><div class="val">{t}</div><div class="p" style="font-size:28px;margin-top:10px">{e}</div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">LO QUE NECESITAS</div>
<div class="row">{c(1,1,'🏢','Bróker','Te conecta al mercado')}{c(2,2,'💻','MetaTrader 5','Abres y cierras operaciones')}{c(3,3,'📊','Gráfico','Ves cómo se mueve el precio')}</div>
</div>"""


def velas():
    return f"""<div class="stage">
<div class="pill" data-s="0">GRÁFICO DE VELAS</div>
<div class="card" data-s="0" style="padding:24px">{velas_svg()}</div>
<div class="row" data-s="2"><div class="p">🟩 <b class="verde">Verde:</b> el precio subió</div><div class="p">🟥 <b class="rojo">Roja:</b> el precio bajó</div></div>
</div>"""


def error():
    return f"""<div class="stage">
<div class="pill" data-s="0" style="border-color:{ROJO};color:{ROJO}">⚠️ ERROR #1 DEL PRINCIPIANTE</div>
<div class="h1" data-s="1">Operar <span class="rojo">sin gestión de riesgo</span></div>
<div class="row" data-s="2"><div class="card"><div class="val rojo">❌ Todo el dinero</div></div><div class="card"><div class="val rojo">❌ Sin stop loss</div></div><div class="card"><div class="val rojo">❌ "Ya se devuelve"</div></div></div>
<div class="card" data-s="4" style="border-color:{ORO}"><div class="lbl">Regla de oro</div><div class="val">Arriesga solo <span class="oro">1% – 2%</span> por operación</div></div>
</div>"""


def demo():
    return f"""<div class="stage">
<div class="pill" data-s="0">CONSEJO</div>
<div class="h1" data-s="1">Empieza en <span class="oro">cuenta demo</span></div>
<div class="p" data-s="2">Dinero virtual · practicas sin arriesgar tu plata</div>
<div class="row" data-s="3"><div class="card"><div class="val">1. Aprende</div></div><div class="arrow">➜</div><div class="card"><div class="val">2. Practica</div></div><div class="arrow">➜</div><div class="card"><div class="val oro">3. Real</div></div></div>
</div>"""


def resumen():
    ck = lambda s, t: f'<div class="chk" data-s="{s}"><b>✓</b>{t}</div>'
    return f"""<div class="stage" style="align-items:center">
<div class="pill" data-s="0">RESUMEN</div>
<div style="display:flex;flex-direction:column;gap:26px">
{ck(1,'Trading = ganar con la diferencia de precio')}
{ck(2,'Ganas cuando sube <span class="verde">▲</span> y cuando baja <span class="rojo">▼</span>')}
{ck(3,'El precio se mueve por oferta y demanda')}
{ck(4,'<span class="oro">Primero la gestión de riesgo</span>')}
</div></div>"""


def cierre():
    return f"""<div class="stage">
<div class="lbl" data-s="0">Siguiente video</div>
<div class="card" data-s="0" style="width:1100px"><div class="val">#2 · Qué mercados operar y <span class="oro">cuál te conviene</span></div></div>
<div class="row" data-s="1"><div class="pill" style="background:{ROJO};border-color:{ROJO};color:#fff">▶ SUSCRÍBETE</div><div class="pill">🔔 ACTIVA LA CAMPANITA</div></div>
<div class="p" data-s="2">🎓 Aprende a fondo en <b class="oro">SKY Academy</b> · link en la descripción</div>
<div class="p" style="font-size:22px;color:#8a826c;margin-top:20px">Contenido educativo. El trading implica riesgo de pérdida de capital.</div>
</div>"""


# ---------- Escenas del Short vertical ----------

def s_gancho():
    return f"""<div class="stage" style="top:200px;bottom:700px">
<div class="pill">⚠️ PRINCIPIANTES</div>
<div class="h1" style="font-size:118px">El error <span class="rojo">#1</span> que <span class="oro">quema cuentas</span></div>
</div>"""


def s_no():
    return f"""<div class="stage" style="top:200px;bottom:700px">
<div class="h2" data-s="0" style="font-size:80px"><s class="dim">La estrategia</s></div>
<div class="h2" data-s="1" style="font-size:80px"><s class="dim">El bróker</s></div>
<div class="h1" data-s="2" style="font-size:100px">Operar <span class="rojo">sin gestión de riesgo</span></div>
</div>"""


def s_mal():
    return f"""<div class="stage" style="top:200px;bottom:700px;gap:30px">
<div class="card" style="width:820px"><div class="val rojo" style="font-size:66px">❌ Toda la cuenta</div></div>
<div class="card" style="width:820px"><div class="val rojo" style="font-size:66px">❌ Sin stop loss</div></div>
<div class="card" style="width:820px"><div class="val rojo" style="font-size:66px">🙏 "Ya se devuelve"</div></div>
</div>"""


def s_regla():
    return f"""<div class="stage" style="top:200px;bottom:700px">
<div class="lbl" style="font-size:36px" data-s="0">La regla de oro</div>
<div class="big oro" data-s="2" style="font-size:250px">1–2%</div>
<div class="h2" data-s="2">por operación</div>
<div class="p" data-s="3" style="font-size:46px">Pierdes varias… y <b class="oro">sigues en el juego</b></div>
</div>"""


def s_cta():
    return f"""<div class="stage" style="top:200px;bottom:700px">
<div class="h1" style="font-size:96px"><span class="oro">JulianVal</span>.fx</div>
<div class="p" style="font-size:46px">Serie completa: <b class="oro">Trading de cero a experto</b></div>
<div class="pill" data-s="1" style="font-size:44px;background:{ROJO};border-color:{ROJO};color:#fff">➕ SÍGUEME</div>
</div>"""


ESCENAS = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_")}


def pagina(nombre, paso, w, h):
    cuerpo = ESCENAS[nombre]()
    vertical = h > w
    extra = ".stage{padding:0 70px}.logo{font-size:46px;top:70px;left:70px}" if vertical else ".stage{zoom:1.15;top:100px;bottom:180px}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{extra}</style></head>
<body><div class="grid"></div><div class="logo">JulianVal<span>.fx</span></div>{'' if vertical else '<div class="tag">Trading de cero a experto</div>'}
{cuerpo}
<script>document.querySelectorAll('[data-s]').forEach(e=>{{if(+e.dataset.s>{paso})e.classList.add('hide')}});</script>
</body></html>"""
