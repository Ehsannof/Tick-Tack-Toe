from asyncio import sleep
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    X_Counter = 0
    O_Counter = 0 
    for row in board:
        for cell in row:
            if cell == "X":
                X_Counter = X_Counter + 1
            elif cell == "O":
                O_Counter = O_Counter + 1
    if X_Counter == O_Counter:
        return X
    else:
        return O

def actions(board):
    if not terminal(board):
        actions = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == None:
                    actions.append([i, j])
        return(actions)
    else:
        raise "Game Ended!"

def result(board, action):
    Player = player(board)
    i, j = action
    board[i][j] = Player
    return board

def winner(board):
    #Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[2] != None:
            return row[0]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[2][j] != None:
            return board[0][j]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[2][2] != None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[2][0] != None:
        return board[0][2]
    
    return None

def terminal(board):
    # check if X or O won
    game_winner = winner(board)
    # check if there is empty room
    if game_winner != None:
        return True
    else:
        for row in board:
            for cell in row:
                if cell == None:
                    return False
    return True

def utility(board):
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return -1
    else:
        return 0

# def minimax(board):
#     AI = player(board)
#     if AI == X:
#         HUMAN = O
#     else:
#         HUMAN = X
#     best_score = float('-inf')
#     best_move = None
#     for action in actions(board):
#         row, col = action
#         board[row][col] = AI
#         score = find_best_move(board, 0, False, AI, HUMAN)
#         board[row][col] = None  # Undo
#         if score > best_score:
#             best_score = score
#             best_move = (row, col)
#     return best_move

# def find_best_move(board, depth, is_maximizing, ai_player, human_player):
#     """
#     Minimax function.
#     - ai_player: the AI's symbol ('O' usually)
#     - human_player: opponent's symbol ('X' usually)
#     Returns the best score for the current position.
#     """
#     # Terminal states
#     if winner(board) == ai_player:
#         return 10 - depth  # AI wins: positive score, prefer quicker wins
#     if winner(board) == human_player:
#         return depth - 10  # Human wins: negative score, delay losses
#     if terminal(board):
#         return 0  # Draw

#     if is_maximizing:  # AI's turn (maximize score)
#         best_score = float('-inf')
#         for row, col in actions(board):
#             board[row][col] = ai_player
#             score = find_best_move(board, depth + 1, False, ai_player, human_player)
#             board[row][col] = None  # Undo move
#             best_score = max(best_score, score)
#         return best_score
#     else:  # Human's turn (minimize score)
#         best_score = float('inf')
#         for row, col in actions(board):
#             board[row][col] = human_player
#             score = find_best_move(board, depth + 1, True, ai_player, human_player)
#             board[row][col] = None  # Undo move
#             best_score = min(best_score, score)
#         return best_score
    
def minimax(board):
    AI = player(board)
    if AI == 'X':
        HUMAN = 'O'
    else:
        HUMAN = 'X'
    best_score = float('-inf')
    best_move = None
    for action in actions(board):
        row, col = action
        board[row][col] = AI
        # Call alpha_beta instead of find_best_move for consistency
        score = alpha_beta(board, 0, False, AI, HUMAN, float('-inf'), float('inf'))
        board[row][col] = None  # Undo
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move

def alpha_beta(board, depth, is_maximizing, ai_player, human_player, alpha, beta):
    """
    Alpha-Beta Pruning Minimax function.
    - ai_player: the AI's symbol ('O' or 'X')
    - human_player: opponent's symbol ('X' or 'O')
    - alpha: best score for maximizer (AI) along the path
    - beta: best score for minimizer (human) along the path
    Returns the best score for the current position.
    """
    # Terminal states
    if winner(board) == ai_player:
        return 10 - depth  # AI wins: positive score, prefer quicker wins
    if winner(board) == human_player:
        return depth - 10  # Human wins: negative score, delay losses
    if terminal(board):
        return 0  # Draw

    if is_maximizing:  # AI's turn (maximize score)
        best_score = float('-inf')
        for row, col in actions(board):
            board[row][col] = ai_player
            score = alpha_beta(board, depth + 1, False, ai_player, human_player, alpha, beta)
            board[row][col] = None  # Undo move
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)  # Update alpha
            if beta <= alpha:  # Prune if beta <= alpha
                break
        return best_score
    else:  # Human's turn (minimize score)
        best_score = float('inf')
        for row, col in actions(board):
            board[row][col] = human_player
            score = alpha_beta(board, depth + 1, True, ai_player, human_player, alpha, beta)
            board[row][col] = None  # Undo move
            best_score = min(best_score, score)
            beta = min(beta, best_score)  # Update beta
            if beta <= alpha:  # Prune if beta <= alpha
                break
        return best_score