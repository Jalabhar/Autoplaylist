import Data_Collector as dc
import numpy as np
import pandas as pd
import collections
import Cluster as CT
import Song_NN_class as NN
import Playlist_Creator as PC
ms = dc.map_songs
mp = dc.map_playlist
f = dc.get_related
playlist = 'Ultimate Metal'
mp('37i9dQZF1DWXHwQpcoF2cC', 'Spotify', playlist)
DF = pd.read_csv(playlist + '.csv')
a = list(set(DF['artist_id'].values))
b = f(a, n=1)
# print(len(b))
b = [item for item, count in collections.Counter(
    b).items() if count > (int(.5 + .25 * len(a)))]
a.extend(b)
a = list(set(a))
c = pd.DataFrame(a)
c.to_csv('tracklist.csv')
# a = pd.read_csv('tracklist.csv')
# a = list(a[0].values)
arq = 'Total ' + playlist
ms(a, arquivo=arq)
n_clusters, score = CT.cluster(playlist)
print(n_clusters, '\n', score)
NN.Classifier()
CT.reassigner(playlist)
CT.list_spliter(playlist)
# n = 33
PC.create_playlists(n_clusters, playlist)
