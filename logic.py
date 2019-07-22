# Snake
# A text based snake game
# Made by BEN MAYDAN
# Copyrighted

# Imports go here
import keyboard
import curses
import sys


def instances(objects, object_type):
    if type(objects) not in [list, set, tuple]:
        frmt = (str(objects)[0:int(len(objects) / 3)]) + "..."
        raise TypeError("Object {} is not a collection of elements".format(frmt))
    for obj in objects:
        if not isinstance(obj, object_type):
            raise TypeError("Object '{}' is not of type {}".format(str(obj), object_type))


def bool_check(objects, boolean):
    if type(objects) not in [list, set, tuple]:
        frmt = (str(objects)[0:int(len(objects) / 3)]) + "..."
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
            msg = """Boolean condition {} evaluated to false for object {} of type {} in objects {}""".format(
                str(obj) + boolean, obj, type(obj), objects)
            raise BooleanFalseEvalWarning(msg)
        else:
            return evaluated


class cycle:
    def __init__(self, c):
        self._c = c
        self._index = -1

    def values(self):
        return self._c

    def next(self):
        self._index += 1
        if self._index >= len(self._c):
            self._index = 0
        return self._c[self._index]

    def previous(self):
        self._index -= 1
        if self._index < 0:
            self._index = len(self._c) - 1
        return self._c[self._index]


class Snake:
    def __init__(self, y, x):
        if y > curses.LINES:
            raise ValueError("Y coordinate '{}' of snake cannot be greater than than the max y coordinate of the screen, '{}'".format(y, curses.LINES))
        elif y < 0:
            raise ValueError("Y coordinate '{}' of snake cannot be less than than the min y coordinate of the screen, '0'".format(y))
        if x > curses.COLS:
            raise ValueError("X coordinate '{}' of snake cannot be greater than than the max x coordinate of the screen, '{}'".format(x, curses.COLS))
        elif x < 0:
            raise ValueError("X coordinate '{}' of snake cannot be less than than the min x coordinate of the screen, '0'".format(x))
        else:
            self.y = y
            self.x = x

    def increment_x(self, bash):
        """
        Increments the x value and checks for collision with the border of the terminal and the snake's own body parts
        :param bash: bash instance
        :return: new x coordinate
        """
        # Before mutating self.x, this xcheck is a third party variable used to check collision
        xcheck = self.x + 1

        # Checks for a collision with the snake's own body
        for piece in bash.snake:
            if self.y == piece.y and self.x == piece.y:
                bash.terminate_curses()
                print("GAME OVER! YOU BUMPED INTO THE BORDER!")
                sys.exit()

        # Checks for a collision with the border of the terminal
        if xcheck == curses.COLS:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            sys.exit()
        # No collision with the border of the terminal
        else:
            self.x += 1
            return self.x

    def decrement_x(self, bash):
        """
        Decrements the x value and checks for collision with the border of the terminal and the snake's own body parts
        :param bash: bash instance
        :return: new x coordinate
        """
        # Before mutating self.x, this xcheck is a third party variable used to check collision
        xcheck = self.x - 1

        # Checks for a collision with the snake's own body
        for piece in bash.snake:
            if self.y == piece.y and self.x == piece.y:
                bash.terminate_curses()
                print("GAME OVER! YOU BUMPED INTO THE BORDER!")
                sys.exit()

        # Checks for a collision with the border of the terminal
        if xcheck < 0:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            sys.exit()
        # No collision with the border of the terminal
        else:
            self.x -= 1
            return self.x

    def increment_y(self, bash):
        """
        Increments the y value and checks for collision with the border of the terminal and the snake's own body parts
        :param bash: bash instance
        :return: new y coordinate
        """
        # Before mutating self.y, this ycheck is a third party variable used to check collision
        ycheck = self.y - 1

        # Checks for a collision with the snake's own body
        for piece in bash.snake:
            if self.y == piece.y and self.x == piece.y:
                bash.terminate_curses()
                print("GAME OVER! YOU BUMPED INTO THE BORDER!")
                sys.exit()

        # Checks for a collision with the border of the terminal
        if ycheck < 0:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            sys.exit()
        # No collision with the border of the terminal
        else:
            self.y -= 1
            return self.y

    def decrement_y(self, bash):
        """
        Decrements the y value and checks for collision with the border of the terminal and the snake's own body parts
        :param bash: bash instance
        :return: new y coordinate
        """
        # Before mutating self.y, this ycheck is a third party variable used to check collision
        ycheck = self.y + 1

        # Checks for a collision with the snake's own body
        for piece in bash.snake:
            if self.y == piece.y and self.x == piece.y:
                bash.terminate_curses()
                print("GAME OVER! YOU BUMPED INTO THE BORDER!")
                sys.exit()

        # Checks for a collision with the border of the terminal
        if ycheck == curses.LINES:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            sys.exit()
        # No collision with the border of the terminal
        else:
            self.y += 1
            return self.y


