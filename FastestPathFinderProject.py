import curses
from curses import wrapper
import queue
import time
#FASTEST PATH FINDER USING QUEUE DATA STRUCTURES!

#MAZE LAYOUT , O is out Initial and X is our Final
maze = [
    ["#", "#", "#", "#", "#", "#", "O", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1) #to make it as a subject use curses module, color_pair(id)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze): #i is define as row, using enumerate(maze)
        for j, value in enumerate(row):  #j is define as column, using enumerate(row): nested for loops
            if (i, j) in path:
              stdscr.addstr(i, j*3, "X", RED)
            else:
              stdscr.addstr(i, j*3, value, BLUE)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None

def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue() #defining queue module
    q.put((start_pos, [start_pos])) #two elements is inserted due to track the current position and the path that allows user to track(allow us to draw the path on the terminal)

    visited = set()

    while not q.empty(): #using while loop conditioning untill it reaches to the end node
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path) #path will be show in the screen for every single iteration
        time.sleep(0.2)
        stdscr.refresh()  #this will help to continuing the progress of the path

        #CONDITIONING

        if maze[row][col] == end:
            return path #we returning the path because in the end the path will show us the output screen

        neighbours = find_neighbours(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if maze[r][c] == "#":
                continue

            #PROCESSING

            new_path = path + [neighbour]
            q.put((neighbour, new_path)) 
            visited.add(neighbour) #we need to add the neighbour coordinates in the visited set to ensure that it wont be processed twice!
        

    #EXPANDING

def find_neighbours(maze, row, col):
    neighbours = [] #the list will filled up as the function starts!

    #UP
    if row > 0:
        neighbours.append((row - 1, col))
    #DOWN
    if row + 1 < len(maze):
        neighbours.append((row + 1, col))
    #LEFT
    if col > 0:
        neighbours.append((row, col - 1))
    #RIGHT
    if col + 1 < len(maze[0]): #len(maze[0]) is identify as the first row of the maze to ensure that the last column is the end of the first row on the right side
        neighbours.append((row, col + 1))

    return neighbours

    
def main(stdscr): #stdscr means standard output screen
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK) #to paint the words, we need to initialize the pair color! (id, 1st color, 2nd color)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # 1st color is foreground and 2nd color is background!
    find_path(maze, stdscr)
    stdscr.addstr(10, 0, "I FOUND IT!", curses.color_pair(1))
    stdscr.getch() #to make sure when you type any characters after output is printed, it will be back to idle terminal


wrapper(main)


