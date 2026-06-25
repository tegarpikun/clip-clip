import os
import yt_dlp

def get_target_channels(file_path="config/channels.txt"):
    if not os.path.exists(file_path):
        print(f"[!] File {file_path} tidak ditemukan.")
        return []
    with open(file_path, "r") as f:
        channels = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
    return channels

def download_latest_video(channel_url, output_dir="storage/raw_videos"):
    os.makedirs(output_dir, exist_ok=True)

    # Ambil info 10 video terbaru tanpa download dulu
    ydl_opts_info = {
        'playlistend': 10,
        'quiet': True,
        'ignoreerrors': True,
        'extract_flat': True,
    }

    print(f"[*] Memeriksa channel: {channel_url}")
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
        except Exception as e:
            print(f"[!] Gagal mengakses channel: {e}")
            return None

    if not info or 'entries' not in info:
        print("[-] Tidak bisa membaca daftar video channel.")
        return None

    # Cari video pertama yang durasinya > 5 menit
    target_video = None
    for entry in info['entries']:
        if not entry:
            continue
        duration = entry.get('duration') or 0
        video_id = entry.get('id')
        title = entry.get('title', 'Unknown')
        print(f"    - '{title}' | durasi: {duration}s")
        if duration > 300:
            target_video = entry
            print(f"[+] Video lolos filter: '{title}' ({duration}s)")
            break

    if not target_video:
        print("[-] Tidak ada video > 5 menit di 10 video terbaru.")
        return None

    # Download video yang dipilih
    video_url = f"https://www.youtube.com/watch?v={target_video['id']}"
    ydl_opts_dl = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': False,
    }

    print(f"[*] Mendownload: {video_url}")
    with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
        try:
            ydl.download([video_url])
            file_path = os.path.join(output_dir, f"{target_video['id']}.mp4")
            print(f"[+] Sukses mendownload: {file_path}")
            return file_path
        except Exception as e:
            print(f"[!] Gagal mendownload video: {e}")
            return None