class Bash:
    def __init__(self):
        # This is for the world tick system
        # This is not needed until I implement food for the snake, which will be a while
        self._tick_value = 0

        # This is used for moving the snake
        self.directions = cycle(['n', 'e', 's', 'w'])
        self.direction = 'n'

        # Curses coordinates
        # Legal coordinates = (0, 0) -> (curses.LINES - 1, curses.COLS - 1)
        # Curses counts coordinates from the top left at(0, 0)

        # Used to test if the keys being pressed are registered
        self.pressed = []

    def start_curses(self):
        """
        This starts the curses application
        The curses application "prints" to the terminal
        :return: None
        """
        # Initializes the curses application
        self.stdscr = curses.initscr()

        # This hides the cursor
        curses.curs_set(False)

        # A terminal normally captures key presses and prints the key being pressed     (similar to input function)
        # This disables that
        curses.noecho()

        # This function is being called so that the enter key will not have to be pressed after clicking a key
        curses.cbreak()

        # This function call allows the user to enter keys without the program freezing
        self.stdscr.nodelay(True)

        # So the terminal does not return multibyte escape sequences
        # Instead, curses returns something like curses.KEY_LEFT
        self.stdscr.keypad(True)

    def terminate_curses(self):
        """
        Terminates the curses application and returns control to the terminal
        :return: None
        """
        curses.flash()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def getch(self):
        """
        Will return the current key being pressed
        :return: A dict with 'W', 'A', 'D', and the arrows and either 0 or 1 depending on if the key is being pressed or not
        """
        gotten = self.stdscr.getch()
        self.pressed.append(gotten)
        return gotten

    def capture_keys(self, key_pressed):
        """
        Will perform some command based on which key is pressed
        :param key_pressed: the current key being pressed
        :return: None
        """
        mapping = {
                    curses.KEY_UP:lambda: self.set_direction('n'),
                    curses.KEY_DOWN:lambda: self.set_direction('s'),
                    curses.KEY_LEFT:lambda: self.set_direction('w'),
                    curses.KEY_RIGHT:lambda: self.set_direction('e'),
                    }
        try:
            mapping[key_pressed]()
        except KeyError:
            pass

    def set_direction(self, direction):
        bool_check(["'{}'".format(direction)], " in {}".format(self.directions.values()))
        self.direction = direction

    def get_tick(self):
        return self._tick_value

    def increment_tick(self):
        self._tick_value += 1
        return self._tick_value

    def tick(self):
        """
        This snake world will operate on ticks like in minecraft
        Every tick the snake will move forward one block
        :return: current tick
        """
        if self.direction == 'n':
            self.move_snake_fowards()
        elif self.direction == 'e':
            self.move_snake_right()
        elif self.direction == 's':
            self.move_snake_backwards()
        elif self.direction == 'w':
            self.move_snake_left()

        self.increment_tick()
        return self.get_tick()

    def create_snake(self):
        """
        Creates the head of the snake in the middle of the terminal
        :return: None
        """
        # Snake head / the X
        self.snake_head = Snake(int(curses.LINES / 2), int(curses.COLS / 2))
        # List of snake body parts
        # Snake body parts will be appended to this list
        self.snake = []

        # Prints the snake head on the screen
        self.add_char(self.snake_head.y, self.snake_head.x)
        self.refresh()

    def move_snake_fowards(self):
        """
        Moves the snake forward one character
        :return: (y, x)
        """
        prev_head = self.snake_head.y
        self.snake_head.increment_y(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x)
        self.del_char(prev_head, self.snake_head.x)
        self.refresh()
        return self.snake_head.y, self.snake_head.x

    def move_snake_backwards(self):
        """
        Moves the snake backwards one character
        :return: (y, x)
        """
        prev_head = self.snake_head.y
        self.snake_head.decrement_y(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x)
        self.del_char(prev_head, self.snake_head.x)
        self.refresh()
        return self.snake_head.y, self.snake_head.x

    def move_snake_right(self):
        """
        Turns the snake to the right and updates the tick
        :return: (x, y)
        """
        prev_head = self.snake_head.x
        self.snake_head.increment_x(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x)
        self.del_char(self.snake_head.y, prev_head)
        self.refresh()
        return self.snake_head.y, self.snake_head.x

    def move_snake_left(self):
        """
        Turns the snake to the left and updates the tick
        :return:
        """
        prev_head = self.snake_head.x
        self.snake_head.decrement_x(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x)
        self.del_char(self.snake_head.y, prev_head)
        self.refresh()
        return self.snake_head.y, self.snake_head.x

    def add_char(self, y, x, char='X'):
        """
        Adds a character at given coordinates
        :param y: y coordinate of char to add
        :param x: x coordinate of char to add
        :return: None
        """
        self.stdscr.addstr(y, x, char)

    def del_char(self, y, x):
        """
        Deletes a character at given coordinates
        :param y: y coordinate of char to delete
        :param x: x coordinate of char to delete
        :return: None
        """
        self.stdscr.addstr(y, x, ' ')

    def clear(self):
        """
        Clears the terminal
        :return: None
        """
        self.stdscr.clear()

    def refresh(self):
        """
        'Draws' the text based snake list on the screen
        :return: printable string
        """
        self.stdscr.refresh()


class BooleanFalseEvalWarning(Exception):
    def __init___(self):
        pass
