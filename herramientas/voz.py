"""Genera la voz (Gonzalo) por frase para cada guion en guiones/*.json.
Salida: audio/<id>/<escena>_<frase>.mp3  (solo genera lo que falta)."""
import asyncio, json, glob, os, re, sys, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import edge_tts
from pronunciacion import aplicar

VOZ = "es-CO-GonzaloNeural"
VELOCIDAD = "+5%"

def nombre(v, j, f):
    return f"{v}_{j:02d}_{hashlib.md5(f.encode()).hexdigest()[:6]}.mp3"


def frases(texto):
    partes = re.split(r"(?<=[.!?:])\s+", texto.strip())
    return [p for p in partes if p]

async def main():
    for g in sorted(glob.glob("guiones/*.json")):
        d = json.load(open(g, encoding="utf-8"))
        out = f"audio/{d['id']}"; os.makedirs(out, exist_ok=True)
        validos = set()
        for i, esc in enumerate(d["escenas"]):
            for j, f in enumerate(frases(esc["texto"])):
                ruta = f"{out}/{nombre(esc['v'], j, f)}"; validos.add(os.path.basename(ruta))
                if os.path.exists(ruta):
                    continue
                for intento in range(3):
                    try:
                        await edge_tts.Communicate(aplicar(f), VOZ, rate=VELOCIDAD).save(ruta)
                        break
                    except Exception as e:
                        print("reintento", ruta, e); await asyncio.sleep(3)
                print(ruta, "|", aplicar(f))
        for viejo in os.listdir(out):
            if viejo not in validos:
                os.remove(f"{out}/{viejo}")

asyncio.run(main())
