import sys
import turtle
from collections import deque
from copy import copy
from turtle import Turtle
import pygame


from maze import Maze

def generate_maze_turtle(length, speed):

    maze = Maze(length)


    maze.generate_maze()

    distance = 750/length

    t = Turtle()
    t.hideturtle()
    t.speed(speed)
    t.penup()
    t.goto(-750, 380)
    t.setheading(0)



    for i in range(length):



        for j in range(length):
            draw_cell(maze.get_maze(), i, j, t, distance)
            t.penup()
            t.forward(distance)

        t.penup()
        t.right(180)
        t.forward(length * distance)
        t.left(90)
        t.forward(distance)
        t.left(90)
    turtle.mainloop()
def draw_cell(grid, i, j, t, distance):

    draw_side(grid, i, j, t, 0, distance)
    draw_side(grid, i, j, t, 2, distance)
    draw_side(grid, i, j, t, 1, distance)
    draw_side(grid, i, j, t, 3, distance)


def draw_side(grid, i, j, t, number, distance):
    if number not in grid[i, j]:
        t.pendown()
    else:
        t.penup()

    t.forward(distance)
    t.right(90)






def generate_maze(length, screen_width, screen_height, screen, line_color, maze):



    # u = up, d = down, l = left, r = right
    ul = ((screen_width - (screen_height - 100)) / 2, 50)
    ur = ((screen_width - (screen_height - 100)) / 2 + screen_height - 100, 50)
    dl = ((screen_width - (screen_height - 100)) / 2, screen_height - 50)
    dr = ((screen_width - (screen_height - 100)) / 2 + screen_height - 100, screen_height - 50)




    #maze_width = (screen_width - (screen_height - 100)) / 2, (screen_width - (screen_height - 100)) / 2 + screen
    #width - (screen_height - 100)
    # maze height = 50, screen_height - 50

    #step 1: draw upside down L
    pygame.draw.line(screen, line_color, ur, dr)
    pygame.draw.line(screen, line_color, ur, ul)
    pygame.draw.line(screen, line_color, dl, dr)
    pygame.draw.line(screen, line_color, dl, ul)

    maze_length = screen_height - 100
    distance = float(maze_length / length)



    #create exit
    pygame.draw.line(screen, (255, 255, 255), ((screen_width - (screen_height - 100)) / 2 + screen_height - 100, 50 + distance * (length - 1)), dr)

    draw_cells(maze.get_maze(), screen, line_color, screen_width, screen_height)

    #create entrance
    pygame.draw.line(screen, (255, 255, 255), ul, ((screen_width - (screen_height - 100)) / 2, 50 + distance))


    pygame.display.flip()
    return maze

def draw_cells(grid, screen, line_color, screen_width, screen_height):

    length = len(grid)
    maze_length = screen_height - 100
    distance = float(maze_length / length)

    for i in range(length):

        for j in range(length):
            #for each cell draw L

            if not 1 in grid[i, j]:

                start_pos = ((screen_width - (screen_height - 100)) / 2 + j * distance, 50 + (i + 1) * distance)
                end_pos = ((screen_width - (screen_height - 100)) / 2 + (j + 1) * distance, 50 + (i + 1) * distance)

                pygame.draw.line(screen, line_color, start_pos, end_pos)


            if not 3 in grid[i, j]:
                start_pos = ((screen_width - (screen_height - 100)) / 2 + j * distance, 50 + i * distance)
                end_pos = ((screen_width - (screen_height - 100)) / 2 + j * distance, 50 + (i + 1) * distance)

                pygame.draw.line(screen, line_color, start_pos, end_pos)

def draw_path(maze, start_x, start_y, screen, screen_width, screen_height, color, path):

    temp_path = copy(path)
    maze_length = screen_height - 100
    distance = float(maze_length / len(maze.get_maze()))
    coords = ((screen_width - (screen_height - 100)) / 2 + (start_x + 0.5) * distance, 50 + (start_y + 0.5) * distance)
    start_coords = coords



    while temp_path:
        next_coords = temp_path.pop()
        pygame.draw.line(screen, color, start_coords, (coords[0] + next_coords[1] * distance, coords[1] + next_coords[0] * distance))
        start_coords = (coords[0] + next_coords[1] * distance, coords[1] + next_coords[0] * distance)


