# Code to create node objects that contain a grid position and cost

class Node():
    def __init__(self, cost: tuple, position: tuple):
        self.cost = cost
        self.position = position
        self.row = position[0]
        self.col = position[1]