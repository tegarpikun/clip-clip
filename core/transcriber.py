import os
import whisper
from moviepy.video.io.VideoFileClip import VideoFileClip

def extract_and_transcribe(video_path, audio_dir="storage/audio_tracks"):
    """Mengekstrak audio dari MP4 lalu mentranskripnya menggunakan OpenAI Whisper."""
    os.makedirs(audio_dir, exist_ok=True)
    video_id = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(audio_dir, f"{video_id}.wav")
    
    print(f"[*] Mengekstrak audio dari {video_path}...")
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le', ffmpeg_params=["-ac", "1"], logger=None)
        video.close()
        
        print("[*] Whisper AI sedang memproses transkripsi (ini memerlukan waktu)...")
        model = whisper.load_model("base")  # Ukuran base cepat dan cukup akurat
        result = model.transcribe(audio_path)
        
        # Bersihkan file audio setelah selesai transkrip untuk hemat space
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        print("[+] Transkripsi selesai.")
        return result["segments"]  # Mengembalikan list berisi teks dan timestamp
    except Exception as e:
        print(f"[!] Gagal melakukan transkripsi: {e}")
        return None
