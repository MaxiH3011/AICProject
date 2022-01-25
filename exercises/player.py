"""
This class was entirely made by us. It makes it possible to move a player around in the maze by using increments
"""


class Player:

    def __init__(self):
        self.position = [6, 6]

    def move(self, increment, maze):
        # the player should not exceed the borders of the maze in the next move
        if self.position[0] + increment[0] <= 9 and self.position[1] + increment[1] <= 9:
            # the player should also not go over walls. The following if statement checks if the node the player wants
            # to go to is in the neighbours of the players current node. This would mean that there is a link between
            # the nodes and therefore no wall
            if maze.grid[self.position[0] + increment[0]][self.position[1] + increment[1]] in maze.grid[self.position[0]][self.position[1]].neighbours:
                # the current position is incremented with the values given
                self.position[0] = self.position[0] + increment[0]
                self.position[1] = self.position[1] + increment[1]

        # the update target method gets called which updates which field is colored for the player
        maze.update_target(self.position)
