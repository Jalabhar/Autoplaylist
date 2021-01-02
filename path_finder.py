# import modin.pandas as mpd
import pandas as pd
import numpy as np
import Data_Collector as DC
import networkx as nx
import matplotlib.pyplot as plt
gr = DC.get_related


def tracker(start, end):
    r_dict = {}
    s = gr([start], n=1)
    r_dict[start] = s
    value_list = []
    c_dict = r_dict.copy()
    V = list(c_dict.values())
    value_list.extend(V[0])
    k = 0
    while end not in value_list and k < 10:
        for v in V:
            for entry in v:
                if entry not in r_dict:
                    try:
                        m = gr([entry], n=1)
                        r_dict[entry] = m
                        value_list.extend(m)
                        if end in value_list:
                            break
                        else:
                            c_dict = r_dict.copy()
                            V = c_dict.values()
                    except:
                        pass
        k += 1
    G = nx.DiGraph(r_dict)
    # print(len(G.edges))
    # print(len(G.nodes))
    path_list = []
    paths = nx.algorithms.shortest_paths.generic.all_shortest_paths(
        G, start, end)
    for path in paths:
        path_list.append(path)
    return path_list

    # nx.draw(G, pos=nx.spring_layout(G), node_size=25, style='dotted')


def Path_Points(f_end, s_end,two_way=False):
    path_1 = tracker(f_end, s_end)
    path_points = []
    for point in path_1:
        path_points.extend(point)
    if two_way:
        path_2 = tracker(s_end, f_end)
        for point in path_2:
            path_points.extend(point)
    path_points = list(set(path_points))
    path_df = pd.DataFrame(path_points, columns=['id'])
    path_df.to_csv('path_list.csv', index=False)
