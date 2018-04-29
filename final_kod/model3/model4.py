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
        self.action_space = ['up', 'down', 'left', 'right','stop']
        self.n_actions = len(self.action_space)
        self.n_features = 14
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
        self.punkt = self.canvas.create_rectangle(
            3*UNIT,2*UNIT,4*UNIT,3*UNIT, fill='red')
        punkter.append(self.punkt)
        self.punkt = self.canvas.create_rectangle(
            3*UNIT,3*UNIT,4*UNIT,4*UNIT, fill='red')
        punkter.append(self.punkt)
        self.punkt = self.canvas.create_rectangle(
            3*UNIT,4*UNIT,4*UNIT,5*UNIT, fill='red')
        punkter.append(self.punkt)

        self.punkt = self.canvas.create_rectangle(
            6*UNIT,5*UNIT,7*UNIT,6*UNIT, fill='red')
        punkter.append(self.punkt)
        self.punkt = self.canvas.create_rectangle(
            6*UNIT,6*UNIT,7*UNIT,7*UNIT, fill='red')
        punkter.append(self.punkt)
        self.punkt = self.canvas.create_rectangle(
            6*UNIT,7*UNIT,7*UNIT,8*UNIT, fill='red')
        punkter.append(self.punkt)



        # create goal
        self.goal1 = self.canvas.create_oval(
            9*UNIT,9*UNIT,10*UNIT,10*UNIT,
            fill='blue')
        goalList.append(self.goal1)

        # create agent
        self.agent1 = self.canvas.create_rectangle(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill='blue')
        agentList.append(self.agent1)

        # pack all
        self.canvas.pack()

    def reset(self):
        #self.update()
        #time.sleep(0.1)
        self.canvas.delete(agentList[0])
        self.agent1 = self.canvas.create_rectangle(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill='blue')
        agentList[0] = self.agent1


    def current_state(self):
        
        agent = np.array(self.canvas.coords(agentList[0])[:2]) 
        goal = np.array(self.canvas.coords(goalList[0])[:2])
        
        frozen_enemy =[]
        distance3 =[]
        distance33 = []
        for j in range(len(punkter)):
            frozen_enemy.append(np.array(self.canvas.coords(punkter[j])[:2]))
            distance3 = ((agent - frozen_enemy[j] )/(MAZE_H*UNIT))
            distance33.append(distance3[0])
            distance33.append(distance3[1])

        distance1 = (agent -goal )/(MAZE_H*UNIT)    

        distance = np.array([distance33[0],distance33[1],distance33[2],distance33[3],distance33[4],distance33[5],
                             distance33[6],distance33[7],distance33[8],distance33[9],distance33[10],distance33[11],
                             distance1[0],distance1[1]])
        return distance



    def step(self, action):

        s = self.canvas.coords(agentList[0])
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
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(agentList[0], base_action[0], base_action[1])  # move agent

        next_coords = self.canvas.coords(agentList[0])  # next state

        # reward function

        reward = -0.1
        done = False
        col = False
        
        if next_coords == self.canvas.coords(goalList[0]):
            reward = 4
            done = True
            
        for i in range(0, len(punkter)):
            if next_coords in [self.canvas.coords(punkter[i])]:
                reward = -2
                done = False
                col = True
                
        #s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(goalList[0])[:2]))/(MAZE_H*UNIT)
        #S_ =np.array([s_[0],s_[1],4])
        return reward, done, col

    def render(self):
         time.sleep(0.01)
         self.update()

