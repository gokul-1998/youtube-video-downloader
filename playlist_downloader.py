import os
from yt_dlp import YoutubeDL

# Ensure the 'videos' directory exists
output_dir = 'videos'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_youtube(url):
    """YouTube downloader that tries highest quality first with fallbacks"""
    
    # List of format options from highest to lowest quality
    format_options = [
        # Try highest quality first
        'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'bestvideo[height<=720]+bestaudio/best[height<=720]', 
        'best[height<=1080][ext=mp4]/best[height<=1080]',
        'best[height<=720][ext=mp4]/best[height<=720]',
        'best[ext=mp4]/best',
        'best[height<=480]/best',
        'worst[height>=360]/worst'  # Last resort
    ]
    
    for i, format_selector in enumerate(format_options, 1):
        print(f"\n--- Attempt {i}: Trying {format_selector.split('/')[0]}... ---")
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'no_warnings': False,  # Show warnings to understand issues
            'writesubtitles': False,
            'writeautomaticsub': False,
            'writethumbnail': False,
            'writeinfojson': False,
            'retries': 3,
            'fragment_retries': 3,
            'socket_timeout': 30,
            # Add user agent to avoid detection
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                # First, get video info to show what we're downloading
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:  # It's a playlist
                    print(f"📋 Playlist: {info.get('title', 'Unknown')}")
                    print(f"📹 Videos: {len(info['entries'])}")
                    
                    # Download playlist
                    ydl.download([url])
                    print(f"✅ Playlist download completed with format: {format_selector}")
                    return True
                    
                else:  # Single video
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 0)
                    uploader = info.get('uploader', 'Unknown')
                    
                    print(f"📹 Video: {title}")
                    print(f"👤 Channel: {uploader}")
                    print(f"⏱️ Duration: {duration//60}:{duration%60:02d}")
                    
                    # Download video
                    ydl.download([url])
                    print(f"✅ Video download completed with format: {format_selector}")
                    return True
                    
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Failed: {error_msg[:100]}...")
            
            # If it's the last attempt, show full error
            if i == len(format_options):
                print(f"Full error: {error_msg}")
            else:
                print("Trying next quality option...")
    
    print("\n💥 All quality options failed!")
    print("\nTroubleshooting:")
    print("1. Check if video is available in your region")
    print("2. Update yt-dlp: pip install --upgrade yt-dlp")  
    print("3. Try with VPN if geo-blocked")
    print("4. Video might have restrictions")
    return False

def show_available_formats(url):
    """Show available formats for the video"""
    print("🔍 Checking available formats...")
    ydl_opts = {
        'listformats': True,
        'quiet': False,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"Error checking formats: {e}")

def main():
    print("🎬 High Quality YouTube Downloader")
    print("=" * 40)
    
    url = input('Enter YouTube URL: ').strip()
    
    if not url:
        print("❌ No URL provided!")
        return
    
    # Ask if user wants to see available formats first
    check_formats = input("\n🔍 Check available formats first? (y/n): ").lower().strip()
    if check_formats == 'y':
        show_available_formats(url)
        proceed = input("\n▶️ Proceed with download? (y/n): ").lower().strip()
        if proceed != 'y':
            print("Download cancelled.")
            return
    
    print(f"\n🚀 Starting download: {url}")
    success = download_youtube(url)
    
    if success:
        print(f"\n🎉 Success! Check the '{output_dir}' folder for your downloads.")
        
        # Show downloaded files
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            if files:
                print(f"\n📁 Downloaded files:")
                for file in sorted(files)[-5:]:  # Show last 5 files
                    print(f"  • {file}")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more files")
    else:
        print(f"\n😞 Download failed. The video might be restricted or unavailable.")

if __name__ == '__main__':
    main()