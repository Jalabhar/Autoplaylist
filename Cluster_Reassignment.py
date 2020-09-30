import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def reassigner(source):
    data = pd.read_csv('song_preds.csv')
    base_cluster = pd.read_csv('cluster_limpo.csv')
    Full_data_cluster = pd.read_csv('Total_clustered.csv')
    base_cluster['cluster'] = data['predicted_cluster']
    base_cluster['probs'] = data['predicted_prob']
    Full_data_cluster['cluster'] = data['predicted_cluster']
    Full_data_cluster['probs'] = data['predicted_prob']
    base_cluster = base_cluster[base_cluster['probs'] >= .9]
    Full_data_cluster = Full_data_cluster[Full_data_cluster['probs'] >= .9]
    base_cluster.to_csv('Clean_NN_' + source + '.csv', index=False)
    Full_data_cluster.to_csv('Full_NN_' + source + '.csv', index=False)
