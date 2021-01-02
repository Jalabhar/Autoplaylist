import spotipy
# import modin.pandas as mpd
import pandas as pd
import spotipy.util as util
import spotipy.oauth2 as oauth
import spotipy.client
from sklearn.preprocessing import StandardScaler as Scaler
import numpy as np
import scipy.spatial as spy
from sort_playlist import reorder
Client_ID = '11b38cefc27c4e399f30c4fbc4bd5f68'
Client_Secret = '1acfedb043d644f48f3cf403e1995778'
username = 'mat.nob'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
scope = 'playlist-modify-public'
credentials = oauth.SpotifyClientCredentials(Client_ID, Client_Secret)


def chunkify(lst, n):
    L = [lst[i::n] for i in range(n)]
    return L


def create_playlists(n, name, Creator='Jalabhar', max_duration=12.0, min_duration=0.0):
    token = util.prompt_for_user_token(username=username,
                                       scope=scope,
                                       client_id=Client_ID,
                                       client_secret=Client_Secret,
                                       redirect_uri=SPOTIPY_REDIRECT_URI)
    existing_playlists = pd.read_csv('playlist register.csv')
    sp = spotipy.Spotify(auth=token)
    lid = []
    names = []
    id_list = []
    for i in range(n):
        k = str(i + 1)
        Name = Creator + "'s " + name + ' ' + k
        file_source = Name + '.csv'
        print(file_source)
        try:
            tracks_database = pd.read_csv(file_source)
            if len(tracks_database.values) > 0:
                tracks_database = sparser(tracks_database)
                tracks_database = reorder(tracks_database)
                tracks_database['total time'] = tracks_database['duration_ms'].cumsum(
                ) / 3600000.0
                running_time = tracks_database['total time'].values
                if len(running_time) > 0 and running_time[-1] >= min_duration:
                    tracks_database = tracks_database[tracks_database['total time']
                                                      <= max_duration]
                    tracks_id = list(tracks_database['id'])
                    if Name not in existing_playlists['playlist_name'].values:
                        new_list = sp.user_playlist_create(
                            username, name=Name, )
                        list_id = new_list['id']
                        L = len(tracks_id)
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
                        id_list.append(list_id)
                    else:
                        plist = existing_playlists[existing_playlists['playlist_name'] == Name]
                        ID_list = plist['playlist_id'].values
                        pl_id = ID_list[0]
                        id_list.append(pl_id)
                        t_id = tracks_id[:100]
                        tracks_id = tracks_id[100:]
                        sp.playlist_replace_items(pl_id, t_id)
                        while len(tracks_id) > 0:
                            t_id = tracks_id[:50]
                            tracks_id = tracks_id[50:]
                            sp.user_playlist_add_tracks(
                                Client_ID, pl_id, t_id)
                tracks_database.to_csv(file_source)
            else:
                pass
        except:
            pass
    df = pd.DataFrame(lid, columns=['playlist_id'])
    df['playlist_name'] = names
    # df2 = pd.read_csv('playlist register.csv')
    df2 = existing_playlists.append(df)
    df2.to_csv('playlist register.csv', index=False)
    return id_list


def sparser(dataset):
    d = dataset.drop(columns=['id', 'artist', 'cluster', 'probs'])
    scaler = Scaler()
    scaled_d = scaler.fit_transform(d)
    # scaled_d = scaled_d[-20:]
    dist = np.triu(spy.distance_matrix(scaled_d, scaled_d))
    scaled_dist = scaler.fit_transform(dist)
    arg = np.max(scaled_dist)
    indexes = np.argwhere(dist > (.25 * arg))
    I = indexes.T
    keep = list(set(I[0]))
    sparse_d = dataset.iloc[keep, :]
    sparse_d = sparse_d.sort_values('probs', ascending=False)
    return sparse_d
