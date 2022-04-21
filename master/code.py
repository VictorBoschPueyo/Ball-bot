import cv2
import numpy as np


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
    
    
    ball_mask, ball = find_ball(frame)
    
    maze = cv2.subtract(frame, ball)
    maze[np.where(ball_mask==255)] = 255
    
    walls, wall_bin = read_board(maze)
    
    
    detector(frame, walls, ball_mask)
    
def calculate_path(frame):
    #############################################
    # Aquesta funció servirà per a calcular el
    # camí que la pilota ha de recorrer fins
    # arribar al final.
    # Retorna la direcció cap on ha d'anar la
    # pilota respecte on es troba
    #############################################
    pass

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
    



