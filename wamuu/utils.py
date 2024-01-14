import numpy as np
from queue import Queue

def prim(nodes, weight, starting_node):
    mst_nodes = { starting_node }
    fringe_nodes = { node for node in nodes }
    fringe_nodes.remove(starting_node)

    next_mst_node = None
    next_fringe_node = None
    edges = []
    while len(fringe_nodes) > 0:
        min_dist = 1e18
        for mnode in mst_nodes:
            for fnode in fringe_nodes:
                if weight[mnode][fnode] < min_dist:
                    next_mst_node = mnode
                    next_fringe_node = fnode
                    min_dist = weight[mnode][fnode]
        fringe_nodes.remove(next_fringe_node)
        mst_nodes.add(next_fringe_node)
        # Making edges this way will result in a directed graph with
        # edges pointing towards the starting_node.
        edges.append([next_fringe_node, next_mst_node])
    return edges

# This function create groups of indices for the sweep algorithm
# as defined in paper.
# Make sure the value of starting_index be in [1,n]
def sweep_groups(n: int, starting_index: int, clockwise: bool, tpg: int):
    groups = []
    i = starting_index
    j = 0
    k = 0
    if clockwise:
        while i <= n:
            groups.append([])
            while j < tpg and i <= n:
                groups[k].append(i)
                i += 1
                j += 1
            j %= tpg
            k += 1
        i = 1
        while i < starting_index:
            groups.append([])
            while j < tpg and i < starting_index:
                groups[k].append(i)
                i += 1
                j += 1
            j %= tpg
            k += 1
    else:
        while i >= 1:
            groups.append([])
            while j < tpg and i >= 1:
                groups[k].append(i)
                i -= 1
                j += 1
            j %= tpg
            k += 1
        i = n
        while i > starting_index:
            groups.append([])
            while j < tpg and i > starting_index:
                groups[k].append(i)
                i -= 1
                j += 1
            j %= tpg
            k += 1
    i = 0
    while not 1 in groups[i]:
        i += 1
    return groups[i:] + groups[:i]

# This function sort the group of turbine indices by its distance to the
# substation in ascending order.
def sort_group_by_subst_dist(group, dist):
    subst_dist = [dist[i][0] for i in group]
    order = sorted(range(len(subst_dist)), key=lambda x: subst_dist[x])
    return [group[i] for i in order]

def get_turb_out_power(group, edges):
    out_d = dict()
    in_d = dict()
    for i in group:
        in_d[i] = []
    for edge in edges:
        out_d[edge[0]] = edge[1]
        in_d[edge[1]].append(edge[0])
    s = list()
    q = Queue()
    q.put(group[0])
    while not q.empty():
        x = q.get()
        for i in in_d[x]:
            s.append(i)
            q.put(i)
    power = dict()
    # We assume the power produced by each turbine as always equals to 1.
    for i in group:
        power[i] = 1
    while len(s) > 0:
        x = s.pop()
        power[out_d[x]] += power[x]
    return power

# power is a dictionary of node as keys and power out value as values.
# cables is the instance set of cables.
# We assume that the availability of cables is infinite.
# Returns dictionary of node-cable_index
# Negative cable index represents an overflow arc and its absolute value
# is equal to the amount of extra flow.
def put_cables(power, cables):
    d = dict()
    for node, power_out in power.items():
        i = 0
        while True:
            if i >= len(cables):
                d[node] = cables[-1]['capacity'] - power_out
                break
            elif power_out <= cables[i]['capacity']:
                d[node] = i
                break
            else: i += 1
    return d

# Checks if two line segments a1b1 and a2b2 crosses each other.
def intersect(a1, b1, a2, b2):
    def direction(p, q, r):
        return (q[1]-p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])

    d1 = direction(a1, b1, a2)
    d2 = direction(a1, b1, b2)
    d3 = direction(a2, b2, a1)
    d4 = direction(a2, b2, b1)

    if d1 == 0 and d2 == 0:
        if b1[0] < a1[0]: a1, b1 = b1, a1
        if b2[0] < a2[0]: a2, b2 = b2, a2
        if a1[0] <= a2[0] and b1[0] >= b2[0]: return True
        if a1[0] >= a2[0] and b1[0] <= b2[0]: return True
        return False
        # if (
        #     a2[0] <= max(a1[0], b1[0]) and
        #     a2[0] >= min(a1[0], b1[0]) and
        #     a2[1] <= max(a1[1], b1[1]) and
        #     a2[1] >= min(a1[1], b1[1])
        # ): return True
        # return False

    if (
        ((d1>=0 and d2<=0) or (d1<=0 and d2>=0)) and
        ((d3>=0 and d4<=0) or (d3<=0 and d4>=0))
    ): return True
    return False

def cost(nodes, edges, dist, cables, node_cableindex, C, M1=1e9, M2=1e9, M3=1e9, M4=1e10, debug=False):
    res = 0
    # Cable costs
    for edge in edges:
        a, b = edge
        if node_cableindex[a] < 0:
            res += dist[a][b]*cables[-1]['cpm'] - M1*node_cableindex[a]
        else:
            res += dist[a][b]*cables[node_cableindex[a]]['cpm']
    if debug: print(f'Cable costs: {res}')
    
    # Connections to the substation
    subst_conn = 0
    for edge in edges:
        if edge[1] == 0: subst_conn += 1
    res += max(0, M2*(subst_conn-C))
    if debug: print(f'Connections to the substation: {max(0, M2*(subst_conn-C))}')

    # Crossings
    crossings = 0
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            if (
                edges[i][0] == edges[j][1] or
                edges[i][1] == edges[j][0] or
                edges[i][1] == edges[j][1]
                ): continue
            crossings += intersect(nodes[edges[i][0]], nodes[edges[i][1]], nodes[edges[j][0]], nodes[edges[j][1]])
    res += M3*crossings
    if debug: print(f'Crossings: {M3*crossings}')

    # Proper Tree
    # Maybe it could be improved by analysing the whole tree.
    res += M4*(len(edges) != len(nodes)-1)
    if debug: print(f'Proper Tree: {M4*(len(edges) != len(nodes)-1)}')

    return res

def prim_solution(instance):
    e = prim(range(instance.n+1), instance.dist, 0)
    p = get_turb_out_power(range(instance.n+1), e)
    return [((ei[0], ei[1]), p[ei[0]]) for ei in e]
