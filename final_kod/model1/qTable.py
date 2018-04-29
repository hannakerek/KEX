import numpy as np
import pandas as panda
import random



# Q(s,a) <-- Q(s,a) + alfa*[reward + gamma*maxQ(s',a')]
#alfa is the learning rate that controls how much the difference between previous and new Q value is considered
#gamma - dicount factor - The discount factor allows us to value short-term reward more than long-term ones
class QTable():
	def __init__(self, actions, learning_rate=0.01, discount_factor=0.9):
		self.actions = actions
		self.alfa = learning_rate
		self.gamma = discount_factor
		self.Qtable = panda.DataFrame(columns=self.actions, dtype=np.float64)

	def addToQtable(self, state):
		if state not in self.Qtable.index:
			lenght = [0]*len(self.actions)
			self.Qtable=self.Qtable.append(
                panda.Series(lenght,index=self.Qtable.columns,name=state))
			#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.html
			#panda.Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)

	def choose_action(self, state):
		self.state = state 
		self.action=None
		action_list=[]
		#check if state exist
		self.addToQtable(state)
		if self.state in self.Qtable.index:
			q = self.Qtable.ix[state] #all possible acction for a given state
			maxq = max(q) #which action gives the largest reward
			for i in range(0,len(q)):
				if q[i]==maxq:
					action_list.append(self.actions[i])
			#check if there is only one acction with the largest reward
			if len(action_list)==1:
				self.action= action_list[0]
			elif len(action_list)>1:
				self.action = random.choice(action_list)
		#print(self.Qtable)
		return self.action


	def printQtable(self):
		print(self.Qtable)




	def updateQTable(self, state, action ,reward, state_):
		#check if the next state is in the Q-table
		self.addToQtable(state_)
		if state_ in self.Qtable.index:
			q =self.Qtable.ix[state_]
			maxq= max(q)
			#update Q-table 
			self.Qtable.loc[state,action] += self.alfa*(reward + self.gamma*maxq)
		# Q(s,a) <-- Q(s,a) + alfa*[reward + gamma*maxQ(s',a')- Q(s,a)]






	


