import numpy as np
from sweep import best_sweep
from solution import Solution
from time import time
from grasp import grasp
from cost import cost
import random
from disjointset import DisjointSet

def ant_algorithm(instance, evaporation=0.001, tl=10*60, seed=None, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    #nodes = [i for i in range(0, instance.n + 1)]   
    pheromones = [[1 for _ in range(instance.n)] for _ in range(instance.n)] 
    
    t = time()
    while time() - t < tl:
        solution = find_path(instance.n, pheromones, instance.dist)
        pheromones = update_pheromones(pheromones, solution, evaporation, instance.n)
        if cost(solution) < cost(best_solution):
            best_solution = solution        
    
    return best_solution 


def find_path(num_nodes, pheromones, dist):
    nodes = [i for i in range(0, num_nodes + 1)]
    disjoint_set = DisjointSet(nodes)

    mst = []
    for vertex1 in range(num_nodes):
        for vertex2 in range(num_nodes):
            if disjoint_set.find(vertex1) != disjoint_set.find(vertex2):
                if random.random() < choose_edge(pheromones, vertex1, vertex2, mst, num_nodes, dist):
                    disjoint_set.union(vertex1, vertex2)
                    mst.append((vertex1, vertex2))

    return mst

def choose_edge(pheromones, vertex1, vertex2, mst, num_nodes, dist):
    choosen_vertex = list(set([elemento for dupla in mst for elemento in dupla]))
    soma = 0
    for i in range(num_nodes):
            soma += 1/dist[choosen_vertex, i] * pheromones[choosen_vertex][i]

    return 1/dist[vertex1, vertex2] * pheromones[vertex1][vertex2] * soma


def update_pheromones(pheromones, solution, evaporation, num_nodes, M=1):
    for i in range(num_nodes):
        for j in range(num_nodes):
            if (i, j) in solution:
                pheromones[i][j] = (evaporation * pheromones[i][j]) + M/cost(solution)
            else:
                pheromones[i][j] = evaporation * pheromones[i][j]
    return pheromones

