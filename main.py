import time, logic, chess, requests, random, traceback, chess.polyglot

PIECES_VAL = {'p': 105, 'n': 322, 'b': 333, 'r': 502, 'q': 925, 'k': 10000}
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
        -5, -4, -1, 5, 5, -1, -4, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, -2, 0, 0, 0, 0, -5,
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

def evaluate(board):
    eval = 0
    isEndgame = is_endgame(board)

    for rowN, row in enumerate(board.pos):
        for colN, squareSymbol in enumerate(row):
            if squareSymbol == '+': continue
            if squareSymbol.isupper():
                eval += PIECES_VAL[squareSymbol.lower()]
                if isEndgame: eval += PIECES_SQUARES_W_ENDGAME[squareSymbol.lower()][rowN*8+colN]
                else: eval += PIECES_SQUARES_W[squareSymbol.lower()][rowN*8+colN]
            else:
                eval -= PIECES_VAL[squareSymbol]
                if isEndgame: eval -= PIECES_SQUARES_B_ENDGAME[squareSymbol][rowN*8+colN]
                else: eval -= PIECES_SQUARES_B[squareSymbol][rowN*8+colN]

    return eval * 1 if board.turn == 1 else eval * -1

def is_endgame(board):
    materialW = 0
    materialB = 0
    for row in board.pos:
        for squareSymbol in row:
            if squareSymbol == '+': continue
            if squareSymbol.isupper():
                materialW += PIECES_VAL[squareSymbol.lower()]
            else:
                materialB += PIECES_VAL[squareSymbol]

    if materialW < 700:
        return True
    if materialB < 700:
        return True
    if materialW + materialB <= 4000:
        return True
    else:
        return False


def amount_of_pieces(pos):
    p = 0
    for row in pos:
        for sq in row:
            if sq != '+': p += 1
    return p


def sort_moves(board):
    remainingMoves = list(board.get_pseudo_legal_moves())
    for move in remainingMoves:
        if board.pos[move.toSquare[0]][move.toSquare[1]] != '+':
            if PIECES_VAL[board.pos[move.fromSquare[0]][move.fromSquare[1]].lower()] - PIECES_VAL[board.pos[move.toSquare[0]][move.toSquare[1]].lower()] < -100:
                remainingMoves.remove(move)
                yield move
        elif move.promotion:
            remainingMoves.remove(move)
            yield move
    for move in remainingMoves:
        yield move

def quiesce(board, alpha, beta):
    if not board.get_king(0) or not board.get_king(1):
        return evaluate(board)
    if board.is_threefold():
        return 0
    eval = evaluate(board)
    if eval >= beta:
        return beta
    if alpha < eval:
        alpha = eval
    for move in sort_moves(board):
        if board.pos[move.toSquare[0]][move.toSquare[1]] == '+': continue
        if not (PIECES_VAL[board.pos[move.fromSquare[0]][move.fromSquare[1]].lower()] - PIECES_VAL[board.pos[move.toSquare[0]][move.toSquare[1]].lower()] < 200) and board.pos[move.fromSquare[0]][move.fromSquare[1]].lower() != 'k':
            continue
        board.move(move)
        score = -quiesce(board, -beta, -alpha)
        board.remove_last()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def pvs(board, alpha, beta, depthLeft):
    #king captured
    if not board.get_king(0) or not board.get_king(1):
        return -evaluate(board), None, 
    #repetition
    if board.is_threefold():
        return 0, None, None
    moves = list(sort_moves(board))
    #stalemate
    if len(moves) == 0:
        return 0, None, None
    best2 = None
    if depthLeft == 0:
        #return evaluate(board), None, None
        return -quiesce(board, alpha, beta), None, None  
        
    best = None
    for index, move in enumerate(moves):
        board.move(move)
        if index == 0:
            score, best2, _ = pvs(board, -beta, -alpha, depthLeft-1)
        else:
            score = -zws(board, -alpha, depthLeft-1)
            if alpha < score < beta:
                score, best2, _ = pvs(board, -beta, -score, depthLeft-1)
        board.remove_last()
        if score > alpha:
            alpha = score
            best = move
        if alpha >= beta:
            best = move
            break
    return -alpha, best, best2

def zws(board, beta, depthLeft):
    if not board.get_king(0) or not board.get_king(1):
        return evaluate(board)
    if board.is_threefold():
        return 0
    moves = list(sort_moves(board))
    #stalemate
    if len(moves) == 0:
        return 0
    if depthLeft == 0:
        #return evaluate(board)
        return quiesce(board, beta-1, beta)
    for move in moves:
        board.move(move)
        score = -zws(board, 1-beta, depthLeft-1)
        board.remove_last()
        if score >= beta:
            return beta
    return beta-1



def find_move(board, timeLeft):
    try:
        with chess.polyglot.open_reader("C:\\Users\\potuz\\Desktop\\Projects\\myChess\\polyglot-collection\\Book.bin") as reader:
            moves = list(reader.find_all(chess.Board(board.get_fen())))
            if len(moves) > 0:
                random.shuffle(moves)
                move = moves[0].move
                move = logic.move_from_pyc(move, chess.Board(board.get_fen()), board)
                print('from opening db')
                return move
    except Exception:
            traceback.print_exc()
    if amount_of_pieces(board.pos) < 7:
        try:
            response = requests.get(
                f"http://tablebase.lichess.ovh/standard?fen={board.get_fen()}")
            json = response.json()
            if len(json['moves']) > 0:
                moveUci = (json['moves'][0])['uci']
                move = chess.Move.from_uci(moveUci)
                move = logic.move_from_pyc(move, chess.Board(board.get_fen()), board)
                print('from endgame db')
                return move
        except Exception:
            traceback.print_exc()
    
    depth = 4 if timeLeft > 10000 else 3
    print(f'Searching for depth {depth}')
    eval, best, best2 = pvs(board, -15000, 15000, depth)
    return best if best else list(board.get_legal_moves())[0]
