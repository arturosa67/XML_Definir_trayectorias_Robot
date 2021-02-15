# !/usr/bin/env python3.4
# -*- coding: utf-8 -*- 
# COPYRIGHT (C) 2014 ARTURO SUELVES ALBERT (ARTURO.SUELVES@GMAIL.COM)
# PROGRAMA PARA LEER FICHERO XML TRAYECTORIAS Y PREPARARLOS PARASU PROCESADO
# EN MATLAB.
# VERSIÓN:1
# DATE: 10-12-2014
# -----------------------------------------------------------------------------------------
# Documentacion y notas:
# http://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree
# Uso las librerias standard de Python: xml.dom y minidom
# Python3.2
# Para la generación de los xml uso xmlcopyeditor (viene con DEbian)
# Debian 7.5
#
#  -----------------------------------------------------------------------------------
import sys 
import os.path
from xml.dom import minidom
#importar el modulo de libreria de robotics (RM.py)
ruta="./libreria-robotics-python/Version2/"
sys.path.append(os.path.abspath(ruta))

import RM

def comprobar_fichero_XML(ARG_fichero_xml_entrada):
	"""Genera un fichero con los puntos de los elementos del XML leidos a
	la descripción de los elementos a soldar de cada una de los grupos 
	del fichero."""
	try:
		# SE INTENTA LEER EL FICHERO XML DE DESCRIPCION DEL MODELO Y VER 
		# SI ESTA CORRECTAMENTE FORMADO COMO XML.SI NO LO ESTA SE SALE DEL PROGRAMA.
		minidom.parse(ARG_fichero_xml_entrada)
		print ('CORRECTO-El fichero '+ARG_fichero_xml_entrada+
			' leido.Parece bien formado como XML.')
	except:
		print('ERROR-El fichero '+ARG_fichero_xml_entrada+
			' no esta formado correctamente como XML.')
		exit()

def MH_segun_angles_type(ARG_x,ARG_y,ARG_z,ARG_a,ARG_b,ARG_c,ARG_angles_type):
	"""Segun el tipo de angilos leidos en el xml se elige entre uno u otro."""
	if ARG_angles_type == 'ZYZ':
		hm = RM.RoboMatrix.make_HM_from_ZYZ(float(ARG_a),float(ARG_b),float(ARG_c),
											float(ARG_x),float(ARG_y),float(ARG_z))
	elif ARG_angles_type == 'ZXZ': 
		hm = RM.RoboMatrix.make_HM_from_ZXZ(float(ARG_a),float(ARG_b),float(ARG_c),
											float(ARG_x),float(ARG_y),float(ARG_z))
	elif ARG_angles_type == 'RPY':
		hm = RM.RoboMatrix.make_HM_from_RPY(float(ARG_a),float(ARG_b),float(ARG_c),
											float(ARG_x),float(ARG_y),float(ARG_z))
	return hm
	
def procesar_LINE(ARG_nodo,ARG_hm):
	"""Procesado del elemento LINE del xml."""
	salida = ''
	x2,y2,z2 = ARG_nodo.getAttribute('xyz2').split(':')
	a2,b2,c2 = ARG_nodo.getAttribute('angles2').split(':')
	angles_type = ARG_nodo.getAttribute('angles_type')
	print ('   Punto2: ',x2 ,y2 ,z2)
	print ('   Ori2: ',a2 ,b2 ,c2)
	print ('   Angles type: ',angles_type)
	#aqui proceso la matriz pasada
		
	hm1 = ARG_hm * MH_segun_angles_type(x2,y2,z2,a2,b2,c2,angles_type)

	print ('   Matriz homogenea del punto2: \n'+ str(hm1))
	salida=salida+ARG_nodo.tagName+'==>'+ARG_nodo.getAttribute('name')+'\n'
	salida=salida+hm1.robomatrix_format_to_matlab_format()+'\n'
	return salida

