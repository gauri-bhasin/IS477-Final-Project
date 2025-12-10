import os
import re
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
USE_SPOTIFY_API = False
# ---------- SPOTIFY SECTION (RUN ONCE) ----------

def get_spotify_tracks():
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-private"
    )

    auth_url = sp_oauth.get_authorize_url()
    print("Go to this URL in your browser, log in, and approve the app:")
    print(auth_url)

    redirected_url = input("\nPaste the FULL redirect URL from your browser here:\n> ")
    code = sp_oauth.parse_response_code(redirected_url)
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]

    sp = spotipy.Spotify(auth=access_token)
    print("Spotify user:", sp.current_user()["display_name"])

    def get_artist_tracks(artist_name):
        print(f"Searching artist: {artist_name}")
        results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
        if not results['artists']['items']:
            print("No artist found:", artist_name)
            return pd.DataFrame()

        artist_id = results['artists']['items'][0]['id']
        print(f"Artist ID for {artist_name}: {artist_id}")

        albums = sp.artist_albums(artist_id, album_type='album,single', limit=50)
        album_ids = list({a['id'] for a in albums['items']})
        print(f"Found {len(album_ids)} albums/singles for {artist_name}")

        tracks = []

        for i, album_id in enumerate(album_ids, start=1):
            print(f"  [{artist_name}] Album {i}/{len(album_ids)}")
            album = sp.album(album_id)
            album_name = album['name']
            release_date = album['release_date']

            album_tracks = sp.album_tracks(album_id)
            track_items = album_tracks['items']

            ids = [t['id'] for t in track_items]
            if not ids:
                continue

            full_tracks = sp.tracks(ids)['tracks']

            for t in full_tracks:
                tracks.append({
                    "track_id": t["id"],
                    "track_name": t["name"],
                    "album_name": album_name,
                    "artist_name": artist_name,
                    "release_date": release_date,
                    "popularity": t.get("popularity", None)
                })

        return pd.DataFrame(tracks)

    artists = ["Taylor Swift", "Drake", "Ariana Grande", "Ed Sheeran"]

    dfs = []
    for a in artists:
        df = get_artist_tracks(a)
        dfs.append(df)

    spotify_df = pd.concat(dfs, ignore_index=True)
    spotify_df.to_csv("spotify_tracks.csv", index=False)
    print("Saved spotify_tracks.csv")
    return spotify_df


# Only fetch from Spotify if we DON'T already have the CSV
if os.path.exists("spotify_tracks.csv"):
    print("Loading existing spotify_tracks.csv...")
    spotify_df = pd.read_csv("spotify_tracks.csv")
else:
    print("spotify_tracks.csv not found, fetching from Spotify API...")
    spotify_df = get_spotify_tracks()

print("Spotify tracks shape:", spotify_df.shape)

# ---------- LYRICS SECTION (OPTIMIZED) ----------

def normalize_title(s):
    if pd.isna(s):
        return s
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"-.*$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# Normalize artist names in spotify_df
spotify_df["artist_norm"] = spotify_df["artist_name"].str.lower().str.strip()
spotify_df["title_norm"] = spotify_df["track_name"].apply(normalize_title)

# We'll only keep lyrics rows for these artists
target_artists = set(spotify_df["artist_norm"].unique())
print("Number of target artists:", len(target_artists))

usecols = ["title", "artist", "views", "tag", "year", "lyrics", "language_cld3", "id"]

print("Reading filtered lyrics from song_lyrics.csv (this may take a bit)...")
lyrics_df = pd.read_csv("song_lyrics.csv", usecols=usecols)

print("Initial lyrics_df shape:", lyrics_df.shape)

# Filter early to shrink data a LOT
lyrics_df = lyrics_df[lyrics_df["language_cld3"] == "en"]
lyrics_df = lyrics_df[lyrics_df["tag"].isin(["pop", "rap"])]
lyrics_df["artist_norm"] = lyrics_df["artist"].str.lower().str.strip()
lyrics_df = lyrics_df[lyrics_df["artist_norm"].isin(target_artists)]

print("Filtered lyrics_df shape:", lyrics_df.shape)

lyrics_df["title_norm"] = lyrics_df["title"].apply(normalize_title)

lyrics_dedup = (
    lyrics_df
    .sort_values("views", ascending=False)
    .drop_duplicates(subset=["artist_norm", "title_norm"])
)

print("Deduplicated lyrics_df shape:", lyrics_dedup.shape)

merged = spotify_df.merge(
    lyrics_dedup[["artist_norm", "title_norm", "lyrics", "tag", "year", "views", "id"]],
    on=["artist_norm", "title_norm"],
    how="left"
)

print("Merged shape:", merged.shape)

merged.to_csv("spotify_with_lyrics.csv", index=False)
print("Saved spotify_with_lyrics.csv")
