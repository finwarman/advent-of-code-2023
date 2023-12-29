#! /usr/bin/env python3
#%%

from collections import defaultdict
import networkx as nx
import itertools
from operator import mul
from functools import reduce

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

ROWS = [row.strip() for row in data.split('\n')[:-1]]

# ==== SOLUTION ====

MAPPINGS = defaultdict(set)

# parse mappings (two-way)
for row in ROWS:
    key, vals = row.split(': ')
    vals = vals.split(' ')
    MAPPINGS[key].update(vals)
    for val in vals:
        MAPPINGS[val].add(key)

# create a networkx graph from MAPPINGS
G = nx.Graph()
for key, vals in MAPPINGS.items():
    for val in vals:
        G.add_edge(key, val)

TARGET_GROUPS        = 2
TARGET_DELETE_EDGES  = 3

def split_groups_by_removing_edges(G):
    if G.number_of_edges() < TARGET_DELETE_EDGES:
        return None, []

    # Sort edges by edge betweenness centrality in descending order
    edge_centrality = nx.edge_betweenness_centrality(G)
    sorted_edges = sorted(edge_centrality, key=edge_centrality.get, reverse=True)

    for edges in itertools.combinations(sorted_edges, TARGET_DELETE_EDGES):
        H = G.copy()
        H.remove_edges_from(edges)

        # Check if exactly two components are formed
        if nx.number_connected_components(H) == TARGET_GROUPS:
            return nx.connected_components(H), list(edges)

    return None, []

# Example usage
communities, removed_edges = split_groups_by_removing_edges(G)
communities = list(communities)

if communities:
    for i, community in enumerate(communities):
        print(f"Community {i+1}: Size {len(community)} [{', '.join(sorted(community)[:4])}, ...]")
    print()
    print(f"Edges removed: {removed_edges}")
    print()
    print(reduce(mul, [len(c) for c in communities], 1))
else:
    print(f"Could not split the graph into {TARGET_GROUPS} groups "
          + "with {TARGET_DELETE_EDGES} edge removals")

# 551196

# %%
