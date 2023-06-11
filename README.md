# Flappy Bird Game using AI

Flappy Bird is an endless game that involves a bird that the player can control. The player has to save the bird from colliding with the hurdles like pipes. Each time the bird passes through the pipes, the score gets incremented by one. The game ends when the bird collides with the pipes or falls down due to gravity.

I have planned to use AI on this game using neural networks. This is a incomplete project. I would be updating it as soon as possible when I study it more and more. For now I have just done the following study and implement a small part of the program.

## Installation

I have used [Python 3.8.0](https://www.python.org/downloads/release/python-380/).

After installing Python and setting the environment variables (for Windows), you can follow the next few steps:-

1. Open Command Prompt(CMD) to install following Libraries:

a. Pygame--
  ```
  pip install pygame
  ```
b. Neat--
  ```
  pip install neat-python
  ```

## Usage

The code is a simple implementation of the Flappy Bird game using the Pygame library in Python.It defines a Bird class that represents the bird character in the game.
The bird can jump, move, and be drawn on the game window.

Here's a brief explanation of the code:

- The constants `WIN_WIDTH` and `WIN_HEIGHT` represent the dimensions of the game window.
- The variables `BIRD_IMGS`, `PIPE_IMG`, `BASE_IMG`, and `BG_IMG` store the images used for the bird, pipes, base, and background, respectively.
- The Bird class represents the bird character in the game. It has attributes such as position, tilt, velocity, and images for animation.
- The `jump()` method is called when the bird needs to jump. It changes the bird's velocity and updates other necessary attributes.
- The `move()` method is responsible for updating the bird's position based on its velocity and gravity. It also handles the rotation of the bird.
- The `draw()` method is used to draw the bird on the game window. It selects the appropriate image based on the animation frame and rotation.
- The `get_mask()` method returns the pixel mask of the bird's current image for collision detection.
- The `draw_window()` function is responsible for drawing the game window. It clears the window, draws the background and bird, and updates the display.
- The `main()` function initializes the game window, creates a Bird object, and runs the game loop. The loop handles events, updates the bird's position, and calls the `draw_window()` function.

To run the code, make sure you have the Pygame library installed. You can then execute the code, and a game window will open displaying the Flappy Bird game.

Please note that this code snippet only includes the basic functionality of the game and does not include other game elements such as pipes, scoring, or collision detection. It can serve as a starting point for further development of the game.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).
