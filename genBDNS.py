# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:05:15 2021

@author: KirstenLNelson

Create balanced-difference near-starter vectors.
"""

from time import time
import collections
import doctest


# increment_shift_sequence: list integer -> list     
# Purpose: Return the next sequence in order for testing
# -----------------------------------------------------------------------------
def increment_shift_sequence(seq, s):
# -----------------------------------------------------------------------------
    '''
    >>> increment_shift_sequence([-1, 0, 0, 2, 0], 8)
    [-1, 0, 0, 2, 1]
    >>> increment_shift_sequence([-1, 0, 3, 3], 4)
    [-1, 1, -1, -1]
    >>> increment_shift_sequence([-1, 0, 0, 0, 2], 3)
    [-1, 0, 0, 1, -1]
    '''
    T = len(seq)
# Find the right-most spot with value < s
    found_position = False
    place_to_inc = 0
# Start at the end of the sequence    
    position = len(seq)-1
    while not found_position:
        if seq[position] != s-1:
            found_position = True
            place_to_inc = position
        position = position - 1
    seq[place_to_inc] = seq[place_to_inc] + 1  
    for i in range(place_to_inc+1, T):
        seq[i] = -1
    return seq    


# dup_set: list integer -> list
# Purpose: We need the next period of the shift sequence to calculate the differences 
# Adding 1 to each element is done mod s.       
# -----------------------------------------------------------------------------
def dup_seq(seq, s):
# -----------------------------------------------------------------------------
    '''
    >>> dup_seq([-1,0,0,2,0],3)
    [-1, 0, 0, 2, 0, -1, 1, 1, 0, 1]
    >>> dup_seq([-1,0,2,0,0],3)
    [-1, 0, 2, 0, 0, -1, 1, 0, 1, 1]
    '''
# Lists are immutable, so let's take a new one    
    new_seq = seq[:]
# Make sure it's actually a list    
    new_seq = list(new_seq)
    for i in range(0, len(seq)):
# An infinity plus 1 is still infinity, else add 1 mod s      
        if seq[i] == -1:
            new_seq.append(-1)
        else:
            new_seq.append((seq[i]+1)%s)
    return new_seq


# all_gaps_met: list integer -> Boolean
# Purpose: Test the differences at all possible separations
# Note that this function takes a duplicated sequence
# -----------------------------------------------------------------------------
def all_gaps_met(poss_seq, g):
# -----------------------------------------------------------------------------
    '''
    >>> all_gaps_met([-1,0,0,2,0,-1,1,1,0,1], 3)
    True
    >>> all_gaps_met([-1,0,0,0,0,-1,1,1,1,1], 3)
    False
    >>> all_gaps_met([-1,0,2,0,0,-1,1,0,1,1], 3)
    False
    >>> all_gaps_met([0,0,1,1,1,0], 2)
    True
    >>> all_gaps_met([0,0,1,0,0,1,1,2,1,1], 3)
    False
    >>> all_gaps_met([-1,0,0,1,0,0,-1,1,1,2,1,1], 3) 
    False
    >>> all_gaps_met([-1,0,1,0,0,-1,1,2,1,1], 3)
    True
    '''
# We took in a duplicated sequence, but we only need to test the first half
# And in fact, we only need to test the first half of the sequence    
    if len(poss_seq)/2 % 2 == 1:
        effective_length = (len(poss_seq)/2 -1)/2+1
    else:
        effective_length = len(poss_seq)/4+1
# Now go through all the possible distances and check them        
    for poss_gap in range(1, int(effective_length)):
        if not is_gap_met(poss_seq, poss_gap, g):
# As soon as a distance is found that doesn't work, fail out            
            return False
# If we made it here, everything is good        
    return True   


# is_gap_met: list integer integer -> Boolean
# Purpose: Given a sequence, the distance gap and the group, determine if all
#   the possible entries at that gap distance occur
# -----------------------------------------------------------------------------
def is_gap_met(seq, d, g):
# -----------------------------------------------------------------------------
    '''
    >>> is_gap_met([0,1,1,2,1,1,3,5,3], 2, 6)
    False
    >>> is_gap_met([0,1,1,2,1,1,3,5,3,1,2,2,3,2,2,4,6,4], 2, 6)
    False
    >>> is_gap_met([-1,-1,0,0,0,3,4,5,3,5,1,0,-1,-1,1,1,1,4,5,0,4,0,2,1], 2, 6)
    True
    >>> is_gap_met([-1,-1,0,0,0,3,4,5,3,5,1,0,-1,-1,1,1,1,4,5,0,4,0,2,1], 3, 6)   
    True
    >>> is_gap_met([-1,-1,0,0,0,3,4,5,3,5,1,0,-1,-1,1,1,1,4,5,0,4,0,2,1], 4, 6) 
    True
    >>> is_gap_met([-1,-1,0,0,0,3,4,5,3,5,1,0,-1,-1,1,1,1,4,5,0,4,0,2,1], 5, 6)  
    True
    >>> is_gap_met([-1,-1,0,0,0,3,4,5,3,5,1,0,-1,-1,1,1,1,4,5,0,4,0,2,1], 6, 6) 
    True
    >>> is_gap_met([0,0,0,1,1,0,3,4,6,3,1,1,1,2,2,1,4,5,0,4], 2, 7)
    True
    >>> is_gap_met([-1,0,2,0,0,-1,1,0,1,1],1,3)
    True
    >>> is_gap_met([-1,0,2,0,0,-1,1,0,1,1],2,3)
    False
    >>> is_gap_met([0,0,1,0,0,1,1,2,1,1],2,3)
    False
    >>> is_gap_met([-1,0,0,1,0,0,-1,1,1,2,1,1], 1, 3)
    True
    >>> is_gap_met([-1,0,0,1,0,0,-1,1,1,2,1,1], 2, 3)
    True
    >>> is_gap_met([-1,0,2,0,0,-1,1,0,1,1], 1, 3)
    True
    >>> is_gap_met([-1,0,2,0,0,-1,1,0,1,1], 2, 3)
    False
    >>> is_gap_met([-1,0,2,0,0,-1,1,0,1,1], 3, 3)
    False
    >>> is_gap_met([-1,0,1,0,0,-1,1,2,1,1], 1, 3)
    True
    >>> is_gap_met([-1,0,1,0,0,-1,1,2,1,1], 2, 3)
    True
    '''
# Initialize the collector for the gaps as a list (?)
    gaps = []
# Range through the possible starting positions, which is the first half
# Because duplicated sequences are passed in
    for i in range(0, int(len(seq)/2)):
# Ignore the elements of infinity for now   
        if seq[i] != -1 and seq[(i+d) % len(seq)] != -1:
# Calculate the gap for this starting place and distance                
            gap_to_add = seq[(i+d) % len(seq)]-seq[i]
# Make sure the gap we're adding is between 0 and g, otherwise adjust it            
            if gap_to_add > g:
                gap_to_add = gap_to_add - g
            if gap_to_add < 0:
                gap_to_add = gap_to_add + g
            if gap_to_add > g or gap_to_add < 0:
                print('error occurred here')
            gaps.append(gap_to_add)
# These three lines force each possible gap to occur        
# Make the list into a set, so we eliminate duplicates
    gap_reps = set(gaps)
# Do a simple count to see if they are all there    
    if len(gap_reps) != g:
        return False
# These four lines force the gaps to occur a nearly-equal number of times
# First turn the raw data into a counted collection, 
#   e.g. [0, 0, 1, 0] becomes Counter({0:3, 1:1})
    gap_counts = collections.Counter(gaps)
# What the heck is this test??? When is a counter True?    
    if gap_counts:
# If the max and min count differ by more than one, we are not balanced-diff        
        if max(gap_counts.values()) - min(gap_counts.values()) > 1:
            return False
# If we made it here, everything is good       
    return True
 
# is_smallest: List, Number -> Boolean
# Purpose: determine whether the given sequence is the canonical version    
# -----------------------------------------------------------------------------
def is_smallest(poss_seq, g):
# -----------------------------------------------------------------------------
    '''
    >>> # Test all rotations of a known sequence        
    >>> is_smallest([-1,0,0,2,0],3)
    True
    >>> is_smallest([0,0,2,0,-1],3)
    False
    >>> is_smallest([0,2,0,-1,1],3)
    False
    >>> is_smallest([2,0,-1,1,1],3)
    False
    >>> is_smallest([0,-1,1,1,0],3)
    False
    >>> # What if there are two infinities?
    >>> is_smallest([-1,-1,0,0,2,0,1],3)
    True
    >>> is_smallest([-1,0,0,2,0,1,-1],3)
    False
    >>> # What if there are two infinities not together?
    >>> is_smallest([-1,0,0,2,-1,0,1],3)
    True
    >>> is_smallest([-1,0,1,-1,0,0,2],3)
    False
    '''
    total_rotations = len(poss_seq)*g
    rotated_seq = poss_seq
    for i in range(0, total_rotations):
        rotated_seq = rotate_this(rotated_seq,g)
# We have proven that gaps are preserved with rotation, so no need to check        
#        if rotated_seq < poss_seq and all_gaps_met(dup_shift,g):
        if rotated_seq < poss_seq:
            return False
        if rotated_seq == poss_seq:
            return True
    return True            

# rotate_this: list integer -> list
# Purpose: Return a sequence rotated by one position
# -----------------------------------------------------------------------------
def rotate_this(poss_seq, g):
# -----------------------------------------------------------------------------
    '''
    >>> rotate_this([0,0,1,1],2)
    [0, 1, 1, 1]
    >>> rotate_this([-1,0,1,1],2)
    [0, 1, 1, -1]
    '''
    new_seq = poss_seq[1:]
    if poss_seq[0] != -1:
        new_seq.append((poss_seq[0]+1) % g)
    else: 
        new_seq.append(-1)
    return new_seq


# create_shifts: integer integer -> list
# Purpose: Given $s$ and $T$, yield all shifts
# -----------------------------------------------------------------------------
def create_shifts(s, T, num_inf):
# -----------------------------------------------------------------------------
    '''
    >>> next(create_shifts(3,2,0))
    [0, 0]
    '''
# This first shift contains infinities first, then zeroes    
    shift = [-1]*num_inf + [0]*(T-num_inf)
# Keep incrementing until we reach the largest possible shift    
    while shift < [0]+[s-1]*(T-1):
        yield shift
# Get the next shift in sequence        
        shift = increment_shift_sequence(shift, s)   
# There is one last one in the bucket that needs to go  
    yield shift   

# ------------------------------------------------------
# Main program begins here
# ------------------------------------------------------
# Run unit tests
doctest.testmod()
# ------------------------------------------------------
# Set your parameters here
# ------------------------------------------------------
# Set your parameters
T = 10  # Desired length of vector
s = 6   # Length of base sequence
gen_all = False # Set this to False to find only one; i.e., prove existence
# If you want to change the file name they are printed to, here you can
output_file_name = 'BDNS_T'+str(T)+'_s'+str(s)+'.txt'
# ------------------------------------------------------
# Here we go!
# ------------------------------------------------------
start_time = time()
number_found = 0
branches = 0
num_inf = int((T-1)/(s+1))
output_file = open(output_file_name, 'w')
keep_running = True
# Create a generator object for the shifts we can call repeatedly
shift_gen = create_shifts(s, T, num_inf)
#
while keep_running:
# We're going to naively generate all possible shifts
    shift = next(shift_gen)
# Only continue if the number of infinities is correct
    if shift.count(-1) == num_inf:
# We need to have two periods of the shift to calculate the gaps        
        dup_shift = dup_seq(shift, s)
# Check all the distances        
        if all_gaps_met(dup_shift, s) == True:
# Only continue if the shift is smallest lexicographically
            if is_smallest(shift, s):
                output_file.write(str(shift)+'\n')
                if number_found == 0:
                    print('I found you this BDNS: ', shift)
                    print('And it took this long: ', time() - start_time)
                    if gen_all == False:
                        keep_running = False
                number_found = number_found + 1
print('number_found is: ', number_found)
print('number of branches is: ', branches)
end_time = time()
print('in: ', end_time - start_time, 'seconds.')
output_file.close()
