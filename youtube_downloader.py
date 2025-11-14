import yt_dlp
import os
import re
import time
import random
from functools import wraps

def rate_limit(max_per_minute=6):
    """Rate limiting decorator"""
    def decorator(func):
        calls = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls older than 1 minute
            calls[:] = [call for call in calls if now - call < 60]
            
            if len(calls) >= max_per_minute:
                sleep_time = 60 - (now - calls[0]) + random.uniform(2, 5)
                print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
                calls.clear()
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
class YouTubeDownloader:
        @rate_limit(max_per_minute=6)  # 6 requests per minute for info
    def get_video_info(self, url):
        # ... keep the existing method body the same

    @rate_limit(max_per_minute=3)  # 3 downloads per minute
    def download_audio(self, url, progress_hook=None):
        # ... keep the existing method body the same
    def __init__(self, download_folder):
        self.download_folder = download_folder
        # Direct path to FFmpeg - use the same path that worked in the manual test
        self.ffmpeg_location = r"C:\ffmpeg\bin"
        print(f"YouTubeDownloader initialized with folder: {download_folder}")
        print(f"FFmpeg location: {self.ffmpeg_location}")

        def get_ydl_opts(self, for_download=False):
        """Return yt-dlp options with proper headers and configuration"""
        base_opts = {
            # Format selection
            'format': 'bestaudio/best',
            
            # Output template
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            
            # Post-processing to convert to MP3
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            
            # FFmpeg location
            'ffmpeg_location': self.ffmpeg_location,
            
            # Basic settings
            'writethumbnail': False,
            'embedthumbnail': False,
            'addmetadata': True,
            
            # Network settings
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            
            # Additional settings
            'extractaudio': True,
            'audioformat': 'mp3',
            
            # Browser-like headers to avoid bot detection
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
        }
        
        if for_download:
            base_opts['quiet'] = False
            base_opts['no_warnings'] = False
        else:
            base_opts['quiet'] = True
            base_opts['no_warnings'] = True
            
        return base_opts

    def get_video_info(self, url):
        """Get video information without downloading"""
        try:
            print(f"Getting video info for: {url}")
            with yt_dlp.YoutubeDL(self.get_ydl_opts(for_download=False)) as ydl:
                info = ydl.extract_info(url, download=False)
                print(f"Video info retrieved: {info.get('title', 'Unknown')}")
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown'),
                    'duration': self.format_duration(info.get('duration', 0)),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0)
                }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return {'success': False, 'error': str(e)}

    def download_audio(self, url, progress_hook=None):
        """Download audio from YouTube URL"""
        try:
            ydl_opts = self.get_ydl_opts(for_download=True)
            
            # Add progress hook if provided
            if progress_hook:
                ydl_opts['progress_hooks'] = [progress_hook]

            print(f"Starting download process for: {url}")
            print(f"Using FFmpeg at: {self.ffmpeg_location}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get info first
                info = ydl.extract_info(url, download=False)
                original_title = info['title']
                expected_filename = self.sanitize_filename(f"{original_title}.mp3")
                expected_path = os.path.join(self.download_folder, expected_filename)
                
                print(f"Expected output: {expected_filename}")
                
                # Download the audio
                print("Starting download and conversion...")
                ydl.download([url])
                print("Download process completed")
            
            # Check if MP3 file was created
            if os.path.exists(expected_path):
                print(f"✓ MP3 file created successfully: {expected_filename}")
                return {
                    'success': True,
                    'filename': expected_filename,
                    'title': original_title,
                    'duration': info.get('duration', 0)
                }
            
            # If expected file doesn't exist, look for any MP3 files
            print("Checking for MP3 files in download folder...")
            mp3_files = []
            for file in os.listdir(self.download_folder):
                if file.endswith('.mp3'):
                    mp3_files.append(file)
                    print(f"Found MP3 file: {file}")
            
            if mp3_files:
                latest_file = max(mp3_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
                print(f"✓ Using MP3 file: {latest_file}")
                return {
                    'success': True,
                    'filename': latest_file,
                    'title': original_title,
                    'duration': info.get('duration', 0)
                }
            
            return {'success': False, 'error': 'No MP3 files were created'}
                
        except Exception as e:
            print(f"Download error: {str(e)}")
            return {'success': False, 'error': str(e)}

            # Add progress hook if provided
            if progress_hook:
                ydl_opts['progress_hooks'] = [progress_hook]

            print(f"Starting download process for: {url}")
            print(f"Using FFmpeg at: {self.ffmpeg_location}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get info first
                info = ydl.extract_info(url, download=False)
                original_title = info['title']
                expected_filename = self.sanitize_filename(f"{original_title}.mp3")
                expected_path = os.path.join(self.download_folder, expected_filename)
                
                print(f"Expected output: {expected_filename}")
                
                # Download the audio
                print("Starting download and conversion...")
                ydl.download([url])
                print("Download process completed")
            
            # Check if MP3 file was created
            if os.path.exists(expected_path):
                print(f"✓ MP3 file created successfully: {expected_filename}")
                return {
                    'success': True,
                    'filename': expected_filename,
                    'title': original_title,
                    'duration': info.get('duration', 0)
                }
            
            # If expected file doesn't exist, look for any MP3 files
            print("Checking for MP3 files in download folder...")
            mp3_files = []
            for file in os.listdir(self.download_folder):
                if file.endswith('.mp3'):
                    mp3_files.append(file)
                    print(f"Found MP3 file: {file}")
            
            if mp3_files:
                latest_file = max(mp3_files, key=lambda f: os.path.getctime(os.path.join(self.download_folder, f)))
                print(f"✓ Using MP3 file: {latest_file}")
                return {
                    'success': True,
                    'filename': latest_file,
                    'title': original_title,
                    'duration': info.get('duration', 0)
                }
            
            return {'success': False, 'error': 'No MP3 files were created'}
                
        except Exception as e:
            print(f"Download error: {str(e)}")
            return {'success': False, 'error': str(e)}

    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        filename = filename.replace('\'', '').replace('"', '')
        
        if len(filename) > 100:
            name, ext = os.path.splitext(filename)
            filename = name[:100-len(ext)] + ext
            
        return filename

    def format_duration(self, seconds):
        """Format duration in seconds to HH:MM:SS"""
        if not seconds:
            return "00:00"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:

            return f"{minutes:02d}:{secs:02d}"
