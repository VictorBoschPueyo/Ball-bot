import numpy as np
import cv2
import copy as cp


class Node:
    def __init__(self, pos_ini, pos_fin, wall, size):
        ############################
        # Actual list of attributes:
        #   -Pos_ini
        #   -Pos_fin
        #   -Size of box
        #   -Is wall or not
        #   -Edges
        #   -Neighbors
        ############################
        
        self.pos_ini = pos_ini
        self.pos_fin = pos_fin
        self.size = size
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
        ############################
        
        self.list_boxes = []
        self.ball_mask, self.ball = self.ball_position(frame)
    

        maze=cv2.subtract(frame, self.ball)
        maze[np.where(self.ball_mask==255)] = 255
        self.walls, self.wall_bin = self.read_board(maze)
        
        self.size = self.calculate_sizeB(self.wall_bin)

        #Eliminado el borde
        self.initial_frame = self.delete_background(self.wall_bin, frame)
        self.ball_mask = self.delete_background(self.wall_bin, self.ball_mask)
        self.ball = self.delete_background(self.wall_bin, self.ball)
        self.walls = self.delete_background(self.wall_bin, self.walls)
        self.wall_bin = self.delete_background(self.wall_bin, self.wall_bin)
        
        self.calculate_boxes()
        self.detector()
        
    
    def calculate_sizeB(self, wall_bin):
        indices = np.argwhere(wall_bin)
        self.size = np.max(indices, axis=0) - np.min(indices, axis=0)
        
    def delete_background(self, wall_bin, img):
        ''' ES NECESARIA LA BINARIZACION DE LAS PAREDES PARA BORRAR EL FONDO'''
        indices = np.argwhere(wall_bin)
        self.size = np.max(indices, axis=0) - np.min(indices, axis=0)
        img = img[np.min(indices, axis=0)[0]:np.max(indices, axis=0)[1],np.min(indices, axis=0)[1]:np.max(indices, axis=0)[1]]
        return img


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
        #############################################
          
        copy_image = cp.deepcopy(self.initial_frame)
        #Quitar puntos aislados
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.morphologyEx(self.ball_mask, cv2.MORPH_OPEN, kernel)

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
                    self.build_box((i,j), (copy_image.shape[0],j+size[1]), self.wall_bin[i:copy_image.shape[0],j:j+size[1]])
                    copy_image = cv2.rectangle(copy_image, (i,j), (copy_image.shape[0],j+size[1]), color, thickness)
                    continue
                else:
                    self.build_box((i,j), (i+size[0],j+size[1]), self.wall_bin[i:i+size[0],j:j+size[1]])
                    copy_image = cv2.rectangle(copy_image, (i,j), (i+size[0],j+size[1]), color, thickness)
                    continue

                '''if j + size[1] > copy_image.shape[1]:
                    copy_image = cv2.rectangle(copy_image, (i,j), (i+size[0],copy_image.shape[1]), color, thickness)
                    continue
                else:
                    copy_image = cv2.rectangle(copy_image, (i,j), (i+size[0],j+size[1]), color, thickness)
                    continue'''
        
        #Mostrar imagen con cuadrados
        cv2.imshow("Cuadricula", copy_image[0:self.size[0], 0:self.size[1]])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

    def build_box(self, pos_ini, pos_fin, box_matrix):
        black_pixels = np.count_nonzero(box_matrix == 0)
        total_pixels = box_matrix.size
        #Pondremos a partir de 60% de pared se define como pared
        if black_pixels / total_pixels > 0.6:
            self.list_boxes.append(Node(pos_ini, pos_fin, True, (pos_fin[0] - pos_ini[0], pos_fin[1] - pos_ini[1])))
        else:
            self.list_boxes.append(Node(pos_ini, pos_fin, False, (pos_fin[0] - pos_ini[0], pos_fin[1] - pos_ini[1])))
    
    def ball_position(self,image):
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