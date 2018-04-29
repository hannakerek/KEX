from model1 import Model
from qTable import QTable
import time 
import pandas
import numpy as np

m = Model()
Qt = QTable(m.actions)
lives = 50000 #number of times we run the simulation
i=0

values =['step','total reward', 'goal','collisions']
info_lista1 =pandas.DataFrame(columns=values, dtype=np.float64)
live =0
find_goal =0

while True:
	total_reward = 0 #total reward in one loop
	step =0 #total number of steps in one loop
	loop = True
	while loop ==True:
		state=m.current_state()
		action = Qt.choose_action(state)
		m.agent_move(action)
		reward, loop, goal, collision = m.reward()
		total_reward += reward
		state_ = m.current_state()
		Qt.updateQTable(state, action ,reward,state_)
		step += 1

		if goal == True:
			find_goal +=1


		if loop == False:
			break

	m.update()
	time.sleep(0.15)
	m.restart()
	print("loop nr", i, "step  ",step, "reward", total_reward, "goal", goal, "collision:", collision)
	total = step, total_reward, find_goal, collision
	info_lista1=info_lista1.append(pandas.Series(total,index=values, name=live))
	live += 1

	i+=1
	if i > lives:
		Qt.printQtable()
		writer = pandas.ExcelWriter('/Users/hannakerek/Documents/KTH/KEX/final_kod/model1/Data1.xlsx')
		info_lista1.to_excel(writer,'Sheet1')
		writer.save()
		break

m.mainloop()



