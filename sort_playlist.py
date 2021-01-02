import benchmarks as bm
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import seaborn as sns
import PSO
# import modin.pandas as mpd
import pandas as pd
from sklearn.preprocessing import MinMaxScaler as Scaler
from scipy.spatial import distance_matrix


def reorder(data):
    F = bm.TSPCF
    scaler = Scaler()
    c_data = data.drop(
        columns=['cluster', 'id', 'artist', 'duration_ms', 'time_signature'])
    c_data = scaler.fit_transform(c_data)
    dist = distance_matrix(c_data, c_data)
    M = 2 * np.max(dist)
    np.fill_diagonal(dist, M)
    L = len(c_data)
    limite = [L * [0], L * [(L - 1)]]
    p = L * [1]
    A, B, C, D = PSO.run(
        F, 1000, limite, 5, 10, dist, passo=p, permut=True)
    edge_lengths = [dist[-1][0]]
    for i in range(len(A) - 1):
        d = dist[i][i + 1]
        edge_lengths.append(d)
    m_d = max(edge_lengths)
    M = edge_lengths.index(m_d)
    A = np.append(A[M:], A[:M])
    B -= m_d
    try:
        L_range = list(range(len(A)))
        N_order = [list(A).index(val) for val in L_range]
        data['new_order'] = N_order
        data = data.sort_values(by='new_order')
        dataset = data.drop(columns=['new_order'])
        try:
            dataset = data.drop(columns=['Unnamed: 0'])
        except:
            pass
        return dataset
    except:
        return data
