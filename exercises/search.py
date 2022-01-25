"""
This class was taken from tutorial 6 and altered by us
"""

import random
from datetime import datetime
from exercises.maze import Maze
import bisect


class Search:

    def __init__(self, graph):
        self.graph = graph
        random.seed(datetime.now())
        # lst to save the entire path
        self.path_l = list()

    # ADD YOU IMPLEMENTATIONS FOR GREEDY AND ASTAR HERE!
    # we decided to use greedy search to make the AI not completely perfect in order to make it easier fro the player
    # to win
    # the code for greedy search was written in tutorial 6
    def greedy_search(self):
        self.graph.reset_state()

        pri_queue = [self.graph.start]
        visited = []

        while len(pri_queue) > 0:
            current_node = pri_queue.pop(0)
            if current_node != self.graph.target:
                if current_node not in visited:
                    visited.append(current_node)
                    for n in current_node.get_neighbours():
                        if n not in visited:
                            n.set_parent(current_node)
                            n.score = n.manhattan_distance(self.graph.target)
                            bisect.insort_left(pri_queue, n)
            else:
                break
        self.highlight_path()

    def highlight_path(self):
        # Compute the path, back to front.
        current_node = self.graph.target.parent

        while current_node is not None and current_node != self.graph.start:
            current_node.set_color((248, 220, 50))
            # all nodes in the path get appended to the path_l list so that we can see the entire path always
            self.path_l.append(current_node)
            current_node = current_node.parent


    def make_move(self, maze):  # , boolean
        # change position of start node to latest path node
        # reload path
        self.greedy_search()
        # the ai can always ,make one move. since the path gets computed backwards, the ai's next step is the
        # one that is last in the list, so the one with index = -1
        maze.update_start(self.path_l[-1].position)

