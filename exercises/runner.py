"""
This class was entirely written by us. It creates a "runner" that tries to escape from the AI player
"""

class Runner:
    def __init__(self):
        self.position = [3, 3]

    # max_node is the node with the highest manhattan distance from current nodes neighbours to ai player
    # this is calculated in the calculate_next_move method
    def make_move(self, max_node, maze):
        # the runner should not exceed the borders of the maze
        if self.position[0] + max_node[0] <= 9 and self.position[1] + max_node[1] <= 9:
            # the following if statement does the same as in the player class. The runner should not run over walls
            if maze.grid[self.position[0] + (max_node[0] - self.position[0])][self.position[1] + (max_node[1] - self.position[1])] in maze.grid[self.position[0]][self.position[1]].neighbours:
                # runners position gets updated with the increment
                self.position[0] = self.position[0] + (max_node[0] - self.position[0])
                self.position[1] = self.position[1] + (max_node[1] - self.position[1])

            # colored grid element gets updated
            maze.update_runner(self.position)

    def calculate_next_move(self, grid, search):
        # distances saves the nodes around the runners current node as well as their manhattan distance to the AI player
        distances = list()
        # neighbours list is filled with neighbours
        neighbours = grid[self.position[0]][self.position[1]].get_neighbours()
        for i in range(len(neighbours)):
            # for every neighbor the manhattan distance is checked and saved in the list distances together with the
            # corresponding node
            distances.append((neighbours[i], neighbours[i].manhattan_distance(search.path_l[-1])))
        # the index of the node with the highest manhattan distance is saved
        max_dist_node_index = distances.index(max(distances, key=lambda x: x[1]))
        # the corresponding node gets returned to the make move function
        return distances[max_dist_node_index][0].position
