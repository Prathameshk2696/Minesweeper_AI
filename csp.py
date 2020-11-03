# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 12:11:15 2020

@author: Prthamesh
"""
from copy import deepcopy as dc

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

# function to compute and return a list of constraints
def get_list_of_constraints(board_visible):
    dim = len(board_visible) # dimension of a board
    constraints_list = [] # empty constraint list
    for r in range(dim): # iterate through every row
        for c in range(dim): # iterate through every column
            status = board_visible[r][c]['status']
            if status == 0: # if cell is safe
                cmn = board_visible[r][c]['cmn'] # get count of mine neighbors
                npl = get_neighbor_positions(dim,r,c) # get list of neighbor positions
                lhnpc = [] # list of hidden neighbor positions in a constraint
                for (nr,nc) in npl: # iterate through a list of neighbor positions
                    if board_visible[nr][nc]['status'] == ' ': # if neighbor cell is hidden
                        lhnpc.append((nr,nc)) # append cell (nr,nc) to list
                cmn_eff = cmn - board_visible[r][c]['cimn'] # count of effective mine neighbors
                constraint = {'lhnpc':lhnpc,'cmn_eff':cmn_eff} # each constraint is a dictionary containing indicator positions and their sum
                constraints_list.append(constraint) # append constraint to the list
    return constraints_list # return a list of constraints

# all domains are {0,1}. Not used currently
def get_domains(board):
    dim = len(board)
    domains_list = []
    for r in range(dim):
        for c in range(dim):
            if board[r][c]['status'] == None:
                domains_list.append({(r,c):[0,1]})
    return domains_list
    
# function that returns a list of constrained positions.
# list is ordered by number of constraints in a descending order.
# Most constrained variable heuristic. Positions (r,c) are the variables.
def get_ordered_variables_list(cl):
    position_count_dict = {} # dictionary to store position:count_of_constraints
    for constraint in cl: # iterate through each constraint
        lhnpc = constraint['lhnpc'] # list of hidden neighbor positions in a constraint 
        for position in lhnpc: # iterate through every position in a constraint
            if position not in position_count_dict: # if position not in dictionary
                position_count_dict[position] = 1 # initialize its count to 1
            else: # if position already in a dictionary
                position_count_dict[position] += 1 # increment its count by 1
    ordered_var_list = [] # list to store positions in the above mentioned order.
    # Insertion sort is used to build the ordered list.
    i = 0 
    for position,count in position_count_dict.items(): 
        j = i-1
        while j>=0:
            ps = ordered_var_list[j]
            if position_count_dict[ps]<position_count_dict[position]:
                j -= 1
                continue
            else:
                ordered_var_list = ordered_var_list[0:j+1]+[position]+ordered_var_list[j+1:]
                break
        else:
            ordered_var_list = [position] + ordered_var_list[:]
        i += 1
    return ordered_var_list

# function that checks if given constraints are satisfied
def are_given_constraints_satisfied(assignment,cl):
    for constraint in cl: # iterate through each constraint
        lhnpc = constraint['lhnpc'] #  list of hidden neighbor positions in a constraint
        if set(lhnpc).issubset(set(assignment.keys())):
            cmn_eff = constraint['cmn_eff'] # sum of constrained indicator positions
            total = 0 # initialize total to 0
            for position in lhnpc: # iterate through each position in a constraint
                total += assignment[position] # add its value to the total
            if total == cmn_eff: # if total matches with the actual sum
                continue # continue to the next constraint
            else: # if total does not match with actual sum
                return False # return False because constraint is not satisfied
    # if all constraints have been satisfied
    return True # return True
        
# function that checks if all constraints are satisfied
def are_all_constraints_satisfied(assignment,cl):
    for constraint in cl: # iterate through each constraint
        lhnpc = constraint['lhnpc'] #  list of hidden neighbor positions in a constraint
        cmn_eff = constraint['cmn_eff'] # sum of constrained indicator positions
        total = 0 # initialize total to 0
        for position in lhnpc: # iterate through each position in a constraint
            total += assignment[position] # add its value to the total
        if total == cmn_eff: # if total matches with the actual sum
            continue # continue to the next constraint
        else: # if total does not match with actual sum
            return False # return False because constraint is not satisfied
    # if all constraints have been satisfied
    return True # return True

# function to execute backtracking
# input parameter: partial or complete assignment, constraints list, depth in a tree
def backtrack_with_pruning(assignment,cl,depth):
    if depth>=len(ordered_variables_list): # if all positions have been assigned
        res = are_all_constraints_satisfied(assignment,cl) # check if all constraints are satisfied
        if res: # if all constraints are satisfied
            all_solutions.append(assignment) # append complete and consistent assignment to the list
            return # return
        else: # if all constraints are not satisfied
            return # return
    position = ordered_variables_list[depth] # get the indicator position to be assigned
    for value in [0,1]: # every indicator position has possible values: safe(0) or mine(1)
        assignment2 = dc(assignment) # copy the partial assignment
        assignment2[position] = value # assign value to the position
        if are_given_constraints_satisfied(assignment2,cl):
            backtrack(assignment2,cl,depth+1) # recursive call to the next level in a tree
    return # return 
    
# function to execute backtracking
# input parameter: partial or complete assignment, constraints list, depth in a tree
def backtrack(assignment,cl,depth):
    if depth>=len(ordered_variables_list): # if all positions have been assigned
        res = are_all_constraints_satisfied(assignment,cl) # check if all constraints are satisfied
        if res: # if all constraints are satisfied
            all_solutions.append(assignment) # append complete and consistent assignment to the list
            return # return
        else: # if all constraints are not satisfied
            return # return
    position = ordered_variables_list[depth] # get the indicator position to be assigned
    for value in [0,1]: # every indicator position has possible values: safe(0) or mine(1)
        assignment2 = dc(assignment) # copy the partial assignment
        assignment2[position] = value # assign value to the position
        backtrack(assignment2,cl,depth+1) # recursive call to the next level in a tree
    return # return 

def reduce_constraints_list(constraints_list):
    global ordered_variables_list
    constraint_list_new = []
    ordered_variables_list = ordered_variables_list[0:16] # first 13 most constrained positions
    for constraint in constraints_list:
        lhnpc = constraint['lhnpc']
        if len(set(lhnpc)-set(ordered_variables_list))==0:
            constraint_list_new.append(constraint)
    return constraint_list_new       
    
# function that executes backtracking search and computes all possible solutions
def backtracking_search(constraints_list):
    global ordered_variables_list
    ordered_variables_list = get_ordered_variables_list(constraints_list) # get a list of ordered positions
    #print('Before',len(ordered_variables_list))
    if len(ordered_variables_list)>=16:
        constraints_list = reduce_constraints_list(constraints_list)
        ordered_variables_list = get_ordered_variables_list(constraints_list)
    #print('After',len(ordered_variables_list))
    global all_solutions
    all_solutions = [] # list to store all possible assignments
    backtrack_with_pruning({},constraints_list,0) # begin backtracking
    return # return

# function that merges all posible solutions to compute resultant domains of every constrained variable
def get_solution_domains(board):
    cl = get_list_of_constraints(board) # get a list of constraints
    if len(cl)==0: # if there are no constraints
        global all_solutions
        all_solutions = []
        return {} # return empty solution domain
    else: # if there is at least one constraint
        backtracking_search(cl) # execute backtracking search to get all possible solutions
        resultant_domains = {} # dictionary to store resultant domains of all constrained positions
        for solution in all_solutions: # iterate through each solution
            for position,value in solution.items(): # iterate through assignment of each position in a solution
                if position not in resultant_domains: # if position is not in resultant domains
                    resultant_domains[position] = {value} # initialize its value
                else: # if position is already in resultant domains
                    resultant_domains[position].add(value) # add value of position to the dictionary
        return resultant_domains # return resultant domains

def get_probabilities_of_cells_being_mine():
    number_of_solutions = len(all_solutions)
    cell_being_mine_counts = {}
    for solution in all_solutions:
        for position,value in solution.items():
            cell_being_mine_counts[position] = 0
    for solution in all_solutions:
        for position,value in solution.items():
            if value == 1:
                cell_being_mine_counts[position] += 1
    cell_being_mine_probabilities = {}
    for position,count in cell_being_mine_counts.items():
        cell_being_mine_probabilities[position] = count/number_of_solutions
    return cell_being_mine_probabilities
    
    
    
    
    