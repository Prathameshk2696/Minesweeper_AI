# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 11:56:30 2020

@author: Prthamesh
"""
import sys
mypath = r'F:\Fall 2020\Introduction to AI\Assignments\Minesweeper\Minesweeper_Project\Code'
sys.path.append(mypath)

import board_generation as bg
import kb_generation as kbg    

# function to play minesweeper manually
# minesweeper board is visualized in a console
# Input parameters: dimension of a board, total count of mines
def manual_play(dim,total_count_of_mines):
    # get the visible board, function to reveal status of position, function to get count of mine neighbors
    board_visible,reveal_position,get_cmn_from_board_actual = bg.get_board(dim,total_count_of_mines)
    kbg.initialize_list_of_unidentified_cells(dim) # initialize a list of cells that are unidentified in visible board
    kbg.initialize_set_of_inferred_safe_cells() # initialize a list of cells that are inferred to be safe
    no_of_mines_stepped = 0 # initialize number of mines stepped to 0
    automate = False # set automate till the end flag to False.
    while kbg.list_of_unidentified_cells: # iterate until all cells in a visible board are identified
        bg.display_board2(board_visible) # display visible board
        print()
        print('Number of mines stepped :',no_of_mines_stepped) # display number of mines stepped so far
        if not automate: # if not automated till the end
            print('Enter row,col for manual reveal move') # manual move to reveal position
            print('Enter row,col,f for manual flag move') # manual move to flag position
            print('Enter 1 for basic AI move') # basic agent move
            print('Enter 2 for single improved AI move') # single improved agent move
            print('Enter 3 for double improved AI move') # double improved agent move
            print('Enter AI_number-auto to automate game till the end') # AI_number-auto will automate the play till the end
            print('Enter e to end the game',end='') # end the game
        if not automate: # if not automated till the end
            input_str = input('Input :') # take input from user
        if input_str == 'e': # if input is e
            break # end the game
        if input_str == '1-auto' or input_str == '2-auto' or input_str == '3-auto': # if input is to automate the game till the end
            input_str = input_str[0] # AI_number
            automate = True # set automate till the end flag to True
        #print('\n')
        print('-'*(dim*6))
        if ',' in input_str: # if input is row,col
            str_splitted = input_str.split(',') # split the input string on comma
            r = int(str_splitted[0]) # get row number
            c = int(str_splitted[1]) # get column number
            if len(str_splitted) == 2:
                move = 'r' # move is to reveal a position
            else:
                move = str_splitted[2] # move is to flag
            kbg.list_of_unidentified_cells.remove((r,c)) # remove position (r,c) from a list of unidentified cells
            if (r,c) in kbg.set_of_inferred_safe_cells: # if (r,c) is in set of inferred safe cells
                kbg.set_of_inferred_safe_cells.remove((r,c)) # remove (r,c) from that set
        elif input_str == '1': # if input is basic agent move
            if len(kbg.set_of_inferred_safe_cells)==0: # if no cell has been inferred to be safe
                kbg.inference1(board_visible) # execute inference 1
                if not kbg.list_of_unidentified_cells: # if inference identifies all remaining cells to be mines
                    break # end the game
            r,c = kbg.get_next_move(board_visible,'basic_agent') # get the next move
        elif input_str == '2': # if input is single improved agent move
            if len(kbg.set_of_inferred_safe_cells)==0: # if no cell has been inferred to be safe
                kbg.inference2(board_visible) # execute inference 2
                if not kbg.list_of_unidentified_cells: # if inference identifies all remaining cells to be mines
                    break # end the game
            r,c = kbg.get_next_move(board_visible,'single_improved_agent') # get the next move
        elif input_str == '3': # if input is double improved agent move
            if len(kbg.set_of_inferred_safe_cells)==0: # if no cell has been inferred to be safe
                kbg.inference2(board_visible) # execute inference 2
                if not kbg.list_of_unidentified_cells: # if inference identifies all remaining cells to be mines
                    break # end the game 
            r,c = kbg.get_next_move(board_visible,'double_improved_agent') # get next move
        if ',' in input_str and move == 'f': # move is to flag a position
            bg.update_board_visible(board_visible,r,c,1,get_cmn_from_board_actual)
        else:
            status = reveal_position(r,c) # reveal the position. get status as 0(safe) or 1(mine)
            bg.update_board_visible(board_visible,r,c,status,get_cmn_from_board_actual) # update attributes of revealed cell and its neighbors
            if status == 1: # if revealed cell is a mine
                no_of_mines_stepped += 1 # increment number of mines stepped by 1
        print('Move played :',(r,c))
        print()
    bg.display_board2(board_visible) # display board at the end of game
    print()
    print('Number of mines stepped :',no_of_mines_stepped) # display number of mines stepped throughout the game
    
# function call to play minesweeper manually
manual_play(dim = 10,total_count_of_mines = 45)