"""Arma el video final: escenas (HTML -> imagen), voz, subtítulos.
Uso: python herramientas/render.py guiones/v01.json salida/v01.mp4"""
import json, os, re, subprocess, sys, wave, shutil
import numpy as np
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(__file__))
from escenas import pagina, intro_frame
import musica as MU

SR = 48000
FPS = 30


def frases(texto):
    return [p for p in re.split(r"(?<=[.!?:])\s+", texto.strip()) if p]


def leer_mp3(ruta):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", ruta, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16)


def recortar_silencio(a, umbral=300):
    idx = np.where(np.abs(a) > umbral)[0]
    if len(idx) == 0:
        return a
    ini = max(idx[0] - int(0.03 * SR), 0)
    fin = min(idx[-1] + int(0.08 * SR), len(a))
    return a[ini:fin]


def t_ass(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def trozos(frase, max_palabras):
    pal = frase.split()
    n = max(1, round(len(pal) / max_palabras + 0.49))
    tam = -(-len(pal) // n)
    return [" ".join(pal[i:i + tam]) for i in range(0, len(pal), tam)]


def main(guion, salida):
    d = json.load(open(guion, encoding="utf-8"))
    vertical = d["formato"] == "vertical"
    W, H = (1080, 1920) if vertical else (1920, 1080)
    adir = f"audio/{d['id']}"
    tmp = f"/tmp/render_{d['id']}"
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)

    # 1) Voz y tiempos
    pistas, segmentos, t = [], [], 0.35
    pistas.append(np.zeros(int(0.35 * SR), np.int16))
    intro_ini = None
    for i, esc in enumerate(d["escenas"]):
        if esc["v"] == "intro":
            dur = 3.4
            segmentos.append(dict(esc=i, paso=0, ini=t, voz=0, fin=t + dur, texto="", v="intro"))
            pistas.append(np.zeros(int(dur * SR), np.int16)); intro_ini = t; t += dur
            continue
        fs = frases(esc["texto"])
        for j, f in enumerate(fs):
            a = recortar_silencio(leer_mp3(f"{adir}/{esc['v']}_{j:02d}.mp3"))
            pausa = 0.12 if f.endswith(":") else 0.28
            if j == len(fs) - 1:
                pausa = 0.55
            dur = len(a) / SR
            segmentos.append(dict(esc=i, paso=j, ini=t, voz=dur, fin=t + dur + pausa, texto=f, v=esc["v"]))
            pistas.append(a); pistas.append(np.zeros(int(pausa * SR), np.int16))
            t += dur + pausa
    total = t + 0.6
    pistas.append(np.zeros(int(0.6 * SR), np.int16))
    voz = np.concatenate(pistas).astype(np.float64) / 32768
    from scipy.ndimage import uniform_filter1d
    env = uniform_filter1d(np.abs(voz), int(0.35 * SR))
    hay_voz = np.clip(env / 0.02, 0, 1)
    fondo = MU.musica(len(voz) / SR, seed=hash(d["id"]) % 100)
    fondo = fondo[:len(voz)] * (0.30 - 0.20 * hay_voz)
    if intro_ini is not None:
        sfx = np.concatenate([MU.whoosh(0.7) * 0.5, MU.brillo_logo() * 0.9])
        k = int(max(intro_ini - 0.35, 0) * SR)
        fondo[k:k + len(sfx)] += sfx[:len(fondo) - k]
    mezcla = voz + fondo
    mezcla = mezcla / max(1.0, np.abs(mezcla).max() / 0.95)
    with wave.open(f"{tmp}/voz.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mezcla * 32767).astype(np.int16).tobytes())

    # 2) Imágenes: una por frase (los elementos van apareciendo)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for k, s in enumerate(segmentos):
            if s["v"] == "intro":
                n = int(round((s["fin"] - s["ini"]) * FPS))
                for f in range(n):
                    pg.set_content(intro_frame(f / (n - 1), W, H))
                    pg.screenshot(path=f"{tmp}/{k:03d}_{f:03d}.jpg", type="jpeg", quality=92)
                s["frames"] = n
                continue
            pg.set_content(pagina(s["v"], s["paso"], W, H))
            pg.wait_for_timeout(60)
            pg.screenshot(path=f"{tmp}/{k:03d}.jpg", type="jpeg", quality=92)
        b.close()

    # 3) Lista de imágenes con duración (la primera arranca en 0)
    with open(f"{tmp}/lista.txt", "w") as L:
        for k, s in enumerate(segmentos):
            ini = 0 if k == 0 else s["ini"]
            fin = segmentos[k + 1]["ini"] if k + 1 < len(segmentos) else total
            if s["v"] == "intro":
                for f in range(s["frames"]):
                    L.write(f"file '{tmp}/{k:03d}_{f:03d}.jpg'\nduration {1 / FPS:.5f}\n")
                continue
            L.write(f"file '{tmp}/{k:03d}.jpg'\nduration {fin - ini:.3f}\n")
        L.write(f"file '{tmp}/{len(segmentos) - 1:03d}.jpg'\n")

    # 4) Subtítulos
    fs_ = 76 if vertical else 50
    mv = 560 if vertical else 60
    ass = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Sub,Inter ExtraBold,{fs_},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,{6 if vertical else 4},2,2,90,90,{mv},1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for s in segmentos:
        if not s["texto"]:
            continue
        partes = trozos(s["texto"], 5 if vertical else 9)
        nchar = sum(len(x) for x in partes)
        t0 = s["ini"]
        for x in partes:
            dt = s["voz"] * len(x) / nchar
            ass.append(f"Dialogue: 0,{t_ass(t0)},{t_ass(t0 + dt)},Sub,,0,0,0,,{x}")
            t0 += dt
    open(f"{tmp}/subs.ass", "w", encoding="utf-8").write("\n".join(ass))

    # 5) Render final
    os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
    tmp_out = salida.replace(".mp4", ".tmp.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/lista.txt", "-i", f"{tmp}/voz.wav",
           "-vf", f"fps={FPS},format=yuv420p,subtitles={tmp}/subs.ass,fade=t=in:st=0:d=0.4,fade=t=out:st={total - 0.5:.2f}:d=0.5",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-movflags", "+faststart", "-t", f"{total:.2f}", tmp_out]
    subprocess.run(cmd, check=True)
    os.replace(tmp_out, salida)
    json.dump(segmentos, open(salida.replace(".mp4", ".tiempos.json"), "w"), ensure_ascii=False, indent=1)
    print(f"OK {salida}  {total:.1f}s  {len(segmentos)} frases")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
