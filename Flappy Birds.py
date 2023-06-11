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

# # Constructor method for creating a new Bird object
    def __init__(self, x, y):
        self.x = x  # X-coordinate of the bird's position
        self.y = y  # Y-coordinate of the bird's position
        self.tilt = 0  # Current tilt angle of the bird
        self.tick_count = 0  # Number of game ticks since the bird's last jump
        self.velocity = 0  # Current vertical velocity of the bird
        self.height = self.y  # The height of the bird's position at the start
        self.img_count = 0  # Counter for animating the bird's images
        self.img = self.IMGS[0]  # Current image of the bird

    
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
    
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VALOCITY

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
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

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
    
    pygame.quit()
    quit()

main()
