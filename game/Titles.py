
#class that writes text on the screen
import turtle

from game.Grid import grid
gameTitle = "pyCheckers v1.00"


class titles(turtle.RawTurtle):

    def __init__(self,screen):
        self.screen = screen
        self.createPen()

    #creates the turtle that will write the text
    def createPen(self):
        super(titles,self).__init__(self.screen)
        self.hideturtle()
        self.speed(0)
        self.width(3)
        self.up()

    #writes the game title and how to play
    def writeTitle(self):
        line0 = gameTitle
        line1 = "Click a pawn to see its possible moves"
        line2 = "Capture enemy pawns by jumping over them"
        line3 = "The player with the last pawn Wins"

        self.clear()
        self.color("black")
        self.goto(-1100/2,600/2)
        self.write(line0,align="left",font=("Arial",20,"normal"))
        self.goto(4*grid.gridSize,5*grid.gridSize)
        self.write(line1,align="right",font=("Arial",14,"normal"))
        self.goto(4*grid.gridSize,4.75*grid.gridSize)
        self.write(line2,align="right",font=("Arial",14,"normal"))
        self.goto(4*grid.gridSize,4.5*grid.gridSize)
        self.write(line3,align="right",font=("Arial",14,"normal"))

    #writes the current turn on the screen
    def writeTurn(self,turn, winner = None):
        string = ""
       
        if(turn == 1):
            string = "It's Red Player's Turn"
            self.color("red")
        elif(turn == 2):
            string = "It's Blue Player's Turn"
            self.color("blue")
        elif(turn == 0):
            string = "Choose the Agents in the terminal"
        elif turn == 3:
          
            if (winner.value != 0):
                self.color("orange")
                string = f"{winner.name} wins!!!"
            else: 
                self.color("gray")
                string = "It's draw"

        self.clear()
        self.goto(0,-5*grid.gridSize)
        self.write(string,align="center",font=("Arial",20,"normal"))
