import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
import os
import yt_dlp as youtube_dl
from pytube import Search



load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_URI = os.getenv("REDIRECT_URI")
scope = "user-library-read"
    
def get_youtube_link(video_title):
    search = Search(video_title)
    for video in search.results:
        return video.watch_url

def download_video_as_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality':'192'
        }],
        'outtmpl' : '%(title)s.mp3',
        'quiet': False,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_URI,
                                               scope=scope))
youtube_video_link = None
results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):
    track = item['track']
    idx = idx + 1
    entire_video_title = track['artists'][0]['name'] + " - " + track['name']
    print(f"entire_video_title is: {entire_video_title}")
    print(idx, track['artists'][0]['name'], " - ", track['name'])
    youtube_video_link = get_youtube_link(entire_video_title)
    download_video_as_mp3(youtube_video_link)
