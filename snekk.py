# snake game
import tkinter as tk
import random
from time import sleep, perf_counter
import numpy
import pygame
pygame.init()
screen = pygame.display.set_mode((800,600))

backgroundColor = "#222222"

clock = pygame.time.Clock()
gamewidth = 15
gameheight = 10

def getPixel (x,y,mode):
    global gamewidth
    global gameheight
    screenw = screen.get_width()
    screenh = screen.get_height()
    if(mode=="grid"):
        return (screenw/gamewidth*x,screenh/gameheight*y,screenw/gamewidth,screenh/gameheight)
    if(mode=="ui"):
        return (screenw/gamewidth*x/3,screenh/gameheight*y/3,screenw/gamewidth/3,screenh/gameheight/3)
def metapixel(grid,x,y):
    global screen
    i=0
    for g in grid:
        pygame.draw.rect(screen, g, pygame.Rect(getPixel(
            x*3+(((i)%3)),
            y*3+numpy.floor(i/3),
            "ui")))
        i+=1
keys = {
    "up":False,
    "down":False,
    "left":False,
    "right":False,
    "enter":False
}

class App():
    def __init__(self):
        self.game = {}
        self.game["grid"] = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,"a",0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        self.game["dead"] = False
        self.game["snake"] = {
            "direction":0, # East
            "location":[4,4],
            "length":3
        }
        self.game["speed"] = 1

        self.tics = []

        
        self.applePlaced = True


        self.boxes = []
        # while( not self.game["dead"] ):
    def stdart (self) :
        print("start")
        global gameheight
        global gamewidth
        # Main LooP 
        while not (self.game["dead"]):

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # checking if keydown event happened or not
                if event.type == pygame.KEYDOWN:
                
                    # if keydown event happened
                    # than printing a string to output
                    # print(f"{event.key} key has been pressed")
                    if(event.key == pygame.K_UP) :
                        keys["up"]= True
                    if(event.key == pygame.K_DOWN) :
                        keys["down"]= True
                    if(event.key == pygame.K_LEFT) :
                        keys["left"]= True
                        self.rotate(-1)
                        self.screen(False)
                    if(event.key == pygame.K_RIGHT) :
                        keys["right"]= True
                        self.rotate(1)
                        self.screen(False)
                    if(event.key == pygame.K_KP_ENTER) :
                        keys["enter"]= True
                if event.type == pygame.KEYUP:
                
                    # if keydown event happened
                    # than printing a string to output
                    # print(f"{event.key} key has been pressed")
                    if(event.key == pygame.K_UP) :
                        keys["up"]= False
                    if(event.key == pygame.K_DOWN) :
                        keys["down"]= False
                    if(event.key == pygame.K_LEFT) :
                        keys["left"]= False
                    if(event.key == pygame.K_RIGHT) :
                        keys["right"]= False
                    if(event.key == pygame.K_KP_ENTER) :
                        keys["enter"]= False
            # Draw the screen
            global backgroundColor
            screen.fill(backgroundColor)
            self.gametick()
            pygame.display.flip()
            for x in range(60):
                clock.tick(60)
    def placeApple (self):
        print("place Apple...")
        x = round(random.random()*len(self.game["grid"]))-1
        y = round(random.random()*len(self.game["grid"][x]))-1
        if(self.game["grid"][x][y] == 0):
            self.game["grid"][x][y] = "a"
            self.applePlaced = True
        else:
            print("apple place failed :(")
    def rotate (self, dir):
        print("rotato")
        # dir should be 1 or -1
        if(dir == 1):
            # clockwise
            if self.game["snake"]["direction"] == 3:
                self.game["snake"]["direction"] = 0
            else :
                self.game["snake"]["direction"] += 1
        else:
            # counter-clockwise
            if self.game["snake"]["direction"] == 0:
                self.game["snake"]["direction"] = 3
            else :
                self.game["snake"]["direction"] -= 1
        self.screen(False)
    def screen (self,deplete) :
        global screen
        global gamewidth
        global gameheight
        global backgroundColor
        y=0
        for b in self.game["grid"]:
            lg = "#67fe9a"
            pg = "#0aff25"
            bl = backgroundColor
            # print(b)
            x = 0
            for cell in b:
                if(cell == 0):
                    metapixel([
                        backgroundColor,
                        backgroundColor,
                        backgroundColor,
                        backgroundColor,
                        "#666666",
                        backgroundColor,
                        backgroundColor,
                        backgroundColor,
                        backgroundColor,
                    ],x,y)
                if(cell == "a"):
                    # pygame.draw.rect(screen, "#ff0000", pygame.Rect(getPixel(x,y,"grid")))
                    metapixel([
                        backgroundColor,
                        "#555500",
                        backgroundColor,
                        "#ff0000",
                        "#ff0000",
                        "#ffaaaa",
                        "#bb0000",
                        "#bb0000",
                        "#ff0000"
                    ],x,y)
                else:
                    if(cell > 0):
                        if cell == self.game["snake"]["length"]:
                            heads = [
                                [pg,pg,bl,lg,lg,lg,pg,pg,bl],# right
                                [pg,lg,pg,pg,lg,pg,bl,lg,bl],# down
                                [bl,pg,pg,lg,lg,lg,bl,pg,pg],# left
                                [bl,lg,bl,pg,lg,pg,pg,lg,pg],# right
                            ]
                            metapixel(heads[self.game["snake"]["direction"]],x,y)
                            # pygame.draw.rect(screen, "#aaffaa", pygame.Rect(getPixel(x,y,"grid")))
                        else:
                            # tail segment
                            tail = [pg,pg,pg,pg,lg,pg,pg,pg,pg]
                            tails = [
                                [bl,pg,pg,lg,lg,lg,bl,pg,pg],# tail end right
                                [bl,lg,bl,pg,lg,pg,pg,lg,pg],# tail end down
                                [pg,pg,bl,lg,lg,lg,pg,pg,bl],# tail end left
                                [pg,lg,pg,pg,lg,pg,bl,lg,bl],# tail end up
                                [pg,pg,pg,lg,lg,lg,pg,pg,pg],# tail straight horizontal
                                [pg,lg,pg,pg,lg,pg,pg,lg,pg],# tail straight vertical
                                [pg,pg,pg,pg,lg,lg,pg,lg,pg],# tail curve down - right
                                [pg,pg,pg,lg,lg,pg,pg,lg,pg],# tail curve left - down
                                [pg,lg,pg,lg,lg,pg,pg,pg,pg],# tail curve up   - left
                                [pg,lg,pg,pg,lg,lg,pg,pg,pg],# tail curve right- up
                                [pg,pg,pg,pg,lg,pg,pg,pg,pg],# error!
                            ]
                            tailmpindex = 0
                            next = -1 # directions as head
                            last = -1
                            if(x<gamewidth-1):
                                if ((b[x+1]==cell+1) or (b[x+1]==cell)) and (next == -1):
                                    next = 0
                            if(x>0):
                                if ((b[x-1]==cell+1) or (b[x-1]==cell)) and (next == -1):
                                    next = 2
                            if(y<gameheight-1):
                                if ((self.game["grid"][y+1][x]==cell+1) or (self.game["grid"][y+1][x]==cell)) and (next == -1):
                                    next = 1
                            if(y>1):
                                if ((self.game["grid"][y-1][x]==cell+1) or ((self.game["grid"][y-1][x]==cell))) and (next == -1):
                                    next = 3
                            if not (cell == 1):
                                if(x<gamewidth-1):
                                    if ((b[x+1]==cell-1) or (b[x+1]==cell)) and (last == -1):
                                        last = 0    
                                if(x>0):
                                    if ((b[x-1]==cell-1) or (b[x-1]==cell)) and (last == -1):
                                        last = 2
                                if(y<gameheight-1):
                                    if ((self.game["grid"][y+1][x]==cell-1) or (self.game["grid"][y+1][x]==cell)) and (last == -1):
                                        last = 1
                                if(y>1):
                                    if ((self.game["grid"][y-1][x]==cell-1) or (self.game["grid"][y-1][x]==cell)) and (last == -1):
                                        last = 3
                            tailmpindex = next
                            if last == -1:
                                if not (cell == 1):
                                    tailmpindex = 10
                            else:
                                tailMapGrid = [
                                    [10,6,4,9],
                                    [6,10,7,5],
                                    [4,7,10,8],
                                    [9,5,8,10],
                                ]
                                tailmpindex = tailMapGrid[next][last]
                            tail = tails[tailmpindex]
                            # print("tail", tailmpindex,next,last)
                            # print(f"comparing {cell} to x+ {b[x+1]}, x- {b[x-1]}, y+ {self.game["grid"][y+1][x]}, y- {self.game["grid"][y-1][x]}")
                            metapixel(tail,x,y)
                x+=1
            y+=1
        y=0
        # have deplete on a seperate pass
        for b in self.game["grid"]:
            x = 0
            for cell in b:
                if(cell == "a"):
                    pass
                else:
                    if(cell > 0):
                        if(deplete):
                            self.game["grid"][y][x]-=1
                x+=1
            y+=1
    def gametick (self) :
        print("game tic")
        if(not self.applePlaced):
            self.placeApple()
        directions = [
            [1,0],
            [0,1],
            [-1,0],
            [0,-1]
        ]
        self.game["snake"]["location"][0]+=directions[self.game["snake"]["direction"]][0]
        self.game["snake"]["location"][1]+=directions[self.game["snake"]["direction"]][1]
        if(self.game["snake"]["location"][1]-directions[self.game["snake"]["direction"]][1]>9 or self.game["snake"]["location"][1]-directions[self.game["snake"]["direction"]][1]<0 or self.game["snake"]["location"][0]-directions[self.game["snake"]["direction"]][0]>14 or self.game["snake"]["location"][0]-directions[self.game["snake"]["direction"]][0]<0):
            self.game["dead"]=True
        if not (self.game["dead"]):
            x = self.game['snake']["location"][0] 
            y = self.game['snake']["location"][1]
            if not (self.game["snake"]["location"][1]>9 or self.game["snake"]["location"][1]<0 or self.game["snake"]["location"][0]>14 or self.game["snake"]["location"][0]<0):
                cell = self.game["grid"][y][x]
                if(cell == "a"):
                    self.game['snake']["length"]+=1
                    self.applePlaced = False
                    if(self.game['snake']["length"]%5==0):
                        self.game['speed']
                else:
                    if(cell > 0):
                        self.game["dead"]=True
                self.game["grid"][y][x]=self.game['snake']["length"]    
        self.screen(True)
        dead = tk.Label(text=f"you died. score: {self.game["snake"]["length"]-3}")
        dead.pack()
app = App()
app.stdart()
# pygame.quit()