agent1 = xlsread('Data.xlsx', 'Sheet1');
agent2 =xlsread('Data.xlsx', 'Sheet2');


lives_agent1 = agent1(:,1);
lives_agent11 = agent1(1:200, 1);
steps_agent1 = agent1(:,2);
steps_agent11= agent1(1:200, 2);
reward_agent1 = agent1(:,3);
reward_agent11 = agent1(1:200, 3);

lives_agent2 = agent2(:,1);
lives_agent22 = agent2(1:200, 1);
steps_agent2 = agent2(:,2);
steps_agent22= agent2(1:200, 2);
reward_agent2 = agent2(:,3);
reward_agent22 = agent2(1:200, 3);

figure(1)
plot(lives_agent1, steps_agent1, 'b')
hold on
plot(lives_agent1, reward_agent1, 'c')
figure(2)
plot(lives_agent2, steps_agent2, 'g')
hold on
plot(lives_agent2, reward_agent2, 'r')