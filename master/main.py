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
    frame=pre_process_image('bdd/prova1.jpeg')
    test=Board(frame)
    start = 1,18
    end = 20,18

    print(list(reversed(test.get_path(start,end))))
 
    
 

    



