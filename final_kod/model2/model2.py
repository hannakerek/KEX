import numpy as np
import time    
import tkinter as tk



#defined global variables
size=50 #size of one square in the grid
width=10*size 
height=10*size
punkter=[] # list which shows all "shelves" (red squares)
agentList=[] #list with all agents
goalList=[] #list with all goals
agentNumber =2 #number of agents

class Model(tk.Tk, object):
	def __init__(self):
		super(Model, self).__init__()
		self.actions = ['up1','down1','left1','right1','stop1','up2','down2','left2','right2','stop2']
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
		#shelves:
		self.punkt = self.background.create_rectangle(
            3*size,2*size,4*size,3*size, fill='red')
		punkter.append(self.punkt)
		self.punkt = self.background.create_rectangle(
            3*size,3*size,4*size,4*size, fill='red')
		punkter.append(self.punkt)
		self.punkt = self.background.create_rectangle(
            3*size,4*size,4*size,5*size, fill='red')
		punkter.append(self.punkt)
		self.punkt = self.background.create_rectangle(
            6*size,5*size,7*size,6*size, fill='red')
		punkter.append(self.punkt)
		self.punkt = self.background.create_rectangle(
            6*size,6*size,7*size,7*size, fill='red')
		punkter.append(self.punkt)
		self.punkt = self.background.create_rectangle(
            6*size,7*size,7*size,8*size, fill='red')
		punkter.append(self.punkt)

		self.goal1 = self.background.create_oval(
            9*size,9*size,10*size,10*size,
            fill='blue')
		goalList.append(self.goal1)

		self.goal2 = self.background.create_oval(
			0*size,0*size,1*size,1*size,fill='pink') #behövs inte i model1
		goalList.append(self.goal2)

		# create agent
		self.agent = self.background.create_rectangle(
            0*size, 0*size,
            1*size, 1*size,
            fill='blue')
		agentList.append(self.agent)

		self.agent = self.background.create_rectangle(
			9*size,9*size,10*size,10*size,fill='pink')	
		agentList.append(self.agent)



	def returnAgent(self, num):
		return agentList[num]

	def returnGoal(self, num):
		return goalList[num]


	#convert the current agent position (in list form) to a string form
	#"string form" is used as a state "name"
	def current_state(self):
		agent1_positions= self.background.coords(agentList[0])
		#agent1_state = ''.join(str(i) for i in agent1_positions)
		agent2_positions= self.background.coords(agentList[1])
		#agent2_state = ''.join(str(i) for i in agent2_positions)
		agent_state = ''.join(str(i) for i in agent1_positions)
		agent_state = agent_state + ''.join(str(i) for i in agent2_positions)
		return agent_state

	#move agent to the next state
	def agent_move(self,do_action, agent,n):

		self.agent = agent
		#time.sleep so that we can see the movement
		#time.sleep(0.1)
		#update the model
		#self.update()
		agent_positions= self.background.coords(self.agent)
		make_move = [0,0]
		if do_action == self.actions[n*5]: #up
			if agent_positions[1] > size or agent_positions[1]== size :
				make_move = [0,-size]
		elif  do_action == self.actions[n*5 +1]: #down
			if agent_positions[1] < (height-size): #or agent_positions[1]== (height-size) :
				make_move = [0,size]
		elif  do_action == self.actions[n*5 +2]: #left
			if agent_positions[0] > size or agent_positions[0]== size:
				make_move = [-size,0]
		elif  do_action == self.actions[n*5 +3]: #right
			if agent_positions[0] < (width -size): # or agent_positions[0]== (width-size):
				make_move = [size,0]
		elif  do_action == self.actions[n*5 + 4]: #stop
				make_move = [0,0]
		self.background.move(self.agent, make_move[0],make_move[1])


	#reward function gives reward for each step 
	#and restarts simulation when agent reaches goal or go in the red squares
	def reward(self,agent,goal):
		
		self.goal = goal
		loopBoth =True
		coll_obst = False
		#next state/ use after agent_move()
		s_= self.background.coords(self.agent)
		reward = -0.1
		loop =True

		for i in range(0,len(punkter)):
			if s_ == self.background.coords(punkter[i]):
				reward = -2
				loop = False
				coll_obst = True
		if s_ == self.background.coords(goal):
			reward = 4
			loop = False

		#check if agents crossed
		pos =[]
		for i in range(len(agentList)):
			pos.append(self.background.coords(agentList[i]))

		if pos[0]==pos[1]:
			reward = -2
			loop = True #collision is more important
			loopBoth = False

		return (reward, loop, loopBoth, coll_obst)
		


	#restart the model to the first stage
	def restartAll(self):
		#delete the old agent and create the new one
		self.background.delete(agentList[0])
		self.background.delete(agentList[1])

		self.agent = self.background.create_rectangle(
            0*size, 0*size,
            1*size, 1*size,
            fill='blue')
		agentList[0]= self.agent

		self.agent = self.background.create_rectangle(
			9*size,9*size,10*size,10*size,fill='pink')	
		agentList[1]= self.agent



	#restart only one of the agents
	def restart(self, agent, n):
		self.agent = agent
		self.background.delete(self.agent)
		if n==0:
			self.agent = self.background.create_rectangle(
            0*size, 0*size,1*size, 1*size,fill='blue')
		if n==1:
			self.agent = self.background.create_rectangle(
				9*size,9*size,10*size,10*size,fill='pink')	
		agentList[n] =self.agent
		


