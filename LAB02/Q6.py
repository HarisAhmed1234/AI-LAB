import time
from typing import Dict

class FirefightingRobot:
    def __init__(self):
        self.grid = {
            'a': ' ', 'b': ' ', 'c': '🔥',
            'd': ' ', 'e': '🔥', 'f': ' ',
            'g': ' ', 'h': ' ', 'j': '🔥'
        }
        self.path = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j']

    def display_grid(self):
        """Display the current state of the grid in a 3x3 format."""
        print("\nCurrent Environment Status:")
        print(f" {self.grid['a']} | {self.grid['b']} | {self.grid['c']} ")
        print("-----------")
        print(f" {self.grid['d']} | {self.grid['e']} | {self.grid['f']} ")
        print("-----------")
        print(f" {self.grid['g']} | {self.grid['h']} | {self.grid['j']} ")
        print("-------------------------")

    def extinguish_fire(self, room: str):
        """Extinguish fire in the specified room."""
        if self.grid[room] == '🔥':
            print(f"🚨 Fire detected in room '{room}'! Extinguishing...")
            time.sleep(1)  # Simulate extinguishing time
            self.grid[room] = '✅'
            print(f"✅ Fire in room '{room}' has been extinguished.")
        else:
            print(f"✅ Room '{room}' is safe. No action needed.")

    def execute_path(self):
        """Move the robot through the predefined path and handle fires."""
        print("🤖 Robot starting at room 'a'.")
        self.display_grid()

        for room in self.path:
            print(f"\n🚶 Robot entering room '{room}'...")
            self.extinguish_fire(room)
            self.display_grid()
            time.sleep(1)  # Simulate movement time

        print("\n🎉 All rooms have been checked. Final environment status:")
        self.display_grid()
        if '🔥' not in self.grid.values():
            print("✅ All fires have been extinguished!")
        else:
            print("❌ Warning: Some fires remain!")

def main():
    robot = FirefightingRobot()
    robot.execute_path()

if __name__ == "__main__":
    main()
