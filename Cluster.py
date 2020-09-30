
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from hdbscan import HDBSCAN
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AffinityPropagation
from pandas.api.types import is_numeric_dtype
from sklearn.preprocessing import MinMaxScaler
sns.set()


def num_encoder(database):
    Data = pd.read_csv(database, index_col=None)
    for column in Data:
        if not is_numeric_dtype(Data[column]):
            Data_1H = pd.factorize(Data[column])
            Data[column] = Data_1H[0]
            return Data


def cluster():
    Full_data = pd.read_csv('Total.csv')
    FD = Full_data
    try:
        Full_data = Full_data.drop('track_number', axis=1)
    except:
        pass
    try:
        Full_data = Full_data.drop('id', axis=1)
    except:
        pass
    try:
        Full_data = Full_data.drop('uri', axis=1)
    except:
        pass
    try:
        Full_data = Full_data.drop('popularity', axis=1)
    except:
        pass
    data = pd.read_csv('Total limpo.csv')
    scaler = MinMaxScaler()
    data_u = scaler.fit_transform(data)
    # pca_transf = PCA(0.8)
    # PCA_data = pca_transf.fit_transform(data_u)
    clusterer = AffinityPropagation(preference=-5, random_state=None)
    # clusterer = HDBSCAN()
    labels = clusterer.fit_predict(data_u)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    labels.shape = (len(labels), 1)
    Full_data['cluster'] = labels + 1
    data['cluster'] = labels + 1
    FD['cluster'] = labels + 1
    noiseless_Data = data[data['cluster'] != 0]
    Full_noiseless = FD[FD['cluster'] != 0]
    Full_data.sort_values(by='cluster')
    data.sort_values(by='cluster')
    data.sort_values(by='cluster')
    noiseless_Data.sort_values(by='cluster')
    noiseless_Data.to_csv('noiseless_cluster.csv', index=False)
    Full_noiseless.to_csv('Full_noiseless_cluster.csv', index=False)
    Full_data.to_csv('clustered.csv', index=False)
    FD.to_csv('Total_clustered.csv', index=False)
    # Data = Data.drop(columns=['artist'])
    data.to_csv('cluster_limpo.csv', index=False)
    print(n_clusters)
    sns.pairplot(data, hue="cluster", palette='YlGnBu')
    # sns.scatterplot(Data['energy'], Data['cluster'],
    #                 hue=Data['artist'], palette='magma', legend=None)
    # f, ax = plt.subplots(figsize=(11, 9))
    # plt.savefig('cluster.jpg', dpi=300)
    plt.show()
    return n_clusters
