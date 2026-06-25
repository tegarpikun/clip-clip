import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Scope gabungan: upload + manage channel
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

TOKEN_PATH = 'config/token.json'

def get_authenticated_service():
    """Autentikasi menggunakan token.json yang sudah ada (non-interactive).
    
    CATATAN: token.json harus dibuat SEKALI secara manual di komputer lokal,
    lalu isinya disimpan sebagai GitHub Secret bernama TOKEN_JSON.
    Workflow akan merekonstruksi file ini setiap kali berjalan.
    """
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Token kedaluwarsa, memperbarui otomatis...")
            creds.refresh(Request())
            # Simpan token yang sudah di-refresh kembali
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
            print("[+] Token berhasil diperbarui.")
        else:
            # Jika sampai sini di GitHub Actions, berarti TOKEN_JSON Secret belum diset
            raise RuntimeError(
                "[!] FATAL: token.json tidak valid dan tidak bisa di-refresh. "
                "Jalankan 'python generate_token.py' di lokal dulu, "
                "lalu copy isi token.json ke GitHub Secret 'TOKEN_JSON'."
            )

    return build('youtube', 'v3', credentials=creds)


def upload_to_youtube(video_path, title, description):
    """Mengunggah video ke YouTube Studio via API resmi."""
    youtube = get_authenticated_service()
    if not youtube:
        print("[!] Gagal menginisiasi YouTube API service.")
        return False

    body = {
        'snippet': {
            'title': title[:100],
            'description': description,
            'categoryId': '22'  # People & Blogs
        },
        'status': {
            'privacyStatus': 'private',
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimeType='video/mp4')

    print(f"[*] Mengunggah '{title}' ke YouTube...")
    try:
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
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
