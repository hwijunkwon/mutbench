import numpy as np
import networkx as nx
from tools.mutclust.network_propagation.core import propagate, build_adjacency_matrix

def test_propagate_seed_highest():
    G = nx.path_graph(5)
    scores = propagate(G, {2}, alpha=0.01, max_iter=100)
    assert scores[2] == max(scores.values())

def test_propagate_neighbors_higher():
    G = nx.path_graph(5)
    # alpha=0.5 gives sufficient restart probability so seed stays highest;
    # with low alpha the random walk converges to degree-proportional stationary
    # distribution where interior nodes dominate over endpoint seeds.
    scores = propagate(G, {0}, alpha=0.5, max_iter=100)
    assert scores[0] > scores[1] > scores[2]

def test_propagate_disconnected():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (2, 3)])
    scores = propagate(G, {0}, alpha=0.01, max_iter=100)
    assert scores[0] > 0
    assert scores[2] < 1e-10

def test_build_adjacency_matrix():
    G = nx.path_graph(3)
    W, nodes = build_adjacency_matrix(G)
    assert W.shape == (3, 3)
    assert abs(W.sum(axis=1) - 1).max() < 1e-10
