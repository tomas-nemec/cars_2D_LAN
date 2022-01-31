import socket
import pygame
from utils import scale_image, rotate_center
from client import Client
from player import *
import copy

WIDTH, HEIGHT = 600, 500

# load images
BG = pygame.image.load("imgs/BG.png")
FINISH = scale_image(pygame.image.load("imgs/finish.png"), 1)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_LOCATION = (10, 300)
TRACK = scale_image(pygame.image.load("imgs/track2.png"), 1)
TRACK_BOARDER  = scale_image(pygame.image.load("imgs/track-border2.png"), 1)
TRACK_BOARDER_MASK = pygame.mask.from_surface(TRACK_BOARDER)


# full scene except cars
bg_images = [(BG, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_LOCATION), (TRACK_BOARDER, (0, 0))]

# CARS
CAR1 = scale_image(pygame.image.load("imgs/car_red.png"),0.5)
CAR2 = scale_image(pygame.image.load("imgs/car_blue.png"),0.5)
CAR3 = scale_image(pygame.image.load("imgs/car_green.png"),0.5)
CAR4 = scale_image(pygame.image.load("imgs/car_yellow.png"),0.5)
CAR5 = scale_image(pygame.image.load("imgs/car_grey.png"),0.5)
# CAR masks
CAR1_mask = pygame.mask.from_surface(CAR1)
CAR2_mask = pygame.mask.from_surface(CAR2)
CAR3_mask = pygame.mask.from_surface(CAR3)
CAR4_mask = pygame.mask.from_surface(CAR4)
CAR5_mask = pygame.mask.from_surface(CAR5)

CARS = [CAR1, CAR2, CAR3, CAR4, CAR5]
CARS_masks = [CAR1_mask, CAR2_mask, CAR3_mask, CAR4_mask, CAR5_mask]

# Dynamic variables
players = []

# FUNCTIONS
def redraw_window(win, images, players, main_player):
    for img, pos in images:
        win.blit(img, pos)

    for player in players:
        if player.ID != main_player.ID:
            player.render(win, CARS[player.ID])

    main_player.render(win, CARS[main_player.ID])

    pygame.display.update()  # redraw everything

# handling of player movement
def movement_of_player(player_car):
    keys = pygame.key.get_pressed()  # what
    moved = False
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()




def main(name):
    clock = pygame.time.Clock()

    global players

    server = Client()      # instance of client = access to server
    current_id = server.connect(name)   # function in class Client returning ID
    print(f"Current ID: {str(current_id)}")
    players = server.send("get")

    current_player = copy.deepcopy(players[current_id])

    run = True
    while run:
        clock.tick(30)  # 30 FPS


        movement_of_player(current_player)        # players[current_id]

        if current_player.collision(TRACK_BOARDER_MASK, CARS_masks[current_id]) != None:
            current_player.bounce()

        data = "move " + str(round(current_player.x)) + " " + str(round(current_player.y)) + " " + str(round(current_player.angle)) # + " " + str(players[current_id].vel)

        players = server.send(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window(WIN, bg_images, players,current_player)









name = "Tomas"     #name = input("Enter your name: ")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing cars - LAN")

main(name)
