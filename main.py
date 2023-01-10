from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

which_year = input("which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
past_billboard = f"https://www.billboard.com/charts/hot-100/{which_year}"
response = requests.get(past_billboard)
soup = BeautifulSoup(response.text, "html.parser")

songs = []
list_song_elements = soup.find_all(class_="o-chart-results-list-row")
for element in list_song_elements:
    rank_element = element.find(class_="c-label")
    rank = rank_element.getText().strip()
    title_element = element.find(class_="c-title")
    title = title_element.getText().strip()
    label_element = element.select_one("span.c-label.lrv-u-display-block")
    label = label_element.getText().strip()
    songs.append((rank, title, label))

print(songs)

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

songs_URI = []

# TODO 3-1: Using the Spotipy documentation, create a list of Spotify song URIs for the list of song names you
# TODO 3-1 ctd: found from step 1 (scraping billboard 100).
# TODO 4-1: Using the Spotipy documentation, create a new private playlist with the name "YYYY-MM-DD Billboard 100",
# TODO 4-1 ctd: where the date is the date you inputted in step 1.
# TODO 4-2: Add each of the songs found in Step 3 to the new playlist.
