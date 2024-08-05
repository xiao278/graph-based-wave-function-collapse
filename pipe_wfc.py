from cWFC import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PipeGen:
    def __init__(self, size:tuple[int]):
        states = ['N','H','V','C','F','G']
        # N is for blank, H is horizontal pipe, V is vertical pipe, C is junction pipe, and F and G are special states for the guide nodes in place of N
        adjacencyRules = {
            'N': ['N','F','G'],
            'H': ['H','C','G'],
            'V': ['V','C','F'],
            'C': ['C','V','H'],
            'F': ['N','V'], # F: NNNNVNNNNVNVVNNN
            'G': ['N','H'], # G: (NNNNNHNNHNNHHHN)^T
        }
        # states = ['0','1','2','3']
        # adjacencyRules = {
        #     '0': ['0'],
        #     '1': ['1'],
        #     '2': ['2'],
        #     '3': ['3'],
        # }
        self.wfc = WaveFunctionCollapse(states, adjacencyRules)
        self.size = size # (row, column)

        # set up 'guide' nodes
        for row in range(size[0]):
            name = "h%d" % (row)
            self.wfc.addNode(name, ('F', 'H'))
        for col in range(size[1]):
            name = "v%d" % (col)
            self.wfc.addNode(name, ('G', 'V'))

        for row in range(size[0]):
            for col in range(size[1]):
                name = "%d,%d" % (row, col)
                self.wfc.addNode(name, ('N','H','V','C'))
                # if row > 0:
                #     self.wfc.addEdge(name, "%d,%d" % (row - 1, col))
                # if col > 0:
                #     self.wfc.addEdge(name, "%d,%d" % (row, col - 1))
                self.wfc.addEdge(name, "h%d" % (row))
                self.wfc.addEdge(name, "v%d" % (col))
        self.wfc.save_initial()
    
    def generate(self):
        self.wfc.solve()

    def as_mat(self):
        mat = np.full(self.size, "?")
        for name, node in self.wfc.nodes.items():
            if name[0] == 'v' or name[0] == 'h':
                continue
            row, col = name.split(",")
            row = int(row)
            col = int(col)
            if node.collapsed is not None:
                mat[row,col] = node.collapsed
        return mat

    def __str__(self):
        return self.as_mat().__str__()
             

if __name__ == "__main__":
    p = PipeGen((4,4))
    p.generate()
    print(p)
    # mat = p.as_mat().astype(int)
    # np.savetxt("classic WFC/result_save.txt", mat, fmt="%10.0f")
    # plt.imshow(mat)
    # plt.waitforbuttonpress()


