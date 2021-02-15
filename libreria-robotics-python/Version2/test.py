# !/home/arturo/miniconda3/bin/env python3.4.2
# -*- coding: utf-8 -*- 
# 2015 ARTURO SUELVES ALBERT (ARTURO.SUELVES@GMAIL.COM)
# pruebas PARA OPERAR MATRICES HOMOGENEAS PARA ROBOTS.
# VERSIoN:1.0
# DATE: 12-12-2014
import RM
from math import cos,pi
#Prueba de multiplicar HM
#m1 = RM.RoboMatrix.make_from_List([[1,0,0,-3],[0,1,0,10],[0,0,1,10],[0,0,0,1]])
#m2 = RM.RoboMatrix.make_from_List([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]])
#m3 = RM.RoboMatrix.make_from_List([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])
#m4=m1*m2*m3
#print (m4)
##Prueba
#m5=RM.RoboMatrix.make_from_List([[1,0,0,1000],[0,1,0,0],[0,0,1,500],[0,0,0,1]])
#m6 = RM.RoboMatrix.make_from_List([[-250],[-250],[0],[1]])
#print(m5*m6)
#m7=RM.RoboMatrix.make_HM_from_ZYZ(3*pi/2,0,0,0,0,0)
#m8=RM.RoboMatrix.make_from_List([[-250],[-250],[0],[1]])
#print(m7)
#print(m7*m8)
#print(cos(180))

m1=RM.RoboMatrix.make_HM_from_RPY(pi/4,0,0,0,0,300)
print (m1)


