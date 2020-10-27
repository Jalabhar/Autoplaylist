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
playlist = 'Swagger'
# playlist_owner = 'Spotify'
# playlist_id =
# não entrar com playlist_ID sem user
mp(playlist, user=None, playlist_ID=None)
DF = pd.read_csv(playlist + '.csv')
a = list(set(DF['artist_id'].values))
b = f(a, n=1)
b = [item for item, count in collections.Counter(
    b).items() if count > (int(.5 + .25 * len(a)))]
a.extend(b)
a = list(set(a))
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
