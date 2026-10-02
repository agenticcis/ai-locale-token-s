"""Base dati hardware + modelli per il calcolatore "AI locale".

I numeri di banda (GB/s) sono valori PRATICI (non teorici di targa): la velocita' di
generazione di un LLM locale e' limitata dalla banda di memoria, e nel reale se ne
sfrutta ~60-75%. Aggiornati a mano; il file dati.json puo' sovrascriverli (vedi
genera_dati.py).

Fonti dei dati di banda: specifiche pubbliche dei produttori (Memoria: DDR4/DDR5/LPDDR5,
VRAM GPU) + benchmark comunitari.
"""

# --- CPU: banda = velocita' della RAM di sistema (il collo di bottiglia in CPU-only) ---
CPUS = [
    {"id": "r3_3200u",  "name": "AMD Ryzen 3 3200U",      "brand": "AMD",   "tput": 30, "igpu": "vega3"},
    {"id": "r5_3500u",  "name": "AMD Ryzen 5 3500U",      "brand": "AMD",   "tput": 35, "igpu": "vega8"},
    {"id": "r5_3600",   "name": "AMD Ryzen 5 3600",       "brand": "AMD",   "tput": 45, "igpu": None},
    {"id": "r5_5600u",  "name": "AMD Ryzen 5 5600U",      "brand": "AMD",   "tput": 45, "igpu": "vega7"},
    {"id": "r7_5800x",  "name": "AMD Ryzen 7 5800X",      "brand": "AMD",   "tput": 48, "igpu": None},
    {"id": "r7_6800h",  "name": "AMD Ryzen 7 6800H",      "brand": "AMD",   "tput": 62, "igpu": "radeon680m"},
    {"id": "r7_7840u",  "name": "AMD Ryzen 7 7840U",      "brand": "AMD",   "tput": 75, "igpu": "radeon780m"},
    {"id": "r7_7800x3d","name": "AMD Ryzen 7 7800X3D",    "brand": "AMD",   "tput": 70, "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    {"id": "r9_7950x",  "name": "AMD Ryzen 9 7950X",      "brand": "AMD",   "tput": 85, "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    # --- generazioni 2025-2026 (local AI) ---
    {"id": "r7_9700x",  "name": "AMD Ryzen 7 9700X",      "brand": "AMD",   "tput": 89, "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    {"id": "r9_9950x",  "name": "AMD Ryzen 9 9950X",      "brand": "AMD",   "tput": 89, "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    {"id": "ai9_hx370", "name": "AMD Ryzen AI 9 HX 370",  "brand": "AMD",   "tput": 120, "igpu": "radeon890m"},
    {"id": "ai9_hx470", "name": "AMD Ryzen AI 9 HX 470",  "brand": "AMD",   "tput": 120, "igpu": "radeon890m"},
    {"id": "ai_max_395","name": "AMD Ryzen AI Max+ 395 (Strix Halo)", "brand": "AMD", "tput": 256, "mem_fissa": True, "igpu": "radeon8060s"},
    {"id": "cu7_155h",  "name": "Intel Core Ultra 7 155H","brand": "Intel", "tput": 120, "igpu": "arc8core"},
    {"id": "cu7_258v",  "name": "Intel Core Ultra 7 258V","brand": "Intel", "tput": 136, "mem_fissa": True, "igpu": "arc140v"},
    {"id": "cu9_285k",  "name": "Intel Core Ultra 9 285K","brand": "Intel", "tput": 89, "igpu": "arc4core"},
    {"id": "sd_x_elite", "name": "Qualcomm Snapdragon X Elite", "brand": "Qualcomm", "tput": 135, "mem_fissa": True, "igpu": "adreno"},
    {"id": "i5_8250u",  "name": "Intel Core i5-8250U",    "brand": "Intel", "tput": 34, "igpu": "uhd620"},
    {"id": "i5_1135g7", "name": "Intel Core i5-1135G7",   "brand": "Intel", "tput": 42, "igpu": "irisxe80"},
    {"id": "i7_1165g7", "name": "Intel Core i7-1165G7",   "brand": "Intel", "tput": 45, "igpu": "irisxe96"},
    {"id": "i5_12600k", "name": "Intel Core i5-12600K",   "brand": "Intel", "tput": 52, "igpu": None},
    {"id": "i7_12700h", "name": "Intel Core i7-12700H",   "brand": "Intel", "tput": 65, "igpu": "irisxe96"},
    {"id": "i7_13700k", "name": "Intel Core i7-13700K",   "brand": "Intel", "tput": 78, "igpu": {"vram": 2, "tput": 14, "name": "UHD 770 (iGPU)"}},
    {"id": "i9_14900k", "name": "Intel Core i9-14900K",   "brand": "Intel", "tput": 88, "igpu": {"vram": 2, "tput": 14, "name": "UHD 770 (iGPU)"}},
    {"id": "m1",        "name": "Apple M1",               "brand": "Apple", "tput": 68,   "mem_fissa": True, "igpu": "unified"},
    {"id": "m2",        "name": "Apple M2",               "brand": "Apple", "tput": 100,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m2pro",     "name": "Apple M2 Pro",           "brand": "Apple", "tput": 200,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m3",        "name": "Apple M3",               "brand": "Apple", "tput": 100,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m3pro",     "name": "Apple M3 Pro",           "brand": "Apple", "tput": 150,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m3max",     "name": "Apple M3 Max",           "brand": "Apple", "tput": 300,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m4",        "name": "Apple M4",               "brand": "Apple", "tput": 120,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m4pro",     "name": "Apple M4 Pro",           "brand": "Apple", "tput": 273,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m4max",     "name": "Apple M4 Max",           "brand": "Apple", "tput": 410,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m1pro",     "name": "Apple M1 Pro",           "brand": "Apple", "tput": 200,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m1max",     "name": "Apple M1 Max",           "brand": "Apple", "tput": 400,  "mem_fissa": True, "igpu": "unified"},
    {"id": "m2max",     "name": "Apple M2 Max",           "brand": "Apple", "tput": 400,  "mem_fissa": True, "igpu": "unified"},
    # --- desktop / fascia media aggiunti su richiesta (02/10) ---
    {"id": "r5_5700x3d","name": "AMD Ryzen 5 5700X3D",    "brand": "AMD",   "tput": 48,  "igpu": None},
    {"id": "r5_7600",   "name": "AMD Ryzen 5 7600",       "brand": "AMD",   "tput": 85,  "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    {"id": "r7_9800x3d","name": "AMD Ryzen 7 9800X3D",    "brand": "AMD",   "tput": 90,  "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    {"id": "r7_8700g",  "name": "AMD Ryzen 7 8700G",      "brand": "AMD",   "tput": 90,  "igpu": "radeon780m"},
    {"id": "r9_7945hx", "name": "AMD Ryzen 9 7945HX",     "brand": "AMD",   "tput": 80,  "igpu": {"vram": 2, "tput": 12, "name": "Radeon Graphics (iGPU)"}},
    {"id": "cu5_125h",  "name": "Intel Core Ultra 5 125H", "brand": "Intel", "tput": 120, "igpu": "arc7core"},
    {"id": "cu7_265k",  "name": "Intel Core Ultra 7 265K", "brand": "Intel", "tput": 90,  "igpu": "arc4core"},
    {"id": "i7_14700k", "name": "Intel Core i7-14700K",   "brand": "Intel", "tput": 88,  "igpu": {"vram": 2, "tput": 14, "name": "UHD 770 (iGPU)"}},
    {"id": "i5_1340p",  "name": "Intel Core i5-1340P",    "brand": "Intel", "tput": 80,  "igpu": "irisxe80"},
    {"id": "n100",      "name": "Intel N100 (mini PC)",   "brand": "Intel", "tput": 25,  "igpu": "uhd24"},
    {"id": "sd_x_plus", "name": "Qualcomm Snapdragon X Plus", "brand": "Qualcomm", "tput": 135, "mem_fissa": True, "igpu": "adreno"},
]

# --- GPU INTEGRATE: il buco che nessun calcolatore copre. Usano le stesse RAM ---
IGPUS = {
    "vega3":     {"name": "Radeon Vega 3 (integrata)",         "vram": 2, "tput": 30},
    "vega8":     {"name": "Radeon Vega 8 (integrata)",         "vram": 2, "tput": 35},
    "vega7":     {"name": "Radeon Vega 7 (integrata)",         "vram": 2, "tput": 42},
    "uhd620":    {"name": "Intel UHD 620 (integrata)",         "vram": 2, "tput": 34},
    "irisxe80":  {"name": "Intel Iris Xe 80EU (integrata)",    "vram": 4, "tput": 45},
    "irisxe96":  {"name": "Intel Iris Xe 96EU (integrata)",    "vram": 4, "tput": 50},
    "radeon680m":{"name": "Radeon 680M (integrata)",           "vram": 4, "tput": 62},
    "radeon780m":{"name": "Radeon 780M (integrata)",           "vram": 8, "tput": 75},
    # --- integrate 2025-2026 ---
    "radeon890m":{"name": "Radeon 890M (integrata)",           "vram": 16, "tput": 120},
    "radeon8060s":{"name": "Radeon 8060S (integrata, Strix Halo)","vram": 64, "tput": 256},
    "arc8core":  {"name": "Intel Arc 8-core (integrata)",      "vram": 16, "tput": 120},
    "arc140v":   {"name": "Intel Arc 140V (integrata)",        "vram": 16, "tput": 136},
    "arc4core":  {"name": "Intel Arc 4-core (integrata)",      "vram": 8,  "tput": 89},
    "adreno":    {"name": "Qualcomm Adreno (integrata)",       "vram": 16, "tput": 135},
    "uhd24":     {"name": "Intel UHD 24EU (integrata)",        "vram": 2, "tput": 30},
    "arc7core":  {"name": "Intel Arc 7-core (integrata)",       "vram": 16, "tput": 120},
    "unified":   {"name": "Memoria unificata Apple",           "vram": 0, "tput": 0},
}

# --- GPU DISCRETE ---
GPUS = [
    {"id": "gtx1080ti","name": "NVIDIA GTX 1080 Ti", "brand": "NVIDIA", "vram": 11, "tput": 484},
    {"id": "gtx1660s", "name": "NVIDIA GTX 1660 Super","brand": "NVIDIA", "vram": 6,  "tput": 336},
    {"id": "p40",      "name": "NVIDIA Tesla P40",   "brand": "NVIDIA", "vram": 24, "tput": 347},
    {"id": "rtx3060",  "name": "NVIDIA RTX 3060",    "brand": "NVIDIA", "vram": 12, "tput": 360},
    {"id": "rtx3070",  "name": "NVIDIA RTX 3070",    "brand": "NVIDIA", "vram": 8,  "tput": 448},
    {"id": "rtx3080",  "name": "NVIDIA RTX 3080",    "brand": "NVIDIA", "vram": 10, "tput": 760},
    {"id": "rtx3090",  "name": "NVIDIA RTX 3090",    "brand": "NVIDIA", "vram": 24, "tput": 936},
    {"id": "rtx4060",  "name": "NVIDIA RTX 4060",    "brand": "NVIDIA", "vram": 8,  "tput": 272},
    {"id": "rtx4060ti","name": "NVIDIA RTX 4060 Ti 16GB","brand": "NVIDIA","vram": 16,"tput": 288},
    {"id": "rtx4070",  "name": "NVIDIA RTX 4070",    "brand": "NVIDIA", "vram": 12, "tput": 504},
    {"id": "rtx4070ts","name": "NVIDIA RTX 4070 Ti Super","brand": "NVIDIA","vram":16,"tput": 672},
    {"id": "rtx4080",  "name": "NVIDIA RTX 4080",    "brand": "NVIDIA", "vram": 16, "tput": 717},
    {"id": "rtx4090",  "name": "NVIDIA RTX 4090",    "brand": "NVIDIA", "vram": 24, "tput": 1008},
    {"id": "rtx5070",  "name": "NVIDIA RTX 5070",    "brand": "NVIDIA", "vram": 12, "tput": 672},
    {"id": "rtx5070ti","name": "NVIDIA RTX 5070 Ti", "brand": "NVIDIA", "vram": 16, "tput": 896},
    {"id": "rtx5080",  "name": "NVIDIA RTX 5080",    "brand": "NVIDIA", "vram": 16, "tput": 960},
    {"id": "rtx5090",  "name": "NVIDIA RTX 5090",    "brand": "NVIDIA", "vram": 32, "tput": 1792},
    {"id": "a4000",    "name": "NVIDIA RTX A4000",   "brand": "NVIDIA", "vram": 16, "tput": 448},
    {"id": "rx6600",   "name": "AMD RX 6600",        "brand": "AMD",    "vram": 8,  "tput": 224},
    {"id": "rx6700xt", "name": "AMD RX 6700 XT",     "brand": "AMD",    "vram": 12, "tput": 384},
    {"id": "rx6800xt", "name": "AMD RX 6800 XT",     "brand": "AMD",    "vram": 16, "tput": 512},
    {"id": "rx7600",   "name": "AMD RX 7600",        "brand": "AMD",    "vram": 8,  "tput": 288},
    {"id": "rx7800xt", "name": "AMD RX 7800 XT",     "brand": "AMD",    "vram": 16, "tput": 624},
    {"id": "rx7900xt", "name": "AMD RX 7900 XT",     "brand": "AMD",    "vram": 20, "tput": 800},
    {"id": "rx7900xtx","name": "AMD RX 7900 XTX",    "brand": "AMD",    "vram": 24, "tput": 960},
    {"id": "arc_a770", "name": "Intel Arc A770",     "brand": "Intel",  "vram": 16, "tput": 560},
    {"id": "arc_b580", "name": "Intel Arc B580",     "brand": "Intel",  "vram": 12, "tput": 456},
    # --- generazioni 2025-2026 ---
    {"id": "rtx5060ti","name": "NVIDIA RTX 5060 Ti 16GB","brand": "NVIDIA", "vram": 16, "tput": 448},
    {"id": "rx9060xt", "name": "AMD RX 9060 XT 16GB", "brand": "AMD",   "vram": 16, "tput": 322},
    {"id": "rx9070",   "name": "AMD RX 9070 16GB",    "brand": "AMD",   "vram": 16, "tput": 640},
    {"id": "rx9070xt", "name": "AMD RX 9070 XT 16GB", "brand": "AMD",   "vram": 16, "tput": 640},
    {"id": "arc_b580_24","name":"Intel Arc B580 24GB", "brand": "Intel", "vram": 24, "tput": 456},
]

# --- Tipi di memoria di sistema (per il moltiplicatore HD/tipo RAM) ---
# "ram_base": banda REALISTICA di quel tipo di memoria (dual-channel, valori pratici).
# Non e' un'etichetta: e' un TETTO. Una CPU veloce non supera la banda della RAM che monta.
RAM_TYPES = [
    {"id": "ddr3",  "name": "DDR3",   "speed": "~1600 MT/s",                "ram_base": 25},
    {"id": "ddr4",  "name": "DDR4",   "speed": "2400-3200 MT/s",            "ram_base": 45},
    {"id": "ddr5",  "name": "DDR5",   "speed": "4800-6000 MT/s",            "ram_base": 90},
    {"id": "lpddr5","name": "LPDDR5", "speed": "6400-8500 MT/s (saldata)",  "ram_base": 130},
]

# --- QUANTITA' di RAM (GB). Conta per: memoria condivisa della GPU integrata, VRAM
#     "unificata" Apple e se il modello ci sta in RAM (CPU-only o straripamento). ---
RAM_SIZES = [8, 12, 16, 24, 32, 48, 64, 96, 128]

# --- HD / SSD: NON conta per la velocita' token (solo modello e RAM contano).
#     Conta per i TEMPI DI CARICO (quanto aspetti all'avvio/in cambio modello). ---
HD_TYPES = [
    {"id": "hdd",    "name": "HDD meccanico (7200rpm)", "read_mbps": 120},
    {"id": "sata",   "name": "SSD SATA",                "read_mbps": 550},
    {"id": "nvme3",  "name": "SSD NVMe PCIe 3.0 x4",    "read_mbps": 3500},
    {"id": "nvme4",  "name": "SSD NVMe PCIe 4.0 x4",    "read_mbps": 7000},
    {"id": "nvme5",  "name": "SSD NVMe PCIe 5.0 x4",    "read_mbps": 14000},
]

# --- Quantizzazioni: bit per peso. Meno bit = modello piu' piccolo = piu' veloce. ---
QUANTS = [
    {"id": "q3km",  "name": "Q3_K_M (~3,9 bit)", "bpw": 3.9},
    {"id": "q4km",  "name": "Q4_K_M (~4,9 bit)", "bpw": 4.85},
    {"id": "q5km",  "name": "Q5_K_M (~5,7 bit)", "bpw": 5.7},
    {"id": "q6k",   "name": "Q6_K (~6,6 bit)",   "bpw": 6.6},
    {"id": "q8",    "name": "Q8_0 (~8,5 bit)",   "bpw": 8.5},
    {"id": "fp16",  "name": "FP16 (16 bit)",     "bpw": 16.0},
]

# --- Modelli (parametri reali, miliardi). I nomi ricalcano quelli su ollama.com. ---
MODELS = [
    {"id": "smollm2_135m","name": "SmolLM2 135M",           "params": 0.135, "family": "SmolLM"},
    {"id": "smollm2_360m","name": "SmolLM2 360M",           "params": 0.36,  "family": "SmolLM"},
    {"id": "qwen25_05b",  "name": "Qwen2.5 0.5B",           "params": 0.5,   "family": "Qwen"},
    {"id": "qwen25_15b",  "name": "Qwen2.5 1.5B",           "params": 1.5,   "family": "Qwen"},
    {"id": "qwen3_06b",   "name": "Qwen3 0.6B",             "params": 0.6,   "family": "Qwen"},
    {"id": "qwen3_17b",   "name": "Qwen3 1.7B",             "params": 1.7,   "family": "Qwen"},
    {"id": "qwen3_4b",    "name": "Qwen3 4B",               "params": 4.0,   "family": "Qwen"},
    {"id": "qwen3_8b",    "name": "Qwen3 8B",               "params": 8.0,   "family": "Qwen"},
    {"id": "qwen25_3b",   "name": "Qwen2.5 3B",             "params": 3.1,   "family": "Qwen"},
    {"id": "qwen25_7b",   "name": "Qwen2.5 7B",             "params": 7.6,   "family": "Qwen"},
    {"id": "qwen25_14b",  "name": "Qwen2.5 14B",            "params": 14.7,  "family": "Qwen"},
    {"id": "qwen25_32b",  "name": "Qwen2.5 32B",            "params": 32.5,  "family": "Qwen"},
    {"id": "qwen25_coder7b","name":"Qwen2.5-Coder 7B",      "params": 7.6,   "family": "Qwen"},
    {"id": "llama32_1b",  "name": "Llama 3.2 1B",           "params": 1.24,  "family": "Llama"},
    {"id": "llama32_3b",  "name": "Llama 3.2 3B",           "params": 3.21,  "family": "Llama"},
    {"id": "llama31_8b",  "name": "Llama 3.1 8B",           "params": 8.03,  "family": "Llama"},
    {"id": "llama33_70b", "name": "Llama 3.3 70B",          "params": 70.6,  "family": "Llama"},
    {"id": "gemma2_2b",   "name": "Gemma 2 2B",             "params": 2.61,  "family": "Gemma"},
    {"id": "gemma2_9b",   "name": "Gemma 2 9B",             "params": 9.24,  "family": "Gemma"},
    {"id": "gemma2_27b",  "name": "Gemma 2 27B",            "params": 27.2,  "family": "Gemma"},
    {"id": "phi3_mini",   "name": "Phi-3 Mini 3.8B",        "params": 3.82,  "family": "Phi"},
    {"id": "phi3_med",    "name": "Phi-3 Medium 14B",       "params": 14.0,  "family": "Phi"},
    {"id": "phi4_14b",    "name": "Phi-4 14B",              "params": 14.7,  "family": "Phi"},
    {"id": "mistral_7b",  "name": "Mistral 7B",             "params": 7.24,  "family": "Mistral"},
    {"id": "mixtral_8x7b","name": "Mixtral 8x7B (MoE)",     "params": 46.7,  "family": "Mistral", "active": 12.9},
    {"id": "mixtral_8x22b","name":"Mixtral 8x22B (MoE)",    "params": 141.0, "family": "Mistral", "active": 39.0},
    {"id": "deepseek_r1_15b","name":"DeepSeek-R1 1.5B",     "params": 1.78,  "family": "DeepSeek"},
    {"id": "deepseek_r1_7b","name": "DeepSeek-R1 7B",       "params": 7.62,  "family": "DeepSeek"},
    {"id": "deepseek_r1_8b","name": "DeepSeek-R1 8B",       "params": 8.03,  "family": "DeepSeek"},
    {"id": "deepseek_r1_14b","name":"DeepSeek-R1 14B",      "params": 14.8,  "family": "DeepSeek"},
    {"id": "deepseek_r1_32b","name":"DeepSeek-R1 32B",      "params": 32.8,  "family": "DeepSeek"},
    {"id": "deepseek_coder16b","name":"DeepSeek-Coder-V2 Lite 16B (MoE)","params": 15.7, "family": "DeepSeek", "active": 2.4},
    {"id": "tinyllama",   "name": "TinyLlama 1.1B",         "params": 1.1,   "family": "Llama"},
    {"id": "yi_34b",      "name": "Yi 34B",                 "params": 34.4,  "family": "Yi"},
    {"id": "codellama_7b","name": "Code Llama 7B",          "params": 6.74,  "family": "Llama"},
    {"id": "codellama_13b","name":"Code Llama 13B",         "params": 13.0,  "family": "Llama"},
    {"id": "vicuna_13b",  "name": "Vicuna 13B",             "params": 13.0,  "family": "Llama"},
    {"id": "openchat_7b", "name": "OpenChat 7B",            "params": 7.24,  "family": "Mistral"},
]

# --- Fattori di correzione (dal modello fisico) ---
# generation e' memory-bandwidth-bound; l'efficienza reale (~60-75%) include overhead FFN/KV.
EFFICIENCY = 0.65
# Overhead fisso per modello (buffer, KV cache a contesto breve): GB
OVERHEAD_GB = 0.5

# --- Soglie "usabile?" per caso d'uso (token/s minimi) ---
USE_CASES = [
    {"id": "chat",   "name": "Chat / assistente", "min_tps": 5},
    {"id": "codice", "name": "Scrittura codice",  "min_tps": 10},
    {"id": "agente", "name": "Agente / tool-use", "min_tps": 15},
    {"id": "realtime","name": "Voce in tempo reale","min_tps": 25},
]
