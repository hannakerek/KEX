from model2 import Model
from qTable2 import QTable
import time 
import pandas
import numpy as np

m = Model()
Qt = QTable(m.actions)

lives = 500000 #number of times we run the simulation
AgentNumber = 2

#save state/action in case of collision
state = [0,0]
action = [0,0]
reward =[0,0]
step =[0,0]
live=[0,0]
totalLoop = True
total_reward =[0,0]

values =['step','total reward','collison', 'collision_obst']
info_lista1 =pandas.DataFrame(columns=values, dtype=np.float64)
info_lista2 =pandas.DataFrame(columns=values, dtype=np.float64)


while totalLoop == True:

	loopBoth = True
	loop = [True,True]
	myLoop = True

	while myLoop ==True:
	
		for j in range(AgentNumber):
			
			if loop[j]==True:			

				state[j] = m.current_state()
				action[j] = Qt.choose_action(state[j],j)
				agent = m.returnAgent(j)
				m.agent_move(action[j], agent,j)
				goal = m.returnGoal(j)
				reward[j], loop[j], loopBoth, coll_obst = m.reward(agent,goal)
				collision=0
				if coll_obst== True:
					collision = 1
				total_reward[j] += reward[j]
				state_ = m.current_state()

				if loop[j] == False:
					Qt.updateQTable(state[j], action[j], reward[j],state_, j)
					print("Agent ",j+1, "   loop  ",live[j],"step: ",step[j], "reward   ", total_reward[j], "col", collision)
					total = step[j], total_reward[j], 0, collision
					if j ==0 :
							info_lista1=info_lista1.append(pandas.Series(total,index=values, name=live[0]))
					if j==1:
							info_lista2=info_lista2.append(pandas.Series(total,index=values, name=live[1]))
					step[j]=0
					live[j] +=1
					total_reward[j] =0
					if loop[0]==False and loop[1]==False:
						m.restartAll()
						loop=[True,True]

				#when more than one agents collide:
				if loopBoth == False:
					total = step[j], total_reward[j], 1, 0
					if j ==0 :
						info_lista1=info_lista1.append(pandas.Series(total,index=values, name=live[0]))
					if j==1:
						info_lista2=info_lista2.append(pandas.Series(total,index=values, name=live[1]))
					#update current agent and the another agent which collided
					for k in range(AgentNumber):
						reward[k] = reward[j]
						Qt.updateQTable(state[k], action[k] ,reward[k],state_, k)

					print("----------------------------------------------------")
					print("Agent1 ", "   loop  ",live[0] ,"step: ",step[0], "reward   ", total_reward[0])
					print("Agent2 ", "   loop  ",live[1] ,"step: ",step[1], "reward   ", total_reward[1])
					print("----------------------------------------------------")
					if loop[0]==True:
						live[0] +=1
					if loop[1]==True:
						live[1] +=1

					step[0]=0
					step[1]=0
					total_reward[0]=0
					total_reward[1]=0
					antalet_collision_obst =[0,0]
					m.restartAll()
					loop =[True, True]
				
				else:
					Qt.updateQTable(state[j], action[j] ,reward[j],state_, j)
					step[j] +=1
				

		if live[0] > lives and live[1]>lives:
			writer = pandas.ExcelWriter('C:/Users/marta/Desktop/model2final/Data2.xlsx')
			info_lista1.to_excel(writer,'Sheet1')
			info_lista2.to_excel(writer,'Sheet2')
			writer.save()
			totalLoop =False
			break
		

m.mainloop()

