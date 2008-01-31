#!/usr/bin/env python
""" Test functions for the splinalg.interface module
"""

from scipy.testing import *

import numpy
from numpy import array, matrix, ones, ravel
from scipy.sparse import csr_matrix

from scipy.splinalg.interface import *


class TestInterface(TestCase):
    def test_aslinearoperator(self):
        cases = []

        cases.append( matrix([[1,2,3],[4,5,6]]) )
        cases.append( array([[1,2,3],[4,5,6]]) )
        cases.append( csr_matrix([[1,2,3],[4,5,6]]) )

        class matlike:
            def __init__(self):
                self.dtype = numpy.dtype('int')
                self.shape = (2,3)
            def matvec(self,x):
                y = array([ 1*x[0] + 2*x[1] + 3*x[2],
                            4*x[0] + 5*x[1] + 6*x[2]])
                if len(x.shape) == 2:
                    y = y.reshape(-1,1)
                return y

            def rmatvec(self,x):
                if len(x.shape) == 1:
                    y = array([ 1*x[0] + 4*x[1],
                                2*x[0] + 5*x[1],
                                3*x[0] + 6*x[1]])
                    return y
                else:
                    y = array([ 1*x[0,0] + 4*x[0,1],
                                2*x[0,0] + 5*x[0,1],
                                3*x[0,0] + 6*x[0,1]])
                    return y.reshape(1,-1)

                return y
               
        cases.append( matlike() )


        for M in cases:
            A = aslinearoperator(M)
            M,N = A.shape

            assert_equal(A.matvec(array([1,2,3])),      [14,32])
            assert_equal(A.matvec(array([[1],[2],[3]])),[[14],[32]])

            assert_equal(A.rmatvec(array([1,2])),  [9,12,15])
            assert_equal(A.rmatvec(array([[1,2]])),[[9,12,15]])

            if hasattr(M,'dtype'):
                assert_equal(A.dtype, M.dtype)

if __name__ == "__main__":
    nose.run(argv=['', __file__])
