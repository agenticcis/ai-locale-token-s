#!/usr/bin/env python3
"""Aggiornamento AUTOMATICO della lista modelli, da Hugging Face (API pubblica, gratis).

Perche' HF e non Ollama: l'API di Ollama (registry.ollama.ai/v2/...) risponde 404, non
espone un catalogo. HF invece da', per ogni modello: id, tag (famiglia/base_model),
download, likes, lastModified. Da quelli ricaviamo nome, famiglia e numero di parametri.

Uso:  python3 aggiorna_modelli.py [--limit 300] [--min-download 5000]
Scrive models_auto.json (usato da genera_dati.py).
"""
import argparse
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone, date
from pathlib import Path

OUT = Path(__file__).parent / "models_auto.json"
API = "https://huggingface.co/api/models"

# Famiglie di LLM di testo. Scarta embedding, reranker, vision, ocr, audio...
FAMIGLIE_OK = ("qwen", "llama", "gemma", "mistral", "mixtral", "phi", "deepseek",
               "smollm", "tinyllama", "yi", "granite", "falcon", "starcoder", "command",
               "olmo", "hermes", "dolphin", "openchat", "vicuna", "zephyr", "internlm",
               "glm", "minicpm", "codegemma", "codestral", "gpt-oss", "granite")
ESCLUSI = ("embed", "rerank", "vision", "vl-", "-vl", "ocr", "whisper", "audio", "clip",
           "image", "diffusion", "detect", "segmentation", "sentence", "blip")


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "openhands-agent",
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def params_da_nome(nome):
    """Ritorna (parametri_totali_miliardi, attivi_miliardi_o_None)."""
    base = nome.split("/")[-1]
    m = re.search(r"(\d+)x(\d+(?:\.\d+)?)[bB]", base)          # 8x7B
    if m:
        return float(m.group(1)) * float(m.group(2)), float(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?)[bB]-[aA](\d+(?:\.\d+)?)[bB]", base)  # 30B-A3B
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?)[bB](?![a-zA-Z0-9])", base)  # 7B, 1.5B
    if m:
        return float(m.group(1)), None
    return None, None


def famiglia_da_tags(tags, nome):
    for t in tags or []:
        if isinstance(t, str) and t.startswith("base_model:"):
            v = t.split(":", 1)[1].split("/", 1)[-1].lower()
            for f in FAMIGLIE_OK:
                if f in v:
                    return f.capitalize()
    basso = nome.lower()
    for f in FAMIGLIE_OK:
        if f in basso:
            return f.capitalize()
    return (nome.split("/")[-1].split("-")[0][:16] or "Altro").capitalize()


RUMORE = {"claude", "opus", "fable", "fable5", "thinking", "flash", "turbo", "latest",
          "official", "uncensored", "abliterated", "preview", "distill", "instruct",
          "gguf", "chat", "it"}
CANON = {"qwen": "Qwen", "llama": "Llama", "gemma": "Gemma", "mistral": "Mistral",
         "mixtral": "Mixtral", "phi": "Phi", "deepseek": "DeepSeek", "smollm": "SmolLM",
         "tinyllama": "TinyLlama", "yi": "Yi", "granite": "Granite", "glm": "GLM",
         "gpt": "GPT", "oss": "OSS", "minicpm": "MiniCPM", "coder": "Coder", "code": "Code",
         "edge": "Edge", "medium": "Medium", "medium": "Medium", "small": "Small",
         "nousresearch": "NousResearch", "huggingfacetb": "HuggingFaceTB",
         "parable": "Parable", "ternary": "Ternary", "bonsai": "Bonsai", "pocket": "Pocket",
         "jirackultra": "JiRackUltra", "lfm": "LFM", "spark": "Spark", "glm": "GLM"}


def _canonizza(parola):
    """'gemma' -> 'Gemma', '1b' -> '1B'. Scarta il rumore: 'v0.1', '2501'.
    I numeri di versione piccoli ('3' in 'gemma 3 1b') restano."""
    if re.fullmatch(r"v\d+(\.\d+)?", parola, flags=re.I) or re.fullmatch(r"\d{3,}", parola):
        return ""
    if re.fullmatch(r"\d+(\.\d+)?[bB]", parola):
        return parola[:-1] + "B"
    c = CANON.get(parola.lower())
    if c:
        return c
    if parola[:1].islower():
        return parola[:1].upper() + parola[1:]
    return parola


def nome_pulito(nome):
    """Toglie suffissi di quantizzazione e parole di rumore, ma CONSERVA i numeri di
    versione (3.2, 2.5...): 'Llama-3.2-1B-Instruct-GGUF' -> 'Llama 3.2 1B'."""
    base = nome.split("/")[-1]
    base = re.sub(r"[-_.]?(gguf|IQ\d[\w]*|Q\d[\w]*|UD|MXFP4|BF16|FP16|F16|\d+bit)$",
                  "", base, flags=re.I)
    parole = re.split(r"[-_\s]+", base)
    tenute = [w for w in parole if w and w.lower() not in RUMORE and not re.fullmatch(r"[bB]", w)]
    can = [c for c in (_canonizza(w) for w in tenute[:4]) if c]
    return re.sub(r"\s+", " ", " ".join(can)).strip()[:44]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--min-download", type=int, default=5000)
    args = ap.parse_args()

    url = (f"{API}?filter=gguf&pipeline_tag=text-generation&sort=downloads&direction=-1"
           f"&limit={args.limit}&full=false")
    try:
        grezzo = _get(url)
    except urllib.error.HTTPError as exc:
        print(f"ERRORE HF ({exc.code}): mantengo il file precedente.")
        raise SystemExit(1)

    visti = {}
    for m in grezzo:
        mid = m.get("id", "")
        nome = m.get("modelId") or mid
        basso = (mid + " " + " ".join(m.get("tags") or [])).lower()
        if any(x in basso for x in ESCLUSI):
            continue
        if (m.get("downloads") or 0) < args.min_download:
            continue
        tot, att = params_da_nome(nome)
        if not tot or not (0.1 <= tot <= 200):
            continue
        fam = famiglia_da_tags(m.get("tags"), nome)
        if fam.lower() not in FAMIGLIE_OK:   # niente famiglie sconosciute: sono rumore
            continue
        nome_buono = nome_pulito(nome)
        if len(nome_buono.split()) < 2:      # un nome senza numero di versione/parametri
            continue
        chiave = (fam.lower(), round(tot, 1))
        nuovo = {
            "id": re.sub(r"[^a-z0-9]+", "_", nome.lower()).strip("_")[:60],
            "name": nome_buono[:44],
            "params": round(tot, 2),
            "family": fam,
            "active": round(att, 2) if att else None,
            "aggiornato": (m.get("lastModified") or "")[:10],
            "downloads": m.get("downloads") or 0,
            "fonte": mid,
        }
        if chiave not in visti or nuovo["downloads"] > visti[chiave]["downloads"]:
            visti[chiave] = nuovo

    modelli = list(visti.values())

    modelli.sort(key=lambda x: x["params"])
    OUT.write_text(json.dumps({
        "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fonte": "huggingface.co/api/models",
        "nota": "Generato automaticamente. Non modificare a mano.",
        "modelli": modelli,
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"scritto {OUT} - {len(modelli)} modelli (aggiornati al {date.today()})")
    print("  esempio:", ", ".join(f"{m['name']} ({m['params']}B)" for m in modelli[:6]))


if __name__ == "__main__":
    main()
