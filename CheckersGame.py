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
import matplotlib.pyplot as plt
import numpy as np
import turtle


class CheckersGame:

    #create game instance
    def __init__(self,screen):
        self.screen = screen
        self.player1 = PLAYERS.NONE.value
        self.player2 = PLAYERS.NONE.value
        self.show_moves_gui = False
        self.iterations = 0
        self.repeating = False
        self.blueWins = []
        self.redWins = []
        self.draws = []
        self.resetGame()

    def calcPercentageOfWins(self, p_wins):
        return p_wins.count(1)/self.iterations*100
    #resets the matrix that stores game data
    def showStatistics(self):
        #plot the results

        #for player 1 and 2 find the cumulative sum 
        # print(self.blueWins, self.redWins, self.draws)
        labels = [f'Red Wins ({self.player1.name})', f'Blue Wins ({self.player2.name})', 'Draws']
        sizes = [self.calcPercentageOfWins(self.redWins), self.calcPercentageOfWins(self.blueWins), self.calcPercentageOfWins(self.draws)]
        colors = ['red', 'blue', 'gray',]

   

        # Manejar el caso de valores cero
        explode = (0.1, 0.1, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
        plt.figure(figsize=(6, 6))  # Tamaño de la figura
        plt.pie(sizes, labels=labels, colors=colors, explode=explode, autopct='%1.1f%%', startangle=140)

        # Añadir una leyenda
        plt.title('Distribution of Wins')

        # Mostrar el diagrama de pastel
        plt.axis('equal')  # Hacer que el pastel se vea como un círculo
        plt.show()

    def resetGame(self):
        self.iterations -= 1
        self.board = Board(main=True)
        self.board.createGrid()
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

        self.text1.writeTurn(self.board.turn, self.currentPlayer())

    def currentPlayer (self):
        if(self.board.turn == 1):
            return self.player1.name
        else: 
            return self.player2.name
    def highlightMoves(self, x, y):
        if(self.board.spaceSelected != 0):
                self.board.deselectAll()
        moves = self.board.findMoves(x,y)
        jumps = self.board.findJumps(x,y)
        for move in moves:
                        self.board.matrix[move[0]][move[1]].selected = 1
                        self.board.highlightedSpaces.append((move[0],move[1]))
                        self.board.matrix[move[0]][move[1]].draw()
                        # print("drawing moves")
        for move in jumps:
                        self.board.matrix[move[0]][move[1]].selected = 2
                        self.board.highlightedSpaces.append((move[0],move[1]))
                        
                        self.board.matrix[move[0]][move[1]].draw()
        self.board.spaceSelected = (x,y)
        logToConsole("\tMoves Highlighted for pawn at (%s,%s)" % (x,y))     
    def move (self):
            while self.currentPlayer() != AgentsNames.YOURSELF.value:
                movement = None
                winner = self.board.checkWinner()
                score = None
                if winner:
                    self.text1.writeTurn(3, playerName=self.currentPlayer(), winner=winner)
                    self.screen.update()  # Actualiza la pantalla
                    if (winner.value == PLAYERS.RED.value):
                        self.redWins.append(1)
                        self.blueWins.append(0)
                        self.draws.append(0)
                    if (winner.value == PLAYERS.BLUE.value):
                        self.redWins.append(0)
                        self.blueWins.append(1)
                        self.draws.append(0)
                    if (winner.value == PLAYERS.DRAW.value):
                        self.redWins.append(0)
                        self.blueWins.append(0)
                        self.draws.append(1)
                    if (self.repeating and  self.iterations > 1):
                            if self.show_moves_gui:
                                sleep(3)
                            return
                    else:
                        return
                    break
                print(winner)
                if (self.board.turn == PLAYERS.RED.value):
                    
                    if self.player1.name == AgentsNames.MINIMAX.value:
                        score, movement = self.player1.move(self.board, PLAYERS.RED.value)
                        # self.screen.update() 
                       
                    else: 
                        movement = self.player1.move()
                    
                elif (self.board.turn == PLAYERS.BLUE.value):

                    if self.player2.name == AgentsNames.MINIMAX.value:
                        score, movement = self.player2.move(self.board, PLAYERS.BLUE.value)
                        # self.screen.update()  # Actualiza la pantalla
                      
                    else: 
                        movement = self.player2.move()    
                print("score: ", score)
                print("move: ", movement)

                if movement:
                    x, y = movement["pawn_coords"]
                    self.highlightMoves(x, y)
                    self.screen.update()
                    if self.show_moves_gui:
                        sleep(1)  
                    self.board.updateBoard(movement, True)
                    """ if self.show_moves_gui:
                        self.screen.delay(1000) """
                    self.board.drawBoard()
                    # self.board.endTurn()
                    self.text1.writeTurn(self.board.turn, self.currentPlayer())
                    self.screen.update()  # Actualiza la pantalla
                else:
                    print("No movement")
                    if self.board.turn == PLAYERS.BLUE.value:
                        self.board.bluePawns = 0
                    else:
                        self.board.redPawns = 0
                self.showBoardState()
    
    def showBoardState(self):
        print(f"BOARD STATE: RED({self.board.redPawns}) y BLUE({self.board.bluePawns})")
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
                self.text1.writeTurn(self.board.turn, self.currentPlayer())
                self.board.drawBoard()
                self.screen.update()
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
                        self.board.drawBoard()
                        self.screen.update()
                else:
                    self.board.deselectAll()
                    self.board.endTurn()
                    self.text1.writeTurn(self.board.turn, self.currentPlayer())
                    self.board.drawBoard()
                    self.screen.update()
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
        # self.text2.writeIterations(self.iterations)

