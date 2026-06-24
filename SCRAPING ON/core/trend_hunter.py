import os
from google import genai

def hunt_high_cpm_channels(api_key):
    """Menggunakan Gemini untuk meriset dan memperbarui daftar channel YouTube potensial."""
    client = genai.Client(api_key=api_key)
    
    prompt = """
    Bertindaklah sebagai Pakar Strategi Media Digital dan Analis YouTube Growth. 
    Berikan 5 URL channel YouTube besar/viral berbahasa Indonesia atau Inggris yang berada di niche:
    1. Keuangan / Crypto / Bisnis (CPM Tertinggi)
    2. Pengembangan Diri / Motivasi Tinggi
    3. Teknologi / Gadget / AI
    
    Pastikan channel tersebut sering mengunggah video panjang (>10 menit) berupa podcast atau monolog edukasi yang berpotensi tinggi menghasilkan penonton jika dipotong menjadi klip pendek (Shorts).
    
    Keluarkan hasil analisis Anda HANYA dalam format daftar URL YouTube murni, satu baris satu URL, tanpa teks penjelasan apa pun, tanpa markdown (no ```).
    """
    
    print("[*] Gemini sedang berburu tren channel ber-CPM tinggi...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        cleaned_urls = [line.strip() for line in response.text.split('\n') if "youtube.com" in line]
        
        if cleaned_urls:
            os.makedirs("config", exist_ok=True)
            with open("config/channels.txt", "w") as f:
                f.write("\n".join(cleaned_urls))
            print(f"[+] Sukses memperbarui config/channels.txt dengan {len(cleaned_urls)} channel baru.")
            return cleaned_urls
        else:
            print("[-] Gemini tidak mengembalikan URL yang valid.")
            return []
    except Exception as e:
        print(f"[!] Gagal menjalankan Trend Hunter: {e}")
        return []