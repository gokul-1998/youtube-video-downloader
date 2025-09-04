from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Replace with your API key
API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = "PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ"

# Build YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_videos_from_playlist(playlist_id):
    videos = []
    next_page_token = None

    while True:
        # Call playlistItems.list API
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            video_title = item["snippet"]["title"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            videos.append({
                "title": video_title,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return videos

if __name__ == "__main__":
    all_videos = get_videos_from_playlist(PLAYLIST_ID)
    # Print JSON output
    print(json.dumps(all_videos, indent=2, ensure_ascii=False))
