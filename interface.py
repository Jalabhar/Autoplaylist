import Data_Collector as dc
import Related_Finder as gr
import numpy as np
import pandas as pd
import collections
import Cluster as CT
import Song_NN_class as NN
import Cluster_Reassignment as CR
import Cluster_Spliter as CS
import Playlist_Creator as PC
ms = dc.map_songs
mp = dc.map_playlist
f = gr.get_related
playlist = 'Ultimate Metal'
mp('37i9dQZF1DWXHwQpcoF2cC', 'Spotify', playlist)
DF = pd.read_csv(playlist + '.csv')
a = list(set(DF['artist_id'].values))
b = f(a)
b = [item for item, count in collections.Counter(
    b).items() if count > min(5, (int(1 + .15 * len(a))))]
# print(b)
a.extend(b)
a = list(set(a))
ms(a)
n = CT.cluster()
print(n)
NN.Classifier()
CR.reassigner(playlist)
CS.list_spliter(playlist)
PC.create_playlists(n, playlist)
