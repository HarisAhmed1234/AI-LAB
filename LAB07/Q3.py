import random

class Battleship:
    def __init__(self):
        self.ship_lengths = [2, 3, 3, 4, 5]
        self.player_ships_grid, self.player_ships, self.coord_to_player_ship = self.place_ships()
        self.ai_ships_grid, self.ai_ships, self.coord_to_ai_ship = self.place_ships()
        self.player_attack_grid = [['.' for _ in range(10)] for _ in range(10)]
        self.ai_attack_grid = [['.' for _ in range(10)] for _ in range(10)]
        self.active_hits = []

    def place_ships(self):
        grid = [['.' for _ in range(10)] for _ in range(10)]
        ships = []
        coord_to_ship = {}
        for length in self.ship_lengths:
            while True:
                direction = random.choice(['H', 'V'])
                if direction == 'H':
                    r = random.randint(0, 9)
                    c = random.randint(0, 9 - length + 1)
                    if all(grid[r][c + i] == '.' for i in range(length)):
                        ship = [(r, c + i) for i in range(length)]
                        for pos in ship:
                            grid[pos[0]][pos[1]] = 'S'
                            coord_to_ship[pos] = ship
                        ships.append(ship)
                        break
                else:
                    r = random.randint(0, 9 - length + 1)
                    c = random.randint(0, 9)
                    if all(grid[r + i][c] == '.' for i in range(length)):
                        ship = [(r + i, c) for i in range(length)]
                        for pos in ship:
                            grid[pos[0]][pos[1]] = 'S'
                            coord_to_ship[pos] = ship
                        ships.append(ship)
                        break
        return grid, ships, coord_to_ship

    def display_boards(self):
        print("Your grid:")
        self.print_grid(self.player_ships_grid, self.ai_attack_grid)
        print("Opponent's grid:")
        self.print_grid(self.player_attack_grid)

    def print_grid(self, ships_grid, attack_grid=None):
        print('  ', end='')
        for i in range(10):
            print(chr(65 + i), end=' ')
        print()
        for r in range(10):
            print(r, end=' ')
            for c in range(10):
                if attack_grid and attack_grid[r][c] in ['H', 'M']:
                    print(attack_grid[r][c], end=' ')
                else:
                    print(ships_grid[r][c], end=' ')
            print()
        print()

    def parse_guess(self, input_str):
        if len(input_str) < 2:
            return None
        col = input_str[0].upper()
        row = input_str[1:]
        if col < 'A' or col > 'J' or not row.isdigit() or int(row) < 0 or int(row) > 9:
            return None
        c = ord(col) - 65
        r = int(row)
        return r, c

    def player_turn(self):
        while True:
            guess_str = input("Enter your guess (e.g., B4): ")
            guess = self.parse_guess(guess_str)
            if guess is None:
                print("Invalid input. Try again.")
                continue
            r, c = guess
            if self.player_attack_grid[r][c] != '.':
                print("Already attacked here. Pick another spot.")
                continue
            if self.ai_ships_grid[r][c] == 'S':
                self.player_attack_grid[r][c] = 'H'
                print("Hit!")
                ship = self.coord_to_ai_ship[(r, c)]
                if all(self.player_attack_grid[pos[0]][pos[1]] == 'H' for pos in ship):
                    print("You sunk a ship!")
            else:
                self.player_attack_grid[r][c] = 'M'
                print("Miss!")
            break

    def ai_turn(self):
        active_hits = []
        for ship in self.player_ships:
            if not all(self.ai_attack_grid[pos[0]][pos[1]] == 'H' for pos in ship):
                for pos in ship:
                    if self.ai_attack_grid[pos[0]][pos[1]] == 'H':
                        active_hits.append(pos)
        candidates = []
        if active_hits:
            for r, c in active_hits:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 10 and 0 <= nc < 10 and self.ai_attack_grid[nr][nc] == '.':
                        candidates.append((nr, nc))
        if not candidates:
            for r in range(10):
                for c in range(10):
                    if self.ai_attack_grid[r][c] == '.':
                        candidates.append((r, c))
        guess = random.choice(candidates)
        r, c = guess
        if self.player_ships_grid[r][c] == 'S':
            self.ai_attack_grid[r][c] = 'H'
            print(f"AI attacks: {chr(65 + c)}{r} → Hit!")
            ship = self.coord_to_player_ship[(r, c)]
            if all(self.ai_attack_grid[pos[0]][pos[1]] == 'H' for pos in ship):
                print("AI sunk your ship!")
        else:
            self.ai_attack_grid[r][c] = 'M'
            print(f"AI attacks: {chr(65 + c)}{r} → Miss")

    def is_all_ships_sunk(self, ships, attack_grid):
        for ship in ships:
            if not all(attack_grid[pos[0]][pos[1]] == 'H' for pos in ship):
                return False
        return True

    def play(self):
        while True:
            self.display_boards()
            self.player_turn()
            if self.is_all_ships_sunk(self.ai_ships, self.player_attack_grid):
                print("You win!")
                break
            self.ai_turn()
            if self.is_all_ships_sunk(self.player_ships, self.ai_attack_grid):
                print("AI wins!")
                break

if __name__ == "__main__":
    game = Battleship()
    game.play()