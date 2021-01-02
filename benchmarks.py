import numpy as np


def ackley(x):
    return -np.exp(-np.sqrt(0.5 * sum([i**2 for i in x]))) - \
        np.exp(0.5 * sum([np.cos(i) for i in x])) + 1 + np.exp(1)


def bukin(x):
    return 100 * np.sqrt(abs(x[1] - 0.01 * x[0]**2)) + 0.01 * abs(x[0] + 10)


def cross_in_tray(x):
    return round(
        -0.0001 * (abs(
            np.sin(x[0]) * np.sin(x[1]) * np.exp(
                abs(100 - np.sqrt(sum([i**2 for i in x])) / np.pi))) + 1)**0.1,
        7)


def sphere(x):
    return sum([i**2 for i in x])


def bohachevsky(x):
    return x[0]**2 + 2 * x[1]**2 - 0.3 * np.cos(
        3 * np.pi * x[0]) - 0.4 * np.cos(4 * np.pi * x[1]) + 0.7


def sum_squares(x):
    return sum([(i + 1) * x[i]**2 for i in range(len(x))])


def sum_diff_powers(x):
    return sum([abs(x[i])**(i + 2) for i in range(len(x))])


def booth(x):
    return (x[0] + 2 * x[1] - 7)**2 + (2 * x[0] + x[1] - 5)**2


def matyas(x):
    return 0.26 * (sum([i**2 for i in x])) - 0.48 * x[0] * x[1]


def mccormick(x):
    return np.sin(x[0] + x[1]) + (x[0] - x[1])**2 - 1.5 * x[0] + 2.5 * x[1] + 1


def dixon_price(x):
    return (x[0] - 1)**2 + sum([(i + 1) * (2 * x[i]**2 - x[i - 1])**2
                                for i in range(1, len(x))])


def six_hump_camel(x):
    return (4 - 2.1 * x[0]**2 + x[0]**4 / 3) * x[0]**2 + x[0] * x[1]\
        + (-4 + 4 * x[1]**2) * x[1]**2


def three_hump_camel(x):
    return 2 * x[0]**2 - 1.05 * x[0]**4 + x[0]**6 / 6 + x[0] * x[1] + x[1]**2


def easom(x):
    return -np.cos(x[0]) * np.cos(x[1]) * np.exp(-(x[0] - np.pi)**2 -
                                                 (x[1] - np.pi)**2)


def separation(x, y):
    return -np.linalg.norm(np.subtract(x, y))


def michalewicz(x):
    return -sum([
        np.sin(x[i]) * np.sin((i + 1) * x[i]**2 / np.pi)**20
        for i in range(len(x))
    ])


def beale(x):
    return (1.5 - x[0] + x[0] * x[1])**2 + (2.25 - x[0] + x[0] * x[1]**2)**2 + \
           (2.625 - x[0] + x[0] * x[1]**3)**2


def drop_wave(x):
    return -(1 + np.cos(12 * np.sqrt(sum([i**2 for i in x])))) / (
        0.5 * sum([i**2 for i in x]) + 2)


def sum_mult(x):
    part1 = 0.0
    part2 = 1.0
    for c in x:
        part1 += abs(c)
        part2 *= abs(c)
    return part1 + part2


def rastrigin(x):
    return 10 * len(x) + sum([(i**2 - 10 * np.cos(2 * np.pi * i)) for i in x])


def area(x):
    perimetro = 2 * x[0] + 2 * x[1]
    area = x[0] * x[1]
    ratio = area / perimetro
    return ratio


'''def constraint(x):
    penalizar = 0
    valor = 0
    if constraint:
        valor = float('inf')
    else:
        valor = func
    return valor'''


def cylinder(x, volume_fixo):
    base_area = np.pi * x[0]**2
    side_area = 2 * np.pi * x[0] * x[1]
    volume = base_area * x[1]
    total_area = side_area + 2 * base_area
    if volume < volume_fixo:
        total_area += 10**9
    return total_area


def alpine(x):
    return sum([(abs(x[i] * np.sin(x[i]) + .1 * x[i])) for i in range(len(x))])


def Rosenbrock(x):
    r = (1 - x[0]**2)**2 + 100 * (x[1] - x[0]**2)**2
    return r


def himmelblau(x):
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2


def knapsack(x, mochila):
    weight = mochila[0]
    value = mochila[1]
    pick_weight = []
    pick_value = []
    for k in range(len(x)):
        if x[k] >= 1:
            pick_weight.append(weight[k] * x[k])
            pick_value.append(value[k] * x[k])
    total_weight = sum(pick_weight)
    total_value = -1 * sum(pick_value)
    if total_weight > mochila[2]:
        total_value /= total_weight
    return total_value


def damavandi(x):
    return (1 - abs(
        np.sin(np.pi * (x[0] - 2)) * np.sin(np.pi * (x[1] - 2)) /
        (np.pi**2 * (x[0] - 2) * (x[1] - 2)))**5) * (2 + (x[0] - 7)**2 + 2 *
                                                       (x[1] - 7)**2)


def TSPCF(x, distances):
    rota = list(x)
    total = 0
    for k in range(len(x)):
        origem = int(x[k - 1])
        destino = int(x[k])
        total += distances[origem][destino]
    return total


def TSPCA(x, distances):
    rota = list(x)
    total = 0
    repetido = 1
    for city in rota:
        if rota.count(city) > 1:
            repetido += rota.count(city)
    for k in range(1, len(x)):
        origem = int(x[k - 1])
        destino = int(x[k])
        total += distances[origem][destino]
    if repetido > 1:
        total *= repetido
    return total


def schwefel(x):
    val = 0
    d = len(x)
    val = np.sum(np.sin(np.sqrt(np.abs(x))))
    val = 418.9829 * d - val
    return val


def clustering(lista, dados):
    lista = np.asarray(lista)
    pontos = dados
    j = len(dados[0])
    k = len(lista) / j
    local = np.split(lista, k)
    soma = 0
    for p in pontos:
        dist = []
        for l in local:
            np.subtract(p, l)
            d = np.linalg.norm(p)
            dist.append(d)
        soma += min(dist)
    n = len(pontos)
    media = soma / n
    return media


def sum_matrix(x):
    soma = 0.0
    for a in x:
        soma += abs(a)
    return soma


def R(x):
    res = (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    return res


def C_1(x):
    res = (x[0] - 1)**3 - x[1] + 1
    return res


def C_2(x):
    res = x[0] + x[1] - 2
    return res
