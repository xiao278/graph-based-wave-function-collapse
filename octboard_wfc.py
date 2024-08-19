from cWFC import WaveFunctionCollapse
import matplotlib.pyplot as plt
import numpy as np
import graphviz

class OctCheckerGen:
    def __init__(self, size:tuple[int]):
        states = ['A','B','C','D']
        # N is for blank, H is horizontal pipe, V is vertical pipe, C is junction pipe, and F and G are special states for the guide nodes in place of N
        adjacencyRules = {
            'A': ['B','C','D'],
            'B': ['C','D','A'],
            'C': ['D','A','B'],
            'D': ['A','B','C']
        }

        self.wfc = WaveFunctionCollapse(states, adjacencyRules)
        self.size = size # (row, column)

        for row in range(size[0]):
            for col in range(size[1]):
                name = "%d,%d" % (row, col)
                self.wfc.addNode(name)
                if row > 0:
                    self.wfc.addEdge(name, "%d,%d" % (row - 1, col))
                    if col > 0:
                        self.wfc.addEdge(name, "%d,%d" % (row - 1, col - 1))
                    if col < size[1] - 1:
                        self.wfc.addEdge(name, "%d,%d" % (row - 1, col + 1))
                if col > 0:
                    self.wfc.addEdge(name, "%d,%d" % (row, col - 1))

        self.wfc.save_initial()
    
    def generate(self):
        self.wfc.solve()

    def as_mat(self):
        mat = np.full(self.size, "?")
        for name, node in self.wfc.nodes.items():
            row, col = name.split(",")
            row = int(row)
            col = int(col)
            if node.collapsed is not None:
                mat[row,col] = node.collapsed
        return mat

    def __str__(self):
        return self.as_mat().__str__()

    def show_img(self):
        rows, cols = self.size
        mat = np.full((rows, cols, 3), (-1,-1,-1))
        for row in range(rows):
            for col in range(cols):
                name = "%d,%d" % (row, col)
                color = self.wfc.nodes[name].collapsed
                assert color is not None
                if color == 'A':
                    mat[row,col,:] = (50,60,70)
                if color == 'B':
                    mat[row,col,:] = (255,128,128)
                if color == 'C': 
                    mat[row,col,:] = (128,255,128)
                if color == 'D':
                    mat[row,col,:] = (128,128,255)
        plt.imshow(mat)
        plt.waitforbuttonpress()

if __name__ == "__main__":
    p = OctCheckerGen((10,10))
    p.generate()
    p.show_img()