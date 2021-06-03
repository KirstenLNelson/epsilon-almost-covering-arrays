# epsilon-almost-covering-arrays
Code for generating epilon-almost-covering-arrays and related discrete objects.

Program gencoverarrays creates covering arrays with parameter set CA(N; t, k, v).  To use, set the value of k to be your desired number of factors, the value t to be the desired strength, and v to be the size of the alphabet.   Set up a base row, which will normally be a near-balanced array of zeroes and ones; if the length is odd, add an extra zero.  The length of this base row controls N, the number of rows in your covering array.

The current version can find all covering arrays (some are isomorphic to others) up to k=10, N=6 in a few minutes.
