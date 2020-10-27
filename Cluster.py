
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import AffinityPropagation
from pandas.api.types import is_numeric_dtype
from sklearn.preprocessing import StandardScaler as Scaler
from sklearn.metrics import silhouette_score


def num_encoder(database):
    Data = pd.read_csv(database, index_col=None)
    for column in Data:
        if not is_numeric_dtype(Data[column]):
            Data_1H = pd.factorize(Data[column])
            Data[column] = Data_1H[0]
            return Data


def cluster(playlist):
    arq = 'Total ' + playlist + '.csv'
    n_clusters = 0
    Full_data = pd.read_csv(arq)
    Full_data = Full_data.dropna(axis=1, how='all')
    Full_data = Full_data.dropna(axis=0, how='any')
    ID = Full_data['id']
    Mode = Full_data['mode']
    length = Full_data['duration_ms']
    artist = Full_data['artist']
    Full_data = Full_data.drop(
        columns=['track', 'album_id', 'artist', 'id', 'mode'])
    Fdata = Full_data.values
    scaler = Scaler()
    data_u = scaler.fit_transform(Fdata)
    clusterer = AffinityPropagation(random_state=None, preference=-450)
    # clusterer = HDBSCAN(min_cluster_size=20)
    # clusterer = MeanShift()
    labels = clusterer.fit_predict(data_u)
    score = silhouette_score(data_u, labels)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    labels.shape = (len(labels), 1)
    Full_data['cluster'] = labels + 1
    Full_data['id'] = ID
    Full_data['mode'] = Mode
    Full_data['artist'] = artist
    Full_data['duration_ms'] = length
    # Full_data.sort_values(by='cluster')
    Full_data.to_csv('clustered.csv', index=False)
    # sns.pairplot(Full_data, hue="cluster", palette='YlGnBu')
    # plt.show()
    return n_clusters, score


def list_spliter(source):
    Data = pd.read_csv('reassigned ' + source + '.csv')
    for i in range(max(Data['cluster'].values)):
        Dados = Data[Data['cluster'] == i + 1]
        k = str(i + 1)
        Name = "Jalabhar's " + source + ' ' + k
        file = Name + '.csv'
        Dados.to_csv(file, index=False)


def reassigner(source):
    data = pd.read_csv('song_preds.csv')
    base_cluster = pd.read_csv('clustered.csv')
    base_cluster['cluster'] = data['predicted_cluster']
    base_cluster['probs'] = data['predicted_prob']
    base_cluster = base_cluster.sort_values(by='probs')
    base_cluster = base_cluster.groupby(by=['artist', 'cluster']).head(8)
    base_cluster = base_cluster.sort_values(by='probs')
    base_cluster.to_csv('reassigned ' + source + '.csv', index=False)