def procesar_TOPOINT(ARG_nodo,ARG_hm):
	"""Procesado del elemento TOPOINT del xml."""
	salida = ''
	x2,y2,z2 = ARG_nodo.getAttribute('xyz').split(':')
	a2,b2,c2 = ARG_nodo.getAttribute('angles').split(':')
	angles_type = ARG_nodo.getAttribute('angles_type')
	print ('   Punto2: ',x2 ,y2 ,z2)
	print ('   Ori2: ',a2 ,b2 ,c2)
	print ('   Angles type: ',angles_type)
	#aqui proceso la matriz pasada
	hm1 =  ARG_hm * MH_segun_angles_type(x2,y2,z2,a2,b2,c2,angles_type)
	print ('   Matriz homogenea del punto2:\n '+ str(hm1))
	salida = salida+ARG_nodo.tagName+'==>'+ARG_nodo.getAttribute('name')+'\n'
	salida = salida+hm1.robomatrix_format_to_matlab_format()+'\n'    
	return salida

def procesar_ARC(ARG_nodo,ARG_hm):
	"""Procesado del elemento ARC del xml."""
	salida = ''
	x2,y2,z2 = ARG_nodo.getAttribute('xyz2').split(':')
	x3,y3,z3 = ARG_nodo.getAttribute('xyz3').split(':')
	a2,b2,c2 = ARG_nodo.getAttribute('angles2').split(':')
	a3,b3,c3 = ARG_nodo.getAttribute('angles3').split(':')
	angles_type = ARG_nodo.getAttribute('angles_type')
	print ('   Punto2: ',x2 ,y2 ,z2)
	print ('   Ori2: ',a2 ,b2 ,c2)
	print ('   Punto3: ',x3 ,y3 ,z3)
	print ('   Ori3: ',a3,b3 ,c3)
	print ('   Angles type: ',angles_type)
	#aqui proceso la matriz pasada
	hm1 = ARG_hm * MH_segun_angles_type(x2,y2,z2,a2,b2,c2,angles_type)

	
	print ('   Matriz homogenea del punto2:\n '+ str(hm1))
	salida = salida+ARG_nodo.tagName+'==>'+ARG_nodo.getAttribute('name')+'\n'
	salida = salida+hm1.robomatrix_format_to_matlab_format()+'\n'
	#aqui proceso la matriz pasada
	hm1 = ARG_hm * MH_segun_angles_type(x3,y3,z3,a3,b3,c3,angles_type)
	
	print ('   Matriz homogenea del punto3:\n '+ str(hm1))
	salida = salida+ARG_nodo.tagName+'==>'+ARG_nodo.getAttribute('name')+'\n'
	salida = salida+hm1.robomatrix_format_to_matlab_format()+'\n'
	return salida

def procesar_POLILINE(ARG_nodo,ARG_hm):
	"""Procesado del elemento POLILINE del xml."""
	salida = ''
	#salida = salida+ARG_nodo.tagName+'==>'+ARG_nodo.getAttribute('name')+'\n'
	for i in ARG_nodo.childNodes:
		if i.nodeType == 1: # ya que minidom coge tambien los nodos salto linea
			if i.tagName == 'LINE':
				salida=salida + procesar_LINE(i,ARG_hm)
	return salida
	

def procesar_GROUP(ARG_nodo,ARG_HM_from_WORLD_to_SITE):
	"""Procesa un nodo de tipo GROUP y devuelve un string con 
	los puntos y su hm"""
	salida=''
	grupo_nombre=ARG_nodo.getAttribute('name')
	print ('Procesando GROUP de nombre : ' + grupo_nombre)
	hm = ARG_nodo.getAttribute('HM_from_SITE_to_PART')
	print ('Leido HM_from_SITE_to_PART:'+hm)
	HM_from_SITE_to_PART = RM.RoboMatrix.make_RoboMatrix_from_format_matlab(hm)
	print ('HM_from_SITE_to_PART:\n'+ str(HM_from_SITE_to_PART))

	hm1 = ARG_HM_from_WORLD_to_SITE * HM_from_SITE_to_PART 
	
	
	#salida=salida+ARG_nodo.tagName+'==>'+ARG_nodo.getAttribute('name')+'\n'
	#aqui porceso el HM_from_WORLD_to_SITE con el HM_from_SITE_to_PART y lo paso
	 # procesado de las mh
	lista_elementos = ARG_nodo.childNodes
	# genero lista de elementos del grupo
	for elemento in lista_elementos:
		if elemento.nodeType == 1: 
			# ya que minidom coge tambien los nodos que son salto de linea
			# del fichero xml
			print (' Elemento : '+elemento.tagName),
			if elemento.tagName == 'LINE':
				salida=salida + procesar_LINE(elemento,hm1)
					
			if elemento.tagName == 'TOPOINT':
				salida=salida + procesar_TOPOINT(elemento,hm1)
				
			if elemento.tagName == 'ARC':
				salida=salida + procesar_ARC(elemento,hm1)
				
			if elemento.tagName == 'POLILINE':
				salida=salida + procesar_POLILINE(elemento,hm1)
					
			if elemento.tagName == 'TOOL':
				pass

	return salida

