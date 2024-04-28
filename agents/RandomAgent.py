from random import choice
from enums import AgentsNames


class RandomAgent:
    def __init__(self, board, player):
        self.name =  AgentsNames.RANDOM.value
        self.player = player
        self.board = board
    def move(self):
        selectedMove = None
        availableMoves = self.board.findAvailableMovements(self.player)
     
        if len(availableMoves) > 0:
            if len(availableMoves["jumps"]):
                selectedMove = choice(availableMoves["jumps"])
            else:
                selectedMove = choice(availableMoves["moves"])
        else:
            selectedMove = False
        return selectedMove