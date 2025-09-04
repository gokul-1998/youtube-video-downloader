import yt_dlp
import re

def extract_playlist_name(url):
    """
    Extract playlist name from a YouTube URL using yt-dlp
    """
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'quiet': True,  # Suppress output
            'no_warnings': True,
            'extract_flat': True,  # Only extract metadata, don't download
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info from the URL
            info = ydl.extract_info(url, download=False)
            
            # Get playlist title
            if 'title' in info:
                return info['title']
            elif 'playlist_title' in info:
                return info['playlist_title']
            else:
                return "Playlist title not found"
                
    except Exception as e:
        return f"Error extracting playlist name: {str(e)}"

def extract_playlist_id(url):
    """
    Extract playlist ID from YouTube URL
    """
    # Pattern to match YouTube playlist URLs
    pattern = r'[?&]list=([^&]+)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None

# Example usage
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=waGfV-IoOt8&list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ&index=3&ab_channel=KunalKushwaha"
    
    # Extract playlist ID
    playlist_id = extract_playlist_id(url)
    print(f"Playlist ID: {playlist_id}")
    
    # Extract playlist name
    playlist_name = extract_playlist_name(url)
    print(f"Playlist Name: {playlist_name}")

# Alternative method using requests and BeautifulSoup (if yt-dlp is not available)
def extract_playlist_name_alternative(url):
    """
    Alternative method using web scraping (less reliable)
    """
    import requests
    from bs4 import BeautifulSoup
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for playlist title in various meta tags
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            return meta_title.get('content')
        
        # Alternative: look for title tag
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip()
            
        return "Playlist title not found"
        
    except Exception as e:
        return f"Error: {str(e)}"

# Installation note:
# print("\nTo install required libraries:")
# print("pip install yt-dlp")
# print("pip install requests beautifulsoup4")