def procesar_INCLUDE(ARG_nodo,ARG_HM_from_WORLD_to_SITE):
	"""Procesa los include metidos en el fichero"""
	salida = ''
	nombre = ARG_nodo.getAttribute('name')
	print ('Procesando INCLUDE de nombre:'+nombre+'\n')
	fichero = ARG_nodo.getAttribute('file')
	grupo = ARG_nodo.getAttribute('group')
	print ('Procesando GROUP '+grupo+' del fichero '+fichero+'\n')
	OVERWRITE_HM_from_SITE_to_PART = ARG_nodo.getAttribute('OVERWRITE_HM_from_SITE_to_PART')
	if OVERWRITE_HM_from_SITE_to_PART != '':
		#entones cambio la HM_from_WORLD_to_SITE por la OvERWriTE
		pass
	#"aqui se proceasaria el fcihero"
	print ('Procesando INCLUDE de nombre : ' + nombre)
	salida=salida + ARG_nodo.tagName + '==>' + ARG_nodo.getAttribute('name') + '\n'
	return salida


def procesar_fichero_XML(ARG_fichero_xml_entrada,ARG_directorio_salida):
	"""Se leen todos los elementos del fichero xml"""

	documento_xml = minidom.parse(ARG_fichero_xml_entrada)
	listadenodos = documento_xml.documentElement
	# cojo el pimer nodo del elemento del que cuelgan todos

	try:
		# EL PRIMER NODO DEL DOCUMENTO ES EL PROCESS.OBLIGATORIO
		# SI NO SE PUEDEN LEER SE SALE DEL PROGRAMA.
		tipo_proceso = listadenodos.getAttribute('type')
		print('Leido tipo del proceso:'+tipo_proceso)
		unidades_proceso = listadenodos.getAttribute('units')
		print('Leido units del proceso:'+unidades_proceso)
		hm = listadenodos.getAttribute('HM_from_WORLD_to_SITE')
		print('Leído HM de WORLD to SITE:'+ hm)
		HM_from_WORLD_to_SITE = RM.RoboMatrix.make_RoboMatrix_from_format_matlab(hm)
		print ('HM_WORLD_to_SITE:\n'+str(HM_from_WORLD_to_SITE))
		
		
	except:
		print('ERROR-No se ha podido leer el type,units o HM del nodo inicial \
		PROCESS.')

# GENERACIÓN DE UNA LISTA CON Los grupos e includes QUE HAY EN EL FICHERO.    

	lista_grupos_includes = []
	for i in listadenodos.childNodes:
		if i.nodeType == 1:
			if i.tagName == 'GROUP' or 'INCLUDE':
				lista_grupos_includes.append(i)

	print('Generada lista de GROUPS e INCLUDES.')
# ---------------------------------------------------------------
# fichero donde escribir la salidas
	
	#normalizo el directorio de salida y compruebo si existe
	d_s= os.path.normpath(ARG_directorio_salida)
	if not(os.path.exists(d_s)):
		print('Directorio de salida no existe.!!!')
		sys.exit(1)

	for i in lista_grupos_includes:
		f_s=os.path.join(d_s, i.getAttribute('name'))#uno el directorio y nombre fic
		fichero_salida = open(f_s+'.txt', 'w')
		if i.tagName == 'GROUP':
			fichero_salida.write(procesar_GROUP(i,HM_from_WORLD_to_SITE))
		if i.tagName == 'INCLUDE':
			fichero_salida.write(procesar_INCLUDE(i,HM_from_WORLD_to_SITE))
		fichero_salida.close()

if __name__ == '__main__':
	# LLAMADA A LA FUNCIÓN generar_fichero_puntos_MATLAB CON LOS NOMBRES DE LOS
	# FICHEROS DE ENTRADA Y DE SALIDA.
	comprobar_fichero_XML('./pruebas/pieza1_welding.xml')
	procesar_fichero_XML('./pruebas/pieza1_welding.xml', './pruebas/salida/')
