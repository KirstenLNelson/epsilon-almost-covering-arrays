"""
Created on Sat May  29 12:16:00 2021

@author: KirstenLNelson

A very naive Python program to generate all covering arrays with parameters 
CA(N;t,k,v) where you input your desired t, k, v, and N.
"""

from time import time
import itertools
import doctest
import math

# is_CA: matrix integer integer -> Boolean
# Purpose: check if a matrix is a covering array for a given strength
# ------------------------------------------------------
def is_CA(array, t, v):
# ------------------------------------------------------
    '''
    >>> is_CA([[0,0,1,1],[0,1,0,1]], 2, 2)
    True
    >>> is_CA([[0,0,1,1],[0,1,0,1],[1,0,1,0]], 2, 2)
    False
    >>> is_CA([[0,0,0,1,1],[0,1,0,0,1],[1,0,0,0,1],[0,0,1,0,1]], 2, 2)
    True
    >>> is_CA([[0,0,0,1,1],[0,1,0,0,1],[1,0,0,0,1],[0,0,1,0,1],[0,1,0,0,1]], 2, 2)
    False
    >>> is_CA([[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1]], 3, 2)
    True
    >>> is_CA([[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1]], 3, 2)
    False
    >>> is_CA([[0,0,0,0,0,1,1,1,1,1],[0,0,0,1,1,1,1,1,0,0],[0,1,0,1,0,1,1,0,0,1],[0,1,1,0,1,1,0,0,1,0]],3,2)
    True
    >>> is_CA([[0,0,0,0,0,1,1,1,1,1],[0,0,0,1,1,1,1,1,0,0],[1,0,0,1,0,1,1,0,0,1],[0,1,1,0,1,1,0,0,1,0]],3,2)
    False
    >>> is_CA([[0,0,0,0,1,1,1,1,2,2,2],[0,2,1,0,1,0,2,1,0,2,1],[1,0,0,2,2,1,1,0,0,2,1],[1,1,2,0,1,2,0,0,0,2,1],[2,0,1,1,0,0,1,2,0,2,1]],2,3)
    True
    '''
# The array may not be full size yet    
    len_array = len(array)
# We can only test the coverage if the number of columns is as big as the 
# strength, so just let it pass the test until then
    if len_array < t:
        return True
# We need to compare the new column to each one already in the array
    for t_set in itertools.combinations(range(len_array), t):
        if not is_t_set_covered(array, t_set, v):
            return False
    return True

# is_t_set_covered: matrix, list, integer -> Boolean
# Purpose: given a matrix and a set of columns, check if they are covered
# ------------------------------------------------------    
def is_t_set_covered(array, t_set, v):
# ------------------------------------------------------
# Examples:
    '''
    >>> is_t_set_covered([[0,0,1,1],[0,1,0,1],[1,0,1,0]], (1,2), 2)
    False
    >>> is_t_set_covered([[0,0,1,1],[0,1,0,1],[1,0,1,0]], (0,1), 2)
    True
    >>> is_t_set_covered([[0,0,0,1,1],[0,1,0,0,1],[1,0,0,0,1],[0,0,1,0,1]], (0,3), 2)
    True
    >>> is_t_set_covered([[0,0,0,1,1],[0,1,0,0,1],[1,1,0,1,0],[0,0,1,0,1]], (2,3), 2)
    False
    >>> is_t_set_covered([[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1]], (0,1,2), 2)
    True
    >>> is_t_set_covered([[0,0,0,0,1,1,1,1],[0,0,1,1,0,0,1,1],[0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1]], (1,2,3), 2)
    False
    '''
    t = len(t_set)
    row_set = []
# Cycle through the k column-rows of the array    
    for j in range(0, len(array[0])):
# Pull out the t-tuple and put it in the set  
        curr_tuple = []
        for m in range(0, len(t_set)):
            curr_tuple.append(array[t_set[m]][j])
        row_set.append([curr_tuple])
    row_set.sort()
# Eliminate the duplicates
    row_set = [i for n, i in enumerate(row_set) if i not in row_set[:n]]
# We need the number of unique tuples to be equal to v^t
    if len(row_set) == v**t:
        return True
    else:
        return False
        
