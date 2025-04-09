# Group 21
'''
ANUJ RAMDAS BALIGA - 2022A4PS1730H
KOTHAMASU SAI ADITHYA - 2022A7PS0076H
HARISANKAR VISHNU SUDHAN - 2022A7PS1317H
PARTH GAUTAM - 2022A8PS0736H
'''

import random
import math
from copy import deepcopy

def group2(self, board):
    possible_moves = self.getPossibleMoves(board)
    if not possible_moves:
        self.game.end_turn()
        return

    best_move = None
    best_choice = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in possible_moves:
        for choice in move[2]:
            new_board = deepcopy(board)
            self.moveOnBoard(new_board, (move[0], move[1]), choice)
            score = minimax(self, new_board, depth=self.depth - 1, alpha=alpha, beta=beta, is_maximizing_player=False)
            if score > best_score:
                best_score = score
                best_move = (move[0], move[1])
                best_choice = choice
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

    if best_move is not None and best_choice is not None:
        return (best_move[0], best_move[1], [best_choice]), best_choice
    else:
        # If no best move was found, pick a random move
        random_move = random.choice(possible_moves)
        random_choice = random.choice(random_move[2])
        return random_move, random_choice

def minimax(self, board, depth, alpha, beta, is_maximizing_player):
    """
    Minimax algorithm with alpha-beta pruning.
    """
    if depth == 0 or isGameOver(self, board):
        return evaluate_board(self, board)

    if is_maximizing_player:
        max_eval = float('-inf')
        moves = self.getPossibleMoves(board)
        for move in moves:
            for choice in move[2]:
                new_board = deepcopy(board)
                self.moveOnBoard(new_board, (move[0], move[1]), choice)
                eval = minimax(self, new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        self.eval_color = self.opponent_color  # Switch to opponent's perspective
        moves = self.getPossibleMoves(board)
        for move in moves:
            for choice in move[2]:
                new_board = deepcopy(board)
                self.moveOnBoard(new_board, (move[0], move[1]), choice)
                eval = minimax(self, new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
        self.eval_color = self.color  # Reset to bot's color
        return min_eval

def isGameOver(self, board):
    """
    Checks if the game is over.
    """
    player_pieces, opponent_pieces = self.allPiecesLocation(board)

    # Game over if either player has no pieces left
    if len(player_pieces) == 0 or len(opponent_pieces) == 0:
        return True

    # Game over if current player has no valid moves
    if len(self.getPossibleMoves(board)) == 0:
        return True

    return False

def evaluate_board(self, board):
    """
    Evaluates the board state and returns a numerical score.
    """
    score = 0

    # Piece values
    piece_value = 5
    king_value = 10

    # Positional weights
    position_weights = [
        [0, 4, 0, 4, 0, 4, 0, 4],
        [4, 0, 3, 0, 3, 0, 3, 0],
        [0, 3, 0, 2, 0, 2, 0, 4],
        [4, 0, 2, 0, 1, 0, 3, 0],
        [0, 3, 0, 1, 0, 2, 0, 4],
        [4, 0, 2, 0, 2, 0, 3, 0],
        [0, 3, 0, 3, 0, 3, 0, 4],
        [4, 0, 4, 0, 4, 0, 4, 0]
    ]

    # Get all possible moves for both players
    player_moves = len(self.getPossibleMoves(board))
    self.eval_color = self.opponent_color
    opponent_moves = len(self.getPossibleMoves(board))
    self.eval_color = self.color  # Reset to bot's color

    # Evaluate each piece on the board
    for i in range(8):
        for j in range(8):
            square = board.getSquare(i, j)
            squarePiece = square.squarePiece
            if squarePiece is not None:
                piece_score = 0
                # Assign base value based on piece type
                if squarePiece.king:
                    piece_score += king_value
                else:
                    piece_score += piece_value

                # Add positional advantage
                piece_score += position_weights[j][i]

                # Add promotion potential for non-king pieces
                if not squarePiece.king:
                    if squarePiece.color == self.color:
                        piece_score += (7 - j) if self.color == self.color else j
                    else:
                        piece_score += j if squarePiece.color == self.opponent_color else (7 - j)

                # Adjust score based on piece ownership
                if squarePiece.color == self.color:
                    score += piece_score
                else:
                    score -= piece_score

    # Add mobility to the score
    score += player_moves * 0.1
    score -= opponent_moves * 0.1

    return score
