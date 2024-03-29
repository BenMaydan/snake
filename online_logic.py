import curses
import json
import requests
import uuid


def hwid():
    """
    Returns the hardware id
    :return: hardware id
    """
    return uuid.UUID(int=uuid.getnode())


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
        self.score = 0

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
        self.snake_list = [SnakeBody(self.snake_head.y + 1, self.snake_head.x)]

        # Prints the snake head on the screen
        self.add_char(self.snake_head.y, self.snake_head.x, 'X')

        # Adds body part right behind the head
        behind_the_head = SnakeBody(self.snake_head.y + 1, self.snake_head.x)
        # Appends body part to snake_list
        self.snake_list.append(behind_the_head)
        # Actually adds the body part right behind the head
        self.add_char(self.snake_head.y + 1, self.snake_head.x, 'O')

        # Creates a second body part right behind the head
        second_behind_the_head = SnakeBody(self.snake_head.y + 2, self.snake_head.x)
        # Appends body part to snake_list
        self.snake_list.append(second_behind_the_head)
        # Actually adds the body part right behind the head
        self.add_char(self.snake_head.y + 2, self.snake_head.x, 'O')

        self.refresh()

    def grow_snake(self):
        """
        Grows an O onto the end of the snake
        :return: None
        """
        second_to_last_part = self.snake_list[-2]
        last_part = self.snake_list[-1]
        # Determines the direction to insert the new snake body part
        # Based off of the directions of the second to last part and the last part
        if second_to_last_part.y < last_part.y:
            # This means the second to last part is underneath the last part
            dir_tuple = (last_part.y - 1, last_part.x)
        elif second_to_last_part.y > last_part.y:
            # This means the second to last part is above the last part
            dir_tuple = (last_part.y + 1, last_part.x)
        elif second_to_last_part.x < last_part.x:
            # This means the second to last part is to the left of the last part
            dir_tuple = (last_part.y, last_part.x - 1)
        elif second_to_last_part.x > last_part.x:
            # This means the second to last part is to the right of the last part
            dir_tuple = (last_part.y, last_part.x + 1)

        new_part = SnakeBody(dir_tuple[0], dir_tuple[1])

        # Appends body part to snake_list
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
        behind_the_head = SnakeBody(self.snake_head.y + 1, self.snake_head.x)
        # Appends body part to snake_list
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
            # Removes the last character of the snake from self.snake_list
            self.snake_list.remove(last_part)

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
        behind_the_head = SnakeBody(self.snake_head.y - 1, self.snake_head.x)
        # Appends body part to snake_list
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
        behind_the_head = SnakeBody(self.snake_head.y, self.snake_head.x - 1)
        # Appends body part to snake_list
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
        behind_the_head = SnakeBody(self.snake_head.y, self.snake_head.x + 1)
        # Appends body part to snake_list
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

    def refresh(self):
        """
        'Draws' the text based snake list on the screen
        :return: printable string
        """
        self.stdscr.refresh()


class Communicator:
    """
    Talks to the raspberry pi to make requests such as move forward or grow snake
    Raspberry pi then determines collision
    """
    def __init__(self, link, intensity):
        self.bash = Bash(10, 0.1)
        # This holds the data that is received from the raspberry pi
        self.data = {}
        # This holds the hwid of the creator of the game
        self.hwid = 0
        # This value is how much the snake grows every time
        self.intensity = intensity
        # Creates a base link to make requests off of
        self.link = link

    def create_game(self, ):
        """
        Sends a POST request to the raspberry to create a game
        :return: None
        """

    def join_game(self, hardware_id, name):
        """
        Joins a game with the specified hwid/game password
        :param game_id: hwid of the creator of the game
        :return: printable
        """
        # Process of sending a POST request
        dict_to_send = {'hwid': hardware_id, 'snake_list': snake_list, 'name': name}
        response = requests.post(self.link + '/join', json=dict_to_send)
        returnable = json.loads(response.text)
        self.hwid = returnable
        return json.loads(response.text)

    def tick(self):
        """
        Sends a request to the server to tick one
        :return: current tick value
        """
        return self.bash.get_tick()
