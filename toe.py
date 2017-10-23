from math import floor
from random import randint
from os import listdir, mkdir
from os.path import isdir, join
from pickle import dump, load
from strext import find, replace
from time import time


dump_dir = 'model-dump'


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
               or (state[2] == tic and state[4] == tic and state[6] == tic)
    return straight_vert or straight_hor or diagonal


def is_tie(state, agent_tic, opponent_tic, empty_tic):
    return empty_tic not in state or is_win(state, agent_tic) and is_win(state, opponent_tic)


def initialize_value_table(agent_tic, opponent_tic, empty_tic, tics):
    value_table = {}
    # value_table['222222222'] = 0
    states = permutate_all_states(tics)
    for state in states:
        if is_tie(state, agent_tic, opponent_tic, empty_tic):
            value_table[state] = 0
        elif is_win(state, opponent_tic):
            value_table[state] = -1
        elif is_win(state, agent_tic):
            value_table[state] = 1
        else:
            value_table[state] = 0.5
    return value_table


def select_next_step(state, value_table, agent_tic, empty_tic, exploitative):
    empty_indices = find(state, empty_tic)
    values = []
    possible_states = []
    best_value = 0
    best_step = ''
    best_index = -1
    for i in empty_indices:
        possible_state = state
        possible_state = replace(possible_state, i, agent_tic)
        values.append(value_table[possible_state])
        possible_states.append(possible_state)
        # if value_table[possible_state] >= best_value:
        #     best_value = value_table[possible_state]
        #     best_step = possible_state
        #     best_index = i
    best_value = max(values)
    indices = [i for i in range(len(values)) if values[i] == best_value]
    indices_index = randint(0, len(indices) - 1)
    best_index = indices[indices_index]
    best_step = possible_states[indices[indices_index]]

    if not exploitative:
        index = best_index
        while index == best_index:
            index_index = randint(0, len(empty_indices) - 1)
            index = empty_indices[index_index]
        best_step = replace(state, index, agent_tic)
    return best_step


def update_value(value_table, prev_state, state, alpha):
    value_table[prev_state] = value_table[prev_state] + alpha * (value_table[state] - value_table[prev_state])
    # print(value_table[prev_state])
    # print(value_table[state])
    return value_table


def opponent_move(state, tic, empty_tic, fixed):
    if fixed:
        fixed_opponent_moves = [[8, 0, 2, 6, 1], [0, 4, 5, 8], [0, 1, 3, 2], [2, 4, 5, 8]]
        moveset_i = randint(0, len(fixed_opponent_moves) - 1)
        index = fixed_opponent_moves[0][state.count(tic)]
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
