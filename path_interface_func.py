import numpy as np
# import modin.pandas as mpd
import spotipy
import pandas as pd
import collections
import Data_Collector as DC
import Cluster as CT
import Song_NN_class as NN
import Playlist_Creator_bot as PC
import path_finder as PF
from spotipy.oauth2 import SpotifyClientCredentials
ms = DC.map_songs
mp = DC.map_playlist
f = DC.get_related


def build_path(artist_1, artist_2, User='Jalabhar', running_time=12.0, cycle=False):
    client_id = '11b38cefc27c4e399f30c4fbc4bd5f68'
    client_secret = '1acfedb043d644f48f3cf403e1995778'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    q_1 = sp.search(q='artist:' + artist_1, type='artist')
    q_2 = sp.search(q='artist:' + artist_2, type='artist')
    id_1 = q_1['artists']['items'][0]['id']
    id_2 = q_2['artists']['items'][0]['id']
    playlist = artist_1 + ' to ' + artist_2
    PF.Path_Points(id_1, id_2, cycle)
    DF = pd.read_csv('path_list.csv')
    a = list(set(DF['id'].values))
    b = f(a, n=1)
    b = [item for item, count in collections.Counter(
        b).items() if count > 1]
    a.extend(b)
    a = list(set(a))
    print(len(a))
    c = pd.DataFrame(a, columns=['id'])
    c.to_csv('tracklist.csv', index=False)
    # h = pd.read_csv('tracklist.csv')
    # a = list(h['id'].values)
    arq = 'Total ' + playlist
    ms(a, arquivo=arq)
    n_clusters, score = CT.cluster(playlist)
    print(n_clusters, '\n', score)
    NN.Classifier()
    CT.reassigner(playlist)
    CT.list_spliter(playlist, author=User)
    playlist_Names = PC.create_playlists(
        n_clusters, playlist, User, max_duration=running_time)
    return playlist_Names
