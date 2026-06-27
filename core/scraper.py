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

    base_url = channel_url.rstrip("/")
    if not base_url.endswith("/videos"):
        base_url = base_url + "/videos"

    print(f"[*] Memeriksa channel: {base_url}")

    ydl_info_opts = {
        'quiet': True,
        'ignoreerrors': True,
        'extract_flat': 'in_playlist',
        'playlistend': 15,
        'cookiefile': 'cookies.txt',
    }

    video_id = None
    with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
        try:
            info = ydl.extract_info(base_url, download=False)
            if not info or 'entries' not in info:
                print("[-] Tidak bisa membaca daftar video.")
                return None
            for entry in info['entries']:
                if not entry:
                    continue
                duration = entry.get('duration') or 0
                vid_id = entry.get('id')
                title = entry.get('title', 'Unknown')
                print(f"    - '{title}' | durasi: {duration}s")
                if duration > 300:
                    video_id = vid_id
                    print(f"[+] Memilih: '{title}' ({duration}s)")
                    break
                elif duration == 0 and vid_id:
                    try:
                        detail = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
                        real_duration = detail.get('duration') or 0
                        print(f"      -> cek detail: {real_duration}s")
                        if real_duration > 300:
                            video_id = vid_id
                            print(f"[+] Memilih: '{title}' ({real_duration}s)")
                            break
                    except:
                        continue
        except Exception as e:
            print(f"[!] Gagal mengakses channel: {e}")
            return None

    if not video_id:
        print("[-] Tidak ada video > 5 menit yang ditemukan.")
        return None

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_dl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': False,
        'cookiefile': 'cookies.txt',
    }

    print(f"[*] Mendownload: {video_url}")
    with yt_dlp.YoutubeDL(ydl_dl_opts) as ydl:
        try:
            dl_info = ydl.extract_info(video_url, download=True)
            if dl_info:
                real_id = dl_info.get('id', video_id)
                file_path = os.path.join(output_dir, f"{real_id}.mp4")
                if os.path.exists(file_path):
                    print(f"[+] Sukses mendownload: {file_path}")
                    return file_path
            files = sorted(
                [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.mp4')],
                key=os.path.getmtime, reverse=True
            )
            if files:
                print(f"[+] Sukses mendownload: {files[0]}")
                return files[0]
            print("[-] File tidak ditemukan setelah download.")
            return None
        except Exception as e:
            print(f"[!] Gagal mendownload: {e}")
            return None
