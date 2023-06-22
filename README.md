# Flappy Bird Game using AI

Flappy Bird is an endless game that involves a bird that the player can control. The player has to save the bird from colliding with the hurdles like pipes. Each time the bird passes through the pipes, the score gets incremented by one. The game ends when the bird collides with the pipes or falls down due to gravity.

I have planned to use AI on this game using neural networks. This is a incomplete project. I would be updating it as soon as possible when I study it more and more. For now I have just done the following study and implement a small part of the program.

[Note: I will be updating the code in phases.]

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

- The code begins by importing the necessary modules and initializing the Pygame font and window dimensions.
- The code defines constants for the bird images, pipe image, base image, and background image.
- The Bird class is defined, which represents the player-controlled bird in the game. It has attributes such as position, tilt, velocity, and image count.
- It also has methods for jumping, moving, and drawing the bird.
- The Pipe class is defined, representing the pipes that the bird needs to navigate through.
- It has attributes for position, height, and images for the top and bottom pipes.
- It also has methods for moving, drawing, and collision detection with the bird.
- The Base class represents the moving ground/base of the game.
- It has attributes for position and scrolling speed.
- It also has methods for moving and drawing the base.
- The draw_window function is defined, which is responsible for drawing the game window.
- It takes the bird, pipes, base, and score as arguments and uses the Pygame functions to draw them on the screen.
- The main function is defined, which serves as the entry point for the game.
- It initializes the bird, base, pipes, and window.
- Inside the main game loop, it handles events, moves the game objects, updates the score, and checks for collisions.
- It also calls the draw_window function to update the screen.
- Finally, the main function is called to start the game.

To run this code, you need to have Pygame installed. Make sure you have the necessary images (bird, pipe, base, and background) in the correct directory structure as specified in the code.
Then, execute the code, and the game window should open, allowing you to play Flappy Bird.

[Note: The code is missing the implementation for collision handling and when the bird touches the ground. You can complete these parts to make the game fully functional.]

## Output
### Phase 1
[Note: The output you are seeing is a .gif image. This is not the actual output, the bird will continue of fly untill the user quits the pygame window]

![Flappy Bird Phase 1](https://github.com/Shubham-Diwadkar/Flappy-Birds-Game-AI/assets/125255910/daf0f2be-f55c-48fc-ba55-df06e8a0f35a)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).
