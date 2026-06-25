import os
import yt_dlp

def get_target_channels(file_path="config/channels.txt"):
    """Membaca daftar URL channel dari file konfigurasi."""
    if not os.path.exists(file_path):
        print(f"[!] File {file_path} tidak ditemukan. Buat file terlebih dahulu.")
        return []
    with open(file_path, "r") as f:
        channels = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
    return channels

def download_latest_video(channel_url, output_dir="storage/raw_videos"):
    """Mendownload 1 video terbaru dari channel jika durasinya > 10 menit."""
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'playlistend': 1,
        'match_filter': lambda info, *, incomplete: None if (
            info.get('duration', 0) > 600
        ) else 'Video tidak memenuhi kriteria (terlalu pendek)',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'ignoreerrors': True,
        'quiet': False
    }

    print(f"[*] Memeriksa channel: {channel_url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=True)
            if info and 'entries' in info and info['entries']:
                video_data = info['entries'][0]
                if video_data:
                    file_path = os.path.join(output_dir, f"{video_data['id']}.mp4")
                    print(f"[+] Sukses mendownload: {file_path}")
                    return file_path
            print("[-] Tidak ada video baru yang sesuai kriteria hari ini.")
            return None
        except Exception as e:
            print(f"[!] Gagal memproses channel {channel_url}: {e}")
            return None
