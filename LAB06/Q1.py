import heapq
import copy

class ChessState:
    def __init__(self, board, moves=[], evaluation=None):
        self.board = board
        self.moves = moves  
        self.evaluation = evaluation if evaluation is not None else self.evaluate_board(board)

    def generate_moves(self):
        moves = []
        directions = {
            'P': [(-1, 0), (-2, 0)],  
            'N': [(-2, -1), (-1, -2), (1, -2), (2, -1), 
                 (2, 1), (1, 2), (-1, 2), (-2, 1)],
            'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            'R': [(-1, 0), (1, 0), (0, -1), (0, 1)],
            'Q': [(-1, -1), (-1, 1), (1, -1), (1, 1),
                 (-1, 0), (1, 0), (0, -1), (0, 1)],
            'K': [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1), (0, 1),
                 (1, -1), (1, 0), (1, 1)]
        }
        
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if not piece.isupper():  
                    continue

                if piece == 'P':
                    if i > 0 and self.board[i-1][j] == '.':
                        self.add_pawn_move(i, j, i-1, j, moves)
                        if i == 6 and self.board[i-2][j] == '.':
                            self.add_pawn_move(i, j, i-2, j, moves)
                    for dj in [-1, 1]:
                        if 0 <= j+dj < 8 and i > 0 and self.board[i-1][j+dj].islower():
                            self.add_pawn_move(i, j, i-1, j+dj, moves)
                    continue

                for dx, dy in directions.get(piece, []):
                    max_steps = 1 if piece in ['N', 'K'] else 7
                    for step in range(1, max_steps+1):
                        x = i + dx * step
                        y = j + dy * step
                        if not (0 <= x < 8 and 0 <= y < 8):
                            break
                        
                        target = self.board[x][y]
                        if target == '.':
                            self.add_move(i, j, x, y, piece, moves)
                        elif target.islower():
                            self.add_move(i, j, x, y, piece, moves)
                            break  
                        else:
                            break  
                        if piece in ['N', 'K']:  
                            break
        return moves

    def add_move(self, i, j, x, y, piece, moves):
        new_board = copy.deepcopy(self.board)
        new_board[i][j] = '.'
        new_board[x][y] = piece
        new_moves = self.moves + [(piece, (i, j), (x, y))]
        moves.append(ChessState(new_board, new_moves))

    def add_pawn_move(self, i, j, x, y, moves):
        new_board = copy.deepcopy(self.board)
        new_board[i][j] = '.'
        new_board[x][y] = 'Q' if x == 0 else 'P'
        new_moves = self.moves + [(self.board[i][j], (i, j), (x, y))]
        moves.append(ChessState(new_board, new_moves))

    def evaluate_board(self, board):
        piece_values = {
            'P': 1, 'N': 3, 'B': 3.2, 'R': 5, 'Q': 9, 'K': 100,
            'p': -1, 'n': -3, 'b': -3.2, 'r': -5, 'q': -9, 'k': -100
        }
        
        positional_bonus = {
            'P': [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                [0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1],
                [0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05],
                [0, 0, 0, 0.2, 0.2, 0, 0, 0],
                [0.05, -0.05, -0.1, 0, 0, -0.1, -0.05, 0.05],
                [0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            'N': [
                [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5],
                [-0.4, -0.2, 0, 0, 0, 0, -0.2, -0.4],
                [-0.3, 0, 0.1, 0.15, 0.15, 0.1, 0, -0.3],
                [-0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05, -0.3],
                [-0.3, 0, 0.15, 0.2, 0.2, 0.15, 0, -0.3],
                [-0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05, -0.3],
                [-0.4, -0.2, 0, 0.05, 0.05, 0, -0.2, -0.4],
                [-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
            ]
        }
        
        score = 0
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece == '.':
                    continue
                
                score += piece_values.get(piece, 0)
                
                if piece.upper() in positional_bonus:
                    table = positional_bonus[piece.upper()]
                    multiplier = 1 if piece.isupper() else -1
                    score += table[i if piece.isupper() else 7-i][j] * multiplier
                    
        return round(score, 2)  

    def __lt__(self, other):
        return self.evaluation > other.evaluation  

def beam_search(start_state, beam_width, depth_limit):
    beam = [(start_state.evaluation, start_state)]
    
    for _ in range(depth_limit):
        candidates = []
        for _, state in beam:
            candidates.extend((move.evaluation, move) for move in state.generate_moves())
        
        if not candidates:
            break
            
        beam = heapq.nlargest(beam_width, candidates, key=lambda x: x[0])
    
    best_state = max(beam, key=lambda x: x[0])[1] if beam else start_state
    return best_state.moves, best_state.evaluation

initial_board = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
]

start_state = ChessState(initial_board)
best_moves, best_score = beam_search(start_state, beam_width=3, depth_limit=2)

print("Best Move Sequence:")
for move in best_moves:
    print(f"{move[0]} from {move[1]} to {move[2]}")
print(f"\nEvaluation Score: {best_score}")