"""
Jalankan script ini SEKALI di komputer lokal untuk membuat token.json.
Setelah dapat token.json, copy isinya ke GitHub Secret bernama TOKEN_JSON.

Cara pakai:
    python generate_token.py

Syarat:
    - File client_secret.json harus ada di folder ini
    - Koneksi internet aktif
    - Browser akan terbuka otomatis untuk login Google
"""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

def main():
    if not os.path.exists('client_secret.json'):
        print("[!] File 'client_secret.json' tidak ditemukan!")
        print("    Download dari Google Cloud Console > API & Services > Credentials")
        return

    print("[*] Membuka browser untuk otorisasi Google...")
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)

    os.makedirs('config', exist_ok=True)
    with open('config/token.json', 'w') as token:
        token.write(creds.to_json())

    print("\n[+] SUKSES! File config/token.json berhasil dibuat.")
    print("\n─── LANGKAH SELANJUTNYA ───────────────────────────────")
    print("1. Buka file config/token.json")
    print("2. Copy SEMUA isinya")
    print("3. Buka GitHub repo > Settings > Secrets and variables > Actions")
    print("4. Buat secret baru:")
    print("   Name : TOKEN_JSON")
    print("   Value: (paste isi token.json di sini)")
    print("5. Buat juga secret:")
    print("   Name : GEMINI_API_KEY")
    print("   Value: (API key Gemini Anda dari ai.google.dev)")
    print("   Name : CLIENT_SECRET_JSON")
    print("   Value: (isi file client_secret.json)")
    print("────────────────────────────────────────────────────────")

if __name__ == "__main__":
    main()
