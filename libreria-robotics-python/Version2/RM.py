#!/home/arturo/miniconda3/bin/env python3.4.2
# -*- coding: utf-8 -*- 
# 2015 ARTURO SUELVES ALBERT (ARTURO.SUELVES@GMAIL.COM)
# modulo sencillo PARA OPERAR MATRICES HOMOGENEAS Y DE ROTACION PARA ROBOTS.
# VERSIoN:2.0
# DATE: 12-12-2014
# -----------------------------------------------------------------------------------------
import random
from math import cos, sin ,sqrt


__version__ = "1.0"
__author__ = "Arturo Suelves. Check for Python v3 "
__email__ = "arturo.suelves@gmail.com"
    
class RoboMatrixError(Exception):
    """ Exception class for RoboMatrix. """
    pass

#Class definition-----------------------------------------------------------
#All instance methods in minus
class RoboMatrix(object):
    """ A simple Python matrix class with basic operations and operator 
    overloading for homogenous matrix, homogenous vectors, rotation matrix and
    vectors, for use in Robotics.
    This module call all these matrix RoboMatrix."""

    def __init__(self, m, n):
        """4x4: Homogenous Matrix.
           4x1 and 1x4: Homogenous Vectors.
           3x3: Rotation Matrix.
           3x1 and 1x3: Vectors."""
        if ((m == n == 4) or (m == 4 and n==1) or (m == 3 and n == 3) or 
        (m==1 and n==4) or (m ==3 and n ==1) or (m==1 and n ==3)):
            self.rows = [[0.0]*n for x in range(m)]
            self.m = m
            self.n = n
        else:
            raise RoboMatrixError("No matrix,vector or homogenous.")
        
    def get_element(self,fila,columna):
        """Get element fila x columna"""
        return (self.rows[fila-1][columna-1])
    def set_element(self,fila,columna,valor):
        """Set value in element fila x columna."""
        self.rows[fila-1][columna-1]=valor
    def about(self):
        """Print information of the RoboMatrix (rows and comuns number,range."""
        print('Information:\n')
        print('Class:'+ str(self.__class__))
        print('Rows number: '+ str(self.m))
        print('Columns number: '+ str(self.n))
        print('Items number: '+ str(self.m * self.n))
        print('Matrix range: '+ str(self.get_range()))
        print(self)
        
    def __getitem__(self, idr):
        """Get row of RoboMatrix."""
        return self.rows[idr]

    def __setitem__(self, idr, valor):
        """Set row in Robomatrix"""
        self.rows[idr] = valor
        
    def __str__(self):
        """How to print RoboMatrix. """
        maxlen = 0 
        for row in self.rows:
            for item in row:
                long=len(str(item))
                if long > maxlen:
                    maxlen=long
        maxlen=maxlen+1
        s='\n'.join([' '.join([str(item).rjust(maxlen) for item in row]) 
        for row in self.rows])
        return s + '\n'

    def __repr__(self):
        """How represent RoboMAtrix. """
        s=str(self.rows)
        rank = str(self.get_range())
        rep="RoboMatrix:\"%s\",range: \"%s\"" % (s,rank)
        return rep

    def transpose(self):
        """ Return a transpose of the RoboMatrix"""
        m, n = self.n, self.m
        robomatrix = RoboMatrix(m, n)
        robomatrix.rows =  [list(i) for i in zip(*self.rows)]
        return robomatrix
        
    def inverse_HM(self):
        """Return inverse of the RoboMatrix"""
        pass
    
    def inverse_RM(self):
        """Return inverse of rotation matrix """
        if self.is_rotation_matrix:
            aux_mat=self.transpose()
            return aux_mat
        else:
            raise RoboMatrixError('Cannot give inverse_RM.')
    
    def get_range(self):
        """Return range of the RoboMAtrix."""
        return (self.m, self.n)

    def __eq__(self, robomatrix):
        """ Test equality. """
        return (robomatrix.rows == self.rows)
        
    def __add__(self, robomatrix):
        """ Add a RoboMatrix to this RoboMatrix and
        return the new RoboMatrix."""     
        raise RoboMatrixError("No defined homogeneous matrix addition.")

    def __sub__(self, robomatrix):
        """ Subtract a RoboMatrix from this RoboMatrix and
        return the new RoboMatrix."""
        raise RoboMatrixError("No defined homogeneous matrix substraction.")

    def __mul__(self, robomatrix):
        """ Multiple a RoboMatrix with this RoboMatrix and
        return the new RoboMatrix."""
        
        robomatrixm, robomatrixn = robomatrix.get_range()
        
        if (self.n != robomatrixm):
            raise RoboMatrixError("RoboMatrix cannot be multipled!.")
        
        robomatrix_t = robomatrix.transpose()
        mulrobomatrix = RoboMatrix(self.m, robomatrixn)
        
        for x in range(self.m):
            for y in range(robomatrix_t.m):
                mulrobomatrix[x][y] = sum([float(item[0])*float(item[1]) for 
                    item in zip(self.rows[x], robomatrix_t[y])])

        return mulrobomatrix
        
    def robomatrix_format_to_matlab_format(self):
        """Give the RoboMatrix in MATLAB format.
        MATLAB format is like a list with rows separate by ; ."""
        A = '['
        for i in self.rows:
            for ii in i:
                A = A + str(ii) + ' '
            A = A[0:len(A) - 1]
            A = A + ';'
        A = A[0:len(A) - 1] + ']'
        return A 
        
    def extract_ori(self):
        """Extract the rotation part (3x3) of RoboMatrix like a list of lists."""
        if self.is_homogeneous_matrix:
            aux=list()
            for i in self.rows[0:3]:
                aux.append(i[0:3])
        return aux

    def extract_pos(self):
        """Extract the position part (3x3) of RoboMatrix like a list of lists."""
        aux=list()
        if self.is_homogeneous_matrix():
            for i in self.rows[0:3]:
                aux.append(i[3])
        elif self.is_homogenous_vector():
            for i in self.rows[0:3]:
                aux.append(i[0])
        return aux
        
    def norm_of_vector(self):
        """Give the vector norm. """
        if self.is_vector :
            norm=0.0
            for i in self.rows:
                for ii in i:
                    norm =ii*ii+norm
        return sqrt(norm)
                


