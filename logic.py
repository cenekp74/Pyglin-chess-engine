import copy
import random
import chess

BOARD = [['+' for i in range(8)] for i in range(8)]

COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


def is_valid_square(square):
    if square[0] >= 0 and square[0] < 8 and square[1] >= 0 and square[1] < 8:
        return True
    else:
        return False


class Move():
    def __init__(self, fromSquare, toSquare, promotion=None, castling=None):
        self.fromSquare = fromSquare
        self.toSquare = toSquare
        self.promotion = promotion
        self.castling = castling

    def uci(self): 
        return get_square_name(self.fromSquare) + get_square_name(self.toSquare)

    def __repr__(self):
        return self.uci()


class Board():
    def __init__(self, pos=[['+' for i in range(8)] for i in range(8)], turn=1,fen = None, cr={1: [False, False], 0: [False, False]}, moves=[], history=[], shortHist = [], enPassant=None, halfMoves=0):
        self.pos = pos
        self.turn = turn
        self.cr = cr
        self.moves = moves
        self.history = history
        self.shortHist = shortHist
        self.enPassant = enPassant
        self.halfMoves = halfMoves
        if fen: self.load_fen(fen)

    def __repr__(self):
        string = ''
        for row in reversed(self.pos):
            string = string + str(row) + ' \n'
        return string

    def load_fen(self, fen):
        fen1 = fen.split(' ')[0]
        for rowN, row in enumerate(reversed(fen1.split('/'))):
            file = 0
            for symbolN, symbol in enumerate(row):
                if symbol.isnumeric():
                    for space in range(int(symbol)):
                        self.pos[rowN][file] = '+'
                        file += 1
                else:
                    self.pos[rowN][file] = symbol
                    file += 1
        fen2 = fen.split(' ', 1)[1]
        if fen2[0] == 'w': self.turn = 1
        else: self.turn = 0
        castling = fen2.split(' ')[1]
        if castling == '-': self.cr = {0: [False, False], 1: [False, False]}
        else:
            if 'K' in castling: self.cr[1][0] = True
            else: self.cr[1][0] = False
            if 'k' in castling: self.cr[0][0] = True
            else: self.cr[0][0] = False
            if 'Q' in castling: self.cr[1][1] = True
            else: self.cr[1][0] = False
            if 'q' in castling: self.cr[0][1] = True
            else: self.cr[0][1] = False
        self.halfMoves = int(fen.split(' ')[4])

    def get_attacks(self, turn=None, pos=None):
        if not pos:
            pos = self.pos
        if turn == None:
            turn = self.turn
        for rowN, row in enumerate(pos):
            for colN, piece in enumerate(row):
                if piece == '+':
                    continue
                if turn == 1:
                    if piece == 'R':
                        directions = [
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                if piece != '+':
                                    yield ([rowN, colN], square)
                                    break
                                yield ([rowN, colN], square)

                    elif piece == 'B':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                if piece != '+':
                                    yield ([rowN, colN], square)
                                    break
                                yield ([rowN, colN], square)
                    elif piece == 'Q':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)],
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                if piece != '+':
                                    yield ([rowN, colN], square)
                                    break
                                yield ([rowN, colN], square)
                    elif piece == 'N':
                        for r in range(-2, 3):
                            for c in range(-2, 3):
                                if r ** 2 + c ** 2 == 5:
                                    square = [r+rowN, c+colN]
                                    if not is_valid_square(square):
                                        continue
                                    piece = pos[square[0]][square[1]]
                                    yield ([rowN, colN], square)
                    elif piece == 'K':
                        for r in range(-1, 2):
                            for c in range(-1, 2):
                                square = [r+rowN, c+colN]
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                yield ([rowN, colN], square)
                    elif piece == 'P':
                        if is_valid_square([rowN+1, colN-1]):
                            yield ([rowN, colN], [rowN+1, colN-1])
                        if is_valid_square([rowN+1, colN+1]):
                            yield ([rowN, colN], [rowN+1, colN+1])
                else:
                    if piece == 'r':
                        directions = [
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                if piece != '+':
                                    yield ([rowN, colN], square)
                                    break
                                yield ([rowN, colN], square)

                    elif piece == 'b':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                if piece != '+':
                                    yield ([rowN, colN], square)
                                    break
                                yield ([rowN, colN], square)
                    elif piece == 'q':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)],
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                if piece != '+':
                                    yield ([rowN, colN], square)
                                    break
                                yield ([rowN, colN], square)
                    elif piece == 'n':
                        for r in range(-2, 3):
                            for c in range(-2, 3):
                                if r ** 2 + c ** 2 == 5:
                                    square = [r+rowN, c+colN]
                                    if not is_valid_square(square):
                                        continue
                                    piece = pos[square[0]][square[1]]
                                    yield ([rowN, colN], square)
                    elif piece == 'k':
                        for r in range(-1, 2):
                            for c in range(-1, 2):
                                square = [r+rowN, c+colN]
                                if not is_valid_square(square):
                                    continue
                                piece = pos[square[0]][square[1]]
                                yield ([rowN, colN], square)
                    elif piece == 'p':
                        if is_valid_square([rowN-1, colN+1]):
                            yield ([rowN, colN], [rowN-1, colN+1])
                        if is_valid_square([rowN-1, colN-1]):
                            yield ([rowN, colN], [rowN-1, colN-1])

    def get_king(self, color, pos=None):
        if not pos:
            pos = self.pos
        if color == 1:
            king = 'K'
        else:
            king = 'k'
        for rowN, row in enumerate(pos):
            if king in row:
                return [rowN, row.index(king)]
        return None

    def is_check(self):
        return self.can_capture_king(0 if self.turn == 1 else 1)

    def gives_check(self, move):
        tempPos = copy.deepcopy(self.pos)
        piece = tempPos[move.fromSquare[0]][move.fromSquare[1]]
        tempPos[move.fromSquare[0]][move.fromSquare[1]] = '+'
        tempPos[move.toSquare[0]][move.toSquare[1]] = piece
        return self.can_capture_king(0 if self.turn == 1 else 1, pos=tempPos)

    def can_capture_king(self, turn=None, pos=None):
        if not pos:
            pos = self.pos
        if turn == None:
            turn = self.turn
        kingSquare = self.get_king(0 if turn == 1 else 1, pos=pos)
        for attack in self.get_attacks(pos=pos, turn=turn):
            if attack[1] == kingSquare:
                return True
        return False

    def exposes_king(self, move):
        tempPos = copy.deepcopy(self.pos)
        piece = tempPos[move[0][0]][move[0][1]]
        tempPos[move[0][0]][move[0][1]] = '+'
        tempPos[move[1][0]][move[1][1]] = piece
        if self.can_capture_king(turn=0 if self.turn == 1 else 1, pos=tempPos):
            return True
        else:
            return False

