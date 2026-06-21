# Checkers AI

A classic 8×8 checkers (draughts) game in Python where you play against — or watch — AI opponents built with adversarial search. The board renders with Python's `turtle` graphics.

University course project on **adversarial search / game-playing AI**.

---

## AI agents

- **Minimax** — minimax search over the game tree
- **Alpha-Beta Minimax** — minimax with alpha-beta pruning (search depth 3)
- **Random** — picks a legal move at random (a baseline to test the others against)
- **Human** — you play by clicking the board

The search scores a position with a simple material heuristic:

```
score = redPawns − bluePawns + 0.5·(redKings − blueKings)
```

maximizing for Red and minimizing for Blue. Alpha-beta pruning skips branches that can't change the outcome, so it reaches the same depth far faster than plain minimax.

---

## Game rules implemented

- Standard checkers on the dark squares of an 8×8 board, 12 pieces per side
- Regular pieces move forward diagonally; reaching the far row **kings** them
- Kings move and capture in both directions
- Captures ("jumps") are mandatory and **chain** (multi-jumps in a single turn)
- A side loses when it runs out of pieces

---

## Running it

Requires Python 3 — it uses the standard-library `turtle` module, so there are no external dependencies.

```bash
python index.py
```

A window opens with the board; click your piece and its destination to move when it's your turn.

---

## Project structure

```
index.py          — entry point: sets up the turtle window and game loop
CheckersGame.py   — game orchestration (turns, agents, win checks)
game/
  Board.py        — board state, move/jump generation, evaluation, kinging
  Grid.py         — individual square rendering
  Titles.py       — board tiles / labels
agents/
  MiniMaxAgent.py       — minimax
  PodaMiniMaxAgent.py   — minimax with alpha-beta pruning
  RandomAgent.py        — random baseline
  YourselfAgent.py      — human input
enums.py          — player, agent and game-status enums
utils.py          — helpers (grid bounds, console logging)
```
