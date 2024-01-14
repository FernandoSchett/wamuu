import numpy as np
from sweep import best_sweep
from solution import Solution
from utils import prim_solution
from cost import cost
from time import time

def sa(instance, T=1.0, alpha=0.99999, tl=10*60, seed=None):
    i = instance.n*2
    rng = np.random.default_rng(seed)
    S = Solution(instance, best_sweep(instance))
    k = 1/cost(instance, prim_solution(instance), 0, 0, 0, 0, True)
    t = time()
    while time() - t < tl:
        node_a = rng.integers(1, instance.n+1)
        node_b = rng.integers(instance.n+1)
        while S.is_in_cc(node_a, node_b):
            node_b = rng.integers(instance.n+1)

        e = S.cost
        S.create_checkpoint(node_a)
        S.one_opt(node_a, node_b)
        e = S.cost - e

        if e > 0 and rng.random() > np.exp(-k*e/T):
            S.restore()
        
        if i > 0: i -= 1
        else: T *= alpha

        if (S._crossings < 0):
            return S
    return S
