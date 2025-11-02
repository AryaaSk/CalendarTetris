import sys
from calendar_api import init_gui, check_selection_joystick
from tetris import main as tetris_main
from pong import main as pong_main
import time

def main():
    """Main launcher"""
    init_gui(False, "selection")
    while True:
        game = check_selection_joystick()
        if game:
            init_gui(False, game)
            if game == "tetris":
                tetris_main()
            elif game == "pong":
                pong_main()
        time.sleep(1)

if __name__ == "__main__":
    main()

