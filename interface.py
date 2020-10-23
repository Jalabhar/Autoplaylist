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
playlist = 'source playlist name'
mp('source playlist id', 'source playlist owner', playlist)
DF = pd.read_csv(playlist + '.csv')
a = list(set(DF['artist_id'].values))
# # b = f(a)
# # b = [item for item, count in collections.Counter(
# #     b).items() if count > min(5, (int(1 + .15 * len(a))))]
# # # print(b)
# # a.extend(b)
# # a = list(set(a))
arq = 'Total ' + playlist
ms(a, arquivo=arq)
n = CT.cluster(playlist)
print(n)
NN.Classifier()
CT.reassigner(playlist)
CT.list_spliter(playlist)
PC.create_playlists(n, playlist)
