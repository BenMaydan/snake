# Normal imports
import sys
import time

# From imports
from logic import Bash



bash = Bash(100, 40)
bash.make_border()
bash.make_filler()
bash.make_keybinds()
bash.set_snake()


try:
    while True:
        bash.tick()
        bash.draw()
        time.sleep(0.3)
except KeyboardInterrupt:
    sys.exit()
