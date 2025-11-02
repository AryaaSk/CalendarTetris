import random
import threading
import sys
import os
import time
from calendar_api import update_grid, init_gui, check_joystick_pong, init_joystick_pong
import calendar_api

previous_grid = []

def GetChar():
    """Gets a single character from stdin without Enter"""
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getch()
        if isinstance(ch, bytes):
            ch = ch.decode('utf-8', errors='ignore')
        return ch
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class Pong:
    """Main Pong game class"""
    
    def __init__(self, width=10, height=24):
        self.width = width
        self.height = height
        self.board = [['.' for _ in range(width)] for _ in range(height)]
        
        # Paddle settings
        self.paddle_length = 3
        self.paddle1_x = width // 2 - self.paddle_length // 2  # Top paddle (Player 1)
        self.paddle2_x = width // 2 - self.paddle_length // 2  # Bottom paddle (Player 2)
        self.paddle1_y = 1  # Top row
        self.paddle2_y = height - 2  # Bottom row
        
        # Ball settings
        self.ball_x = width // 2
        self.ball_y = height // 2
        self.ball_dx = random.choice([-1, 1])  # Horizontal direction
        self.ball_dy = random.choice([-1, 1])  # Vertical direction
        
        # Game state
        self.score1 = 0  # Player 1 (top)
        self.score2 = 0  # Player 2 (bottom)
        self.gameOver = False
        self.gameSpeed = 0.1  # Time between frames in seconds
        
    def MovePaddle1(self, direction):
        """Move Player 1's paddle (top) left (-1) or right (1)"""
        if self.gameOver:
            return
        
        new_x = self.paddle1_x + direction
        
        # Check boundaries
        if new_x >= 0 and new_x + self.paddle_length <= self.width:
            self.paddle1_x = new_x
    
    def MovePaddle2(self, direction):
        """Move Player 2's paddle (bottom) left (-1) or right (1)"""
        if self.gameOver:
            return
        
        new_x = self.paddle2_x + direction
        
        # Check boundaries
        if new_x >= 0 and new_x + self.paddle_length <= self.width:
            self.paddle2_x = new_x
    
    def UpdateBall(self):
        """Updates ball position and handles collisions"""
        if self.gameOver:
            return
        
        # Move ball
        new_x = self.ball_x + self.ball_dx
        new_y = self.ball_y + self.ball_dy
        
        # Check for paddle collisions before boundary checks
        # Check if ball will hit paddle1 (top paddle)
        if new_y == self.paddle1_y and self.ball_dy < 0:  # Moving up toward paddle1
            if self.paddle1_x <= new_x < self.paddle1_x + self.paddle_length:
                self.ball_dy = -self.ball_dy  # Bounce back down
                # Add some randomness occasionally
                if random.random() < 0.2:
                    self.ball_dx = random.choice([-1, 1])
                new_y = self.ball_y  # Don't move into paddle
            # Check if ball will hit paddle2 (bottom paddle)
        elif new_y == self.paddle2_y and self.ball_dy > 0:  # Moving down toward paddle2
            if self.paddle2_x <= new_x < self.paddle2_x + self.paddle_length:
                self.ball_dy = -self.ball_dy  # Bounce back up
                # Add some randomness occasionally
                if random.random() < 0.2:
                    self.ball_dx = random.choice([-1, 1])
                new_y = self.ball_y  # Don't move into paddle
        
        # Check horizontal boundaries (walls)
        if new_x < 0 or new_x >= self.width:
            self.ball_dx = -self.ball_dx
            new_x = self.ball_x  # Keep ball at current position this frame
        
        # Check vertical boundaries (scoring)
        if new_y < 0:
            # Ball went past top - Player 2 scores
            self.score2 += 1
            self.ResetBall()
            return
        elif new_y >= self.height:
            # Ball went past bottom - Player 1 scores
            self.score1 += 1
            self.ResetBall()
            return
        
        # Update ball position
        self.ball_x = new_x
        self.ball_y = new_y
    
    def ResetBall(self):
        """Resets the ball to the center after a point"""
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        time.sleep(0.5)  # Brief pause before resuming
    
    def Tick(self):
        """Main game tick - updates ball position"""
        if self.gameOver:
            return
        
        self.UpdateBall()
        
        # Check win condition (first to 5 points, for example)
        if self.score1 >= 5 or self.score2 >= 5:
            self.gameOver = True
    
    def Render(self):
        """Renders the current game state"""
        global previous_grid
        # Clear the board
        render_board = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw paddle 1 (top, Player 1) - using 'B' for Blue
        for i in range(self.paddle_length):
            if 0 <= self.paddle1_x + i < self.width:
                render_board[self.paddle1_y][self.paddle1_x + i] = 'B'
        
        # Draw paddle 2 (bottom, Player 2) - using 'R' for Red
        for i in range(self.paddle_length):
            if 0 <= self.paddle2_x + i < self.width:
                render_board[self.paddle2_y][self.paddle2_x + i] = 'R'
        
        # Draw ball - using 'Y' for Yellow
        if 0 <= self.ball_y < self.height and 0 <= self.ball_x < self.width:
            render_board[self.ball_y][self.ball_x] = 'Y'
        
        # Draw scores on the sides (using small indicators)
        # Score indicators: use colored dots to show score
        # Left side for Player 1, Right side for Player 2
        if self.score1 > 0:
            for i in range(min(self.score1, 5)):
                if i < self.height and 0 < self.width:
                    render_board[i][0] = 'C'  # Cyan for Player 1 score
        
        if self.score2 > 0:
            for i in range(min(self.score2, 5)):
                if self.height - 1 - i >= 0 and self.width - 1 >= 0:
                    render_board[self.height - 1 - i][self.width - 1] = 'M'  # Magenta for Player 2 score
        
        # Update the grid
        if previous_grid != []:
            update_grid(previous_grid, calendar_api.event_ids, render_board)
        previous_grid = render_board
    
    def game_loop(self):
        """Main game loop"""
        while not self.gameOver:
            joystick_input = check_joystick_pong()
            print(joystick_input)
            if joystick_input == 1:
                init_joystick_pong(1)
                self.MovePaddle1(-1)
            elif joystick_input == 2:
                init_joystick_pong(1)
                self.MovePaddle1(1)
            elif joystick_input == 3:
                init_joystick_pong(2)
                self.MovePaddle2(-1)
            elif joystick_input == 4:
                init_joystick_pong(2)
                self.MovePaddle2(1)
            self.Tick()
            self.Render()
            time.sleep(self.gameSpeed)
        
        # Game over screen
        self.EndScreen()
    
    def EndScreen(self):
        """Displays game over screen"""
        winner = "Player 1" if self.score1 >= 5 else "Player 2"
        
        # Clear board and show winner
        for y in range(self.height):
            self.board[y] = ["."] * self.width
        
        # Simple "WIN" text for winner
        if self.score1 >= 5:
            # Player 1 wins - show "P1" pattern
            for y in range(10, 14):
                if y < self.height:
                    self.board[y] = ["."] * self.width
            if 11 < self.height:
                self.board[11][3:5] = ['B', 'B']  # P1
        else:
            # Player 2 wins - show "P2" pattern
            for y in range(10, 14):
                if y < self.height:
                    self.board[y] = ["."] * self.width
            if 11 < self.height:
                self.board[11][3:5] = ['R', 'R']  # P2
        
        self.Render()
        time.sleep(3)
        
        # Clear the grid
        update_grid(previous_grid, calendar_api.event_ids, [['.'] * 10 for _ in range(24)])
    
    def input_loop(self):
        """Handles user input in a separate thread"""
        print("Pong Game Started!")
        print("Controls:")
        print("  Player 1 (Top): 'a' = left, 'd' = right")
        print("  Player 2 (Bottom): 'j' = left, 'l' = right")
        print("  'q' = quit")
        print("\nFirst to 5 points wins!\n")
        
        while not self.gameOver:
            try:
                move = GetChar().lower()
                
                if move == 'q':
                    print("\nQuitting game...")
                    self.gameOver = True
                    update_grid(previous_grid, calendar_api.event_ids, [['.'] * 10 for _ in range(24)])
                    break
                elif move == 'a':
                    self.MovePaddle1(-1)
                elif move == 'd':
                    self.MovePaddle1(1)
                elif move == 'j':
                    self.MovePaddle2(-1)
                elif move == 'l':
                    self.MovePaddle2(1)
            except Exception as e:
                print(f"Input error: {e}")
                break


def main():
    """Main game loop"""
    # Initialize the GUI/calendar
    init_gui(False, "pong")
    
    game = Pong()

    # Start input thread (daemon)
    input_thread = threading.Thread(target=game.input_loop, daemon=True)
    input_thread.start()
    
    # Main thread runs the game loop
    game.game_loop()


if __name__ == "__main__":
    main()

