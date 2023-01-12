from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

which_year = input("which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
past_billboard = f"https://www.billboard.com/charts/hot-100/{which_year}"
response = requests.get(past_billboard)
soup = BeautifulSoup(response.text, "html.parser")

songs = []
list_song_elements = soup.find_all(class_="o-chart-results-list-row")
for element in list_song_elements:
    title_element = element.find(class_="c-title")
    title = title_element.getText().strip()
    label_element = element.select_one("span.c-label.lrv-u-display-block")
    label = label_element.getText().strip()
    songs.append((title, label))

scope = "playlist-modify-private playlist-read-private user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

songs_URIs = []
for song in songs:
    track_dict = sp.search(q=f"track:{song[0]} artist:{song[1]}", type="track")
    track_items = track_dict["tracks"]["items"]
    if not track_items: continue
    track_URI = track_items[0]['uri']
    songs_URIs.append(track_URI)

playlist = sp.user_playlist_create(user=sp.current_user()["id"], name=f"{which_year} Billboard 100", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=songs_URIs)
print(f"Your playlist can be found at {playlist['external_urls']['spotify']}")

# TODO: comments
