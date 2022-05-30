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
    
    cap = cv2.VideoCapture(0)
    leido, frame = cap.read()
    if leido == True:
        frame=pre_process_image(frame)
    else:
        cap.release()
        raise ValueError("Error de acceso a la camara")
        exit()
    
    cap.release()
    
    #aqui procesamos este primer frame captado
    #frame=pre_process_image('bdd/foto_taulell.jpg')
    
    #aqui ya creamos el objeto Board con el primer frame
    board=Board(frame)
    
    #ponemos como inicio la posicion de la bola, y como final el cuadradito que siempre será fijo (sera una constante)
    start_position_path = board.ball_position
    end_position_path = board.calculate_endPosition()
    
    #calculamos el camino
    start = time.time()
    path = list(reversed(board.get_path(start_position_path,end_position_path)))
    end = time.time()
    print("Tiempo de calculo del camino provisional: ", end - start)
    
    #aqui empezaríamos un bucle donde, la condicion de seguir sería que no hemos llegado al final
    # (ball_position != final), pero tambien tenemos que parar cuando no encontremos la bola,
    # es decir, ball_position sea indefinido
    while (board.ball_position != end_position_path and board.ball_position != None): #NOTA: este bucle se hará cada vez que se capte un frame de la camara
        last_ballPosition = board.ball_position
        #captamos el frame del videostream (osea captar el frame de la camara)
        cap = cv2.VideoCapture(0)
        leido, frame = cap.read()
        if leido == True:
            frame=pre_process_image(frame)
            #calcular posición actual de la bola
            board.process_frame(frame)
        else:
            cap.release()
            raise ValueError("Error de acceso a la camara")
            exit()
        
        #si (ball_position not in camino calculado) recalculamos camino
        if (board.ball_position not in path):
            move_board('stop')
            start_position_path = board.ball_position
            path = list(reversed(board.get_path(start_position_path,end_position_path)))
        
        #si (ball_position in camino calculado)
        else:
            #entonces miramos si de una iteración a otra ha cambiado la posición de la bola, 
            if (board.ball_position != last_ballPosition):
                #si ha cambiado entonces miramos cual es la siguiente
                #casilla del camino para determinar la dirección del camino, y mover el servo segun sea conveniente
                next_box = path[path.index(board.ball_position) + 1]
                #aqui llamariamos a la función que mira la siguiente dirección y entonces moveriamos el servo
                move_board(board.ball_position.Neighbors[next_box])
    cap.release()
    
 

    



