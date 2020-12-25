import numpy as np
import pandas as pd
import collections
import Data_Collector as DC
import Cluster as CT
import Song_NN_class as NN
import Playlist_Creator as PC
import path_finder as PF
ms = DC.map_songs
mp = DC.map_playlist
f = DC.get_related
artist_1 = ''    # enter first artist name
end_1 = ''     # enter first artist id
artist_2 = ''    # enter second artist name
end_2 = ''     # enter second artist id
playlist = artist_1 + ' to ' + artist_2
PF.path_points(end_1, end_2)
DF = pd.read_csv('path_list.csv')
a = list(set(DF['id'].values))
b = f(a, n=1)
b = [item for item, count in collections.Counter(
    b).items() if count > 1]
a = list(set(b))
print(len(a))
c = pd.DataFrame(a, columns=['id'])
c.to_csv('tracklist.csv', index=False)
h = pd.read_csv('tracklist.csv')
a = list(h['id'].values)
arq = 'Total ' + playlist
ms(a, arquivo=arq)
n_clusters, score = CT.cluster(playlist)
print(n_clusters, '\n', score)
NN.Classifier()
CT.reassigner(playlist)
CT.list_spliter(playlist)
PC.create_playlists(n_clusters, playlist)
