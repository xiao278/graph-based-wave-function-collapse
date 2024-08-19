from heapq import *
import random
import copy

class Node:
    def __init__(self, name:str, states:'list[str]', assign:'str|tuple[str]|None'=None, priority_modifier:int=0):
        states = states.copy()
        self.possible_states:dict[str,bool] = dict()
        if type(assign) == tuple:
            for s in states:
                self.possible_states[s] = False
            for s in assign:
                self.possible_states[s] = True
        else:
            for s in states:
                self.possible_states[s] = (assign is None)
        self.collapsed:str|None = (assign if type(assign) == str else None)
        self.state_count:int = len(assign) if (type(assign) == tuple) else len(states)
        self.priority_modifier:int = priority_modifier
        self.name = name
    
    def num_states(self) -> int:
        return self.state_count + self.priority_modifier + (0 if self.collapsed is None else len(self.possible_states))
    
    def update_possible_states(self, state:str) -> bool:
        # returns True if the possible state is updated, otherwise false

        if self.collapsed is not None:
            return False

        prev_possible = self.possible_states[state]
        self.possible_states[state] = False
        if prev_possible:
            self.state_count -= 1
            assert self.state_count > 0
        return prev_possible
    
    def collapse(self) -> bool:
        if self.collapsed is not None:
            return False
        
        assert self.state_count > 0
        
        possible_states:list[str] = []
        for state, possible in self.possible_states.items():
            if possible:
                possible_states.append(state)
                self.possible_states[state] = False
        
        self.collapsed = possible_states[random.randrange(len(possible_states))]
        return True

    def __lt__(self, node:'Node'):
        return self.num_states() < node.num_states()
    
    def __str__(self):
        return "{%s | %s | %d}" % (self.name, self.collapsed, self.num_states())
        

class NodeSort:
    def __init__(self, states:'list[str]'):
        self.states = states
        self.node_bucket:dict[str,int] = dict()
        self.buckets:tuple[set[str]] = tuple(set() for _ in range(len(states) + 1)) # buckets to store node names in

    def add(self, node:Node):
        assert node.name not in self.node_bucket
        possible_states = max(min(node.num_states(), len(self.states)), 0) # clamp value so no index out of range
        self.buckets[possible_states] = node.name
        self.node_bucket[node.name] = possible_states

    def remove(self, node_name:str):
        if node_name in self.node_bucket:
            bucket = self.node_bucket[node_name]
            del self.node_bucket[node_name]
            self.buckets[bucket].remove(node_name)
    
    def update(self, node:Node):
        assert node.name in self.node_bucket
        bucket = self.node_bucket[node.name]
        self.buckets[bucket].remove(node.name)
        new_bucket = max(min(node.num_states(), len(self.states)), 0)
        self.node_bucket[node.name] = new_bucket
        self.buckets[new_bucket] = node.name

    def pop(self):
        for bucket in self.buckets:
            if len(bucket) != 0:
                item = bucket.pop()
                del self.node_bucket[item]



        

class WaveFunctionCollapse:
    def __init__(self, states:'list[str]', adjacencyAllow:'dict[str,list[str]]'):
        self.states = states.copy()
        self.nodes:dict[str,Node] = dict()
        self.uncertain_nodes:list[Node] = []
        self.adjacencyList:dict[str,set[str]] = dict()
        self.adjacencyAllow = adjacencyAllow.copy()
        self.adjacencyBan:dict[str,list[str]] = dict() # what states are not allowed to be adjacent to each other, the inverse of adj
        
        self.nodes_initial:dict[str,Node] = None
        self.uncertain_nodes_initial:list[Node] = None

        for state, adj_states in self.adjacencyAllow.items():
            # compile the list of banned states not allowed to be adjacent to each other
            adj_ban_states = self.states.copy()
            for adj_state in adj_states:
                adj_ban_states.remove(adj_state)
            self.adjacencyBan[state] = adj_ban_states
    
    def addNode(self, name:str, assign:'str|tuple[str]|None'=None, priority_modifier:int=0):
        # positive priority modifier means lower priority
        node = Node(name, self.states, assign, priority_modifier)
        self.nodes[name] = node
        self.adjacencyList[name] = set()
        if type(assign) != str:
            heappush(self.uncertain_nodes, node)

    def addEdge(self, node1_name:str, node2_name:str):
        assert node1_name in self.nodes
        assert node2_name in self.nodes
        assert (node1_name in self.adjacencyList[node2_name]) == (node2_name in self.adjacencyList[node1_name])

        if node1_name in self.adjacencyList[node2_name]:
            return False

        self.adjacencyList[node1_name].add(node2_name)
        self.adjacencyList[node2_name].add(node1_name)

    def save_initial(self):
        self.nodes_initial = copy.deepcopy(self.nodes)
        self.uncertain_nodes_initial = []
        for name, node in self.nodes_initial.items():
            if node.collapsed is None:
                heappush(self.uncertain_nodes_initial, node)

    def load_initial(self):
        self.nodes = copy.deepcopy(self.nodes_initial)
        self.uncertain_nodes = []
        for name, node in self.nodes.items():
            if node.collapsed is None:
                heappush(self.uncertain_nodes, node)

    # @profile
    def assert_adjacency_rule(self, name:str, state:str):
        assert state in self.states
        neighbors = self.adjacencyList[name]
        ban_states = self.adjacencyBan[state]

        for nb in neighbors:
            for s in ban_states:
                nb_node = self.nodes[nb]
                if nb_node.collapsed is None:
                    nb_node.update_possible_states(s)

        heapify(self.uncertain_nodes)

    def propagate(self):
        node = heappop(self.uncertain_nodes)
        name = node.name
        try:
            success = node.collapse()
            if not success:
                print("Collapse of node %s Failed (Already collapsed)" % (name))
            else:
                self.assert_adjacency_rule(name, node.collapsed)
            return True
        except Exception as error:
            # print(error, node)
            return False
    
    def solve(self):
        while len(self.uncertain_nodes) > 0:
            success = self.propagate()
            if not success:
                # print("Fail---------")
                # for name, node in self.nodes.items():
                #     print(node)
                self.load_initial()
                

    


if __name__ == '__main__':
    NodeSort(['a','b','c'])
    pass



    



        
            
            