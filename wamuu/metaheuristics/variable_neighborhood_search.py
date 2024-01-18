import numpy as np
from sweep import best_sweep
from solution import Solution
from time import time

def vns(instance, Kmax, tl=10*60, seed=None, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
    rng = np.random.default_rng(seed)
    S0 = Solution(instance, best_sweep(instance, M1, M2, M3, M4))
    S = Solution(instance, S0.solution)

    t = time()
    while time() - t < tl:
        k = 1
        while k <= Kmax:
            # Shaking
            for _ in range(k):
                node_from = rng.integers(1, instance.n+1)
                node_to = rng.integers(instance.n+1)
                while S.is_in_cc(node_from, node_to):
                    node_to = rng.integers(instance.n+1)
                S.one_opt(node_from, node_to)
            
            # Local Search
            while True:
                best_cost = 1e18
                best_move = None
                for node_from in range(1, instance.n+1):
                    for node_to in range(instance.n+1):
                        if S.is_in_cc(node_from, node_to):
                            continue
                        S.save(node_from)
                        S.one_opt(node_from, node_to)
                        if S.cost < best_cost:
                            best_cost = S.cost
                            best_move = (node_from, node_to)
                        S.undo()
                if round(best_cost, 2) < round(S.cost, 2):
                    S.one_opt(best_move[0], best_move[1])
                else:
                    break
            
            # Neighborhood Change
            if round(S.cost, 2) < round(S0.cost, 2):
                S0 = Solution(instance, S.solution)
                k = 1
            else:
                S = Solution(instance, S0.solution)
                k += 1
            
    return S