# create_base_row: integer integer -> list 
# Purpose: Given the number of rows and symbols, return the first row        
# ------------------------------------------------------
def create_base_row(N, v):
# ------------------------------------------------------
# Examples:
    '''
    >>> create_base_row(10,3)
    [0, 0, 0, 0, 1, 1, 1, 2, 2, 2]
    >>> create_base_row(8,2)
    [0, 0, 0, 0, 1, 1, 1, 1]
    '''
# Initialize the list we'll be returning    
    base_row = []
# We'll be adding at least this many of each symbol; e.g. floor(10/3)=3, floor(8/2)=4.    
    base_num = math.floor(N/v)
# We'll be adding one extra of some symbols, starting with the smallest one, to make up the difference; 
# e.g. 10 % 3 = 1 so we'll add an extra 0, 8 % 2 = 0 so we don't need any extras.
    extra_num = N % v
# Loop over all the symbols we're adding    
    for k in range(0, v):
# For each symbol, add at least the base number        
        for l in range(0, base_num):
            base_row.append(k)
# If we're in the smaller numbers, add the extra symbol; e.g. for 10/3 we add an extra 0.
        if k < extra_num:
            base_row.append(k)
    return base_row
        
# create_second_row: list integer -> list 
# Purpose: Given a base row and the alphabet, return the second row        
# ------------------------------------------------------
def create_second_row(base_row, v):
# ------------------------------------------------------
# Examples:
    '''
    >>> create_second_row([0,0,0,0,1,1,1,2,2,2],3)
    [0, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    >>> create_second_row([0,0,0,0,1,1,1,1],2)
    [0, 0, 1, 1, 0, 0, 1, 1]
    >>> create_second_row([0,0,0,1,1],2)
    [0, 0, 1, 0, 1]
    >>> create_second_row([0,0,0,0,0,1,1,1,1,1],2)
    [0, 0, 0, 1, 1, 0, 0, 1, 1, 1]
    '''
# Initialize the list we'll be returning  
    row_buckets = []
    for k in range(0, v):
        row_buckets.append([])  
# Keep track of which bucket is next to dump an element in    
    bucket_num = 0
    for k in range(0, len(base_row)):
        row_buckets[bucket_num].append(base_row[k])
        bucket_num = (bucket_num + 1) % v
# Flatten the list of lists into a single list to return        
    second_row = [item for sublist in row_buckets for item in sublist]    
    return second_row

# search_CA: matrix, integer -> recursive call
# Purpose: a recursive search for covering arrays        
# ------------------------------------------------------
def search_CA(temp_array, i, t, k, v):
# ------------------------------------------------------
    global number_found
    global branches
    v_div_N = False
    if len(base_row) % v == 0:
        v_div_N = True
    if i == k and is_CA(temp_array, t, v):
        number_found = number_found + 1
        if number_found == 1:
            print(temp_array)
            print('in this many seconds: ', start_time - time())
        branches = branches + 1
    else:
        branches = branches + 1
# This is a terrible solution for the fact that we are getting each possible
# row four times more often than we need it.
        for column in list(set(itertools.permutations(base_row))):
# If v divides N, we can re-label a column to have a 0 in the first entry
            if (not v_div_N) or (v_div_N and column[0] == 0):
                new_array = temp_array[:]
                column = list(column)
# We want our rows to be in increasing order
                if column > new_array[-1]:
                    new_array.append(column)
                    if is_CA(new_array, t, v):
                        search_CA(new_array, i+1, t, k, v)

# ------------------------------------------------------
# Main program begins here
# ------------------------------------------------------
# Run unit tests
doctest.testmod()
# ------------------------------------------------------
# Set your parameters here
# ------------------------------------------------------
# Set your parameters for a CA(N;t,k,v)
N = 16
t = 2
k = 4
v = 5
# ------------------------------------------------------
# Here we go!
# ------------------------------------------------------
start_time = time()
number_found = 0
branches = 0
base_row = create_base_row(N, v)
row_two = create_second_row(base_row, v)
search_CA([base_row,row_two], 2, t, k, v)
print('number_found is: ', number_found)
print('number of branches is: ', branches)
end_time = time()
print('in: ', end_time - start_time, 'seconds.')
