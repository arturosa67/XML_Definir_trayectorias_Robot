#/usr/bin/env python 
# -*- coding: utf-8 -*- 
# COPYRIGHT (C) 2014 ARTURO SUELVES ALBERT (ARTURO.SUELVES@GMAIL.COM) 
# PROGRAMA PARA GENERAR FICHERO RSL PARA EL ENTORNO DE SIMULACIÓN SIMPRO DE KUKA
# VERSIÓNN:1
#-----------------------------------------------------------------------------------
import os, os.path, sys
from math import pi

#definiciones de String-----------------------------------------------------------
CABECERA_RSL="""    <rrs2_Program version="2.4">
    <rrs2_ProgramName value="KR6_Programa"/>
    <rrs2_MainRoutine>
    <rrs2_RoutineBody>
    """
INICIO_FIN="""   <rrs2_PureMotionStatement>
    <Target>
    <Joints>
    <DOUBLE value="0.000000"/>
    <DOUBLE value="-90.000000"/>
    <DOUBLE value="90.000000"/>
    <DOUBLE value="0.000000"/>
    <DOUBLE value="0.000000"/>
    <DOUBLE value="0.000000"/>
    </Joints>
    <Parameters>
    <VALUE name="Interpolator::JointForce" value="100.000000"/>
    <VALUE name="Interpolator::JointSpeed" value="100.000000"/>
    <VALUE name="Interpolator" value="Joint"/>
    <VALUE name="Base" value="BASE[1]"/>
    <VALUE name="Tool" value="TOOL[1]"/>
    <VALUE name="KR 6::Configuration" value="010"/>
    <VALUE name="KR 6::Joint1" value="0.000000"/>
    <VALUE name="KR 6::Joint4" value="0.000000"/>
    <VALUE name="Interpolator::Synchronize" value="1"/>
    </Parameters>
    </Target>
    <Frame aw="0.000000" ax="0.000000" ay="-1.000000" az="0.000000" flags="1" name="IFP1" nw="0.000000" nx="0.000000" ny="-0.000000" nz="-1.000000" ow="0.000000" ox="1.000000" oy="0.000000" oz="0.000000" pw="1.000000" px="575.010986" py="-145.000000" pz="602.000002"/>
    </rrs2_PureMotionStatement>
    """
PIE_RSL="""    </rrs2_RoutineBody>
    </rrs2_MainRoutine>
    </rrs2_Program>
    """
