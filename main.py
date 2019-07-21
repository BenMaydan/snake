# A text based snake game
# MADE BY
# BEN MAYDAN

# Tip: If you are using Windows and are using MINGW64 / Git bash, run this program by typing "winpty python main.py"
# The reason why is because this terminal has a bug with running curses
# Unless you want to mess with python aliases in .bash_profile, this is the best way to go about running this game


# Normal imports
import sys
import time
import traceback

# From imports
from logic import Bash


#Initialization of bash
bash = Bash()
bash.start_curses()


try:
    while True:
        # bash.tick()
        bash.move_snake_fowards()
        # bash.move_snake_backwards()
        # bash.move_snake_right()
        #bash.move_snake_left()
        time.sleep(0.1)
except Exception as e:
    bash.terminate_curses()
    traceback.print_exc()
    sys.exit()
