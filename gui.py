from random import random
from strext import replace
from toe import load_parameters, initial_state, initialize_value_table, is_tie, is_win, select_next_step, update_value, save_parameters
import tkinter as tk


tics = [0, 1, 2]  # none, X, O
agent_tic = tics[1]  # RL agent uses X
opponent_tic = tics[2]
empty_tic = tics[0]
value_table = initialize_value_table(agent_tic, tics)
epsilon = 0.1
alpha = 0.8
load = False

if load:
    value_table = load_parameters()


class MyApp(tk.Tk):
    temp_state = ''
    tmp_empty_tic = ''
    tmp_player_tic = ''
    episodes = 1000
    wins = 0
    losses = 0
    draws = 0
    game_state = initial_state()

    def __init__(self):
        """ initialize the frame and widgets"""
        tk.Tk.__init__(self)
        fr = tk.Frame(self)
        self.player_turn = True
        self.quit = tk.Button(self, text='-',
                              command=self.quit_game,
                              relief=tk.RAISED, height=3,
                              width=7, font=('Helvetica', 24))
        self.buttons = []
        self.desc_label = tk.Label(self, text='Your turn')
        self.episodes = tk.IntVar()
        self.episodes.set(100)
        self.episodes_label = tk.Label(self, textvariable=self.episodes)

        # use a loop to build my field buttons
        for i in range(9):
            button = tk.Button(self, text=str(i),
                               command=lambda j=i: self.do_button(j),
                               relief=tk.RAISED, height=3,
                               width=7, font=('Helvetica', 24))
            self.buttons.append(button)
        # grid everything into the frame
        fr.grid()

        # use a loop to grid the field buttons
        myL = [[0, 2, 0], [1, 2, 1], [2, 2, 2],  # button number, row, column
               [3, 3, 0], [4, 3, 1], [5, 3, 2],
               [6, 4, 0], [7, 4, 1], [8, 4, 2]]
        for i in myL:
            self.buttons[i[0]].grid(row=i[1], column=i[2])
        self.desc_label.grid(row=5, column=0)
        self.episodes_label.grid(row=5, column=1)

    def do_button(self, i):
        global value_table, empty_tic, opponent_tic, agent_tic
        if self.player_turn and self.episodes.get() > 0:
            if self.game_state[i] == str(empty_tic):
                self.game_state = replace(self.game_state, i, str(opponent_tic))
                self.buttons[i]['text'] = 'X'
                self.player_turn = False
                if is_win(self.game_state, str(opponent_tic)):
                    self.desc_label['text'] = 'You have won'
                    self.losses += 1
                    self.episodes.set(self.episodes.get() - 1)
                    self.game_state = initial_state()
                elif is_tie(self.game_state, str(empty_tic)):
                    self.desc_label['text'] = 'Tie game'
                    self.draws += 1
                    self.episodes.set(self.episodes.get() - 1)
                    self.game_state = initial_state()
                else:
                    exploitative = random() > epsilon
                    step = select_next_step(self.game_state, value_table, str(agent_tic), str(empty_tic), exploitative)
                    if exploitative:
                        value_table = update_value(value_table, self.game_state, step, alpha)
                    self.game_state = step
                    if is_win(self.game_state, str(agent_tic)):
                        self.desc_label['text'] = 'Agent has won'
                        self.wins += 1
                        self.episodes.set(self.episodes.get() - 1)
                        self.game_state = initial_state()
                self.set_state(self.game_state)
                self.player_turn = True
        else:
            self.quit_game()

    def player_move(self, state, tic, empty_tic, fixed):
        self.temp_state = state
        self.tmp_empty_tic = empty_tic
        self.tmp_player_tic = tic
        self.desc_label.text = 'Your turn'
        if fixed:
            fixed_opponent_moves = [8, 0, 2, 1]
            index = fixed_opponent_moves[state.count(tic)]
            self.temp_state = replace(self.temp_state, index, tic)
        else:
            self.player_turn = True

    def set_state(self, state):
        for i in range(len(state)):
            if state[i] == '0':
                self.buttons[i]['text'] = '-'
            elif state[i] == '1':
                self.buttons[i]['text'] = 'O'
            elif state[i] == '2':
                self.buttons[i]['text'] = 'X'

    def quit_game(self):
        save_parameters(value_table)
        self.destroy()


root = MyApp()
root.title("Tic Tac Toe RL")
root.mainloop()
