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
# Make sure the value of starting_index be in [0,n[
def sweep_groups(n: int, starting_index: int, clockwise: bool, tpg: int):
    groups = []
    i = starting_index
    j = 0
    k = 0
    if clockwise:
        while i < n:
            groups.append([])
            while j < tpg and i < n:
                groups[k].append(i)
                i += 1
                j += 1
            j %= tpg
            k += 1
        i = 0
        while i < starting_index:
            groups.append([])
            while j < tpg and i < starting_index:
                groups[k].append(i)
                i += 1
                j += 1
            j %= tpg
            k += 1
    else:
        while i >= 0:
            groups.append([])
            while j < tpg and i >= 0:
                groups[k].append(i)
                i -= 1
                j += 1
            j %= tpg
            k += 1
        i = n - 1
        while i > starting_index:
            groups.append([])
            while j < tpg and i > starting_index:
                groups[k].append(i)
                i -= 1
                j += 1
            j %= tpg
            k += 1
    i = 0
    while not 0 in groups[i]:
        i += 1
    return groups[i:] + groups[:i]

# This function sort the group of turbine indices by its distance to the
# substation in ascending order.
def sort_group_by_subst_dist(group, dist):
    subst_dist = [dist[i][i] for i in group]
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
