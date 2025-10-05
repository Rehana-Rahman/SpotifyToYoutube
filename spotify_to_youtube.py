import os
import re
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------- CONFIG ----------
SPOTIFY_CLIENT_ID = "613e026346794be88daaac78710967dc"
SPOTIFY_CLIENT_SECRET = "72f911d0895e4b1d91c09f21f26b172d"
SPOTIFY_REDIRECT_URI = "https://abcdef1234.ngrok.io/callback"
SPOTIFY_SCOPE = "playlist-read-private"

YOUTUBE_OAUTH_FILE = "client_secrets.json"
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube"]

SPOTIFY_PLAYLIST = "https://open.spotify.com/playlist/66xlJ7lqHLGMZ1JeD72t59?si=OYUDv1I0QnqVf_c9vbAIjg&pi=JMtk8KiBTcSAb"
MAX_SEARCH_RESULTS = 3
# ----------------------------

def get_spotify_tracks(sp_client, playlist_uri):
    tracks = []
    results = sp_client.playlist_items(
        playlist_uri,
        additional_types=['track'],
        fields='items.track.name,items.track.artists.name,next',
        limit=100
    )
    while results:
        for item in results['items']:
            track = item['track']
            if not track:
                continue
            title = track['name']
            artists = ", ".join([a['name'] for a in track['artists']])
            tracks.append({'title': title, 'artists': artists})
        results = sp_client.next(results) if results.get('next') else None
    return tracks

def youtube_authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_OAUTH_FILE, scopes=YOUTUBE_SCOPES)
    creds = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=creds)

def youtube_search_video(youtube, query, max_results=3):
    response = youtube.search().list(q=query, part='id,snippet', type='video', maxResults=max_results).execute()
    return response.get('items', [])

def best_query(track):
    return f"{track['title']} {track['artists']} audio"

def create_youtube_playlist(youtube, title, description="", privacy="private"):
    body = {
        "snippet": {"title": title, "description": description},
        "status": {"privacyStatus": privacy}
    }
    return youtube.playlists().insert(part="snippet,status", body=body).execute()['id']

def add_video_to_playlist(youtube, playlist_id, video_id):
    body = {
        "snippet": {"playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}
    }
    youtube.playlistItems().insert(part="snippet", body=body).execute()

def main():
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE,
        open_browser=False
    )
    print("Please open this URL in your browser to authenticate Spotify:")
    print(auth_manager.get_authorize_url())
    sp = Spotify(auth_manager=auth_manager)

    match = re.search(r'playlist/([a-zA-Z0-9]+)', SPOTIFY_PLAYLIST)
    playlist_id = match.group(1) if match else SPOTIFY_PLAYLIST

    print("Fetching Spotify tracks...")
    tracks = get_spotify_tracks(sp, playlist_id)
    print(f"Found {len(tracks)} tracks.")

    yt = youtube_authenticate()
    yt_playlist_title = f"Imported from Spotify - {playlist_id}"
    yt_playlist_id = create_youtube_playlist(yt, yt_playlist_title, description="Imported via script")
    print("YouTube playlist created:", yt_playlist_title)

    added = 0
    for i, track in enumerate(tracks, start=1):
        q = best_query(track)
        items = youtube_search_video(yt, q, max_results=MAX_SEARCH_RESULTS)
        chosen = None
        for item in items:
            vid = item['id']['videoId']
            title = item['snippet']['title'].lower()
            if "live" in title or "acoustic" in title:
                continue
            chosen = vid
            break
        if not chosen and items:
            chosen = items[0]['id']['videoId']
        if chosen:
            add_video_to_playlist(yt, yt_playlist_id, chosen)
            added += 1
            print(f"{i}/{len(tracks)} added: {track['title']} - {track['artists']}")
            time.sleep(0.5)
        else:
            print(f"{i}/{len(tracks)} NOT FOUND: {track['title']} - {track['artists']}")

    print(f"Done. Playlist: https://www.youtube.com/playlist?list={yt_playlist_id} ({added} videos added)")

if __name__ == "__main__":
    main()
