# Importing required modules
import pygame  # Import the pygame library for game development
import neat  # Import the neat library for neuroevolution of augmenting topologies
import time  # Import the time module for time-related functions
import os  # Import the os module for operating system-related functions
import random  # Import the random module for generating random numbers

# Defining constants for the game window
WIN_WIDTH = 600  # Width of the game window in pixels
WIN_HEIGHT = 700  # Height of the game window in pixels

# Defining constants for loading bird images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

# Defining constants for loading pipe, base, and background images
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Defining a class "Bird"
class Bird:
    IMGS = BIRD_IMGS  # Assigns the list of bird images to the IMGS variable
    MAX_ROTATION = 25  # Maximum rotation angle for the bird image
    ROTATION_VELOCITY = 20  # Velocity at which the bird image rotates
    ANIMATION_TIME = 5  # Time duration for each frame of bird animation

    # Constructor method for creating a new Bird object
    def __init__(self, x, y):
        self.x = x  # X-coordinate of the bird's position
        self.y = y  # Y-coordinate of the bird's position
        self.tilt = 0  # Current tilt angle of the bird
        self.tick_count = 0  # Number of game ticks since the bird's last jump
        self.velocity = 0  # Current vertical velocity of the bird
        self.height = self.y  # The height of the bird's position at the start
        self.img_count = 0  # Counter for animating the bird's images
        self.img = self.IMGS[0]  # Current image of the bird

    # Method to make the bird jump
    def jump(self):
        self.velocity = -10.5  # Set the velocity of the bird to make it move upwards
        self.tick_count = 0  # Reset the tick count to start tracking the time since the last jump
        self.height = self.y  # Store the current height of the bird for reference

    # Method to make the bird move
    def move(self):
        self.tick_count += 1  # Increment the tick count to track the time
    
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2  # Calculate the displacement based on velocity and time
    
        if displacement >= 16:  # Limit the maximum displacement
            displacement = 16

        if displacement < 0:  # Add additional displacement adjustment for upward movement
            displacement -= 2

        self.y = self.y + displacement  # Update the vertical position of the bird

        if displacement < 0 or self.y < self.height + 50:  # Check if bird is moving upward or near its highest point
            if self.tilt < self.MAX_ROTATION:  # Adjust the tilt angle of the bird for upward movement
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:  # Adjust the tilt angle of the bird for downward movement
                self.tilt -= self.ROTATION_VALOCITY

    # Method to draw the bird on the game window
    def draw(self, win):
        self.img_count += 1  # Increment the image count for animation

        if self.img_count < self.ANIMATION_TIME:  # Determine the current bird image based on the image count
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:  # Adjust the bird image and count for extreme upward tilt
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)  # Rotate the bird image based on tilt angle
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)  # Create a new rectangle for rotated image positioning
        win.blit(rotated_image, new_rectangle.topleft)  # Draw the rotated bird image on the window


    # Method to retrieve the mask for the bird's image
    def get_mask(self):
        return pygame.mask.from_surface(self.img)   # The mask is created and returned

# Method to draw the game window
def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))    # Blit the background image onto the window at position (0, 0)
    bird.draw(win)  # Draw the bird onto the window
    pygame.display.update() # Update the display to show the changes

# Main game loop that handles events, updates the bird's position, and redraws the game window
def main():
    bird = Bird(200, 200)  # Create a bird object with initial position (200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # Set up the game window with the specified width and height
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate

    run = True
    while run:
        clock.tick(30)  # Limit the frame rate to 30 frames per second
        for event in pygame.event.get():  # Check for events (e.g., user input)
            if event.type == pygame.QUIT:  # If the user clicks the close button, stop the game loop
                run = False
        bird.move()  # Move the bird based on its current velocity and position
        draw_window(win, bird)  # Draw the game window with the bird's current state
    
    pygame.quit()  # Quit Pygame
    quit()  # Quit the Python program

main()  # Main Entry point of the program
