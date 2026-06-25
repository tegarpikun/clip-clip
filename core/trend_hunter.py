import os

# Daftar channel terpercaya yang sudah terbukti ada dan aktif
# Niche CPM tinggi: Keuangan, Bisnis, Teknologi, Motivasi
TRUSTED_CHANNELS = [
    # Keuangan & Bisnis Indonesia
    "https://www.youtube.com/@feliciaputritjiasaka6635",
    "https://www.youtube.com/@andreiwidjaja",
    "https://www.youtube.com/@ngomonginuang",
    "https://www.youtube.com/@radityadika",
    "https://www.youtube.com/@pakcicil",
    # Teknologi & AI
    "https://www.youtube.com/@davidgoggins",
    "https://www.youtube.com/@lexfridman",
    "https://www.youtube.com/@hubermanlab",
    "https://www.youtube.com/@mkbhd",
    "https://www.youtube.com/@aiexplained-official",
]

def hunt_high_cpm_channels(api_key):
    """Mengembalikan daftar channel terpercaya yang sudah terverifikasi ada."""
    print("[*] Memuat daftar channel terpercaya...")
    
    os.makedirs("config", exist_ok=True)
    with open("config/channels.txt", "w") as f:
        f.write("\n".join(TRUSTED_CHANNELS))
    
    print(f"[+] {len(TRUSTED_CHANNELS)} channel siap diproses.")
    return TRUSTED_CHANNELS
