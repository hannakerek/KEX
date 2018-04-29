import numpy as np
import pandas as panda
import random
import scipy.io
import matplotlib as plt
import openpyxl #needed to be able to save the data to Excel



numberOfAgents=2 #number of agents we want to have moving on the grid

# Q(s,a) <-- Q(s,a) + alfa*[reward + gamma*maxQ(s',a')]
#alfa is the learning rate that controls how much the difference between previous and new Q value is considered
#gamma - dicount factor - The discount factor allows us to value short-term reward more than long-term ones

#create Qtable
class QTable():
	def __init__(self, actions, learning_rate=0.01, discount_factor=0.9):
		self.actions = actions
		self.alfa = learning_rate
		self.gamma = discount_factor
		self.Qtable = panda.DataFrame(columns=self.actions, dtype=np.float64)

	#add a state to Qtable if it is not there yet
	def addToQtable(self, state):
		if state not in self.Qtable.index:
			lenght = [0]*len(self.actions)
			self.Qtable=self.Qtable.append(
                panda.Series(lenght,index=self.Qtable.columns,name=state))
			#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html
			#panda.Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)

	#choose one of the avaiable actions
	def choose_action(self, state, currentAgentNumber):
		self.state = state 
		self.action = None
		self.currentAgentNumber =currentAgentNumber
		action_list=[]
		#check if state exist
		self.addToQtable(state)
		if self.state in self.Qtable.index:
			q = self.Qtable.ix[state] #all possible acction for a given state
			slut = 5 * (currentAgentNumber + 1)
			start = slut - 5
			q_new = q[start:slut]
			maxq = max(q_new) #which action gives the largest reward
			for i in range(0,len(q_new)):
				if q_new[i]==maxq:
					action_list.append(self.actions[i+(5*currentAgentNumber)])
			#check if there is only one acction with the largest reward
			if len(action_list)==1:
				self.action= action_list[0]
			elif len(action_list)>1:
				self.action = random.choice(action_list)
	
		#print(self.Qtable) 
		return self.action

	def printQtable(self):
		#saves Qtable to an Excel file:
		'''
		writer = panda.ExcelWriter('C:/Users/marta/Desktop/QtableEx.xlsx')
		self.Qtable.to_excel(writer,'Sheet1')
		writer.save()
		'''
		#prints Qtable
		print(self.Qtable)


	def updateQTable(self, state, action ,reward, state_,agentNumber):
		#check if the next state is in the Q-table
		self.addToQtable(state_)
		if state_ in self.Qtable.index:
			q =self.Qtable.ix[state_]
			slut = 5* (agentNumber +1)
			start = slut -5
			#choose only from action which are associated with the given agent
			q = q[start:slut]
			maxq= max(q)
			#update Q-table 
			self.Qtable.loc[state,action] += self.alfa*(reward + self.gamma*maxq)
			# Q(s,a) <-- Q(s,a) + alfa*[reward + gamma*maxQ(s',a')- Q(s,a)]
