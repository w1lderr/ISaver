import logging
import yt_dlp

def download_video(url, temp_file_path, platform):
    ydl_opts = {
        "format": "best",
        "outtmpl": f"{temp_file_path}.%(ext)s",
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(result)
    except Exception as e:
        logging.error(f"Download error for {platform}: {e}")
        return None