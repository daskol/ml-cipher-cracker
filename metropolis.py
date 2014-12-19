# -*- coding: utf-8 -*-
from random import random, seed
from math import log
"""
This module implements algorithm of Metropolis-Hastings for random variable generation.

The algorithm generate random variables from a disered distribution (which may be unnormalized).
"""

def metropolis( desiredPDF, initValue, computableRVS, skipIterations = 200 ):
    """
    This function return a generator, which generates random variables from some space S with a desired distribution using Metropolis-Hastings algorithm.
    
    Args:
        desiredPDF (func) : PDF of desired distribution p( T ), where T from S
        initValue : an object from S to initialize the starting point of iterative proccess
        computableRVS (func) : a generator of random value from space S with given parameter T, which is also from S
        skipIterations (int) : number of iterations to skip (skipping more iterations leads to better accuracy? but greater time consuming)
        
    Returns: generator, which produce some values from S and their denisity according to distribution desiredPDF
    """

    seed()

    random_variable = initValue
    random_variableDensityValue = desiredPDF( random_variable )
    """
    A state of MCMC
    """
    
    #ignore first iterations to let the iterative proccess to converge to some distribution, which is close to desired
    for i in xrange( skipIterations ):
        candidate = computableRVS( random_variable )
        candidateDensityValue = desiredPDF( candidate )        
        """
        next candidate for sample, generated by computableRVS
        """
        
        acceptanceProb = min( 0, candidateDensityValue - random_variableDensityValue )
        """
        probability to accept candidate to sample
        """

        print(candidate, candidateDensityValue)
        
        if log( random() ) < acceptanceProb:
            random_variable = candidate
            random_variableDensityValue = candidateDensityValue
            
    #now when the procces is converged to desired distribution, return acceptable candidates
    while True:
        print('While loop')
        candidate = computableRVS( random_variable )
        candidateDensityValue = desiredPDF( candidate )
        """
        next candidate for sample, generated by computableRVS
        """
        
        acceptanceProb = min(0, candidateDensityValue - random_variableDensityValue)
        """
        probability to accept candidate to sample
        """

        print(candidate, candidateDensityValue)
        
        if log( random() ) < acceptanceProb:
            print('Update')
            random_variable = candidate
            random_variableDensityValue = candidateDensityValue
        yield random_variable, random_variableDensityValue

def densityMaximization( desiredPDF, initValue, computableRVS, skipIterations = 200 ):
    """
    This function return a generator, which generates random variables from some space S by trying to maximize givven density. The algorithm is a modification of Metropolis-Hastings. It rejects all objects, which decrease density.
    
    Args:
        desiredPDF (func) : PDF of desired distribution p( T ), where T from S
        initValue : an object from S to initialize the starting point of iterative proccess
        computableRVS (func) : a generator of random value from space S with given parameter T, which is also from S
        skipIterations (int) : number of iterations to skip (skipping more iterations leads to better accuracy? but greater time consuming)
        
    Returns: generator, which produce some values from S, where each next value has no less density, and their denisity
    """

    seed()

    random_variable = initValue
    random_variableDensityValue = desiredPDF( random_variable )
    """
    A state of MCMC
    """
    
    #ignore first iterations to let the iterative proccess to enter the high density regions
    for i in xrange( skipIterations ):
        candidate = computableRVS( random_variable )
        candidateDensityValue = desiredPDF( candidate )
        """
        next candidate for sample, generated by computableRVS
        """
        
        if random_variableDensityValue < candidateDensityValue:
            random_variable = candidate
            random_variableDensityValue = candidateDensityValue
            
    #now when the procces is in high density regions, return acceptable candidates
    while True:
        candidate = computableRVS( random_variable )
        candidateDensityValue = desiredPDF( candidate )
        """
        next candidate for sample, generated by computableRVS
        """
        
        if random_variableDensityValue < candidateDensityValue:
            random_variable = candidate
            random_variableDensityValue = candidateDensityValue
        yield random_variable, random_variableDensityValue
