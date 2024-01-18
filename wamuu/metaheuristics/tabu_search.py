import numpy as np
from sweep import best_sweep
from solution import Solution
from time import time
from ordered_set import OrderedSet

class Tabulist:
    def __init__(self, values, tenure: int):
        self._ubat = {v for v in values}
        self._tabu = OrderedSet()
        self._tenure = tenure
    
    @property
    def tenure(self):
        return self._tenure
    
    @tenure.setter
    def tenure(self, value):
        self._tenure = value
        self._refresh()
    
    def _refresh(self):
        while len(self._tabu) > self._tenure:
            self._ubat.add(self._tabu.index(0))
            self._tabu.pop(0)
    
    def add(self, value):
        self._ubat.remove(value)
        self._tabu.add(value)
        self._refresh()

    def remove(self, value):
        self._ubat.add(value)
        self._tabu.remove(value)

    def is_tabu(self, value):
        return bool(self._tabu.count(value))

    def reset(self):
        while len(self._tabu):
            self._ubat.add(self._tabu.pop(0))


def ts_node_from(instance, diversify_after=None, tl=10*60, seed=None, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    diversify_after = diversify_after or instance.n
    rng = np.random.default_rng(seed)
    k = False
    i = 0
    S = Solution(instance, best_sweep(instance, M1, M2, M3, M4))
    Sf = Solution(instance, S.solution)
    t = time()
    tabulist = Tabulist(range(1, instance.n+1), rng.integers((instance.n+1 if instance.n%2 else instance.n)//2, instance.n))
    while time() - t < tl:
        i += 1
        best_cost = 1e18
        best_move = None
        for node_from in range(1, instance.n+1):
            for node_to in range(instance.n+1):
                if S.is_in_cc(node_from, node_to):
                    continue
                S.save(node_from)
                S.one_opt(node_from, node_to)
                if (S.cost < best_cost and not tabulist.is_tabu(node_from)) or S.cost < Sf.cost:
                    best_cost = S.cost
                    best_move = (node_from, node_to)
                S.undo()
        if best_move:
            S.one_opt(best_move[0], best_move[1])
            if tabulist.is_tabu(best_move[0]):
                tabulist.remove(best_move[0])
            tabulist.add(best_move[0])
        
        if S.cost < Sf.cost:
            Sf = Solution(instance, S.solution)
        
        # Diversification Strategy
        if i > diversify_after:
            i = 0
            k = not k
            if k:
                tabulist.reset()
            else:
                tabulist.tenure = rng.integers((instance.n+1 if instance.n%2 else instance.n)//2, instance.n)
    return Sf

def ts_node_to(instance, diversify_after=None, tl=10*60, seed=None, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    diversify_after = diversify_after or instance.n
    rng = np.random.default_rng(seed)
    k = False
    i = 0
    S = Solution(instance, best_sweep(instance, M1, M2, M3, M4))
    Sf = Solution(instance, S.solution)
    t = time()
    tabulist = Tabulist(range(instance.n+1), rng.integers((instance.n+1 if instance.n%2 else instance.n)//2, instance.n))
    while time() - t < tl:
        i += 1
        best_cost = 1e18
        best_move = None
        for node_from in range(1, instance.n+1):
            for node_to in range(instance.n+1):
                if S.is_in_cc(node_from, node_to):
                    continue
                S.save(node_from)
                S.one_opt(node_from, node_to)
                if (S.cost < best_cost and not tabulist.is_tabu(node_to)) or S.cost < Sf.cost:
                    best_cost = S.cost
                    best_move = (node_from, node_to)
                S.undo()
        if best_move:
            S.one_opt(best_move[0], best_move[1])
            if tabulist.is_tabu(best_move[1]):
                tabulist.remove(best_move[1])
            tabulist.add(best_move[1])
        
        if S.cost < Sf.cost:
            Sf = Solution(instance, S.solution)
        
        # Diversification Strategy
        if i > diversify_after:
            i = 0
            k = not k
            if k:
                tabulist.reset()
            else:
                tabulist.tenure = rng.integers((instance.n+1 if instance.n%2 else instance.n)//2, instance.n)
    return Sf

def ts_arc(instance, diversify_after=None, tl=10*60, seed=None, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    diversify_after = diversify_after or instance.n
    rng = np.random.default_rng(seed)
    k = False
    i = 0
    S = Solution(instance, best_sweep(instance, M1, M2, M3, M4))
    Sf = Solution(instance, S.solution)
    t = time()
    tabulist = Tabulist(
        [(node_from, node_to) for node_from in range(1, instance.n+1) for node_to in range(instance.n+1)],
        rng.integers((instance.n+1 if instance.n%2 else instance.n)//2, instance.n)
    )
    while time() - t < tl:
        i += 1
        best_cost = 1e18
        best_move = None
        for node_from in range(1, instance.n+1):
            for node_to in range(instance.n+1):
                if S.is_in_cc(node_from, node_to):
                    continue
                S.save(node_from)
                S.one_opt(node_from, node_to)
                if (S.cost < best_cost and not tabulist.is_tabu((node_from, node_to))) or S.cost < Sf.cost:
                    best_cost = S.cost
                    best_move = (node_from, node_to)
                S.undo()
        if best_move:
            S.one_opt(best_move[0], best_move[1])
            if tabulist.is_tabu(best_move):
                tabulist.remove(best_move)
            tabulist.add(best_move)
        
        if S.cost < Sf.cost:
            Sf = Solution(instance, S.solution)
        
        # Diversification Strategy
        if i > diversify_after:
            i = 0
            k = not k
            if k:
                tabulist.reset()
            else:
                tabulist.tenure = rng.integers((instance.n+1 if instance.n%2 else instance.n)//2, instance.n)
    return Sf
