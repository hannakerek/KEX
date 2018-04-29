import numpy as np
import time    
import tkinter as tk



#defined variables
size=50#size of one square in the grid
width=10*size 
height=10*size
obstacles=[] # list which shows all "shelves" (red squares)



class Model(tk.Tk, object):
	def __init__(self):
		super(Model, self).__init__()
		self.actions = ['up','down','left','right','stop']
		#build the grid
		self.geometry('500x500')
		self.background = tk.Canvas(self, bg ='white', height= height, width=width)
		for n in range(0, height,size):
			x0=0
			x=width
			y0=n
			y=n
			self.background.create_line(x0,y0,x,y)
		for m in range(0, width,size):
			x0=m
			x=m
			y0=0
			y=height
			self.background.create_line(x0,y0,x,y)
		self._create_objects()
		self.background.pack()
		
	#create shelves, goal and agent
	def _create_objects(self):
		self.obstacle = self.background.create_rectangle(3*size,2*size,4*size,3*size, fill='red')
		obstacles.append(self.obstacle)
		self.obstacle = self.background.create_rectangle(3*size,3*size,4*size,4*size, fill='red')
		obstacles.append(self.obstacle)
		self.obstacle = self.background.create_rectangle(3*size,4*size,4*size,5*size, fill='red')
		obstacles.append(self.obstacle)

		self.obstacle = self.background.create_rectangle(6*size,5*size,7*size,6*size, fill='red')
		obstacles.append(self.obstacle)
		self.obstacle = self.background.create_rectangle(6*size,6*size,7*size,7*size, fill='red')
		obstacles.append(self.obstacle)
		self.obstacle = self.background.create_rectangle(6*size,7*size,7*size,8*size, fill='red')
		obstacles.append(self.obstacle)

		self.goal1 = self.background.create_oval(
            9*size,9*size,10*size,10*size,
            fill='blue')

		self.agent1 = self.background.create_rectangle(
            0*size, 0*size,
            1*size, 1*size,
            fill='blue')



	#convert the current agent position (in list form) to a string form
	#"string form" is used as a state "name"
	def current_state(self):
		agent1_positions= self.background.coords(self.agent1)
		agent1_state = ''.join(str(i) for i in agent1_positions)
		return agent1_state


	#move agent to the next state
	def agent_move(self,do_action):
		agent1_positions= self.background.coords(self.agent1)
		make_move = [0,0]
		if do_action == self.actions[0]: #up
			if agent1_positions[1] > size:
				make_move = [0,-size]
		elif  do_action == self.actions[1]: #down
			if agent1_positions[1] < (height-size):
				make_move = [0,size]
		elif  do_action == self.actions[2]: #left
			if agent1_positions[0] > size :
				make_move = [-size,0]
		elif  do_action == self.actions[3]: #right
			if agent1_positions[0] < (width -size):
				make_move = [size,0]
		self.background.move(self.agent1, make_move[0],make_move[1])


	#reward function gives reward for each step 
	#and restarts simulation when agent reaches goal or go in the red squares
	def reward(self):
		
		s1_= self.background.coords(self.agent1)
		reward = -0.1

		loop =True
		goal = False
		collision = 0
		for i in range(len(obstacles)):
			if s1_ == self.background.coords(obstacles[i]):
				reward = -2
				loop = False
				collision = 1
		if s1_ == self.background.coords(self.goal1):
			reward = 4
			loop = False
			goal = True
		return (reward, loop, goal, collision)

	#restart the model to the first stage
	def restart(self):
		self.background.delete(self.agent1)
		self.agent1 = self.background.create_oval(
			0,0,size,size,fill='blue')
		self.agent2 = self.background.create_oval(
			width,height,width,height,fill='pink')	



