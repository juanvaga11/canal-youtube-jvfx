"""Música de fondo y efectos generados por código (100% propios, sin derechos de autor)."""
import numpy as np

SR = 48000


def _env(n, ataque, caida):
    e = np.ones(n)
    a = int(ataque * SR); c = int(caida * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if c: e[-c:] *= np.linspace(1, 0, c)
    return e


def _nota(f, dur, vol=1.0, ataque=0.8, caida=1.2, brillo=0.25):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for det in (-0.12, 0.0, 0.11):
        ff = f * 2 ** (det / 12)
        s += np.sin(2 * np.pi * ff * t) + brillo * np.sin(2 * np.pi * 2 * ff * t) * np.exp(-t * 0.8)
    return s * _env(len(t), ataque, caida) * vol / 3


def _campana(f, dur=1.6, vol=0.3):
    t = np.arange(int(dur * SR)) / SR
    s = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.01 * t) + 0.15 * np.sin(2 * np.pi * f * 3.98 * t))
    return s * np.exp(-t * 3.2) * _env(len(t), 0.005, 0.05) * vol


def _reverb(x, mezcla=0.3):
    out = x.copy()
    for d, g in ((0.031, .5), (0.047, .45), (0.071, .4), (0.113, .33), (0.167, .27), (0.241, .2), (0.353, .14)):
        k = int(d * SR)
        out[k:] += x[:-k] * g * mezcla
    return out


def _paso_bajo(x, corte=1800):
    from scipy.signal import lfilter
    a = np.exp(-2 * np.pi * corte / SR)
    return lfilter([1 - a], [1, -a], x)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def musica(duracion, seed=1):
    """Pad suave tipo 'lo-fi ambiental' en loop: Am - F - C - G, 72 bpm."""
    rnd = np.random.default_rng(seed)
    acordes = [[57, 60, 64], [53, 57, 60], [48, 55, 64], [55, 59, 62]]
    bajos = [45, 41, 48, 43]
    compas = 4 * 60 / 72
    ciclo = int(compas * 4 * SR)
    loop = np.zeros(ciclo + SR * 3)
    for k, (ac, b) in enumerate(zip(acordes, bajos)):
        ini = int(k * compas * SR)
        for m in ac:
            s = _nota(hz(m), compas + 1.2, 0.20, 0.9, 1.4)
            loop[ini:ini + len(s)] += s
        s = _nota(hz(b - 12), compas + 0.8, 0.22, 0.3, 1.0, 0.1)
        loop[ini:ini + len(s)] += s
        for n in range(4):
            if rnd.random() < 0.75:
                m = ac[rnd.integers(0, 3)] + 12
                s = _campana(hz(m), 1.8, 0.07)
                p = ini + int(n * compas / 4 * SR)
                loop[p:p + len(s)] += s
    cola = loop[ciclo:]; loop = loop[:ciclo].copy(); loop[:len(cola)] += cola
    loop = _reverb(loop, 0.35)
    reps = int(np.ceil(duracion * SR / len(loop))) + 1
    out = np.tile(loop, reps)[:int(duracion * SR)]
    out = _paso_bajo(out, 2200)
    out *= _env(len(out), 1.5, 2.5)
    return out / (np.abs(out).max() + 1e-9) * 0.5


def whoosh(dur=1.0):
    n = int(dur * SR)
    ruido = np.random.default_rng(3).standard_normal(n)
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 2
    y = np.empty(n); acc = 0.0
    for i in range(n):
        corte = 300 + 5000 * env[i]
        a = np.exp(-2 * np.pi * corte / SR)
        acc = (1 - a) * ruido[i] + a * acc; y[i] = acc
    return y * env / (np.abs(y).max() + 1e-9) * 0.6


def brillo_logo():
    """Acorde brillante para la aparición del logo."""
    out = np.zeros(int(3.0 * SR))
    for m, d in ((69, 0), (73, 0.06), (76, 0.12), (81, 0.18), (88, 0.26)):
        s = _campana(hz(m), 2.6, 0.22)
        p = int(d * SR); out[p:p + len(s)] += s[:len(out) - p]
    s = _nota(hz(45), 2.8, 0.35, 0.02, 1.8, 0.1)
    out[:len(s)] += s
    return _reverb(out, 0.45)


def clic():
    n = int(0.03 * SR)
    r = np.random.default_rng(5).standard_normal(n) * np.exp(-np.linspace(0, 12, n))
    return _paso_bajo(r, 4000) * 1.5
