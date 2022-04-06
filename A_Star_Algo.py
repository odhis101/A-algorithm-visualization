import pygame
import math 
from queue import PriorityQueue

from pygame import color

width = 700
win= pygame.display.set_mode((width,width))
pygame.display.set_caption(" Path A*Finding Algorithm")

RED = (255,0,0)
GREEN=(0,255,0)
BLUE=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
PURPLE=(128,0,128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUISE=(64,224,208)



class Spot:
    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col = col
        self.x= row*width
        self.y= col*width
        self.color=WHITE
        self.width =width
        self.total_rows= total_rows

    def get_pos(self): # here we are defining the position row and col respectively 
        return self.row,self.col

        #the below code just explains the code of the color that we give instructions to 
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color== BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUISE
    def reset(self):
        self.color = WHITE
    def make_open(self):
        self.color = GREEN
    def make_closed(self):
        self.color = RED
    def make_barrier(self):
        self.color=BLACK
    def make_start (self):
        self.color = ORANGE
    def make_end(self):
        self.color= TURQUISE
    def make_path(self):
        self.color = PURPLE
    def draw(self,win):# drawing the box we are dealing with 
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def update_neighbors(self,grid):
        self.neighbors =[]
        
        if self.row <self.total_rows -1 and not grid[self.row+ 1][self.col].is_barrier(): # checks if moves down
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row >0 and not grid[self.row -1][self.col].is_barrier(): # checks if moves up
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col <self.total_rows -1 and not grid[self.row][self.col+1].is_barrier(): # checks if moves Right
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col >0 and not grid[self.row][self.col-1].is_barrier(): # checks if moves Left
            self.neighbors.append(grid[self.row][self.col-1])

def h(p1,p2):# this uses L distance technique to guess the fastes supposed way 
    x1,y1= p1
    x2,y2= p2
    return abs(x1-x2 )+ abs(y1-y2)

def make_grid (rows,width):
    grid=[]
    gap = width // rows# the width
    for i in range(rows):
        grid.append([]) # creating a 2d list ( [[],[],[]] )
        for j in range(rows):
            spot= Spot(i,j,gap,rows) # to create a new spot we need to pass the parameters stated above 
            grid[i].append(spot)# now we just append it to the grid(so all grids have a spot)
    return grid


def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
def algorithm (draw, grid,start,end):
    count=0
    open_set = PriorityQueue() 
    open_set.put((0,count, start))# this is the calculations for the nodes (start being node itself )(0 is the first f score)
    came_from={}
    g_score={spot:float("inf") for row in grid for spot in row} # keeps track of the current shortest distance from start node to the current node 
    g_score[start]=0
    f_score={spot:float("inf") for row in grid for spot in row} #guesses or gives educated guess on the distance to the end node 
    f_score[start]=h(start.get_pos(),end.get_pos())

    open_set_hash={start} # this basically stores the node information where it is easier to access

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #allows us to quit the game
                pygame.quit()
        current = open_set.get()[2] #this is the current node we are looking at 
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1

            if temp_g_score<g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor]= temp_g_score
                f_score[neighbor]= temp_g_score +h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False

def draw_grid(win,rows,width): # this is just drawing the grid lines 
    gap= width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap), (width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0), (j*gap, width))
def draw(win,grid,rows,width): # this just clears and redraws everything 
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_glicked_pos(pos,rows,width): # given the mouse position this you want to find the row and column position
    gap = width//rows
    y,x=pos
    row = y//gap
    col=x//gap
    return row, col
def main(win,width):
    rows = 50
    grid = make_grid(rows,width)

    start =None
    end = None

    run = True
    start= False
    while run:
        draw(win,grid,rows,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if pygame.mouse.get_pressed()[0]:
                pos =pygame.mouse.get_pos()
                row,col = get_glicked_pos(pos,rows,width)
                spot = grid[row][col]
                if not start and spot != end:
                    start =spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()


            elif pygame.mouse.get_pressed()[2]:
                pos =pygame.mouse.get_pos()
                row,col = get_glicked_pos(pos,rows,width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None 
                elif spot == end:
                    end =None
            if event.type==pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win,grid,rows,width), grid, start ,end) #lambda is just a function anonymus
                if event.key ==pygame.K_c:
                    start= None
                    end = None
                    grid = make_grid(rows,width)
    
    pygame.quit()
main(win,width)




