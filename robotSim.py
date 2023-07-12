import pygame
import math
import os

class Robot:
    def __init__(self, startpos, robotimg, width, follow=None):
        self.leader = False     # is this robot a leader?
        self.follow = follow    # who to follow?

        self.x, self.y = startpos
        self.theta = 0
        self.trail_set = []
        self.w = width
        self.a = 20

        self.u = 30         # linear velocity[pix/sec]
        self.w = 0          # angular velocity[rad/sec]
        self.m2p = 3779.52  # scaling from meters to pixels

        self.img = pygame.image.load(robotimg)  # skin img path provided in the arguments
        self.rotated = self.img
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

    def move(self, event = None):
        self.x += (self.u*math.cos(self.theta) - self.a*math.sin(self.theta)*self.w) * dt
        self.y += (self.u*math.sin(self.theta) - self.a*math.cos(self.theta)*self.w) * dt
        self.theta += self.w * dt

        self.rotated = pygame.transform.rotozoom(self.img,
                                                 math.degrees(-self.theta), 1)
        self.rect = self.rotated.get_rect(center=(self.x, self.y))

        if self.leader == True:
            if event is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.u += 0.001 * self.m2p
                    elif event.key == pygame.K_DOWN:
                        self.u -= 0.001 * self.m2p
                    elif event.key == pygame.K_RIGHT:
                        self.w += 0.0001 * self.m2p
                    elif event.key == pygame.K_LEFT:
                        self.w -= 0.0001 * self.m2p
        else:
            self.following()
    
    def following(self):
        target = self.follow.trail_set[0]
        delta_x = target[0] - self.x
        delta_y = target[1] - self.y
        self.u = delta_x*math.cos(self.theta) + delta_y*math.sin(self.theta)
        self.w = (-1/self.a)*math.sin(self.theta)*delta_x + (1/self.a)*math.cos(self.theta)*delta_y

    def dist(self, point1, point2):
        (x1, y1) = point1
        (x2, y2) = point2
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)

        # calculation
        px = (x1 - x2) ** (2)
        py = (y1 - y2) ** (2)
        distance = (px + py) ** (0.5)
        return distance

    def draw(self, map):
        map.blit(self.rotated, self.rect)
        pass

    def trail(self, pos, map, color):
        for i in range(0, len(self.trail_set)-1):
            pygame.draw.line(map, color, 
                             (self.trail_set[i][0], self.trail_set[i][1]),
                             (self.trail_set[i+1][0], self.trail_set[i+1][1]))
        if self.trail_set.__sizeof__() > 2000:
            self.trail_set.pop(0)
        self.trail_set.append(pos)

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

def robot_simulate(Robot, event=None):
    Robot.move(event=event)
    Robot.draw(environment.map)
    Robot.trail((Robot.x, Robot.y), environment.map, environment.yel)
    
# initialization area
skins = [r'fig/robot_green.png',
         r'fig/robot_red.png',
         r'fig/robot_blue.png',
         r'fig/robot_orange.png',
         r'fig/robot_purple.png']

pygame.init()
running = True
iterations = 0
dt = 0
lasttime = pygame.time.get_ticks()
start = (200, 200)
dims = (600, 1200)
environment = Envir(dims)

# robots----------------
robots_number = 5
robots = []
# leader
robots.append(Robot(start, skins[0], width=80))
robots[0].leader = True
# followers
for i in range(1, robots_number):
    robot = Robot((start[0]-i*100, start[1]), skins[i], 80, robots[i-1])
    robots.append(robot)

# animation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for robot in robots:
            if not robot.leader and iterations<1:
                continue
            robot_simulate(robot, event)
    
    for robot in robots:
        if not robot.leader and iterations < 1:
            continue
        robot_simulate(robot)

    
    pygame.display.update()
    environment.map.fill(environment.black)
    dt = (pygame.time.get_ticks() - lasttime) / 1000    # seconds
    lasttime = pygame.time.get_ticks()
    iterations+=1