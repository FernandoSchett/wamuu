from cost import cost, cable_cost, intersect

class Solution:
    def __init__(self, instance, solution, cost_parameters={}):
        self._instance = instance
        self._M1 = cost_parameters.get('M1') or 1e9
        self._M2 = cost_parameters.get('M2') or 1e9
        self._M3 = cost_parameters.get('M3') or 1e9
        self._M4 = cost_parameters.get('M4') or 1e10
        self._cost = cost(instance, solution, self._M1, self._M2, self._M3, self._M4)

        self._node_up = [None for _ in instance.nodes]
        self._node_down = [set() for _ in instance.nodes]
        self._node_power = [None for _ in instance.nodes]
        self._cables_cost = 0
        self._subst_conn = 0
        self._crossings = 0

        self._checkpoint = [
            self._cost,
            self._node_up.copy(),
            self._node_down.copy(),
            self._node_power.copy(),
            self._cables_cost,
            self._subst_conn,
            self._crossings
        ]
        
        for x in solution:
            a, b = x[0]
            self._node_up[a] = b
            self._node_down[b].add(a)
            self._node_power[a] = x[1]
            self._cables_cost += cable_cost(instance, a, b, x[1], self._M1)
            self._subst_conn += b == 0
        
        for i in range(len(solution)):
            for j in range(i+1, len(solution)):
                self._crossings += intersect(
                    instance.nodes[solution[i][0][0]],
                    instance.nodes[solution[i][0][1]],
                    instance.nodes[solution[j][0][0]],
                    instance.nodes[solution[j][0][1]])

    @property
    def instance(self):
        return self._instance
    
    @property
    def cost(self):
        return (
            self._cables_cost +
            self._M2*max(0, self._subst_conn-self._instance.C) +
            self._M3*self._crossings
            # It is not necessary to compute if the solution is a proper tree
            # as we take care of it for every step of manipulation
            # self._M4*self._is_proper_tree()
        )
    
    @property
    def node_up(self):
        return self._node_up
    
    @property
    def node_down(self):
        return self._node_down
    
    @property
    def node_power(self):
        return self._node_power
    
    # def _is_proper_tree(self):
    #     vis = [False for _ in self._instance.nodes]
    #     def dfs(node):
    #         if vis[node]: return
    #         vis[node] = True
    #         for x in self._node_down[node]:
    #             dfs(x)
    #     dfs(0)
    #     return sum(vis) == self._instance.n+1

    def create_checkpoint(self):
        self._checkpoint[0] = self._cost,
        self._checkpoint[1] = self._node_up.copy(),
        self._checkpoint[2] = self._node_down.copy(),
        self._checkpoint[3] = self._node_power.copy(),
        self._checkpoint[4] = self._cables_cost,
        self._checkpoint[5] = self._subst_conn,
        self._checkpoint[6] = self._crossings
    
    def restore(self):
        self._cost = self._checkpoint[0]
        self._node_up = self._checkpoint[1]
        self._node_down = self._checkpoint[2]
        self._node_power = self._checkpoint[3]
        self._cables_cost = self._checkpoint[4]
        self._subst_conn = self._checkpoint[5]
        self._crossings = self._checkpoint[6]
    
    def is_in_cc(self, node_a, node_b):
        def dfs_down(node_to_find, curr_node):
            if node_to_find == curr_node: return True
            for node in self._node_down[curr_node]:
                if dfs_down(node_to_find, node): return True
            return False
        return dfs_down(node_a, node_b)
    
    def one_opt(self, node_a, node_b):
        node = self._node_up[node_a]
        self._cost -= cable_cost(self._instance, node_a, node, self._node_power[node_a], self._M1)
        while node != 0:
            next_node = self._node_up[node]
            self._cost -= cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            self._node_power[node] -= self._node_power[node_a]
            self._cost += cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            node = next_node
        node = node_b
        self._cost += cable_cost(self._instance, node_a, node, self._node_power[node_a], self._M1)
        while node != 0:
            next_node = self._node_up[node]
            self._cost -= cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            self._node_power[node] += self._node_power[node_a]
            self._cost += cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            node = node = next_node
        
        self._subst_conn -= self._node_up[node_a] == 0
        self._subst_conn += node_b == 0

        for i in range(1, self._instance.n+1):
            self._crossings -= intersect(
                self._instance.nodes[node_a],
                self._instance.nodes[self._node_up[node_a]],
                self._instance.nodes[i],
                self._instance.nodes[self._node_up[i]])

        self.node_up[node_a] = node_b
        self.node_down[node_b].add(node_a)

        for i in range(1, self._instance.n+1):
            self._crossings += intersect(
                self._instance.nodes[node_a],
                self._instance.nodes[node_b],
                self._instance.nodes[i],
                self._instance.nodes[self._node_up[i]])
