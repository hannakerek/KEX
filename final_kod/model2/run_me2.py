from model2 import Model
from qTable2 import QTable
import time 
import pandas
import numpy as np


m = Model()
Qt = QTable(m.actions)

lives = 10000 #number of times we run the simulation
AgentNumber = 2
live = [] #saves number of loops/lives
step = [] #saves number of steps in each loop
reward = [] #total reward in one loop
nrCollisions = []
nrGoal = []
findGoal = []


#save state/action in case of collision
state = []
action = []

values =['step','total reward','collison','goal']
info_lista1 =pandas.DataFrame(columns=values, dtype=np.float64)
info_lista2 =pandas.DataFrame(columns=values, dtype=np.float64)

for a in range(0,AgentNumber):
	reward.append(0)
	step.append(0)
	live.append(0)
	nrCollisions.append(0)
	nrGoal.append(0)
	findGoal.append(False)

totalLoop = True


while totalLoop == True:

	loopBoth = True
	loop = [True,True]
	myLoop = True

	while myLoop ==True:
	
		for j in range(AgentNumber):

			if len(state)<2:
				state_nu = m.current_state()
				state.append(state_nu)
				action_nu = Qt.choose_action(state_nu,j)
				action.append(action_nu)
			else:
				state[j] = m.current_state()
				action[j] = Qt.choose_action(state[j],j)

			agent = m.returnAgent(j)
			m.agent_move(action[j], agent,j)
			goal = m.returnGoal(j)
			reward[j], loop[j], loopBoth, findGoal[j] = m.reward(agent,goal)
			#time.sleep(0.01)
			state_ = m.current_state()
			if findGoal[j]==True:
				nrGoal[j] += 1

			#m.update()
			#time.sleep(0.15)
			#Qt.updateQTable(state, action, reward[j],state_, j)
			#when one agent collide with the red square/reach the goal
			if loop[j] == False:
				Qt.updateQTable(state[j], action[j], reward[j],state_, j)
				m.update()
				time.sleep(0.15)
				live[j] +=1
				print("Agent ",j+1, "   loop  ",live[j],"step: ",step[j], "reward   ", reward[j])
				step[j]=0
				m.restart(agent,j)

			#when more than one agents collide:
			elif loopBoth == False:
				#update current agent and the another agent which collided
				for k in range(AgentNumber):
					reward[k] = reward[j]
					#condition if not filed yet?/althought imposible case 
					Qt.updateQTable(state[k], action[k] ,reward[k],state_, k)
				
				m.update()
				time.sleep(0.15)
				live[1] +=1
				live[0] +=1
				print("----------------------------------------------------")
				print("Agent1 ", "   loop  ",live[0] ,"step: ",step[0], "reward   ", reward[0])
				print("Agent2 ", "   loop  ",live[1] ,"step: ",step[1], "reward   ", reward[1])
				print("----------------------------------------------------")
				step[0]=0
				step[1]=0
				m.restartAll()
			
			else:
				Qt.updateQTable(state[j], action[j] ,reward[j],state_, j)
				#counts steps
				step[j] +=1
				m.update()

		
		if live[0]==1000:
			#prints Qtable after agent1 did 1000 loops
			Qt.printQtable()
			writer = pandas.ExcelWriter('/Users/hannakerek/Documents/KTH/KEX/final_kod/model2/Data.xlsx')
			info_lista1.to_excel(writer,'Sheet1')
			info_lista2.to_excel(writer,'Sheet2')
			writer.save()
			totalLoop =False
			break
		

m.mainloop()