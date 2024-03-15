#adding the pygame lib to use as a game engine.
import pygame

#initializing pygame lib
pygame.init()
#creating a display surface for pygame with 1 fps rendered and an 800x400 screen size(width and height). 
screen = pygame.display.set_mode((800,400))
#to continue playing the game (continuous fps rendered), all of my code needs to be inside a while loop. 
while True: #keeps the game running indefinetly. Draw all elements and update everything
    for event in pygame.event.get(): #catches all events
        if event.type == pygame.quit:
            pygame.quit() #for the user to quit the game
    pygame.display.update() #updates the display surface