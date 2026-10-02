#!/usr/bin/env python3
"""Genera data.json per il sito: hardware + modelli + quantizzazioni + costanti.

Questo e' il punto dove, in futuro, entra la RACCOLTA AUTOMATICA (scraping di listini
hardware e del catalogo modelli di Ollama). Oggi i dati sono curati a mano in data.py:
la raccolta automatica e' un rischio legale/tecnico (siti che cambiano, blocchi, ToS),
quindi NON e' attiva. Se un giorno si attiva, si aggiorna data.py e si rilancia questo.

Uso:  python3 genera_dati.py
"""
import json
from pathlib import Path

import data as D
import engine as E

OUT = Path(__file__).parent / "data.json"


def main():
    payload = {
        "cpus": sorted(D.CPUS, key=lambda c: c["name"]),
        "gpus": sorted(D.GPUS, key=lambda g: (g["brand"], -g["tput"])),
        "igpus": D.IGPUS,
        "ram": D.RAM_TYPES,
        "hd": D.HD_TYPES,
        "quants": D.QUANTS,
        "models": sorted(D.MODELS, key=lambda m: m["params"]),
        "efficiency": D.EFFICIENCY,
        "overhead_gb": D.OVERHEAD_GB,
        "use_cases": D.USE_CASES,
        "meta": {
            "nota": "Banda di memoria in GB/s (valori pratici). Token/s = banda/modello*0,65.",
            "modelli": len(D.MODELS), "cpu": len(D.CPUS), "gpu": len(D.GPUS),
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"scritto {OUT} ({OUT.stat().st_size} byte) - {payload['meta']}")


if __name__ == "__main__":
    main()
