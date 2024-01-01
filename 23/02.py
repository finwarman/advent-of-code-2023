#! /usr/bin/env python3
# %%

import numpy as np
from functools import cache
import networkx as nx

# ==== INPUT ====

INPUT = 'input.txt'
# INPUT = 'example.txt'
with open(INPUT, 'r', encoding='UTF-8') as file:
    data = file.read()

GRID = np.array([list(row.strip()) for row in data.split('\n')[:-1]])
HEIGHT, WIDTH = GRID.shape

# ==== SOLUTION ====

FOREST = '#'
DIRS = (UP, DOWN, LEFT, RIGHT) = (0, -1), (0, 1), (-1, 0), (1, 0) # (dx, dy)

START_POS  = (1, 0) # (x, y)
TARGET_POS = (WIDTH-2, HEIGHT-1)

# find the longest path, never step onto same tile twice

@cache
def get_all_neighbours(pos):
    x, y = pos
    new_neighbours = []
    for neighbour in ((x+dx, y+dy) for (dx, dy) in DIRS):
        nx, ny = neighbour
        if nx < 0 or nx >= WIDTH:
            continue
        if ny < 0 or ny >= HEIGHT:
            continue
        if GRID[ny][nx] == FOREST:
            continue
        new_neighbours.append(neighbour)
    return new_neighbours

def get_valid_neighbours(pos, seen):
    return [n for n in get_all_neighbours(pos) if (n not in seen)]

# Identify vertices (points with more than two valid neighbors, plus start/end)
vertices = set()
valid_positions = {(x, y) for y in range(HEIGHT) for x in range(WIDTH) if GRID[y][x] != FOREST}
for x, y in valid_positions:
    neighbors = get_all_neighbours((x, y))
    if (len(neighbors) > 2) or ((x, y) in (START_POS, TARGET_POS)):
        vertices.add((x, y))

# print("Vertices:", sorted(vertices))
print("Vertex count:", len(vertices))

# Initialize the graph with vertices


graph = {vertex: set() for vertex in vertices}
queue = [ # last_vertex, position, distance, seen
          (START_POS, START_POS, 0, {START_POS}) ]
seen_vertices = {vertex: 0 for vertex in vertices}
def bfs(pop_in=-1):
    while queue:
        last_vertex, current_pos, distance, seen = queue.pop(pop_in)

        if current_pos in vertices:
            if seen_vertices[current_pos] > 5: # bodge to ensure we get every edge
                continue
            seen_vertices[current_pos] += 1

            if current_pos != last_vertex:
                graph[current_pos].add((last_vertex, distance))
                graph[last_vertex].add((current_pos, distance))
                last_vertex = current_pos
                distance = 0  # Reset distance only if current_pos is a new vertex

        # Optimized the for loop to reduce redundant set copying
        for neighbour in get_valid_neighbours(current_pos, seen):
            if neighbour not in seen:
                queue.append((last_vertex, neighbour, distance + 1, seen | {neighbour}))
                # Used set union (|) for a more concise and efficient seen set update
bfs()
# slight bodge to get ensure we get every edge
seen_vertices = {vertex: 0 for vertex in vertices}
queue = [ # last_vertex, position, distance, seen
          (TARGET_POS, TARGET_POS, 0, {TARGET_POS}) ]
bfs(pop_in=0)

# build graph
G = nx.Graph()
for vertex in graph:
    G.add_node(vertex)
    for neighbour, distance in graph[vertex]:
        G.add_edge(vertex, neighbour, weight=distance)

# print("Graph:", graph)
print("Edges:", G.number_of_edges())

# Get longest path
try:
    simple_paths = nx.all_simple_paths(G, START_POS, TARGET_POS)
    max_dist = max([
        (path, sum(G.edges[pair]['weight'] for pair in list(nx.utils.pairwise(path))))
        for path in simple_paths
    ], key=lambda x: x[1])
    print("Length:", max_dist[-1])
except:
    print("No paths (empty sequence)")

# 6486

# show graph
def draw_graph():
    from matplotlib import pyplot as plt

    # Create a position dictionary based on node coordinates
    # each node is a tuple of (x, y)
    pos = {node: (node[0], -node[1]) for node in G.nodes()}  # flip-y

    # draw nodes
    nx.draw(G, pos, with_labels=True, font_weight='bold', font_size=8, node_size=10)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight') # get edge weights
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.show()

draw_graph()

# %%
