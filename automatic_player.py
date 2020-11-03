# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 13:06:03 2020

@author: Prthamesh
"""

import sys
mypath = r'F:\Fall 2020\Introduction to AI\Assignments\Minesweeper\Minesweeper_Project\Code'
sys.path.append(mypath)

import board_generation as bg
import kb_generation as kbg
import plotly.graph_objects as go
from copy import deepcopy as dc                 

# function to play single game by AI agent
# Input parameters: visible board, name of agent, function to reveal position, function to get count of mine neighbors
def automatic_play(board_visible,agent_name,reveal_position,get_cmn_from_board_actual):
    dim = len(board_visible) # dimension of a board
    kbg.initialize_list_of_unidentified_cells(dim) # initialize a list of cells that are unidentified in visible board
    kbg.initialize_set_of_inferred_safe_cells() # initialize a list of cells that are inferred to be safe
    no_of_mines_stepped = 0 # initialize number of mines stepped to 0
    #kbg.count_of_identified_cells = 0
    if agent_name == 'basic_agent': # if agent is basic
        kbg.inference1(board_visible) # execute inference 1
    elif agent_name == 'single_improved_agent' or agent_name == 'double_improved_agent': # if agent is single or double improved
#        st = time.time()
        kbg.inference2(board_visible) # execute inference 2 (CSP - backtracking search based inference)
#        et = time.time()
#        print('I',et-st)
    while kbg.list_of_unidentified_cells: # iterate until all cells in a visible board are identified
        position = kbg.get_next_move(board_visible,agent_name) # get the position of a cell to reveal
        status = reveal_position(*position) # reveal the position. returns status as 0(safe) or 1(mine)
        bg.update_board_visible(board_visible,*position,status,get_cmn_from_board_actual) # update attributes of revealed cell and its neighbors
        #kbg.count_of_identified_cells += 1
        if status == 1: # if revealed cell is a mine (mine is stepped)
            no_of_mines_stepped += 1 # increment number of mines stepped by 1
        if len(kbg.set_of_inferred_safe_cells)==0: # if set of inferred safe cells is empty, then execute inference
            if agent_name == 'basic_agent': # if agent is basic
                kbg.inference1(board_visible) # execute inference 1
            elif agent_name == 'single_improved_agent' or agent_name == 'double_improved_agent': # if agent is single or double improved
#                print('Inside Inference:',end=' ')
#                st = time.time()
                kbg.inference2(board_visible) # execute inference 2 (CSP - backtracking search based inference)
#                et = time.time()
#                print(et-st)
    return no_of_mines_stepped # return number of mines stepped by AI agent

# function that creates data for the line chart
# Input parameters: dimension of a board, start mine density, stop mine density,
# step mine density, total number of runs to compute average, agent indicator random variables
def create_data(dim,start_md,stop_md,step_md,total_runs=1,agent_1=0,agent_2=0,agent_3=0):
    md_list = [] # list of mine densities. (x-axis values for the line chart)
    avg_final_scores_list_1,avg_final_scores_list_2,avg_final_scores_list_3 = [],[],[] # y-axis values for the line chart (one line per agent)
    md = start_md # initialize mine density to start mine density
    while md<=stop_md: # iterate while mine density <= stop mine density
        run_number = 1 # initialize run number to 1
        final_scores_list_1,final_scores_list_2,final_scores_list_3 = [],[],[] # list to store final scores
        while run_number<=total_runs: # iterate total_runs number of times
            total_count_of_mines = round((dim**2)*md) # total count of mines to be set
            # get the visible board, function to reveal status of position, function to get count of mine neighbors
            board_visible_1,reveal_position,get_cmn_from_board_actual = bg.get_board(dim,total_count_of_mines) 
            board_visible_2 = dc(board_visible_1) # deepcopy visible board for single improved agent
            board_visible_3 = dc(board_visible_1) # deepcopy visible board for double improved agent
            # Basic agent
            if agent_1 == 1: # if indicator variable of agent 1 is 1
                # play a single game and get number of mines stepped by basic agent
                no_of_mines_stepped = automatic_play(board_visible_1,'basic_agent',reveal_position,get_cmn_from_board_actual)
                print(run_number,md,'basic agent',no_of_mines_stepped)
                no_of_safely_identified_mines = total_count_of_mines - no_of_mines_stepped # count of safely identified mines (not stepped)
                final_score = no_of_safely_identified_mines/total_count_of_mines # compute final score
                final_scores_list_1.append(final_score) # append final score to the list of basic agent
            # Single improved agent
            if agent_2 == 1: # if indicator variable of agent 2 is 1
                # play a single game and get number of mines stepped by single improved agent
                no_of_mines_stepped = automatic_play(board_visible_2,'single_improved_agent',reveal_position,get_cmn_from_board_actual)
                print(run_number,md,'single improved agent',no_of_mines_stepped)
                no_of_safely_identified_mines = total_count_of_mines - no_of_mines_stepped # count of safely identified mines (not stepped)
                final_score = no_of_safely_identified_mines/total_count_of_mines # compute final score
                final_scores_list_2.append(final_score) # append final score to the list of single improved agent
            # Double improved agent
            if agent_3 == 1: # if indicator variable of agent 3 is 1
                # play a single game and get number of mines stepped by double improved agent
                no_of_mines_stepped = automatic_play(board_visible_3,'double_improved_agent',reveal_position,get_cmn_from_board_actual)
                print(run_number,md,'double improved agent',no_of_mines_stepped)
                no_of_safely_identified_mines = total_count_of_mines - no_of_mines_stepped # count of safely identified mines (not stepped)
                final_score = no_of_safely_identified_mines/total_count_of_mines # compute final score
                final_scores_list_3.append(final_score) # append final score to the list of double improved agent
            run_number += 1 # increment run number by 1
        if agent_1 == 1: # if indicator variable of basic agent is 1
            avg_final_score_1 = sum(final_scores_list_1)/len(final_scores_list_1) # compute average of final scores of basic agent
            avg_final_scores_list_1.append(avg_final_score_1) # append average final score for a particular mine density to the list
        if agent_2 == 1: # if indicator variable of single improved agent is 1
            avg_final_score_2 = sum(final_scores_list_2)/len(final_scores_list_2) # compute average of final scores
            avg_final_scores_list_2.append(avg_final_score_2) # append average final score for a particular mine density to the list
        if agent_3 == 1: # if indicator variable of double improved agent is 1
            avg_final_score_3 = sum(final_scores_list_3)/len(final_scores_list_3) # compute average of final scores
            avg_final_scores_list_3.append(avg_final_score_3) # append average final score for a particular mine density to the list
        md_list.append(md) # append mine density to its list
        md += step_md # increment mine density by step mine density
    avg_final_scores_dict = {} # dictionary to contain a list of average final scores for all 3 agents
    if agent_1 == 1: # if indicator variable of basic agent is 1
        avg_final_scores_dict['basic_agent'] = avg_final_scores_list_1 # add basic agent's list of average final scores to a dict
    if agent_2 == 1: # if indicator variable of single improved agent is 1
        avg_final_scores_dict['single_improved_agent'] = avg_final_scores_list_2 # add single improved agent's list of average final scores to a dict
    if agent_3 == 1: # if indicator variable of double improved agent is 1
        avg_final_scores_dict['double_improved_agent'] = avg_final_scores_list_3 # add double improved agent's list of average final scores to a dict
    return md_list,avg_final_scores_dict # return list of mine densities and dictionary containing average final scores lists

# function to plot line charts of final scores vs mine density for given agents
# Input parameters: dimension of a board, start mine density, stop mine density,
# step mine density, total number of runs to compute average, agent indicator random variables
def plot_data(dim,start_md,stop_md,step_md,total_runs=1,agent_1=0,agent_2=0,agent_3=0):
    md_list,avg_final_scores_dict = create_data(dim,start_md,stop_md,step_md,total_runs,agent_1,agent_2,agent_3) # get the data for line charts
    fig = go.Figure() # create Figure object
    if agent_1 == 1: # if indicator variable of basic agent is 1
        avg_final_scores_list1 = avg_final_scores_dict['basic_agent'] # get a list of average final scores of basic agent
        fig.add_trace(go.Scatter(x=md_list,y=avg_final_scores_list1,name='Basic Agent')) # add line chart of basic agent to figure
    if agent_2 == 1: # if indicator variable of single improved agent is 1
        avg_final_scores_list2 = avg_final_scores_dict['single_improved_agent'] # get a list of average final scores of single improved agent
        fig.add_trace(go.Scatter(x=md_list,y=avg_final_scores_list2,name='Single Improved Agent')) # add line chart of single improved agent to figure
    if agent_3 == 1: # if indicator variable of double improved agent is 1
        avg_final_scores_list3 = avg_final_scores_dict['double_improved_agent'] # get a list of average final scores of double improved agent
        fig.add_trace(go.Scatter(x=md_list,y=avg_final_scores_list3,name='Double Improved Agent')) # add line chart of double improved agent to figure
    fig.update_layout(title = 'Dimension : '+str(40)+' | Final Score vs Mine Density',
                      xaxis_title="Mine Density",
                      yaxis_title="Final Score",
                      legend_title="Agent Name")
    fig.show() # show figure in console
    
# function call to plot data
plot_data(dim=10,start_md=0.1,stop_md=0.45,step_md=0.1,total_runs=1,agent_1=1,agent_2=1,agent_3=1)







