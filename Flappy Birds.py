import pygame# Import the Pygame library
import neat# Import the NEAT library for neuroevolution
import time# Import the time module
import os# Import the os module for file path operations
import random# Import the random module for randomization

pygame.font.init()# Initialize the Pygame font module

WIN_WIDTH = 500# Set the width of the game window
WIN_HEIGHT = 800# Set the height of the game window

# Load and scale the bird images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))# Load and scale the pipe image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))# Load and scale the base image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))# Load and scale the background image

STAT_FONT = pygame.font.SysFont("comicsans", 50)# Create a font object for displaying text

class Bird:
    IMGS = BIRD_IMGS# Assign the bird images to the class attribute IMGS
    MAX_ROTATION = 25# Maximum tilt rotation of the bird
    ROTATION_VALOCITY = 20# Velocity of the rotation
    ANIMATION_TIME = 5# Animation time for the bird's wing flap

    # Constructor method to initialize the bird object
    def __init__(self, x, y):
        self.x = x# Current x-coordinate of the bird
        self.y = y# Current y-coordinate of the bird
        self.tilt = 0# Current tilt angle of the bird
        self.tick_count = 0# Counter for tracking time
        self.velocity = 0# Current velocity of the bird
        self.height = self.y# Initial height of the bird
        self.img_count = 0# Counter for tracking bird image animation
        self.img = self.IMGS[0]# Current image of the bird
    
    # Method for making the bird jump
    def jump(self):
        self.velocity = -10.5# Set the velocity to make the bird jump
        self.tick_count = 0# Reset the tick counter
        self.height = self.y# Set the initial height of the bird

    # Method for moving the bird
    def move(self):
        self.tick_count += 1# Increase the tick counter by 1
    
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2# Calculate the displacement

        # Limit the maximum downward velocity
        if displacement >= 16:
            displacement = 16

        # Fine-tune the upward jump
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement# Update the y-coordinate of the bird

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
        self.img_count += 1# Increase the image counter

        # Animation for wing flap
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]# Set the current image to the first image in the list
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]# Set the current image to the second image in the list
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]# Set the current image to the third image in the list
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]# Set the current image back to the second image in the list
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]# Set the current image back to the first image in the list
            self.img_count = 0# Reset the image count to 0

        # Animation when the bird is nosediving
        if self.tilt <= -80:
            self.img = self.IMGS[1]# Set the current image to the second image in the list
            self.img_count = self.ANIMATION_TIME * 2# Set the image count to twice the animation time

        rotated_image = pygame.transform.rotate(self.img, self.tilt)# Rotate the bird image
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)# Adjust the position
        win.blit(rotated_image, new_rectangle.topleft)# Draw the rotated image onto the window

    # Create and return a mask for collision detection
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200# Gap between the top and bottom pipes
    VEL = 5# Velocity at which the pipes move horizontally

    # Constructor method to initialize the pipe object
    def __init__(self, x):
        self.x = x# Initialize the x-coordinate of the pipe
        self.height = 0# Initialize the height of the gap between the pipes

        self.top = 0# Initialize the top position of the top pipe
        self.bottom = 0# Initialize the top position of the bottom pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)# Flip the pipe image for the top pipe
        self.PIPE_BOTTOM = PIPE_IMG# Use the original pipe image for the bottom pipe

        self.passed = False# Flag to check if the bird has passed the pipe
        self.set_height()# Set the initial height of the gap between the pipes

    # Setting the height of pipes
    def set_height(self):
        self.height = random.randrange(50, 450)# Set a random height for the gap between the pipes
        self.top = self.height - self.PIPE_TOP.get_height()# Calculate the top position of the top pipe
        self.bottom = self.height + self.GAP# Calculate the top position of the bottom pipe

    # Method for moving the pipes
    def move(self):
        self.x -= self.VEL# Move the pipe horizontally based on the velocity

    # Method for drawing the pipes
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))# Draw the top pipe on the window
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))# Draw the bottom pipe on the window

    # Method for collision of the pipes and the bird
    def collide(self, bird):
        bird_mask = bird.get_mask()# Get the mask of the bird
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)# Get the mask of the top pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)# Get the mask of the bottom pipe

        top_offset = (self.x - bird.x, self.top - round(bird.y))# Calculate the offset between bird and top pipe
        bottom_offset = (self.x - bird.x, self.bottom -round(bird.y))# Calculate the offset between bird and bottom pipe

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)# Check for collision between bird and bottom pipe
        t_point = bird_mask.overlap(top_mask, top_offset) # Check for collision between bird and top pipe

        # If collision occurs
        if t_point or b_point:
            return True# Return True (collision has occurred)
        
        return False# Return False (no collision)
    
class Base:
    VEL = 5# Velocity of the base
    WIDTH = BASE_IMG.get_width()# Width of the base image
    IMG = BASE_IMG# Base image

    # Constructor method to initialize the base object
    def __init__(self, y):
        self.y = y# Vertical position of the base
        self.x1 = 0# X position of the first base image
        self.x2 = self.WIDTH# X position of the second base image

    # Method for moving the base
    def move(self):
        self.x1 -= self.VEL# Move the first base image to the left
        self.x2 -= self.VEL# Move the second base image to the left

        # Reset the position of the first base image
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        # Reset the position of the second base image
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    # Method for drawing the base
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))# Draw the first base image
        win.blit(self.IMG, (self.x2, self.y))# Draw the second base image

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: "+ str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #bird.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x <bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        if bird.y +bird.img.get_height() > 730:
            pass


        base.move()
        draw_window(win, bird, pipes, base, score)
    
    pygame.quit()
    quit()

main()
