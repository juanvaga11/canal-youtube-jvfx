"""Plantillas visuales (HTML) de cada escena. Marca JulianVal.fx: negro y dorado.
Los elementos con data-s="n" aparecen cuando la voz llega a la frase n de la escena."""
import random, base64, os
_M = os.path.join(os.path.dirname(__file__), "..", "marca")
def _uri(f):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(_M, f), "rb").read()).decode()
JV = _uri("jv.png")
LOGO = _uri("logo_completo.png")

ORO = "#D4AF37"
ORO2 = "#F5D97A"
VERDE = "#22C55E"
ROJO = "#EF4444"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:var(--w);height:var(--h);overflow:hidden;background:#07070a;font-family:'Inter',sans-serif;color:#fff}}
body{{background:radial-gradient(ellipse at 50% 35%,#1b1708 0%,#0b0a07 45%,#050505 100%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(212,175,55,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(212,175,55,.05) 1px,transparent 1px);background-size:80px 80px}}
.logo{{position:absolute;top:34px;left:50px;display:flex;align-items:center;gap:14px;font-family:'Inter Display';font-weight:900;font-size:34px;letter-spacing:1px;color:{ORO}}}
.logo span{{color:#fff;font-weight:600}} .logo img{{height:64px;filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))}}
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
.hide{{opacity:0}} tr.hide td{{border-color:transparent}}
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
<img src="{LOGO}" style="height:330px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.7))">
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
    ck = lambda s, t: f'<div class="chk" data-s="{s}"><b>✓</b><span>{t}</span></div>'
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
<img src="{JV}" style="height:150px">
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
<img src="{LOGO}" style="width:760px">
<div class="p" style="font-size:46px">Serie completa: <b class="oro">Trading de cero a experto</b></div>
<div class="pill" data-s="1" style="font-size:44px;background:{ROJO};border-color:{ROJO};color:#fff">➕ SÍGUEME</div>
</div>"""



def inversion():
    return f"""<div class="stage">
<div class="pill" data-s="0">TRADING ≠ INVERTIR</div>
<div class="row">
<div class="card" data-s="1" style="width:560px"><div class="ico">🏦</div><div class="val">Inversión</div><div class="p" style="font-size:30px;margin-top:10px">Compras y guardas<br><b class="oro">durante años</b></div></div>
<div class="card" data-s="2" style="width:560px;border-color:{ORO}"><div class="ico">⚡</div><div class="val oro">Trading</div><div class="p" style="font-size:30px;margin-top:10px">Movimientos cortos:<br><b class="oro">minutos · horas · días</b></div></div>
</div>
<div class="p" data-s="4">Ninguno es mejor: <b class="oro">son dos formas distintas</b></div>
</div>"""


def estilos():
    c = lambda s, i, n, t, e: f'<div class="card" data-s="{s}" style="width:440px"><div class="ico">{i}</div><div class="val">{n}</div><div class="pill" style="margin:16px 0 8px;font-size:24px">{t}</div><div class="p" style="font-size:28px">{e}</div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">ESTILOS DE TRADING</div>
<div class="row">{c(1,'⏱️','Scalping','MINUTOS','Muchas operaciones rápidas')}{c(2,'☀️','Intradía','EL MISMO DÍA','Abres y cierras hoy')}{c(3,'📈','Swing','VARIOS DÍAS','Menos pantalla, más paciencia')}</div>
<div class="p" data-s="4">Cada estilo se adapta a <b class="oro">tu tiempo y tu personalidad</b></div>
</div>"""


def operacion():
    rnd = random.Random(11)
    p, vs = 100.0, []
    for k in range(30):
        o = p; c = o + rnd.gauss(0.5 if k > 8 else -0.2, 1.6)
        vs.append((o, max(o, c) + abs(rnd.gauss(0, .8)), min(o, c) - abs(rnd.gauss(0, .8)), c)); p = c
    W, H, cw = 1150, 470, 22
    entrada = vs[-1][3]; sl = min(v[2] for v in vs[-8:]) - 1.0; tp = entrada + (entrada - sl) * 2
    mn = min(min(v[2] for v in vs), sl) - 1; mx = max(max(v[1] for v in vs), tp) + 1
    y = lambda v: 15 + (mx - v) / (mx - mn) * (H - 30)
    out = [f'<svg width="{W}" height="{H}">']
    for i, (o, hi, lo, c) in enumerate(vs):
        x = 20 + i * cw; col = VERDE if c >= o else ROJO
        out.append(f'<line x1="{x}" x2="{x}" y1="{y(hi)}" y2="{y(lo)}" stroke="{col}" stroke-width="3"/><rect x="{x-7}" y="{y(max(o,c))}" width="14" height="{max(y(min(o,c))-y(max(o,c)),3)}" fill="{col}" rx="2"/>')
    out.append('</svg>')
    x0 = 20 + 29 * cw
    def ln(v, col, txt, s, fill=None):
        return f'<div data-s="{s}" style="position:absolute;left:{x0}px;width:{W - x0 - 10}px;top:{y(v)}px;border-top:4px dashed {col}"><span style="position:absolute;right:0;top:-46px;background:{col};color:#0a0a0a;font-weight:800;font-size:26px;padding:6px 16px;border-radius:10px">{txt}</span></div>'
    zonas = f'<div data-s="4" style="position:absolute;left:{x0}px;width:{W-x0-10}px;top:{y(tp)}px;height:{y(entrada)-y(tp)}px;background:rgba(34,197,94,.12)"></div><div data-s="3" style="position:absolute;left:{x0}px;width:{W-x0-10}px;top:{y(entrada)}px;height:{y(sl)-y(entrada)}px;background:rgba(239,68,68,.12)"></div>'
    return f"""<div class="stage" style="gap:26px">
<div class="pill" data-s="0">UNA OPERACIÓN COMPLETA</div>
<div class="card" style="padding:20px"><div style="position:relative;width:{W}px;height:{H}px">{"".join(out)}{zonas}
{ln(entrada, ORO, '① ENTRADA', 2)}{ln(sl, ROJO, '② STOP LOSS', 3)}{ln(tp, VERDE, '③ TAKE PROFIT', 4)}</div></div>
<div class="p" data-s="5">Las 3 se definen <b class="oro">antes de entrar</b>, nunca después</div>
</div>"""


def riesgo():
    barra = lambda pct, col: f'<div style="height:26px;background:#222;border-radius:13px;overflow:hidden;margin-top:14px"><div style="width:{pct}%;height:100%;background:{col}"></div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">EN NÚMEROS</div>
<div class="row" data-s="1"><div class="card"><div class="lbl">Cuenta</div><div class="val">$1.000</div></div><div class="arrow">✕</div><div class="card"><div class="lbl">Riesgo</div><div class="val oro">1%</div></div><div class="arrow">=</div><div class="card"><div class="lbl">Pérdida máxima</div><div class="val">$10</div></div></div>
<div class="row">
<div class="card" data-s="2" style="width:600px;border-color:{VERDE};text-align:left"><div class="val verde" style="font-size:40px">✅ Riesgo 1%</div><div class="p" style="text-align:left;font-size:30px">5 pérdidas seguidas → <b>$950</b></div>{barra(95, VERDE)}</div>
<div class="card" data-s="3" style="width:600px;border-color:{ROJO};text-align:left"><div class="val rojo" style="font-size:40px">❌ Riesgo 50%</div><div class="p" style="text-align:left;font-size:30px">2 pérdidas → <b>cuenta quemada</b></div>{barra(2, ROJO)}</div>
</div></div>"""


def mitos():
    m = lambda s1, s2, t, r: f'<div style="display:flex;align-items:center;gap:26px"><div class="card" data-s="{s1}" style="width:760px;text-align:left;padding:24px 34px"><div class="val" style="font-size:40px">“{t}”</div></div><div data-s="{s2}" style="display:flex;align-items:center;gap:18px"><div class="pill" style="background:{ROJO};border-color:{ROJO};color:#fff">FALSO</div><div class="p" style="text-align:left;font-size:30px;width:560px">{r}</div></div></div>'
    return f"""<div class="stage" style="gap:24px">
<div class="pill" data-s="0">3 MITOS DEL TRADING</div>
{m(2,3,'Necesitas mucho dinero','Aprende gratis en demo, empieza con poco')}
{m(6,7,'Es como apostar','Método + gestión de riesgo = lógica')}
{m(10,11,'Te vuelves rico en un mes','Es una carrera de largo plazo')}
</div>"""


def ruta():
    pasos = [('1', 'Fundamentos', 1), ('2', 'Estructura', 2), ('3', 'SMC', 3), ('4', 'Modelo de entrada', 4), ('5', 'Instrumentos', 5), ('6', 'Experto', 6)]
    items = "".join(f'<div class="card" data-s="{s}" style="width:205px;padding:24px 12px{";border-color:" + ORO + ";box-shadow:0 0 40px rgba(212,175,55,.35)" if n == "1" else ""}"><div class="big oro" style="font-size:80px">{n}</div><div class="val" style="font-size:26px">{t}</div>{"<div class=pill style=font-size:18px;margin-top:12px>ESTÁS AQUÍ</div>" if n == "1" else ""}</div>' for n, t, s in pasos)
    return f"""<div class="stage">
<div class="pill" data-s="0">LA RUTA: DE CERO A EXPERTO</div>
<div class="row" style="gap:16px">{items}</div>
<div class="p" data-s="8">Síguela <b class="oro">en orden</b> y vas a entender el mercado</div>
</div>"""


def por_que_pierden():
    c = lambda s, n, i, t, e: f'<div class="card" data-s="{s}" style="width:470px;border-color:rgba(239,68,68,.5)"><div class="lbl">Razón {n}</div><div class="ico" style="margin:12px 0">{i}</div><div class="val" style="font-size:44px">{t}</div><div class="p" style="font-size:27px;margin-top:10px">{e}</div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0" style="border-color:{ROJO};color:{ROJO}">¿POR QUÉ PIERDEN?</div>
<div class="row">{c(2,1,'🗺️','Sin plan','Entran por lo que vieron en redes')}{c(5,2,'😰','Emociones','Miedo y avaricia mandan')}{c(8,3,'🔁','Sobreoperar','Más operaciones ≠ más ganancia')}</div>
<div class="p" data-s="11">El que gana <b class="oro">espera con paciencia</b> su oportunidad</div>
</div>"""


def realidad():
    return f"""<div class="stage" style="gap:24px">
<div class="h2" data-s="0" style="font-size:56px">¿Cuánto se puede <span class="oro">ganar</span>?</div>
<div class="card" data-s="2" style="width:1000px"><div class="val">No hay una cifra fija</div><div class="row" style="margin-top:22px;gap:18px"><div class="pill">💰 CAPITAL</div><div class="pill">⚖️ RIESGO</div><div class="pill">🔁 CONSISTENCIA</div></div></div>
<div class="card" data-s="4" style="width:1000px;border-color:{ORO}"><div class="lbl">Tu meta al principio</div><div class="val">Aprender a <span class="oro">no perder</span> y proteger tu cuenta</div></div>
<div class="p" data-s="6">Las ganancias son la <b class="oro">consecuencia</b> de un buen proceso</div>
</div>"""


def aprovechar():
    ck = lambda s, i, t: f'<div class="chk" data-s="{s}" style="font-size:48px"><b>{i}</b><span>{t}</span></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">CÓMO APROVECHAR LA SERIE</div>
<div style="display:flex;flex-direction:column;gap:24px">
{ck(1,'1','Mira los videos <span class="oro">en orden</span>')}
{ck(2,'2','Toma apuntes cortos')}
{ck(3,'3','Practica en tu <span class="oro">cuenta demo</span>')}
{ck(4,'4','Deja tus dudas en los <span class="oro">comentarios</span> 💬')}
</div></div>"""


# ================= VIDEO 2: MERCADOS =================
def _card(s, ico, tit, sub="", w=330, borde=None, extra=""):
    b = f";border-color:{borde}" if borde else ""
    return f'<div class="card" data-s="{s}" style="width:{w}px{b}"><div class="ico">{ico}</div><div class="val" style="font-size:40px">{tit}</div>{f"<div class=lbl>{sub}</div>" if sub else ""}{extra}</div>'


def _mercado(s_pill, n, ico, nombre, s_items, items, color=None):
    col = color or ORO
    filas = "".join(f'<div class="chk" data-s="{si}" style="font-size:38px"><b>✓</b><span>{t}</span></div>' for si, t in zip(s_items, items))
    return f"""<div class="stage" style="flex-direction:row;gap:80px">
<div style="text-align:center" data-s="{s_pill}"><div class="lbl">Mercado {n} de 6</div><div style="font-size:180px;line-height:1.1">{ico}</div><div class="h2" style="color:{col}">{nombre}</div></div>
<div style="display:flex;flex-direction:column;gap:30px;max-width:900px">{filas}</div></div>"""


def v2_gancho():
    return f"""<div class="stage">
<div class="row" data-s="0">{_card(0,'🥇','Oro')}{_card(0,'💱','Forex')}{_card(0,'₿','Cripto')}{_card(0,'📊','Índices')}</div>
<div class="h2" data-s="0">¿Todo al mismo tiempo? <span class="rojo">Error</span></div>
<div class="p" data-s="1">Cada mercado <b class="oro">se mueve distinto</b></div>
<div class="pill" data-s="2">LOS 6 MERCADOS · HORARIOS · CUÁL ELEGIR</div>
</div>"""


def v2_marca():
    return f"""<div class="stage">
<img src="{LOGO}" style="height:300px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.7))">
<div class="row" data-s="1"><div class="card"><div class="lbl">Serie</div><div class="val">Fundamentos</div></div><div class="card"><div class="lbl">Video</div><div class="val oro">#2</div></div></div>
<div class="p" data-s="2">Antes: qué es el trading → <b class="oro">Hoy: los mercados</b></div>
</div>"""


def v2_activo():
    return f"""<div class="stage">
<div class="pill" data-s="0">PALABRA CLAVE</div>
<div class="h1" data-s="1">ACTIVO</div>
<div class="p" data-s="2">Cualquier cosa que puedes <b class="oro">comprar o vender</b> en trading</div>
<div class="row" data-s="3">{_card(3,'💶','Moneda',w=260)}{_card(3,'🥇','Oro',w=260)}{_card(3,'🏢','Acción',w=260)}{_card(3,'₿','Bitcoin',w=260)}</div>
<div class="p" data-s="4">Cada uno: <b class="oro">gráfico · horario · personalidad</b></div>
</div>"""


def v2_forex():
    return _mercado(1, 1, "💱", "Forex", [2, 3, 5, 5], ["Se compran y venden <span class='oro'>monedas</span>", "El mercado <span class='oro'>más grande del mundo</span>", "24 horas, <span class='oro'>lunes a viernes</span>", "Mucha liquidez"])


def v2_par():
    return f"""<div class="stage">
<div class="pill" data-s="0">CÓMO SE LEE UN PAR</div>
<div class="row" data-s="1" style="align-items:center"><div class="card"><div class="ico">🇪🇺</div><div class="val">EUR</div><div class="lbl">Base</div></div><div class="arrow">/</div><div class="card"><div class="ico">🇺🇸</div><div class="val">USD</div><div class="lbl">Cotización</div></div><div class="arrow">=</div><div class="card" style="border-color:{ORO}"><div class="val oro" style="font-size:70px">1.08</div><div class="lbl">1 € = 1,08 $</div></div></div>
<div class="row"><div class="card" data-s="3" style="border-color:{VERDE};width:560px"><div class="val verde">COMPRAS ▲</div><div class="p" style="font-size:28px">El euro se fortalece</div></div><div class="card" data-s="4" style="border-color:{ROJO};width:560px"><div class="val rojo">VENDES ▼</div><div class="p" style="font-size:28px">El euro se debilita</div></div></div>
</div>"""


def v2_mayores():
    par = lambda s, a, b: f'<div class="card" data-s="{s}" style="width:300px;padding:26px"><div class="val" style="font-size:44px">{a}<span class="oro">/{b}</span></div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">PARES MAYORES (todos con USD)</div>
<div class="row">{par(1,'EUR','USD')}{par(1,'GBP','USD')}{par(1,'USD','JPY')}{par(1,'AUD','USD')}</div>
<div class="row">{par(1,'USD','CHF')}{par(1,'USD','CAD')}{par(1,'NZD','USD')}</div>
<div class="p" data-s="2">Para empezar: <b class="oro">más ordenados y más baratos</b></div>
</div>"""


def v2_oro():
    return _mercado(1, 2, "🥇", "Oro · XAUUSD", [2, 3, 5, 7], ["Oro contra el dólar", "<span class='oro'>Activo refugio</span>: sube con el miedo", "Se mueve fuerte: <span class='oro'>oportunidad</span> y <span class='rojo'>riesgo</span>", "Gestión de riesgo <span class='oro'>todavía más importante</span>"])


def v2_indices():
    return _mercado(0, 3, "📊", "Índices", [1, 2, 2, 4], ["Varias empresas en <span class='oro'>un solo precio</span>", "<span class='oro'>Nasdaq</span>: tecnología", "<span class='oro'>Dow Jones</span>: 30 gigantes de EE.UU.", "Se mueven en la <span class='oro'>apertura de Nueva York</span>"])


def v2_materias():
    return _mercado(0, 4, "🛢️", "Materias primas", [0, 1, 2], ["Petróleo · plata", "Dependen de <span class='oro'>producción y conflictos</span>", "Para empezar: <span class='rojo'>no son las más sencillas</span>"])


def v2_cripto():
    return _mercado(0, 5, "₿", "Criptomonedas", [1, 2, 3], ["<span class='oro'>24/7</span>, incluso fines de semana", "Se mueven <span class='oro'>muchísimo</span> en poco tiempo", "<span class='rojo'>De las más peligrosas</span> para principiantes"])


def v2_sinteticos():
    t = lambda s, n, e: f'<div class="card" data-s="{s}" style="width:330px"><div class="val" style="font-size:40px">{n}</div><div class="p" style="font-size:26px;margin-top:8px">{e}</div></div>'
    return f"""<div class="stage">
<div class="h2" data-s="0">⚡ Mercado 6 de 6: <span class="oro">Índices sintéticos</span></div>
<div class="row" data-s="1"><div class="pill">🤖 CREADOS POR UN ALGORITMO</div><div class="pill" data-s="3">🕐 24/7</div><div class="pill" data-s="3">📰 SIN NOTICIAS</div></div>
<div class="row">{t(5,'Crash / Boom','Picos fuertes')}{t(5,'Volatility','Niveles de movimiento')}{t(5,'Step','Pasos fijos')}</div>
<div class="p" data-s="6">Solo algunos brókers · <b class="rojo">alto riesgo</b></div>
</div>"""


def v2_cfd():
    return f"""<div class="stage">
<div class="pill" data-s="0">ALGO IMPORTANTE</div>
<div class="row" data-s="1"><div class="card" style="width:520px"><div class="ico">🚫📦</div><div class="val">No compras el activo real</div></div><div class="card" data-s="3" style="width:520px;border-color:{ORO}"><div class="ico">📈</div><div class="val">Operas el <span class="oro">precio</span></div><div class="lbl">Contrato con tu bróker</div></div></div>
<div class="card" data-s="5" style="width:1080px;border-color:{ROJO}"><div class="val">⚠️ Apalancamiento: multiplica <span class="verde">ganancias</span> y <span class="rojo">pérdidas</span></div></div>
</div>"""


def v2_comparativa():
    fila = lambda s, m, h, v, n: f'<tr data-s="{s}"><td>{m}</td><td>{h}</td><td>{v}</td><td>{n}</td></tr>'
    return f"""<div class="stage">
<style>table{{border-collapse:collapse;font-size:42px}} td,th{{padding:18px 40px;border-bottom:1px solid rgba(212,175,55,.25);text-align:left}} th{{color:#bfae7a;font-size:22px;letter-spacing:2px;text-transform:uppercase}} td:first-child{{font-weight:800}}</style>
<div class="pill" data-s="0">LADO A LADO</div>
<table><tr><th>Mercado</th><th>Horario</th><th>Movimiento</th><th>Noticias</th></tr>
{fila(1,'💱 Forex','Lun–Vie','Moderado','Sí')}
{fila(2,'🥇 Oro','Lun–Vie','<span class=rojo>Fuerte</span>','Mucho')}
{fila(3,'📊 Índices','Horario de bolsa','Medio-alto','Sí')}
{fila(4,'₿ Cripto','Todos los días','<span class=rojo>Muy alto</span>','Sí')}
{fila(5,'⚡ Sintéticos','Todos los días','<span class=rojo>Brusco</span>','<span class=verde>No</span>')}
</table></div>"""


def v2_horarios():
    ses = lambda s, ico, n, h: f'<div class="card" data-s="{s}" style="width:400px"><div class="ico">{ico}</div><div class="val">{n}</div><div class="p" style="font-size:30px;margin-top:8px">{h}</div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">SESIONES · HORA COLOMBIA 🇨🇴</div>
<div class="row">{ses(2,'🌏','Asia','Noche')}{ses(3,'🇬🇧','Londres','2:00 – 3:00 a.m.')}{ses(4,'🇺🇸','Nueva York','7:00 – 8:00 a.m.')}</div>
<div class="card" data-s="5" style="border-color:{ORO};width:1000px"><div class="val">🔥 Londres + Nueva York = <span class="oro">más movimiento</span></div><div class="lbl">En la mañana de Colombia</div></div>
</div>"""


def v2_elegir():
    c = lambda s, n, i, t, e: f'<div class="card" data-s="{s}" style="width:440px"><div class="lbl">{n}</div><div class="ico" style="margin:10px 0">{i}</div><div class="val">{t}</div><div class="p" style="font-size:26px;margin-top:8px">{e}</div></div>'
    return f"""<div class="stage">
<div class="h2" data-s="0">¿Cuál te conviene <span class="oro">a ti</span>?</div>
<div class="row">{c(2,'Primero','⏰','Tu tiempo','¿Mañanas, noches o fines de semana?')}{c(4,'Segundo','💓','Tu riesgo','¿Te ponen nervioso los movimientos fuertes?')}{c(6,'Tercero','💰','Tu capital','Que puedas operar pequeño')}</div>
</div>"""


def v2_recomendacion():
    return f"""<div class="stage">
<div class="pill" data-s="0">MI RECOMENDACIÓN</div>
<div class="row">
<div class="card" data-s="1" style="width:580px"><div class="ico">🌅</div><div class="lbl">Mañanas libres</div><div class="val">Euro dólar → <span class="oro">Oro</span></div></div>
<div class="card" data-s="2" style="width:580px"><div class="ico">🌙</div><div class="lbl">Noches / fines de semana</div><div class="val">Sintéticos <span class="oro">en demo</span></div><div class="p" style="font-size:26px">Con riesgo muy pequeño</div></div>
</div>
<div class="h2" data-s="3">Escoge <span class="oro">uno solo</span> y domínalo</div>
</div>"""


def v2_error():
    return f"""<div class="stage">
<div class="pill" data-s="0" style="border-color:{ROJO};color:{ROJO}">ERROR COMÚN</div>
<div class="row" data-s="1"><div class="card"><div class="val">Hoy 🥇</div></div><div class="card"><div class="val">Mañana ₿</div></div><div class="card"><div class="val">Pasado 📊</div></div></div>
<div class="p" data-s="2">Así <b class="rojo">nunca aprendes</b> cómo se mueve ninguno</div>
<div class="h1" data-s="5" style="font-size:84px">Menos mercados, <span class="oro">más dominio</span></div>
</div>"""


def v2_mio():
    return f"""<div class="stage">
<img src="{JV}" style="height:170px">
<div class="lbl" data-s="0">Lo que yo opero</div>
<div class="row" data-s="0">{_card(0,'🥇','Oro')}{_card(0,'💶','Euro dólar')}{_card(0,'⚡','Sintéticos')}</div>
<div class="p" data-s="2">La estructura y el SMC <b class="oro">sirven para cualquier activo</b></div>
</div>"""


def v2_resumen():
    ck = lambda s, t: f'<div class="chk" data-s="{s}"><b>✓</b><span>{t}</span></div>'
    return f"""<div class="stage"><div class="pill" data-s="0">RESUMEN</div>
<div style="display:flex;flex-direction:column;gap:24px">
{ck(1,'6 mercados: forex, oro, índices, materias, cripto, sintéticos')}
{ck(3,'Cada uno tiene su horario y su personalidad')}
{ck(4,'Operas el precio, no el activo real')}
{ck(5,'<span class="oro">Escoge uno y domínalo</span>')}
</div></div>"""


def v2_cierre():
    return f"""<div class="stage">
<img src="{JV}" style="height:150px">
<div class="lbl" data-s="0">Siguiente video</div>
<div class="card" data-s="0" style="width:1150px"><div class="val">#3 · Qué es un bróker y <span class="oro">cómo no caer en estafas</span></div></div>
<div class="row" data-s="2"><div class="pill" style="background:{ROJO};border-color:{ROJO};color:#fff">▶ SUSCRÍBETE</div><div class="pill">🔔 ACTIVA LA CAMPANITA</div></div>
<div class="p" data-s="3">📅 Agenda una llamada conmigo · <b class="oro">link en la descripción</b></div>
<div class="p" style="font-size:22px;color:#8a826c;margin-top:20px">Contenido educativo. El trading implica riesgo de pérdida de capital.</div>
</div>"""


# ---- Short 2 ----
def s2_gancho():
    return f"""<div class="stage" style="top:200px;bottom:700px"><div class="pill">PRINCIPIANTES</div>
<div class="h1" style="font-size:110px">¿Qué mercado <span class="oro">operar</span>?</div><div style="font-size:130px">🥇💱⚡</div></div>"""


def s2_tiempo():
    return f"""<div class="stage" style="top:200px;bottom:700px"><div class="h2" style="font-size:76px">Depende de <span class="oro">tu tiempo</span></div>
<div class="card" data-s="1" style="width:880px"><div class="ico">🌅</div><div class="lbl" style="font-size:30px">Mañanas libres</div><div class="val" style="font-size:66px">Euro dólar → <span class="oro">Oro</span></div></div></div>"""


def s2_noche():
    return f"""<div class="stage" style="top:200px;bottom:700px"><div class="card" style="width:880px"><div class="ico">🌙</div><div class="lbl" style="font-size:30px">Noches / fines de semana</div><div class="val" style="font-size:66px">Sintéticos</div><div class="pill" data-s="1" style="margin-top:20px;font-size:36px">PRIMERO EN DEMO</div></div></div>"""


def s2_regla():
    return f"""<div class="stage" style="top:200px;bottom:700px"><div class="lbl" style="font-size:36px">La regla de oro</div>
<div class="h1" data-s="1" style="font-size:110px">Escoge <span class="oro">uno</span> y domínalo</div>
<div class="p" data-s="2" style="font-size:46px">El que opera todo, <b class="rojo">no domina nada</b></div></div>"""


def s2_cta():
    return s_cta()


def v2_noticias():
    n = lambda s, i, t: f'<div class="card" data-s="{s}" style="width:400px"><div class="ico">{i}</div><div class="val" style="font-size:38px">{t}</div></div>'
    return f"""<div class="stage">
<div class="pill" data-s="0">📰 NOTICIAS QUE MUEVEN EL PRECIO</div>
<div class="row">{n(2,'👷','Empleo EE.UU.')}{n(2,'🛒','Inflación')}{n(2,'🏦','Tasas de interés')}</div>
<div class="p" data-s="3">En segundos se mueve <b class="rojo">lo que normalmente toma horas</b></div>
<div class="card" data-s="4" style="width:1000px;border-color:{ORO}"><div class="val">📅 Revisa el <span class="oro">calendario económico</span></div><div class="lbl" data-s="5">Principiante: sin operaciones abiertas en la noticia</div></div>
</div>"""


def v2_tarea():
    ck = lambda s, i, t: f'<div class="chk" data-s="{s}" style="font-size:44px"><b>{i}</b><span>{t}</span></div>'
    return f"""<div class="stage"><div class="pill" data-s="0">📝 TAREA DE LA SEMANA</div>
<div style="display:flex;flex-direction:column;gap:26px">
{ck(1,'1','Abre una cuenta demo')}
{ck(1,'2','Agrega <span class="oro">euro dólar · oro · un sintético</span>')}
{ck(2,'3','No operes: <span class="oro">solo observa</span> a distintas horas')}
{ck(3,'4','Anota cuál se mueve más y cuál va con tu horario')}
</div></div>"""


def intro_frame(t, w=1920, h=1080):
    """t de 0 a 1. Logo aparece con zoom, destello dorado y barrido de luz."""
    import math
    e = 1 - (1 - min(t / 0.35, 1)) ** 3
    esc = 0.82 + 0.18 * e + 0.03 * t
    op = min(t / 0.25, 1) * (1 - max(0, (t - 0.9) / 0.1))
    barr = -60 + 220 * min(max((t - 0.3) / 0.45, 0), 1)
    glow = math.exp(-((t - 0.32) / 0.12) ** 2)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}
.c{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}}
.halo{{position:absolute;width:{900*w/1920}px;height:{900*w/1920}px;border-radius:50%;background:radial-gradient(circle,rgba(245,217,122,{0.35*glow+0.12*op}) 0%,rgba(212,175,55,0) 65%)}}
.wrap{{position:relative;transform:scale({esc});opacity:{op}}}
.wrap img{{height:{620*w/1920 if w>h else 560}px;display:block;filter:drop-shadow(0 30px 60px rgba(0,0,0,.8))}}
.sh{{position:absolute;inset:0;-webkit-mask:url({LOGO}) center/contain no-repeat;mask:url({LOGO}) center/contain no-repeat;background:linear-gradient(105deg,transparent {barr}%,rgba(255,255,255,.85) {barr+8}%,transparent {barr+16}%)}}
</style></head><body><div class="grid" style="opacity:{op}"></div><div class="c"><div class="halo"></div><div class="wrap"><img src="{LOGO}"><div class="sh"></div></div></div></body></html>"""


ESCENAS = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_")}


def pagina(nombre, paso, w, h):
    cuerpo = ESCENAS[nombre]()
    vertical = h > w
    extra = ".stage{padding:0 70px}.logo{font-size:46px;top:70px;left:70px}.logo img{height:96px}" if vertical else ".stage{zoom:1.15;top:100px;bottom:180px}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}{extra}</style></head>
<body><div class="grid"></div><div class="logo"><img src="{JV}"><div>JulianVal<span>.fx</span></div></div>{'' if vertical else '<div class="tag">Trading de cero a experto</div>'}
{cuerpo}
<script>document.querySelectorAll('[data-s]').forEach(e=>{{if(+e.dataset.s>{paso})e.classList.add('hide')}});</script>
</body></html>"""
