
from copy import deepcopy
from game.Board import Board
from enums import PLAYERS, AgentsNames
import turtle
from time import sleep

screen = turtle.Screen()

class PodaMiniMaxAgent:
    def __init__(self):
        self.name = AgentsNames.PODAMINIMAX.value
        self.maxDepth = 3
    def move(self, board, player):
        maxPlayer = True if player == PLAYERS.RED.value else False

        return self.findBestMove(board, maximizing=maxPlayer)
   
    def findBestMove(self, board, alpha = float("-inf"), beta = float("inf"), maximizing = True, depth = 0):
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

            # print("maximizing.", " depth: ", depth)
            
            for move in movements:   
                temp_matrix = board.copyMatrix()   
                child = Board(matrix=temp_matrix, redPawns=board.redPawns, bluePawns=board.bluePawns, blueKings = board.blueKings, redKings = board.redKings)
                # print("length of movements: ", len(movements))
                child.updateBoard(move)
                nodeValue = self.findBestMove(child, alpha, beta, False, depth + 1)[0]
                maxEval = max(maxEval, nodeValue);
                alpha = max(alpha, nodeValue)
                if maxEval == nodeValue:
                    bestMove = move
                if beta <= alpha:
                    print("pruning max")
                    break
            return maxEval, bestMove
        
        if not maximizing:
            maxEval = float('inf')
            bestMove = None
            movements = board.findAvailableMovements(PLAYERS.BLUE.value)

            if movements["jumps"]:
                movements = movements["jumps"]
            else: 
                movements = movements["moves"]

            # print("minimizing.", " depth: ", depth)
            
            for move in movements:
                temp_matrix = board.copyMatrix()   
                child = Board(matrix=temp_matrix, redPawns=board.redPawns, bluePawns=board.bluePawns, blueKings = board.blueKings, redKings = board.redKings)
                # print("length of movements: ", len(movements))

                child.updateBoard(move)
               
                nodeValue = self.findBestMove(child, alpha, beta, True, depth + 1)[0]
                maxEval = min(maxEval, nodeValue)
                beta = min(beta, nodeValue)
                if maxEval == nodeValue:
                    bestMove = move
                if beta <= alpha:
                    print("pruning min")
                    break
                
            
            return maxEval, bestMove
              
            
                
