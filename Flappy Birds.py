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
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VALOCITY

    # Method for drawing the bird on the game window
    def draw(self, win):
        self.img_count += 1# Increase the image counter

        # Animation for wing flap
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

        # Animation when the bird is nosediving
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)# Rotate the bird image
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)# Adjust the position
        win.blit(rotated_image, new_rectangle.topleft)# Draw the rotated image onto the window

    # Create and return a mask for collision detection
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom -round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

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
