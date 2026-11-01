"""Diccionario de pronunciación: cambia palabras para que la voz IA las diga bien."""
import re, sys
CAMBIOS = {
    r"\bJulianVal\.fx\b": "Julián Val punto efe equis",
    r"\bJulianVal\b": "Julián Val",
    r"\bJulian\b": "Julián",
    r"\btrading\b": "tréiding",
    r"\bTrading\b": "Tréiding",
    r"\btrader(s?)\b": r"tréider\1",
    r"\bTrader(s?)\b": r"Tréider\1",
    r"\bSMC\b": "ese eme ce",
    r"\bSmart Money Concepts\b": "Esmart Moni Cónsepts",
    r"\bOrder Blocks?\b": "Órder Blok",
    r"\bFVG\b": "efe ve ge",
    r"\bBOS\b": "bos",
    r"\bCHoCH\b": "chok",
    r"\bXAUUSD\b": "equis, a, u, u, ese, de",
    r"\bMT5\b": "Meta Tréider cinco",
    r"\bMetaTrader\b": "Meta Tréider",
    r"\bforex\b": "fórex",
    r"\bstop loss\b": "estop los",
    r"\btake profit\b": "teik prófit",
    r"\bSKY Academy\b": "Skai Académi",
    r"\bYouTube\b": "Iutub",
    r"\bNasdaq\b": "Násdak",
    r"\bDow Jones\b": "Dau Yons",
    r"\bCrash\b": "Crash",
    r"\bBoom\b": "Bum",
    r"\bVolatility\b": "Volátiliti",
    r"\bStep\b": "Estep",
    r"\bbitcoin\b": "bítcoin",
    r"\bShorts?\b": "Shorts",
}
def aplicar(texto):
    for k, v in CAMBIOS.items():
        texto = re.sub(k, v, texto)
    return texto
if __name__ == "__main__":
    print(aplicar(open(sys.argv[1], encoding="utf-8").read()))
