import numpy as np
import cv2
import copy as cp
import math

class Node:
    def __init__(self, pos, wall):
        ############################
        # Actual list of attributes:
        #   -Pos_ini
        #   -Pos_fin
        #   -Size of box
        #   -Is wall or not
        #   -Edges
        #   -Neighbors
        ############################
        
        self.pos = pos
        self.is_wall = wall # true/false
        self.egdes = [] #list of egdes 
        self.neighbours = [] #list of neighbours 
    
    def set_neighbour(self, node):
        self.neighbours.append(node)

        
class Board:
    def __init__(self, frame):
        ############################
        # Actual list of attributes:
        #   -List of boxes
        #   -Ball, and its mask
        #   -Walls and its mask
        #   -Initial frame
        #   -Size of the board
        #   -Ball position
        ############################
        
        self.list_boxes = []
        self.ball_position = (0,0)
        self.ball_mask, self.ball = self.binarize_ball(frame)
    

        maze=cv2.subtract(frame, self.ball)
        maze[np.where(self.ball_mask==255)] = 255
        self.walls, self.wall_bin = self.read_board(maze)

        #Eliminado el borde de madera (el fondo que estorba, vamos)
        self.initial_frame = self.delete_background(self.wall_bin, frame)
        self.ball_mask = self.delete_background(self.wall_bin, self.ball_mask)
        self.ball = self.delete_background(self.wall_bin, self.ball)
        self.walls = self.delete_background(self.wall_bin, self.walls)
        self.wall_bin = self.delete_background(self.wall_bin, self.wall_bin)
        
        self.calculate_boxes()
        self.calculate_ballPosition()
        #self.detector()
        self.calculate_neighbors()
        
        
    def delete_background(self, wall_bin, img):
        ''' ES NECESARIA LA BINARIZACION DE LAS PAREDES PARA BORRAR EL FONDO'''
        indices = np.argwhere(wall_bin)
        img = img[np.min(indices, axis=0)[0]:np.max(indices, axis=0)[1],np.min(indices, axis=0)[1]:np.max(indices, axis=0)[1]]
        #Quitar puntos aislados
        kernel = np.ones((3,3),np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return cv2.resize(img, (20,20))


    def solve_maze(self):
        #############################################
        # Aquesta funció servirà per a calcular el
        # camí que la pilota ha de recorrer fins
        # arribar al final.
        # Retorna la direcció cap on ha d'anar la
        # pilota respecte on es troba
        #############################################
        pass

    def read_board(self,maze):
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
    
    def calculate_boxes(self):
        ###########################################
        # Calcular información sobre cada pixel
        ###########################################
        for i in range(0,20):
            for j in range(0,20):
                self.list_boxes.append(Node((i,j),self.wall_bin[i,j] == 0))
    
    def binarize_ball(self,image):
        #############################################
        # Aquesta funció servirà per a determinar
        # la posició de la pilota en el frame actual
        # Retorna la posició de la pilota
        #############################################
        result = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([0,125,100])
        upper = np.array([10,255,255])
        mask = cv2.inRange(image, lower, upper)
        result = cv2.bitwise_and(result, result, mask=mask)
        
        return mask, result

    def detector(self):
        #############################################
        # Aquesta funció servirà per a detectar
        # els diferents elements del laberint
        #############################################
   
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(cv2.bitwise_not(self.ball))
            
        img=cv2.drawKeypoints(self.initial_frame,keypoints,np.array([]),(0,255,0),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)    
        
        ## DETECT WALLS
        contours, hierarchy = cv2.findContours(self.walls, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img, contours, -1, (0,0,255), 1)
        
        cv2.imshow('Image con contornos', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculate_neighbors(self):
         #############################################
        # Aquesta funció servirà per a calcular
        # els veins possibles de cada node
        #############################################
        tots = self.list_boxes.copy()
        for node1 in tots:
            for node2 in tots:
                if node1 != node2 and node2.is_wall == False:
                    if (node2.pos[1] == node1.pos[1]):
                        if (node2.pos[0] == node1.pos[0]+1) or (node2.pos[0] == node1.pos[0]-1):
                            node1.set_neighbour(node2)
                    if (node2.pos[0] == node1.pos[0]):
                        if (node2.pos[1] == node1.pos[1]+1) or (node2.pos[1] == node1.pos[1]-1):
                            node1.set_neighbour(node2)
                   
    def calculate_ballPosition(self):
        ##############################################
        # Calcula la posicion del centro de la pelota
        ##############################################
        
        indices = np.where(self.ball_mask == 255)
        indices = np.sort(indices)
        indices = np.median(indices, axis=1)
        self.ball_position = (int(indices[0]), int(indices[1]))

