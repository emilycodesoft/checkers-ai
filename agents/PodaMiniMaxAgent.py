
from copy import deepcopy
from game.Board import Board
from enums import PLAYERS, AgentsNames
import turtle
import random
screen = turtle.Screen()
class PodaMiniMaxAgent:
    def __init__(self):
        self.name = AgentsNames.PODAMINIMAX.value
        self.maxDepth = 6
        self.transpositionTable = {}  # Tabla de transposición para almacenar evaluaciones previas

    def move(self, board, player):
        maxPlayer = True if player == PLAYERS.RED.value else False
        alpha = float('-inf')
        beta = float('inf')
        self.transpositionTable.clear()  # Limpiar la tabla al inicio de cada movimiento
        return self.findBestMove(board, maxPlayer, 0, alpha, beta)

    def findBestMove(self, board, maximizing=True, depth=0, alpha=float('-inf'), beta=float('inf')):
        # Crear una clave única para el estado actual del tablero
        board_key = (board.hash(), maximizing, depth)
        if board_key in self.transpositionTable:
            # print("Transposition table hit!")
            return self.transpositionTable[board_key]

        isTerminal = board.checkWinner()
        if isTerminal or depth == self.maxDepth:
            eval_result = (board.evaluate(), None)
            self.transpositionTable[board_key] = eval_result
            return eval_result

        if maximizing:
            maxEval = float('-inf')
            bestMoves = []
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
                    bestMoves = [move]
                elif eval == maxEval:
                    bestMoves.append(move)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            result = (maxEval, random.choice(bestMoves) if bestMoves else False)
            self.transpositionTable[board_key] = result
            return result

        else:
            minEval = float('inf')
            bestMoves = []
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
                    bestMoves = [move]
                elif eval == minEval:
                    bestMoves.append(move)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            result = (minEval, random.choice(bestMoves) if bestMoves else False)
            self.transpositionTable[board_key] = result
            return result