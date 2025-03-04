import pygame
import stringParser
import warehouse
import config
pygame.init()


#name:  main
#args:  list of commands in the shape [[command1],[command2],.....,[command n]]
#returns: none
#effect:  sets up and runs the graphical display
def main(commandList):

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (100,100,100)

    # for possible use
    numberOfRemainingBoxes = len(stringParser.getListOfBoxes())

    # Set the width and height of the screen [width, height]
    SCREEN_WIDTH = config.scale*len(stringParser.emptyMatrix[0])
    SCREEN_HEIGHT = config.scale*len(stringParser.emptyMatrix)



    class EmptyCell(pygame.sprite.Sprite):
        def __init__(self, color, width, height,x,y):
            super().__init__()

            # Create a cell with specified color,width,height,x coordinate and y coordinate
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


        #flag for changing color of visited cells
        # name: isDropOffZone
        # args:  coordinates of forklift
        # returns:  True if forklift coordinates equal drop off zone coordinates , False otherwise
        # effect:

        def isDropOffZone(self,fx,fy):
            return (fx==config.initialForkliftX and fy==config.initialForkliftY)

        # name:
        # args:  coordinates of forklift and coordinates of an empty cell
        # returns:  True if two sets of coordinates have equal values , False otherwise
        # effect:
        def visitedByForklift(self,fx,fy,sx,sy):
            return (fx==sx and fy==sy)

        # name: display_query_symbol
        # args: EmptyCellObject
        # returns: none
        # effect: renders and asterisk in the empty cell
        def display_query_symbol(self):
            font = pygame.font.SysFont(None, 60)
            text_surface = font.render(' *', True, BLUE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


        def update(self,
                   nextForkliftXIncrement,
                   nextForkliftYIncrement,
                   forkliftX,
                   forkliftY,
                   boxID,
                   initialForkliftCoordinates,
                   forkliftHasBox
                   ):
           if config.showPath:
            if self.visitedByForklift(forkliftX,forkliftY,self.rect.x,self.rect.y):
                color = (200,200,200)
                self.image.fill(color)
            else:
                pass
           if self.isDropOffZone(forkliftX,forkliftY):
                color = (0,255,0)
                self.image.fill(color)
           else:
                pass


    class Wall(pygame.sprite.Sprite):
        def __init__(self, color, width, height,x,y):
            super().__init__()

            # Create a cell with specified color,width,height,x coordinate and y coordinate
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        # name:display_query_symbol()
        # args: none
        # returns: nothing
        # effect: displays an asterisk in every wall cell that has been queried
       # listOfCommands = config.commandList
        def display_query_symbol(self):
            font = pygame.font.SysFont(None, 60)
            text_surface = font.render(' *', True, BLUE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        # name:
        # args:
        # returns:
        # effect:
        def update(self,
                   nextForkliftXIncrement,
                   nextForkliftYIncrement,
                   forkliftX,
                   forkliftY,
                   boxID,
                   initialForkliftCoordinates,
                   forkliftHasBox
                   ):
            pass




    class Box(pygame.sprite.Sprite):
        def __init__(self, color, width, height,x,y,id):
            super().__init__()

            # Create a sprite with a specified color,width,height,x coordinate,y coordinate and ID
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.ID = id

        #listOfCommands = config.commandList
        commandIndex = 0

        # name: draw_number
        # args:  none
        # returns: nothing
        # effect: draws the id number of each box in the box cell


        def draw_number(self):
            font = pygame.font.SysFont(None, 30)
            text_surface = font.render(str(self.ID), True, GREEN)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        # name:display_query_symbol()
        # args: none
        # returns: nothing
        # effect: displays an asterisk in every box cell that has been queried
        def display_query_symbol(self):
            font = pygame.font.SysFont(None, 60)
            text_surface = font.render(' *', True, BLUE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        # name:
        # args:
        # returns:
        # effect:
        def update(self,
                   nextForkliftXIncrement,
                   nextForkliftYIncrement,
                   forkliftX,
                   forkliftY,
                   boxID,
                   initialForkliftCoordinates,
                   forkliftHasBox
                   ):

            # name:ForkliftIsAdjacentToSelf
            # args: screen coordinates of the forklift
            # returns: true if the forklift is adjacent to a box, false otherwise
            # effect: none
            def ForkliftIsAdjacentToSelf(self,forkliftXCord,forkLiftYCord):
                scale = config.scale
                return (
                        (forkliftXCord== self.rect.x-scale and forkLiftYCord==self.rect.y) or #E
                        (forkliftXCord== self.rect.x and forkLiftYCord==self.rect.y+scale) or #N
                        (forkliftXCord== self.rect.x + scale and forkLiftYCord==self.rect.y) or #W
                        (forkliftXCord== self.rect.x and forkLiftYCord==self.rect.y-scale)or #S

                        (forkliftXCord == self.rect.x - scale and forkLiftYCord == self.rect.y + scale) or #NE
                        (forkliftXCord == self.rect.x - scale and forkLiftYCord == self.rect.y - scale) or #SE
                        (forkliftXCord == self.rect.x +scale and forkLiftYCord == self.rect.y - scale) or #SW
                        (forkliftXCord == self.rect.x + scale and forkLiftYCord == self.rect.y + scale) #NW
                        )

            # name: IDmatch
            # args: ID number of a lift command
            # returns: true if command ID number matches the box ID number, false otherwise
            # effect:
            def IDmatch(self,liftCommandID):
               return self.ID==liftCommandID

            # name: forkLiftLiftsThisBox
            # args: box ID in a lift command, coordinates of the forklift
            # returns:True if the lift command ID number matches the
            #          ID number of the box and if the forklift is adjacent to the box
            #          False otherwise
            # effect: none
            def forkliftLiftsThisBox(self,liftCommandID,xCord,yCord):
                return ForkliftIsAdjacentToSelf(self,forkliftX,forkliftY) and IDmatch(self,liftCommandID)
            # if the forklift lifts a box, the box sprite removes itself from the sprite group
            if not forklift.hasBox:
                if forkliftLiftsThisBox(self,boxID,forkliftX,forkliftY):
                    forklift.hasBox = True
                    self.image.fill((0,255,0))
                    #self.kill()


    class Forklift(pygame.sprite.Sprite):
       # def __init__(self, height, width):
        def __init__(self,xcoord,ycoord):
            super().__init__()
            self.image = pygame.image.load("images/emptyForkliftE.png")
            self.image = pygame.transform.scale(self.image, (config.scale, config.scale))
            self.rect = self.image.get_rect()
            self.rect.x = xcoord
            self.rect.y = ycoord
            self.hasBox = False
            self.direction = 'E'
        def selectLoadedImage(self):
            match config.commandDirection:
                case 'N':
                    return "images/loadedForkliftN.png"
                case 'E':
                    return "images/loadedForkliftE.png"
                case 'W':
                    return "images/loadedForkliftW.png"
                case 'S':
                    return "images/loadedForkliftS.png"
                case 'NW':
                    return "images/loadedForkliftN.png"
                case 'NE':
                    return "images/loadedForkliftN.png"
                case 'SW':
                    return "images/loadedForkliftS.png"
                case 'SE':
                    return "images/loadedForkliftS.png"

        def selectEmptyImage(self):
            match config.commandDirection:
                case 'N':
                    return "images/emptyForkliftN.png"
                case 'E':
                    return "images/emptyForkliftE.png"
                case 'W':
                    return "images/emptyForkliftW.png"
                case 'S':
                    return "images/emptyForkliftS.png"
                case 'NW':
                    return "images/emptyForkliftN.png"
                case 'NE':
                    return "images/emptyForkliftN.png"
                case 'SW':
                    return "images/emptyForkliftS.png"
                case 'SE':
                    return "images/emptyForkliftS.png"



        def update(self,
                   nextForkliftXIncrement,
                   nextForkliftYIncrement,
                   forkliftX,
                   forkliftY,
                   boxID,
                   initialForkliftCoordinates,
                   forkliftHasBox
                   ):
            # Move the forklift
            self.rect.x += nextForkliftXIncrement
            self.rect.y += nextForkliftYIncrement
            config.FLx=self.rect.x
            config.FLy = self.rect.y
            if self.hasBox:
                self.image = pygame.image.load(self.selectLoadedImage())
                self.image = pygame.transform.scale(self.image, (config.scale, config.scale))

            else:
                self.image = pygame.image.load(self.selectEmptyImage())
                self.image = pygame.transform.scale(self.image, (config.scale, config.scale))


    # input:
    # name:
    # args:
    # returns:
    # effect:
    def parseCommand(direction ):

                match direction:
                    case'NONE':
                        return [0, 0]
                    case 'N':
                        return [0, -1 * config.scale]
                    case 'E':
                        return[config.scale,0]
                    case 'W':
                        return[-1*config.scale,0]
                    case 'S':
                        return[0,config.scale]
                    case 'NW':
                        return[-1*config.scale,-1*config.scale]
                    case 'NE':
                        return[config.scale,-1*config.scale]
                    case 'SW':
                        return[-1*config.scale,config.scale]
                    case 'SE':
                        return[config.scale,config.scale]

    # name:
    # args:
    # returns:
    # effect:
    def getCoordFromFloorPlan():

        #matrix = stringParser.getMatrix()
        for row in config.warehouse:
            for cell in row:
                if cell[1]=='f':
                    return cell[0]






    # Set up the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Warehouse")

    # Create a group of sprites
    config.sprite_group = pygame.sprite.Group()


    # fetch list of walls and list of boxes from floorplan
    listOfWalls=stringParser.getListOfWalls()
    listOfBoxes = stringParser.getListOfBoxes()
    listOfEmptyCells = stringParser.getListOfEmptyCells()

    # Create empty cells and add them to the group
    for x in range (0,len(listOfEmptyCells)):
        xcoord=((listOfEmptyCells[x])[0])[0]
        ycoord = ((listOfEmptyCells[x])[0])[1]
        sprite = EmptyCell(
            #WHITE,
            GREEN,
            config.scale, config.scale,
            xcoord,
            ycoord)
        config.sprite_group.add(sprite)

    # Create walls and add them to the group
    for x in range (0,len(listOfWalls)):
        xcoord=((listOfWalls[x])[0])[0]
        ycoord = ((listOfWalls[x])[0])[1]
        sprite = Wall(
            GREY,
            config.scale, config.scale,
            xcoord,
            ycoord)
        config.sprite_group.add(sprite)

    # Create boxes and add them to the group

    for x in range (0,len(listOfBoxes)):
        xcoord=((listOfBoxes[x])[0])[0]
        ycoord = ((listOfBoxes[x])[0])[1]

        sprite = Box(
            RED,
            config.scale, config.scale,
            xcoord,
            ycoord,
            x)

        config.sprite_group.add(sprite)

    config.initialForkliftX=(getCoordFromFloorPlan())[0]
    config.initialForkliftY=(getCoordFromFloorPlan())[1]


    # create empty cell to remain at the initial location of the forklift
    xcoord = config.initialForkliftX
    ycoord = config.initialForkliftY
    sprite = EmptyCell(
        (0,255,0),
        config.scale, config.scale,
        xcoord,
        ycoord)

    config.sprite_group.add(sprite)







    # create forklift and add it to the group
    forklift = Forklift(config.initialForkliftX, config.initialForkliftY)
    config.sprite_group.add(forklift)

    clock = pygame.time.Clock()


    commandIndex = 0
    # Main loop
    # name:
    # args:
    # returns:
    # effect:
    def actualDir():
        Dx = config.initialForkliftX
        Dy = config.initialForkliftY
        Fx = forklift.rect.x
        Fy = forklift.rect.y
        scale=config.scale

        if Dx==Fx+scale and Dy==Fy+scale:
            return 'SE'
        if Dx==Fx and Dy==Fy+scale:
            return 'S'
        if Dx==Fx-scale and Dy==Fy+scale:
            return 'SW'
        if Dx==Fx+scale and Dy==Fy:
            return 'E'
        if Dx==Fx-scale and Dy==Fy:
            return 'W'
        if Dx==Fx+scale and Dy==Fx-scale:
            return 'NE'
        if Dx==Fx and Dy==Fx-scale:
            return 'N'
        if Dx==Fx-scale and Dy==Fx-scale:
            return 'NW'

    # name:
    # args:
    # returns:
    # effect:
    def forkliftIsAdjacentoDropOffLocationInCorrectOrientation(commandDir):

        result = commandDir==actualDir()
        return result

    # name:
    # args:
    # returns:
    # effect:

    def hitWallCostIncrementor():
        #if config.forkliftHasMovedSinceLastHit:
            for s in config.sprite_group:
                if isinstance(s, Wall):
                    if config.FLx == s.rect.x and \
                        config.FLy == s.rect.y:
                        #config.forkliftHasMovedSinceLastHit=False
                        config.hitCost += 50


    forkliftHasBox=False
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Update all sprites


        if commandIndex >= len(commandList):
           pass
        else:
            boxID=1000
            command=commandList[commandIndex][0]



            match command:
                case 'move':
                    config.commandDirection= (commandList[commandIndex])[1]
                    delta = parseCommand((commandList[commandIndex])[1])
                    nextForkliftXIncrement = delta[0]
                    nextForkliftYIncrement = delta[1]
                    config.forkliftHasMovedSinceLast=True

                case 'lift':
                    boxID = commandList[commandIndex][1]
                    nextForkliftXIncrement = 0
                    nextForkliftYIncrement = 0
                case 'drop':
                    commandDirection = commandList[commandIndex][1]
                    if forkliftIsAdjacentoDropOffLocationInCorrectOrientation(commandDirection) :
                         forklift.hasBox = False
                    nextForkliftXIncrement = 0
                    nextForkliftYIncrement = 0


            config.sprite_group.update(
                nextForkliftXIncrement,
                nextForkliftYIncrement,
                forklift.rect.x,
                forklift.rect.y,
                boxID,
                getCoordFromFloorPlan(),
                forkliftHasBox
                )
            hitWallCostIncrementor()
            commandIndex+=1

        # Clear the screen
        screen.fill(WHITE)

        # Draw all sprites
        config.sprite_group.draw(screen)

        for s in config.sprite_group:
            if isinstance(s, Box):
                s.draw_number()



        for queried_cell in config.queriedCells:
                    for sprite_in_sprite_group in config.sprite_group:
                            if not isinstance(sprite_in_sprite_group,Forklift):
                                if sprite_in_sprite_group.rect.x == queried_cell[0] \
                                        and sprite_in_sprite_group.rect.y == queried_cell[1]:
                                    sprite_in_sprite_group.display_query_symbol()

        # Update the screen
        pygame.display.flip()

        # Limit frames per second
        clock.tick(config.fps)
        #clock.tick(1)

    def accumulateCosts():
        for command in config.commandList:
            dir = command[1]
            if (dir == 'N' or dir == 'E' or dir == 'S' or dir == 'W'):
                config.orthogonalMoveCost += 2
            elif (dir == 'NE' or dir == 'NW' or dir == 'SE' or dir == 'SW'):
                config.diagonalMoveCost += 3

#name: displayCosts
#args: none
#effect:  print to console
    # name:
    # args:
    # returns:
    # effect:
    def displayCosts():
        print("orthogonal move cost = " + str(config.orthogonalMoveCost))
        print("diagonal move cost   = " + str(config.diagonalMoveCost))
        print("wall collision cost  = " + str(config.hitCost))
        print("total cost           = " + str(config.hitCost+config.orthogonalMoveCost+config.diagonalMoveCost))
    def displayNumberOfQueriedCells():
        print("Number of queried cells =" + str(len(config.queriedCells)))
    accumulateCosts()
    displayCosts()
    displayNumberOfQueriedCells()
    pygame.quit()



if __name__ == "__main__":
    main()








