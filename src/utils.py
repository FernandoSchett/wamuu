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
    return groups