MOVIMIENTO_TOPOINT="""
    <rrs2_PureMotionStatement>
    <Target>
    <Joints>
    <DOUBLE value="VALOR_ART_1"/>
    <DOUBLE value="VALOR_ART_2"/>
    <DOUBLE value="VALOR_ART_3"/>
    <DOUBLE value="VALOR_ART_4"/>
    <DOUBLE value="VALOR_ART_5"/>
    <DOUBLE value="VALOR_ART_6"/>
    </Joints>
    <Parameters>
    <VALUE name="Interpolator" value="Joint"/>
    <VALUE name="Base" value="BASE[1]"/>
    <VALUE name="Tool" value="TOOL[1]"/>
    <VALUE name="KR 6::Configuration" value="010"/>
    <VALUE name="KR 6::Joint1" value="0.000000"/>
    <VALUE name="KR 6::Joint4" value="0.000000"/>
    <VALUE name="Interpolator::JointSpeed" value="100.000000"/>
    <VALUE name="Interpolator::JointForce" value="100.000000"/>
    <VALUE name="Interpolator::Synchronize" value="1"/>
    </Parameters>
    </Target>
    <Frame aw="VALOR_AW" ax="VALOR_AX" ay="VALOR_AY" az="VALOR_AZ" flags="1" name="VALOR_NAME" nw="VALOR_NW" nx="VALOR_NX" ny="VALOR_NY" nz="VALOR_NZ" ow="VALOR_OW" ox="VALOR_OX" oy="VALOR_OY" oz="VALOR_OZ" pw="VALOR_PW" px="VALOR_PX" py="VALOR_PY" pz="VALOR_PZ"/>
    </rrs2_PureMotionStatement>
"""
MOVIMIENTO_LINE="""
     <rrs2_PureMotionStatement>
        <Target incomplete="1">
        <Joints>
        <DOUBLE value="VALOR_ART_1"/>
        <DOUBLE value="VALOR_ART_2"/>
        <DOUBLE value="VALOR_ART_3"/>
        <DOUBLE value="VALOR_ART_4"/>
        <DOUBLE value="VALOR_ART_5"/>
        <DOUBLE value="VALOR_ART_6"/>
        </Joints>
        <Parameters>
        <VALUE name="Interpolator" value="Linear"/>
        <VALUE name="Base" value="BASE[1]"/>
        <VALUE name="Tool" value="TOOL[1]"/>
        <VALUE name="KR 6::Configuration" value="010"/>
        <VALUE name="KR 6::Joint1" value="0.000000"/>
        <VALUE name="KR 6::Joint4" value="0.000000"/>
        <VALUE name="Interpolator::JointSpeed" value="100.000000"/>
        <VALUE name="Interpolator::JointForce" value="100.000000"/>
        <VALUE name="Interpolator::Synchronize" value="1"/>
        <VALUE name="Interpolator::MaxSpeed" value="1000.000000"/>
        <VALUE name="Interpolator::Acceleration" value="2000.000000"/>
        <VALUE name="Interpolator::Deceleration" value="2000.000000"/>
        <VALUE name="Interpolator::MaxAngularSpeed" value="180.000000"/>
        <VALUE name="Interpolator::AngularAcceleration" value="360.000000"/>
        <VALUE name="Interpolator::AngularDeceleration" value="360.000000"/>
        </Parameters>
        </Target>
        <Frame aw="VALOR_AW" ax="VALOR_AX" ay="VALOR_AY" az="VALOR_AZ" flags="1" name="VALOR_NAME" nw="VALOR_NW" nx="VALOR_NX" ny="VALOR_NY" nz="VALOR_NZ" ow="VALOR_OW" ox="VALOR_OX" oy="VALOR_OY" oz="VALOR_OZ" pw="VALOR_PW" px="VALOR_PX" py="VALOR_PY" pz="VALOR_PZ"/>
        </rrs2_PureMotionStatement>
     """


