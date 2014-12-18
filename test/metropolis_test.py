#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import unittest
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import metropolis
import scipy.stats
"""
Unit test of metropolis and density maximization algorithm.
"""

class TestMetropolis( unittest.TestCase ):
    def setUp( self ):
        """
        For test cases we setting up desired distribution to normal with mean 10 and variance 25. For a computable generator we use also normal distribution with mean as a parameter. All algorithms are tested on samples with size 10000.
        """
        
        self.desiredDistribution = scipy.stats.norm( loc = 10, scale = 5 )
        self.computableGen = lambda t: scipy.stats.norm( loc = t ).rvs()
        
        self.n = 10000
	self.skipSteps = 5000
        
    def test_metropolis( self ):
        """
        Testing metropolis algorithm using KS test.
        """
        
        metropolisGen = metropolis.metropolis( self.desiredDistribution.pdf, 0, self.computableGen, self.skipSteps )
        
        #sample from generator
        x = []
        for i in xrange( self.n ):
            x.append( metropolisGen.next()[0] )
            
        #check using KS test, that produxed sample is from given distribution
        KSPValue = scipy.stats.kstest( x, self.desiredDistribution.cdf )[ 0 ]
        
        #if p value is greater than 0.05, we should accept hypotisys, that sample from given distribution
        self.assertGreater( KSPValue, 0.05 )
        
    def test_densityMaximization( self ):
        """
        Testing density maximization algorithm, comparing density of each object with next object from sample.
        """
        
        densityMaximization = metropolis.densityMaximization( self.desiredDistribution.pdf, 0, self.computableGen, self.skipSteps )
        
        #in a cycle check that density of next pbject is not less than of current one
        densityValueOld = None
        densityValueNew = densityMaximization.next()[1]
        for i in xrange( self.n ):
            densityValueOld = densityValueNew
            densityValueNew = densityMaximization.next()[1]
            self.assertLessEqual( densityValueOld, densityValueNew )

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase( TestMetropolis )
    unittest.TextTestRunner(verbosity=2).run(suite)
