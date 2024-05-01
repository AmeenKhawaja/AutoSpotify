import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp as youtube_dl
from pytube import Search

class SpotifyYouTubeDownloader:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_URI = os.getenv("REDIRECT_URI")
        self.scope = "user-library-read"
        self.mp3_directory = "mp3s"

        self.ensure_directory_exists(self.mp3_directory)

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_URI,
            scope=self.scope
        ))

    def ensure_directory_exists(self, file_path):
        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def get_youtube_link(self, video_title):
        search = Search(video_title)
        for video in search.results:
            return video.watch_url
        return None 

    def download_video_as_mp3(self, url):
        if url is None:
            print("No URL provided for download.")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            'outtmpl': os.path.join(self.mp3_directory, '%(title)s.%(ext)s'),
            'quiet': False,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def run(self):
        results = self.sp.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            entire_video_title = f"{track['artists'][0]['name']} - {track['name']}"
            print(f"{idx + 1}: {entire_video_title}")
            youtube_video_link = self.get_youtube_link(entire_video_title)
            self.download_video_as_mp3(youtube_video_link)

if __name__ == '__main__':
    downloader = SpotifyYouTubeDownloader()
    downloader.run()
