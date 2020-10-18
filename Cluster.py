
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from hdbscan import HDBSCAN
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift
from sklearn.cluster import DBSCAN
from sklearn.cluster import AffinityPropagation
from pandas.api.types import is_numeric_dtype
from sklearn.preprocessing import StandardScaler as Scaler


def num_encoder(database):
    Data = pd.read_csv(database, index_col=None)
    for column in Data:
        if not is_numeric_dtype(Data[column]):
            Data_1H = pd.factorize(Data[column])
            Data[column] = Data_1H[0]
            return Data


def cluster():
    n_clusters = 0
    Full_data = pd.read_csv('Total.csv')
    Full_data = Full_data.dropna(axis=1, how='all')
    Full_data = Full_data.dropna(axis=0, how='any')
    ID = Full_data['id']
    Mode = Full_data['mode']
    length = Full_data['duration_ms']
    Full_data = Full_data.drop(
        columns=['track', 'album_id', 'artist', 'id', 'mode'])
    Fdata = Full_data.values
    scaler = Scaler()
    data_u = scaler.fit_transform(Fdata)
    # pca_transf = PCA(0.8)
    # PCA_data = pca_transf.fit_transform(data_u)
    clusterer = AffinityPropagation(random_state=None, preference=-400)
    # clusterer = HDBSCAN(min_cluster_size=20)
    # clusterer = MeanShift()
    labels = clusterer.fit_predict(data_u)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    labels.shape = (len(labels), 1)
    Full_data['cluster'] = labels + 1
    Full_data['id'] = ID
    Full_data['mode'] = Mode
    Full_data['duration_ms'] = length
    Full_data.sort_values(by='cluster')
    Full_data.to_csv('clustered.csv', index=False)
    # sns.pairplot(Full_data, hue="cluster", palette='YlGnBu')
    # plt.show()
    return n_clusters
