from enums import AgentsNames


class YourselfAgent:
    def __init__(self, board):
        self.name =  AgentsNames.YOURSELF.value
        self.board = board