#needs updte -_-
    def get_legal_moves(self):
        for rowN, row in enumerate(self.pos):
            if self.turn == 1:
                for colN, piece in enumerate(row):
                    if piece == '+':
                        continue
                    if piece == 'R':
                        directions = [
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    if not is_valid_square(square):
                                        continue
                                    if self.pos[square[0]][square[1]] != '+':
                                        break
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    break
                                elif pieceTo.islower():
                                    yield Move([rowN, colN], square)
                                    break
                    elif piece == 'B':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    if not is_valid_square(square):
                                        continue
                                    if self.pos[square[0]][square[1]] != '+':
                                        break
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    break
                                elif pieceTo.islower():
                                    yield Move([rowN, colN], square)
                                    break
                    elif piece == 'Q':
                        directions = [
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)],
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    if not is_valid_square(square):
                                        continue
                                    if self.pos[square[0]][square[1]] != '+':
                                        break
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    break
                                elif pieceTo.islower():
                                    yield Move([rowN, colN], square)
                                    break
                    elif piece == 'N':
                        for r in range(-2, 3):
                            for c in range(-2, 3):
                                if r ** 2 + c ** 2 == 5:
                                    square = [r+rowN, c+colN]
                                    if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                        continue
                                    pieceTo = self.pos[square[0]][square[1]]
                                    if pieceTo == '+':
                                        yield Move([rowN, colN], square)
                                    elif pieceTo.islower():
                                        yield Move([rowN, colN], square)
                    elif piece == 'K':
                        for r in range(-1, 2):
                            for c in range(-1, 2):
                                square = [r+rowN, c+colN]
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.islower():
                                    yield Move([rowN, colN], square)

                        if self.cr[1][0]:
                            if is_valid_square([rowN, colN+1]) and is_valid_square([rowN, colN+2]):
                                if self.pos[rowN][colN+1] == '+' and self.pos[rowN][colN+2] == '+':
                                    if not self.exposes_king(([rowN, colN], [rowN, colN+1])) and not self.exposes_king(([rowN, colN], [rowN, colN+2])):
                                        yield Move([rowN, colN], [rowN, colN+2])
                        if self.cr[1][1]:
                            if is_valid_square([rowN, colN-1]) and is_valid_square([rowN, colN-2]) and is_valid_square([rowN, colN-3]):
                                if self.pos[rowN][colN-1] == '+' and self.pos[rowN][colN-2] == '+' and self.pos[rowN][colN-3] == '+':
                                    if not self.exposes_king(([rowN, colN], [rowN, colN-1])) and not self.exposes_king(([rowN, colN], [rowN, colN-2])):
                                        yield Move([rowN, colN], [rowN, colN-2])
                    elif piece == 'P':
                        if rowN == 1 and self.pos[rowN+2][colN] == '+' and self.pos[rowN+1][colN] == '+':
                            if not self.exposes_king(([rowN, colN], [rowN+2, colN])):
                                yield Move([rowN, colN], [rowN+2, colN])
                        if is_valid_square([rowN+1, colN]):
                            if self.pos[rowN+1][colN] == '+':
                                if not self.exposes_king(([rowN, colN], [rowN+1, colN])):
                                    if rowN+1 == 7:
                                        yield Move([rowN, colN], [rowN+1, colN], promotion='Q')
                                        yield Move([rowN, colN], [rowN+1, colN], promotion='R')
                                        yield Move([rowN, colN], [rowN+1, colN], promotion='B')
                                        yield Move([rowN, colN], [rowN+1, colN], promotion='N')
                                    else:
                                        yield Move([rowN, colN], [rowN+1, colN])
                        if is_valid_square([rowN+1, colN-1]) and self.pos[rowN+1][colN-1] != '+' and self.pos[rowN+1][colN-1].islower():
                            if not self.exposes_king(([rowN, colN], [rowN+1, colN-1])):
                                if rowN+1 == 7:
                                    yield Move([rowN, colN], [rowN+1, colN-1], promotion='Q')
                                    yield Move([rowN, colN], [rowN+1, colN-1], promotion='R')
                                    yield Move([rowN, colN], [rowN+1, colN-1], promotion='B')
                                    yield Move([rowN, colN], [rowN+1, colN-1], promotion='N')
                                else:
                                    yield Move([rowN, colN], [rowN+1, colN-1])
                        if is_valid_square([rowN+1, colN+1]) and self.pos[rowN+1][colN+1] != '+' and self.pos[rowN+1][colN+1].islower():
                            if not self.exposes_king(([rowN, colN], [rowN+1, colN+1])):
                                if rowN+1 == 7:
                                    yield Move([rowN, colN], [rowN+1, colN+1], promotion='Q')
                                    yield Move([rowN, colN], [rowN+1, colN+1], promotion='R')
                                    yield Move([rowN, colN], [rowN+1, colN+1], promotion='B')
                                    yield Move([rowN, colN], [rowN+1, colN+1], promotion='N')
                                else:
                                    yield Move([rowN, colN], [rowN+1, colN+1])
            else:
                for colN, piece in enumerate(row):
                    if piece == '+':
                        continue
                    if piece == 'r':
                        directions = [
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    if not is_valid_square(square):
                                        continue
                                    if self.pos[square[0]][square[1]] != '+':
                                        break
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    yield Move([rowN, colN], square)
                                    break
                                elif pieceTo.islower():
                                    break
                    elif piece == 'b':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    if not is_valid_square(square):
                                        continue
                                    if self.pos[square[0]][square[1]] != '+':
                                        break
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    yield Move([rowN, colN], square)
                                    break
                                elif pieceTo.islower():
                                    break
                    elif piece == 'q':
                        directions = [
                            [[rowN + i, colN + i] for i in range(1, 8)],
                            [[rowN + i, colN - i] for i in range(1, 8)],
                            [[rowN - i, colN + i] for i in range(1, 8)],
                            [[rowN - i, colN - i] for i in range(1, 8)],
                            [[rowN + i, colN] for i in range(1, 8 - rowN)],
                            [[rowN - i, colN] for i in range(1, rowN + 1)],
                            [[rowN, colN + i] for i in range(1, 8 - colN)],
                            [[rowN, colN - i] for i in range(1, colN + 1)]
                        ]
                        for direction in directions:
                            for square in direction:
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    if not is_valid_square(square):
                                        continue
                                    if self.pos[square[0]][square[1]] != '+':
                                        break
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    yield Move([rowN, colN], square)
                                    break
                                elif pieceTo.islower():
                                    break
                    elif piece == 'n':
                        for r in range(-2, 3):
                            for c in range(-2, 3):
                                if r ** 2 + c ** 2 == 5:
                                    square = [r+rowN, c+colN]
                                    if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                        continue
                                    pieceTo = self.pos[square[0]][square[1]]
                                    if pieceTo == '+':
                                        yield Move([rowN, colN], square)
                                    elif pieceTo.isupper():
                                        yield Move([rowN, colN], square)
                    elif piece == 'k':
                        for r in range(-1, 2):
                            for c in range(-1, 2):
                                square = [r+rowN, c+colN]
                                if not is_valid_square(square) or self.exposes_king(([rowN, colN], square)):
                                    continue
                                pieceTo = self.pos[square[0]][square[1]]
                                if pieceTo == '+':
                                    yield Move([rowN, colN], square)
                                elif pieceTo.isupper():
                                    yield Move([rowN, colN], square)

                        if self.cr[0][0]:
                            if self.pos[rowN][colN+1] == '+' and self.pos[rowN][colN+2] == '+':
                                if not self.exposes_king(([rowN, colN], [rowN, colN+1])) and not self.exposes_king(([rowN, colN], [rowN, colN+2])):
                                    yield Move([rowN, colN], [rowN, colN+2])
                        if self.cr[0][1]:
                            if self.pos[rowN][colN-1] == '+' and self.pos[rowN][colN-2] == '+' and self.pos[rowN][colN-3] == '+':
                                if not self.exposes_king(([rowN, colN], [rowN, colN-1])) and not self.exposes_king(([rowN, colN], [rowN, colN-2])):
                                    yield Move([rowN, colN], [rowN, colN-2])
                    elif piece == 'p':
                        if rowN == 6 and self.pos[rowN-2][colN] == '+' and self.pos[rowN-1][colN] == '+':
                            if not self.exposes_king(([rowN, colN], [rowN-2, colN])):
                                yield Move([rowN, colN], [rowN-2, colN])
                        if is_valid_square([rowN-1, colN]):
                            if self.pos[rowN-1][colN] == '+':
                                if not self.exposes_king(([rowN, colN], [rowN-1, colN])):
                                    if rowN-1 == 0:
                                        yield Move([rowN, colN], [rowN-1, colN], promotion='q')
                                        yield Move([rowN, colN], [rowN-1, colN], promotion='r')
                                        yield Move([rowN, colN], [rowN-1, colN], promotion='b')
                                        yield Move([rowN, colN], [rowN-1, colN], promotion='n')
                                    else:
                                        yield Move([rowN, colN], [rowN-1, colN])
                        if is_valid_square([rowN-1, colN-1]) and self.pos[rowN-1][colN-1] != '+' and self.pos[rowN-1][colN-1].isupper():
                            if not self.exposes_king(([rowN, colN], [rowN-1, colN-1])):
                                if rowN-1 == 0:
                                    yield Move([rowN, colN], [rowN-1, colN-1], promotion='q')
                                    yield Move([rowN, colN], [rowN-1, colN-1], promotion='r')
                                    yield Move([rowN, colN], [rowN-1, colN-1], promotion='b')
                                    yield Move([rowN, colN], [rowN-1, colN-1], promotion='n')
                                else:
                                    yield Move([rowN, colN], [rowN-1, colN-1])
                        if is_valid_square([rowN-1, colN+1]) and self.pos[rowN-1][colN+1] != '+' and self.pos[rowN-1][colN+1].isupper():
                            if not self.exposes_king(([rowN, colN], [rowN-1, colN+1])):
                                if rowN-1 == 0:
                                    yield Move([rowN, colN], [rowN-1, colN+1], promotion='q')
                                    yield Move([rowN, colN], [rowN-1, colN+1], promotion='r')
                                    yield Move([rowN, colN], [rowN-1, colN+1], promotion='b')
                                    yield Move([rowN, colN], [rowN-1, colN+1], promotion='n')
                                else:
                                    yield Move([rowN, colN], [rowN-1, colN+1])

    def get_pseudo_legal_moves(self):
        for rowN, row in enumerate(self.pos):
                    if self.turn == 1:
                        for colN, piece in enumerate(row):
                            if piece == '+':
                                continue
                            if piece == 'R':
                                directions = [
                                    [[rowN + i, colN] for i in range(1, 8 - rowN)],
                                    [[rowN - i, colN] for i in range(1, rowN + 1)],
                                    [[rowN, colN + i] for i in range(1, 8 - colN)],
                                    [[rowN, colN - i] for i in range(1, colN + 1)]
                                ]
                                for direction in directions:
                                    for square in direction:
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            break
                                        elif pieceTo.islower():
                                            yield Move([rowN, colN], square)
                                            break
                            elif piece == 'B':
                                directions = [
                                    [[rowN + i, colN + i] for i in range(1, 8)],
                                    [[rowN + i, colN - i] for i in range(1, 8)],
                                    [[rowN - i, colN + i] for i in range(1, 8)],
                                    [[rowN - i, colN - i] for i in range(1, 8)]
                                ]
                                for direction in directions:
                                    for square in direction:
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            break
                                        elif pieceTo.islower():
                                            yield Move([rowN, colN], square)
                                            break
                            elif piece == 'Q':
                                directions = [
                                    [[rowN + i, colN] for i in range(1, 8 - rowN)],
                                    [[rowN - i, colN] for i in range(1, rowN + 1)],
                                    [[rowN, colN + i] for i in range(1, 8 - colN)],
                                    [[rowN, colN - i] for i in range(1, colN + 1)],
                                    [[rowN + i, colN + i] for i in range(1, 8)],
                                    [[rowN + i, colN - i] for i in range(1, 8)],
                                    [[rowN - i, colN + i] for i in range(1, 8)],
                                    [[rowN - i, colN - i] for i in range(1, 8)]
                                ]
                                for direction in directions:
                                    for square in direction:
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            break
                                        elif pieceTo.islower():
                                            yield Move([rowN, colN], square)
                                            break
                            elif piece == 'N':
                                for r in range(-2, 3):
                                    for c in range(-2, 3):
                                        if r ** 2 + c ** 2 == 5:
                                            square = [r+rowN, c+colN]
                                            if not is_valid_square(square):
                                                continue
                                            pieceTo = self.pos[square[0]][square[1]]
                                            if pieceTo == '+':
                                                yield Move([rowN, colN], square)
                                            elif pieceTo.islower():
                                                yield Move([rowN, colN], square)
                            elif piece == 'K':
                                for r in range(-1, 2):
                                    for c in range(-1, 2):
                                        square = [r+rowN, c+colN]
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.islower():
                                            yield Move([rowN, colN], square)
                                if self.can_capture_king(turn=0): continue
                                if self.cr[1][0]:
                                    if is_valid_square([rowN, colN+1]) and is_valid_square([rowN, colN+2]):
                                        if self.pos[rowN][colN+1] == '+' and self.pos[rowN][colN+2] == '+':
                                            yield Move([rowN, colN], [rowN, colN+2], castling='K')
                                if self.cr[1][1]:
                                    if is_valid_square([rowN, colN-1]) and is_valid_square([rowN, colN-2]) and is_valid_square([rowN, colN-3]):
                                        if self.pos[rowN][colN-1] == '+' and self.pos[rowN][colN-2] == '+' and self.pos[rowN][colN-3] == '+':
                                            yield Move([rowN, colN], [rowN, colN-2], castling='Q')
                            elif piece == 'P':
                                if rowN == 1 and self.pos[rowN+2][colN] == '+' and self.pos[rowN+1][colN] == '+':
                                    yield Move([rowN, colN], [rowN+2, colN])
                                if is_valid_square([rowN+1, colN]):
                                    if self.pos[rowN+1][colN] == '+':
                                        if rowN+1 == 7:
                                            yield Move([rowN, colN], [rowN+1, colN], promotion='Q')
                                            yield Move([rowN, colN], [rowN+1, colN], promotion='R')
                                            yield Move([rowN, colN], [rowN+1, colN], promotion='B')
                                            yield Move([rowN, colN], [rowN+1, colN], promotion='N')
                                        else:
                                            yield Move([rowN, colN], [rowN+1, colN])
                                if is_valid_square([rowN+1, colN-1]) and self.pos[rowN+1][colN-1] != '+' and self.pos[rowN+1][colN-1].islower():
                                    if rowN+1 == 7:
                                        yield Move([rowN, colN], [rowN+1, colN-1], promotion='Q')
                                        yield Move([rowN, colN], [rowN+1, colN-1], promotion='R')
                                        yield Move([rowN, colN], [rowN+1, colN-1], promotion='B')
                                        yield Move([rowN, colN], [rowN+1, colN-1], promotion='N')
                                    else:
                                        yield Move([rowN, colN], [rowN+1, colN-1])
                                if is_valid_square([rowN+1, colN+1]) and self.pos[rowN+1][colN+1] != '+' and self.pos[rowN+1][colN+1].islower():
                                    if rowN+1 == 7:
                                        yield Move([rowN, colN], [rowN+1, colN+1], promotion='Q')
                                        yield Move([rowN, colN], [rowN+1, colN+1], promotion='R')
                                        yield Move([rowN, colN], [rowN+1, colN+1], promotion='B')
                                        yield Move([rowN, colN], [rowN+1, colN+1], promotion='N')
                                    else:
                                        yield Move([rowN, colN], [rowN+1, colN+1])
                    else:
                        for colN, piece in enumerate(row):
                            if piece == '+':
                                continue
                            if piece == 'r':
                                directions = [
                                    [[rowN + i, colN] for i in range(1, 8 - rowN)],
                                    [[rowN - i, colN] for i in range(1, rowN + 1)],
                                    [[rowN, colN + i] for i in range(1, 8 - colN)],
                                    [[rowN, colN - i] for i in range(1, colN + 1)]
                                ]
                                for direction in directions:
                                    for square in direction:
                                        if not is_valid_square(square) :
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            yield Move([rowN, colN], square)
                                            break
                                        elif pieceTo.islower():
                                            break
                            elif piece == 'b':
                                directions = [
                                    [[rowN + i, colN + i] for i in range(1, 8)],
                                    [[rowN + i, colN - i] for i in range(1, 8)],
                                    [[rowN - i, colN + i] for i in range(1, 8)],
                                    [[rowN - i, colN - i] for i in range(1, 8)]
                                ]
                                for direction in directions:
                                    for square in direction:
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            yield Move([rowN, colN], square)
                                            break
                                        elif pieceTo.islower():
                                            break
                            elif piece == 'q':
                                directions = [
                                    [[rowN + i, colN + i] for i in range(1, 8)],
                                    [[rowN + i, colN - i] for i in range(1, 8)],
                                    [[rowN - i, colN + i] for i in range(1, 8)],
                                    [[rowN - i, colN - i] for i in range(1, 8)],
                                    [[rowN + i, colN] for i in range(1, 8 - rowN)],
                                    [[rowN - i, colN] for i in range(1, rowN + 1)],
                                    [[rowN, colN + i] for i in range(1, 8 - colN)],
                                    [[rowN, colN - i] for i in range(1, colN + 1)]
                                ]
                                for direction in directions:
                                    for square in direction:
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            yield Move([rowN, colN], square)
                                            break
                                        elif pieceTo.islower():
                                            break
                            elif piece == 'n':
                                for r in range(-2, 3):
                                    for c in range(-2, 3):
                                        if r ** 2 + c ** 2 == 5:
                                            square = [r+rowN, c+colN]
                                            if not is_valid_square(square):
                                                continue
                                            pieceTo = self.pos[square[0]][square[1]]
                                            if pieceTo == '+':
                                                yield Move([rowN, colN], square)
                                            elif pieceTo.isupper():
                                                yield Move([rowN, colN], square)
                            elif piece == 'k':
                                for r in range(-1, 2):
                                    for c in range(-1, 2):
                                        square = [r+rowN, c+colN]
                                        if not is_valid_square(square):
                                            continue
                                        pieceTo = self.pos[square[0]][square[1]]
                                        if pieceTo == '+':
                                            yield Move([rowN, colN], square)
                                        elif pieceTo.isupper():
                                            yield Move([rowN, colN], square)
                                if self.can_capture_king(turn=1): continue
                                if self.cr[0][0]:
                                    if self.pos[rowN][colN+1] == '+' and self.pos[rowN][colN+2] == '+':
                                        yield Move([rowN, colN], [rowN, colN+2], castling='k')
                                if self.cr[0][1]:
                                    if self.pos[rowN][colN-1] == '+' and self.pos[rowN][colN-2] == '+' and self.pos[rowN][colN-3] == '+':
                                        yield Move([rowN, colN], [rowN, colN-2], castling='q')
                            elif piece == 'p':
                                if rowN == 6 and self.pos[rowN-2][colN] == '+' and self.pos[rowN-1][colN] == '+':
                                    if not self.exposes_king(([rowN, colN], [rowN-2, colN])):
                                        yield Move([rowN, colN], [rowN-2, colN])
                                if is_valid_square([rowN-1, colN]):
                                    if self.pos[rowN-1][colN] == '+':
                                        if rowN-1 == 0:
                                            yield Move([rowN, colN], [rowN-1, colN], promotion='q')
                                            yield Move([rowN, colN], [rowN-1, colN], promotion='r')
                                            yield Move([rowN, colN], [rowN-1, colN], promotion='b')
                                            yield Move([rowN, colN], [rowN-1, colN], promotion='n')
                                        else:
                                            yield Move([rowN, colN], [rowN-1, colN])
                                if is_valid_square([rowN-1, colN-1]) and self.pos[rowN-1][colN-1] != '+' and self.pos[rowN-1][colN-1].isupper():
                                    if rowN-1 == 0:
                                        yield Move([rowN, colN], [rowN-1, colN-1], promotion='q')
                                        yield Move([rowN, colN], [rowN-1, colN-1], promotion='r')
                                        yield Move([rowN, colN], [rowN-1, colN-1], promotion='b')
                                        yield Move([rowN, colN], [rowN-1, colN-1], promotion='n')
                                    else:
                                        yield Move([rowN, colN], [rowN-1, colN-1])
                                if is_valid_square([rowN-1, colN+1]) and self.pos[rowN-1][colN+1] != '+' and self.pos[rowN-1][colN+1].isupper():
                                    if rowN-1 == 0:
                                        yield Move([rowN, colN], [rowN-1, colN+1], promotion='q')
                                        yield Move([rowN, colN], [rowN-1, colN+1], promotion='r')
                                        yield Move([rowN, colN], [rowN-1, colN+1], promotion='b')
                                        yield Move([rowN, colN], [rowN-1, colN+1], promotion='n')
                                    else:
                                        yield Move([rowN, colN], [rowN-1, colN+1])

    def move(self, move, uci=None, python_chess=None):
        if python_chess:
            pycm = python_chess[0]
            pycb = python_chess[1]
            move.fromSquare = get_sq_from_name(pycm.uci()[0:2])
            move.toSquare = get_sq_from_name(pycm.uci()[2:4])
            if pycm.promotion:
                move.promotion = chess.piece_symbol(pycm.promotion).lower() if self.turn == 0 else chess.piece_symbol(pycm.promotion).upper()
            if pycb.is_queenside_castling(pycm):
                print(move)
                move.toSquare = [0, 2] if self.turn == 1 else [7, 2]
                move.castling = 'q' if self.turn == 0 else 'Q'
            if pycb.is_kingside_castling(pycm):
                print(move)
                move.toSquare = [0, 6] if self.turn == 1 else [7, 6]
                move.castling = 'k' if self.turn == 0 else 'K'
            if pycb.is_en_passant(pycm):
                if self.turn == 1:
                    self.pos[move.toSquare[0]-1][move.toSquare[1]] = '+'
                else:
                    self.pos[move.toSquare[0]+1][move.toSquare[1]] = '+'
        fen = self.get_fen()
        self.history.append(fen)
        self.shortHist.append(fen.split(' ')[0])
        self.turn = 0 if self.turn == 1 else 1
        self.moves.append(move)
        piece = self.pos[move.fromSquare[0]][move.fromSquare[1]]
        if self.pos[move.toSquare[0]][move.toSquare[1]] != '+':
            self.halfMoves = 0
        self.pos[move.fromSquare[0]][move.fromSquare[1]] = '+'
        self.pos[move.toSquare[0]][move.toSquare[1]] = piece
        if piece == 'p' or piece == 'P':
            self.halfMoves = 0
        #     if move[0][0] == 1:
        #         if move[1][0] == 3:
        #             self.enPassant = move[1]
        else:
            self.halfMoves += 1

        if piece == 'k': self.cr[0] = [False, False]
        elif piece == 'K': self.cr[1] = [False, False]
        elif piece == 'R':
            if move.fromSquare[1] == 0: self.cr[1][0] = False
            elif move.fromSquare[1] == 6: self.cr[1][1] = False
        elif piece == 'r':
            if move.fromSquare[1] == 0: self.cr[0][0] = False
            elif move.fromSquare[1] == 6: self.cr[0][1] = False

        if move.promotion:
            self.pos[move.toSquare[0]][move.toSquare[1]] = move.promotion

        if move.castling == 'q':
            self.pos[7][0] = '+'
            self.pos[7][3] = 'r'
        elif move.castling == 'Q':
            self.pos[0][0] = '+'
            self.pos[0][3] = 'R'
        elif move.castling == 'k':
            self.pos[7][7] = '+'
            self.pos[7][5] = 'r'
        elif move.castling == 'K':
            self.pos[0][7] = '+'
            self.pos[0][5] = 'R'

    def remove_last(self):
        self.turn = 0 if self.turn == 1 else 1
        self.moves.pop()
        self.load_fen(self.history[-1])
        self.history.pop()
        self.shortHist.pop()

    def get_fen(self):
        fen = ''
        empty = 0
        for index, row in enumerate(reversed(self.pos)):
            for piece in row:
                if piece == '+':
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += piece
            if empty > 0:
                fen += str(empty)
                empty = 0
            if index == 7:
                continue
            fen += '/'
        fen += ' w' if self.turn == 1 else ' b'
        if self.cr[1][0] or self.cr[1][1] or self.cr[0][0] or self.cr[0][1]:
            fen += ' '
        else:
            fen += ' -'
        if self.cr[1][0]:
            fen += 'K'
        if self.cr[1][1]:
            fen += 'Q'
        if self.cr[0][0]:
            fen += 'k'
        if self.cr[0][1]:
            fen += 'q'
        fen += ' - '
        fen += str(self.halfMoves)
        fen += ' '
        fen += str(len(self.moves)//2+1)
        return fen

    def is_threefold(self):
        if self.shortHist.count(self.get_fen().split(' ')[0]) >= 2:
            return True
        return False

def get_square_name(square):
    file = COLUMNS[square[1]]
    return file + str(square[0]+1)

def get_sq_from_name(name):
    file = name[0]
    file = COLUMNS.index(file)
    return [int(name[1])-1, file]

def random_move(board):
    return chess.Move.from_uci(random.choice(list(board.get_pseudo_legal_moves())).uci())

def create_pyc_move(board, move):
    pycMove = chess.Move(None, None)
    pycMove.from_square = chess.square(move.fromSquare[1], move.fromSquare[0])
    pycMove.to_square = chess.square(move.toSquare[1], move.toSquare[0])
    if move.promotion:
        if move.promotion.lower() == 'b': pieceType = chess.BISHOP
        elif move.promotion.lower() == 'n': pieceType = chess.KNIGHT
        elif move.promotion.lower() == 'q': pieceType = chess.QUEEN
        elif move.promotion.lower() == 'r': pieceType = chess.ROOK
        pycMove.promotion = pieceType
    return pycMove

def move_from_pyc(pycm, pycb, board):
    move = Move(None, None)
    move.fromSquare = get_sq_from_name(pycm.uci()[0:2])
    move.toSquare = get_sq_from_name(pycm.uci()[2:4])
    if pycm.promotion:
        move.promotion = chess.piece_symbol(pycm.promotion).lower() if board.turn == 0 else chess.piece_symbol(pycm.promotion).upper()
    if pycb.is_queenside_castling(pycm):
        move.castling = 'q' if board.turn == 0 else 'Q'
    if pycb.is_kingside_castling(pycm):
        move.castling = 'k' if board.turn == 0 else 'K'
    if pycb.is_en_passant(pycm):
        if board.turn == 1:
            board.pos[move.toSquare[0]-1][move.toSquare[1]] = '+'
        else:
            board.pos[move.toSquare[0]+1][move.toSquare[1]] = '+'
    return move

if __name__ == '__main__':
    board = Board(fen='rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1')
    print(board.get_fen())
    print(board.pos)
    print(list(board.get_pseudo_legal_moves()))

