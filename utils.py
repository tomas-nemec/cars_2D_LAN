import pygame

# function to resize picture
def scale_image(img, factor):
    new_size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, new_size)

# function to rotate object
def rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)