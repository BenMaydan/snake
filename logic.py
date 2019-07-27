# Snake
# A text based snake game
# Made by BEN MAYDAN
# Copyrighted

# Imports go here
import keyboard
import curses
import random
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


def opposite_direction(facing, dir):
    """
    Returns the opposite direction
    N - S
    E - W
    S - N
    W - E
    :param facing: The direction the snake is facing
    :param dir: The direction/key the user pressed
    :return:
    """
    # Checks if for example n == s or e == w
    # to prevent the ability from turning the opposite direction the user is currently going
    return facing == {curses.KEY_UP:curses.KEY_DOWN, curses.KEY_RIGHT:curses.KEY_LEFT, curses.KEY_DOWN:curses.KEY_UP, curses.KEY_LEFT:curses.KEY_RIGHT}[dir]


def key_exists(dictionary, key_to_check):
    """
    Raises KeyError if key_to_check does not exist in dictionary
    :return: None
    """
    if key_to_check not in dictionary:
        raise KeyError()


def snake_body_collision(bash, head):
    """
    Checks for a collision with the snake's own body
    Terminates the program if there is collision
    :param bash: Bash instance
    :param head: Snake head
    :return: None
    """
    # Checks for a collision with the snake's own body
    for piece in bash.snake_list:
        if head.y == piece.y and head.x == piece.x:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO YOURSELF!")
            print(score(bash))
            print(highscore(bash))
            sys.exit()


def snake_food_collision(bash, head):
    """
    Checks for collision with snake head and food
    Since there will not be lots of food on the screen I need to loop over
    A simple single if statement will do the trick
    :param bash: Bash instance
    :param head: Snake head
    :return: True or False
    """
    # A simple collision check by checking if the coordinates of the snake head and the food are the same
    if head.y == bash.food[0] and head.x == bash.food[1]:
        # This is a test to see if the snake can actually grow
        # This can be commented out safely
        for x in range(10):
            try:
                bash.grow_snake()
            # curses._curses_error is not accessible so I need to catch all errors
            except:
                # Breaks the loop of snake body pieces to grow to avoid unnecessary computation
                break
        bash.sleep -= 0.001

        bash.food_exists = False
        bash.score += 1

        # Resets the tick so the food can generate again
        bash.reset_tick()
    return not bash.food_exists


def update_score_on_screen(bash):
    """
    Updates the characters at the top left to say "score = (current score)"
    :param bash: Bash instance
    :return: User's current score
    """
    x = 0
    letters = ['S', 'c', 'o', 'r', 'e', ' ', '=', ' ', str(bash.score)]
    for letter in letters:
        bash.del_char(0, x)
        bash.add_char(0, x, letter)
        x += 1
    bash.refresh()


def score(bash):
    """
    Multiplies score by time spent in the game alive
    :param bash: Bash instance
    :return: New score
    """
    return "Your score was: " + str(bash.score)


def highscore(bash):
    """
    Returns the text to print for a highscore
    :return: Text
    """
    with open('highscore.txt', 'r') as f:
        high = f.read()
    if bash.score > int(high):
        with open('highscore.txt', 'w') as f:
            high = bash.score
            f.write(str(bash.score))
    return "Your highscore is: " + str(high)


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


class SnakeHead:
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

        # Collision checks if the snake head collides with a piece of it's body
        # The program terminates if true
        snake_body_collision(bash, self)

        # Checks for snake food collision. If there is collision, the snake will grow and score will increase
        snake_food_collision(bash, self)

        # Checks for a collision with the border of the terminal
        if xcheck == curses.COLS:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            print(score(bash))
            print(highscore(bash))
            sys.exit()

        # This only happens if there is no collision
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

        # Collision checks if the snake head collides with a piece of it's body
        # The program terminates if true
        snake_body_collision(bash, self)

        # Checks for snake food collision. If there is collision, the snake will grow and score will increase
        snake_food_collision(bash, self)

        # Checks for a collision with the border of the terminal
        if xcheck < 0:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            print(score(bash))
            print(highscore(bash))
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

        # Collision checks if the snake head collides with a piece of it's body
        # The program terminates if true
        snake_body_collision(bash, self)

        # Checks for snake food collision. If there is collision, the snake will grow and score will increase
        snake_food_collision(bash, self)

        # Checks for a collision with the border of the terminal
        if ycheck < 0:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            print(score(bash))
            print(highscore(bash))
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

        # Collision checks if the snake head collides with a piece of it's body
        # The program terminates if true
        snake_body_collision(bash, self)

        # Checks for snake food collision. If there is collision, the snake will grow and score will increase
        snake_food_collision(bash, self)

        # Checks for a collision with the border of the terminal
        if ycheck == curses.LINES:
            bash.terminate_curses()
            print("GAME OVER! YOU BUMPED INTO THE BORDER!")
            print(score(bash))
            print(highscore(bash))
            sys.exit()
        # No collision with the border of the terminal
        else:
            self.y += 1
            return self.y


