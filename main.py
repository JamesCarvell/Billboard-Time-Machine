from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

FEATURING_ALTS = [" Featuring ", " X ", " x ", " & ", " Duet With ", " With ", " with "]

# Scrape top 100 songs from billboard.com for user input date
which_year = input("which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
past_billboard = f"https://www.billboard.com/charts/hot-100/{which_year}"
response = requests.get(past_billboard)
soup = BeautifulSoup(response.text, "html.parser")

songs = []
list_song_elements = soup.find_all(class_="o-chart-results-list-row")
for element in list_song_elements:
    track_element = element.find(class_="c-title")
    track_text = track_element.getText().strip()
    artist_element = element.select_one("span.c-label.lrv-u-display-block")
    artist_text = artist_element.getText().strip()
    songs.append((track_text, artist_text))

# Search Spotify for list of songs, and create new list of Spotify URIs
scope = "playlist-modify-private playlist-read-private user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

songs_URIs = []
for song in songs:
    track_dict = sp.search(q=f"track:{song[0]} artist:{song[1]}", type="track")
    track_items = track_dict["tracks"]["items"]
    if track_items:
        track_URI = track_items[0]["uri"]
        songs_URIs.append(track_URI)
        continue

    # Spotify won't take "Artist" + " Featuring " + "Other Artist", or any similar string, except for " AND "
    artists = song[1]
    for alt in FEATURING_ALTS:
        artists = artists.replace(alt, " AND ")
        track_dict = sp.search(q=f"track:{song[0]} artist:{artists}", type="track")
        track_items = track_dict["tracks"]["items"]
        if track_items:
            break
    if track_items:
        track_URI = track_items[0]["uri"]
        songs_URIs.append(track_URI)
        continue

    # Spotify doesn't like apostrophes
    track = song[0].replace("'", " ")
    track_dict = sp.search(q=f"track:{track} artist:{artists}", type="track")
    track_items = track_dict["tracks"]["items"]
    if track_items:
        track_URI = track_items[0]["uri"]
        songs_URIs.append(track_URI)
    else:
        print(f"Couldn't find {song}")

# Create Spotify Playlist with list of URIs
playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=f"{which_year} Billboard 100", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=songs_URIs)
print(f"Your playlist can be found at {playlist['external_urls']['spotify']}")

# TODO: DRY
