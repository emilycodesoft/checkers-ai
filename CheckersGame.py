#main game class
from random import randint, choice
from time import sleep
from game.Board import Board
from game.Grid import grid
from agents.MiniMaxAgent import MiniMaxAgent
from agents.RandomAgent import RandomAgent
from game.Titles import titles
from agents.YourselfAgent import YourselfAgent
from enums import PLAYERS, AgentsNames
from utils import clearScreen, logToConsole, onGrid


class CheckersGame:

    #create game instance
    def __init__(self,screen):
        self.screen = screen
        self.player1 = PLAYERS.NONE.value
        self.player2 = PLAYERS.NONE.value
        self.show_moves_gui = False
        self.iterations = 1
        self.repeating = False
        self.resetGame()

    #resets the matrix that stores game data
    def showStatistics():
        pass
    def resetGame(self):
        if self.iterations == 0:
            self.showStatistics()
        self.iterations -= 1
        self.board = Board(self.screen, main=True)
        
        self.screen.update()  # Actualiza la pantalla
        self.board.turn = randint(PLAYERS.RED.value,PLAYERS.BLUE.value)

        logToConsole("\tStarting Player: %s" % (self.board.turn))
        if not self.repeating: 
            self.createTitles()
            self.menu()
        else:
            self.player1.board = self.board
            self.player2.board = self.board
        clearScreen()
        logToConsole("\tAgents has been chosen")
        self.move()

    def menu (self):
        print("--------------------------MENU------------------------------------------")
        
        self.player1 = self.chooseAgent(PLAYERS.RED)
        clearScreen()
        self.player2 = self.chooseAgent(PLAYERS.BLUE)
       

        if (self.player1.name != AgentsNames.YOURSELF.value and self.player2.name != AgentsNames.YOURSELF.value):
            option = int(input("¿DESEA VER LOS MOVIMIENTOS EN LA PANTALLA? 1. SI 2. NO: "))
            if option == 1:
                self.show_moves_gui = True

        self.iterations = int(input("¿CUANTAS ITERACIONES DESEA JUGAR?: "))

        if(self.iterations > 1):
            self.repeating = True

        self.text1.writeTurn(self.board.turn)

    def currentPlayer (self):
        if(self.board.turn == 1):
            return self.player1.name
        else: 
            return self.player2.name
   
    def move (self):
            while self.currentPlayer() != AgentsNames.YOURSELF.value:
                movement = None
                winner = self.board.checkWinner()

                if winner:
                    self.text1.writeTurn(3, winner)
                    #create a function
                    if (self.iterations > 1 and self.show_moves_gui):
                            sleep(3)
                            self.resetGame()
                            self.screen.update()  # Actualiza la pantalla
                    break
                         
                if (self.board.turn == PLAYERS.RED.value):
                    if self.player1.name == AgentsNames.MINIMAX.value:
                        what = self.player1.move(self.screen, self.board, PLAYERS.RED.value)
                        print("WHAT: ", what)
                        # print("MINIMAX MOVEMENTS: ",self.player1.nodesMap)
                        # candidate = choice(self.player1.nodesMap)
                        candidate = choice(what)
                        movement = candidate[1]
                    
                    else: 
                        movement = self.player1.move()
                    
                elif (self.board.turn == PLAYERS.BLUE.value):

                    if self.player2.name == AgentsNames.MINIMAX.value:
                        what = self.player2.move(self.screen, self.board, PLAYERS.BLUE.value)
                        print("WHAT: ", what)
                        # print("MINIMAX MOVEMENTS: ",self.player2.nodesMap)
                        # candidate = choice(self.player2.nodesMap)
                        candidate = choice(what)
                        movement = candidate[1]

                    else: 
                        movement = self.player2.move()    
                
                print("move: ", movement)

                if movement:
                    self.board.updateBoard(movement)
                    print(f"****************BOARD STATE: RED({self.board.redPawns}) y BLUE({self.board.bluePawns}) ***********************")
                    if self.show_moves_gui:
                        # sleep(1)
                        # self.screen.delay(1000)
                        self.screen.update()  # Actualiza la pantalla
                    self.text1.writeTurn(self.board.turn)
            print(f"****************BOARD STATE: RED({self.board.redPawns}) y BLUE({self.board.bluePawns}) ***********************")

    def chooseAgent(self, player):
        print(f"Choose Agent for player {player.name}: ")

        options = [AgentsNames.YOURSELF.name, AgentsNames.RANDOM.name, AgentsNames.MINIMAX.name, AgentsNames.PODAMINIMAX.name, AgentsNames.QAGENT.name, AgentsNames.NEURALAGENT.name]

        for i, option in enumerate(options):
            print(f"{" "*7}{i+1}. {option}")
        option = int(input("Choose an option: "))

        if option == 1:
            return YourselfAgent(self.board)
        elif option == 2:
            return RandomAgent(self.board, player.value)
        else: 
            return MiniMaxAgent()
    
    #this funcion is called whenever the window is clicked
    def mouseEvent (self,pixelX,pixelY):
        x = int((pixelX + 4*grid.gridSize) // grid.gridSize)
        y = int((pixelY + 4*grid.gridSize) // grid.gridSize)
        if(onGrid(x,y) == True):
            logToConsole("Mouse Event at coords (%s,%s)" % (x,y))

            #if grid clicked contains a pawn and the current player it, highlight it's possible moves
            if((self.board.matrix[x][y].pawn == True) and (self.board.matrix[x][y].player == self.board.turn)):
                if(self.board.spaceSelected != 0):
                    self.board.deselectAll()
                moves = self.board.findMoves(x,y)
                jumps = self.board.findJumps(x,y)
                for move in moves:
                    self.board.matrix[move[0]][move[1]].selected = 1
                    self.board.highlightedSpaces.append((move[0],move[1]))
                    self.board.matrix[move[0]][move[1]].draw()
                for move in jumps:
                    self.board.matrix[move[0]][move[1]].selected = 2
                    self.board.highlightedSpaces.append((move[0],move[1]))
                    self.board.matrix[move[0]][move[1]].draw()
                self.board.spaceSelected = (x,y)
                logToConsole("\tMoves Highlighted for pawn at (%s,%s)" % (x,y))

            #if grid clicked can be moved too, move the selected pawn
            elif(self.board.matrix[x][y].selected == 1):
                self.board.movePawn(self.board.spaceSelected,(x,y))
                self.board.deselectAll()
                self.board.endTurn()
                self.move()

            #if grid clicked can be jumped too, jump the selected pawn
            elif(self.board.matrix[x][y].selected == 2):
                self.board.jumpPawn(self.board.spaceSelected,(x,y))
                jumps = self.board.findJumps(x,y)

                # create function
                if self.board.turn == PLAYERS.RED.value:
                    self.board.bluePawns -= 1
                else: 
                    self.board.redPawns -= 1
                
                if(jumps != []):
                    self.board.deselectAll()
                    self.board.spaceSelected = (x,y)
                    for move in jumps:
                        self.board.matrix[move[0]][move[1]].selected = 2
                        self.board.highlightedSpaces.append((move[0],move[1]))
                        self.board.matrix[move[0]][move[1]].draw()
                else:
                    self.board.deselectAll()
                    self.board.endTurn()
                    self.move()
                    
            else:
                self.board.deselectAll()
            
            logToConsole("\tMouse Event completed\n")
        
    
    #creates text to display game information such as the current turn
    def createTitles(self):
        self.text0 = titles(self.screen)
        self.text1 = titles(self.screen)
        self.text2 = titles(self.screen)
        self.text3 = titles(self.screen)
        self.text0.writeTitle()
        self.text1.writeTurn(0)

