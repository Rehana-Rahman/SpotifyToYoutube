# Spotify to YouTube Playlist Transfer

A Python tool that automatically transfers your Spotify playlists to YouTube, saving you from manually searching and adding each song.

## Overview

This script takes all the songs from a Spotify playlist and recreates the same playlist on YouTube automatically. No more copying and pasting song names or spending hours rebuilding playlists on different platforms.

## How It Works

1. **Connect to Spotify** - Uses your developer app credentials to access your chosen playlist
2. **Extract playlist data** - Grabs all song titles and artists from the Spotify playlist  
3. **Search on YouTube** - Automatically searches for each song and finds the best matching video
4. **Create YouTube playlist** - Makes a new playlist on your YouTube account
5. **Add all videos** - Populates the playlist with all found videos

## Requirements

- Python 3
- Spotify Developer account (for client ID and secret)
- Google account with YouTube access
- YouTube Data API enabled in Google Cloud Console

### Python Dependencies

```
pip install spotipy google-auth-oauthlib google-api-python-client requests
```

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/Rehana-Rahman/spotify-to-youtube-transfer.git
cd spotify-to-youtube-transfer
```

### 2. Install Dependencies

```
pip install spotipy google-auth-oauthlib google-api-python-client requests
```

### 3. Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app
3. Copy your Client ID and Client Secret
4. Add redirect URI: `http://127.0.0.1:8888/callback`

**Note for Termux/Mobile users:** If you encounter redirect URI issues on mobile, you can also use `http://localhost:8888/callback` as an alternative.

### 4. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the YouTube Data API v3
3. Create OAuth 2.0 client ID credentials
4. Download the `client_secrets.json` file
5. Place it in the project directory

### 5. Configure the Script

Update the Python script with your Spotify credentials:

```
SPOTIFY_CLIENT_ID = 'your_client_id_here'
SPOTIFY_CLIENT_SECRET = 'your_client_secret_here'
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'
```

## Usage

```
python spotify_to_youtube.py
```

1. The script will provide a Spotify login URL - open it in your browser, authorize the app, then copy the redirect URL back to the terminal
2. Next, it will open a Google login URL - authorize YouTube access
3. Enter your Spotify playlist URL or ID when prompted
4. Watch as your playlist gets recreated on YouTube automatically

## Notes & Tips

- **Security**: This tool uses OAuth tokens only - your passwords are never stored
- **Mobile/Termux users**: The script works directly in Termux without additional tools needed
- **Video matching**: The script tries to find official videos but may occasionally select covers or live versions
- **Search accuracy**: You can adjust the number of search results checked per song in the script settings

## Why This Project Exists

Manually copying playlists between platforms is tedious and time-consuming. This tool instantly transfers your favorite Spotify playlists to YouTube, plus it's a great example of working with multiple APIs in Python.

## License

Feel free to use, modify, and share this project. Just remember:
- Don't commit your API credentials (`client_secrets.json`, Spotify client ID/secret) to public repositories
- Keep your sensitive files private
- Consider using environment variables for credentials

---

**Note**: This project is for educational and personal use. Make sure to comply with both Spotify and YouTube's terms of service when using their APIs.
```
