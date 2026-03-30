import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

def get_music_recommendations(query):
    results = sp.search(q=query, type='track', limit=10)
    return [
        {"name": item["name"], "artist": item["artists"][0]["name"], "url": item["external_urls"]["spotify"]}
        for item in results["tracks"]["items"]
    ]