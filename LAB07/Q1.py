import copy
import math

class Checkers:
    def __init__(self):
        self.board = [
            ['.', 'B', '.', 'B', '.', 'B', '.', 'B'],
            ['B', '.', 'B', '.', 'B', '.', 'B', '.'],
            ['.', 'B', '.', 'B', '.', 'B', '.', 'B'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['W', '.', 'W', '.', 'W', '.', 'W', '.'],
            ['.', 'W', '.', 'W', '.', 'W', '.', 'W'],
            ['W', '.', 'W', '.', 'W', '.', 'W', '.']
        ]
        self.current_player = 'W'

    def print_board(self):
        print('  ', end='')
        for i in range(8):
            print(i, end=' ')
        print()
        for r in range(8):
            print(r, end=' ')
            for c in range(8):
                print(self.board[r][c], end=' ')
            print()
        print()

    def get_legal_moves(self, player):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c].upper() == player.upper():
                    directions = [(-1, -1), (-1, 1)] if player == 'W' else [(1, -1), (1, 1)]
                    if self.board[r][c].isupper():
                        directions.extend([(1, -1), (1, 1)] if player == 'W' else [(-1, -1), (-1, 1)])
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] == '.':
                            moves.append((r, c, nr, nc))
                        elif (0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc].upper() != player.upper() and
                              0 <= nr + dr < 8 and 0 <= nc + dc < 8 and self.board[nr + dr][nc + dc] == '.'):
                            moves.append((r, c, nr + dr, nc + dc))
        return moves

    def make_move(self, move):
        r, c, nr, nc = move
        self.board[nr][nc] = self.board[r][c]
        self.board[r][c] = '.'
        if abs(nr - r) == 2:
            mr, mc = (r + nr) // 2, (c + nc) // 2
            self.board[mr][mc] = '.'
        if nr == 0 and self.board[nr][nc] == 'W':
            self.board[nr][nc] = 'WK'
        elif nr == 7 and self.board[nr][nc] == 'B':
            self.board[nr][nc] = 'BK'

    def evaluate(self):
        score = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 'W':
                    score -= 1
                elif self.board[r][c] == 'B':
                    score += 1
                elif self.board[r][c] == 'WK':
                    score -= 2
                elif self.board[r][c] == 'BK':
                    score += 2
        return score

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0 or not self.get_legal_moves('B' if maximizing else 'W'):
            return self.evaluate()
        if maximizing:
            max_eval = -math.inf
            for move in self.get_legal_moves('B'):
                new_board = copy.deepcopy(self)
                new_board.make_move(move)
                eval = new_board.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_legal_moves('W'):
                new_board = copy.deepcopy(self)
                new_board.make_move(move)
                eval = new_board.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def ai_move(self, depth=3):
        best_move = None
        best_value = -math.inf
        for move in self.get_legal_moves('B'):
            new_board = copy.deepcopy(self)
            new_board.make_move(move)
            move_value = new_board.minimax(depth - 1, -math.inf, math.inf, False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move

    def play(self):
        while True:
            self.print_board()
            if self.current_player == 'W':
                while True:
                    move_input = input("Enter move (e.g., '2,3 to 3,4') or 'quit' to exit: ")
                    if move_input.lower() == 'quit':
                        print("Game quit by player.")
                        return
                    try:
                        r, c, nr, nc = map(int, move_input.replace(' to ', ',').split(','))
                        move = (r, c, nr, nc)
                        if move in self.get_legal_moves('W'):
                            self.make_move(move)
                            self.current_player = 'B'
                            break
                        else:
                            print("Invalid move. Please enter a legal move or 'quit'.")
                    except (ValueError, IndexError):
                        print("Invalid input. Use format 'row,col to new_row,new_col' or 'quit'.")
            else:
                move = self.ai_move()
                if move:
                    self.make_move(move)
                    print(f"AI moves: ({move[0]},{move[1]}) → ({move[2]},{move[3]})")
                    self.current_player = 'W'
                else:
                    print("AI has no moves left.")
                    print("Player wins!")
                    break
            if not self.get_legal_moves('W'):
                print("AI wins!")
                break
            elif not self.get_legal_moves('B'):
                print("Player wins!")
                break

if __name__ == "__main__":
    game = Checkers()
    game.play()