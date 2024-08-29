from cWFC import *
import numpy as np

class Sudoku:
    def __init__(self, size):
        self.size = size
        assert np.sqrt(self.size) - int(np.sqrt(self.size)) < 0.0001
        states = [str(num + 1) for num in range(size)]
        adjacency_rules = dict()
        for state in states:
            adj_states = states.copy()
            adj_states.remove(state)
            adjacency_rules[state] = adj_states
        self.wfc = WaveFunctionCollapse(states, adjacency_rules)
        
        for row in range(self.size):
            for col in range(self.size):
                name = "%d,%d" % (row, col)
                self.wfc.addNode(name)

        # connect cells with the other ones on its row and col
        for row in range(self.size):
            for col in range(self.size):
                name = "%d,%d" % (row, col)
                for r in range(self.size):
                    if r != row:
                        self.wfc.addEdge(name, "%d,%d" % (r, col))
                for c in range(self.size):
                    if c != col:
                        self.wfc.addEdge(name, "%d,%d" % (row, c))

        # group cells into squares
        square_size = int(np.sqrt(self.size))
        for start_row in range(0, self.size, square_size):
            for start_col in range(0, self.size, square_size):
                for row in range(square_size):
                    for col in range(square_size):
                        name = "%d,%d" % (row + start_row, col + start_col)
                        for r in range(square_size):
                            for c in range(square_size):
                                if r != row and c != col:
                                    self.wfc.addEdge(name, "%d,%d" % (r + start_row, c + start_col))

        self.wfc.save_initial()
    
    def generate(self):
        self.wfc.solve()

    def as_mat(self):
        mat = np.full((self.size, self.size), "?")
        for name, node in self.wfc.nodes.items():
            row, col = name.split(",")
            row = int(row)
            col = int(col)
            if node.collapsed is not None:
                mat[row,col] = node.collapsed
        return mat

    def __str__(self):
        return self.as_mat().__str__()
    

if __name__ == "__main__":
    p = Sudoku(9)
    p.generate()
    print(p)

    