def generar_fichero_RSL(fichero_entrada, fichero_salida_RSL):
	print('entro')
	salida = ''
	salida= salida+CABECERA_RSL
	salida =salida+INICIO_FIN
	f_e=open(fichero_entrada,'r')
	lineas=f_e.readlines()
	f_e.close()

	for linea in lineas:
		print('entro')
		print('Linea leida:' + linea)
		lista=linea.split('==>')
		print('Datos leidos:',lista)
		tipo_mov=lista[0]
		print('Tipo de movimiento:',tipo_mov)
		name=lista[1]
		print('Nombre :' ,name)
		joints=lista[2].split(' ')
		print('Coordenadas articulares' ,joints)
		hm = lista[3].split(' ')
		print('MH:',hm)
		
		#Si es el KR6 como lleva 2 ejes externos hay que poner esto
		#ext1,ext2,j1,j2,j3,j4,j5,j6,espacio = joints		#sino esto
		j1,j2,j3,j4,j5,j6,espacio = joints
		
		
		if tipo_mov == 'TOPOINT':
			print('Entro al if de TOPOINT:')
			movimiento_TOPOINT='caca'
			movimiento_TOPOINT=MOVIMIENTO_LINE
			#SE PONE EL NOMBRE DEL PUNTO EN EL MOVIEMIENTO A ESCRIBIR
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_NAME', name)
			#SE PONEN LAS COORDENADAS ARTICULARES EN EL MOVIEMIENTO A ESCRIBIR
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_ART_1', str(float (j1)*180/pi))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_ART_2', str(float(j2)*180/pi))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_ART_3', str(float(j3)*180/pi))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_ART_4', str(float(j4)*180/pi))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_ART_5', str(float(j5)*180/pi))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_ART_6', str(float(j6)*180/pi))
			#SE PONEN LOS DATOS DEL FRAME (MATRIZ MH) EN EL MOVIMIENTO A ESCRIBIR
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_NX', str(hm[0]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_NY', str(hm[1]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_NZ', str(hm[2]))	
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_NW', str(hm[3]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_OX', str(hm[4]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_OY', str(hm[5]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_OZ', str(hm[6]))	
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_OW', str(hm[7]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_AX', str(hm[8]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_AY', str(hm[9]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_AZ', str(hm[10]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_AW', str(hm[11]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_PX', str(hm[12]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_PY', str(hm[13]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_PZ', str(hm[14]))
			movimiento_TOPOINT=movimiento_TOPOINT.replace('VALOR_PW', str(hm[15]))
			salida=salida+movimiento_TOPOINT
		if tipo_mov == 'LINE':
			movimiento_LINE='caca'
			movimiento_LINE=MOVIMIENTO_LINE
			#SE PONE EL NOMBRE DEL PUNTO EN EL MOVIEMIENTO A ESCRIBIR
			movimiento_LINE=movimiento_LINE.replace('VALOR_NAME', name)
			#SE PONEN LAS COORDENADAS ARTICULARES EN EL MOVIEMIENTO A ESCRIBIR
			movimiento_LINE=movimiento_LINE.replace('VALOR_ART_1', str(float (j1)*180/pi))
			movimiento_LINE=movimiento_LINE.replace('VALOR_ART_2', str(float(j2)*180/pi))
			movimiento_LINE=movimiento_LINE.replace('VALOR_ART_3', str(float(j3)*180/pi))
			movimiento_LINE=movimiento_LINE.replace('VALOR_ART_4', str(float(j4)*180/pi))
			movimiento_LINE=movimiento_LINE.replace('VALOR_ART_5', str(float(j5)*180/pi))
			movimiento_LINE=movimiento_LINE.replace('VALOR_ART_6', str(float(j6)*180/pi))
			#SE PONEN LOS DATOS DEL FRAME (MATRIZ MH) EN EL MOVIMIENTO A ESCRIBIR
			movimiento_LINE=movimiento_LINE.replace('VALOR_NX', hm[0])
			movimiento_LINE=movimiento_LINE.replace('VALOR_NY', hm[1])
			movimiento_LINE=movimiento_LINE.replace('VALOR_NZ', hm[2])
			movimiento_LINE=movimiento_LINE.replace('VALOR_NW', hm[3])
			movimiento_LINE=movimiento_LINE.replace('VALOR_OX', hm[4])
			movimiento_LINE=movimiento_LINE.replace('VALOR_OY', hm[5])
			movimiento_LINE=movimiento_LINE.replace('VALOR_OZ', hm[6])
			movimiento_LINE=movimiento_LINE.replace('VALOR_OW', hm[7])
			movimiento_LINE=movimiento_LINE.replace('VALOR_AX', hm[8])
			movimiento_LINE=movimiento_LINE.replace('VALOR_AY', hm[9])
			movimiento_LINE=movimiento_LINE.replace('VALOR_AZ', hm[10])
			movimiento_LINE=movimiento_LINE.replace('VALOR_AW', hm[11])
			movimiento_LINE=movimiento_LINE.replace('VALOR_PX', hm[12])
			movimiento_LINE=movimiento_LINE.replace('VALOR_PY', hm[13])
			movimiento_LINE=movimiento_LINE.replace('VALOR_PZ', hm[14])
			movimiento_LINE=movimiento_LINE.replace('VALOR_PW', hm[15])
			salida=salida+movimiento_LINE
	salida = salida + INICIO_FIN
	salida = salida + PIE_RSL

	f_s=open(fichero_salida_RSL,'w')
	f_s.write(salida)
	f_s.close()
	
if __name__ =='__main__':
	generar_fichero_RSL('./pruebas/salida/salida_matlab_Pieza2_Welding_KR16.txt','./pruebas/salida/programa_Pieza2_Welding_KR16.rsl')


