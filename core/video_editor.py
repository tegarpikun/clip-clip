import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.crop import crop

def render_vertical_shorts(video_path, start_time, end_time, output_dir="storage/output_shorts"):
    os.makedirs(output_dir, exist_ok=True)
    video_id = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_dir, f"shorts_{video_id}.mp4")

    print(f"[*] Memotong dan mengedit video ke format 9:16...")
    try:
        video = VideoFileClip(video_path).subclipped(start_time, end_time)
        w, h = video.size

        new_w = int(h * (9 / 16))
        x1 = (w - new_w) // 2
        x2 = x1 + new_w

        cropped_video = crop(video, x1=x1, y1=0, x2=x2, y2=h)

        print("[*] Proses rendering file MP4 Shorts...")
        cropped_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            bitrate="5000k",
            logger=None
        )

        video.close()
        cropped_video.close()
        print(f"[+] Sukses merender Shorts: {output_path}")
        return output_path
    except Exception as e:
        print(f"[!] Video Editor Error: {e}")
        return None
