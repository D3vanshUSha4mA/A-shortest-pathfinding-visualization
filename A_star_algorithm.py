import pygame
import math
from queue import PriorityQueue

WIDTH=800
WIN=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)
YELLOW    = (255, 255, 0)
WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
PURPLE    = (128, 0, 128)
ORANGE    = (255, 165, 0)
GREY      = (128, 128, 128)
TURQUOISE = (64, 224, 208)



class Spot:                                                              #represents each cell in the grid......
    def __init__(self,row,col,width,total_rows):
        self.row=row                                                     #grid coordinates....
        self.col=col
        self.x=width*row                                                 #pixel coordinates for drawing.....  
        self.y=width*col
        self.color=WHITE
        self.neighbours=[]                                               #list of valid(white) neighbours
        self.width=width
        self.total_rows=total_rows
    def get_pos(self):
        return self.row,self.col
    def is_closed(self):                    #already visited
        return self.color==RED
    def is_open(self):                      #in the queue,not visited yet
        return self.color==GREEN
    def is_barrier(self):                   #not walkable
        return self.color==BLACK
    def is_start(self):                     #starting point
        return self.color==ORANGE
    def is_end(self):                       #ending point
        return self.color==TURQUOISE
    def reset(self):
        self.color=WHITE
    def make_start(self):
        self.color=ORANGE
    def make_closed(self):
        self.color=RED
    def make_open(self):
        self.color=GREEN
    def make_barrier(self):
        self.color=BLACK
    def make_end(self):
        self.color=TURQUOISE
    def make_path(self):
        self.color=PURPLE
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    def update_neighbours(self,grid):                                  #resets the neighbours list.....ensures only valid ones go to the list...
        self.neighbours=[]
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbours.append(grid[self.row+1][self.col])
        
        if self.row>0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbours.append(grid[self.row-1][self.col])
        
        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbours.append(grid[self.row][self.col+1])
        
        if self.col>0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbours.append(grid[self.row][self.col-1])
        

    def __lt__(self,other):
        return False
def h(p1,p2):                  #Heuristic function-Manhattan Distance....
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)
def reconstruct_path(came_from,current,draw):       #backtrack from the end node to the start node using came_from dictionary and colour the path purple
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()



def algorithm(draw,grid,start,end):
    count=0                                        #prevents error when f_score of two spots are same.....
    open_set=PriorityQueue()                       #This queue holds the next nodes to be visited....it is sorted by (f_score,count) so lowest cost node is chosen...
    open_set.put((0,count,start))                  #start node with f score as zero...
    came_from={}                                   #dictionary to keep track of path...
    g_score={spot:float("inf") for row in grid for spot in row}       #actual cost to reach a spot from the start...intially everything is unreachable(infinity)...
    g_score[start]=0                                #cost to reach itself is zero....
    f_score={spot:float("inf") for row in grid for spot in row}     #f_score=(g_score+heuristic)....
    f_score[start]=h(start.get_pos(),end.get_pos())
    open_set_hash={start}                          #track what's currently inside open_set.....
    while not open_set.empty():                    #as long as there are nodes lefto explore
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]               #picks the node with lowest f_score from priority queue...
        open_set_hash.remove(current)             #removes it from the hash set...
        if current==end:                          #if the end node is reached construct the path...
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True
        for neighbour in current.neighbours:       #explore neighbours
            temp_g_score=g_score[current]+1        #cost to move to a neighbour
            if temp_g_score < g_score[neighbour]:  #if better path
                came_from[neighbour]=current       #update path
                g_score[neighbour]=temp_g_score    #update cost
                f_score[neighbour]=temp_g_score+h(neighbour.get_pos(),end.get_pos())    #f_score
                if neighbour not in open_set_hash:  #if not is open_set already
                    count+=1
                    open_set.put((f_score[neighbour],count,neighbour)) #add to queue 
                    open_set_hash.add(neighbour)                       #add to hash_set
                    neighbour.make_open()                              #make it open
        draw()                   

        if(current!=start):
            current.make_closed()
    return False




def make_grid(rows,width):
    grid=[]
    gap=width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid
def draw_grid(win,rows,width):
    gap=width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))
def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap=width//rows
    y,x=pos
    row=y//gap
    col=x//gap
    return row,col
def main(win,width):
    ROWS=50
    grid=make_grid(ROWS,width)
    start=None
    end=None
    run=True
    started=False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
             
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width) 
                spot=grid[row][col]
                if not start and spot!=end:
                    start=spot
                    start.make_start()
                elif not end and spot!=start:
                    end=spot
                    end.make_end()
                elif spot!=end and spot!=start:
                    spot.make_barrier() 
                    

            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                spot.reset()
                if spot==start:
                    start=None
                elif spot==end:
                    end=None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid);
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
                if event.key == pygame.K_c:
                    start=None
                    end=None
                    grid=make_grid(ROWS,width)

    pygame.quit()
main(WIN,WIDTH)

