"""
This class is based on the maze class from tutorial 6. It has been altered with our own code
"""

import random
from datetime import datetime
from exercises.grid_element import GridElement


class Maze:

    def __init__(self, grid_size_x, grid_size_y, screen_size):

        self.grid_size = (grid_size_x, grid_size_y)

        self.cell_width = screen_size[0] / grid_size_x
        self.cell_height = screen_size[1] / grid_size_y
        self.grid = []

        for x in range(grid_size_x):

            self.grid.append([])
            for y in range(grid_size_y):
                self.grid[x].append(GridElement(x, y, (self.cell_width, self.cell_height)))

        self.start = self.grid[0][0]
        self.target = self.grid[6][6]
        # new colored blocks have been added to the game area
        self.f_target = self.grid[6][7]
        self.runner = self.grid[3][3]
        self.reset_all()
        random.seed(datetime.now())

        self.increment = (0, 0)

    # The three methods below include the reset state method to reset the color of the objects
    """
    This method takes the coordinates of the ai player and updates its position
    """

    def update_start(self, ai_coord):
        self.start = self.grid[ai_coord[0]][ai_coord[1]]
        self.reset_state()

    """
    This method takes the coordinates of the human player and updates its position
    """

    def update_target(self, player_coord):
        self.target = self.grid[player_coord[0]][player_coord[1]]
        self.reset_state()

    """
    This method takes the coordinates of the runner and updates its position
    """

    def update_runner(self, runner_coord):
        self.runner = self.grid[runner_coord[0]][runner_coord[1]]
        self.reset_state()

    """
    This method makes it possible for the human player to see in which direction he/she is facing. This works by using
    a potentiometer - the player can "turn around"
    """

    def display_player_step(self, serial, player_coord):  # made by us
        # potentiometer values are 0 -1023- this is divided by 4 to provide 4 directions to turn in
        # facing left
        if 0 < serial.data_l[0] < 255:
            self.f_target = self.grid[player_coord[0] - 1][player_coord[1]]
            # if the increment is added to the players position it results in a north/south/west/east movement
            # within the grid
            self.increment = (-1, 0)
        else:
            pass
        # facing up
        if 256 < serial.data_l[0] < 511:
            self.f_target = self.grid[player_coord[0]][player_coord[1] - 1]
            self.increment = (0, -1)
        else:
            pass
        # facing right
        if 512 < serial.data_l[0] < 767:
            self.f_target = self.grid[player_coord[0] + 1][player_coord[1]]
            self.increment = (1, 0)
        else:
            pass
        # facing down
        if 768 < serial.data_l[0] < 1023:
            self.f_target = self.grid[player_coord[0]][player_coord[1] + 1]
            self.increment = (0, 1)
        else:
            pass
        self.reset_state()
        # the increment and the f_target coordinations are returned to move the playe in the facing direction
        # when he/she wants
        return [self.increment, self.f_target]

    def reset_all(self):
        for row in self.grid:
            for cell in row:
                cell.reset_neighbours()
        self.reset_state()
        return None

    def reset_state(self):
        for row in self.grid:
            for cell in row:
                cell.reset_state()
        self.start.set_distance(0)
        self.start.set_score(0)

        # different colors for different objects are added
        # red = AI, blue = human player, grey = player direction vision, white = runner
        self.start.color = (240, 100, 100)
        self.target.color = (100, 100, 240)
        self.f_target.color = (30, 30, 30)
        self.runner.color = (255, 255, 255)

        return None

    def set_source(self, cell):
        if cell != self.target:
            self.start = cell
            self.reset_state()

    def set_target(self, cell):
        if cell != self.start:
            self.target = cell
            self.reset_state()

    def print_maze(self):
        transposed = list(zip(*self.grid))
        for row in transposed:
            print(row)
        return None

    def draw_maze(self, surface):
        for row in self.grid:
            for element in row:
                element.draw_grid_element(surface)
        return None

    def possible_neighbours(self, cell):
        neighbours = []
        if cell.position[0] > 0:  # North
            neighbours.append(self.grid[cell.position[0] - 1][cell.position[1]])
        if cell.position[0] < self.grid_size[0] - 1:  # East
            neighbours.append(self.grid[cell.position[0] + 1][cell.position[1]])
        if cell.position[1] < self.grid_size[1] - 1:  # South
            neighbours.append(self.grid[cell.position[0]][cell.position[1] + 1])
        if cell.position[1] > 0:  # West
            neighbours.append(self.grid[cell.position[0]][cell.position[1] - 1])
        return neighbours

    def del_link(self, cell1, cell2):
        if cell2 in cell1.neighbours:
            cell1.neighbours.remove(cell2)
        if cell1 in cell2.neighbours:
            cell2.neighbours.remove(cell1)
        return None

    def add_link(self, cell1, cell2):
        if cell1.manhattan_distance(cell2) == 1:
            cell1.neighbours.append(cell2)
            cell2.neighbours.append(cell1)
        return None

    def generate_maze(self):
        self.reset_all()

        wait = [self.start]
        passed = set()
        while len(wait) > 0:
            current_element = wait.pop(-1)
            if current_element not in passed:
                passed.add(current_element)

                neighbours = self.possible_neighbours(current_element)  # Here we want to us all possible neighbours
                for cell in neighbours[:]:
                    if cell in passed:
                        neighbours.remove(cell)
                random.shuffle(neighbours)
                wait.extend(neighbours)
                for next_element in neighbours:
                    next_element.parent = current_element

                if current_element.parent is not None:  # The source has no parent
                    self.add_link(current_element.parent, current_element)

        # add a few random links
        for i in range(max(self.grid_size)):
            random_row = random.choice(self.grid)
            random_element = random.choice(random_row)
            possible = self.possible_neighbours(random_element)
            for cell in possible[:]:
                if cell in random_element.get_neighbours():
                    possible.remove(cell)
            if len(possible) > 0:
                random_neighbor = random.choice(possible)
                self.add_link(random_element, random_neighbor)

        self.reset_state()
        return None

    # this method returns the current grid to the main class to that can be used in other child classes
    def give_grid(self):
        return self.grid
