

from enum import Enum


class AgentsNames(Enum):
    MINIMAX = "MiniMax"
    RANDOM = "Random"
    PODAMINIMAX = "Poda Alpha-Beta MiniMax"
    QAGENT = "QLearning"
    NEURALAGENT = "Neural Network"
    YOURSELF = "Yourself"

class GameStatus(Enum):
    RUNNING = "Running"
    PAUSED = "Paused"
    ENDED = "Ended"

class PLAYERS(Enum):
    RED = 1
    BLUE = 2
    NONE = 0
    DRAW = 3