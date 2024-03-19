import pygame #adding the pygame lib to use as a game engine.
from sys import exit #to safely interrupt code from running (helps quiting the game)

pygame.init() #initializing pygame lib
screen = pygame.display.set_mode((800,400)) #creating a display surface for pygame with 1 fps rendered and an 800x400 screen size(width and height). 
pygame.display.set_caption('introGame') #setting game's name
clock = pygame.time.Clock() #creating a Clock obj to cap the game's fps

sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

while True: #keeps the game running indefinetly. Draw all elements and update everything
    for event in pygame.event.get(): #event catcher
        if event.type == pygame.QUIT: #it's QUIT, not quit.
            pygame.quit() #for the user to quit the game. This creates an error because python can't keep up, but it's solved with the "exit" function
            exit() #ends the game. at least on windows

    screen.blit(sky_surface,(0,0)) #blit == block image transfer, meaning putting one surface on other   
    screen.blit(ground_surface,(0,300))

    pygame.display.update() #updates the display surface
    clock.tick(60) #frames per seccond capped to 60
