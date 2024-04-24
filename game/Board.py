


from game.Grid import grid
from enums import PLAYERS
from utils import logToConsole, onGrid


class Board:
    def __init__(self,screen, matrix = None, main=False):
        self.screen = screen
        self.matrix = matrix
        self.main = main
        self.createGrid()
        self.highlightedSpaces = []
        self.spaceSelected = False
        self.turn = PLAYERS.NONE.value
        self.bluePawns = 12
        self.redPawns = 12
    #create the matrix that stores the game data
    def copyMatrix (self):
        matrixCopy = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8]

        #populate matrixCopy with grid objects and assign them attributes
        for x in range(8):
            for y in range(8):
                matrixCopy[x][y] = grid(self.screen)
                matrixCopy[x][y].moveGrid(x,y)
                if(((x + y) % 2) == 1):
                    matrixCopy[x][y].colored = self.matrix[x][y].colored
                    if(y in [0,1,2]):
                        matrixCopy[x][y].pawn = self.matrix[x][y].pawn
                        matrixCopy[x][y].player = self.matrix[x][y].player
                    if(y in [5,6,7]):
                        matrixCopy[x][y].pawn = self.matrix[x][y].pawn
                        matrixCopy[x][y].player = self.matrix[x][y].player
        return matrixCopy
    def createGrid(self):
        #create empty matrix
        if not self.main: 
            return
        self.matrix = [[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8,[None]*8]

        #populate matrix with grid objects and assign them attributes
        for x in range(8):
            for y in range(8):
                self.matrix[x][y] = grid(self.screen)
                self.matrix[x][y].moveGrid(x,y)
                if(((x + y) % 2) == 1):
                    self.matrix[x][y].colored = True
                    if(y in [0,1,2]):
                        self.matrix[x][y].pawn = True
                        self.matrix[x][y].player = 1
                    if(y in [5,6,7]):
                        self.matrix[x][y].pawn = True
                        self.matrix[x][y].player = 2
                if self.main:
                    self.matrix[x][y].draw()
            
        #create list to hold values of highlighted spaces
        self.highlightedSpaces = []
        self.spaceSelected = False
    #moves a pawn from gridA to gridB
    def movePawn(self,gridA,gridB):
        self.matrix[gridB[0]][gridB[1]].importPawn(self.matrix[gridA[0]][gridA[1]], self.main)
        self.matrix[gridA[0]][gridA[1]].clearPawn(self.main)
        self.kingPawn(gridB[0],gridB[1])
        if self.main:
            logToConsole("\tMoved pawn at %s to %s" % (gridA,gridB))

    #moves a pawn from gridA to gridC by jumping over the pawn in gridB
    def jumpPawn(self,gridA,gridC):
        gridB = (int((gridC[0]+gridA[0])/2),int((gridC[1]+gridA[1])/2))
        self.matrix[gridC[0]][gridC[1]].importPawn(self.matrix[gridA[0]][gridA[1]], self.main)
        self.matrix[gridB[0]][gridB[1]].clearPawn(self.main)
        self.matrix[gridA[0]][gridA[1]].clearPawn(self.main)
        self.kingPawn(gridC[0],gridC[1])
        if self.main:
            logToConsole("\tPawn at %s jumped over pawn at %s to coords %s" % (gridA,gridB,gridC))

    #kings the pawn at coords (x, y) if it has reached it's kings row
    def kingPawn(self,x,y):
        if((self.matrix[x][y].player == 1) and (y == 7)):
            self.matrix[x][y].king = True
            self.matrix[x][y].draw()
            if self.main:
                logToConsole("\tPawn at (%s,%s) was Kinged" % (x,y))
        elif((self.matrix[x][y].player == 2) and (y == 0)):
            self.matrix[x][y].king = True
            self.matrix[x][y].draw()
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
    #returns moves available to a pawn at (x, y)
    def findMoves(self,x,y):
        if(self.matrix[x][y].player == 1):
            moves = [(-1,1),(1,1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1,-1),(1,-1)]

        elif(self.matrix[x][y].player == 2):
            moves = [(-1,-1),(1,-1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1,1),(1,1)]

        coords = []
        for move in moves:
            x1 = x + move[0]
            y1 = y + move[1]
            if((onGrid(x1,y1) == True) and (self.matrix[x1][y1].pawn == False)):
                coords.append((x1,y1))
       
        return coords
    def updateBoard(self, move):
        # print(move["move_coords"])
        x, y = move["move_coords"]
        pawn_x, pawn_y = move["pawn_coords"]
        self.spaceSelected = (x,y)
    
        if(not move["is_jump"]):
                self.movePawn(move["pawn_coords"], self.spaceSelected)
                self.deselectAll()
                self.endTurn()
        #if grid clicked can be jumped too, jump the selected pawn
        elif(move["is_jump"]):
                if self.matrix[pawn_x][pawn_y].player == PLAYERS.RED.value:
                            self.bluePawns -= 1
                else: 
                            self.redPawns -= 1
                self.jumpPawn(move["pawn_coords"], self.spaceSelected)
                self.deselectAll()
                self.endTurn()
              
                
        else:
                self.deselectAll()
    def boardState (self):
        return self.redPawns - self.bluePawns
            
    #returns coords of jumps available to a pawn at coords (x, y)
    def findJumps(self,x,y):
        if(self.matrix[x][y].player == 1):
            moves = [(-1,1),(1,1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1,-1),(1,-1)]

        elif(self.matrix[x][y].player == 2):
            moves = [(-1,-1),(1,-1)]
            if(self.matrix[x][y].king == 1):
                moves += [(-1,1),(1,1)]

        coords = []
        for move in moves:
            x1 = x + move[0]
            y1 = y + move[1]
            x2 = x + 2*move[0]
            y2 = y + 2*move[1]
            if((onGrid(x2,y2) == True) and (self.matrix[x2][y2].pawn == False)):
                if((self.matrix[x1][y1].pawn == True)):
                    if((self.matrix[x][y].player == 1) and (self.matrix[x1][y1].player == 2)):
                        coords.append((x2,y2))
                    elif((self.matrix[x][y].player == 2) and (self.matrix[x1][y1].player == 1)):
                        coords.append((x2,y2))
       
        return coords
    def findAvailableMovements (self, player):
        movements_coords = {"moves": [], "jumps": []}
        for x in range(8):
            for y in range(8):
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
        red_pawns = 0
        blue_pawns = 0
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y].player == PLAYERS.RED.value:
                    red_pawns += 1
                elif self.matrix[x][y].player == PLAYERS.BLUE.value:
                    blue_pawns += 1
        if red_pawns == 0:
            return PLAYERS.BLUE
        elif blue_pawns == 0:
            return PLAYERS.RED
        elif red_pawns == 1 and blue_pawns == 1:
            return PLAYERS.NONE
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
                        
                      