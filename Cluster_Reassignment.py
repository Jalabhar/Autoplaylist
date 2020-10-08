import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def reassigner(source):
    data = pd.read_csv('song_preds.csv')
    base_cluster = pd.read_csv('clustered.csv')
    p = 3.0 / (np.max(data['predicted_cluster'].values))
    base_cluster['cluster'] = data['predicted_cluster']
    base_cluster['probs'] = data['predicted_prob']
    base_cluster = base_cluster[base_cluster['probs'] >= p]
    base_cluster.to_csv('reassigned ' + source + '.csv', index=False)
