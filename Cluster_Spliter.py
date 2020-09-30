import pandas as pd


def list_spliter(source):
    Data = pd.read_csv('Clean_NN_' + source + '.csv')
    All_data = pd.read_csv('Full_NN_' + source + '.csv')
    # Data = pd.read_csv('All_reclustered_limpo.csv')
    # All_data = pd.read_csv('All_reclustered.csv')
    All_data = All_data.drop_duplicates('name')
    for i in range(max(Data['cluster']) + 1):
        Dados = Data[Data['cluster'] == i]
        Dados = Dados.nlargest(100, 'probs')
        T_Dados = All_data[All_data['cluster'] == i]
        T_Dados = T_Dados.nlargest(100, 'probs')
        k = str(i)
        file = source + k + '.csv'
        T_file = 'Complete' + source + k + '.csv'
        if len(Dados.values) > 10:
            Dados.to_csv(file, index=False)
            T_Dados.to_csv(T_file, index=False)
