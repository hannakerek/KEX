
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
obstacles=[]
agentList=[]
goalList=[]


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['up', 'down', 'left', 'right','stop']
        self.n_actions = len(self.action_space)
        self.n_features = 20
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

        self.obstacle = self.canvas.create_rectangle(3*UNIT,2*UNIT,4*UNIT,3*UNIT, fill='red')
        obstacles.append(self.obstacle)
        self.obstacle = self.canvas.create_rectangle(3*UNIT,3*UNIT,4*UNIT,4*UNIT, fill='red')
        obstacles.append(self.obstacle)
        self.obstacle = self.canvas.create_rectangle(3*UNIT,4*UNIT,4*UNIT,5*UNIT, fill='red')
        obstacles.append(self.obstacle)

        self.obstacle = self.canvas.create_rectangle(6*UNIT,5*UNIT,7*UNIT,6*UNIT, fill='red')
        obstacles.append(self.obstacle)
        self.obstacle = self.canvas.create_rectangle(6*UNIT,6*UNIT,7*UNIT,7*UNIT, fill='red')
        obstacles.append(self.obstacle)
        self.obstacle = self.canvas.create_rectangle(6*UNIT,7*UNIT,7*UNIT,8*UNIT, fill='red')
        obstacles.append(self.obstacle)
  

        col =['blue','pink','yellow','green']

        # create goal
        self.goal = self.canvas.create_oval(
            9*UNIT,9*UNIT,
            10*UNIT,10*UNIT,
            fill=col[0])
        goalList.append(self.goal)

        self.goal = self.canvas.create_oval(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill=col[1])
        goalList.append(self.goal)

        self.goal = self.canvas.create_oval(
            9*UNIT, 0*UNIT,
            10*UNIT, 1*UNIT,
            fill=col[2])
        goalList.append(self.goal)

        self.goal = self.canvas.create_oval(
            0*UNIT, 9*UNIT,
            1*UNIT, 10*UNIT,
            fill=col[3])
        goalList.append(self.goal)



        # create agent
        self.agent = self.canvas.create_rectangle(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill=col[0])
        agentList.append(self.agent)

        self.agent = self.canvas.create_rectangle(
            9*UNIT,9*UNIT,
            10*UNIT,10*UNIT,
            fill=col[1])
        agentList.append(self.agent)

        self.agent = self.canvas.create_rectangle(
            0*UNIT, 9*UNIT,
            1*UNIT, 10*UNIT,
            fill=col[2])
        agentList.append(self.agent)

        self.agent = self.canvas.create_rectangle(
            9*UNIT, 0*UNIT,
            10*UNIT, 1*UNIT,
            fill=col[3])
        agentList.append(self.agent)

        # pack all
        self.canvas.pack()


    def resetAll(self):

        col =['blue','pink','yellow','green']
        
        for n in range(len(agentList)):

            self.canvas.delete(agentList[n])

       
        self.agent = self.canvas.create_rectangle(
            0*UNIT, 0*UNIT,
            1*UNIT, 1*UNIT,
            fill=col[0])
        agentList[0] = self.agent

   
        self.agent = self.canvas.create_rectangle(
            9*UNIT,9*UNIT,
            10*UNIT,10*UNIT,
            fill=col[1])
        agentList[1] = self.agent
    
   
        self.agent = self.canvas.create_rectangle(
            0*UNIT, 9*UNIT,
            1*UNIT, 10*UNIT,
            fill=col[2])
        agentList[2] = self.agent

        self.agent = self.canvas.create_rectangle(
            9*UNIT, 0*UNIT,
            10*UNIT, 1*UNIT,
            fill=col[3])
        agentList[3] = self.agent
        
        


    def current_state(self,n):
        agent = np.array(self.canvas.coords(agentList[n])[:2]) 
        goal = np.array(self.canvas.coords(goalList[n])[:2])

        distance1 = (agent - goal)/(MAZE_H*UNIT)

        distance2 =np.array([0,0,0,0,0,0])
        i=0
        for a in range(len(agentList)):
            if a!= n:
                enemy = np.array(self.canvas.coords(agentList[n])[:2])
                distance2[i] =( agent[0]-enemy[0] )/(MAZE_H*UNIT)
                i +=1
                distance2[i] = (agent[1] - enemy[1])/(MAZE_H*UNIT)
                i +=1

        frozen_enemy = []
        distance3 = []

        distance33 = []
        for j in range(len(obstacles)):
            frozen_enemy.append(np.array(self.canvas.coords(obstacles[j])[:2]))
            distance3 =((agent-frozen_enemy[j] )/(MAZE_H*UNIT))
            distance33.append(distance3[0])
            distance33.append(distance3[1])
     
  


        distance = np.array([distance2[0], distance2[1],distance2[2], distance2[3],
                             distance2[4], distance2[4],distance1[0], distance1[1],
                             distance33[0], distance33[1],distance33[2], distance33[3],
                             distance33[4], distance33[5],distance33[6], distance33[7],
                             distance33[8], distance33[9],distance33[10], distance33[11] ])

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
        collisionAgent = False
        collisionObst = False
        for i in range(0, len(obstacles)):
            if next_coords in [self.canvas.coords(obstacles[i])]:
                reward = -2
                done = False
                collisionObst = True

        for a in range(len(agentList)):
            if a != n:
                if next_coords in [self.canvas.coords(agentList[a])]:
                    reward = -2
                    done = False
                    collisionAgent = True

        if next_coords == self.canvas.coords(goalList[n]):
            reward = 4
            done = True



        return  reward, done, collisionAgent, collisionObst

    def render(self):
         time.sleep(0.01)
         self.update()