class SnakeBody:
    def __init__(self, y, x, direction):
        if direction not in ['n', 'e', 's', 'w']:
            raise ValueError("Snake body direction {} must be one of the following {}".format(direction, ['n', 'e', 's', 'w']))
        self.y = y
        self.x = x
        self.direction = direction

    def follow(self, bash):
        """
        Follows the snake body closest to it and to the snake head
        :return: new (y, x) coordinates for this body
        """
        bash.del_char(self.y, self.x)
        bash.add_char(self.y - 1, self.x, 'O')


class Bash:
    def __init__(self, generate_food, sleep):
        # This is for the world tick system
        # This is not needed until I implement food for the snake, which will be a while
        self._tick_value = 0
        self.sleep = sleep

        # Curses coordinates
        # Legal coordinates = (0, 0) -> (curses.LINES - 1, curses.COLS - 1)
        # Curses counts coordinates from the top left at(0, 0)

        # This is used for moving the snake
        self.directions = cycle(['n', 'e', 's', 'w'])
        self.direction = 'n'

        # This value is to see if it is time to generate food
        # Every tick this value is incremented, unless food has just been generated
        # In that case, this value is set to 0
        self.food_tick = generate_food

        # This is for the food generation system. This list will hold all of the food
        # And when the snake moves it will check if the head is colliding
        # If the head is colliding the snake will grow and the score will increment by 1
        self.food = (-1, -1)
        self.food_exists = False

        # This score will be printed at the end. It is incremented every time the snake eats a piece of food
        # And at the end of the game it is multiplied by how many seconds you stayed alive
        self.score = 0
        self.time_spent = 1

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
        return self.stdscr.getch()

    def capture_keys(self, key_pressed):
        """
        Will perform some command based on which key is pressed
        :param key_pressed: the current key being pressed
        :return: None
        """
        mapping = {
                    curses.KEY_UP: lambda: self.set_direction('n'),
                    curses.KEY_DOWN:lambda: self.set_direction('s'),
                    curses.KEY_LEFT:lambda: self.set_direction('w'),
                    curses.KEY_RIGHT:lambda: self.set_direction('e'),
                    }
        try:
            # Raises key error if key does not exist in mapping dict
            # I.E. user pressed W or A
            key_exists(mapping, key_pressed)
        except KeyError:
            pass
        else:
            # This is to ensure the user does not accidentally bump into themselves
            # when they are facing a direction and click a key to go in the opposite direction
            if not opposite_direction({'n':curses.KEY_UP, 'e':curses.KEY_RIGHT, 's':curses.KEY_DOWN, 'w':curses.KEY_LEFT}[self.direction], key_pressed):
                mapping[key_pressed]()

    def set_direction(self, direction):
        bool_check(["'{}'".format(direction)], " in {}".format(self.directions.values()))
        self.direction = direction

    def get_tick(self):
        return self._tick_value

    def reset_tick(self):
        """
        Everytime food is generated self.tick_value will reset so I can check the next time
        If food should be generated
        :return: None
        """
        self._tick_value = 0

    def increment_tick(self):
        self._tick_value += 1
        return self._tick_value

    def tick(self):
        """
        This snake world will operate on ticks like in minecraft
        Every tick the snake will move forward one block by default
        :return: current tick
        """
        # Moves the head of the snake depending on the current direction
        if self.direction == 'n':
            self.move_snake_forwards()
            # Refreshes the screen
            self.refresh()
        elif self.direction == 'e':
            self.move_snake_right()
            # Refreshes the screen
            self.refresh()
        elif self.direction == 's':
            self.move_snake_backwards()
            # Refreshes the screen
            self.refresh()
        elif self.direction == 'w':
            self.move_snake_left()
            # Refreshes the screen
            self.refresh()

        # This if statement is for the food generation system
        # Every some amount of ticks, a piece of food is placed
        # At a random (y, x) coordinate on the screen
        if self.get_tick() == self.food_tick and self.food_exists is False:
            random_y_coordinate = random.randrange(2, curses.LINES - 2)
            random_x_coordinate = random.randrange(2, curses.COLS - 2)

            # This while loop is a sanity check to make sure the food does not spawn on the snake
            while self.get_char(random_y_coordinate, random_x_coordinate) in ('X', 'O'):
                random_y_coordinate = random.randrange(2, curses.LINES - 2)
                random_x_coordinate = random.randrange(2, curses.COLS - 2)

            self.food = (random_y_coordinate, random_x_coordinate)

            # Adds char to the screen
            self.add_char(random_y_coordinate, random_x_coordinate, 'F')
            self.reset_tick()

            # Used so food will not spawn until this food has been eaten
            self.food_exists = True

            # There is no need to update the score on the screen every tick
            # Since bash.score only gets incremented every time food is eated
            update_score_on_screen(self)

            # Finally, after all the random coordinates have been found and a char was added, the screen will refresh
            self.refresh()

        self.increment_tick()
        return self.get_tick()

    def create_snake(self):
        """
        Creates the head of the snake in the middle of the terminal
        :return: None
        """
        # Snake head / the X
        self.snake_head = SnakeHead(int(curses.LINES / 2), int(curses.COLS / 2))
        # List of snake body parts
        # Snake body parts will be appended to this list
        self.snake_dict = {id((self.snake_head.y + 1, self.snake_head.x)):SnakeBody(self.snake_head.y + 1, self.snake_head.x, 'n')}
        self.snake_list = [SnakeBody(self.snake_head.y + 1, self.snake_head.x, 'n')]

        # Prints the snake head on the screen
        self.add_char(self.snake_head.y, self.snake_head.x, 'X')

        # Adds body part right behind the head
        behind_the_head = SnakeBody(self.snake_head.y + 1, self.snake_head.x, 'n')
        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((self.snake_head.y + 1, self.snake_head.x))] = behind_the_head
        self.snake_list.append(behind_the_head)
        # Actually adds the body part right behind the head
        self.add_char(self.snake_head.y + 1, self.snake_head.x, 'O')

        # Creates a second body part right behind the head
        second_behind_the_head = SnakeBody(self.snake_head.y + 2, self.snake_head.x, 'n')
        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((self.snake_head.y + 2, self.snake_head.x))] = second_behind_the_head
        self.snake_list.append(second_behind_the_head)
        # Actually adds the body part right behind the head
        self.add_char(self.snake_head.y + 2, self.snake_head.x, 'O')

        self.refresh()

    def grow_snake(self):
        """
        Grows an O onto the end of the snake
        :return: None
        """
        last_part = self.snake_list[-1]
        second_to_last_part = self.snake_list[-2]
        new_part = SnakeBody(last_part.y - 1, last_part.x, 'n')

        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((new_part.y, new_part.x))] = new_part
        self.snake_list.append(new_part)

        # Creates char on the screen (body part right behind the head
        self.add_char(new_part.y, new_part.x, 'O')
        self.refresh()

    def move_snake_forwards(self):
        """
        Moves the snake forward one character
        :return: (y, x)
        """
        prev_head = self.snake_head.y
        self.snake_head.increment_y(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x, 'X')
        self.del_char(prev_head, self.snake_head.x)

        # Adds body part right behind the head
        behind_the_head = SnakeBody(self.snake_head.y + 1, self.snake_head.x, 'n')
        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((self.snake_head.y + 1, self.snake_head.x))] = behind_the_head
        self.snake_list.insert(0, behind_the_head)
        # Creates char on the screen (body part right behind the head
        self.add_char(self.snake_head.y + 1, self.snake_head.x, 'O')

        # Deletes the last character of the snake on the screen
        last_part = self.snake_list[-1]
        try:
            self.del_char(last_part.y, last_part.x)
        except:
            self.snake_list.pop(-1)
        else:
            # Removes the last character of the snake from self.snake_list and self.snake-dict
            self.snake_list.remove(last_part)
            del self.snake_dict[id((last_part.y, last_part.x))]

        return self.snake_head.y, self.snake_head.x

    def move_snake_backwards(self):
        """
        Moves the snake backwards one character
        :return: (y, x)
        """
        prev_head = self.snake_head.y
        self.snake_head.decrement_y(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x, 'X')
        self.del_char(prev_head, self.snake_head.x)

        # Adds body part right behind the head
        behind_the_head = SnakeBody(self.snake_head.y - 1, self.snake_head.x, 'n')
        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((self.snake_head.y - 1, self.snake_head.x))] = behind_the_head
        self.snake_list.insert(0, behind_the_head)
        # Creates char on the screen (body part right behind the head
        self.add_char(self.snake_head.y - 1, self.snake_head.x, 'O')

        # # Deletes the last character of the snake on the screen
        last_part = self.snake_list[-1]
        try:
            self.del_char(last_part.y, last_part.x)
        except:
            self.snake_list.pop(-1)
        else:
            # Removes the last character of the snake from self.snake_list and self.snake-dict
            self.snake_list.remove(last_part)
            del self.snake_dict[id((last_part.y, last_part.x))]

        return self.snake_head.y, self.snake_head.x

    def move_snake_right(self):
        """
        Turns the snake to the right and updates the tick
        :return: (x, y)
        """
        prev_head = self.snake_head.x
        self.snake_head.increment_x(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x, 'X')
        self.del_char(self.snake_head.y, prev_head)

        # Adds body part right behind the head
        behind_the_head = SnakeBody(self.snake_head.y, self.snake_head.x - 1, 'n')
        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((self.snake_head.y, self.snake_head.x - 1))] = behind_the_head
        self.snake_list.insert(0, behind_the_head)
        # Creates char on the screen (body part right behind the head
        self.add_char(self.snake_head.y, self.snake_head.x - 1, 'O')

        # # Deletes the last character of the snake on the screen
        last_part = self.snake_list[-1]
        try:
            self.del_char(last_part.y, last_part.x)
        except:
            self.snake_list.pop(-1)
        else:
            # Removes the last character of the snake from self.snake_list and self.snake-dict
            self.snake_list.remove(last_part)
            del self.snake_dict[id((last_part.y, last_part.x))]

        return self.snake_head.y, self.snake_head.x

    def move_snake_left(self):
        """
        Turns the snake to the left and updates the tick
        :return:
        """
        prev_head = self.snake_head.x
        self.snake_head.decrement_x(self)

        # Updates the screen to move the X forward
        self.add_char(self.snake_head.y, self.snake_head.x, 'X')
        self.del_char(self.snake_head.y, prev_head)

        # Adds body part right behind the head
        behind_the_head = SnakeBody(self.snake_head.y, self.snake_head.x + 1, 'n')
        # Appends body part to snake_dict and snake_list
        self.snake_dict[id((self.snake_head.y, self.snake_head.x + 1))] = behind_the_head
        self.snake_list.insert(0, behind_the_head)
        # Creates char on the screen (body part right behind the head
        self.add_char(self.snake_head.y, self.snake_head.x + 1, 'O')

        # # Deletes the last character of the snake on the screen
        last_part = self.snake_list[-1]
        try:
            self.del_char(last_part.y, last_part.x)
        except:
            self.snake_list.pop(-1)
        else:
            # Removes the last character of the snake from self.snake_list and self.snake-dict
            self.snake_list.remove(last_part)
            del self.snake_dict[id((last_part.y, last_part.x))]

        return self.snake_head.y, self.snake_head.x

    def add_char(self, y, x, char):
        """
        Adds a character at given coordinates
        :param y: y coordinate of char to add
        :param x: x coordinate of char to add
        :param: char: the type of body part of the snake (X = head, O = body)
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

    def get_char(self, y, x):
        """
        Returns the character at the given coordinates
        :param x: x coordinate of screen
        :param y: y coordinate of screen
        :return: The character at the given coordinates
        """
        return chr(self.stdscr.inch(y, x))

    def clear_screen(self):
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
