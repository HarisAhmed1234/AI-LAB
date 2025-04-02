# Lab 05: Map Coloring using Backtracking (CSP)
# Assigns colors to 4 players with adjacent differences
def is_safe(assignment, player, color, constraints):
    for p1, p2 in constraints:
        if p1 == player and p2 in assignment and assignment[p2] == color:
            return False
        if p2 == player and p1 in assignment and assignment[p1] == color:
            return False
    return True

def solve_csp(players, colors, constraints, assignment={}):
    if len(assignment) == len(players):
        return assignment
    unassigned = [p for p in players if p not in assignment]
    current_player = unassigned[0]
    for color in colors:
        if is_safe(assignment, current_player, color, constraints):
            assignment[current_player] = color
            result = solve_csp(players, colors, constraints, assignment)
            if result is not None:
                return result
            del assignment[current_player]
    return None

players = ["P1", "P2", "P3", "P4"]
colors = ["Red", "Yellow", "Green", "Blue"]
constraints = [("P1", "P2"), ("P2", "P3"), ("P3", "P4"), ("P4", "P1")]

solution = solve_csp(players, colors, constraints)
if solution:
    print("Solution found:")
    for player, color in solution.items():
        print(f"{player}: {color}")
else:
    print("No solution found.")
