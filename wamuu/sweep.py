from utils import sweep_groups, sort_group_by_subst_dist, prim, get_turb_out_power
from cost import cost

# Returns list of edges and node power.
def sweep(instance, starting_turbine: int, clockwise: bool, tpg: int):
    groups = sweep_groups(instance.n, starting_turbine, clockwise, tpg)
    groups = [sort_group_by_subst_dist(group, instance.dist) for group in groups]
    edges_group = [prim(group, instance.dist, group[0]) for group in groups]
    powers = [get_turb_out_power(groups[i], edges_group[i]) for i in range(len(groups))]
    power = dict()
    for p in powers: power |= p
    edges = []
    for eg in edges_group: edges.extend(eg)
    for group in groups: edges.append([group[0], 0])
    
    return [((edge[0], edge[1]), power[edge[0]]) for edge in edges]

def best_sweep(instance, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    curr_cost = 1e18
    curr_solution = None
    for starting_turbine in range(1, instance.n+1):
        for clockwise in (True, False):
            for tpg in range(instance.n//instance.C, instance.max_cable_capacity+1):
                s = sweep(instance, starting_turbine, clockwise, tpg)
                c = cost(instance, s, M1, M2, M3, M4, simple=True)
                if c < curr_cost:
                    curr_cost = c
                    curr_solution = s
    return curr_solution