#Boolean Functions-----------------------------------------------------------
#All boolean functions begin with is_
    def is_square(self):
        """Check if Matrix is square."""
        aux = False
        if self.m == self.n:
            aux = True
        return aux
    def is_homogeneous_matrix(self):
        """Check if Matrix is homogenous."""
        aux = False
        if ((self.m == 4) and (self.n == 4)):
            if self.rows[3] == [0.0,0.0,0.0,1.0]:
                aux = True
        return aux
    def is_homogenous_vector(self):
        """Check if Vector is homogenous."""
        aux = False
        if (self.m == 4 and self.n ==1):
            if self.rows[3] == [1]:
                aux = True
        if (self.m ==1 and self.n ==4):
            if self.rows[0][3]==1:
                aux =True
        return aux
    def is_rotation_matrix(self):
        """Check if Matrix is a Rotation Matrix."""
        #ya que A por inv(A) debe ser I osea transpost(A)=inverse(A)
        aux = False
        if (self.m ==3 and self.n ==3):
            aux1_mat=self.transpose()
            aux2_mat=self*aux1_mat
            aux3_mat=RoboMatrix.make_Id(3)
            if aux2_mat == aux3_mat:
                aux = True
        return aux
    def is_vector(self):
        """Check if Vector is a vector."""
        aux = False
        if ((self.m ==3 and self.n==1) or (self.m ==1 and self.n==3)):
            aux = True
        return aux

