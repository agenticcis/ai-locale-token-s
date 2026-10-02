"""Motore di stima: modello + hardware -> token/s, VRAM occupata, usabilita'.

Il modello fisico (standard per LLM locali a singolo utente):
    token/s ~= banda_di_memoria_usata / dimensione_del_modello * efficienza
Perche': per generare OGNI token bisogna leggere TUTTI i pesi del modello dalla memoria.
Non e' un limite di calcolo (FLOPs), e' un limite di BANDA. Da qui la regola pratica:
piu' banda hai, piu' token/s; modello piu' piccolo (quantizzato), piu' token/s.

Un modello puo' stare in VRAM (veloce) o straripare in RAM (lento, 5-20x). Lo stimatore
usa la banda dello strato dove STA il modello: se non entra in VRAM, il collo di bottiglia
diventa la RAM.
"""

from data import (CPUS, GPUS, IGPUS, QUANTS, MODELS, RAM_TYPES, RAM_SIZES, HD_TYPES,
                  EFFICIENCY, OVERHEAD_GB, USE_CASES)


def _trova(seq, id_):
    for x in seq:
        if x["id"] == id_:
            return x
    raise KeyError(id_)


def _risolvi_igpu(igpu):
    """L'iGPU di una CPU puo' essere: None / chiave di IGPUS / dict esplicito / 'unified'."""
    if igpu is None:
        return None
    if isinstance(igpu, dict):
        return dict(igpu)
    if igpu == "unified":
        return {"name": "Memoria unificata (Apple)", "vram": 0, "tput": 0, "unified": True}
    base = dict(IGPUS[igpu])
    base["key"] = igpu
    return base


def opzioni_cpu():
    return [{"id": c["id"], "name": c["name"], "brand": c["brand"]} for c in CPUS]


def opzioni_gpu(cpu_id):
    """GPU scegliibili: integrate (SOLO se la CPU ne ha una) + discrete."""
    out = []
    cpu = _trova(CPUS, cpu_id)
    ig = _risolvi_igpu(cpu.get("igpu"))
    if ig:
        out.append({"id": "igpu", "name": ig["name"], "tput": ig.get("tput", 0),
                    "vram": ig.get("vram", 0), "tipo": "integrata"})
    for g in GPUS:
        out.append({"id": g["id"], "name": g["name"], "tput": g["tput"],
                    "vram": g["vram"], "tipo": "discreta"})
    return out


def opzioni_ram():
    return [{"id": r["id"], "name": f"{r['name']} ({r['speed']})"} for r in RAM_TYPES]


def opzioni_hd():
    return [{"id": h["id"], "name": h["name"]} for h in HD_TYPES]


def opzioni_quant():
    return [{"id": q["id"], "name": q["name"]} for q in QUANTS]


def opzioni_modelli():
    return [{"id": m["id"], "name": m["name"], "params": m["params"],
             "family": m["family"]} for m in sorted(MODELS, key=lambda m: m["params"])]


