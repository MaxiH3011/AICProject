"""
AI&P Project 2022 - by Maximilian Haverkämper and Benjamin Jansen
Based on Code from Tutorial 06 from Assignments
Expanded by own code

In this game the blue player has to catch the white runner, while the red AI chases him/her
"""

import pygame
import sys
from player import Player
from exercises.maze import Maze
from exercises.helpers.constants import Constants
from exercises.search import Search
from exercises.serial_arduino import SerialArduino
from exercises.runner import Runner
from exercises.win_screen import WinScreen


class Game:
    """
    Initialize PyGame and create a graphical surface to write. Similar
    to void setup() in Processing
    """

    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 64)
        self.time = pygame.time.get_ticks()
        # the serial connection to the arduino game controller gets active here
        self.serial = SerialArduino()
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_maze()
        self.search = Search(self.maze)
        # besides the search, a player class and a runner class was added (look into the classes for more information)
        self.player = Player()
        self.runner = Runner()
        # the win screen is in the current implementation only a text in the console
        self.win_screen = WinScreen()
        # the boolean turn shows who's turn it is in the game
        self.turn = True

    """
    Method 'game_loop' will be executed every frame to drive
    the display and handling of events in the background. 
    In Processing this is done behind the screen. Don't 
    change this, unless you know what you are doing.
    """

    def game_loop(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.time
        self.time = current_time
        # the method classify data from the serial class need data from the read input as parameters.
        # this is constantly updated
        self.serial.classify_data(self.serial.read_input())
        self.handle_events()
        self.update_game(delta_time)
        # handle game and handle step call methods for the different players if it is their turn
        self.handle_game()
        self.handle_step()
        # the win screen gets the coordinates from all players to evaluate a win or lose situation ("CATCH")
        self.win_screen.detect_win(self.player.position, self.runner.position, self.search.path_l[-1].position)
        # the player can make a step when it is not the AI's turn
        if not self.turn:
            self.maze.display_player_step(self.serial, self.player.position)
        self.draw_components()

    def update_game(self, dt):
        pass

    def draw_components(self):
        self.screen.fill([255, 255, 255])
        self.maze.draw_maze(self.screen)
        pygame.display.flip()

    """
    This method handles the methods for objects that are active if it is the AIs turn. This includes the runners turn
    """
    def handle_game(self):
        if self.turn:
            self.search.make_move(self.maze)
            # the runners position update method needs the calculate_next_move method as a parameter which needs
            # the maze.give_grid() method
            self.runner.make_move(self.runner.calculate_next_move(self.maze.give_grid(), self.search), self.maze)
            self.turn = False
        else:
            pass

    def reset(self):
        pass

    """
    This method handels the method for the player to move, if it is no the AI's turn
    """

    def handle_step(self):
        if not self.turn:
            if self.serial.data_l[2] == 1:
                self.player.move(self.maze.increment, self.maze)
                self.turn = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
