import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lxml
from bs4 import BeautifulSoup
import requests


ClientID="dacdb5ad0dbc4f37b8b8e9bd9a9cd60a"
ClientSecret="05f0d7c2dea647589ef2fd437f933136"
date=input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}

response=requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", headers=header)
BillBoard_web_page=response.text


soup=BeautifulSoup(BillBoard_web_page, "lxml")
titles=[]
ok=[]
title=soup.select("li ul li h3")
for songs in title:
    titles.append(songs.get_text(strip=True))
with open("songs.txt", "w", encoding="utf-8") as text:
    text.writelines(titles)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ClientID,
                                               client_secret=ClientSecret,
                                               redirect_uri="http://127.0.0.1:8888/callback",
                                               scope="playlist-modify-private",show_dialog=True,
                                               cache_path="token.txt",
                                                ))
user_id = sp.current_user()["id"]
print(user_id)

song_uris=[]
year=date.split("-")[0]
for song in titles:
    result=sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    print(song)
    try:
        uri=result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
