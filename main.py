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
