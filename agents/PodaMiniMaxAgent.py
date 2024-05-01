
from copy import deepcopy
from game.Board import Board
from enums import PLAYERS, AgentsNames
import turtle
from time import sleep

screen = turtle.Screen()
class PodaMiniMaxAgent:
    def __init__(self):
        self.name = AgentsNames.PODAMINIMAX.value
        self.maxDepth = 6

    def move(self, board, player):
        maxPlayer = True if player == PLAYERS.RED.value else False
        alpha = float('-inf')
        beta = float('inf')
        return self.findBestMove(board, maxPlayer, 0, alpha, beta)

import random  # Import random library

def findBestMove(self, board, maximizing=True, depth=0, alpha=float('-inf'), beta=float('inf')):
        isTerminal = board.checkWinner()  
        if isTerminal or depth == self.maxDepth:
            return board.evaluate(), None

        if maximizing:
            maxEval = float('-inf')
            bestMoves = []  # List to store the best moves
            movements = board.findAvailableMovements(PLAYERS.RED.value)

            if movements["jumps"]:
                movements = movements["jumps"]
            else:
                movements = movements["moves"]

            for move in movements:
                temp_matrix = board.copyMatrix()
                child = Board(matrix=temp_matrix, redPawns=board.redPawns, bluePawns=board.bluePawns, blueKings=board.blueKings, redKings=board.redKings)
                child.updateBoard(move)
                eval = self.findBestMove(child, False, depth + 1, alpha, beta)[0]
                if eval > maxEval:
                    maxEval = eval
                    bestMoves = [move]  # Reset the list with the new best move
                elif eval == maxEval:
                    bestMoves.append(move)  # Add this move to the list of best moves
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, random.choice(bestMoves) if bestMoves else False  # Choose randomly from the best moves

        else:
            minEval = float('inf')
            bestMoves = []  # List to store the best moves
            movements = board.findAvailableMovements(PLAYERS.BLUE.value)

            if movements["jumps"]:
                movements = movements["jumps"]
            else:
                movements = movements["moves"]

            for move in movements:
                temp_matrix = board.copyMatrix()
                child = Board(matrix=temp_matrix, redPawns=board.redPawns, bluePawns=board.bluePawns, blueKings=board.blueKings, redKings=board.redKings)
                child.updateBoard(move)
                eval = self.findBestMove(child, True, depth + 1, alpha, beta)[0]
                if eval < minEval:
                    minEval = eval
                    bestMoves = [move]  # Reset the list with the new best move
                elif eval == minEval:
                    bestMoves.append(move)  # Add this move to the list of best moves
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, random.choice(bestMoves) if bestMoves else False  # Choose randomly from the best moves
