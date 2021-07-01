# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 09:28:47 2021

@author: KirstenLNelson

Given a base and shift sequence, create the interleaved sequence and
calculate the coverage.
"""

import doctest
from time import time
import numpy
import itertools

# create_il_seq: list list -> list     
# Purpose: Given base and shift sequences, create the interleaved sequence
# -----------------------------------------------------------------------------
def create_il_seq(base_seq, shift_seq):
# -----------------------------------------------------------------------------
# Examples:
    '''
    >>> create_il_seq([0,1,2],[-1,0,2,1])
    [0, 0, 2, 1, 0, 1, 0, 2, 0, 2, 1, 0]
    '''  
    il_seq = []
    for i in range(0, len(base_seq)):
        for j in range(0, len(shift_seq)):
# Where the shift sequence has an infinity, the whole column is zeroes            
            if int(shift_seq[j]) == -1:
                il_seq.append(0)
            else: 
                il_seq.append(base_seq[(shift_seq[j] + i) % len(base_seq)])
    return il_seq


# circ_seq: list -> array
# Purpose: given a sequence, create the circulant covering array
# -----------------------------------------------------------------------------
def circ_seq(seq):
# -----------------------------------------------------------------------------    
# Example:
    '''
    circ_seq([0, 0, 1, 0, 1, 1, 1])
    [[0 0 1 0 1 1 1]
    [0 1 0 1 1 1 0]
    [1 0 1 1 1 0 0]
    [0 1 1 1 0 0 1]
    [1 1 1 0 0 1 0]
    [1 1 0 0 1 0 1]
    [1 0 0 1 0 1 1]]
    '''
    s = len(seq)
# It's easiest to create this first as a list of lists    
    new_mat = []
    for i in range(0, s):
        new_mat.append([])
        for j in range(0, s):
            new_mat[i].append(seq[(i+j) % s])
# Now create the actual array from the list of lists            
    new_array = numpy.array(new_mat, dtype=int) 
    return new_array    

# is_t_set_covered: array list integer -> Boolean
# Purpose: check a single t_set of a covering array
# ------------------------------------------------------
def is_t_set_covered(cover_array, t_set, v):
# ------------------------------------------------------
# Examples:
    '''
    >>> is_t_set_covered(numpy.array([[0,1,1],[1,0,1],[1,1,0]]), [0,1], 2)
    False
    >>> is_t_set_covered(numpy.array([[0,0],[0,1],[1,0],[1,1]]), [0,1], 2)
    True
    '''
# t was defined by the user, but we can get it from the length of the set    
    t = len(t_set)
# Take the rows indicated by the t_set and put them in a subarray    
    test_rows = cover_array[:,t_set].tolist()
    test_rows.sort()
# Take out any duplicates    
    test_rows = [i for n, i in enumerate(test_rows) if i not in test_rows[:n]]
# We simply check if the number of t-tuples is the number we need 
    if len(test_rows) == v**t:
        return True
    return False


# ------------------------------------------------------
# Main program begins here
# ------------------------------------------------------
# Run unit tests
doctest.testmod()
# ------------------------------------------------------
# Give your inputs/set parameters here
# ------------------------------------------------------
# What size of alphabet?  (The elements of the base_seq come from this)
v = 2
# What sequences are we testing today?
# Use the integer -1 to represent a shift of infinity.
base_seq = [0, 1, 1]
shift_seq = [-1, 0, 0, 2, 0]
# Set your parameters
t = 3 # strength to check for
# ------------------------------------------------------
# Here we go!
# ------------------------------------------------------
start_time = time()
total_sets = 0
num_covered = 0
il_seq = create_il_seq(base_seq, shift_seq)
cover_array = circ_seq(il_seq)
N = len(base_seq) * len(shift_seq)
for t_set in itertools.combinations(range(0, N), t):
    total_sets = total_sets + 1
    if is_t_set_covered(cover_array, t_set, v):
        num_covered = num_covered + 1
print('This array has' , num_covered, 't_sets covered out of', total_sets, '.')
print('Time taken (in seconds):', time()-start_time)