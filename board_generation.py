# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:37:15 2020

@author: Prthamesh
"""

import numpy as np
import random

# function that displays visible board
def display_board(board_visible):
    dim = len(board_visible) # dimension of a board
    l = [[] for _ in range(dim)] # 
    for i in range(dim): # iterate through every row
        for j in range(dim): # iterate through every column
            if board_visible[i][j]['status']==1: # if cell is revealed to be a mine(1)
                l[i].append('M') # append letter M
            elif board_visible[i][j]['status']==0: # if cell is revealed to be safe(0)
                l[i].append(board_visible[i][j]['cmn']) # append count of mine neighbors
            else: # if cell is not revealed
                l[i].append(' ') # append white space of length 1
    arr = np.array(l) # construct ndarray of a board
    print(arr) # display ndarray
    
def display_board2(board_visible):
    dim = len(board_visible)
    print('  ',end='')
    for i in range(dim):
        print('  {} '.format(i),end='')
    print()
    print('  ',end='')
    print('-'*(4*dim+1))
    for r in range(dim):
        print('{} |'.format(r),end=' ')
        for c in range(dim):
            if board_visible[r][c]['status']==1: # if cell is revealed to be a mine(1)
                print('M',end=' | ') # append letter M
            elif board_visible[r][c]['status']==0: # if cell is revealed to be safe(0)
                print(board_visible[r][c]['cmn'],end=' | ') # append count of mine neighbors
            else: # if cell is not revealed
                print(' ',end=' | ') # append white space of length 1
        print()
        print('  ',end='')
        print('-'*(4*dim+1))
    
# function that returns a list of neighbor positions
def get_neighbor_positions(dim,r,c):
    npl = [] # empty neighbor positions list
    # check existence of cells in all 8 directions and
    # if cell exists, add its position to neighbor positions list
    if r<(dim-1): npl.append((r+1,c))
    if r>0: npl.append((r-1,c))
    if c<(dim-1): npl.append((r,c+1))
    if c>0: npl.append((r,c-1))
    if r>0 and c>0: npl.append((r-1,c-1))
    if r>0 and c<(dim-1): npl.append((r-1,c+1))
    if r<(dim-1) and c>0: npl.append((r+1,c-1))
    if r<(dim-1) and c<(dim-1): npl.append((r+1,c+1))
    return npl # return updated neighbor positions list

# function creates and returns actual board
# actual board stores all the information about the board
# actual board is not accessible to the AI agent
# information from actual board is copied to the visible board based on agent's actions
def get_actual_board(dim):
    board_actual = [[] for _ in range(dim)] # board initialized to a list of empty list
    for i in range(dim): # iterate through each row
        for j in range(dim): # iterate through each column
            status = 0 # initialize status to safe
            count_of_mine_neighbors = 0 # initialize count of adjacent mines to 0 
            if ((i,j)==(0,0) or # left upper corner cell
                (i,j)==(dim-1,0) or # left lower corner cell
                (i,j)==(0,dim-1) or # right upper corner cell
                (i,j)==(dim-1,dim-1)): # right lower corner cell
                count_of_total_neighbors = 3 # corner cells have 3 neighbors
            elif i==0 or i==(dim-1) or j==0 or j==(dim-1): # boundary cells except corner cells
                count_of_total_neighbors = 5 # they have 5 neighbors
            else: # all other cells
                count_of_total_neighbors = 8 # they have 8 neighbors
            # each cell is a dictionary
            cell = {
                    'status':status,
                    'cmn':count_of_mine_neighbors,
                    'ctn':count_of_total_neighbors
                    }
            board_actual[i].append(cell) # append cell to the list in a board
    return board_actual # return actual board

# function creates and returns visible board
# visible board is the environment of AI agent
# information is revealed in the visible board based on agent's actions
def get_visible_board(dim):
    board_visible = [[] for _ in range(dim)] # board initialized to a list of empty list
    for i in range(dim): # iterate through every row
        for j in range(dim): # iterate through every column
            status = ' ' # whitespace(not known) , 0(safe) , 1(mine)
            count_of_mine_neighbors = None # count of adjacent mines is unknown initially
            count_of_identified_safe_neighbors = 0 # 0 safe neighbors has been identified
            count_of_identified_mine_neighbors = 0 # 0 mine neighbors has been identified
            if ((i,j)==(0,0) or # left upper corner cell
                (i,j)==(dim-1,0) or # left lower corner cell
                (i,j)==(0,dim-1) or # right upper corner cell
                (i,j)==(dim-1,dim-1)): # right lower corner cell
                count_of_hidden_neighbors = 3 # corner cells have 3 neighbors
            elif i==0 or i==(dim-1) or j==0 or j==(dim-1): # boundary cells except corner cells
                count_of_hidden_neighbors = 5 # they have 5 neighbors
            else: # all other cells
                count_of_hidden_neighbors = 8 # they have 8 neighbors
            count_of_total_neighbors = count_of_hidden_neighbors # initially, they are equal
            # each cell is a dictionary
            cell = {
                    'status':status,
                    'cmn':count_of_mine_neighbors,
                    'cisn':count_of_identified_safe_neighbors,
                    'cimn':count_of_identified_mine_neighbors,
                    'chn':count_of_hidden_neighbors,
                    'ctn':count_of_total_neighbors
                    } 
            board_visible[i].append(cell) # append cell to the list in a board
    return board_visible # return visible board
        
# function to set mines in an actual board
# Inputs- actual board, count of mines to be set
def set_mines(board_actual,total_count_of_mines):
    dim = len(board_actual) # dimension of a board
    count_of_mines_set = 0 # count of mines set is initially 0
    while count_of_mines_set < total_count_of_mines: # iterate until given number of mines are set
        r = random.randint(0,dim-1) # random choice of row number
        c = random.randint(0,dim-1) # random choice of col number
        if board_actual[r][c]['status'] != 1: # if cell at (r,c) is not already a mine 
            board_actual[r][c]['status'] = 1 # set a mine at (r,c)
            count_of_mines_set += 1 # increment count of mines set by 1
        
# function that returns count of mine neighbors of a cell at (r,c)
def get_count_of_mine_neighbors(board_actual,r,c):
    dim = len(board_actual) # dimenison of a board 
    cmn = 0 # initialize count of mine neighbors to 0
    # check for existence of a cell in all 8 directions and 
    # if cell exists, check if its status is a mine(1)
    if r<(dim-1) and board_actual[r+1][c]['status']==1: cmn += 1 
    if r>0 and board_actual[r-1][c]['status']==1: cmn += 1
    if c<(dim-1) and board_actual[r][c+1]['status']==1: cmn += 1
    if c>0 and board_actual[r][c-1]['status']==1: cmn += 1
    if r>0 and c>0 and board_actual[r-1][c-1]['status']==1: cmn += 1
    if r>0 and c<(dim-1) and board_actual[r-1][c+1]['status']==1: cmn += 1
    if r<(dim-1) and c>0 and board_actual[r+1][c-1]['status']==1: cmn += 1
    if r<(dim-1) and c<(dim-1) and board_actual[r+1][c+1]['status']==1: cmn += 1
    return cmn # return updated count of mine neighbors
        
# function that initializes count of mine neighbors of every cell in actual board
def initialize_cmn(board_actual):
    dim = len(board_actual) # dimension of board
    for row_num in range(dim): # iterate through every row
        for col_num in range(dim): # iterate through every column
            cmn = get_count_of_mine_neighbors(board_actual,row_num,col_num) # get count of mine neighbors
            board_actual[row_num][col_num]['cmn'] = cmn # initialize cmn
        
# function that updates counts of neighbors of revealed cell
# count of identified mine neighbors
# count of identified safe neighbors
# count of hidden neighbors
def update_counts_of_neighbors(board_visible,row,col,status):
    dim = len(board_visible) # dimension of a board
    npl = get_neighbor_positions(dim,row,col) # get a list of neighbor positions
    if status == 1: # if cell was revealed to be a mine
        for (r,c) in npl: # iterate through its neighbor cells
            board_visible[r][c]['cimn'] += 1 # increment count of identified mine neighbors by 1
    elif status == 0: # if cell was revealed to be safe
        for (r,c) in npl: # iterate through its neighbor cells
            board_visible[r][c]['cisn'] += 1 # increment count of identified safe neighbors by 1
    for (r,c) in npl: # iterate through neighbor cells
        board_visible[r][c]['chn'] -= 1 # decrement count of hidden neighbors by 1
        
def update_board_visible(board_visible,r,c,status,get_cmn_from_board_actual):
    board_visible[r][c]['status'] = status # copy status to visible board
    if status == 0: # if cell is safe(0)
        board_visible[r][c]['cmn'] = get_cmn_from_board_actual(r,c) # copy count of mine neighbors
    update_counts_of_neighbors(board_visible,r,c,status) # update counts of neighbors of a revealed cell

# function that creates actual and visible board
# It returns visible board
# It also returns a function reveal_position that stores actual board by state retention mechanism of closure function
# reveal_position is used to update the visible board by copying information from actual board
def get_board(dim,total_count_of_mines):
    board_actual = get_actual_board(dim) # get actual board
    set_mines(board_actual,total_count_of_mines) # set mines in actual board
    initialize_cmn(board_actual) # initialize counts of mine neighbors
    board_visible = get_visible_board(dim) # get visible board 
    # function that will reveal information based on agent's actions
    # It takes row number, column number played by agent as input
    def reveal_position(r,c): 
        status = board_actual[r][c]['status'] # get the status of a cell at (r,c) from actual board
        return status # return the status of revealed cell
    def get_cmn_from_board_actual(r,c):
        if board_actual[r][c]['status'] == 0:
            return board_actual[r][c]['cmn']
        else:
            return None
    return board_visible, reveal_position, get_cmn_from_board_actual # return visible board and function reveal_position
