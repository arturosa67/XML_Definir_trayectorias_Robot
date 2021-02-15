# !/home/arturo/miniconda3/bin/env python3.4.2
# -*- coding: utf-8 -*- 
# 2015 ARTURO SUELVES ALBERT (ARTURO.SUELVES@GMAIL.COM)
# modulo de pruebaas para MATRICES HOMOGENEAS PARA ROBOTS.
# VERSIoN:2.0
# DATE: 12-12-2014

import RM
import unittest
import random 
from math import pi,cos,sin

#tests------------------------------------------------------------------------

class RoboMatrixTests(unittest.TestCase):
    def test_init_HM(self):
        #Test of Homogenous matrix
        m1 = RM.RoboMatrix.make_from_List([[1,2,3,4],[5,6,7,8],[9,10,11,12],
                                           [0,0,0,1]])
        self.assertTrue(m1.is_homogeneous_matrix())
    def test_init_RM(self):
        #test of Rotation matrix
        m1 = RM.RoboMatrix.make_from_List([[1,0,0],[0,cos(pi/4),-sin(pi/4)],
                                           [0,sin(pi/4),cos(pi/4)]])
        self.assertTrue(m1.is_rotation_matrix())
    def test_init_HV_1(self):
        #Test of Homogenous vector (rows)
        m1 = RM.RoboMatrix.make_from_List([[4],[3],[2],[1]])
        self.assertTrue(m1.is_homogenous_vector())
    def test_init_HV_2(self):
        #Test of Homogenous vector (columns)
        m1 = RM.RoboMatrix.make_from_List([[4,3,2,1]])
        self.assertTrue(m1.is_homogenous_vector())
    def test_init_V_1(self):
        #Test of Vector (columns)
        m1 = RM.RoboMatrix.make_from_List([[10,20,30]])
        self.assertTrue(m1.is_vector())
    def test_init_V_2(self):
        #Test of vector (rows)
        m1 = RM.RoboMatrix.make_from_List([[10],[20],[30]])
        self.assertTrue(m1.is_vector())

