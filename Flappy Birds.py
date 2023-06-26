# Import the Pygame library
import pygame

# Import the NEAT library for neuroevolution
import neat

# Import the time module
import time

# Import the os module for file path operations
import os

# Import the random module for randomization
import random

# Initialize the Pygame font module
pygame.font.init()

# Set the width of the game window
WIN_WIDTH = 500

# Set the height of the game window
WIN_HEIGHT = 800

# Load and scale the bird images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

# Load and scale the pipe image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

# Load and scale the base image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

# Load and scale the background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Create a font object for displaying text
STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:

    # Assign the bird images to the class attribute IMGS
    IMGS = BIRD_IMGS

    # Maximum tilt rotation of the bird
    MAX_ROTATION = 25

    # Velocity of the rotation
    ROTATION_VALOCITY = 20

    # Animation time for the bird's wing flap
    ANIMATION_TIME = 5

    # Constructor method to initialize the bird object
    def __init__(self, x, y):

        # Current x-coordinate of the bird
        self.x = x

        # Current y-coordinate of the bird
        self.y = y

        # Current tilt angle of the bird
        self.tilt = 0

        # Counter for tracking time
        self.tick_count = 0

        # Current velocity of the bird
        self.velocity = 0

        # Initial height of the bird
        self.height = self.y

        # Counter for tracking bird image animation
        self.img_count = 0

        # Current image of the bird
        self.img = self.IMGS[0]
    
    # Method for making the bird jump
    def jump(self):

        # Set the velocity to make the bird jump
        self.velocity = -10.5

        # Reset the tick counter
        self.tick_count = 0

        # Set the initial height of the bird
        self.height = self.y

    # Method for moving the bird
    def move(self):

        # Increase the tick counter by 1
        self.tick_count += 1

        # Calculate the displacement
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        # Limit the maximum downward velocity
        if displacement >= 16:
            displacement = 16

        # Fine-tune the upward jump
        if displacement < 0:
            displacement -= 2

        # Update the y-coordinate of the bird
        self.y = self.y + displacement

        # Adjust the tilt angle based on the bird's movement
        if displacement < 0 or self.y < self.height + 50:

            # Limit the tilt angle to the maximum rotation angle
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:

            # Reduce the tilt angle by the rotation velocity
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VALOCITY
    
    # Method for drawing the bird on the game window
    def draw(self, win):

        # Increase the image counter
        self.img_count += 1

        # Animation for wing flap
        if self.img_count < self.ANIMATION_TIME:

            # Set the current image to the first image in the list
            self.img = self.IMGS[0]
        
        elif self.img_count < self.ANIMATION_TIME * 2:

            # Set the current image to the second image in the list
            self.img = self.IMGS[1]
        
        elif self.img_count < self.ANIMATION_TIME * 3:

            # Set the current image to the third image in the list
            self.img = self.IMGS[2]

        elif self.img_count < self.ANIMATION_TIME * 4:

            # Set the current image back to the second image in the list
            self.img = self.IMGS[1]

        elif self.img_count == self.ANIMATION_TIME * 4 + 1:

            # Set the current image back to the first image in the list
            self.img = self.IMGS[0]

            # Reset the image count to 0
            self.img_count = 0

        # Animation when the bird is nosediving
        if self.tilt <= -80:

            # Set the current image to the second image in the list
            self.img = self.IMGS[1]

            # Set the image count to twice the animation time
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate the bird image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)

        # Adjust the position
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        # Draw the rotated image onto the window
        win.blit(rotated_image, new_rectangle.topleft)

    # Create and return a mask for collision detection
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:

    # Gap between the top and bottom pipes
    GAP = 200

    # Velocity at which the pipes move horizontally
    VEL = 5

    # Constructor method to initialize the pipe object
    def __init__(self, x):

        # Initialize the x-coordinate of the pipe
        self.x = x

        # Initialize the height of the gap between the pipes
        self.height = 0

        # Initialize the top position of the top pipe
        self.top = 0

        # Initialize the top position of the bottom pipe
        self.bottom = 0

        # Flip the pipe image for the top pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)

        # Use the original pipe image for the bottom pipe
        self.PIPE_BOTTOM = PIPE_IMG

        # Flag to check if the bird has passed the pipe
        self.passed = False

        # Set the initial height of the gap between the pipes
        self.set_height()

    # Setting the height of pipes
    def set_height(self):

        # Set a random height for the gap between the pipes
        self.height = random.randrange(50, 450)

        # Calculate the top position of the top pipe
        self.top = self.height - self.PIPE_TOP.get_height()

        # Calculate the top position of the bottom pipe
        self.bottom = self.height + self.GAP

    # Method for moving the pipes
    def move(self):

        # Move the pipe horizontally based on the velocity
        self.x -= self.VEL

    # Method for drawing the pipes
    def draw(self, win):

        # Draw the top pipe on the window
        win.blit(self.PIPE_TOP, (self.x, self.top))

        # Draw the bottom pipe on the window
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # Method for collision of the pipes and the bird
    def collide(self, bird):

        # Get the mask of the bird
        bird_mask = bird.get_mask()

        # Get the mask of the top pipe
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)

        # Get the mask of the bottom pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Calculate the offset between bird and top pipe
        top_offset = (self.x - bird.x, self.top - round(bird.y))

        # Calculate the offset between bird and bottom pipe
        bottom_offset = (self.x - bird.x, self.bottom -round(bird.y))

        # Check for collision between bird and bottom pipe
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        # Check for collision between bird and top pipe
        t_point = bird_mask.overlap(top_mask, top_offset)

        # If collision occurs
        if t_point or b_point:
            
            # Return True (collision has occurred)
            return True
        
        # Return False (no collision)
        return False
    
