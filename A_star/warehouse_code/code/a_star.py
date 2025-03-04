# Has code for the A* algorithm to run

import warehouse
import stringParser
from node import Node
from frontier import Frontier

w = warehouse.w
w_char_list = stringParser.splitTemplateRowsIntoDistinctListsOfSingleCharacters(w)

# Gets the coordinates of where the forklift starts
def getInitialForkliftCoordinates():
    for row in w_char_list:
        for col in row:
            if col=='f':
                col_index = row.index(col)
                row_index = w_char_list.index(row)
                return (col_index, row_index)
            
original_fork_position = getInitialForkliftCoordinates()
# original_starting_node = Node()

# gets the coordinates of the boxes inside of the grid
def getBoxCoordinates():
    boxes = []
    for row in w_char_list:
        for col in row:
            if col=='b':
                col_index = row.index(col)
                row_index = w_char_list.index(row)
                box = (row_index, col_index)
                boxes.append(box)
    
    return boxes

box_coords = getBoxCoordinates()
# print(box_coords)

## TEMP COORDS  WILL LOOP THRU BOX COORDINATES NEXT
pos1 = (0,2)
goal1 = (1, 13)

bumpers = {'North': False, 'South': False, 'East': False, 'West': False}

# Calculates Manhattan distance between input node positions and the goal position
def h(node_position: tuple, goal: tuple):
    node_row = node_position[0]
    node_col = node_position[1]
    goal_row = goal[0]
    goal_col = goal[1]
    manhattan_row_dist = abs(goal_row-node_row)
    manhattan_col_dist = abs(goal_col-node_col)
    return (manhattan_row_dist, manhattan_col_dist)

# Calculates the total cost to get from the initial start to the current node
def g(initial_position: tuple, node_position: tuple):
    i_row = initial_position[0]
    i_col = initial_position[1]
    node_row = node_position[0]
    node_col = node_position[1]
    current_cost_row = abs(i_row-node_row)
    current_cost_col = abs(i_col-node_col)
    return (current_cost_row, current_cost_col)

def f(starting_position: tuple, node_position: tuple, goal_position: tuple):
    h_cost = h(node_position, goal_position)
    g_cost = g(starting_position, node_position)
    print(f"H cost {h_cost}")
    print(f"G cost {g_cost}")
    row_cost = h_cost[0] + g_cost[0] # Adds together row costs
    col_cost = h_cost[1] + g_cost[1] # Adds together col costs
    cost = (row_cost, col_cost)
    return cost

start_node = Node(f(original_fork_position, original_fork_position, goal1), original_fork_position)
# print(i_node)

# # Expand the frontier with adjacent nodes.  Looks to see if there are walls around it.
# print(stringParser.getMatrix())
def check_adjacent_cells(node: Node):
    directions = {"N": (-1, 0), "S": (1,0), "E": (0,1), "W": (0,-1),
                "NW": (-1,-1), "NE": (-1,1), "SW": (1,-1), "SE":(1,1)}
    valid_types = ['e', 'b']
    valid_cells = []
    for change in directions.values():
        checked_row = change[0] + node.row
        checked_col = change[1] + node.col
        cell_type = stringParser.queryWarehouse(checked_row, checked_col)
        if cell_type in valid_types:
            valid_cells.append((checked_row, checked_col))
            
    return valid_cells

adj_cells = check_adjacent_cells(start_node)
frontier = Frontier(start_node)
def expand_frontier(frontier: Frontier, neighbors: list[tuple]):
    for neighbor_position in neighbors:
        # if frontier.size == 0:
        #     start_node = Node(f(original_fork_position, original_fork_position, goal1), original_fork_position)
        #     frontier.add_node(start_node)
        #  Add accessible adjecent nodes to the frontier.  Check to see if you can move in them first
        cost = f(original_fork_position, neighbor_position, goal1)
        print(f"Cost is {cost}")
        neighbor = Node(cost, neighbor_position)
        frontier.add_node(neighbor)
    
expand_frontier(frontier, adj_cells)
frontier_nodes = frontier.getFrontier()
breakpoint()