#    def test_add(self):
#        m1 = RM.RoboMatrix.make_from_List([[1], [2],[3],[1]])
#        m2 = RM.RoboMatrix.make_from_List([[1.1], [2.2],[3.3],[1]])       
#        #m3 = m1 + m2
#        self.assertRaises(RM.RoboMatrixError,m3=m1+m2)
#
#
#    def test_sub(self):
#        m1 = RM.RoboMatrix.make_from_List([[1, 2, 3], [4, 5, 6]])
#        m2 = RM.RoboMatrix.make_from_List([[7, 8, 9], [10, 11, 12]])        
#        m3 = m2 - m1
#        self.assertRaises(RM.RoboMatrixError)

    def test_mul_1(self):
        #Test of
        m1 = RM.RoboMatrix.make_from_List([[1,2,3,4],[5,6,7,8],[9,10,11,12],
                                           [0,0,0,1]])
        m2 = RM.RoboMatrix.make_from_List([[.1,.2,.3,.4],[.5,.6,.7,.8],
                                           [.9,.10,.11,.12],[0,0,0,1]])
        self.assertTrue(m1 * m2 == RM.RoboMatrix.make_from_List(
        [[3.8000000000000003,1.7,2.03,6.359999999999999],
         [9.8,5.3,6.469999999999999,15.64],[15.8,8.9,10.91,24.92],[0,0,0,1]]))

    def test_mul_2(self):
        m1 = RM.RoboMatrix.make_from_List([[1,0,0,-3],[0,1,0,10],[0,0,1,10],[0,0,0,1]])
        m2 = RM.RoboMatrix.make_from_List([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]])
        m3 = RM.RoboMatrix.make_from_List([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
        m4 = RM.RoboMatrix.make_from_List([[0.0,0.0,1.0,-3.0],[-1.0,0.0,0.0,10.0],
                                           [0.0,-1.0,0.0,10.0],[0.0,0.0,0.0,1.0]])
        self.assertTrue(m1*m2*m3 == m4)

    def test_transpose(self):
        m1 = RM.RoboMatrix.make_RandomMatrix(test_m, test_n)
        m2 = m1  
        m3 = m1.transpose()
        m4 = m2.transpose()
        self.assertTrue(m4 == m3)

    def test_id(self):
        m1 = RM.RoboMatrix.make_Id(test_n)
        m2 = RM.RoboMatrix.make_RandomMatrix(test_n, test_n)
        m3 = m2 * m1
        self.assertTrue(m3 == m2)
    
    def test_matlab(self):
        m1 = RM.RoboMatrix.make_RandomMatrix(test_m,test_n)
        cadena = m1.robomatrix_format_to_matlab_format()
        m2 = RM.RoboMatrix.make_RoboMatrix_from_format_matlab(cadena)
        self.assertTrue(m1 == m2) 

    def test_make_HM_from_ZYZ(self):
        m1 = RM.RoboMatrix.make_HM_from_ZYZ(0.34,0.2,0.3,100.5,100.4,100.3)
        self.assertTrue(m1.is_homogeneous_matrix() == True)

    def test_make_HM_from_ZXZ(self):
        m1 = RM.RoboMatrix.make_HM_from_ZXZ(0.34,0.2,0.3,100.5,100.4,100.3)
        self.assertTrue(m1.is_homogeneous_matrix() == True)

    def test_make_HM_from_RPY(self):
        m1 = RM.RoboMatrix.make_HM_from_RPY(0.34,0.2,0.3,100.5,100.4,100.3)
        self.assertTrue(m1.is_homogeneous_matrix() == True) 

    def test_get_element(self): 
        m1=RM.RoboMatrix.make_RandomMatrix(test_m,test_n)
        ele1=m1.get_element(test_row+1,test_colum+1)
        self.assertTrue(ele1 == m1.rows[test_row][test_colum])
         
    def test_set_element(self):
        m1 = RM.RoboMatrix.make_RandomMatrix(test_m,test_n)
        m1.set_element(test_row+1,test_colum+1,test_value)
        self.assertTrue(m1.rows[test_row][test_colum] == test_value)
    
    def test_norm_of_vector(self):
        m1 = RM.RoboMatrix.make_from_List([[0.34,0.2,0.3]])
        m2 = RM.RoboMatrix.make_from_List([[0.34],[0.2],[0.3]])
        self.assertTrue(m1.norm_of_vector() == m2.norm_of_vector() == 
                        0.4955804677345547)
                                                                   

#Test of boolean functions----------------------------------------------------        
    def test_issquare(self):
        m1 = RM.RoboMatrix.make_RandomMatrix(test_m,test_m)
        self.assertTrue(m1.get_range() == (test_m,test_m))
    def test_ishomogenous_matrix(self):
        m1 = RM.RoboMatrix.make_Id(4)
        self.assertTrue(m1.is_homogeneous_matrix)
        
    def test_ishomogenous_vector(self):
        m1 = RM.RoboMatrix.make_from_List([[4],[3],[2],[1]])
        self.assertTrue(m1.is_homogenous_vector)
    
    def test_extract_ori(self):
        m1 = RM.RoboMatrix.make_from_List([[1,2,3,4],[5,6,7,8],[9,10,11,12],
                                           [0,0,0,1]])
        self.assertTrue(m1.extract_ori() == [[1,2,3],[5,6,7],[9,10,11]])
    
    def test_extract_pos_from_HM(self):
        #test for matrix
        m1 = RM.RoboMatrix.make_from_List([[1,2,3,4],[5,6,7,8],[9,10,11,12],
                                           [0,0,0,1]])
        self.assertTrue(m1.extract_pos() == [4,8,12])
    def test_extract_pos_from_vector(self):
        #testfor vector
        m1 = RM.RoboMatrix.make_from_List([[1],[5],[9],[1]])
        self.assertTrue(m1.extract_pos() == [1,5,9])
        
        
   # def test_make_HM_from_ZYZ

if __name__ == "__main__":
    low=2
    high=100
    test_m = 4
    test_n = 4
    test_row = random.randrange(0, test_m)
    test_colum = random.randrange(0, test_n)
    test_value = random.randrange(1,1000)
 
    for i in range(1):
        unittest.main(verbosity=2)
