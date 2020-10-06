import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def reassigner(source, p=0.9):
    data = pd.read_csv('song_preds.csv')
    base_cluster = pd.read_csv('clustered.csv')
    base_cluster['cluster'] = data['predicted_cluster']
    base_cluster['probs'] = data['predicted_prob']
    base_cluster = base_cluster[base_cluster['probs'] >= p]
    base_cluster.to_csv('reassigned ' + source + '.csv', index=False)
