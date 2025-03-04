import config

#SETTINGS:

config.scale = 40 #determines the side length of a cell in pixels
config.fps = 8   #determines the animation speed in frames per second
config.showPath = False# set to True to shade the cells which have been visited by the forklift

import stringParser
import display


#API:             #*****************************************************************************************
                  #                                                                                        *
                  # name:    display.getInitialForkliftCoordinates()                                               *
                  # args:    none                                                                          *
                  # returns: return initial forklift coordinates by row and column in the form [<row>,<column>]             *
                  #                                                                                        *
                  # ****************************************************************************************
                  #                                                                                        *
                  # name:    stringParser.queryWarehouse(<row>,<column>)                                   *
                  # args:    position of cell being queried by row and column                              *
                  # returns: category of cell being queried as one of 'w','b',or 'e'                       *
                  #                                                                                        *
                  #*****************************************************************************************
                  #                                                                                        *
                  # name:    stringParser.getListOfBoxes()                                                 *
                  # args:    none                                                                          *
                  # returns: list of box cells                                                             *
                  #                                                                                        *
                  #*****************************************************************************************


#EXAMPLES:

#print(stringParser.queryWarehouse(0,2))
#print(stringParser.queryWarehouse(2,1))
#print(stringParser.queryWarehouse(3,2))
#print(stringParser.getListOfBoxes())

#print(stringParser.getInitialForkliftCoordinates())


#STUDENT CODE GOES HERE

stringParser.queryWarehouse(1,0)
stringParser.queryWarehouse(2,1)
stringParser.queryWarehouse(3,2)
stringParser.queryWarehouse(3,2)

config.commandList = [
 ['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','E'],
['move','W'],
['move', 'SW'],
['move','E'],
['move', 'S'],
['move', 'S'],
['move', 'S'],
['move', 'S'],
['lift',3],
['move', 'N'],
['move', 'N'],
['move', 'N'],
['move', 'N'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['move', 'W'],
['drop', 'NW'],
['move','S'],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['lift', 2],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['move', 'E'],
['lift', '1'],# tests that the forklift will not lift more than one box at a time
['move','S'],
['move','W'],
['move','W'],
['move','W'],
['move','W'],
['move','N'],
['move','N'],
['move','N'],
['move','W'],
['move','W'],
['move','W'],
['move','W'],
['move','W'],
['move','W'],
['move','W'],
['drop','W'],
]






# DO NOT CHANGE THE CODE BELOW THIS LINE
display.main(config.commandList)



