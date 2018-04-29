dql = xlsread('Data4.xlsx', 'Sheet1');
ql = xlsread('Data1.xlsx', 'Sheet1');


%episodes_agent1 = dql(:,1);
episodes_agent11 = dql(1:1000, 1);
%steps_agent1 = dql(:,2);
steps_agent11= dql(1:1000, 2);
%reward_agent1 = dql(:,3);
reward_agent11 = dql(1:1000, 3);

%episodes_agent2 = ql(:,1);
episodes_agent21 = ql(1:1000, 1);
%steps_agent2 = ql(:,2);
steps_agent21= ql(1:1000, 2);
%reward_agent2 = ql(:,3);
reward_agent21 = ql(1:1000, 3);

subplot(2,1,1)
plot(episodes_agent21, reward_agent21, 'b')
axis([0 1000 -2 5])
set(gca,'FontSize',14);
legend('Q-learning')
xlabel('Episode')
ylabel('Reward')

subplot(2,1,2)
plot(episodes_agent11, reward_agent11, 'r')
set(gca,'FontSize',14);
legend('deep Q-learning')
xlabel('Episode')
ylabel('Reward')

