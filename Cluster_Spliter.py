import pandas as pd


def list_spliter(source):
    Data = pd.read_csv('reassigned' + source + '.csv')
    for i in range(max(Data['cluster'].values)):
        Dados = Data[Data['cluster'] == i + 1]
        Dados = Dados.nlargest(150, 'probs')
        k = str(i + 1)
        Name = "Jalabhar's " + source + ' ' + k
        file = Name + '.csv'
        Dados.to_csv(file, index=False)
