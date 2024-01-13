from utils import intersect

def cable_cost(instance, node_a, node_b, node_power, M1):
    c = instance.get_cable_index_from_node_power(node_power)
    length_cost = instance.dist[node_a][node_b]*instance.cables[c]['cpm']
    overflow_cost = M1*max(0, node_power-instance.max_cable_capacity)
    return length_cost + overflow_cost


def cost(instance, solution, M1=1e9, M2=1e9, M3=1e9, M4=1e10, simple=False):
    res = 0
    # Cable costs
    for x in solution:
        res += cable_cost(instance, x[0][0], x[0][1], x[1], M1)
    
    # Connections to the substation
    subst_conn = 0
    for x in solution: subst_conn += x[0][1] == 0
    res += max(0, M2*(subst_conn-instance.C))

    if simple: return res

    # Crossings
    crossings = 0
    for i in range(len(solution)):
        for j in range(i+1, len(solution)):
            crossings += intersect(
                instance.nodes[solution[i][0][0]],
                instance.nodes[solution[i][0][1]],
                instance.nodes[solution[j][0][0]],
                instance.nodes[solution[j][0][1]])
    res += M3*crossings

    # Proper Tree
    # Maybe it could be improved by analysing the whole tree.
    res += M4*(len(solution) != instance.n)

    return res
