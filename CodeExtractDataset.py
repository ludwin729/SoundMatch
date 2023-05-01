import csv
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

client_id = "a3365dba42c346b5bb077c1eb34061a8"
client_secret = "99175a3dd79346f9a9187ea730453dc8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

username = "roy reyes.01"
playlist_link = input("Enter the playlist link: ")
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

def get_playlist_tracks():
    sp_playlist = sp.user_playlist_tracks(username, playlist_id=playlist_URI)
    tracks = sp_playlist['items']
    while sp_playlist['next']:
        sp_playlist = sp.next(sp_playlist)
        tracks.extend(sp_playlist['items'])
    return tracks

def get_list_songs(tracks_ids):
    list_listas = []
    for song in tracks_ids:
        name_track = song["track"]["name"]
        artist_track = song["track"]["artists"][0]["name"]
        uri_track = song["track"]["uri"]
        # PARA SABER EL GÉNERO
        try:
            result = sp.search(artist_track)
            track = result['tracks']['items'][0]
            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
            genre = str(artist["genres"])
            genre = re.sub("\[|\'|\]", "", genre)
        except:
            genre = "Unknown"
        # OBTENCIÓN DE LOS DATOS DEL TEMPO Y POPULARIDAD
        try:
            features = sp.audio_features(uri_track)[0]
            tempo = round(features["tempo"])
        except:
            tempo = "Unknown"
        popularity = song["track"]["popularity"]
        lista = [name_track, artist_track, uri_track, popularity, tempo, genre]
        list_listas.append(lista)
    return list_listas

track_list = get_playlist_tracks()
list_songs = get_list_songs(track_list)

headers = ["name_track", "artist_track", "uri_track", "popularity", "tempo", "genres"]

with open('Dataset.csv', 'w', newline='', encoding="utf-8") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(headers)
    # writing the data rows
    csvwriter.writerows(list_songs)
