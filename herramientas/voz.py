"""Genera la voz (Gonzalo) por frase para cada guion en guiones/*.json.
Salida: audio/<id>/<escena>_<frase>.mp3  (solo genera lo que falta)."""
import asyncio, json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import edge_tts
from pronunciacion import aplicar

VOZ = "es-CO-GonzaloNeural"
VELOCIDAD = "+5%"

def frases(texto):
    partes = re.split(r"(?<=[.!?:])\s+", texto.strip())
    return [p for p in partes if p]

async def main():
    for g in sorted(glob.glob("guiones/*.json")):
        d = json.load(open(g, encoding="utf-8"))
        out = f"audio/{d['id']}"; os.makedirs(out, exist_ok=True)
        for i, esc in enumerate(d["escenas"]):
            for j, f in enumerate(frases(esc["texto"])):
                ruta = f"{out}/{i:02d}_{j:02d}.mp3"
                if os.path.exists(ruta):
                    continue
                for intento in range(3):
                    try:
                        await edge_tts.Communicate(aplicar(f), VOZ, rate=VELOCIDAD).save(ruta)
                        break
                    except Exception as e:
                        print("reintento", ruta, e); await asyncio.sleep(3)
                print(ruta, "|", aplicar(f))

asyncio.run(main())
