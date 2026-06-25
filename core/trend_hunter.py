import os

TRUSTED_CHANNELS = [
    "https://www.youtube.com/@lexfridman",
    "https://www.youtube.com/@hubermanlab",
    "https://www.youtube.com/@mkbhd",
    "https://www.youtube.com/@aiexplained-official",
    "https://www.youtube.com/@veritasium",
    "https://www.youtube.com/@Fireship",
    "https://www.youtube.com/@TED",
    "https://www.youtube.com/@kurzgesagt",
    "https://www.youtube.com/@pewdiepie",
    "https://www.youtube.com/@MrBeast",
]

def hunt_high_cpm_channels(api_key):
    print("[*] Memuat daftar channel terpercaya...")
    os.makedirs("config", exist_ok=True)
    with open("config/channels.txt", "w") as f:
        f.write("\n".join(TRUSTED_CHANNELS))
    print(f"[+] {len(TRUSTED_CHANNELS)} channel siap diproses.")
    return TRUSTED_CHANNELS
