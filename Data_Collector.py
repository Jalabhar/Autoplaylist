import spotipy
import time
import pandas as pd
import numpy as np
import json
import csv
from spotipy.oauth2 import SpotifyClientCredentials
# To access authorised Spotify data


def audio_features(spotify_albums, album, sp):
    # Add new key-values to store audio features
    spotify_albums[album]['acousticness'] = []
    spotify_albums[album]['duration'] = []
    spotify_albums[album]['danceability'] = []
    spotify_albums[album]['energy'] = []
    spotify_albums[album]['instrumentalness'] = []
    spotify_albums[album]['liveness'] = []
    spotify_albums[album]['loudness'] = []
    spotify_albums[album]['speechiness'] = []
    spotify_albums[album]['tempo'] = []
    spotify_albums[album]['valence'] = []
    spotify_albums[album]['popularity'] = []
    spotify_albums[album]['time_signature'] = []
    spotify_albums[album]['key'] = []
    # create a track counter
    track_count = 0
    for track in spotify_albums[album]['id']:
        try:
            # pull audio features per track
            features = sp.audio_features(track)
            # analysis = sp.audio_analysis(track)
            # Append to relevant key-value
            spotify_albums[album]['acousticness'].append(
                features[0]['acousticness'])
            spotify_albums[album]['duration'].append(
                features[0]['duration_ms'])
            spotify_albums[album]['danceability'].append(
                features[0]['danceability'])
            spotify_albums[album]['energy'].append(features[0]['energy'])
            spotify_albums[album]['instrumentalness'].append(
                features[0]['instrumentalness'])
            spotify_albums[album]['liveness'].append(features[0]['liveness'])
            spotify_albums[album]['loudness'].append(features[0]['loudness'])
            spotify_albums[album]['speechiness'].append(
                features[0]['speechiness'])
            spotify_albums[album]['valence'].append(features[0]['valence'])
            spotify_albums[album]['tempo'].append(features[0]['tempo'])
            spotify_albums[album]['time_signature'].append(
                features[0]['time_signature'])
            spotify_albums[album]['key'].append(
                features[0]['key'])
            # popularity is stored elsewhere
            data = sp.track(track)
            spotify_albums[album]['popularity'].append(data['popularity'])
            track_count += 1
        except:
            pass


def albumSongs(uri, spotify_albums, sp, album_names, album_count):
    album = uri  # assign album uri to a_name

    spotify_albums[album] = {}  # Creates dictionary for that specific album

# Create keys-values of empty lists inside nested dictionary for album
    spotify_albums[album]['album'] = []  # create empty list
    spotify_albums[album]['track_number'] = []
    spotify_albums[album]['id'] = []
    spotify_albums[album]['name'] = []
    spotify_albums[album]['uri'] = []

    tracks = sp.album_tracks(album)  # pull data on album tracks
    for n in range(len(tracks['items'])):  # for each song track
        # append album name tracked via album_count
        spotify_albums[album]['album'].append(album_names[album_count])
        spotify_albums[album]['track_number'].append(
            tracks['items'][n]['track_number'])
        spotify_albums[album]['id'].append(tracks['items'][n]['id'])
        spotify_albums[album]['name'].append(tracks['items'][n]['name'])
        spotify_albums[album]['uri'].append(tracks['items'][n]['uri'])
    return spotify_albums


def map_songs(lista, arquivo='Total'):
    client_id = '11b38cefc27c4e399f30c4fbc4bd5f68'
    client_secret = '1acfedb043d644f48f3cf403e1995778'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    albums = []
    for artist_id in lista:
        results = sp.artist_albums(
            artist_id, album_type='album', country='BR')
        r = results['items']
        # time.sleep(1)
        for i in range(len(r)):
            albums.append([r[i]['artists'][0]['id'],
                           r[i]['artists'][0]['name'],
                           r[i]['id'], r[i]['name']])
        while results['next']:
            results = sp.next(results)
            r = results['items']
            for i in range(len(r)):
                albums.append([r[i]['artists'][0]['id'],
                               r[i]['artists'][0]['name'],
                               r[i]['id'], r[i]['name']])
    Albums = pd.DataFrame(
        albums, columns=['artist id', 'artist name', 'album id', 'album name'])
    # Albums = Albums.rename()
    album_ids = list(Albums['album id'])
    # print(len(album_ids))
    data = pd.DataFrame()
    tr = []
    for album_id in album_ids:
        t = sp.album_tracks(album_id, limit=50, market='BR')
        tr.extend(t['items'])
        # time.sleep(1)
    # print(len(tr))
    # print(tr[0].keys())
    for i in range(len(tr)):
        artist = tr[i]['artists'][0]['name']
        # print(artist)
        track = tr[i]['name']
        album_id = tr[i]['id']
        duration = tr[i]['duration_ms']
        features = sp.audio_features(album_id)
        Features = pd.DataFrame(features)
        Features['artist'] = artist
        Features['track'] = track
        Features['album_id'] = album_id
        data = data.append(Features, ignore_index=True)
        if i % 50 == 49:
            time.sleep(1)
    data = data.drop(columns=['type', 'uri', 'track_href', 'analysis_url'])
    data = data.drop_duplicates(subset=['track'])
    data = data[~data['track'].str.contains(
        'live|Live|commentary|Commentary|version|Version|Edition|edition')]
    data = data[data['liveness'] < 0.5]
    Data = data[data['speechiness'] < 0.8]
    file = arquivo + '.csv'
    Data.to_csv(file, index=False)


def chunkify(lst, n):
    L = [lst[i::n] for i in range(n)]
    return L


def map_playlist(playlist_ID, user, arquivo):
    sleep_min = 0.5
    sleep_max = 1.0
    request_count = 0
    client_id = '11b38cefc27c4e399f30c4fbc4bd5f68'
    client_secret = '1acfedb043d644f48f3cf403e1995778'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    INFO = pd.DataFrame()
    tracks = getPlaylistTrackIDs(user, playlist_ID)
    playlist_info = []
    for song_id in tracks:
        # pull audio features per track
        meta = sp.track(song_id)
        features = sp.audio_features(song_id)
        # analysis = sp.audio_analysis(track)
        # Append to relevant key-value
        name = meta['name']
        album = meta['album']['name']
        artist = meta['album']['artists'][0]['name']
        artist_id = meta['album']['artists'][0]['id']
        release_date = meta['album']['release_date']
        length = meta['duration_ms']
        popularity = meta['popularity']
        acousticness = features[0]['acousticness']
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        instrumentalness = features[0]['instrumentalness']
        liveness = features[0]['liveness']
        loudness = features[0]['loudness']
        speechiness = features[0]['speechiness']
        tempo = features[0]['tempo']
        time_signature = features[0]['key']
        key = features[0]['time_signature']
        track = [name, album, artist, artist_id, release_date, length, popularity,
                 acousticness, danceability, energy, instrumentalness,
                 liveness, loudness, speechiness, tempo, time_signature, key]
        labels = ['name', 'album', 'artist', 'artist_id', 'release_date', 'length', 'popularity',
                  'acousticness', 'danceability', 'energy', 'instrumentalness',
                  'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'key']
        playlist_info.append(track)
    INFO = pd.DataFrame(playlist_info, columns=labels)
    INFO.to_csv(arquivo + '.csv', index=False)
    # desc = INFO.describe()


def getPlaylistTrackIDs(user, playlist_id):
    client_id = '11b38cefc27c4e399f30c4fbc4bd5f68'
    client_secret = '1acfedb043d644f48f3cf403e1995778'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])

    return ids
