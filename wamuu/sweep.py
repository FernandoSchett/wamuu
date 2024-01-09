from utils import sweep_groups, sort_group_by_subst_dist, prim, get_turb_out_power, put_cables

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
