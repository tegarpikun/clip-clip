import json
from google import genai

def analyze_best_moment(segments, api_key):
    """Meminta Gemini menganalisis momen paling menarik untuk dijadikan Shorts."""
    client = genai.Client(api_key=api_key)
    
    # Format data transkrip agar ringkas dikirim ke API
    transcript_data = ""
    for seg in segments:
        transcript_data += f"[{seg['start']:.1f} - {seg['end']:.1f}] {seg['text']}\n"
        
    prompt = f"""
    Berikut adalah transkrip video ber-timestamp. Cari SATU potongan momen berdurasi antara 30 sampai 50 detik yang paling menarik, klimaks, kontroversial, atau edukatif untuk dijadikan YouTube Shorts yang viral.
    
    Buat juga judul yang memicu rasa penasaran (clickbait positif) beserta deskripsi kaya SEO dan hashtag populer (#Shorts, #Fyp).
    
    Anda WAJIB merespons HANYA dalam format JSON mentah tanpa markdown (jangan gunakan ```json) dengan struktur seperti ini:
    {{
        "start": 120.5,
        "end": 165.2,
        "title": "Judul Video Di Sini",
        "description": "Deskripsi video dan link affiliate di sini #Shorts #Fyp"
    }}

    Transkrip:
    {transcript_data}
    """
    
    print("[*] Gemini sedang menganalisis momen terbaik untuk klip...")
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        # Parsing data JSON dari Gemini
        data = json.loads(response.text.strip())
        print(f"[+] Momen ditemukan: Detik {data['start']} sampai {data['end']}")
        return data
    except Exception as e:
        print(f"[!] Gemini Clipper gagal menganalisis teks: {e}")
        return None