# Pyglin-chess-engine
Chess engine written in python

### Chess logic implemented using python-chess library: https://github.com/niklasf/python-chess

## Algorythms:
### Pvs alpha-beta
Uses the pvs alpha-beta prunning algorythm and transposition table for move sorting.
The pvs algorythm is enhanced with simple zero window search.
### Quiesce search:
Runs short quiesce search for "good" captures and checks
The count of quiesce searches is limited to 50, otherwise it can slow down too much while playing bullet in complicated positions.
### Evaluation:
Uses static evaluation based on position of pieces on board.
Evaluates checkmate positions as +10000 or -10000

