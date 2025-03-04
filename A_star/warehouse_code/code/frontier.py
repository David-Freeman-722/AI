# Contains the frontier for the A* search.  Stores nodes which are tuples of grid locations 
# along with their individual cost from the starting node

from node import Node
# from queue import Queeue

class Frontier:
    def __init__(self, start_node):
        self.queue: list[Node] = [start_node] # Holds a queue of nodes
        self.size: int = 1
    
    # Adds a node to the priority queue frontier
    def add_node(self, node: Node):
        self.queue.append(node)
        self.queue.sort(key=lambda n: n.cost) # Sorts list based on cost

    # Removes node from frontier priority queue (occurs when the node is chosen)
    def remove_node(self, cost, position):
        self.queue.remove((cost, position))
        self.size -= 1
        
    # Returns the queue of neighbors
    def getFrontier(self):
        return self.queue
    
    