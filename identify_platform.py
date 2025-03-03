import logging
import yt_dlp

YOUTUBE_IDENTIFIERS = ["/shorts/"]
TIKTOK_IDENTIFIERS = ["tiktok.com"]
INSTAGRAM_IDENTIFIERS = ["/reel/"]

def identify_platform(url):
    if any(identifier in url for identifier in YOUTUBE_IDENTIFIERS):
        return "YouTube"
    elif any(identifier in url for identifier in TIKTOK_IDENTIFIERS):
        return "TikTok"
    elif any(identifier in url for identifier in INSTAGRAM_IDENTIFIERS):
        return "Instagram"
    else:
        return None