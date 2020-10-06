import pandas as pd


def list_spliter(source):
    Data = pd.read_csv('Clean_NN_' + source + '.csv')
    for i in range(max(Data['cluster']) + 1):
        Dados = Data[Data['cluster'] == i]
        Dados = Dados.nlargest(100, 'probs')
        k = str(i)
        file = source + k + '.csv'
        if len(Dados.values) > 10:
            Dados.to_csv(file, index=False)
