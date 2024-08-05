from cWFC import *
import numpy as np
import matplotlib.pyplot as plt

class CheckerGen:
    def __init__(self, size:tuple[int]):
        states = ['B','W']
        # N is for blank, H is horizontal pipe, V is vertical pipe, C is junction pipe, and F and G are special states for the guide nodes in place of N
        adjacencyRules = {
            'B': ['W'],
            'W': ['B']
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
                if color == 'B':
                    mat[row,col,:] = (0,0,0)
                if color == 'W':
                    mat[row,col,:] = (255,255,255)

        plt.imshow(mat)
        plt.waitforbuttonpress()

if __name__ == "__main__":
    p = CheckerGen((12,12))
    p.generate()
    p.show_img()