# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 16:11:04 2016

@author: shengquan
"""

from keras.models import Sequential
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.noise import GaussianNoise
from keras.optimizers import SGD, Adam, Adamax
from keras.callbacks import EarlyStopping

import numpy as np
#import random

import connectfour as cf

import minimax_ai as mini_ai

#create the dnn player
model = Sequential()
    
layers = [
    Dense(256, init='lecun_uniform', input_shape=(42*3,)), Activation('relu'), Dropout(0.5),
    Dense(200, init='lecun_uniform'), Activation('relu'), Dropout(0.5),
    Dense(100, init='lecun_uniform'), Activation('relu'), Dropout(0.5),
    Dense(7, init='lecun_uniform'), Activation('linear')
]
    
for layer in layers:
    model.add(layer)
    
model.compile(loss='mse', optimizer='rmsprop')
    
def train_dnn_player():    
    
    #start reinforcement learning
    epochs = 15 #no of rounds
    gamma = 0.9 #discount factor
    epsilon = 1 #exploitation vs exploration
    
    for i in range(epochs):        
        #start a new game        
        state = cf.init_game() #state: (board, status)
        print ('Game #: {}'.format(i))
        
        while state[1] == 'ongoing':
            #dnn_player makes it move based on q-learning
            print "board before dnn player:"
            print state[0]
            
            qval = model.predict(reshape_board(state[0]), batch_size=1)            
            if np.random.random() < epsilon:
                action = np.random.randint(0,7)
            else:
                action = np.argmax(qval)
            
            new_state = cf.make_move(state[0], action, True) #(board, col, first_player?)

            #get the reward for the new state
            reward = cf.get_reward(new_state[1])
            
            #let the trainer AI make the move
            # state_after_opponent_move = constant_AI_make_move(new_state[0])
            state_after_opponent_move = cf.make_move(new_state[0], mini_ai.minimax(new_state[0], False), False)
            #human_make_move(new_state[0])
            
            #get the q-function after the move and get the reward for the best move thereafter
            newQ = model.predict(reshape_board(state_after_opponent_move[0]), batch_size=1)
            maxQ = np.max(newQ)
            y = np.zeros((1,7))
            y[:] = qval[:]
            
            if new_state[1] == 'ongoing': #if not a winning move, have to add a discounted maxQ
                update = (reward + gamma * maxQ)
            else: #if won then just add reward, because no further maxQ
                update = reward
            
            y[0][action] = update
            
            #update the model
            model.fit(reshape_board(state[0]), y, batch_size=1, nb_epoch=1, verbose=1)
            
            #update the state
            state = state_after_opponent_move
        
        if epsilon > 0.1:
            epsilon -= (1 / epochs)


def human_make_move(board):
    #makes move and return the new state
    print "board before human move:"
    print board
    return cf.make_move(board, input("Enter cols 1 to 7 as your next move: ")-1, False)
    
def constant_AI_make_move(board):
    print "board before constant_AI:"
    print board
    return cf.make_move(board, 1, False)
    
def reshape_board(board):
    board = board.reshape(1,42)
    
    new_board = []
    for block in board[0]:
        if block == -1:
            new_board.append([1,0,0])
        elif block == 0:
            new_board.append([0,1,0])
        else:
            new_board.append([0,0,1])
    
    return np.reshape(new_board, (1,126))
    
#--------------
train_dnn_player()