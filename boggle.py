#############################################################
# FILE: boggle.py
# AUTHORS: 1. Amir Harel
#          2. Nadav Porat
# EXERCISE: Exercise 12
# DESCRIPTION: Boggle
#############################################################

from screen import Screen
from boggle_board_randomizer import *
import sys

'''Magic Variables'''
TITLE = 'Boggle - By Amir Harel and Nadav Porat'
# dictionary that will do the desired function given games status
ENDING_NEW = {
    'exit': lambda self: sys.exit(),
    'retry': lambda self: self.restart()
}


class BoardItem:
    """
    class that each item represents the data of a specific item in the board
    """

    def __init__(self, data, location):
        self.__data = data
        self.__is_pressed = False
        self.__location = location  # coordinates

    def __str__(self):
        return f'{self.__data}'

    def get_data(self):
        return self.__data

    def press(self):
        if self.__is_pressed:
            self.__is_pressed = False
        else:
            self.__is_pressed = True

    def get_status(self):
        return self.__is_pressed

    def get_location(self):
        return self.__location


class BoggleGame:

    def __init__(self):
        self.__screen = Screen()
        self.init_game()

    def init_game(self):
        self.__screen.set_title(TITLE)
        self.board = randomize_board()
        self.__screen.set_board(self.get_board())
        self.__screen.set_dict(parse_boggle_dict())

    def get_board(self):
        board_dict = {}
        for i, row in enumerate(randomize_board()):
            for j, item in enumerate(row):
                board_dict[(i, j)] = BoardItem(item, (i, j))
        return board_dict

    def init_monitor(self):
        """
        need to add after that will make this function update all the time.
        from here we call relevant functions according to users commands
        """
        root = self.__screen.get_root()
        status = self.__screen.get_game_status()
        if status:
            ENDING_NEW[status](self)  # ends or restarts game
        root.after(100, self.init_monitor)  # runs loop on int monitor

    def play(self):
        self.init_monitor()
        self.__screen.start_screen()

    def restart(self):
        self.__screen.set_board(self.get_board())
        self.__screen.reset_screen()  # need to create this function
        self.play()


def parse_boggle_dict():
    file = open('boggle_dict.txt', 'r')
    dictt = file.read()
    file.close()
    dictt = dictt.split('\n')
    return dictt[:-1]


boggle = BoggleGame()
boggle.play()
