# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 15:34:37 2020

@author: Prthamesh
"""

import random
import board_generation as bg
import csp

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

# function that executes basic agent algorithm
def inference1(board_visible):
    global set_of_inferred_safe_cells
    dim = len(board_visible) # dimension of a board
    for r in range(dim): # iterate through every row
        for c in range(dim): # iterate through every column
            if board_visible[r][c]['status']!=' ': # if cell at (r,c) is revealed
                cell = board_visible[r][c] # get the dictionary representation of cell at (r,c)
                status = cell['status'] # status of a cell. 
                if status == 0: # if cell is safe
                    cmn = cell['cmn'] # count of mine neighbors
                    cisn = cell['cisn'] # count of identified safe neighbors
                    cimn = cell['cimn'] # count of identified mine neighbors
                    chn = cell['chn'] # count of hidden neighbors
                    ctn = cell['ctn'] # count of total neighbors
                    # if count_of_mine_neighbors == count_of_identified_mine_neighbors+count_of_hidden_neighbors
                    if cmn == (cimn + chn):
                        # then, every hidden neighbor is a mine
                        npl = get_neighbor_positions(dim,r,c) # get a list of neighbor positions
                        for nr,nc in npl: # iterate through a list of neighbors
                            if board_visible[nr][nc]['status']==' ': # if neighbor is hidden
                                board_visible[nr][nc]['status'] = 1 # cell at (nr,nc) is a mine
                                bg.update_counts_of_neighbors(board_visible,nr,nc,1) # update counts of neighbors of revealed cell
                                list_of_unidentified_cells.remove((nr,nc))
                    # if count of safe neighbors == count of identified safe neighbors + count of hidden neighbors
                    elif (ctn-cmn)==(cisn+chn):
                        # then, every hidden neighbor is safe
                        npl = get_neighbor_positions(dim,r,c) # get a list of neighbor positions
                        for nr,nc in npl: # iterate through a list of neighbors
                            if board_visible[nr][nc]['status']==' ': # if neighbor is hidden
                                set_of_inferred_safe_cells.add((nr,nc)) # add inferred safe cell to the set
                        

def inference2(board_visible):
    inference1(board_visible) # check if inference1 is sufficient to find at least 1 safe cell
    if len(set_of_inferred_safe_cells)>0: # if at least 1 safe cell is inferred
        return # return
    else: # if inference1 could not infer any safe cell
        solution_domain = csp.get_solution_domains(board_visible) # get solution domain by backtracking search
        for position,domain in solution_domain.items():
            r,c = position
            if domain == {0}:
                set_of_inferred_safe_cells.add((r,c))
            elif domain == {1}:
                board_visible[r][c]['status'] = 1 # cell at (r,c) is a mine
                bg.update_counts_of_neighbors(board_visible,r,c,1) # update counts of neighbors of revealed cell
                list_of_unidentified_cells.remove((r,c))
    
def get_position_with_least_mine_probability():
    cell_being_mine_probabilities = csp.get_probabilities_of_cells_being_mine()
    min_position,min_prob = None,1
    for position,prob in cell_being_mine_probabilities.items():
        if prob < min_prob:
            min_position = position
            min_prob = prob
    return min_position

# function that executes inference and returns next move to be played by AI agent
def get_next_move(board_visible,agent_name):
    if len(set_of_inferred_safe_cells)>0: # if set of inferred safe cells is not empty
        position = set_of_inferred_safe_cells.pop() # pop the inferred safe position
        list_of_unidentified_cells.remove(position)
        return position # return position, count of flagged mines
    else: # if set of inferred safe cells is still empty even after inference
        if agent_name == 'basic_agent' or agent_name == 'single_improved_agent':
            position = random.choice(list_of_unidentified_cells)
            list_of_unidentified_cells.remove(position)
        elif agent_name == 'double_improved_agent':
            position = get_position_with_least_mine_probability()
            # print('Least mine probability :',position)
            if position is not None:
                list_of_unidentified_cells.remove(position)
            else:
                position = random.choice(list_of_unidentified_cells)
                list_of_unidentified_cells.remove(position)
        return position
    
def initialize_set_of_inferred_safe_cells():
    global set_of_inferred_safe_cells
    set_of_inferred_safe_cells = set()
                
def initialize_list_of_unidentified_cells(dim):
    global list_of_unidentified_cells
    list_of_unidentified_cells = [(i,j) for i in range(dim) for j in range(dim)]