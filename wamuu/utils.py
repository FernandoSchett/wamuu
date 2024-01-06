"""
File:           utils.py
Last changed:   06/01/2023 10:53
Purpose:        here are the static utils functions that will be used on all sets of tha application         
Authors:        Fernando Antonio Marques Schettini, Pedro miranda         
""" 

import numpy as np
from queue import Queue

class utils:

    @staticmethod
    def read_turb():
        return "Este é um método estático!"

    @staticmethod
    def read_cable():
        return "Este é um método estático!"

    @staticmethod
    def dist_matrix(turbs):
        n = len(turbs)
        matrix = np.empty((n, n))
        for i in range(n):
            matrix[i][i] = np.linalg.norm(turbs[i])
            for j in range(i + 1, n):
                matrix[j][i] = matrix[i][j] = np.linalg.norm(turbs[i] - turbs[j])
        return matrix

    @staticmethod
    def prim(group, dist):
        mst_vertices = {group[0]}
        fringe_vertices = {group[i] for i in range(1, len(group))}
        mst = dict()
        for i in group:
            mst[i] = []
        next_mst_vertex = None
        next_fringe_vertex = None
        while len(fringe_vertices) > 0:
            min_dist = 1e18
            for mst_vertex in mst_vertices:
                for fringe_vertex in fringe_vertices:
                    if dist[mst_vertex][fringe_vertex] < min_dist:
                        next_mst_vertex = mst_vertex
                        next_fringe_vertex = fringe_vertex
                        min_dist = dist[mst_vertex][fringe_vertex]
            fringe_vertices.remove(next_fringe_vertex)
            mst_vertices.add(next_fringe_vertex)
            mst[next_mst_vertex].append(next_fringe_vertex)
            mst[next_fringe_vertex].append(next_mst_vertex)
        return mst

    @staticmethod
    def sweep_groups(n: int, start_index: int, clockwise: bool, tpg: int):
        assert start_index < n
        groups = []
        i = start_index
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
            while i < start_index:
                groups.append([])
                while j < tpg and i < start_index:
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
            while i > start_index:
                groups.append([])
                while j < tpg and i > start_index:
                    groups[k].append(i)
                    i -= 1
                    j += 1
                j %= tpg
                k += 1
        return groups

    @staticmethod
    def sort_group_by_subst_dist(group, dist):
        subst_dist = [dist[i][i] for i in group]
        order = sorted(range(len(subst_dist)), key=lambda x: subst_dist[x])
        return [group[i] for i in order]

    @staticmethod
    def get_turb_out_power(group, mst):
        levels = [[group[0]]]
        level = {group[0]: 0}
        vis = set()
        q = Queue()
        q.put(group[0])
        k = 0
        while not q.empty():
            i = q.get()
            vis.add(i)
            levels.append([])
            k += 1
            for j in mst[i]:
                if j not in vis:
                    q.put(j)
                    levels[k].append(j)
                    level[j] = k
        levels = levels[::-1]
        power = dict()
        for i in group:
            power[i] = 1
        for i in levels[0]:
            q.put(i)
        while not q.empty():
            i = q.get()
            for j in mst[i]:
                if level[j] < level[i]:
                    power[j] += power[i]
                    q.put(j)
        return power

    @staticmethod
    def sweep(instance, start_turbine: int, clockwise: bool, tpg: int):
        groups = utils.sweep_groups(instance.n, start_turbine, clockwise, tpg)
        assert len(groups) <= instance.C
        groups = [utils.sort_group_by_subst_dist(group, instance.dist) for group in groups]
        msts = [utils.prim(group, instance.dist) for group in groups]
        return msts