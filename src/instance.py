import numpy as np
from os import path

# C is the substation's cable capacity
class Instance():
    def __init__(self,
                 instance_dir: str,
                 instance: str,
                 C: int = 0):
        with open(f'{path.join(instance_dir, instance)}.turb') as f:
            line = f.readline().split()
            self._delta = (float(line[0]), float(line[1]))
            self._Cmin = -int(line[2]) - 1
            nodes = [[0, 0]]
            # We assume the power produced by each turbine as always equals to 1.
            for line in f:
                line = line.split()
                nodes.append([
                    float(line[0]) - self._delta[0],
                    float(line[1]) - self._delta[1]
                ])
        
        if C == 0:
            self._C = self._Cmin + 1
        elif C < self._Cmin:
            raise f'C ({C}) cannot be lower than Cmin ({self._Cmin}) given by instance.'
        else:
            self._C = C
        
        self._nodes = np.array(nodes)


        # Sort turbines by clockwise order relative to the substation.
        # This way, each turbine will be uniquely identified by its index after sort.
        clockwise_order = []
        h = np.array([1, 0])
        for turb in self._nodes[1::]:
            t = turb / np.linalg.norm(turb)
            d = np.dot(h, t)
            angle = np.arccos(d)
            clockwise_order.append(angle)
        self._nodes[1::] = self._nodes[1::][np.argsort(clockwise_order)]


        # Create the matrix of distances between each node i to each node j.
        self._dist = np.empty((len(self._nodes), len(self._nodes)))
        for i in range(len(self._nodes)):
            self._dist[i][i] = 0.0
            for j in range(i+1, len(self._nodes)):
                self._dist[i][j] = np.linalg.norm(self._nodes[i] - self._nodes[j])
                self._dist[j][i] = self._dist[i][j]
        

        self._cables = []
        with open(f'{path.join(instance_dir, instance)}.cable') as f:
            for line in f:
                line = line.split()
                self._cables.append({
                    'capacity': int(line[0]),
                    'cpm': int(line[1]),
                    'availability': int(line[2]),
                })
        # Sort cables in capacity ascending order.
        self._cables = sorted(self._cables, key=lambda cable: cable['capacity'])
    
    @property
    def delta(self):
        return self._delta
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def cables(self):
        return self._cables
    
    @property
    def dist(self):
        return self._dist
    
    @property
    def C(self):
        return self._C
    
    @property
    def Cmin(self):
        return self._Cmin
    
    @property
    def n(self):
        return len(self._nodes)-1
