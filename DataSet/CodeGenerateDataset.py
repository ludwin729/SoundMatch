import csv
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

client_id = "3dee3d8ea57c4586b454a51dc1b78a88"
client_secret = "edcf663c85ce4864a49c24acd8b7915a"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = "Axekran"
playlist_link=input("Enter the playlist link: ")
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

def get_playlist_tracks():
    sp_playlist = sp.user_playlist_tracks(username, playlist_id=playlist_URI)
    tracks = sp_playlist['items']
    while sp_playlist['next']:
        sp_playlist = sp.next(sp_playlist)
        tracks.extend(sp_playlist['items'])

    return tracks

def get_list_songs(tracks_ids):
    list_listas=[]

    for song in tracks_ids:

        name_track = song["track"]["name"]
        artist_track = song["track"]["artists"][0]["name"]
        uri_track = song["track"]["uri"]
        album_track=song["track"]["album"]["name"]
        #PARA SABER EL GENERO
        result=sp.search(artist_track)
        track=result['tracks']['items'][0]
        artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
        genre=str(artist["genres"])
        genre=re.sub("\[|\'|\]","",genre)
        #https://open.spotify.com/playlist/2JWzGt1rH97a4fyRqez8ZY?si=f2b2557c758845f1
        #AQUI TERMINA
        #OBTENCION DE LOS DATOS DEL TEMPO Y POPULARIDAD
        features = sp.audio_features(uri_track)[0]
        tempo=round(features["tempo"])
        popularity=song["track"]["popularity"]
        urlImage = song["track"]["album"]["images"][2]["url"]
        lista = [name_track, artist_track, uri_track,popularity,tempo,genre,urlImage,album_track]
        list_listas.append(lista)
        #print(json.dumps(song,indent=2))

    return list_listas


track_list  = get_playlist_tracks()
list_songs  = get_list_songs(track_list)

headers=["name_track","artist_track","uri_track","popularity","tempo","genres","urlImage","album"]


#print(len(list_songs))
#print(list_songs)

with open('Dataset.csv','w', newline='',encoding="utf-8") as csvfile:
    #creating  a csv writer object
    csvwriter = csv.writer(csvfile)
    #writing the fields
    csvwriter.writerow(headers)
    # writing the data rows
    csvwriter.writerows(list_songs)