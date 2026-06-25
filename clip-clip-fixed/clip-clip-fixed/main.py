import os
import sys
from core.trend_hunter import hunt_high_cpm_channels
from core.scraper import get_target_channels, download_latest_video
from core.transcriber import extract_and_transcribe
from core.ai_clipper import analyze_best_moment
from core.video_editor import render_vertical_shorts
from core.uploader import upload_to_youtube

def main():
    # Ambil API key Gemini dari environment variable (GitHub Secret)
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("[!] FATAL: Environment variable GEMINI_API_KEY tidak ditemukan.")
        print("    Set GitHub Secret 'GEMINI_API_KEY' dengan API key Gemini Anda.")
        sys.exit(1)

    print("=" * 60)
    print("  CLIP-CLIP AUTOMATION - Memulai Pipeline Harian")
    print("=" * 60)

    # ─── STEP 1: Hunt tren channel ber-CPM tinggi ───────────────
    print("\n[STEP 1/5] Hunting channel tren...")
    channels = hunt_high_cpm_channels(gemini_api_key)
    if not channels:
        # Fallback ke channels.txt yang sudah ada
        print("[*] Fallback ke config/channels.txt yang tersimpan...")
        channels = get_target_channels()

    if not channels:
        print("[!] Tidak ada channel target. Pipeline berhenti.")
        sys.exit(0)

    # ─── STEP 2-5: Proses tiap channel ─────────────────────────
    uploaded_count = 0
    MAX_UPLOADS = 4  # Batasi upload harian

    for channel_url in channels:
        if uploaded_count >= MAX_UPLOADS:
            print(f"\n[*] Sudah mencapai batas upload harian ({MAX_UPLOADS} video). Selesai.")
            break

        print(f"\n{'─'*50}")
        print(f"[*] Memproses channel: {channel_url}")

        # STEP 2: Download video terbaru
        print("\n[STEP 2/5] Mendownload video terbaru...")
        video_path = download_latest_video(channel_url)
        if not video_path:
            print("[-] Tidak ada video baru. Lanjut ke channel berikutnya.")
            continue

        # STEP 3: Transkripsi audio
        print("\n[STEP 3/5] Transkripsi dengan Whisper AI...")
        segments = extract_and_transcribe(video_path)
        if not segments:
            print("[-] Transkripsi gagal. Lanjut ke channel berikutnya.")
            continue

        # STEP 4: Analisis momen terbaik dengan Gemini
        print("\n[STEP 4/5] Analisis momen terbaik dengan Gemini...")
        clip_data = analyze_best_moment(segments, gemini_api_key)
        if not clip_data:
            print("[-] Analisis klip gagal. Lanjut ke channel berikutnya.")
            continue

        # STEP 5: Edit video → format 9:16 Shorts
        print("\n[STEP 5/5] Render video format Shorts 9:16...")
        output_path = render_vertical_shorts(
            video_path,
            clip_data['start'],
            clip_data['end']
        )
        if not output_path:
            print("[-] Render video gagal. Lanjut ke channel berikutnya.")
            continue

        # STEP 6: Upload ke YouTube
        print("\n[STEP 6/6] Upload ke YouTube...")
        success = upload_to_youtube(
            output_path,
            clip_data['title'],
            clip_data['description']
        )
        if success:
            uploaded_count += 1
            print(f"[+] Total uploaded hari ini: {uploaded_count}/{MAX_UPLOADS}")

    print(f"\n{'='*60}")
    print(f"  Pipeline selesai. Total video diupload: {uploaded_count}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
