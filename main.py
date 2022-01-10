import chess
import time
import requests
import random

PIECES_VAL = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 0}
PIECES_SQUARES_W = {
    'p': [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 9, -23, -23, 9, 10,  5,
        5, -5, -10,  0,  0, -10, -5,  5,
        0,  0,  0,  22, 22,  0,  0,  0,
        5,  5, 10, 26, 26, 10,  5,  5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    'n': [
        -50, -35, -30, -30, -30, -30, -35, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ],
    'b': [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ],
    'r': [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    'q': [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ],
	'k': [
        20, 40, 10, 0, 0, 20, 35, 20,
        20, 20, 0, 0, 0, 0, 20, 20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]
}

max_tt = 1e5

PIECES_SQUARES_B = {
    'p': list(reversed(PIECES_SQUARES_W['p'])),
    'n': list(reversed(PIECES_SQUARES_W['n'])),
    'b': list(reversed(PIECES_SQUARES_W['b'])),
    'r': list(reversed(PIECES_SQUARES_W['r'])),
    'q': list(reversed(PIECES_SQUARES_W['q'])),
	'k': list(reversed(PIECES_SQUARES_W['k']))
}

PIECES_SQUARES_W_ENDGAME = {
    'p': [
        0,  0,  0,  0,  0,  0,  0,  0,
        -10, -10, -10, -15, -15, -10, -10,  -10,
        -5, -5, -5,  -1,  -1, -5, -5,  5,
        0,  0,  0, 5, 5,  0,  0,  0,
        15,  15, 15, 20, 20, 15,  15,  15,
        30, 30, 30, 32, 32, 30, 30, 30,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    'n': [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ],
    'b': [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ],
    'r': [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0
    ],
    'q': [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ],
    'k': [
        50, -30, -30, -30, -30, -30, -30, -50,
        -30, -30,  0,  0,  0,  0, -30, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 30, 40, 40, 30, -10, -30,
        -30, -10, 20, 30, 30, 20, -10, -30,
        -30, -20, -10,  0,  0, -10, -20, -30,
        -50, -40, -30, -20, -20, -30, -40, -50
    ]
}

PIECES_SQUARES_B_ENDGAME = {
    'p': list(reversed(PIECES_SQUARES_W_ENDGAME['p'])),
    'n': list(reversed(PIECES_SQUARES_W_ENDGAME['n'])),
    'b': list(reversed(PIECES_SQUARES_W_ENDGAME['b'])),
    'r': list(reversed(PIECES_SQUARES_W_ENDGAME['r'])),
    'q': list(reversed(PIECES_SQUARES_W_ENDGAME['q'])),
    'k': list(reversed(PIECES_SQUARES_W_ENDGAME['k']))
}

tt = {}

def quiesce(board, alpha, beta, searchN):
    eval = evaluate(board)
    if searchN > 50:
        print(searchN)
        return eval
    if eval >= beta:
        return beta
    if alpha < eval:
        alpha = eval
    if board.is_checkmate() or board.is_repetition() or board.is_stalemate():
        return eval
    for move in list(board.legal_moves):
        if searchN > 50:
            print(searchN)
            return eval
        if (board.is_capture(move) and not board.is_en_passant(move)):
            if ((PIECES_VAL[board.piece_at(move.to_square).symbol().lower()] - PIECES_VAL[board.piece_at(move.from_square).symbol().lower()]) > 100) or not board.is_attacked_by(not board.turn, move.to_square):
                board.push(move)
                searchN += 1
                score = -quiesce(board, -beta, -alpha, searchN)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        if board.gives_check(move):
            board.push(move)
            searchN += 1
            score = -quiesce(board, -beta, -alpha, searchN)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def evaluate(board):
    eval = 0
    isEndgame = is_endgame(board)
    if board.is_checkmate():
        if board.turn:
            return -10000
        else:
            return 10000
    if board.is_stalemate() or board.is_fivefold_repetition() or board.is_repetition():
        return 0

    if isEndgame:
        for piecetype, value in PIECES_VAL.items():
            for wPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 1):
                eval += value + PIECES_SQUARES_W_ENDGAME[piecetype][wPieceSq]
            for bPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 0):
                eval -= value + PIECES_SQUARES_B_ENDGAME[piecetype][bPieceSq]
    else:
        for piecetype, value in PIECES_VAL.items():
            for wPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 1):
                eval += value + PIECES_SQUARES_W[piecetype][wPieceSq]
            for bPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 0):
                eval -= value + PIECES_SQUARES_B[piecetype][bPieceSq]

    return eval * 1 if board.turn else eval * -1


