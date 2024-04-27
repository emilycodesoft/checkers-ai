
from copy import deepcopy
from game.Board import Board
from enums import PLAYERS, AgentsNames
import turtle
from time import sleep

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
            bestMove = None
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
                maxEval = max(maxEval, nodeValue);
                if maxEval == nodeValue:
                    bestMove = move

            return maxEval, bestMove
        
        if not maximizing:
            maxEval = float('inf')
            bestMove = None
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
                maxEval = min(maxEval, nodeValue)
                
                if maxEval == nodeValue:
                    bestMove = move      
            
            return maxEval, bestMove
              
            
                
