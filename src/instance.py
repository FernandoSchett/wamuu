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
            self._subst = (float(line[0]), float(line[1]))
            self._Cmin = -int(line[2]) - 1
            turbs = []
            # We assume the power produced by each turbine as always equals to 1.
            for line in f:
                line = line.split()
                turbs.append([
                    float(line[0]) - self._subst[0],
                    float(line[1]) - self._subst[1]
                ])
        
        if C == 0:
            self._C = self._Cmin + 1
        elif C < self._Cmin:
            raise f'C ({C}) cannot be lower than Cmin ({self._Cmin}) given by instance.'
        else:
            self._C = C
        
        self._turbs = np.array(turbs)


        # Sort turbines by clockwise order relative to the substation.
        clockwise_order = []
        h = np.array([1, 0])
        for turb in self._turbs:
            t = turb / np.linalg.norm(turb)
            d = np.dot(h, t)
            angle = np.arccos(d)
            clockwise_order.append(angle)
        self._turbs = self._turbs[np.argsort(clockwise_order)]


        # Create the matrix of distances between each turbine i to each turbine j.
        # The distance of turbine i to itself is its distance to the substation.
        self._dist = np.empty((len(self._turbs), len(self._turbs)))
        for i in range(len(self._turbs)):
            self._dist[i][i] = np.linalg.norm(self._turbs[i])
            for j in range(i+1, len(self._turbs)):
                self._dist[i][j] = np.linalg.norm(self._turbs[i] - self._turbs[j])
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
    def dist(self):
        return self._dist
    
    @property
    def C(self):
        return self._C
    
    @property
    def Cmin(self):
        return self._Cmin
