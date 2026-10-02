#!/usr/bin/env python3
"""Genera data.json per il sito: hardware + modelli + quantizzazioni + costanti.

Questo e' il punto dove, in futuro, entra la RACCOLTA AUTOMATICA (scraping di listini
hardware e del catalogo modelli di Ollama). Oggi i dati sono curati a mano in data.py:
la raccolta automatica e' un rischio legale/tecnico (siti che cambiano, blocchi, ToS),
quindi NON e' attiva. Se un giorno si attiva, si aggiorna data.py e si rilancia questo.

Uso:  python3 genera_dati.py
"""
import json
from datetime import date
from pathlib import Path

import data as D
import engine as E

OUT = Path(__file__).parent / "data.json"
AUTO = Path(__file__).parent / "models_auto.json"


def _unisci_modelli():
    """Base = modelli curati a mano (nomi leggibili, stile Ollama). Gli automatici da HF
    si aggiungono SOLO se portano un modello nuovo: stessa famiglia con parametri entro
    il 20% = considerato gia' presente."""
    uniti = [dict(m) for m in D.MODELS]
    auto, aggiornato = [], None
    if AUTO.exists():
        blob = json.loads(AUTO.read_text(encoding="utf-8"))
        auto = blob.get("modelli", [])
        aggiornato = (blob.get("generato") or "")[:10]

    def fam(m):
        f = (m.get("family") or "").lower()
        return "mistral" if f == "mixtral" else f

    def presente(m):
        # tolleranza simmetrica: l'automatico ricava i parametri dal nome (2B), il curato
        # li ha reali (2,61B). Confronto sul maggiore dei due.
        return any(fam(x) == fam(m)
                   and abs(x["params"] - m["params"]) <= 0.35 * max(x["params"], m["params"], 1)
                   for x in uniti)

    n_nuovi = 0
    for m in auto:
        if not presente(m):
            m = dict(m)
            m["auto"] = True
            uniti.append(m)
            n_nuovi += 1
    # Guardia anti-duplicati: senza questa, un modello ri-aggiunto a mano finisce due volte
    # nella tendina. Si tiene il primo (i curati vengono prima degli automatici).
    visti_id, visti_nome, senza_dup = set(), set(), []
    for m in uniti:
        m["auto"] = bool(m.get("auto"))
        chiave = m["name"].lower()
        if m["id"] in visti_id or chiave in visti_nome:
            continue
        visti_id.add(m["id"]); visti_nome.add(chiave); senza_dup.append(m)
    uniti = senza_dup
    uniti.sort(key=lambda x: x["name"].lower())
    return uniti, n_nuovi, aggiornato


def main():
    modelli, n_auto, aggiornato = _unisci_modelli()
    payload = {
        "cpus": sorted(D.CPUS, key=lambda c: c["name"]),
        "gpus": sorted(D.GPUS, key=lambda g: (g["brand"], -g["tput"])),
        "igpus": D.IGPUS,
        "ram": D.RAM_TYPES,
        "ram_sizes": D.RAM_SIZES,
        "hd": D.HD_TYPES,
        "quants": D.QUANTS,
        "models": modelli,
        "efficiency": D.EFFICIENCY,
        "overhead_gb": D.OVERHEAD_GB,
        "use_cases": D.USE_CASES,
        "meta": {
            "nota": "Banda di memoria in GB/s (valori pratici). Token/s = banda/modello*0,65.",
            "modelli": len(modelli), "cpu": len(D.CPUS), "gpu": len(D.GPUS),
            "modelli_auto": n_auto, "dati_aggiornati": aggiornato or date.today().isoformat(),
        },
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"scritto {OUT} ({OUT.stat().st_size} byte) - {payload['meta']}")


if __name__ == "__main__":
    main()
