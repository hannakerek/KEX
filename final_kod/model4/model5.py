"""
Reinforcement learning maze example.
Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].
This script is the environment part of this example.
The RL is in RL_brain.py.
View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""
import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40   # pixels
MAZE_H = 10  # grid height
MAZE_W = 10 # grid width
height =MAZE_H*UNIT
width =MAZE_W*UNIT
punkter=[]
agentList=[]
goalList=[]


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.action_space)
        self.n_features = 4
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)


        # obstacle
        for i in range(1,3):
            self.punkt = self.canvas.create_rectangle(
                3*UNIT,0*UNIT,4*UNIT,1*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                6*UNIT,0*UNIT,7*UNIT,1*UNIT, fill='red')
            punkter.append(self.punkt)
            
            self.punkt = self.canvas.create_rectangle(
                0*UNIT,3*UNIT,1*UNIT,4*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                3*UNIT,3*UNIT,4*UNIT,4*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                6*UNIT,3*UNIT,7*UNIT,4*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                9*UNIT,3*UNIT,10*UNIT,4*UNIT, fill='red')
            punkter.append(self.punkt)
            
            self.punkt = self.canvas.create_rectangle(
                0*UNIT,6*UNIT,1*UNIT,7*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                3*UNIT,6*UNIT,4*UNIT,7*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                6*UNIT,6*UNIT,7*UNIT,7*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                9*UNIT,6*UNIT,10*UNIT,7*UNIT, fill='red')
            punkter.append(self.punkt)


            self.punkt = self.canvas.create_rectangle(
                3*UNIT,9*UNIT,4*UNIT,10*UNIT, fill='red')
            punkter.append(self.punkt)
            self.punkt = self.canvas.create_rectangle(
                6*UNIT,9*UNIT,7*UNIT,10*UNIT, fill='red')
            punkter.append(self.punkt)


        # create goal
        self.goal1 = self.canvas.create_oval(
            9*UNIT,9*UNIT,10*UNIT,10*UNIT,
            fill='blue')
        goalList.append(self.goal1)

        self.goal2 = self.canvas.create_oval(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill='pink')
        goalList.append(self.goal2)

        # create agent
        self.agent1 = self.canvas.create_rectangle(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill='blue')
        agentList.append(self.agent1)

        self.agent2 = self.canvas.create_rectangle(
            9*UNIT,9*UNIT,10*UNIT,10*UNIT,
            fill='pink')
        agentList.append(self.agent2)

        # pack all
        self.canvas.pack()

    def reset(self,n):
        #self.update()
        #time.sleep(0.01)
        col =['blue','pink','yellow','green']
        self.canvas.delete(agentList[n])

        if n==0:
            self.agent = self.canvas.create_rectangle(
                0*UNIT, 0*UNIT,
                1*UNIT, 1*UNIT,
                fill=col[n])
        if n==1:
            self.agent = self.canvas.create_rectangle(
                9*UNIT, 9*UNIT,
                10*UNIT, 10*UNIT,
                fill=col[n])
        agentList[n] = self.agent


    def current_state(self,n):
        agent = np.array(self.canvas.coords(agentList[n])[:2]) 
        goal = np.array(self.canvas.coords(goalList[n])[:2])

        if n==0: 
            enemy = np.array(self.canvas.coords(agentList[1])[:2])
        if n==1:
            enemy = np.array(self.canvas.coords(agentList[0])[:2])

        #distance=((agent -goal)[0],(agent -goal)[1],(agent -enemy)[0],(agent -enemy)[1])/(MAZE_H*UNIT)
        distance1 = (agent - goal)/(MAZE_H*UNIT)
        distance2 = (agent - enemy)/(MAZE_H*UNIT)
        #print(distance1, distance2)
        distance = np.array([distance2[0], distance2[1],distance1[0],distance1[1]])


        #distance = (np.array(self.canvas.coords(agentList[n])[:2]) 
         #   - np.array(self.canvas.coords(goalList[n])[:2]))/(MAZE_H*UNIT)

        #print("State: ", distance)
        return distance
        

    def step(self, action,n):

        s = self.canvas.coords(agentList[n])
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT or s[1]==UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT or s[0]==UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT or s[0]==UNIT:
                base_action[0] -= UNIT

        self.canvas.move(agentList[n], base_action[0], base_action[1])  # move agent

        next_coords = self.canvas.coords(agentList[n])  # next state

        # reward function

        reward = -0.1
        done = False
        collision = False
        
        for i in range(0, len(punkter)):
            if next_coords in [self.canvas.coords(punkter[i])]:
                reward = -1
                done = False
                #print("HELL")
        if n==0:
            if next_coords in [self.canvas.coords(agentList[1])]:
                reward = -2
                done = False
                #print("collision")
                collision = True
        if n==1:
            if next_coords in [self.canvas.coords(agentList[0])]:
                reward = -2
                done = False
                #print("collision")
                collision=True

        if next_coords == self.canvas.coords(goalList[n]):
            reward = 4
            done = True
            #print("Goal", n+1)


        #s_ = Maze.current_state(action, n)
        return  reward, done, collision

    def render(self):
         #time.sleep(0.01)
         self.update()