def stima(cpu_id, gpu_id, ram_id, hd_id, model_id, quant_id, ram_gb=16):
    cpu = _trova(CPUS, cpu_id)
    ram = _trova(RAM_TYPES, ram_id)
    hd = _trova(HD_TYPES, hd_id)
    model = _trova(MODELS, model_id)
    quant = _trova(QUANTS, quant_id)

    # 1) dimensione del modello in memoria (GB): parametri * bit-per-peso / 8
    # Per i MoE solo una parte dei parametri e' attiva, ma TUTTI i pesi stanno in memoria:
    # la banda va calcolata sui pesi TOTALI (gia' che ci siamo), la dimensione pure.
    peso_gb = model["params"] * quant["bpw"] / 8.0
    tot_gb = peso_gb + OVERHEAD_GB

    # 2) dove sta il modello: VRAM o RAM?
    # Il tipo di RAM sceglie la BANDA (velocita'); la quantita' sceglie solo la CAPACITA'.
    # Mai far dipendere la banda dalla capacita': sarebbe un'illusione (64 GB non velocizzano
    # una macchina lenta). Il "tput" della CPU e' gia' la banda reale della sua RAM tipica;
    # il tipo di RAM scelto la scala se molto piu' lenta/veloce.
    fattore_ram = {"ddr3": 0.55, "ddr4": 1.0, "ddr5": 1.25, "lpddr5": 1.2}.get(ram["id"], 1.0)
    if cpu.get("igpu") == "unified":
        # Apple: il "tput" E' gia' la banda reale della memoria unificata (LPDDR5 saldata).
        # Moltiplicarla di nuovo doppierebbe un guadagno che non esiste.
        fattore_ram = 1.0
    banda_sistema = cpu["tput"] * fattore_ram

    if gpu_id == "igpu":
        igpu = _risolvi_igpu(cpu.get("igpu"))
        if igpu:
            unified = igpu.get("unified", False)
            gpu_name = igpu["name"]
            # iGPU (Apple o Intel/AMD/Qualcomm) = memoria condivisa, ~75% della RAM installata.
            banda_vram = banda_sistema * (1.0 if unified else 0.85)
            vram_disp = ram_gb * 0.75
        else:
            # CPU senza GPU integrata: inferenza sulla CPU, banda = RAM di sistema.
            gpu_name = f"{cpu['name']} (nessuna GPU: inferenza su CPU)"
            banda_vram = banda_sistema
            vram_disp = ram_gb * 0.75
    else:
        # GPU discreta: VRAM dedicata, indipendente dalla quantita' di RAM di sistema.
        g = _trova(GPUS, gpu_id)
        gpu_name = g["name"]
        vram_disp = g["vram"]
        banda_vram = g["tput"]

    banda_ram = banda_sistema

    # 3) entra in VRAM?
    fits = tot_gb <= vram_disp
    # 3b) entra in RAM? Senza questo, una macchina con poca RAM "farebbe girare" modelli
    #     che in pratica non ci stanno.
    fits_ram = tot_gb <= ram_gb * 0.9

    # 4) banda usata
    if fits:
        banda = banda_vram
    else:
        # straripa: il collo di bottiglia diventa la RAM (i layer in GPU non salvano la media)
        banda = banda_ram

    tps = banda / tot_gb * EFFICIENCY
    if not fits_ram:
        tps = 0.0   # non ci sta: niente token/s onesti da mostrare

    # 5) tempi di carico (SSD/HD) e di prefill (prompt)
    load_s = (tot_gb * 1024) / hd["read_mbps"]
    prefill_s = 0.0  # non stimato nel v1 (dipende dal prompt)

    # 6) usabilita'
    usi = []
    for u in USE_CASES:
        usi.append({"name": u["name"], "ok": tps >= u["min_tps"], "min": u["min_tps"]})
    if not fits_ram:
        giudizio = f"Non ci sta: {ram_gb} GB di RAM"
    elif tps < 1:
        giudizio = "Inutilizzabile"
    elif tps < 5:
        giudizio = "Molto lento"
    elif tps < 10:
        giudizio = "Usabile in chat"
    elif tps < 20:
        giudizio = "Scorrevole"
    else:
        giudizio = "Molto veloce"

    return {
        "cpu": cpu["name"], "gpu": gpu_name, "ram": ram["name"], "ram_gb": ram_gb,
        "hd": hd["name"],
        "model": model["name"], "quant": quant["name"],
        "peso_gb": round(peso_gb, 2), "tot_gb": round(tot_gb, 2),
        "vram_disp": round(vram_disp, 1), "fits": fits, "fits_ram": fits_ram,
        "banda": round(banda, 0), "tps": round(tps, 1),
        "tps_basso": round(tps * 0.6, 1), "tps_alto": round(tps * 1.3, 1),
        "secondi_50tok": round(50 / tps, 1) if tps > 0 else None,
        "load_s": round(load_s, 1),
        "giudizio": giudizio, "usi": usi,
        "dove": ("RAM condivisa" if gpu_id == "igpu"
                 else ("VRAM" if fits else "RAM (straripa: lento)")),
    }
