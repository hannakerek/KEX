from model6 import Maze
import time
from DQL6 import DeepQNetwork
import openpyxl
import pandas
import numpy as np


run= 10

def run_maze():
  values =['step','total reward','collisonAgent','collisonObst']
  info_lista1 =pandas.DataFrame(columns=values, dtype=np.float64)
  info_lista2 =pandas.DataFrame(columns=values, dtype=np.float64)
  info_lista3 =pandas.DataFrame(columns=values, dtype=np.float64)
  info_lista4 =pandas.DataFrame(columns=values, dtype=np.float64)

  nr_col_agent =[0,0,0,0]
  nr_col_obst = [0,0,0,0]

  step = [0,0,0,0]
  move =[0,0,0,0]
  reward_total =[0,0,0,0]
  live=[0,0,0,0]
  done=[False,False,False,False]

  while True:

    for agent in range(4): 

      if done[agent] == False:


        #env.render()

        observation = env.current_state(agent)

        # RL choose action based on observation
        action = RL[agent].choose_action(observation)
        # RL take action and get next observation and reward
        reward, done[agent], collisonAgent, collisonObst = env.step(action,agent)
        observation_ = env.current_state(agent)
        reward_total[agent] +=reward
        
        if collisonAgent==True:
          nr_col_agent[agent] +=1

        if collisonObst==True:
          nr_col_obst[agent] +=1

        RL[agent].store_transition(observation, action, reward, observation_)

        if (step[agent] > 200) and (step[agent] % 5 == 0):
            RL[agent].learn()

        step[agent] += 1
        move[agent] += 1


        if done[agent] == True:
            print("Agent",agent+1,"  episode:", live[agent], "  step:",move[agent], " reward:", reward_total[agent], "collision agent:", nr_col_agent[agent], "collision obst:", nr_col_obst[agent])
            total = move[agent], reward_total[agent], nr_col_agent[agent], nr_col_obst[agent]
            if agent==0:
                info_lista1=info_lista1.append(pandas.Series(total,index=values, name=live[0]))
            if agent==1:
                info_lista2=info_lista2.append(pandas.Series(total,index=values, name=live[1]))
            if agent==2:
                info_lista3=info_lista3.append(pandas.Series(total,index=values, name=live[2]))
            if agent==3:
                info_lista4=info_lista4.append(pandas.Series(total,index=values, name=live[3]))
            move[agent]=0
            reward_total[agent]=0
            live[agent] +=1
            nr_col_agent[agent] =0
            nr_col_obst[agent] = 0

        if done[0]==True and done[1]==True and done[2]==True and done[3]==True:
            env.resetAll()
            for i in range(4):
              done[i] = False     

      if live[0] > run and live[1] > run and live[2] > run and live[3]>run :
        print('game over')
        writer = pandas.ExcelWriter('/Users/hannakerek/Documents/KTH/KEX/final_kod/model5/Data6.xlsx')
        info_lista1.to_excel(writer,'Sheet1')
        info_lista2.to_excel(writer,'Sheet2')
        info_lista3.to_excel(writer,'Sheet3')
        info_lista4.to_excel(writer,'Sheet4')
        writer.save()
        env.destroy()
        break 
          

if __name__ == "__main__":
    # maze game

    env = Maze()
    RL1 = DeepQNetwork(0,env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      )

    RL2 = DeepQNetwork(1,env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      )
    RL3 = DeepQNetwork(2,env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      )
    RL4 = DeepQNetwork(3,env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      )
    RL =[RL1,RL2,RL3,RL4]
    env.after(100, run_maze)
    env.mainloop()
  