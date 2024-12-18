from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from src.collision import Collision
from src.cube import Cube
from src.input import Input
from src.movement import Movement
from src.texture import Texture
import sys
import time  # Import time for the 3-second delay

window = 0
cube_size = 2
collision_padding = 0.5
camera_pos = [-2.0, 0.0, -2.0]  # Starting position inside the maze
camera_rot = 140.0
rotate_angle = 1

collision = Collision()
input = Input()
movement = Movement()

map = []  # Replace with your full map data

wall_textures = []
# Flag to check if the maze is completed
isMazeCompleted = False

def initGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def drawScene():
    global camera_pos, isMazeCompleted
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    cube = Cube()

    # Set up the current maze view.
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(camera_rot, 0.0, 1.0, 0.0)
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])
    # Build the maze: back to front, left to right.
    row_count = 0
    column_count = 0

    for i in map:
        for j in i:
            # Draw walls only (1 - 9).
            if 0 < j < 10:
                cube.drawcube(wall_textures[int(j) - 1], 1.0)

            # Move left to right one cube size.
            glTranslatef(cube_size, 0.0, 0.0)
            column_count += 1

        # Reset position for the next row.
        glTranslatef(((cube_size * column_count) * -1), 0.0, cube_size)
        row_count += 1
        column_count = 0

    glutSwapBuffers()

    # Stop handling input if maze is completed
    if not isMazeCompleted:
        handleInput()
    else:
        showMazeCompletedMessage()

def handleInput():
    global input, camera_pos, camera_rot, isMazeCompleted

    if input.isKeyDown(Input.KEY_STATE_ESCAPE):
        sys.exit()

    if input.isKeyDown(Input.KEY_STATE_LEFT):
        camera_rot -= rotate_angle

    if input.isKeyDown(Input.KEY_STATE_RIGHT):
        camera_rot += rotate_angle

    if isMazeCompleted:
        return  # Stop accepting input after maze completion

    intended_pos = [camera_pos[0], 0, camera_pos[2]]

    if input.isKeyDown(Input.KEY_STATE_FORWARD) or input.isKeyDown(Input.KEY_STATE_BACK):
        modifier = 1 if input.isKeyDown(Input.KEY_STATE_FORWARD) else -1
        intended_pos = movement.getIntendedPosition(camera_rot, camera_pos[0], camera_pos[2], 90, modifier)

    if input.isKeyDown(Input.KEY_STATE_LEFT_STRAFE) or input.isKeyDown(Input.KEY_STATE_RIGHT_STRAFE):
        modifier = 1 if input.isKeyDown(Input.KEY_STATE_LEFT_STRAFE) else -1
        intended_pos = movement.getIntendedPosition(camera_rot, camera_pos[0], camera_pos[2], 0, modifier)

    intended_x = intended_pos[0]
    intended_z = intended_pos[2]

    # Detect collision with walls.
    if collision.testCollision(cube_size, map, intended_x, intended_z, collision_padding):
        slide_time = False
        if not collision.testCollision(cube_size, map, intended_x, camera_pos[2], collision_padding):
            intended_z = camera_pos[2]
            slide_time = True
        elif not collision.testCollision(cube_size, map, camera_pos[0], intended_z, collision_padding):
            intended_x = camera_pos[0]
            slide_time = True

        if slide_time:
            camera_pos[0] = intended_x
            camera_pos[2] = intended_z
    else:
        camera_pos[0] = intended_x
        camera_pos[2] = intended_z

    # Check for maze completion
    checkMazeCompletion()

def checkMazeCompletion():
    global isMazeCompleted
    exit_x = -56.0
    exit_z = -58.0

    # Check if player is near the exit position
    if abs(camera_pos[0] - exit_x) < collision_padding and abs(camera_pos[2] - exit_z) < collision_padding:
        isMazeCompleted = True
        print("Maze Completed!")  # Log message for console

def showMazeCompletedMessage():
    print("Congratulations! Maze Completed!")  # Display message in console
    time.sleep(3)  # Wait 3 seconds before closing
    sys.exit("Exiting...")  # Gracefully exit the program

def main():
    global window, wall_textures, map
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutInitWindowPosition(200, 200)
    window = glutCreateWindow('Welcome to Maze')
    map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1],
    [1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1],
    [1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,1,1,0,1,0,1,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1],
    [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1],
    [1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,1,1,0,1,0,1,1,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]
]
    # Load textures
    texture = Texture()
    wall_textures.append(texture.loadImage('texture/marble.jpg'))
    glutIgnoreKeyRepeat(1)
    glutKeyboardFunc(input.registerKeyDown)
    glutKeyboardUpFunc(input.registerKeyUp)
    glutDisplayFunc(drawScene)
    glutIdleFunc(drawScene)
    initGL(1024, 768)
    glutMainLoop()

if __name__ == "__main__":
    main()