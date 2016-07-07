# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 16:11:04 2016

@author: shengquan
"""
# import theano.sandbox.cuda
# theano.sandbox.cuda.use('gpu0')
from keras.models import Sequential
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.noise import GaussianNoise
from keras.optimizers import SGD, Adam, Adamax
from keras.callbacks import EarlyStopping
import random
import time
import numpy as np
#import random

import connectfour as cf

import minimax_ai as mini_ai

#create the dnn player
model = Sequential()
    
layers = [
    Dense(126, init='lecun_uniform', input_shape=(42*3,)), Activation('relu'), Dropout(0.5),
    Dense(126, init='lecun_uniform'), Activation('relu'), Dropout(0.5),
    Dense(90, init='lecun_uniform'), Activation('relu'), Dropout(0.5),
    Dense(60, init='lecun_uniform'), Activation('relu'), Dropout(0.5),
    Dense(7, init='lecun_uniform'), Activation('linear')
]
    
for layer in layers:
    model.add(layer)
    
model.compile(loss='mse', optimizer='rmsprop')
    
def train_dnn_player():    
    
    #start reinforcement learning
    epochs = 10000 #no of rounds
    gamma = 0.9 #discount factor
    epsilon = 1 #exploitation vs exploration
    buffer = 80
    replay = []
    batchSize = 40
    h = 0
    
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
            
            #let minimax play
            if new_state[1] =='ongoing':
                new_state = cf.make_move(new_state[0], mini_ai.minimax(new_state[0], False), False)
                newQ = model.predict(reshape_board(new_state[0]), batch_size=1)
                maxQ = np.max(newQ)
                update = (reward + (gamma * maxQ))
            else:
                update = reward
            
            
            
            #experience replay; basically we are going to create a list of replays for the NN to refer to everytime it's called
            if (len(replay)<buffer):
                replay.append((state, action, update, new_state))
            else: #buffer is full, overwrite old values
                if (h < (buffer-1)):
                    h += 1
                else:
                    h = 0
                replay[h] = (state, action, update, new_state)
                
                #randomly sample our experience replay memory
                minibatch = random.sample(replay, batchSize)
                X_train = []
                y_train = []
                
                for memory in minibatch:
                    #get max_Q(S', a)
                    old_state, action, update, new_state = memory
                    old_qval = model.predict(reshape_board(old_state[0]), batch_size=1)
                    
                    """
                    newQ = model.predict(reshape_board(new_state[0]), batch_size=1)
                    maxQ = np.max(newQ)
                    y = np.zeros((1,7))
                    y[:] = old_qval[:]
                    if new_state[1] =='ongoing':
                        new_state = cf.make_move(new_state[0], mini_ai.minimax(new_state[0], False), False)
                        #newQ = model.predict(reshape_board(new_state[0]), batch_size=1)                        
                        update = (reward + (gamma * maxQ))
                    else:
                        update = reward
                        
                    y[0][action] = update
                    """
                    
                    y = np.zeros((1,7))
                    y[:] = old_qval[:]
                    y[0][action] = update
                    
                    X_train.append( reshape_board(old_state[0]).reshape(126) )
                    y_train.append( y.reshape(7) )
                   
                X_train = np.array(X_train)
                y_train = np.array(y_train)
                model.fit(X_train, y_train, batch_size=batchSize, verbose=1)
            
            state = new_state
                
        if epsilon > 0.1:
            epsilon -= (1 / epochs)

        print(state)


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
start_time = time.time()
train_dnn_player()
print('Time: {:.2f}s'.format(time.time() - start_time))