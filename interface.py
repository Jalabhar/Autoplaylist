import numpy as np
import pandas as pd
import collections
import Data_Collector as DC
import Cluster as CT
import Song_NN_class as NN
import Playlist_Creator as PC
ms = DC.map_songs
mp = DC.map_playlist
f = DC.get_related
playlist = 'Instrumental Madness'
playlist_owner = None
playlist_id = None
#  não entrar com playlist_ID sem user
mp(playlist, playlist_owner, playlist_id)
DF = pd.read_csv(playlist + '.csv')
a = list(set(DF['artist_id'].values))
DF = pd.read_csv('tracklist.csv')
a = list(set(DF['id'].values))
b = f(a, n=1)
b = [item for item, count in collections.Counter(
    b).items() if count > 1]
a = list(set(b))
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
CT.list_spliter(playlist)
PC.create_playlists(n_clusters, playlist)
