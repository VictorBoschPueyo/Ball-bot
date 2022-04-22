
class Node:
    def __init__(self, row, col, wall):
        position = (row, col)
        is_wall = wall # true/false
        neighbours = []
        
    def set_neighbourg(self, node):
        self.neighbours.append(node)
        


class Board:
    def __init__(self, nodes, height, width, frame):
        box_list = nodes
        size = (height, width)
        initial_frame = frame
        ball_position = self.ball_position(frame)
        pass
    
    def solve_maze(self):
        #############################################
        # Aquesta funció servirà per a calcular el
        # camí que la pilota ha de recorrer fins
        # arribar al final.
        # Retorna la direcció cap on ha d'anar la
        # pilota respecte on es troba
        #############################################
        pass
    
    def ball_position(self, frame):
        pass
    