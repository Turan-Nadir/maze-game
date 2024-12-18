
Maze Game with OpenGL and PyOpenGL
This is a simple maze game developed for a Computer Graphics class. The game uses OpenGL for rendering and Pillow for texture loading.

Features
3D Maze rendering with wall textures.
Minimalist design to enhance focus.
Handcrafted map using a custom map maker (available upon request).
Installation
Clone or fork the repository:

bash
Copy code
git clone <https://github.com/Turan-Nadir/maze-game.git>
cd maze-game
Install dependencies:

bash
Copy code
pip install PyOpenGL Pillow
Run the game:

bash
Copy code
python maze.py
# or
python3 maze.py
# or, if using conda
conda maze.py
Gameplay Description
Navigate through the maze to find the exit.
Wall textures are applied for better visualization; the ground and sky remain black for minimal distractions.
Use the following controls:
Arrow keys for movement and rotation.
Escape key to exit the game.
Map
The maze map was handcrafted using a custom map maker built with React. If you need the map maker, email me at robertbenn95@gmail.com.
In case you're stuck, here's the default map file: /map.jpeg.

Code Overview
Dependencies
OpenGL.GL, OpenGL.GLUT, OpenGL.GLU: For rendering and handling OpenGL operations.
Pillow: To load and apply textures.
Custom Modules:
collision.py: Handles collision detection.
cube.py: Defines cube rendering.
input.py: Captures user input.
movement.py: Calculates camera movement.
texture.py: Loads textures.
Key Constants
cube_size: Size of the maze cubes.
camera_pos: Starting position of the player.
isMazeCompleted: Tracks if the maze is completed.
Main Functions
drawScene: Renders the maze and handles camera updates.
handleInput: Processes player input.
checkMazeCompletion: Checks if the player has reached the maze exit.
main: Initializes the OpenGL environment and game loop.
Notes
Ensure the texture file (marble.jpg) is in the texture directory.
The game closes automatically when the maze is completed, displaying a "Maze Completed!" message.
Contribution
Feel free to fork the project, submit pull requests, or report issues. For any inquiries, email robertbenn95@gmail.com.

