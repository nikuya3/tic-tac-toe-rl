from random import random
from toe import load_parameters, initial_state, initialize_value_table, is_tie, is_win, opponent_move,\
    select_next_step, update_value, save_parameters
from matplotlib import pyplot as plt

tics = [0, 1, 2]  # none, X, O
agent_tic = tics[1]  # RL agent uses X
opponent_tic = tics[2]
empty_tic = tics[0]
value_table = initialize_value_table(str(agent_tic), str(opponent_tic), str(empty_tic), tics)
game_state = initial_state()
epsilon = 0.2
alpha = 0.4
fixed_opponent = True
load = False
results = [0]
wins = 0
losses = 0
draws = 0
episodes = 10000

if load:
    value_table = load_parameters()

while episodes > 0:
    print(game_state)
    if is_win(game_state, str(opponent_tic)):
        print('You have won')
        losses += 1
        results.append(results[-1] - 1)
        episodes -= 1
        game_state = initial_state()
    elif is_win(game_state, str(agent_tic)):
        print('Agent has won')
        wins += 1
        results.append(results[-1] + 1)
        episodes -= 1
        game_state = initial_state()
    elif is_tie(game_state, str(agent_tic), str(opponent_tic), str(empty_tic)):
        print('Tie game')
        draws += 1
        results.append(results[-1])
        episodes -= 1
        game_state = initial_state()
    else:
        game_state = opponent_move(game_state, str(opponent_tic), str(empty_tic), fixed_opponent)
        if str(empty_tic) not in game_state:
            continue
        exploitative = random() > epsilon
        step = select_next_step(game_state, value_table, str(agent_tic), str(empty_tic), exploitative)
        if exploitative or True:
            value_table = update_value(value_table, game_state, step, alpha)
        game_state = step

save_parameters(value_table)
print('Wins:', wins, 'Losses', losses, 'Draws', draws)
plt.plot(results)
plt.xlabel('Episode')
plt.ylabel('Cumulative Reward')
plt.show()
