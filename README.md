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
The code is a simple implementation of the Flappy Bird game using the Pygame library in Python.

Here's a brief explanation of the code:
- The code imports the necessary libraries: `pygame` for creating the game, `neat` for implementing the NEAT algorithm, `time` for time-related functions, `os` for file path operations, and `random` for generating random numbers.
- It initializes the pygame library and sets the dimensions of the game window (`WIN_WIDTH` and `WIN_HEIGHT`).
- It loads the required images for the game, including the bird images, pipe image, base image, and background image.
- The images are scaled up by a factor of 2 using `pygame.transform.scale2x()`.

1. The Bird Class:
   - The code defines the `Bird` class, which represents the player-controlled bird.
   - It has attributes such as position (`x` and `y`), tilt, velocity, and image.
   - It also has methods for jumping, moving, and drawing the bird on the game window.

2. The Pipe Class:
   - The `Pipe` class represents the pipes that the bird needs to navigate through.
   - It has attributes such as position (`x`), height, and images for the top and bottom pipes.
   - It also has methods for moving and drawing the pipes on the game window, as well as checking for collisions with the bird.

3. The Base Class:
   - The `Base` class represents the base on which the bird stands.
   - It has attributes such as position (`y`) and images.
   - It also has methods for moving and drawing the base on the game window.

- The `draw_window()` function is defined, which handles rendering the game on the window.
- It takes parameters such as the game window, bird objects, pipe objects, base object, and the current score.
- It draws the background, pipes, base, birds, and the score text on the window using the loaded images and the `blit()` function.
- The `main()` function is the main game loop.
- It takes two parameters: `genomes` (a list of genome objects) and `config` (the NEAT configuration object).
- It sets up the initial game state, creates the neural networks for each bird, and starts the game loop.
- Within the game loop, it handles user input, updates the game state (moving objects, checking collisions, etc.), and renders the game on the window.
- It also applies the NEAT algorithm to control the birds' behavior by activating the neural networks based on input and making them jump when necessary.
- The `run()` function is defined, which takes a `config_path` parameter.
- It creates a NEAT configuration object based on the provided configuration file path.
- It creates a NEAT population, adds reporters for displaying statistics, and runs the main game loop (`main()`) for a specified number of generations (in this case, 50).
- Finally, the `__name__ == "__main__"` block is used to run the game.
- It sets the configuration file path, calls the `run()` function with the configuration path, and starts the game.

Overall, the code combines the Flappy Bird game mechanics with the NEAT algorithm to create an AI agent that learns to play the game by evolving neural networks. The AI agent tries to maximize its score by avoiding collisions with pipes and navigating through the gaps.
To run this code, you need to have Pygame installed. Make sure you have the necessary images (bird, pipe, base, and background) in the correct directory structure as specified in the code.
Then, execute the code, and the game window should open, allowing you to play Flappy Bird.

[Note: The path of the file is set to default location in local directory (C:) on Desktop]

## Start the Run
[Note: I prefer you to save the file on Desktop]

1. Create a folder and give it a name of your choice.
2. Save all the folders and files (i.e., `imgs` folder, `config_feedforward.txt` file and the `Flappy Birds.py` file) in that folder.
3. Open the `Flappy Bird.py` file change the `"YOUR_FOLDER_NAME"` into your folder name you choose.
4. Save the file and run the code. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).
