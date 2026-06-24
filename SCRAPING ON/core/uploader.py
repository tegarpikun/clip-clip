import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Cakupan akses yang dibutuhkan untuk mengunggah video
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Mengautentikasi user menggunakan OAuth 2.0 client_secret.json."""
    creds = None
    # Token.json menyimpan akses token agar tidak perlu login ulang tiap hari
    if os.path.exists('config/token.json'):
        creds = Credentials.from_authorized_user_file('config/token.json', SCOPES)
        
    if not creds or not creds.valid:
        if not os.path.exists('client_secret.json'):
            print("[!] File 'client_secret.json' tidak ditemukan di root directory!")
            return None
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Simpan credentials untuk eksekusi otomatis berikutnya
        with open('config/token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('youtube', 'v3', credentials=creds)

def upload_to_youtube(video_path, title, description):
    """Mengunggah video otomatis ke YouTube Studio via API resmi."""
    youtube = get_authenticated_service()
    if not youtube:
        print("[!] Gagal menginisiasi YouTube API service.")
        return False
        
    body = {
        'snippet': {
            'title': title[:100], # Batasan maksimal judul YouTube
            'description': description,
            'categoryId': '22' # Kategori: People & Blogs
        },
        'status': {
            'privacyStatus': 'private', # Aman, bisa diubah ke public/scheduled manual atau otomatis
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimeType='video/mp4')
    
    print(f"[*] Mengunggah '{title}' ke YouTube...")
    try:
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[+] Progress Upload: {int(status.progress() * 100)}%")
        print(f"[+] Video SUKSES Diupload! Video ID: {response['id']}")
        return True
    except Exception as e:
        print(f"[!] Gagal mengunggah video ke YouTube: {e}")
        return False