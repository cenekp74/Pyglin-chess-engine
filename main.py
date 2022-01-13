import chess
import time
import requests

PIECES_VAL = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 0}
PIECES_SQUARES_W = {
    'p': [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 9, -23, -23, 9, 10,  5,
        8, -5, -10,  0,  0, -10, -5,  8,
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
        -5, -5, 0, 5, 5, -1, -5, -5,
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
        15, 40, 5, 0, 0, 30, 35, 15,
        8, 10, -10, -10, -10, -10, 10, 8,
        -15, -25, -30, -30, -30, -30, -25, -15,
        20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30
    ]
}

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
        -25, -25, -25, -25, -25, -25, -25,  -25,
        -15, -15, -15,  -15,  -15, -15, -15,  15,
        -5, -5,  -5, -5, -5,  -5,  -5,  -5,
        30,  30, 30, 30, 30, 30,  30,  30,
        50, 50, 50, 50, 50, 50, 50, 50,
        70, 70, 70, 70, 70, 70, 70, 70,
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

max_tt = 1e5

tt = {}

def evaluate(board):
    eval = 0
    isEndgame = is_endgame(board)
    outcome = board.outcome()
    if outcome != None:
        if outcome.termination == chess.Termination.CHECKMATE:
            return 10000 if outcome.winner else -10000
    if board.is_stalemate() or board.is_repetition():
        return 0
    pawnsW = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    pawnsB = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    whiteKingSq = board.king(chess.WHITE)
    blackKingSq = board.king(chess.BLACK)
    if isEndgame:
        for piecetype, value in PIECES_VAL.items():
            for wPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 1):
                eval += value + PIECES_SQUARES_W_ENDGAME[piecetype][wPieceSq]
                if piecetype == 'p':
                    file = chess.square_file(wPieceSq)
                    pawnsW[file] += 1
                    if pawnsW[file] > 1:
                        eval -= 22
                    if chess.square_distance(wPieceSq, whiteKingSq) <= 2:
                        eval += 7
            for bPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 0):
                eval -= value + PIECES_SQUARES_B_ENDGAME[piecetype][bPieceSq]
                if piecetype == 'p':
                    file = chess.square_file(bPieceSq)
                    pawnsB[file] += 1
                    if pawnsB[file] > 1:
                        eval += 22
                    if chess.square_distance(bPieceSq, blackKingSq) <= 2:
                        eval -= 7
    else:
        for piecetype, value in PIECES_VAL.items():
            for wPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 1):
                eval += value + PIECES_SQUARES_W[piecetype][wPieceSq]
                if piecetype == 'p':
                    file = chess.square_file(wPieceSq)
                    pawnsW[file] += 1
                    if pawnsW[file] > 1:
                        eval -= 22
                    if chess.square_distance(wPieceSq, whiteKingSq) <= 2:
                        eval += 7
            for bPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 0):
                eval -= value + PIECES_SQUARES_B[piecetype][bPieceSq]
                if piecetype == 'p':
                    file = chess.square_file(bPieceSq)
                    pawnsB[file] += 1
                    if pawnsB[file] > 1:
                        eval += 22
                    if chess.square_distance(bPieceSq, blackKingSq) <= 2:
                        eval -= 7

    return eval * 1 if board.turn else eval * -1

def quiesce(board, alpha, beta, searchN):
    eval = evaluate(board)
    if eval >= beta:
        return beta
    if alpha < eval:
        alpha = eval
    for move in sort_moves(board):
        if (board.is_capture(move) and not board.is_en_passant(move)):
            if PIECES_VAL[board.piece_at(move.to_square).symbol().lower()] >= PIECES_VAL[board.piece_at(move.from_square).symbol().lower()] or not board.is_attacked_by(not board.turn, move.to_square):
                board.push(move)
                searchN += 1
                score = -quiesce(board, -beta, -alpha, searchN)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
            elif board.gives_check(move):
                board.push(move)
                searchN += 1
                score = -quiesce(board, -beta, -alpha, searchN)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        elif board.gives_check(move):
            board.push(move)
            searchN += 1
            score = -quiesce(board, -beta, -alpha, searchN)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

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
color = {'self':None}

def search(board, depth):
    result = pvs(board, -10000, 10000, depth)
    eval = result[0]
    move = result[1]
    return move, eval

def find_move(board, depth):
    start = time.time()
    color['self'] = not board.turn
    if board.ply() < 30:
        response = requests.get(f"https://explorer.lichess.ovh/masters?fen={board.fen()}")
        json = response.json()
        if len(json['moves']) > 0:
            moveUci = (json['moves'][0])['uci']
            move = chess.Move.from_uci(moveUci)
            return move
    move, eval = search(board, depth)


    times.append(time.time() - start)
    print(sum(times) / len(times))
    if len(tt) > max_tt:
        tt.clear()
        print('clearing tt')
    if move == None:
        print('None')
        return list(board.legal_moves)[0]
    print(eval)
    return move

def is_endgame(board):
    material = 0
    for piecetype, value in PIECES_VAL.items():
        for wPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 1):
            material += value
            if piecetype == 'q':
                material += 100
        for bPieceSq in board.pieces(chess.PIECE_SYMBOLS.index(piecetype), 0):
            material += value
            if piecetype == 'q':
                material += 100
    if material <= 4000:
        return True
    else:
        return False


def pvs(board, alpha, beta, depthLeft):
    if board.is_game_over():
        return evaluate(board), None
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
    if board.is_game_over():
        return evaluate(board)
    if depthLeft == 0:
        return quiesce(board, beta-1, beta, 0)
    for move in sort_moves(board):
        board.push(move)
        score = -zws(board, 1-beta, depthLeft-1)
        board.pop()
        if score >= beta:
            return beta
    return beta-1
