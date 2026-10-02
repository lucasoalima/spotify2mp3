from exceptions import ConfigVideoLowViewCount, ConfigVideoMaxLength, YoutubeItemNotFound
import os
import truststore

truststore.inject_into_ssl()

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


class YouTube:
    def __init__(self):
        pass

    def search(self, search_query, max_length, min_view_count, search_count=1):
        options = {"quiet": True, "no_warnings": True, "noplaylist": True}

        try:
            with YoutubeDL(options) as youtube:
                results = youtube.extract_info(
                    f"ytsearch{search_count}:{search_query}", download=False)
        except DownloadError as error:
            raise YoutubeItemNotFound(
                f"Skipped song -- Could not search YouTube: {error}") from error

        videos = results.get("entries", [])
        videos = [video for video in videos if video and video.get("webpage_url")]
        if not videos:
            raise YoutubeItemNotFound('Skipped song -- Could not load from YouTube')

        chosen_video = max(videos, key=lambda video: video.get("view_count") or 0)
        youtube_video_link = chosen_video["webpage_url"]
        duration = chosen_video.get("duration") or 0
        view_count = chosen_video.get("view_count") or 0

        if duration >= max_length:
            raise ConfigVideoMaxLength(
                f'Length {duration}s exceeds MAX_LENGTH value of {max_length}s [{youtube_video_link}]')

        if view_count <= min_view_count:
            raise ConfigVideoLowViewCount(
                f'View count {view_count} does not meet MIN_VIEW_COUNT value of {min_view_count} [{youtube_video_link}]')

        return youtube_video_link

    def download(self, url, audio_bitrate):
        quality_kbps = max(48, min(320, audio_bitrate // 1000))
        options = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "nopart": True,
            "quiet": True,
            "no_warnings": True,
            "outtmpl": "temp/%(id)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": str(quality_kbps),
            }],
        }

        with YoutubeDL(options) as youtube:
            info = youtube.extract_info(url, download=True)
            source_path = youtube.prepare_filename(info)

        return os.path.splitext(source_path)[0] + ".mp3", quality_kbps
