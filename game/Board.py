


from random import choice
from time import sleep
import turtle
from game.Grid import grid
from enums import PLAYERS
from utils import logToConsole, onGrid

screen = turtle.Screen()
class Board:
    def __init__(self, matrix = None, bluePawns = 12, redPawns = 12, blueKings = 0, redKings = 0, main=False):
        self.matrix = matrix
        self.main = main
        self.highlightedSpaces = []
        self.spaceSelected = False
        self.turn = PLAYERS.NONE.value
        self.bluePawns = bluePawns
        self.blueKings = blueKings
        self.redPawns = redPawns
        self.redKings = redKings
        #create list to hold values of highlighted spaces
        self.highlightedSpaces = []
        self.spaceSelected = False
    #create the matrix that stores the game data
    def copyMatrix (self):
        matrixCopy = [[None]*8 for _ in range(8)]

        #populate matrixCopy with grid objects and assign them attributes
        for x in range(8):
            for y in range(8):
                matrixCopy[x][y] = grid()
                matrixCopy[x][y].moveGrid(x,y)
                matrixCopy[x][y].colored = self.matrix[x][y].colored
                   
                matrixCopy[x][y].pawn = self.matrix[x][y].pawn
                matrixCopy[x][y].player = self.matrix[x][y].player
                   
                matrixCopy[x][y].pawn = self.matrix[x][y].pawn
                matrixCopy[x][y].player = self.matrix[x][y].player
        return matrixCopy
    def createGrid(self):
        #create empty matrix
        self.matrix = [[None]*8 for _ in range(8)]

        #populate matrix with grid objects and assign them attributes
        for x in range(8):
            for y in range(8):
                self.matrix[x][y] = grid()
                self.matrix[x][y].moveGrid(x,y)
                if(((x + y) % 2) == 1):
                    self.matrix[x][y].colored = True
                    if(y in [0,1,2]):
                        self.matrix[x][y].pawn = True
                        self.matrix[x][y].player = 1
                    if(y in [5,6,7]):
                        self.matrix[x][y].pawn = True
                        self.matrix[x][y].player = 2
                self.matrix[x][y].draw()

        #create list to hold values of highlighted spaces
        self.highlightedSpaces = []
        self.spaceSelected = False
            
    #moves a pawn from gridA to gridB
    def movePawn(self,gridA,gridB):
        self.matrix[gridB[0]][gridB[1]].importPawn(self.matrix[gridA[0]][gridA[1]])
        self.matrix[gridA[0]][gridA[1]].clearPawn()
        self.kingPawn(gridB[0],gridB[1])
        if self.main:
            logToConsole("\tMoved pawn at %s to %s" % (gridA,gridB))

    #moves a pawn from gridA to gridC by jumping over the pawn in gridB
    def jumpPawn(self,gridA,gridC):
        gridB = (int((gridC[0]+gridA[0])/2),int((gridC[1]+gridA[1])/2))
        self.matrix[gridC[0]][gridC[1]].importPawn(self.matrix[gridA[0]][gridA[1]])
        self.matrix[gridB[0]][gridB[1]].clearPawn()
        self.matrix[gridA[0]][gridA[1]].clearPawn()
        self.kingPawn(gridC[0],gridC[1])
        if self.main:
            logToConsole("\tPawn at %s jumped over pawn at %s to coords %s" % (gridA,gridB,gridC))

    def drawBoard (self):
        for x in range(8):
            for y in range(8):
                 self.matrix[x][y].draw()
        screen.update()
    #kings the pawn at coords (x, y) if it has reached it's kings row
    def kingPawn(self,x,y):
        if((self.matrix[x][y].player == 1) and (y == 7)):
            self.matrix[x][y].king = True
            self.redKings += 1
            self.redPawns -= 1
           
            if self.main:
                logToConsole("\tPawn at (%s,%s) was Kinged" % (x,y))
        elif((self.matrix[x][y].player == 2) and (y == 0)):
            self.matrix[x][y].king = True
            self.blueKings += 1
            self.bluePawns -= 1
           
            if self.main:
                logToConsole("\tPawn at (%s,%s) was Kinged" % (x,y))  
    def undoMove(self, move):
        # print(move["move_coords"])
        x, y = move["move_coords"]
        pawn_x, pawn_y = move["pawn_coords"]
        self.spaceSelected = (x,y)
    
        if(not move["is_jump"]):
                self.movePawn(self.spaceSelected, move["pawn_coords"])
                self.deselectAll()
                self.endTurn()
        #if grid clicked can be jumped too, jump the selected pawn
        elif(move["is_jump"]):
                if self.matrix[pawn_x][pawn_y].player == PLAYERS.RED.value:
                            self.bluePawns += 1
                else: 
                            self.redPawns += 1
                self.jumpPawn(self.spaceSelected, move["pawn_coords"])
                self.deselectAll()
                self.endTurn()
    """ def getPieces(self, player):
        pieces = []      
        for x in range(8):
            for y in range(8):
                if (((x + y) % 2) == 1):
                    if self.matrix[x][y].pawn:
                        if self.matrix[x][y].player == player:
                            pieces.append((x,y))               
        return pieces
    def getValidMoves(self, piece):
        x, y = piece
        jumps = self.findJumps(x, y)
        if len(jumps):
            return jumps
        else:
            moves = self.findMoves(x, y)
            return moves """
         
    #returns moves available to a pawn at (x, y)
    def findMoves(self, x, y):
        moves = [(-1, 1), (1, 1)] if self.matrix[x][y].player == 1 else [(-1, -1), (1, -1)]
        if self.matrix[x][y].king:
            moves += [(-1, -1), (1, -1)] if self.matrix[x][y].player == 1 else [(-1, 1), (1, 1)]

        coords = [(x + move[0], y + move[1]) for move in moves if onGrid(x + move[0], y + move[1]) and not self.matrix[x + move[0]][y + move[1]].pawn]

        return coords
    
    def updatePlayerPieces(self, player):
        if player == PLAYERS.RED.value:
            if self.matrix[self.spaceSelected[0]][self.spaceSelected[1]].king:
                self.blueKings -= 1
            else:
                self.bluePawns -= 1
        else:
            if self.matrix[self.spaceSelected[0]][self.spaceSelected[1]].king:
                self.redKings -= 1
            else:
                self.redPawns -= 1
    def updateBoard(self, move, main=False):
        x, y = move["move_coords"]
        pawn_x, pawn_y = move["pawn_coords"]
        self.spaceSelected = (x,y)
    
        if(not move["is_jump"]):
                self.movePawn(move["pawn_coords"], self.spaceSelected)
                self.deselectAll()
                self.endTurn()
        #if grid clicked can be jumped too, jump the selected pawn
        elif(move["is_jump"]):
                self.jumpPawn(move["pawn_coords"], self.spaceSelected)
                self.updatePlayerPieces(self.matrix[pawn_x][pawn_y].player)
               
                jumps = self.findJumps(x,y)

                while len(jumps):
                    j = choice(jumps)
                    if main:
                        for jx in jumps:
                            self.matrix[jx[0]][jx[1]].selected = 2
                            self.highlightedSpaces.append((jx[0],jx[1]))
                            self.matrix[jx[0]][jx[1]].draw()
                        self.drawBoard()
                        screen.update()
                        sleep(1)
                    self.jumpPawn(self.spaceSelected, j)
                    self.updatePlayerPieces(self.matrix[pawn_x][pawn_y].player)
                    jumps = self.findJumps(j[0],j[1])
                    self.deselectAll()
                    self.spaceSelected = j   
                self.deselectAll()
                self.endTurn()           
        else:
                self.deselectAll()
    def evaluate (self):
        return self.redPawns - self.bluePawns + (self.redKings * 0.5 - self.blueKings* 0.5)

            
    #returns coords of jumps available to a pawn at coords (x, y)
    def findJumps(self, x, y):
        moves = [(-1, 1), (1, 1), (-1, -1), (1, -1)] if self.matrix[x][y].king else [(-1, 1), (1, 1)] if self.matrix[x][y].player == 1 else [(-1, -1), (1, -1)]
        
        coords = []
        for dx, dy in moves:
            x1, y1 = x + dx, y + dy
            x2, y2 = x + 2*dx, y + 2*dy
            if onGrid(x2, y2) and not self.matrix[x2][y2].pawn and self.matrix[x1][y1].pawn and self.matrix[x1][y1].player != self.matrix[x][y].player:
                coords.append((x2, y2))
        
        return coords
    
    def findAvailableMovements (self, player):
        movements_coords = {"moves": [], "jumps": []}
        for x in range(8):
            for y in range(8):
                if (((x + y) % 2) == 1):
                    if (self.matrix[x][y].player == player and self.matrix[x][y].pawn):
                        move_coords = self.findMoves(x, y)
                        jumps_coords = self.findJumps(x, y)
                        if len(move_coords) or len(jumps_coords):
                            movements_coords["moves"].extend([{"move_coords": (mov_x, mov_y), "pawn_coords": (x, y), "is_jump": False} for (mov_x, mov_y) in move_coords])
                            movements_coords["jumps"].extend([{"move_coords": (mov_x, mov_y), "pawn_coords": (x, y), "is_jump": True} for (mov_x, mov_y) in jumps_coords])
        return movements_coords
    #deselects all of the selected grid spaces
    
    def deselectAll(self):
        for space in self.highlightedSpaces:
            self.matrix[space[0]][space[1]].selected = 0
            self.matrix[space[0]][space[1]].draw()
        self.spaceSelected = False
        if self.main:
             logToConsole("\tAll Spaces Un-highlited")
    def checkWinner(self):
        # if self.redPawns == 0 and self.redKings == 0:
        if self.redPawns == 0:
            return PLAYERS.BLUE
        # elif self.bluePawns == 0 and self.blueKings == 0:
        elif self.bluePawns == 0:
            return PLAYERS.RED
        elif self.redPawns == 1 and self.bluePawns == 1:
            return PLAYERS.DRAW
        return False

    #ends the current turn
    def endTurn(self):
        if(self.turn == PLAYERS.RED.value):
            if self.main:
                 logToConsole("\tRed Player's turn has ended")
            self.turn = PLAYERS.BLUE.value
        elif(self.turn == PLAYERS.BLUE.value):
            if self.main:
                logToConsole("\tBlue Player's turn has ended")
            self.turn = PLAYERS.RED.value
                        
                      