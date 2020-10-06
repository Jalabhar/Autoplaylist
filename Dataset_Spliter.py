import pandas as pd
Data = pd.read_csv('clustered.csv')
All_data = pd.read_csv('Total_clustered.csv')
All_data = All_data.drop_duplicates('name')
for i in range(max(Data['cluster']) + 1):
    Dados = Data[Data['cluster'] == i]
    k = str(i)
    file = 'Cluster_' + k + '.csv'
    Dados.to_csv(file, index=False)
for i in range(max(All_data['cluster']) + 1):
    T_Dados = All_data[All_data['cluster'] == i]
    k = str(i)
    T_file = 'Complete_Cluster_' + k + '.csv'
    T_Dados.to_csv(T_file, index=False)