#Class Methods-------------------------------------------------------------
#All class methods begin with make_
    @classmethod
    def make_RoboMatrix(cls, rows):
        """Make of RoboMatrix. """
        m = len(rows)
        n = len(rows[0])
        # Validity check
        if any([len(row) != n for row in rows[1:]]):
            raise RoboMatrixError("Inconsistent row length.")
        cls = RoboMatrix(m,n)
        cls.rows = rows
        return cls
        
    @classmethod
    def make_RandomMatrix(cls, m, n, low=1.0, high=100.0):
        """Make a random RoboMatrix with elements in range (low-high)."""      
        cls = RoboMatrix(m, n)
        for i in range(m):
            for ii in range(n):
                cls.rows[i][ii]= random.randrange(low, high)
        return cls


    @classmethod
    def make_Id(cls, m):
        """ Make identity RoboMatrix of rank (mxm). """
        rows = [[0.0]*m for x in range(m)]
        idr = 0      
        for row in rows:
            row[idr] = 1
            idr = idr +1
        return cls.make_from_List(rows)
    
    @classmethod
    def make_from_List(cls, listoflists):
        """ Create a RoboMatrix by a list of lists. """
        # Ej: RoboMatrix.make_from_List([[1 2 3], [4,5,6], [7,8,9]])
        rows = listoflists[:]
        return cls.make_RoboMatrix(rows)

    @classmethod    
    def make_RoboMatrix_from_format_matlab(cls, ARG_string):
        """Paso formato MATLAB al de lista de listas"""
        list_aux=ARG_string[1:-1].split(';') #quito los [ y separo por;
        lista1=[]
        for i in list_aux:
            lista2=[]
            for ii in i.split(' '):
                lista2.append(float(ii))
            lista1.append(lista2)        
        #return lista1
        return cls.make_from_List(lista1)


    @classmethod
    def make_HM_from_ZYZ(cls,angle_z1, angle_y, angle_z2, px, py, pz,escala=1.0):
        """Calculate a MH by ZYZ Euler angles.Angles in radians. 
        Parameters:angle_z1, angle_y, angle_z2: Euler angles.
        px, py, pz: point coordinates.
        Important: First translate to point, next rotation."""
        # REFERENCIA-BIBLIOGRAFIA:INTRODUCCION A LA ROBOTICA. PAG.87
        f1 = [round(cos(angle_z1)*cos(angle_y)*cos(angle_z2)-sin(angle_z1)*sin(angle_z2), 3),
              round(-cos(angle_z1) * cos(angle_y) * sin(angle_z2) - sin(angle_z1) * cos(angle_z2), 3),
              round(cos(angle_z1) * sin(angle_y), 3), px]
        f2 = [round(sin(angle_z1) * cos(angle_y) * cos(angle_z2) + cos(angle_z1) * sin(angle_z2), 3),
              round(-sin(angle_z1) * cos(angle_y) * sin(angle_z2) + cos(angle_z1) * cos(angle_z2), 3),
              round(sin(angle_z1) * sin(angle_y), 3), py]
        f3 = [round(-sin(angle_y) * cos(angle_z2), 3), round(sin(angle_y) * sin(angle_z2), 3), 
        round(cos(angle_y), 2), pz]
        f4 = [0.0, 0.0, 0.0, escala]
        aux = [f1, f2, f3, f4] #matriz de lista de listas (por filas)
        return cls.make_from_List(aux)

    @classmethod
    def make_HM_from_ZXZ(cls,angle_z1, angle_x, angle_z2, px, py, pz,escala=1.0):
        """Calculate a MH by ZXZ Euler angles.Angles in radians.
        Parameters:angle_z1, angle_x, angle_z2:Euler angles.
        px, py, pz:point coordinates.
        Important: First translate to point, next rotation."""        
        f1 = [round(cos(angle_z1) * cos(angle_z2) - sin(angle_z1) * cos(angle_x) * sin(angle_z2), 3),
              round(-cos(angle_z1)* sin(angle_z2) - sin(angle_z1) *cos(angle_x)* cos(angle_z2), 3),
              round(cos(angle_z1) * sin(angle_x), 3), px]           
        f2 = [round(sin(angle_z1) * cos(angle_z2) + cos(angle_z1) *cos(angle_x)* sin(angle_z2), 3),
              round(-sin(angle_z1) * sin(angle_z2) + cos(angle_z1) *cos(angle_x)* cos(angle_z2), 3),
              round(-sin(angle_z1) * sin(angle_x), 3), py]      
        f3 = [round(sin(angle_x) * cos(angle_z2), 3), round(sin(angle_x) * cos(angle_z2), 3), 
        round(cos(angle_x), 3), pz]
        f4 = [0.0, 0.0, 0.0, escala]
        aux = [f1, f2, f3, f4] #matriz de lista de listas (por filas)
        return cls.make_from_List(aux)
    
    @classmethod
    def make_HM_from_RPY(cls,x, y, z, px, py, pz,escala=1.0):
        """Calculate a MH by Euler angles Roll-Pitch-Yaw.Angles in radians. 
        Parameters:roll, pitch, yaw :Euler angles.
        px, py, pz: point coordinates.
        Important: First translate to point, next rotation."""   
        f1 = [round(cos(z) * cos(y) , 3),round(cos(z)* sin(y)*sin(x) - sin(z) *cos(x), 3),
              round(cos(z) * sin(y)*cos(x)+sin(z)*sin(x), 3), px] 
        f2 = [round(sin(z) * cos(y), 3),
              round(sin(z) * sin(y)*sin(x) + cos(z) *cos(x), 3),
              round(sin(z) *sin(y)* cos(x)-cos(z)*sin(x), 3), py] 
        f3 = [round(sin(y), 3), round(cos(y) * sin(x), 3), 
        round(cos(y)*cos(x), 3), pz]
        f4 = [0.0, 0.0, 0.0, escala]
        aux = [f1, f2, f3, f4] #matriz de lista de listas (por filas)
        return cls.make_from_List(aux)
    
    @classmethod   #Creo que hay que poner en estas que sean 4X4-------------------
    def make_RM_around_X(cls,angle):
        """Make a Rotation Matrix around X axis of angle."""
        aux = [[1.0,0.0,0.0],[0.0,cos(angle),-sin(angle)],
               [0.0,sin(angle),cos(angle)]]
        return cls.make_from_List(aux)

    @classmethod   
    def make_RM_around_Y(cls,angle):
        """Make a Rotation Matrix around Y axis of angle."""
        aux = [[cos(angle),0.0,sin(angle)],[0.0,1.0,0.0],
               [-sin(angle),1.0,cos(angle)]]
        return cls.make_from_List(aux)

    @classmethod   
    def make_RM_around_Z(cls,angle):
        """Make a Rotation Matrix around Z axis of angle."""
        aux = [[cos(angle),-sin(angle),0.0],[sin(angle),cos(angle),0.0],
               [0.0,0.0,1.0]]
        return cls.make_from_List(aux)

    @classmethod
    def make_RM_around_AXIS(cls,vector,angle):
        """Make a Rotation Matrix around an axis (x,y,z)."""
        if vector.is_vector():
            if vector.norm_of_vector() == 1.0:
                pass
        pass
        
    
        
        
        
        
        
        
        
        
    
