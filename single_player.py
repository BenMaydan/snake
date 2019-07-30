# A text based snake game
# MADE BY
# BEN MAYDAN

# Tip: If you are using Windows and are using MINGW64 / Git bash, run this program by typing "winpty python single_player.py"
# The reason why is because this terminal has a bug with running curses
# Unless you want to mess with python aliases in .bash_profile, this is the best way to go about running this game


# Normal imports
import argparse
import curses
import sys
import traceback
import time

# From imports
from logic import Bash, score, highscore


# Argument parser if the user wants a custom intensity
parser = argparse.ArgumentParser(description='This is an online snake game')
parser.add_argument('-i', '--intensity', nargs='?', const=True, default=3, help='This is how much the snake grows every time food is eaten', type=int)
args = parser.parse_args()
# If a negative growth is given
if args.intensity <= 0:
    print("Intensity is not allowed to be less than or equal to 0!")
    sys.exit()


# Initialization of bash
bash = Bash(args.intensity, 10, 0.1)
bash.start_curses()

# Creates the snake
bash.create_snake()

# Initial key press
prev_key = curses.KEY_UP
key = curses.KEY_UP

try:
    while True:
        # Captures keys
        key = bash.getch()
        if key != 27:
            bash.capture_keys(key)

            # Acts based off of key pressed
            # Else it will default to keep moving
            bash.tick()
            try:
                time.sleep(bash.sleep)
            except ValueError:
                # This means bash.sleep went negative
                time.sleep(0.03)
        else:
            # print("GAME OVER! YOU BUMPED INTO YOURSELF!")
            # print(score(bash))
            # print(highscore(bash))
            while key == 27:
                # While no other key was pressed after the escape key, the game is paused
                pressed = bash.getch()
                if pressed in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, 27]:
                    key = pressed
                    break

except Exception as e:
    bash.terminate_curses()
    traceback.print_exc()
    sys.exit()
