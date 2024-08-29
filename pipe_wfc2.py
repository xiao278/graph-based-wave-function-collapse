from cWFC import *
import numpy as np
import matplotlib.pyplot as plt

# demonstration of using auxiliary nodes and states to denote direction

class PipeGen:
    def __init__(self, size:tuple[int], alt=False):
        # UP-RIGHT-DOWN-LEFT, so 0000 is blank, and 1111 is a cross, and 1100 is a vertical line
        
        self.direction_index = {
            'U': 0,
            'R': 1,
            'D': 2,
            'L': 3
        }

        self.index_direction = 'URDL'

        if alt:
            pipe_states = (
                # '0000', # blank tile
                '1100', '0110', '0011', '1001', # ╚, ╔, ╗, ╝
                '1010', '0101', # ║, ═
                # '0111', '1011', '1101', '1110', # ╦, ╣, ╩, ╠
                # '1111', # ╬
            )
        else:
            pipe_states = (
                '0000', # blank tile
                '1100', '0110', '0011', '1001', # ╚, ╔, ╗, ╝
                '1010', '0101', # ║, ═
                '0111', '1011', '1101', '1110', # ╦, ╣, ╩, ╠
                '1111', # ╬
            )
        
        aux_states = (
            'U1', 'U0',
            'R1', 'R0',
            'D1', 'D0',
            'L1', 'L0'
        )

        states = list(pipe_states + aux_states)
                
        adjacencyRules:dict[str,list[str]] = dict()

        for pipe_state in pipe_states:
            adjacencyRules[pipe_state] = ['U%s' % pipe_state[0], 'R%s' % pipe_state[1], 'D%s' % pipe_state[2], 'L%s' % pipe_state[3]]

        for aux_state in aux_states:
            dir = aux_state[0]
            dir_idx = self.direction_index[dir]
            has = aux_state[1]
            temp_list = []
            opposite_dir = self.index_direction[(dir_idx + 2) % len(self.direction_index)]
            temp_list.append("%s%s" % (opposite_dir, has))
            for pipe_state in pipe_states:
                pipe_has = pipe_state[dir_idx]
                if pipe_has == has:
                    temp_list.append(pipe_state)
            adjacencyRules[aux_state] = temp_list

        # [print(k,v) for k,v in adjacencyRules.items()]

        self.wfc = WaveFunctionCollapse(states, adjacencyRules)
        self.size = size # (row, column)

        for row in range(size[0]):
            for col in range(size[1]):
                name = "%d,%d" % (row, col)
                self.wfc.addNode(name, pipe_states)
                for dir in self.index_direction:
                    self.wfc.addNode("$" + dir + name, (dir + "0", dir + "1"))
                    self.wfc.addEdge("$" + dir + name, name)
                if row > 0:
                    up_neighbor = "%d,%d" % (row - 1, col)
                    self.wfc.addEdge("$U" + name, "$D" + up_neighbor)
                if col > 0:
                    left_neighbor = "%d,%d" % (row, col - 1)
                    self.wfc.addEdge("$L" + name, "$R" + left_neighbor)
        
        self.wfc.save_initial()

    def generate(self):
        self.wfc.solve()
    
    def show_img(self):
        rows, cols = self.size
        mat = np.full((rows * 3, cols * 3, 3), (255,255,255))
        for row in range(rows):
            for col in range(cols):
                if row % 2 == col % 2:
                    mat[row * 3: row * 3 + 3, col * 3: col * 3 + 3,:] = (213,223,249)
                name = "%d,%d" % (row, col)
                pipe_type = self.wfc.nodes[name].collapsed
                assert pipe_type is not None
                if pipe_type[0] == '1':
                    mat[row * 3: row * 3 + 2, col * 3 + 1,:] = (0,0,0)
                if pipe_type[2] == '1':
                    mat[row * 3 + 1: row * 3 + 3, col * 3 + 1,:] = (0,0,0)
                if pipe_type[1] == '1':
                    mat[row * 3 + 1, col * 3 + 1: col * 3 + 3,:] = (0,0,0)
                if pipe_type[3] == '1':
                    mat[row * 3 + 1, col * 3: col * 3 + 2,:] = (0,0,0)
                # if pipe_type == 'V' or pipe_type == 'C':
                #     # draw a vertical line
                #     mat[row * 3: row * 3 + 3, col * 3 + 1,:] = (0,0,0)

        plt.imshow(mat)
        plt.waitforbuttonpress()            

if __name__ == "__main__":
    p = PipeGen((10,10), True)
    p.generate()
    p.show_img()