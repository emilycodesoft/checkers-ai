from copy import deepcopy
from game.Board import Board
from enums import PLAYERS, AgentsNames
import turtle
from time import sleep
import random  # Importa la librería random

screen = turtle.Screen()

class MiniMaxAgent:
    def __init__(self):
        self.name = AgentsNames.MINIMAX.value
        self.maxDepth = 3
    def move(self, board, player):
        maxPlayer = True if player == PLAYERS.RED.value else False

        return self.findBestMove(board, maxPlayer)

    def findBestMove(self, board, maximizing = True, depth = 0):
        # evitar que siempre haga el mismo movimiento con nodesMap
        isTerminal = board.checkWinner()
        
        if(isTerminal or depth == self.maxDepth):
                return  board.evaluate(), board
        if (maximizing):
        
            maxEval = float('-inf');
            bestMoves = []  # Lista para almacenar los mejores movimientos
            movements = board.findAvailableMovements(PLAYERS.RED.value)

            if movements["jumps"]:
                movements = movements["jumps"]
            else: 
                movements = movements["moves"]
            
            for move in movements:   
                temp_matrix = board.copyMatrix()   
                child = Board(matrix=temp_matrix, redPawns=board.redPawns, bluePawns=board.bluePawns, blueKings = board.blueKings, redKings = board.redKings)

                child.updateBoard(move)
                nodeValue = self.findBestMove(child, False, depth + 1)[0]
                if nodeValue > maxEval:
                    maxEval = nodeValue
                    bestMoves = [move]  # Reinicia la lista con el nuevo mejor movimiento
                elif nodeValue == maxEval:
                    bestMoves.append(move)  # Agrega este movimiento a la lista de mejores movimientos

            if bestMoves:
                return maxEval, random.choice(bestMoves)
            else:
                return maxEval, False  # Devuelve un valor predeterminado cuando no hay movimientos disponibles
        
        if not maximizing:
            minEval = float('inf')
            bestMoves = []  # Lista para almacenar los mejores movimientos
            movements = board.findAvailableMovements(PLAYERS.BLUE.value)

            if movements["jumps"]:
                movements = movements["jumps"]
            else: 
                movements = movements["moves"]
            
            for move in movements:
                temp_matrix = board.copyMatrix()   
                child = Board(matrix=temp_matrix, redPawns=board.redPawns, bluePawns=board.bluePawns, blueKings = board.blueKings, redKings = board.redKings)
            
                child.updateBoard(move)
            
                nodeValue = self.findBestMove(child, True, depth + 1)[0]
                if nodeValue < minEval:
                    minEval = nodeValue
                    bestMoves = [move]  # Reinicia la lista con el nuevo mejor movimiento
                elif nodeValue == minEval:
                    bestMoves.append(move)  # Agrega este movimiento a la lista de mejores movimientos
            
            if bestMoves:
                return minEval, random.choice(bestMoves)
            else:
                return minEval, False  # Devuelve un valor predeterminado cuando no hay movimientos disponibles              
                
                
                    
