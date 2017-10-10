import numpy as np


def permutate_all_states():
    # 0: none, 1: X, 2: O
    states = []
    for nr in range(9):
        prev_states = states
        states = []
        for s in range(3):
            if nr == 0:
                states.append(str(s))
            else:
                temp_prev_states = prev_states.copy()
                for i in range(len(prev_states)):
                    temp_prev_states[i] = temp_prev_states[i] + str(s)
                states.extend(temp_prev_states)
    return states

value_table = {}
# value_table['222222222'] = 0
states = permutate_all_states()
for state in states:
    value_table[state] = 0.5