class Base:

    # Velocity of the base
    VEL = 5

    # Width of the base image
    WIDTH = BASE_IMG.get_width()

    # Base image
    IMG = BASE_IMG

    # Constructor method to initialize the base object
    def __init__(self, y):

        # Vertical position of the base
        self.y = y

        # X position of the first base image
        self.x1 = 0

        # X position of the second base image
        self.x2 = self.WIDTH

    # Method for moving the base
    def move(self):

        # Move the first base image to the left
        self.x1 -= self.VEL

        # Move the second base image to the left
        self.x2 -= self.VEL

        # Reset the position of the first base image
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        # Reset the position of the second base image
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    # Method for drawing the base
    def draw(self, win):

        # Draw the first base image
        win.blit(self.IMG, (self.x1, self.y))

        # Draw the second base image
        win.blit(self.IMG, (self.x2, self.y))

# Method for drawing the window
def draw_window(win, birds, pipes, base, score):

    # Draw the background image at the top-left corner of the window
    win.blit(BG_IMG, (0, 0))

    # Draw each pipe on the window
    for pipe in pipes:
        pipe.draw(win)

    # Render the score text
    text = STAT_FONT.render("Score: "+ str(score), 1, (255, 255, 255))

    # Draw the score text at the top-right corner of the window
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Draw the base at its current position
    base.draw(win)

    # Draw each bird on the window
    for bird in birds:
        bird.draw(win)

    # Update the display to show the changes
    pygame.display.update()

# Method to start the program
def main(genomes, config):

    # List to store the neural networks for each genome
    nets = []

    # List to store the genomes
    ge = []

    # List to store the bird objects
    birds = []

    # For each genome created
    for _, g in genomes:

        # Create a neural network using the current genome and the provided configuration
        net = neat.nn.FeedForwardNetwork.create(g, config)

        # Add the neural network to the list
        nets.append(net)

        # Create a bird object and add it to the list
        birds.append(Bird(230, 350))

        # Initialize the fitness of the genome
        g.fitness = 0

        # Add the genome to the list
        ge.append(g)

    # Create a base object at the specified height (730)
    base = Base(730)

    # Create a list of pipes with an initial pipe at the specified position (600)
    pipes = [Pipe(600)]

    # Create a game window with the specified dimensions (WIN_WIDTH, WIN_HEIGHT)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Create a clock object to control the frame rate of the game
    clock = pygame.time.Clock()

    # Initialize the score to 0
    score = 0

    # Initialize the flag to control the game loop
    run = True


    while run:

        # Limit the frame rate to 30 frames per second
        clock.tick(30)

        # Check for the quit event (user closes the window)
        for event in pygame.event.get():

            # If detected, exit the game loop, close the window, and quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Initialize the pipe index to 0
        pipe_ind = 0

         # Determine the pipe index to consider for the bird's decision-making
        if len(birds) > 0:

            # If there are birds and multiple pipes, check if the first pipe has been passed
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():

                # If passed, consider the next pipe (pipe index 1)
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):

            # Move each bird
            bird.move()

            # Increase the fitness of the bird
            ge[x].fitness += 0.1

            # Activate the neural network for the bird using the input values
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            # If the output value of the network is greater than 0.5, make the bird jump
            if output[0] > 0.5:
                bird.jump()

        # Initialize variables for managing pipes
        add_pipe = False
        rem = []

        for pipe in pipes:
            for x, bird in enumerate(birds):

                # Check if any bird collides with the pipe
                if pipe.collide(bird):

                    # If collided, decrease the fitness of the bird, remove it from lists
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # Check if the bird has passed through the pipe
                if not pipe.passed and pipe.x <bird.x:

                    # If passed, mark the pipe as passed and set the flag to add a new pipe
                    pipe.passed = True
                    add_pipe = True

            # Check if the pipe has moved off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:

                # If moved off, add it to the removal list
                rem.append(pipe)

            # Move the pipe
            pipe.move()

        # Check if add_pipe variable is true
        if add_pipe:

            # Increase the score
            score += 1

            for g in ge:

                # Increase the fitness of all birds
                g.fitness += 5

            # Add a new pipe at a specified position (600)
            pipes.append(Pipe(600))

        # Remove the pipes that have moved off the screen
        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):

            # Check if any bird hits the ground or goes above the screen
            if bird.y +bird.img.get_height() > 730 or bird.y < 0:

                # If so, remove the bird from lists
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        # Move the base
        base.move()

        # Draw the window with the updated game objects and score
        draw_window(win, birds, pipes, base, score)

# Method to run the NEAT algorithm
def run(config_path):

    # Load the NEAT configuration file to configure the NEAT algorithm
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create a NEAT population based on the loaded configuration
    population = neat.Population(config)

    # Add a reporter to print the progress of the population to the console
    population.add_reporter(neat.StdOutReporter(True))

    # Add a reporter to gather statistics about the population
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run the NEAT algorithm for a specified number of generations, using the main function as the fitness function
    winner = population.run(main, 50)

    # Return the winning genome from the NEAT algorithm
    return winner


if __name__ == "__main__":

    # Set the path to the configuration file for the NEAT algorithm
    config_path = path = os.path.join(os.environ["USERPROFILE"],"Desktop", "YOUR_FOLDER_NAME","config_feedforward.txt")
    
    # Run the `run` function with the provided configuration file path
    run(config_path)
