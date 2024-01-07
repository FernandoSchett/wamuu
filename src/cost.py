from utils import intersect

def cost(instance, solution, M1=1e9, M2=1e9, M3=1e9, M4=1e10, simple=False):
    res = 0
    # Cable costs
    for x in solution:
        a, b = x[0]
        if x[1] < 0:
            res += instance.dist[a][b]*instance.cables[-1]['cpm'] - M1*x[1]
        else:
            res += instance.dist[a][b]*instance.cables[x[1]]['cpm']
    
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
