from cost import cable_cost, intersect

class Solution:
    def __init__(self, instance, solution, M1=1e9, M2=1e9, M3=1e9, M4=1e10):
        self._instance = instance
        self._M1 = M1
        self._M2 = M2
        self._M3 = M3
        self._M4 = M4

        self._node_up = [None for _ in instance.nodes]
        self._node_down = [set() for _ in instance.nodes]
        self._node_power = [None for _ in instance.nodes]
        self._cables_cost = 0
        self._subst_conn = 0
        self._crossings = 0

        self._checkpoint = [
            self._cables_cost,
            self._subst_conn,
            self._crossings,
            None,
            None,
            self._node_power.copy()
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
                if (
                    solution[i][0][0] == solution[j][0][1] or
                    solution[i][0][1] == solution[j][0][0] or
                    solution[i][0][1] == solution[j][0][1]
                    ): continue
                self._crossings += intersect(
                    instance.nodes[solution[i][0][0]],
                    instance.nodes[solution[i][0][1]],
                    instance.nodes[solution[j][0][0]],
                    instance.nodes[solution[j][0][1]])

    @property
    def instance(self):
        return self._instance
    
    # It is not necessary to compute if the solution is a proper tree
    # as we take care of it for every step of manipulation
    @property
    def cost(self):
        return (
            self._cables_cost +
            self._M2*max(0, self._subst_conn-self._instance.C) +
            self._M3*self._crossings
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

    def _change_edge(self, node_a, node_b):
        self._node_down[self._node_up[node_a]].remove(node_a)
        self._node_up[node_a] = node_b
        self._node_down[node_b].add(node_a)

    def save(self, node):
        self._checkpoint[0] = self._cables_cost
        self._checkpoint[1] = self._subst_conn
        self._checkpoint[2] = self._crossings
        self._checkpoint[3] = node
        self._checkpoint[4] = self._node_up[node]
        self._checkpoint[5] = self._node_power.copy()
    
    def undo(self):
        self._cables_cost = self._checkpoint[0]
        self._subst_conn = self._checkpoint[1]
        self._crossings = self._checkpoint[2]
        self._change_edge(self._checkpoint[3], self._checkpoint[4])
        self._node_power = self._checkpoint[5]
    
    def is_in_cc(self, node_a, node_b):
        if node_a == node_b: return True
        for node in self._node_down[node_a]:
            if self.is_in_cc(node, node_b): return True
        return False
    
    def one_opt(self, node_a, node_b):
        node = self._node_up[node_a]
        self._cables_cost -= cable_cost(self._instance, node_a, node, self._node_power[node_a], self._M1)
        while node != 0:
            next_node = self._node_up[node]
            self._cables_cost -= cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            self._node_power[node] -= self._node_power[node_a]
            self._cables_cost += cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            node = next_node
        node = node_b
        self._cables_cost += cable_cost(self._instance, node_a, node, self._node_power[node_a], self._M1)
        while node != 0:
            next_node = self._node_up[node]
            self._cables_cost -= cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            self._node_power[node] += self._node_power[node_a]
            self._cables_cost += cable_cost(self._instance, node, next_node, self._node_power[node], self._M1)
            node = node = next_node
        
        self._subst_conn -= self._node_up[node_a] == 0
        self._subst_conn += node_b == 0

        for i in range(1, self._instance.n+1):
            if (
                i == node_a or
                i == self._node_up[node_a] or
                self._node_up[i] == node_a or
                self._node_up[i] == self._node_up[node_a]
                ): continue
            self._crossings -= intersect(
                self._instance.nodes[node_a],
                self._instance.nodes[self._node_up[node_a]],
                self._instance.nodes[i],
                self._instance.nodes[self._node_up[i]])

        self._change_edge(node_a, node_b)

        for i in range(1, self._instance.n+1):
            if (
                i == node_a or
                i == self._node_up[node_a] or
                self._node_up[i] == node_a or
                self._node_up[i] == self._node_up[node_a]
                ): continue
            self._crossings += intersect(
                self._instance.nodes[node_a],
                self._instance.nodes[node_b],
                self._instance.nodes[i],
                self._instance.nodes[self._node_up[i]])
