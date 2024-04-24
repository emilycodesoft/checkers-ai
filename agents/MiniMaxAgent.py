
from random import choice

from game.Board import Board
from enums import PLAYERS, AgentsNames


class MiniMaxAgent:
    def __init__(self):
        self.name = AgentsNames.MINIMAX.value
        self.maxDepth = 3
        self.nodesMap = []
    def move(self, screen, board, player):
        maxPlayer = None
        if (player == PLAYERS.RED.value):
            maxPlayer = True
        else: 
            maxPlayer = False
        return self.findBestMove(screen, board, maxPlayer)
   
    def findBestMove(self,screen, board, maximizing = True, depth = 0):
        if (depth == 0): self.nodesMap.clear()
        isTerminal = board.checkWinner()
        if(isTerminal or depth == self.maxDepth):
                state = board.redPawns - board.bluePawns
                return state
                
        if (maximizing):
            # Initialize best to the lowest possible value
            best = -800;
            # Loop through all empty cells
            movements = board.findAvailableMovements(PLAYERS.RED.value)
           
            if movements["jumps"]:
                movements = movements["jumps"]
            else: 
                movements = movements["moves"]
           
            for move in movements:           
                child = Board(screen, board.copyMatrix())
                child.updateBoard(move)
                nodeValue = self.findBestMove(screen, child, False, depth + 1);
                best = max(best, nodeValue);
                # board.undoMove(move)
                if depth == 0:
                    self.nodesMap.append((nodeValue,move))
            if depth == 0:
                print("BEST: ", best)
                gg = filter(lambda x: x[0] == best, self.nodesMap)
                return list(gg)
              
            return best
        
        if not maximizing:
            best = 100
            movements = board.findAvailableMovements(PLAYERS.BLUE.value)
           
            if movements["jumps"]:
                movements = movements["jumps"]
            else: 
                movements = movements["moves"]
          
            
            for move in movements:
                child = Board(screen, board.copyMatrix())
                child.updateBoard(move)
                nodeValue = self.findBestMove(screen, child, True, depth + 1)
                best = min(best, nodeValue)
                # board.undoMove(move)
                if depth == 0:
                    self.nodesMap.append((nodeValue,move))
            if depth == 0:
                print("BEST: ", best)
                gg = filter(lambda x: x[0] == best, self.nodesMap)
                return list(gg)
              
            return best
                
