# BALLBOT
![This is our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/foto_robot.jpg)

# Table of Contents
   * [Project description](#Project-description)
   * [Requirements](#Requirements)
   * [How to use](#How-to-use)
   * [Electronic components](#Electronic-components)
   * [Hardware Scheme](#Hardware-Scheme)
   * [Software Architecture](#Software-Architecture)
        * [Software design](#Software-design)
        * [Flowchart](#Flowchart)
        * [Class diagram](#Class-diagram)
   * [Amazing contributions](#Amazing-contributions)
   * [Extra components and 3D pieces](#Extra-components-and-3D-pieces)
   * [Features](#Features)
   * [Links](#Links)
   * [License](#License)
   * [Authors](#Authors)
   

## Project description
This project aims to recreate the maze game with a ball. This ball will move with the movement of the board, in order to reach the final destination.
To give it a different point of view, it will be the same BALLBOT who moves the board, and it will be the player who designs the circuit. Therefore, the robot must be able to adapt to the board each time the user modifies it.
In addition, there will be a screen showing the circuit that captures the camera, and the circuit that the robot has calculated to take the ball to its final destination will be drawn in real time.

## Requirements
For running each sample code:
- [Adafruit-CircuitPython] - CircuitPython helper library for the PWM/Servo FeatherWing, Shield and Pi HAT and Bonnet kits.
- [numpy] - NumPy offers comprehensive mathematical functions, random number generators, linear algebra routines, Fourier transforms, and more.
- [opencv-python-headless] - Pre-built CPU-only OpenCV packages for Python.
- [Pillow] - The Python Imaging Library adds image processing capabilities to your Python interpreter.

## Documentation
An introduction to the project that was developed for the Robotics subject is included in this README.
Documents related to the project development can be found in the following [folder].
Whether you have recommendations about it, or if you have suggestions for improving it, let us know.
Our project can be scaled up and improved by adding new tools that provide more robustness and ease of use for the robot.

## How to use
1. Clone this repo.
```sh
git clone  https://github.com/VictorBoschPueyo/Robotics-project 
```
2. Install the required libraries.
```sh
pip install -r requirements/requirements.txt
```
3.Execute python script.

## Electronic components
- JETSON NANO
- CAMERA
- SD
- SERVOMOTOR (2)
- PCA9665

## Hardware Scheme
![This is the hardware scheme of our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/hardware_scheme.PNG)

Here we have the hardware scheme of Ball Bot.
The connections will go as follow:
- Both power supplies will be connected to a Power Bank
- Camera connected to Jetson Nano camera module
- Jetson Nano pin 6 (GND) to PCA9665 GND pin
- Jetson Nano pin 2 (5V) to PCA9665 VCC pin
- Jetson Nano pin 3 (GPIO 2) to PCA9665 SDA pin
- Jetson Nano pin 5 (GPIO 3) to PCA9665 SCL pin
- 2 servos connected to PCA9665 0, 8 and 15

## Software Architecture
Here we will describe the software architecture of our project.
## Software design
![This is the software design of our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/software_design.PNG)
- Board treatment: Identify the structure of the maze (position and orientation
of the walls, identification of start and goal points).
- Ball treatment: identifying the ball's position; necessary for calculating the
path to follow.
- Search algorithm: determine the path the ball must follow to reach the goal
point (there are different types of search algorithms, for example:
backtracking, branch&bound).

![Recreation](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/master/recreation.gif)

- The module indicates to the servos what type of movement they need to
perform (orientation, force, etc.)

## Flowchart
![This is the Flowchart of our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/spr3-diag-flujo.drawio.png)
## Class diagram
![This is the Class diagram of our robot](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/spr2-diag-clases.drawio.png)

## Example of how it works
To understand how does this project work, we will explain it with an example.
1. First of all, we place the walls in the board making a labyrinth for the robot to solve.
![This is the board](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/foto_taulell.jpg)

2. The second step is to localize the ball and the end point to erase them from the board and be able to binarize it. To locate this two points, we will do some binarization with adaptive thresholds, in order to deal with shadows.

![foto_binarizado](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/master/bdd/bin_walls_exemple.JPG)

3. The third step is calculate the path that will follow the ball. This step is being done with an algorithm that can build an incremental solution,
   by adding sub-elements to the path, since the full path is built. (gif del luis)


4. Move the board, following the steps that lead the different nodes of the path. Every node of the path follows a determinated direction, so the principal loop has to determinate the next direction to follow.


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

![3D Pieces 1](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/prototype.PNG)

![3D Pieces 1](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/3d_pieces_1.PNG)
![3D Pieces 2](https://github.com/VictorBoschPueyo/Robotics-project/blob/main/docs/diagrams/3d_pieces_2.PNG)
## Features

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF


## Links

| Plugin | link |
| ------ | ------ |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |

## License
**Free Software**

## Authors
* Juan Carlos Martinez Moreno 1566936
* Victor Bosch Pueyo                 1566583
* Alvaro Caravaca Hernández   1566685
* Luis Fernando Paz  Galeano   1567369

   [PlGh]: <https://github.com/VictorBoschPueyo/Robotics-project.git>
   [PlGd]: <https://drive.google.com/drive/folders/1HyyOAsSVA52dkZ4_BdE1-cv34iZsNWCG>
   [Adafruit-CircuitPython]:<https://docs.circuitpython.org/projects/servokit/en/latest/>
   [gpio]: <https://pypi.org/project/RPi.GPIO/>
   [numpy]:<https://numpy.org/>
   [opencv-python-headless]: <https://pypi.org/project/opencv-python-headless/>
   [Pillow]:<https://pillow.readthedocs.io/en/stable/>
   [folder]:<https://github.com/VictorBoschPueyo/Robotics-project/tree/main/docs>
   [Adafruit-servokit]:<https://docs.circuitpython.org/projects/servokit/en/latest/>
