# 3D Rendering Engine

## 1. Introduction

This project is a simple 3D rendering engine implemented in Python. It allows for the rendering of 3D objects in a terminal window using ASCII characters. The engine supports basic 3D transformations, camera movements, and lighting effects.

Key features:
- Terminal-based 3D rendering
- Object loading from .obj files
- Camera movement and rotation
- Basic lighting including ambient, diffuse and specular shading
- Vector and matrix operations for 3D graphics

## 2. Project Structure

The project consists of the following main components:

- `lib_math.py`: Contains mathematical classes and functions for 3D graphics operations.
- `moteur_graphique.py`: Implements the core rendering engine and graphics primitives.
- `main.py`: The main entry point of the application, handling user input and scene setup.
- `cube.obj`: A sample 3D object file representing a cube.
- `venv/`: A Python virtual environment directory (not included in the repository).

## 3. Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/3d-rendering-engine.git
   cd 3d-rendering-engine
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install keyboard
   ```

## 4. Usage

To run the 3D rendering engine:

1. Ensure your terminal window is maximized for the best viewing experience.
2. Run the main script:
   ```
   python main.py
   ```

3. Use the following controls to navigate the 3D scene:
   - Arrow keys: Rotate the camera
   - W/A/S/D: Move the camera forward/left/backward/right
   - Space: Move the camera up
   - Shift: Move the camera down
   - Q: Quit the application

## 5. Core Components

### 5.1 lib_math.py

This module provides essential mathematical classes and functions for 3D graphics operations.

Key components:
- `vec2`: 2D vector class
- `vec3`: 3D vector class
- `Triangle2D`: 2D triangle class
- `Triangle3D`: 3D triangle class

Important functions:
- `LinePlaneCollision`: Calculates the intersection point between a line and a plane
- `dot`: Calculates the dot product of two vectors
- `crossProd`: Calculates the cross product of two vectors

These classes and functions form the backbone of the 3D math operations used throughout the project.

### 5.2 moteur_graphique.py

This module implements the core rendering engine and graphics primitives.

Key components:
- `Camera`: Represents the viewpoint in the 3D scene
- `LightSource`: Represents a light source in the 3D scene
- Drawing functions: `draw()`, `clear()`, `putPixel()`, `putTriangle()`
- `clip()`: Implements the clipping algorithm for triangles outside the view frustum
- `loadObj()`: Loads 3D models from .obj files
- `diffuseLight()`: Calculates ambient, diffuse and specular lighting for shading
- `putMesh()`: Renders a 3D mesh with proper depth sorting and shading

This module handles the conversion of 3D geometry to 2D screen space and manages the ASCII-based rendering in the terminal.

### 5.3 main.py

The main entry point of the application, responsible for:
- Setting up the initial scene
- Handling user input for camera movement
- Managing the main rendering loop

This file ties together all the components and provides the interactive experience for the user.

## 6. 3D Rendering Process

The rendering process follows these main steps:

1. **Object Loading**: 3D models are loaded from .obj files using the `loadObj()` function in `moteur_graphique.py`.

2. **Camera Setup**: A `Camera` object is created with an initial position and orientation.

3. **Main Loop**:
   a. Handle user input for camera movement
   b. Clear the screen
   c. For each triangle in the 3D mesh:
      - Apply camera transformations
      - Clip triangles against the view frustum
      - Project 3D points to 2D screen space
      - Calculate lighting and shading
      - Render the triangle using ASCII characters

4. **Display**: The rendered frame is displayed in the terminal.

This process repeats continuously, creating the illusion of a 3D scene in real-time.

## 7. Camera Controls

The camera can be controlled using the following keys:

- Arrow Up/Down: Adjust camera pitch (look up/down)
- Arrow Left/Right: Adjust camera yaw (look left/right)
- W: Move forward
- S: Move backward
- A: Move left
- D: Move right
- Space: Move up
- Shift: Move down

The camera movement is implemented in the `inputs()` function in `main.py`. The movement speed is adjusted based on the frame time (`dt`) to ensure consistent movement across different frame rates.

## 8. Extending the Project

To extend the project, consider the following areas:

1. **Add More 3D Models**: Create or download additional .obj files and load them into the scene.

2. **Implement Texture Mapping**: Extend the rendering system to support texture coordinates and basic texture mapping.

3. **Optimize Performance**: Implement techniques like backface culling or octree space partitioning to improve rendering speed for complex scenes.

4. **Add Color Support**: Modify the rendering system to use colored ASCII characters or switch to a graphical rendering backend like Pygame.

5. **Implement More Shading Models**: Specular lighting is now implemented; further improvements like ambient occlusion could enhance realism.

6. **Scene Graph**: Implement a scene graph to manage multiple objects and their transformations more efficiently.

7. **User Interface**: Add an on-screen UI for adjusting rendering options or scene parameters.

## 9. Troubleshooting

Common issues and their solutions:

1. **Screen Flickering**: If you experience excessive screen flickering, try adjusting the main loop's frame rate or implement double buffering.

2. **Distorted Rendering**: Ensure your terminal window is set to a monospace font and is properly sized. The rendering assumes a specific aspect ratio.

3. **Missing Dependencies**: If you encounter `ModuleNotFoundError`, make sure you've activated the virtual environment and installed all required packages.

4. **Performance Issues**: On slower systems, you may need to reduce the complexity of the 3D models or optimize the rendering loops.

## 10. Contributing

Contributions to this project are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code adheres to the existing style and includes appropriate comments and documentation.

---

This README provides a comprehensive overview of the 3D rendering engine project. For further details on specific implementations, refer to the comments within each source file.
