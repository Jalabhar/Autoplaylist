import spotipy
import pandas as pd
import spotipy.util as util
import spotipy.oauth2 as oauth
import spotipy.client
from sklearn.preprocessing import StandardScaler as Scaler
import numpy as np
import scipy.spatial as sp
Client_ID = 'your client id here'
Client_Secret = 'you client secret here'
username = 'your username here'
SPOTIPY_REDIRECT_URI = 'your redirect url here'
scope = 'playlist-modify-public'
credentials = oauth.SpotifyClientCredentials(Client_ID, Client_Secret)


def chunkify(lst, n):
    L = [lst[i::n] for i in range(n)]
    return L


token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=Client_ID,
                                   client_secret=Client_Secret,
                                   redirect_uri=SPOTIPY_REDIRECT_URI)


def create_playlists(n, name, max_duration=15.0, min_duration=1.0):
    sp = spotipy.Spotify(auth=token)
    lid = []
    names = []
    for i in range(n):
        k = str(i + 1)
        Name = "Jalabhar's " + name + ' ' + k
        file_source = Name + '.csv'
        try:
            tracks_database = pd.read_csv(file_source)
            tracks_database = sparser(tracks_database)
            # tracks_database = tracks_database[tracks_database['probs'] > .9]
            tracks_database['total time'] = tracks_database['duration_ms'].cumsum(
            ) / 3600000.0
            running_time = tracks_database['total time'].values
            if len(running_time) > 0 and running_time[-1] >= min_duration:
                tracks_database = tracks_database[tracks_database['total time'] <=
                                                  max_duration]
                new_list = sp.user_playlist_create(
                    username, name=Name, )
                list_id = new_list['id']
                tracks_id = list(tracks_database['id'])
                L = len(tracks_id)
                # DB = pd.DataFrame(columns=['playlist_ids'])
                if L > 10:
                    if L % 50 != 0.0:
                        n = 1 + int(L / 50)
                    else:
                        n = int(L / 50)
                    T = chunkify(tracks_id, n)
                    for chunk in T:
                        sp.user_playlist_add_tracks(
                            Client_ID, list_id, chunk)
                    lid.append(list_id)
                    names.append(Name)
        except FileNotFoundError:
            pass
    df = pd.DataFrame(lid, columns=['playlist_id'])
    df['playlist_name'] = names
    df2 = pd.read_csv('playlist register.csv')
    df2 = df2.append(df)
    df2.to_csv('playlist register.csv', index=False)


def sparser(dataset):
    d = dataset.drop(columns=['id', 'artist', 'cluster', 'probs'])
    scaler = Scaler()
    scaled_d = scaler.fit_transform(d)
    # scaled_d = scaled_d[-20:]
    dist = np.triu(sp.distance_matrix(scaled_d, scaled_d))
    scaled_dist = scaler.fit_transform(dist)
    arg = np.max(scaled_dist)
    # print(Max)
    indexes = np.argwhere(dist > (.5 * arg))
    I = indexes.T
    keep = list(set(I[0]))
    sparse_d = dataset.iloc[keep, :]
    sparse_d = sparse_d.sort_values('probs', ascending=False)
    return sparse_d
