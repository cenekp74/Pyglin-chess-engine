# Pyglin chess engine
Chess engine written in python

#### Lichess: https://lichess.org/@/Pyglin

## Logic:
Interprets board as a 2d array (empty square = '+')
Knights moves calculated using pythagoras (square must be sq root from original square)
Can calculate legal or pseudo legal moves, but calculating legal is very slow because it has to check is king can be captured by any of enemy pieces, threfore the bot uses pseudo legal moves.
Supports communication with python-chess library.

## Algorythms:
### Pvs alpha-beta
Uses the pvs alpha-beta prunning algorythm.
The pvs algorythm is enhanced with simple zero window search.


### Quiesce search:
Runs short quiesce search for "good" captures.
### Evaluation:
Uses static evaluation based on position of pieces on board.
King and pawns evaluation changes in endgame.
Does not detect mate - allows king capture => can make illegal moves or mate without realising on depth 1
