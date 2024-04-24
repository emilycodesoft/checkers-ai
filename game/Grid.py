
import turtle
from enums import PLAYERS
gameTitle = "pyCheckers v1.00"


#class that defines a grid space and its properties
class grid(turtle.RawTurtle):
    
    #variables that set the grids size
    gridSize = 60
    pawnRadius = 20
    crownRadius = 10

    #create grid space and give it default attributes
    def __init__(self,screen):
        self.screen = screen
        self.defaultAttributes()
        self.createPen()

    #creates the turtle that will draw the grid space
    def createPen(self):
        super(grid,self).__init__(self.screen)
        self.hideturtle()
        self.speed(0)
        self.width(3)
        self.up()

    #sets the grid's attributes
    def defaultAttributes(self):
        self.gridX = 0
        self.gridY = 0
        self.colored = False #True if the square is shaded, False if white
        self.selected = 0 #0 if space is normal, 1 or 2 if space is highlighted
        self.pawn = False #True if there is a pawn on the grid space
        self.player = PLAYERS.NONE.value #1 if pawn is player1 (red), 2 if pawn is player2 (blue)
        self.king = False #True if pawn has been kinged

    #removes the pawn from the grid
    def clearPawn(self, main):
        self.selected = False
        self.pawn = False
        self.player = PLAYERS.NONE.value
        self.king = False
        if main:
            self.draw()

    #imports all attributes from another grid object
    def importPawn(self,gridObj, main):
        self.colored = gridObj.colored
        self.pawn = gridObj.pawn
        self.player = gridObj.player
        self.king = gridObj.king
        if main:
            self.draw()

    #places the grid at a new set of coords
    def moveGrid(self,gX,gY):
        self.gridX = gX
        self.gridY = gY

    #draws the grid
    def draw(self):
        pixleX = int(self.gridX*grid.gridSize - 4*grid.gridSize)
        pixleY = int(self.gridY*grid.gridSize - 4*grid.gridSize)
        self.clear()

        self.goto(pixleX,pixleY)
        self.seth(0)
        self.down()
        if(self.colored == True):
            if(self.selected in [1,2]):
                self.color((0,0,0),(0.5,1,0.5))
            else:    
                self.color((0,0,0),(0.75,0.75,0.75))
            self.begin_fill()
        for f in range(4):
            self.fd(grid.gridSize)
            self.left(90)
        self.end_fill()
        self.up()

        if(self.pawn == True):
            self.goto(pixleX + 0.5*grid.gridSize,pixleY + 0.5*grid.gridSize - grid.pawnRadius)
            if(self.player == PLAYERS.RED.value):
                self.color((0,0,0),(1,0.5,0.5))
            elif(self.player == PLAYERS.BLUE.value):
                self.color((0,0,0),(0.5,0.5,1))
            else:
                self.color((0,0,0),(1,0.5,1))
            self.down()
            self.begin_fill()
            self.circle(grid.pawnRadius,360,16)
            self.end_fill()
            self.up()

            if(self.king == True):
                self.goto(pixleX + 0.5*grid.gridSize,pixleY + 0.5*grid.gridSize - grid.crownRadius)
                self.color((0,0,0),(1,0.85,0))
                self.down()
                self.begin_fill()
                self.circle(grid.crownRadius,360,16)
                self.end_fill()
                self.up()

