from model4 import Maze
from DQL4 import DeepQNetwork
import openpyxl
import pandas
import time
import numpy as np



def run_maze():
    
    values =['step','total reward','collison']
    info_lista1 =pandas.DataFrame(columns=values, dtype=np.float64)
    step = 0
    collison = 0
    for episode in range(50000):

        # initial observation
        observation = env.current_state()
        move =0
        reward_total =0
        while True:
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            reward, done, col = env.step(action)
            observation_ = env.current_state()
            reward_total +=reward

            if col == True:
                collison +=1

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            step += 1
            move += 1

            # break while loop when end of this episode
            if done == True:
                env.reset()
                print("episode:", episode, "  step:",move, " reward:", reward_total, collison)
                total = move, reward_total, collison
                info_lista1=info_lista1.append(pandas.Series(total,index=values, name=episode))
                collison = 0
                reward_total = 0
                break

    # end of game
    print('game over')
    writer = pandas.ExcelWriter('/Users/hannakerek/Documents/KTH/KEX/final_kod/model3/Data4.xlsx')
    info_lista1.to_excel(writer,'Sheet1')
    writer.save()
    env.destroy()


if __name__ == "__main__":
    # maze game

    env = Maze()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    env.after(100, run_maze)
    env.mainloop()