import numpy as np
from sweep import best_sweep
from solution import Solution
from time import time
from grasp import grasp
from cost import cost
import random
from utils import sweep_groups, sort_group_by_subst_dist, prim, get_turb_out_power
from disjointset import DisjointSet

def ant_algorithm(instance, evaporation=0.001, tl=10*600, seed=None, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    pheromones = [[1 for _ in range(instance.n)] for _ in range(instance.n)] 
    
    best_solution, mst = find_path(instance.n, pheromones, instance.dist)
    pheromones = update_pheromones(instance, pheromones, best_solution, evaporation, instance.n, mst)

    t = time()
    while time() - t < tl:
        solution, mst = find_path(instance.n, pheromones, instance.dist)
        print(solution)
        pheromones = update_pheromones(instance, pheromones, solution, evaporation, instance.n, mst)
        custo = cost(instance, solution)
        print("custo:")
        print(custo)
        if custo < cost(instance, best_solution):
            
            best_solution = solution        
    
    return best_solution 


def find_path(num_nodes, pheromones, dist):
    disjoint_set = DisjointSet([i for i in range(0, num_nodes + 1)])
    
    poss_edges = []
    edge_val = {}

    soma = 0
    for vertex1 in range(num_nodes):
        for vertex2 in range(num_nodes):
            if vertex1 != vertex2:
                val = 1 / dist[vertex1][vertex2] * pheromones[vertex1][vertex2]
                edge_val[(vertex1, vertex2)] = val
                soma += val 
                
    
    mst = []
    
    while True:
        poss_edges.clear()
        
        for vertex1 in range(num_nodes):
            for vertex2 in range(num_nodes):
                if disjoint_set.find(vertex1) != disjoint_set.find(vertex2):
                    poss_edges.append((vertex1, vertex2))
                
        if not poss_edges:
            break     
        
        prob = [edge_val[i]*soma for i in poss_edges]
        probabilidades_normalizadas = [i / sum(prob) for i in prob]
        
        poss_edges_indices = list(range(len(poss_edges)))

        edge_indice = np.random.choice(poss_edges_indices, size=1, p=probabilidades_normalizadas)[0]    
        edge = poss_edges[edge_indice]
        soma = update_sum(edge_val, mst, num_nodes)
        disjoint_set.union(edge[0], edge[1])
        mst.append(edge)
        print(edge)

    nodes = [i for i in range(0, num_nodes + 1)]
    power = get_turb_out_power(nodes, mst)
    
    return [((edge[0], edge[1]), power[edge[0]]) for edge in mst], mst  

def update_sum(edge_val, mst, num_nodes):
    soma = 0
    for vertex1 in range(num_nodes):
        for vertex2 in range(num_nodes):
            if vertex1 != vertex2 and (vertex1, vertex2) not in mst:
                soma += edge_val[(vertex1, vertex2)] 
    return soma



def update_pheromones(instance, pheromones, solution, evaporation, num_nodes, mst, M=1):
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if (i, j) in mst:
                pheromones[i][j] = (evaporation * pheromones[i][j]) + M/cost(instance, solution)
            else:
                pheromones[i][j] = evaporation * pheromones[i][j]
    return pheromones

