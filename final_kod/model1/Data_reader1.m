agent1 = xlsread('Data1.xlsx', 'Sheet1');



lives_agent1 = agent1(:,1);
lives_agent11 = agent1(1:2000, 1);
steps_agent1 = agent1(:,2);
steps_agent11= agent1(1:2000, 2);
reward_agent1 = agent1(:,3);
reward_agent11 = agent1(1:2000, 3);




plot(lives_agent11, steps_agent11, 'b')
hold on
plot(lives_agent11, reward_agent11, 'r')