def sort_moves(board):
    remaining = list(board.legal_moves)
    t = tt.get(board.fen())
    if t:
        best = t[2]
        if best:
            remaining.remove(best)
            yield best

    for move in remaining:
        if (board.is_capture(move) and not board.is_en_passant(move)):
            if (PIECES_VAL[board.piece_at(move.to_square).symbol().lower()] - PIECES_VAL[board.piece_at(move.from_square).symbol().lower()]) > 50:
                remaining.remove(move)
                yield move
                
    for move in remaining:
        if board.gives_check(move) or move.promotion != None:
            remaining.remove(move)
            yield move

    for move in remaining:
        if board.is_attacked_by(not board.turn, move.from_square) and not board.is_attacked_by(board.turn, move.from_square):
            remaining.remove(move)
            yield move

    for move in remaining:
        yield move

times = []

def search(board, depth):
    result = pvs(board, -10000, 10000, depth)
    eval = result[0]
    move = result[1]
    return move, eval

def find_move(board, depth):
    start = time.time()
    if board.ply() < 30:
        response = requests.get(f"https://explorer.lichess.ovh/masters?fen={board.fen()}")
        json = response.json()
        if len(json['moves']) > 1:
            moveUci = (json['moves'][random.randint(0, 1)])['uci']
            move = chess.Move.from_uci(moveUci)
            return move
    move = search(board, depth)[0]


    times.append(time.time() - start)
    print(sum(times) / len(times))
    if len(tt) > max_tt:
        tt.clear()
        print('clearing tt')
    if move == None:
        print('None')
        return list(board.legal_moves)[0]
    return move

def is_endgame(board):
    material = 0
    for piecetype, value in PIECES_VAL.items():
        for wPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 1):
            material += value
        for bPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 0):
            material += value
    if material <= 4800:
        return True
    else:
        return False


def pvs(board, alpha, beta, depthLeft):
    if board.is_checkmate() or board.is_stalemate() or board.is_repetition():
        return -evaluate(board), None
    if depthLeft == 0:
        return -quiesce(board, alpha, beta, 0), None
    t = tt.get(board.fen())
    if t:
        if t[1] >= depthLeft:
            return -t[0], t[2]
    best = None
    for index, move in enumerate(sort_moves(board)):
        board.push(move)
        if index == 0:
            score, _ = pvs(board, -beta, -alpha, depthLeft-1)
        else:
            score = -zws(board, -alpha, depthLeft-1)
            if alpha < score < beta:
                score, _ = pvs(board, -beta, -score, depthLeft-1)
        board.pop()
        if score > alpha:
            alpha = score
            best = move
        if alpha >= beta:
            best = move
            break
    tt[board.fen()] = [alpha, depthLeft, best]
    return -alpha, best

def zws(board, beta, depthLeft):
    if board.is_checkmate() or board.is_stalemate() or board.is_repetition():
        return -evaluate(board)
    if depthLeft == 0:
        return quiesce(board, beta-1, beta, 0)
    for move in sort_moves(board):
        board.push(move)
        score = -zws(board, 1-beta, depthLeft-1)
        board.pop()
        if score >= beta:
            return beta
    return beta-1

if __name__ == '__main__':
    board = chess.Board('rnbqkbnr/pppppppp/8/7Q/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 1')
    start = time.time()
    print(find_move(board, 3))
    print(time.time() - start)
