import os
import re
from yt_dlp import YoutubeDL

# Base output directory
base_output_dir = 'videos'
if not os.path.exists(base_output_dir):
    os.makedirs(base_output_dir)

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_youtube(url):
    """YouTube downloader that automatically downloads best quality and organizes by playlist"""
    
    # Best quality format selector
    format_selector = 'bestvideo+bestaudio/best'
    
    print(f"🚀 Starting download: {url}")
    print(f"📊 Format: {format_selector}")
    
    # First, get video info to determine if it's a playlist or single video
    info_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:  # It's a playlist
                playlist_title = sanitize_filename(info.get('title', 'Unknown_Playlist'))
                playlist_dir = os.path.join(base_output_dir, playlist_title)
                
                print(f"📋 Playlist detected: {info.get('title', 'Unknown')}")
                print(f"📹 Videos: {len(info['entries'])}")
                print(f"📁 Saving to: {playlist_dir}")
                
                # Create playlist directory
                if not os.path.exists(playlist_dir):
                    os.makedirs(playlist_dir)
                
                # Download with playlist numbering
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': os.path.join(playlist_dir, '%(playlist_index)02d - %(title)s.%(ext)s'),
                    'ignoreerrors': True,
                    'no_warnings': False,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                    'writethumbnail': False,
                    'writeinfojson': False,
                    'retries': 3,
                    'fragment_retries': 3,
                    'socket_timeout': 30,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                }
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    print(f"✅ Playlist download completed!")
                    return True, playlist_dir
                    
            else:  # Single video
                title = sanitize_filename(info.get('title', 'Unknown'))
                uploader = info.get('uploader', 'Unknown')
                duration = info.get('duration', 0)
                
                print(f"📹 Single video: {info.get('title', 'Unknown')}")
                print(f"👤 Channel: {uploader}")
                if duration:
                    print(f"⏱️ Duration: {duration//60}:{duration%60:02d}")
                
                # For single videos, save directly to videos folder
                single_video_dir = base_output_dir
                
                ydl_opts = {
                    'format': format_selector,
                    'outtmpl': os.path.join(single_video_dir, '%(title)s.%(ext)s'),
                    'ignoreerrors': True,
                    'no_warnings': False,
                    'writesubtitles': False,
                    'writeautomaticsub': False,
                    'writethumbnail': False,
                    'writeinfojson': False,
                    'retries': 3,
                    'fragment_retries': 3,
                    'socket_timeout': 30,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                }
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    print(f"✅ Single video download completed!")
                    return True, single_video_dir
                    
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        
        # Fallback: try with lower quality
        print("🔄 Trying fallback quality...")
        fallback_format = 'best[height<=720]/best'
        
        try:
            # Try to determine structure again for fallback
            with YoutubeDL(info_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:  # Playlist fallback
                    playlist_title = sanitize_filename(info.get('title', 'Unknown_Playlist'))
                    playlist_dir = os.path.join(base_output_dir, playlist_title)
                    
                    if not os.path.exists(playlist_dir):
                        os.makedirs(playlist_dir)
                    
                    ydl_opts = {
                        'format': fallback_format,
                        'outtmpl': os.path.join(playlist_dir, '%(playlist_index)02d - %(title)s.%(ext)s'),
                        'ignoreerrors': True,
                        'retries': 2,
                    }
                    output_dir = playlist_dir
                else:  # Single video fallback
                    ydl_opts = {
                        'format': fallback_format,
                        'outtmpl': os.path.join(base_output_dir, '%(title)s.%(ext)s'),
                        'ignoreerrors': True,
                        'retries': 2,
                    }
                    output_dir = base_output_dir
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    print(f"✅ Fallback download completed!")
                    return True, output_dir
                    
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {str(fallback_error)}")
            print("\n💡 Troubleshooting:")
            print("1. Check if video is available in your region")
            print("2. Update yt-dlp: pip install --upgrade yt-dlp")
            print("3. Video might have restrictions or be private")
            return False, None

def show_downloaded_files(output_dir):
    """Show the downloaded files"""
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
        if files:
            print(f"\n📁 Downloaded files in '{output_dir}':")
            for file in sorted(files)[-10:]:  # Show last 10 files
                print(f"  • {file}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more files")
        else:
            print(f"\n📁 Directory '{output_dir}' is empty")

def main():
    print("🎬 Auto YouTube Downloader")
    print("🎯 Features: Best quality, Auto-organize playlists, Numbered videos")
    print("=" * 60)
    
    url = input('Enter YouTube URL: ').strip()
    
    if not url:
        print("❌ No URL provided!")
        return
    
    success, output_dir = download_youtube(url)
    
    if success and output_dir:
        print(f"\n🎉 Success! Files saved to: {output_dir}")
        show_downloaded_files(output_dir)
    else:
        print(f"\n😞 Download failed. Please check the URL and try again.")

if __name__ == '__main__':
    main()