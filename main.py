import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Tentukan scope (izin) yang dibutuhkan. 
# SCOPES ini memberi izin penuh untuk mengelola channel YouTube (termasuk upload).
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    creds = None
    
    # File token.json menyimpan token akses pengguna dan dibuat otomatis saat
    # alur otorisasi pertama kali diselesaikan.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # Jika tidak ada kredensial yang valid (atau token kedaluwarsa), silakan login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Memperbarui token akses yang kedaluwarsa...")
            creds.refresh(Request())
        else:
            print("Memulai alur otorisasi baru via Browser...")
            # Membaca konfigurasi dari client_secret.json yang Anda buat manual tadi
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Simpan kredensial untuk dijalankan otomatis di lain waktu
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("File token.json berhasil dibuat/diperbarui.")

    # Membangun service API YouTube
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def main():
    try:
        # 1. Jalankan Autentikasi
        youtube = get_authenticated_service()
        print("Autentikasi Google Cloud sukses!")
        
        # 2. Test Koneksi API (Mengambil info channel Anda sendiri sebagai tes awal)
        print("Mencoba mengambil data channel YouTube Anda...")
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        # Menampilkan nama channel jika sukses tersambung
        if "items" in response:
            channel_name = response["items"][0]["snippet"]["title"]
            print(f"Sukses terhubung ke Channel: {channel_name}")
        else:
            print("Aplikasi terhubung, tetapi tidak menemukan data channel.")
            
    except googleapiclient.errors.HttpError as e:
        print(f"Terjadi error HTTP pada API: {e.resp.status} - {e.content}")
    except Exception as e:
        print(f"Terjadi error sistem: {e}")

if __name__ == "__main__":
    main()