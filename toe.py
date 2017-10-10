from math import floor
from random import randint, random
from os import listdir, mkdir
from os.path import isdir, join
from pickle import dump, load
from time import time

dump_dir = 'model-dump'


def find(s, ch):
    return [index for index, s_c in enumerate(s) if s_c == ch]


def replace(s, i, c):
    return s[:i] + c + s[i + 1:]


def permutate_all_states(tics):
    # 0: none, 1: X, 2: O
    states = []
    for nr in range(9):
        prev_states = states
        states = []
        for s in range(len(tics)):
            if nr == 0:
                states.append(str(s))
            else:
                temp_prev_states = prev_states.copy()
                for i in range(len(prev_states)):
                    temp_prev_states[i] = temp_prev_states[i] + str(s)
                states.extend(temp_prev_states)
    return states


def is_win(state, tic):
    straight_vert = (state[0] == tic and state[3] == tic and state[6] == tic) \
               or (state[1] == tic and state[4] == tic and state[7] == tic) \
               or (state[2] == tic and state[5] == tic and state[8] == tic)
    straight_hor = (state[0] == tic and state[1] == tic and state[2] == tic) \
                   or (state[3] == tic and state[4] == tic and state[5] == tic) \
                   or (state[6] == tic and state[7] == tic and state[8] == tic)
    diagonal = (state[0] == tic and state[4] == tic and state[8] == tic) \
               or (state[2] == tic and state[4] == tic and state[5] == tic)
    return straight_vert or straight_hor or diagonal


def is_tie(state, empty_tic):
    return empty_tic not in state


def initialize_value_table(agent_tic, tics):
    value_table = {}
    # value_table['222222222'] = 0
    states = permutate_all_states(tics)
    for state in states:
        if is_win(state, str(agent_tic)):
            value_table[state] = 1
        elif is_win(state, '2'):
            value_table[state] = 0
        else:
            value_table[state] = 0.5
    return value_table


def select_next_step(state, value_table, agent_tic, empty_tic, exploitative):
    empty_indices = find(state, empty_tic)
    best_value = 0
    best_step = ''
    best_index = -1
    for i in empty_indices:
        possible_state = state
        possible_state = replace(possible_state, i, agent_tic)
        if value_table[possible_state] >= best_value:
            best_value = value_table[possible_state]
            best_step = possible_state
            best_index = i
    if not exploitative:
        index = best_index
        while index == best_index:
            index_index = randint(0, len(empty_indices) - 1)
            index = empty_indices[index_index]
        best_step = replace(state, index, agent_tic)
    return best_step


def update_value(value_table, prev_state, state, alpha):
    value_table[prev_state] = value_table[prev_state] + alpha * (value_table[state] - value_table[prev_state])
    return value_table


def opponent_move(state, tic, empty_tic, fixed):
    if fixed:
        fixed_opponent_moves = [8, 0, 2, 1]
        index = fixed_opponent_moves[state.count(tic)]
    else:
        index = -1
        while index < 0:
            temp_index = int(input())
            if state[temp_index] == empty_tic:
                index = temp_index
    new_state = state
    new_state = replace(new_state, index, tic)
    return new_state


def initial_state():
    return '000000000'


def save_parameters(value_table):
    if not isdir(dump_dir):
        mkdir(dump_dir)
    filename = 'model_' + str(floor(time())) + '.p'
    path = join(dump_dir, filename)
    with open(path, 'wb') as file:
        dump(value_table, file)


def load_parameters(path=None):
    if path is None:
        if not isdir(dump_dir):
            raise AttributeError('No parameters available')
        filenames = sorted(listdir(dump_dir))
        path = join(dump_dir, filenames[-1])
    with open(path, 'rb') as file:
        return load(file)


tics = [0, 1, 2] # none, X, O
agent_tic = tics[1]  # RL agent uses X
opponent_tic = tics[2]
empty_tic = tics[0]
value_table = initialize_value_table(agent_tic, tics)
game_state = initial_state()
epsilon = 0.2
alpha = 0.5
fixed_opponent = True
wins = 0
losses = 0
draws = 0
episodes = 100000

# value_table = load_parameters()

while episodes > 0:
    print(game_state)
    if is_win(game_state, str(opponent_tic)):
        print('You have won')
        losses += 1
        episodes -= 1
        game_state = initial_state()
    elif is_win(game_state, str(agent_tic)):
        print('Agent has won')
        wins += 1
        episodes -= 1
        game_state = initial_state()
    elif is_tie(game_state, str(empty_tic)):
        print('Tie game')
        draws += 1
        episodes -= 1
        game_state = initial_state()
    else:
        game_state = opponent_move(game_state, str(opponent_tic), str(empty_tic), fixed_opponent)
        if str(empty_tic) not in game_state:
            continue
        exploitative = random() < epsilon
        step = select_next_step(game_state, value_table, str(agent_tic), str(empty_tic), exploitative)
        if exploitative:
            value_table = update_value(value_table, game_state, step, alpha)
        game_state = step

save_parameters(value_table)
print('Wins:', wins, 'Losses', losses, 'Draws', draws)
