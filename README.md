# BALLBOT
## Project description
This project aims to recreate the maze game with a ball. This ball will move with the movement of the board, in order to reach the final destination.
To give it a different point of view, it will be the same BALLBOT who moves the board, and it will be the player who designs the circuit. Therefore, the robot must be able to adapt to the board each time the user modifies it.
In addition, there will be a screen showing the circuit that captures the camera, and the circuit that the robot has calculated to take the ball to its final destination will be drawn in real time.

# Table of Contents
   * [Electronic components](#Electronic-components)
   * [Hardware Scheme](#Hardware-Scheme)
   * [Software Architecture](#Software-Architecture)
        * [Software design](#Software-design)
        * [Flowchart](#Flowchart)
        * [Class diagram](#Class-diagram)
   * [Amazing contributions](#Amazing-contributions)
   * [Extra components and 3D pieces](#Extra-components-and-3D-pieces)
   

## Electronic components
- RASPBERRY PI 3
- CAMERA
- SD
- SERVOMOTOR (3)
- SCREEN

## Hardware Scheme
Insertar foto del esquema

The connections will go as follow:
- Both power supplies will be connected to a Power Bank
- Camera connected to Raspberry Pi camera module
- Screen connected to Raspberry Pi display module
- Raspberry Pi pin 6 (GND) to PCA9665 GND pin
- Raspberry Pi pin 2 (5V) to PCA9665 VCC pin
- Raspberry Pi pin 3 (GPIO 2) to PCA9665 SDA pin
- Raspberry Pi pin 5 (GPIO 3) to PCA9665 SCL pin
- 3 servos connected to PCA9665 0, 8 and 15

## Software Architecture
## Software design
Insertar foto del esquema de software design
- Board treatment: Identify the structure of the maze (position and orientation
of the walls, identification of start and goal points).
- Ball treatment: identifying the ball's position; necessary for calculating the
path to follow.
- Search algorithm: determine the path the ball must follow to reach the goal
point (there are different types of search algorithms, for example:
backtracking, branch&bound).
- The module indicates to the servos what type of movement they need to
perform (orientation, force, etc.)

## Flowchart
![This is the Flowchart of our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/spr3-diag-flujo.drawio.png)
## Class diagram
![This is the Class diagram of our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/spr2-diag-clases.drawio.png)


## Amazing contributions 
The following features make our project unique:
- The structure of the maze is built through user interaction.
- Mazes can be solved in an infinite number of ways.
- The robot's ability to guide the ball to the goal.
- Control of the edges, because the ball cannot go out of the board.
- Device for displaying the path to be taken, or the path that is currently being taken.

## Extra components and 3D pieces
- POREXPAN BOARD
- POREXPAN PIECES
- WOOD PLANK
- RED FOAM BALL
- CAMERA SUPPORT

Insertar foto del prototipo

Insertar fotos de las piezas 3D

## Features

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF



## Requerimientos

Is necesary to add the following libraries

## Links

| Plugin | link |
| ------ | ------ |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |

## License
Juan Carlos Martinez Moreno 1566936
Victor Bosch Pueyo                 1566583
Alvaro Caravaca Hernández   1566685
Luis Fernando Paz  Galeano   1567369
**Free Software**

   [PlGh]: <https://github.com/VictorBoschPueyo/Robotics-project.git>
   [PlGd]: <https://drive.google.com/drive/folders/1HyyOAsSVA52dkZ4_BdE1-cv34iZsNWCG>
