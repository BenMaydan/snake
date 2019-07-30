# Online snake text game
# Works globally
# Made by Ben Maydan

import argparse
import curses
import sys
import os
import time
import traceback

# From imports
from logic import highscore
from online_logic import Communicator


# Argument parser for determining whether the user wants to create a game or join one
parser = argparse.ArgumentParser(description='This is an online snake game')
# For create and join flags
group = parser.add_mutually_exclusive_group(required=True)

# Adds keyword arguments. Including create, join, intensity, and name
group.add_argument('-c', '--create', help='This option is if you want to create a game', action='store_true')
group.add_argument('-j', '--join', help='This option is if you want to join a game')
parser.add_argument('-n', '--name', required=True, help='The name of the person who won is printed at the end', type=str)
parser.add_argument('-i', '--intensity', nargs='?', const=True, default=3, help='This is how much the snake grows every time food is eaten', type=int)

# Parses the args
args = parser.parse_args()
print(vars(args))


# Initialization of raspberry pi communicator
communicator = Communicator('https://27bcddaf.ngrok.io', args.intensity)

# Takes action based off of which args were given
if args.create:
    communicator.create_game()
else:
    communicator.join_game(args.join, args.name)
