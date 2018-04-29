from model5 import Maze
from DQL5 import DeepQNetwork
import openpyxl
import pandas
import numpy as np


run= 10000

def run_maze():
    values =['step','total reward','collison']
    info_lista1 =pandas.DataFrame(columns=values, dtype=np.float64)
    info_lista2 =pandas.DataFrame(columns=values, dtype=np.float64)

    anatalet_col =[0,0]

    step = [0,0]
    move =[0,0]
    reward_total =[0,0]
    live=[0,0]

        
    while True:

        for agent in range(2):
            #fresh env
            #env.render()
            observation = env.current_state(agent)

            # RL choose action based on observation
            action = RL[agent].choose_action(observation)
            # RL take action and get next observation and reward
            reward, done, collison = env.step(action,agent)
            observation_ = env.current_state(agent)
            reward_total[agent] +=reward
            
            if collison==True:
              anatalet_col[agent] +=1

            RL[agent].store_transition(observation, action, reward, observation_)

            if (step[agent] > 200) and (step[agent] % 5 == 0):
                RL[agent].learn()

            # swap observation
            #observation = observation_
            step[agent] += 1
            move[agent] += 1


            if done == True:
                print("Agent",agent+1,"  episode:", live[agent], "  step:",move[agent], " reward:", reward_total[agent], "Collision", anatalet_col[agent])
                total = move[agent], reward_total[agent], anatalet_col[agent]
                if agent==0:
                    info_lista1=info_lista1.append(pandas.Series(total,index=values, name=live[0]))
                if agent==1:
                    info_lista2=info_lista2.append(pandas.Series(total,index=values, name=live[1]))
                move[agent]=0
                reward_total[agent]=0
                env.reset(agent)
                live[agent] +=1
                

        if live[0] > run and live[1] > run :
            break 
            

    # end of game
    print('game over')
    writer = pandas.ExcelWriter('C:/Users/marta/Desktop/model5final/Data.xlsx')
    info_lista1.to_excel(writer,'Sheet1')
    info_lista2.to_excel(writer,'Sheet2')
    writer.save()
    env.destroy()


if __name__ == "__main__":
    # maze game

    env = Maze()
    RL1 = DeepQNetwork(0,env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )

    RL2 = DeepQNetwork(1,env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    RL =[RL1,RL2]
    env.after(100, run_maze)
    env.mainloop()
    #RL.plot_cost()