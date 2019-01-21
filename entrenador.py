# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 19:38:09 2019

@author: Hollwann & Gina
"""
import random
import version1
import numpy as np
import tensorflow as tf
from tensorflow import keras
import datetime


'''Variables importantes'''
n_cubos = 1000   #numero de cubos para el entrenamiento
max_mov_dist=6 #numero maximo de movimientos distancia
log=[]
 
for iteracion in range(1000):
    
    def build_model():
      model = keras.Sequential([
              keras.layers.Conv2D(random.randint(4,20), kernel_size=(4, 4),   #(numero del filtros ,tamaño del filtro, funcion de activacion ...)
                     activation='relu',
                     input_shape=(12,16,1)),
        keras.layers.Flatten(),
        keras.layers.Dense(random.randint(20,200),activation=tf.nn.relu),  #capas de la red
        keras.layers.Dense(random.randint(20,200),activation=tf.nn.relu),  #capas de la red
        keras.layers.Dense(random.randint(20,200),activation=tf.nn.relu),  #capas de la red
        keras.layers.Dense(random.randint(20,200),activation=tf.nn.relu),  #capas de la red
        keras.layers.Dense(random.randint(20,200),activation=tf.nn.relu),  #capas de la red
        keras.layers.Dense(1, activation=tf.nn.relu),
        
      ])
    
      model.compile(loss='mse',
                    optimizer='adam',
                    metrics=['mae'])
      return model

    modelo=build_model() #compila modelo
    modelo.summary()     #resumen del modelo
    
    for j in range(50): #entrene mas veces, genera una nuevos cubos cada vez que empieza
        cubos_matriz=[]
        valoracion_matriz=[]
        
        #crea n numero de cubos y hace un scramble con m movimoentos distancia 
        for i in range(n_cubos):#n cubos
            
            mov_distancia=random.randint(0,max_mov_dist)    #genera un random de movimientos distancia
            cubos_matriz.append(version1.scramble(mov_distancia))#m movimientos distancia
            valoracion_matriz.append((max_mov_dist-mov_distancia)/max_mov_dist)
            
        #convierte los cubos a matriz
        cubos_matriz=np.array(cubos_matriz)
        cubos_matriz=cubos_matriz.reshape(cubos_matriz.shape[0],12,16,1)
        
        #Entrena la red
        modelo.fit(cubos_matriz,valoracion_matriz,epochs=5, verbose=1) #(entadas, lo que yo quiero que salga, iteraciones, mostrar en pantalla)
    
    
    #solucionador del cubo (el que hace los movimientos)
    scramble=[]
    for i in range(20):#genera 20 cubos y los guarda en scramble como lista
            scramble.append(version1.scramble(max_mov_dist))#cada cubo se agrega a la lista scramble
            
    #Intenta armar los 20 cubos y muestra el porcetaje de aciertos
    cubos_armados=0        
    for n,cubo in enumerate(scramble):
        cont=0
        print("Solucionando cubo #"+str(n))
        while (cont<max_mov_dist*3):    #numero maximo de movimientos para armarlo
            if not((cubo==version1.x).all()):   #si el cubo no esta armado
                puntuacion=[]
                for i in range (0,54): #recorrido de la lista de movimientos 
                    a,b=version1.n_to_mov(i)  #movimiento y numero de veces
                    b_value=version1.mov(cubo,a,b)  #before value
                    puntuacion.append(modelo.predict(b_value.reshape(1,12,16,1)))
                a,b = version1.n_to_mov(puntuacion.index(max(puntuacion))) # se descifra el movimiento
                cubo= version1.mov(cubo,a,b)
                #print(str(a)+" , "+str(b))
            else: #si entra aqui, significa que armo el cubo
                print("cubo armado")
                cubos_armados+=1
                break
            cont+=1
    
    print("Porcentaje de cubos armados: "+str(cubos_armados*5)+"%")
    log.append(cubos_armados)
    #guarda el modelo en un archivo con la fecha de nombre si el porcentaje es mayor al 80%
    if cubos_armados>=16:
        modelo.save('modelo'+str(datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S'))+'.h5') 



