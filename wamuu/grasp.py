import random
from utils import sweep_groups, sort_group_by_subst_dist, prim, get_turb_out_power
from cost import cost

def grasp(instance, starting_node, list_size, probability, flag=False):
    nodes = [i for i in range(1, instance.n + 1)]   
    edges_group = grasp_edges(nodes, starting_node, instance.dist, list_size, probability)
    nodes.remove(starting_node)
    nodes.insert(0,starting_node)
    power = get_turb_out_power(nodes, edges_group)
    edges = edges_group
    edges.append([starting_node, 0])  

    if flag == True:
        nodes = sort_group_by_subst_dist(nodes, instance.dist)
        for i in range(instance.C):
            edges.append([nodes[i], 0])

    return [((edge[0], edge[1]), power[edge[0]]) for edge in edges]

def grasp_edges(nodes, starting_node, weight, list_size, probability):
    def calculate_quality(mnode, fnode):
        return weight[mnode][fnode]

    mst_nodes = {starting_node}
    fringe_nodes = {node for node in nodes}
    fringe_nodes.remove(starting_node)

    edges = []
    while len(fringe_nodes) > 0:
        candidate_list = []
        for mnode in mst_nodes:
            for fnode in fringe_nodes:
                candidate_list.append((mnode, fnode, calculate_quality(mnode, fnode)))

        candidate_list.sort(key=lambda x: x[2])

        limited_candidate_list = candidate_list[:list_size]

        if limited_candidate_list:
            if random.random() < probability:
                next_mst_node, next_fringe_node, _ = random.choice(limited_candidate_list)
            else:
                next_mst_node, next_fringe_node, _ = limited_candidate_list[0]

            fringe_nodes.remove(next_fringe_node)
            mst_nodes.add(next_fringe_node)
            edges.append([next_fringe_node, next_mst_node])
    return edges