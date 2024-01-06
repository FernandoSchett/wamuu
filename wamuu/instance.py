"""
File:           instance.py
Last changed:   06/01/2024 10:54
Purpose:        class that represents an problem instance         
Authors:        Fernando Antonio Marques Schettini, Pedro Miranda    
"""

import numpy as np
import os
from utils import dist_matrix

# C is the cable capacity of the substation
class Instance:
    def __init__(self, dir, n, s, t, w, C):
        path = os.path.join(dir, f'n{n}_s0{s}_t0{t}_w0{w}')
        self._n = n
        self._turbs = np.empty((n, 2))
        with open(f'{path}.turb', 'r') as f:
            line = f.readline().split()
            self._subst = (float(line[0]), float(line[1]))
            self._cmin = -int(line[2]) - 1
            # We assume the power produced by each turbine as always equals to 1.
            for i in range(n):
                line = f.readline().split()
                self._turbs[i][0] = float(line[0]) - self._subst[0]
                self._turbs[i][1] = float(line[1]) - self._subst[1]

        assert C >= self._cmin
        self._C = C

        clockwise_order = []
        h = np.array([1, 0])
        for turb in self._turbs:
            t = turb / np.linalg.norm(turb)
            d = np.dot(h, t)
            angle = np.arccos(d)
            clockwise_order.append(angle)
        self._turbs = self._turbs[np.argsort(clockwise_order)]

        self._dist = dist_matrix(self._turbs)

        self._cables = {
            'capacity': [],
            'cpm': [],
            'availability': []
        }
        with open(f'{path}.cable', 'r') as f:
            for line in f:
                line = line.split()
                self._cables['capacity'].append(int(line[0]))
                self._cables['cpm'].append(int(line[1]))
                self._cables['availability'].append(int(line[2]))
    
    @property
    def n(self):
        return self._n
    
    @property
    def subst(self):
        return self._subst

    @property
    def turbs(self):
        return self._turbs
    
    @property
    def cables(self):
        return self._cables
    
    @property
    def C(self):
        return self._C
    
    @property
    def dist(self):
        return self._dist

if __name__ == "__main__": # How to use Instance class
    print("teste")