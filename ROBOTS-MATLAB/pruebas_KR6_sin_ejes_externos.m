%PROGRAMA DE CALCULO DE LAS COORDENADAS ARTICULARES DEL ROBOT KR6 PARA 
%CELULA ROBOTIZADA DE SOLDADURA PARA DEPOSITOS A PRESION (con 2 ejes base)
%Copyright (C) 2014 Arturo Suelves Albert <arturo.suelves@gmail.com> 
%Versión: 9
%#########################################################################

%INCIALIZACION DEL ENTORNO DE ROBOTICA Y CTES-----------------------------
clear;%borro el entorno por si aca
startup_rvc; %Inicializacion  de toolbox de robotica
con=pi/180; %cte de conversion de grados a radianes añadido por claridad 
            %para convertir gra. a rad.
%PARAMETROS DEL ROBOT K6--------------------------------------------------
%Definición de los Links según los parámetros de Denavitt-Hattenberg.


%##########################################################
%            theta     d       a       alpha   sigma(0=rot;1=prisma)
L(1) = Link([   0     675.0   260.0     -pi/2        0]);
L(2) = Link([   0       0     680.0       0          0]);
L(3) = Link([  pi/2     0        0       pi/2        0]);
L(4) = Link([   0     -670.0   -35.0    -pi/2        0]);
L(5) = Link([   0       0        0       pi/2        0]);
L(6) = Link([   0     -115.0     0        pi         0]);
%##########################################################

%Posición ZERO-HOME(reposo) del robot KR6
%qz =[0 0 pi/2 0 -pi/2 0 0 0];
qz =[0 0 -pi/2 0 0 0];
%##########################################################

%MH de la posición del robot respecto a sistema de coordenadas WORLD
base_robot=[1 0 0 0;0 1 0 0;0 0 1 0;0 0 0 1];
%MH de la herramienta de soldadura (TOOL)
tool_robot=[1 0 0 0;0 0.707 -0.707 0;0 0.707 0.707 300;0 0 0 1];% TORCH 45

%Definición del robot-----------------------------------------------------
ROBOT=SerialLink(L,'base', base_robot ,'tool',tool_robot);
%Limites de las articulaciones del robot [qmin qmax] (N x 2)
ROBOT.qlim=([-con*185 con*185;-con*155 con*35;-con*130 con*154;-con*350 con*350;
    -con*130 con*130;-con*350 con*350]);
ROBOT.name='KR6';
ROBOT.manuf='KUKA';
Q0=qz;
figure(1)
ROBOT.plot(Q0);
Tn=ROBOT.fkine(Q0);

[R,P]=tr2rt(Tn); %Imprimo la matriz de rota y la pos
disp('Posición:');
disp(P);
mensaje=['Representando Robot ',ROBOT.name,' de ',ROBOT.manuf];
disp(mensaje)
pausa=input('Pulse cualquier tecla para continuar.');

%DEFINICION DE FICHEROS---------------------------------------------------
%#########################################################################
 %Fichero de entrada de puntos y sus datos
  fichero_entrada = fopen('./G1.txt','r');
 %Fichero de salida de resultados
  fichero_salida = fopen('./salida_matlab_G1.txt','w');
%#########################################################################
%Procesado de ficheros----------------------------------------------------

%Leo la 1 linea del fichero 
linea = fgetl(fichero_entrada);
  
  while ischar(linea) %ischar() determina si es un array de caracteres
 
      nombre_punto=linea;
      disp(linea); %Display del texto o array
      linea_mh = fgetl(fichero_entrada);%lee la MH del punto a calcular 
      T=eval(linea_mh);
      %Calculo de las coordenadas articulares del robot (cinematica inversa) 
      %con incio en las coordenadas Q0
      Q = ROBOT.ikine(T, Q0,'pinv');
      %Ploteo del robot para visualizarlo.
      figure(1); 
      ROBOT.plot(Q,'name');
      Tn=ROBOT.fkine(Q);
      [R,P]=tr2rt(Tn); %Imprimo la matriz de rota y la pos
      disp('Posición:');
      disp(R);
      disp(P);
      
      
      
      %ROBOT.plotp(P);
        
      pausa=input('Posición OK?.Continuo(s/n)?','s');
      if pausa == 'n'
         ROBOT.teach('q0',Q0)
         N_J_C=input('Introduzca matriz con las nuevas coordenadas articulares:\n');
         Q = ROBOT.ikine(T,N_J_C,'pinv');
         figure(1)
         ROBOT.plot(Q,'name')
         Tn=ROBOT.fkine(Q);
         [R,P]=tr2rt(Tn);
          disp('Posición:');
         disp(P);
         Q0=Q; %Se escoje como punto de aproximacion inicial el anterior calculado
      else
         Q0=Q; %Se escoje como punto de aproximacion inicial el anterior calculado
      end
      %Lee siguiente linea del fichero de entrada
      linea=fgetl(fichero_entrada);
      
      %Escritura del fichero de salida con la matriz de coordenadas 
      %articulares calculada  
      fprintf(fichero_salida,nombre_punto);
      fprintf(fichero_salida,'==>');%escritura de un separador
      fprintf(fichero_salida,'%.3f ',Q);%escritura en fichero de salida de 
      %matriz Q con 3 decimales de precision
      fprintf(fichero_salida,'==>');%escritura de un separador
      Tn=ROBOT.fkine(Q);
      fprintf(fichero_salida,'%.3f ',Tn);%escritura en fichero de salida de 
      %matriz T la HM con 3 decimales de precision
      
      fprintf(fichero_salida,'\n');%escritura de un salto de linea
      
  end
  
 
 %Cierre de ficheros
 fclose(fichero_salida);
 fclose(fichero_entrada);
 



