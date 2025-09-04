




from get_videos_from_playlist import get_videos_from_playlist
from playlist_utils import extract_playlist_id, extract_playlist_name
import json
from utils import youtube_down
url="https://www.youtube.com/watch?v=waGfV-IoOt8&list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ&index=3&ab_channel=KunalKushwaha"

playlist_name = extract_playlist_name(url)
playlist_id = extract_playlist_id(url)

print(f"Playlist Name: {playlist_name}")
all_videos = get_videos_from_playlist(playlist_id)
print(json.dumps(all_videos, indent=2, ensure_ascii=False))
for video in all_videos:
    youtube_down(video['url'])