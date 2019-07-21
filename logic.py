# Snake
# A text based snake game
# Made by BEN MAYDAN
# Copyrighted

# Imports go here
import keyboard

# From imports
from os import system, name
from itertools import cycle


def instances(objects, object_type):
    if type(objects) not in [list, set, tuple]:
        frmt = (str(objects)[0:int(len(objects) / 3)]) + "..."
        raise TypeError("Object {} is not a collection of elements".format(frmt))
    for obj in objects:
        if not isinstance(obj, object_type):
            raise TypeError("Object '{}' is not of type {}".format(str(obj), object_type))


def bool_check(objects, boolean):
    if type(objects) not in [list, set, tuple]:
        frmt = (str(objects)[0:int(len(objects)/3)]) + "..."
        raise TypeError("Object {} is not a collection of elements".format(frmt))
    if not isinstance(boolean, str):
        raise TypeError("Boolean {} is not of type str".format(boolean))

    # Does the boolean check for every object in the collection of objects
    for obj in objects:
        try:
            evaluated = eval(str(obj) + boolean)
            if not evaluated:
                raise BooleanFalseEvalWarning
        except BooleanFalseEvalWarning:
            msg = """Boolean condition {} evaluated to false for object {} of type {} in objects {}""".format(str(obj) + boolean, obj, type(obj), objects)
            raise BooleanFalseEvalWarning(msg)
        else:
            return evaluated


class Bash:
    def __init__(self, height, width):
        instances([height, width], int)
        bool_check([height, width], ' >= 5')
        self.height = height
        self.width = width

        # Access values using simple x and y coordinates
        # Example, snake_list[x][y]
        # It is possible this list is actually indexed by doing snake_list[y][x]
        self.snake_list = [[None for x in range(self.height)] for x in range(self.width)]
        self.x_list = [number for number in range(len(self.snake_list[1]) - 2, 0, -1)]
        self.y_list = [number for number in range(len(self.snake_list) - 2, 0, -1)]
        self.x = self.x_list[int(len(self.x_list) / 2)]
        self.y = self.y_list[int(len(self.y_list) / 2)]

        # These lists are used for increment_x and increment_y
        self.xlist = cycle(self.x_list[self.x:] + self.x_list[0:self.x])
        self.ylist = cycle(self.y_list[self.y:] + self.y_list[0:self.y])

        # This is for the world tick system
        self._tick_value = 0

        # This is used for moving the snake
        self.directions = ['n', 'e', 's', 'w']
        self.direction = self.directions[0]

    def make_border(self):
        # The below for loops fill the lists with the border characters
        # The left and right borders
        self.snake_list[0] = ['_' for x in range(self.height)]
        self.snake_list[-1] = ['_' for x in range(self.height)]

        # The top and bottom columns
        for column in self.snake_list[1:]:
            column[0] = '|'
            column[-1] = '|'

    def make_filler(self):
        """
        Creates the filler for the snake list
        I.E. this method fills in the list with spaces
        So when printed to the screen, the list does not appear condensed unless there is a snake there
        """
        for column in self.snake_list:
            for character in column:
                if character not in ['-', '_', '|']:
                    column[column.index(character)] = ' '

    def make_keybinds(self):
        """
        Will return a dictionary of the keys that are currently being pressed while the program is running
        A key that is being actively pressed will have a value of 1 in the dict
        A key that is not being actively pressed will have a value of 0 in the dict
        :return: A dict with 'W', 'A', 'D', and the arrows and either 0 or 1 depending on if the key is being pressed or not
        """
        # Right arrow = \x1b[C
        # Left arrow = \x1b[D
        keyboard.add_hotkey('a', self.turn_snake_left(), args=tuple())
        keyboard.add_hotkey('d', self.turn_snake_right(), args=tuple())
        keyboard.add_hotkey('t', print, args=("This is a test to see if the keys work", 't'))
        # keyboard.add_hotkey('\x1b[C', self.turn_snake_right(), args=tuple())
        # keyboard.add_hotkey('\x1b[D', self.turn_snake_left(), args=tuple())

    def get_tick(self):
        return self._tick_value

    def increment_tick(self):
        self._tick_value += 1
        return self._tick_value

    def coordinates(self):
        return self.x, self.y

    def increment_x(self):
        """
        Increments the x coordinate of the "X" of the snake by 1
        :return: new self.x coordinate
        """
        self.x = next(self.xlist)
        return self.x

    def increment_y(self):
        """
        Increments the y coordinate of the "X" of the snake by 1
        :return: new self.y coordinate
        """
        self.y = next(self.ylist)
        return self.y

    def tick(self):
        """
        This snake world will operate on ticks like in minecraft
        Every tick the snake will move forward one block
        :return: current tick
        """
        self.increment_tick()
        self.move_snake_fowards()
        return self.get_tick()

    def connecting_body_parts(self, x, y):
        """
        Returns the connecting "o" body parts of the snake
        :param x: x coordinate of the x of the snake
        :param y: y coordinate of the x of the snake
        :return: ((x, y), (x, y), ...) of the connecting o's
        """
        pass

    def move_snake_fowards(self):
        """
        Moves the snake forward one character
        :return: (x, y)
        """
        prev_y = self.y
        self.increment_y()
        self.snake_list[self.y][self.x] = 'X'
        self.snake_list[prev_y][self.x] = ' '
        self.draw()

    def turn_snake_right(self):
        """
        Turns the snake to the right and updates the tick
        :return: (x, y)
        """
        self.draw()

    def turn_snake_left(self):
        """
        Turns the snake to the left and updates the tick
        :return:
        """
        self.draw()

    def set_snake(self):
        """
        Resets x and y coordinates of the snake to the middle of the snake list
        Also calls the update function to redraw the snake list in the bash
        :return: (x, y)
        """
        self.snake_list[self.y][self.x] = 'X'

    def clear(self):
        """
        Clears the terminal
        :return: None
        """
        # for windows
        if name == 'nt':
            _ = system('cls')

        # for mac and linux (os name is 'posix')
        else:
            _ = system('clear')

    def draw(self):
        """
        'Draws' the text based snake list on the screen
        :return: printable string
        """
        new_string = ''
        for column in self.snake_list:
            for char in column:
                new_string += char
            new_string += '\n'

        # Clears the terminal before drawing the string
        self.clear()
        print(new_string)


class BooleanFalseEvalWarning(Exception):
    def __init___(self):
        pass