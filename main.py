# A text based snake game
# MADE BY
# BEN MAYDAN

# Tip: If you are using Windows and are using MINGW64 / Git bash, run this program by typing "winpty python main.py"
# The reason why is because this terminal has a bug with running curses
# Unless you want to mess with python aliases in .bash_profile, this is the best way to go about running this game


# Normal imports
import curses
import sys
import time
import traceback

# From imports
from logic import Bash


# Initialization of bash
bash = Bash(10)
bash.start_curses()

# Mandatory two refreshes
bash.refresh()
bash.refresh()

# Creates the snake
bash.create_snake()

try:
    while True:
        # Captures keys
        bash.capture_keys(bash.getch())

        # Acts based off of keys
        bash.tick()
        time.sleep(0.1)

        # # print("Pressed key:", bash.getch())
        # # Performs commands based on which is key is being pressed
        # for x in range(25):
        #     result = bash.getch()
        #     bash.capture_keys(result)
        #     if result > 0:
        #         bash.tick()
        #     time.sleep(0.01)
        #     #bash.grow_snake()

except Exception as e:
    bash.terminate_curses()
    traceback.print_exc()
    sys.exit()

# This finally is for printing debugging statements
# Because they don't show up while the program is running
# finally:
#     print("Right arrow key:", curses.KEY_RIGHT)
