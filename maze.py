from collections import deque
from copy import deepcopy, copy
from typing import List, Deque

import numpy as np
import random

from numpy.random import randint


class Maze:



    def __init__(self, length):

        self.__grid = np.empty((length, length), dtype=object)  # Each element is a set

        # Initialize each cell with an empty set



    def generate_maze(self):

        length = len(self.__grid)
        end = [randint(length), randint(length)]
        non_maze_cells = set()

        for i in range(length):
            for j in range(length):

                if end == [i, j]:
                    self.__grid[i, j] = set()

                else:
                    self.__grid[i, j] = -1
                    non_maze_cells.add((i, j))

        while non_maze_cells:
            chosen_cell = non_maze_cells.pop()
            self.random_walk(chosen_cell[0], chosen_cell[1], non_maze_cells)





    def random_walk(self, row, column, non_maze_set):

        current_row = row

        current_column = column

        while not isinstance(self.__grid[current_row, current_column], set):

            last_row = current_row
            last_column = current_column


            direction = random.randint(0, 3)
            self.__grid[last_row, last_column] = direction


            if direction == 0:
                if current_row > 0:
                    current_row -= 1

            if direction == 1:
                if current_row < len(self.__grid) - 1:
                    current_row += 1

            if direction == 2:
                if current_column < len(self.__grid) - 1:
                    current_column += 1

            if direction == 3:
                if current_column > 0:
                    current_column -= 1

            #self.__grid[last_row, last_column] = direction

        self.build_hallway(row, column, non_maze_set)

    def build_hallway(self, row, column, non_maze_set):

        row, column, direction = self.step(row, column)

        while not isinstance(self.__grid[row, column], set):
            non_maze_set.remove((row, column))
            row, column, direction = self.step(row, column, direction)


        if direction >= 2:
            self.__grid[row, column].add(5 - direction)
        else:
            self.__grid[row, column].add(1 - direction)




    def step(self, row, column, last_direction = None)-> [int, int, int]: #row, column, direction
        """check the current direction, move and update the cells to a maze call(set)"""

        last_row = row
        last_column = column

        direction = self.__grid[row, column]

        row, column = self.update_coords(direction, row, column)

        if last_direction is not None:
            if last_direction >= 2:
                self.__grid[last_row, last_column] = {direction, 5 - last_direction}
            else:
                self.__grid[last_row, last_column] = {direction, 1 - last_direction}



        else:
            self.__grid[last_row, last_column] = {direction}



        return [row, column, direction]

    def update_coords(self, direction, row, column):

        if direction == 0:
            row -= 1

        if direction == 1:
            row += 1

        if direction == 2:
            column += 1

        if direction == 3:
            column -= 1

        return row, column

    def print_maze(self):
        # Loop over each row in the grid
        for row in self.__grid:
            # Convert each set of numbers to a comma-separated string and print the row
            row_str = ", ".join(str(sorted(cell)) for cell in row)
            print(row_str)

    def get_maze(self):
        return self.__grid

    def solve_maze(self, x1, y1, x2, y2)-> Deque[List[int]]: #x1 y1 start, x2 y2 end
        """return a path from point a to point b"""

        return self.__solve_maze_helper(x2, y2, x1, y1,deque())


    def __solve_maze_helper(self, cur_x: int, cur_y: int, target_x, target_y, path: Deque[List[int]])-> Deque[List[int]]:

        if cur_x == target_x and cur_y == target_y:
            return path


        for direction in self.__grid[cur_y, cur_x]:


            next_y1, next_x1 = self.update_coords(direction, cur_y, cur_x)

            if not path or [next_y1, next_x1] != path[-1]:

                updated_path = copy(path)
                updated_path.append([cur_y, cur_x])


                path_info = self.__solve_maze_helper(next_x1, next_y1, target_x, target_y, updated_path)
                if path_info:

                    return path_info
        return



















