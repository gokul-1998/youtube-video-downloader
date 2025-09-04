




from get_videos_from_playlist import get_videos_from_playlist
from playlist_utils import extract_playlist_id, extract_playlist_name
import json
import os
from utils import youtube_down, get_safe_folder_name

url=input("paste playlist url : ")
playlist_name = extract_playlist_name(url)
playlist_id = extract_playlist_id(url)

print(f"Playlist Name: {playlist_name}")
print(f"Playlist ID: {playlist_id}")

# Create a safe folder name for the playlist
safe_playlist_name = get_safe_folder_name(playlist_name)

# Additional safety check - if the folder name is too long or contains errors, use playlist ID
if len(safe_playlist_name) > 50 or "Error" in safe_playlist_name or "error" in safe_playlist_name:
    safe_playlist_name = f"Playlist_{playlist_id}" if playlist_id else "Unknown_Playlist"
    safe_playlist_name = get_safe_folder_name(safe_playlist_name)

playlist_folder = os.path.join('videos', safe_playlist_name)
print(f"Safe folder name: {safe_playlist_name}")

# Create the playlist directory if it doesn't exist
full_playlist_path = os.path.join('static', playlist_folder)
if not os.path.exists(full_playlist_path):
    os.makedirs(full_playlist_path)
    print(f"Created folder: {full_playlist_path}")

all_videos = get_videos_from_playlist(playlist_id)
print(json.dumps(all_videos, indent=2, ensure_ascii=False))
print(f"\nDownloading {len(all_videos)} videos to folder: {playlist_folder}")

# Download videos with serial numbers
for index, video in enumerate(all_videos, 1):
    print(f"Downloading video {index}/{len(all_videos)}: {video['title']}")
    youtube_down(video['url'], custom_output_dir=playlist_folder, serial_number=index)