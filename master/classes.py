import numpy as np
import cv2
from PIL import Image, ImageDraw
import time 
import multiprocessing


class Node:
    def __init__(self, pos, wall):
        ############################
        # Actual list of attributes:
        #   -Pos
        #   -Is wall or not
        #   -Visited
        #   -Neighbors
        ############################
        
        self.pos = pos
        self.is_wall = wall # true/false
        self.visited = False  
        self.Neighbors= {}


   

        
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
        self.N=20
        self.images = []
        

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
        self.get_neigbors()
        
        self.a=np.pad(1-self.get_simple_matrix(), 1, 'constant', constant_values=1)
        self.images=[]
        
    def delete_background(self, wall_bin, img):
        ''' ES NECESARIA LA BINARIZACION DE LAS PAREDES PARA BORRAR EL FONDO'''
        indices = np.argwhere(wall_bin)
        img = img[np.min(indices, axis=0)[0]:np.max(indices, axis=0)[1],np.min(indices, axis=0)[1]:np.max(indices, axis=0)[1]]
        #Quitar puntos aislados
        kernel = np.ones((3,3),np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return cv2.resize(img, (20,20))

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

    
                   
    def calculate_ballPosition(self):
        ##############################################
        # Calcula la posicion del centro de la pelota
        ##############################################
        
        indices = np.where(self.ball_mask == 255)
        indices = np.sort(indices)
        indices = np.median(indices, axis=1)
        self.ball_position = (int(indices[0]), int(indices[1]))

    def calcule_index_from_ball_position(self,cordinates):
        ##############################################
        # Calcula el index del node a partir de les cordenades
        ##############################################
        for node in self.list_boxes:
            if node.pos == cordinates:
                return self.list_boxes.index(node)
        return -1


    def get_simple_matrix(self):
        ##############################################
        # Calcula la matriu de veins simple
        ##############################################
        nodes=np.zeros((20,20))
        matriz_nodes = np.array(self.list_boxes)
        matriz_nodes=matriz_nodes.reshape(20,20)
        #if node is not wall put 1 in nodes
        for i in range(0,20):
            for j in range(0,20):
                if matriz_nodes[i,j].is_wall==False:
                    nodes[i,j]=1
        return nodes


    def make_step(self,k,m):
        ##############################################
        # Realiza un pas de la busqueda
        ##############################################
            for i in range(len(m)):
                for j in range(len(m[i])):
                    if m[i][j] == k:
                         if i>0 and m[i-1][j] == 0 and self.a[i-1][j] == 0:
                            m[i-1][j] = k + 1
                         if j>0 and m[i][j-1] == 0 and self.a[i][j-1] == 0:
                            m[i][j-1] = k + 1
                         if i<len(m)-1 and m[i+1][j] == 0 and self.a[i+1][j] == 0:
                            m[i+1][j] = k + 1
                         if j<len(m[i])-1 and m[i][j+1] == 0 and self.a[i][j+1] == 0:
                            m[i][j+1] = k + 1


    def draw_matrix(self,a,m,start,end, the_path = []):
        ##############################################
        # Dibuja la matriu de veins
        ##############################################
        zoom = 20
        borders = 6

        im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (255, 255, 255))
        draw = ImageDraw.Draw(im)


        for i in range(len(a)):
            for j in range(len(a[i])):
                color = (255, 255, 255)
                r = 0
                if a[i][j] == 1:
                    color = (0, 0, 0)
                if i == start[0] and j == start[1]:
                    color = (0, 0, 255)
                    r = borders
                if i == end[0] and j == end[1]:
                    color = (0, 255, 0)
                    
                    r = borders
                draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
                if m[i][j] > 0:
                    r = borders
                    draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                                        fill=(255,0,0))

        
        for u in range(len(the_path)-1):
            draw.line((the_path[u][1]*zoom+zoom/2, the_path[u][0]*zoom+zoom/2, the_path[u+1][1]*zoom+zoom/2, the_path[u+1][0]*zoom+zoom/2), fill=(0,255,0),width=3)
        
        self.images.append(im)
        

    def save_img(self):
        ##############################################
        # Guarda la imatge
        ##############################################
        self.images[0].save('recreation.gif',save_all=True, append_images= self.images[1:],optimize=False, duration=1, loop=0)



    def get_neigbors(self):
        ##############################################
        # Calcula els veins de cada node
        # hem de guardar els veins en un diccionari 
        # si el vei esta a la dreta pusem la posicio del vei : d
        # si el vei esta a la esquerra pusem la posicio del vei : e
        # si el vei esta a l'adalt pusem la posicio del vei : a
        # si el vei esta a l'abaix pusem la posicio del vei : b
        ##############################################
        for node in self.list_boxes:
            if node.is_wall == False:
                for node2 in self.list_boxes:
                    if node2.is_wall == False:
                        if node2.pos[1] == node.pos[1]:
                            if node2.pos[0] == node.pos[0]+1:
                                node.Neighbors[node2.pos] = 'down'
                                continue
                            if node2.pos[0] == node.pos[0]-1:
                                node.Neighbors[node2.pos] = 'up'
                                continue
                        if node2.pos[0] == node.pos[0]:
                            if node2.pos[1] == node.pos[1]+1:
                                node.Neighbors[node2.pos] = 'right'
                                continue
                            if node2.pos[1] == node.pos[1]-1:
                                node.Neighbors[node2.pos] = 'left'
                                continue
        

  

    
    def get_path(self,start,end):
        ##############################################
        # Calcula el cammin de la busqueda
        ##############################################
            
            m = []
            for i in range(len(self.a)):
                m.append([])
                for j in range(len(self.a[i])):
                    m[-1].append(0)

            i,j = start
            m[i][j] = 1
            k = 0

            while m[end[0]][end[1]] == 0:
                k += 1
                self.make_step(k,m)
                self.draw_matrix(self.a, m,start,end)

            i, j = end
            k = m[i][j]
            the_path = [(i,j)]

            
            while k > 1:
                if i > 0 and m[i - 1][j] == k-1:
                    i, j = i-1, j
                    the_path.append((i, j))
                    k-=1
                elif j > 0 and m[i][j - 1] == k-1:
                    i, j = i, j-1
                    the_path.append((i, j))
                    k-=1
                elif i < len(m) - 1 and m[i + 1][j] == k-1:
                    i, j = i+1, j
                    the_path.append((i, j))
                    k-=1
                elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
                    i, j = i, j+1
                    the_path.append((i, j))
                    k -= 1
                self.draw_matrix(self.a, m,start,end, the_path)

            for i in range(10):
                if i % 2 == 0:
                    self.draw_matrix(self.a, m,start,end, the_path)
                else:
                    self.draw_matrix(self.a, m,start,end)

            self.save_img()
            # if there are not solutions break the loop
            return the_path


    

    