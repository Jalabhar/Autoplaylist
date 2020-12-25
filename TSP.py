import numpy as np

def TSPCF(x, distances):
    rota = list(x)
    total = 0
    for k in range(len(x)):
        origem = int(x[k - 1])
        destino = int(x[k])
        total += distances[origem][destino]
    return total