def update_path(path, next_coords, direction, grid):

    if direction == 0:
        x_change = 0
        y_change = -1

    if direction == 1:
        x_change = 0
        y_change = 1

    if direction == 2:
        x_change = 1
        y_change = 0

    if direction == 3:
        x_change = -1
        y_change = 0

    next_x = next_coords[1] + x_change
    next_y = next_coords[0] + y_change



    if not path:
        if direction in grid[0, 0]:
            path.append(next_coords)

            return (next_y, next_x)
        return next_coords

    elif path[-1] == (next_y, next_x):

        return path.pop()
    elif direction in grid[next_coords]:

        path.append(next_coords)
        return (next_y, next_x)
    return next_coords


def draw(solved, solve, maze, screen, screen_width, screen_height, solve_color, path_color, path, next_coords):

    fixed_path = deque()
    fixed_path.append(next_coords)

    while path:
        fixed_path.append(path.pop())

    if not solved:

        draw_path(maze, 0, 0, screen, screen_width, screen_height, solve_color, solve)
        generate_maze(size, screen_width, screen_height, screen, (0, 0, 0), maze)
        draw_path(maze, 0, 0, screen, screen_width, screen_height, path_color, fixed_path)
        pygame.display.flip()

        while fixed_path:
            path.append(fixed_path.pop())
        path.pop()


        return True


    else:

        generate_maze(size, screen_width, screen_height, screen, (0, 0, 0), maze)
        draw_path(maze, 0, 0, screen, screen_width, screen_height, path_color, fixed_path)
        pygame.display.flip()

        while fixed_path:
            path.append(fixed_path.pop())
        path.pop()
        return False



# Initialize Pygame
pygame.init()

sys.setrecursionlimit(1000000)

# Get the screen resolution
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Set up the display (fullscreen mode)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Fullscreen Window")

# Define the line color (RGB)
line_color = (0, 0, 0)  # Red
drawn = False

# Main loop
running = True
solved = False
size = 30

maze = Maze(size)
maze.generate_maze()
solve = deque()
path = deque()
next_coords = (0, 0)

while running:

    # Clear screen
    screen.fill((255, 255, 255))  # Fill with white background

    # Draw a simple line (x1, y1, x2, y2)

    #pygame.draw.line(screen, line_color, (50, 50), (screen_width - 50, 50), 5)
    if not drawn:
        # Draw something
        screen.fill((255, 255, 255))  # Fill with white
        maze = generate_maze(size, screen_width, screen_height, screen, (0, 0, 0), maze)
        drawn = True  # Stop refreshing after drawing once
        solve = maze.solve_maze(0, 0, size - 1, size - 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close button on window
            running = False


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC key to exit
                running = False
            if event.key == pygame.K_RETURN:  # ESC key to exit
                solved = draw(solved, solve, maze, screen, screen_width, screen_height, (255, 0, 0),
                              (255, 120, 23), path, next_coords)

            if event.key == pygame.K_w or event.key == pygame.K_UP:  # ESC key to exit
                next_coords = update_path(path, next_coords, 0, maze.get_maze())
                draw(not solved, solve, maze, screen, screen_width, screen_height, (255, 0, 0), (255, 120, 23), path, next_coords)

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:  # ESC key to exit
                next_coords = update_path(path, next_coords, 1, maze.get_maze())
                draw(not solved, solve, maze, screen, screen_width, screen_height, (255, 0, 0), (255, 120, 23), path, next_coords)

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # ESC key to exit
                next_coords = update_path(path, next_coords, 2, maze.get_maze())
                draw(not solved, solve, maze, screen, screen_width, screen_height, (255, 0, 0), (255, 120, 23), path, next_coords)

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:  # ESC key to exit
                next_coords = update_path(path, next_coords, 3, maze.get_maze())
                draw(not solved, solve, maze, screen, screen_width, screen_height, (255, 0, 0), (255, 120, 23), path, next_coords)






    # Update the screen
    #

# Quit Pygame
pygame.quit()


#maze width = (screen width - (screen height - 100)) / 2, (screen width - (screen height - 100)) / 2 + screen width - (screen height - 100)
#maze height = 50, screen_height - 50