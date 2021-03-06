# -*- coding: utf-8 -*-
from random import randint, sample
from copy import copy
"""
This module provide some functions, that generate random permutations with different distributions. There are a uniform distribution and a symmetric distribution, which depends on some other permutation.
"""

def uniform( n ):
    """
    Generates random permutation using Knuth algorithm.
    
    Args:
        n (int) : length of permutation
        
    Returns: random permutation of length n from uniform distribution
    """
    
    #initialize permutation with identical
    permutation = [ i for i in xrange( n ) ]
    
    #swap ith object with random onject from i to n - 1 enclusively
    for i in xrange( n ):
        j = randint( i, n - 1 )
        permutation[ i ], permutation[ j ] = permutation[ j ], permutation[ i ]
        
    return permutation

def applyedTranspostions( basePermutation ):
    """
    This function returns random permutation by applying random traonspositions to given permutation.
    
    The result distribution is not uniform and summetric assuming parameter.
    
    Args:
        basePermutation (array) : parameter of distribution
        
    Returns: random permutation generated from basePermutation
    """
    
    n = len( basePermutation )
    """
    length of permutation
    """
    
    permutation = copy( basePermutation )
    """
    permutation to retur after some mpdifications
    we use a copy method, because initial arguments must leaved uncahnge
    """
    
    #apply n random transpositions (including identical) to base permutation
    for i in xrange( n ):
        k, l = sample( range( n ), 2 )
        permutation[ k ], permutation[ l ] = permutation[ l ], permutation[ k ]
        
    return  permutation