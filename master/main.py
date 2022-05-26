import cv2
import numpy as np
from hardware import *
from classes import *
import copy as cp
import time



def pre_process_image(path):
    #############################################
    # Aquesta funció s'encarrega de fer una
    # pre-processat de la imatge.
    #############################################
    frame = cv2.imread(path)
    frame = cv2.resize(frame, (540, 540))
    #Quitar puntos aislados
    kernel = np.ones((3,3),np.uint8)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    
    return frame


def inclination(direction):
    #############################################
    # Aquesta funció s'encarrega de calcular i
    # inclinar el taulell cap on indica la funció
    # calculate_path().
    # No retorna res.
    #############################################
    pass

def process_per_frame(frame):
    #############################################
    # Aquesta funció crida en ordre totes les
    # funcions necessaries per a resoldre el
    # laberint
    #############################################
    pass

def setup_components():
    #############################################
    # Aquesta funció comprova que tots els compo-
    # nents siguin funcionals.
    ############################################
    pass

    
#################################################
######## SPACE FOR MORE NEEDED FUNCTIONS ########
#################################################
def show_matriz(sol):
    for i in sol:
        for j in i:
            print(str(j) + " ", end ="")
        print("")


if __name__ == '__main__':
    #aqui captariamos la primera foto de la camara, que es el tablero en reposo, para asi calcular el camino
    #al principio
    #############
    
    #aqui procesamos este primer frame captado
    frame=pre_process_image('bdd/prova1.jpeg')
    
    #aqui ya creamos el objeto Board con el primer frame
    test=Board(frame)
    
    #ponemos como inicio la posicion de la bola, y como final el cuadradito que siempre será fijo (sera una constante)
    start = 1,18
    end = 20,18
    
    #calculamos el camino
    startt = time.time()
    print(list(reversed(test.get_path(start,end))))
    end = time.time()
    print(end - startt)
    
    #aqui empezaríamos un bucle donde, la condicion de seguir sería que no hemos llegado al final
    # (ball_position != final), pero tambien tenemos que parar cuando no encontremos la bola,
    # es decir, ball_position sea indefinido
    while (True): #NOTA: este bucle se hará cada vez que se capte un frame de la camara
        #captamos el frame del videostream (osea captar el frame de la camara)
        #calcular posición actual de la bola
        #si (ball_position not in camino calculado) recalculamos camino
        #si (ball_position in camino calculado) 
            #entonces miramos si de una iteración a otra
            #ha cambiado la posición de la bola, si ha cambiado entonces miramos cual es la siguiente
            #casilla del camino para determinar la dirección del camino, y mover el servo segun sea conveniente
 
    
 

    



