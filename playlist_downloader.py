import os
from yt_dlp import YoutubeDL

# Ensure the 'videos' directory exists
output_dir = 'videos'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_youtube(url):
    """Simple YouTube downloader with minimal options"""
    
    # Very minimal options to avoid errors
    ydl_opts = {
        'format': 'worst[ext=mp4]/worst',  # Start with worst quality to test
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading...")
            ydl.download([url])
            print("Download completed!")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nTrying alternative format...")
        
        # Try with even simpler options
        ydl_opts_simple = {
            'format': 'best',
            'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),  # Use video ID as filename
        }
        
        try:
            with YoutubeDL(ydl_opts_simple) as ydl:
                ydl.download([url])
                print("Download completed with alternative method!")
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")

if __name__ == '__main__':
    url = input('Enter YouTube URL: ')
    download_youtube(url)