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
    if board.is_stalemate() or board.is_repetition():
        return 0
    eval = 0
    isEndgame = is_endgame(board)
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

def quiesce(board, alpha, beta, root):
    if board.is_checkmate():
        return -10000
    eval = evaluate(board)
    if eval >= beta:
        return beta
    if alpha < eval:
        alpha = eval
    for move in sort_moves(board):
        if board.gives_check(move):
            board.push(move)
            score = -quiesce(board, -beta, -alpha, False)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        elif (board.is_capture(move) and not board.is_en_passant(move)):
            if PIECES_VAL[board.piece_at(move.to_square).symbol().lower()] >= PIECES_VAL[board.piece_at(move.from_square).symbol().lower()] or not board.is_attacked_by(not board.turn, move.to_square):
                board.push(move)
                score = -quiesce(board, -beta, -alpha, False)
                board.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
#TA ZKURVENA MRDKA PORAD SERE MATYYYYYY (neidi -m4 4r3/3k4/4r3/8/4q3/8/5PPP/Q1R2K2_b_-_-_0_1 ???)
    return alpha

def sort_moves(board):
    remaining = list(board.legal_moves)

    # if len(board.move_stack) > 0:
    #     lastMove = board.peek()
    #     if board.is_capture(lastMove) and lastMove in remaining:
    #         for move in remaining:
    #             if board.is_capture(move):
    #                 if move.to_square == lastMove.to_square:
    #                     remaining.remove(move)
    #                     yield move

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
    eval, *line = pvs(board, -10000, 10000, depth)
    return line[0], eval, line

def find_move(board, depth):
    start = time.time()
    if board.ply() < 30:
        response = requests.get(f"https://explorer.lichess.ovh/masters?fen={board.fen()}")
        json = response.json()
        if len(json['moves']) > 0:
            moveUci = (json['moves'][0])['uci']
            move = chess.Move.from_uci(moveUci)
            return move
    move, eval, line = search(board, depth)
    print(line)


    times.append(time.time() - start)
    print(sum(times) / len(times))
    if len(tt) > max_tt:
        tt.clear()
        print('clearing tt')
    if move == None:
        print('None')
        return list(board.legal_moves)[0]
    eval = -eval if board.turn else eval
    print(eval)
    return move

# def alpha_beta(board, alpha, beta, depthLeft):
#     best = False
#     if depthLeft == 0:
#         return quiesce(board.copy(), alpha, beta)
#     fen = board.fen()
#     if fen in tp_table and depthLeft > 1:
#         if tp_table[fen][0] >= depthLeft:
#             return -tp_table[fen][1]
#     for move in sort_moves(board):
#         board.push(move)
#         fenAfterPush = board.fen()
#         score = -alpha_beta(board, -beta, -alpha, depthLeft-1)
#         tp_table[fenAfterPush] = [depthLeft, score]
#         board.pop()
#         if score >= beta:
#             tp_moves[fen] = move
#             return beta
#         if score > alpha:
#             best = move
#             alpha = score
#     if best:
#         tp_moves[fen] = best
#     return alpha

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
    if board.is_checkmate():
        return 10000, None, None
    best2 = None
    if depthLeft == 0:
        return quiesce(board, alpha, beta, True), None, None
    t = tt.get(board.fen())
    if t:
        if t[1] >= depthLeft:
            return -t[0], t[2], None
    best = None
    for index, move in enumerate(sort_moves(board)):
        board.push(move)
        if index == 0:
            score, best2, _ = pvs(board, -beta, -alpha, depthLeft-1)
        else:
            score = -zws(board, -alpha, depthLeft-1)
            if score == 10000 or score == -10000:
                print(score)
            if alpha < score < beta:
                score, best2, _ = pvs(board, -beta, -score, depthLeft-1)
        board.pop()
        if score > alpha:
            alpha = score
            best = move
        if alpha >= beta:
            best = move
            break
    tt[board.fen()] = [alpha, depthLeft, best]
    return -alpha, best, best2

def zws(board, beta, depthLeft):
    if board.is_checkmate():
        return -10000
    if depthLeft == 0:
        return quiesce(board, beta-1, beta, True)
    for move in sort_moves(board):
        board.push(move)
        score = -zws(board, 1-beta, depthLeft-1)
        board.pop()
        if score >= beta:
            return beta
    return beta-1

# def pvsA(board, alpha, beta, depthLeft):
#     if depthLeft == 0:
#         return quiesce(board, alpha, beta)
#     legalMoves = list(sort_moves(board))
#     if len(legalMoves) == 0:
#         return evaluate(board)
#     board.push(legalMoves[0])
#     best = -pvsA(board, -beta, -alpha, depthLeft-1)
#     board.pop()
#     if best > alpha:
#         if best >= beta:
#             return best
#         alpha = best
#     legalMoves.remove(legalMoves[0])
#     for move in legalMoves:
#         board.push(move)
#         score = -pvsA(board, -alpha-1, -alpha, depthLeft-1)
#         if score > alpha and score < beta:
#             score = -pvsA(board, -beta, -alpha, depthLeft-1)
#             if score > alpha:
#                 alpha = score
#         board.pop()
#         if score > best:
#             if score >= beta:
#                 best = score
#                 break
#             best = score
    
#     return best

if __name__ == '__main__':
    board = chess.Board('4r3/3k4/4r3/8/4q3/8/5PPP/Q1R2K2 b - - 0 1')
    start = time.time()
    print(find_move(board, 3))
    print(time.time() - start)
