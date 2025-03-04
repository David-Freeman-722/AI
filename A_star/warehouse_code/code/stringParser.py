import warehouse
import config

w=warehouse.w
scale=config.scale

forkliftInWarehouse = False

# input: warehouse template
# output: 2D array of [0,0],"x",False] cells to be
#         filled in later
#name:
#args:
#returns:
#effect:
def createEmptyMatrix(w):
    m=[]
    for row in range (len(w)):
        n=[]
        for col in range(len((w[row])[0])):
            n.append([[0,0],"x",False])
        m.append(n)
    return m
#input: warehouse template
#output: [['x', '', ''......]....]

#name:
#args:
#returns:
#effect:
def splitTemplateRowsIntoDistinctListsOfSingleCharacters(input):
    matrix = []
    for row in range(len(input)):
        for col in range(len(input[0])):
            matrix.append(list(map(str, (input[row])[col])))

    return matrix

#name:
#args:
#returns:
#effect:
def assignCoordinates(row,column):
    hCoord = column*scale
    vCoord = row*scale
    return[hCoord,vCoord]
# set boolean forkliftAdded to True for first forklift
# raise Exception if second forklift is found in template
def checkForForklift(type):
    if not config.forkliftInWarehouse and type == 'f':
            config.forkliftInWarehouse = True

# input: list of single characters, empty matrix
# output: matrix with all fields complete
#name:
#args:
#returns:
#effect:
def addDetailsToMatrix(listOfSingleCharacters,emptyMatrix):
    numRowsinEmptyMatrix = len(emptyMatrix)
    numColumnsinEmptyMatrix = len(emptyMatrix[0])
    for row in range(numRowsinEmptyMatrix):
        for col in range(numColumnsinEmptyMatrix):
            ((emptyMatrix[row])[col])[0]=assignCoordinates(row,col)
            checkForForklift(listOfSingleCharacters[row][col])
            ((emptyMatrix[row])[col])[1]=listOfSingleCharacters[row][col]
            ((emptyMatrix[row])[col])[2]=False
    finalMatrix=emptyMatrix
    if not config.forkliftInWarehouse:
        raise Exception("You must add a forklift to the warehouse.")
    return finalMatrix

emptyMatrix = createEmptyMatrix(w)

listOfSingleCharacters = splitTemplateRowsIntoDistinctListsOfSingleCharacters(w)
#name:
#args:
#returns:
#effect:
def getMatrix():
    config.warehouse = addDetailsToMatrix(listOfSingleCharacters,emptyMatrix)
    return config.warehouse
getMatrix()

#name:
#args:
#returns:
#effect:
def getInitialForkliftCoordinates():
    #temp = getMatrix()
    for row in config.warehouse:
        for col in row:
            if col[1]=='f':
                tempCol = (col[0])[0]
                tempRow = (col[0])[1]
                return [int(tempCol/config.scale),int(tempRow/config.scale)]
#name:
#args:
#returns:
#effect:
def getListOfWalls():
    listOfWalls = []
    ID=1
    #temp = getMatrix()
    for row in config.warehouse:
        for col in row:
            if col[1]=='w':
                listOfWalls.append(col)
    return listOfWalls

#name:
#args:
#returns:
#effect:
def getListOfBoxes():
    listOfBoxes = []
    ID=1
    #temp = getMatrix()
    for row in config.warehouse:
        for col in row:
            if col[1][0]=='b':
                listOfBoxes.append(col)
    return listOfBoxes

#name:
#args:
#returns:
#effect:
def getListOfEmptyCells():
    listOfEmptyCells = []
    ID=1
    #temp = getMatrix()
    for row in config.warehouse:
        for col in row:
            if col[1][0]=='e':
                listOfEmptyCells.append(col)
    return listOfEmptyCells

def queryWarehouse(row,col):
    cellType=(((config.warehouse[row])[col])[1])
    queriedCell=[col*config.scale,row*config.scale]
    if not(queriedCell in config.queriedCells):    
        config.queriedCells.append(queriedCell)
    return cellType



