import pygame
import math

class Robot:
    def __init__(self, startpos, robotimg, width, follow=None):
        self.leader = False     # is this robot a leader?
        self.follow = follow    # who to follow?

        self.x, self.y = startpos
        self.theta = 0
        self.w = width

        self.u = 30         # linear velocity[pix/sec]
        self.w = 0          # angular velocity[rad/sec]
        self.m2p = 3779.52  # scaling from meters to pixels

        self.img = pygame.image.load(robotimg)  # skin img path provided in the arguments
        

    def move(self):
        pass

    def following(self):
        pass

    def dist(self, point1, point2):
        pass

    def draw(self):
        pass

    def trail(self):
        pass

class Envir:
    def __init__(self, dimentions):
        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        # map dimention
        self.height, self.width = dimentions
        
        # window settings
        pygame.display.set_caption("diff drive")
        self.map = pygame.display.set_mode((self.width, self.height))
        pass

    def write_info(self):
        pass

    def robot_frame(self):
        pass

# initialization
pygame.init()
running = True
start = (200, 200)
dims = (600, 1200)
environment = Envir(dims)

# animation loop
while running:
    for event in pytame.event.get():
        if event.type == pygame.QUIT:
            running = False