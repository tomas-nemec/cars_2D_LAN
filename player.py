import math
import pygame
from utils import rotate_center

class AbstractPlayer:
    def __init__(self,max_vel, rotation_vel, x, y, ID, name):
        self.ID = ID
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = x, y
        self.acceleration = 0.1
        self.name = name

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def render(self, win, image):
        rotate_center(win, image,(self.x, self.y), self.angle )

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()



    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collision(self, mask_map,mask_car, x=0, y=0):
        offset = (int(self.x - x), int(self.y - y))
        point_of_intersection = mask_map.overlap(mask_car, offset)
        return point_of_intersection


class Player(AbstractPlayer):
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel