import math
from collections import defaultdict

import networkx as nx

# List with node and edge attributes to compute stats
# plots.py imports them to make the plots
nattrs = ["functional_area", "work", "rank", "gender", "age"]
eattrs = ["strength", "frequency", "helps", "context"]

##
## Basic stats functions
##
def std(x):
    if sum(x) == 0: return 0
    n = float(len(x))
    sum_x1 = sum(x)
    sum_x2 = sum([i**2 for i in x])
    mean = sum_x1 / n
    return math.sqrt(abs((sum_x2 / n) - (mean * mean)))

def mean(x):
    if sum(x) == 0: return 0
    return sum(x) / float(len(x))

def median(x):
    sorted_x = sorted(x)
    count = len(sorted_x)

    if count % 2 == 1:
        return sorted_x[(count+1)/2-1]
    else:
        lower = sorted_x[count/2-1]
        upper = sorted_x[count/2]
        return (float(lower + upper)) / 2

##
## Edge and node attributes
##
def get_node_percentages(G, attr):
    result = defaultdict(int)
    nodes = set(n for n, d in G.nodes(data='True', default=False) if G.nodes[n]['is_ego'])
    total = float(len(nodes))
    for n in nodes:
        if G.nodes[n][attr] is not None:
            result[G.nodes[n][attr]] += 1
    return dict((k, (v/total)*100) for k, v in result.items())

def get_edge_percentages(G, attr):
    ego = next(n for n, d in G.nodes(data='True', default=False) if G.nodes[n]['is_ego'])
    result = defaultdict(int)
    edges = [d for u, v, d in G.edges(ego, data=True)]
    total = float(len(edges))
    for e in edges:
        if e[attr] is not None:
            result[e[attr]] += 1
    return dict((k, (v/total)*100) for k, v in result.items())

def get_age_ranges(G):
    ego = next(n for n, d in G.nodes(data='True', default=False) if G.nodes[n]['is_ego'])
    age = nx.get_node_attributes(G,'age')
    del(age[ego])
    total = float(len(age))
    result = {"20-30":0,
              "31-40":0,
              "41-50":0,
              "51-60":0,
              "61-70":0,
              "71-80":0,
              "81-90":0}
    for a in (v for v in age.values() if v):
        if int(a) <= 30:
            result["20-30"] += 1
        elif int(a) <= 40:
            result["31-40"] += 1
        elif int(a) <= 50:
            result["41-50"] += 1
        elif int(a) <= 60:
            result["51-60"] += 1
        elif int(a) <= 70:
            result["61-70"] += 1
        elif int(a) <= 80:
            result["71-80"] += 1
        elif int(a) <= 90:
            result["81-90"] += 1
    return dict((k, (v/total)*100) for k,v in result.items() if v)

##
## Node and edges attributes for the whole reference group
##
def accumulate_attributes(G, attr, result, nodes_or_edges='nodes'):
    if nodes_or_edges == 'nodes':
        if attr == 'age':
            this_result = get_age_ranges(G)
        else:
            this_result = get_node_percentages(G, attr)
    else:
        this_result = get_edge_percentages(G, attr)
    for k, v in this_result.items():
        if k not in result:
            result[k] = v
        else: 
            result[k] += v
    return result

##
## Global egonetwork measures
##
def centralization_degree(H, exclude_ego=True):
    if exclude_ego:
        G = H.copy()

        G.remove_node(ego)
    else:
        G = H
    # Isolated ego corner case
    if G.order() < 2:
        return 0
    deg = G.degree()
    dmax = max(deg.values())
    num = sum([(dmax - d) for d in deg.values()])
    denom = float((len(G) - 1) * (len(G) - 2))
    return (num / denom) if denom else 0

