import cv2
import numpy as np
from hardware import *
import copy as cp


def find_ball(image):
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0,125,100])
    upper = np.array([10,255,255])
    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(result, result, mask=mask)
    
    return mask, result

def read_board(maze):
    lower_white = np.array([0, 0, 175])
    upper_white = np.array([255, 80, 255])
    maze = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)

    wall_mask = cv2.inRange(maze, lower_white, upper_white)
    wall = cv2.bitwise_and(maze, maze, mask=wall_mask)
    wall_gray = cv2.cvtColor(wall, cv2.COLOR_BGR2GRAY)

    _, wall_bin = cv2.threshold(wall_gray, 0, 190, cv2.THRESH_BINARY)
    
    kernel_d = np.ones((13, 13), np.uint8)
    kernel_e = np.ones((10, 10), np.uint8)
    
    walls = cv2.dilate(wall_bin, kernel_d, iterations=1) # erode a parets
    walls = cv2.erode(walls, kernel_e, iterations=3) # dilate a parets
    
    return walls, wall_bin

def detector(image, walls, ball):
    ## DETECT BALL
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(cv2.bitwise_not(ball))
        
    img=cv2.drawKeypoints(image,keypoints,np.array([]),(0,255,0),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    ## DETECT WALLS
    contours, hierarchy = cv2.findContours(walls, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (0,0,255), 1)
    
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def process_frame(name):
    frame = cv2.imread(name)
    frame = cv2.resize(frame, (540, 540))
    #Quitar puntos aislados
    kernel = np.ones((3,3),np.uint8)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    
    ball_mask, ball = find_ball(frame)
    
    maze = cv2.subtract(frame, ball)
    maze[np.where(ball_mask==255)] = 255
    
    walls, wall_bin = read_board(maze)
    
    #Eliminamos fondos
    frame = delete_background(wall_bin, frame)
    ball_mask = delete_background(wall_bin, ball_mask)
    walls = delete_background(wall_bin, walls)
    ball = delete_background(wall_bin, ball)
    
    calculate_boxes(frame, ball_mask)
    
    detector(frame, walls, ball_mask)
    
def delete_background(wall_bin, img):
    ''' ES NECESARIA LA BINARIZACION DE LAS PAREDES PARA BORRAR EL FONDO'''
    indices = np.argwhere(wall_bin)
    size_board = np.max(indices, axis=0) - np.min(indices, axis=0) #podria ser util
    img = img[np.min(indices, axis=0)[0]:np.max(indices, axis=0)[1],np.min(indices, axis=0)[1]:np.max(indices, axis=0)[1]]
    return img
    

def calculate_boxes(image, ball_mask):
    copy_image = cp.deepcopy(image)
    #Quitar puntos aislados
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.morphologyEx(ball_mask, cv2.MORPH_OPEN, kernel)
    
    #Conocer pixeles que corresponden a la bola
    indices = np.argwhere(mask == 255)
    
    #Calcular tamaño en pixeles de la bola, aprox
    size = np.max(indices, axis=0) - np.min(indices, axis=0)
    
    '''Dibujo los cuadrados. En (i,j) tenemos el punto de comienzo de cada cuadrado (esquina superior izquierda),y 
       (i+size[0],j+size[1]) es el punto final de cada cuadrado (esquina inferior derecha)'''
    # Blue color in BGR
    color = (255, 0, 0)
  
    # Line thickness of 2 px
    thickness = 2
    for i in range(0, copy_image.shape[0], size[0]):
        for j in range(0, copy_image.shape[1], size[1]):
            if i + size[0] > copy_image.shape[0]:
                copy_image = cv2.rectangle(copy_image, (i,j), (copy_image.shape[0],j+size[1]), color, thickness)
                continue
            else:
                copy_image = cv2.rectangle(copy_image, (i,j), (i+size[0],j+size[1]), color, thickness)
                continue
            
            if j + size[1] > copy_image.shape[1]:
                copy_image = cv2.rectangle(copy_image, (i,j), (i+size[0],copy_image.shape[1]), color, thickness)
                continue
            else:
                copy_image = cv2.rectangle(copy_image, (i,j), (i+size[0],j+size[1]), color, thickness)
                continue
    #Muestro imagen
    cv2.imshow("Cuadricula", copy_image) 


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

if __name__ == '__main__':    
    process_frame('bdd/prova1.jpeg')
    



