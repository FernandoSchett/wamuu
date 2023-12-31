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
