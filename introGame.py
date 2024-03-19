import pygame #adding the pygame lib to use as a game engine.
from sys import exit #to safely interrupt code from running (helps quiting the game)

pygame.init() #initializing pygame lib
screen = pygame.display.set_mode((800,400)) #creating a display surface for pygame with 1 fps rendered and an 800x400 screen size(width and height). 
pygame.display.set_caption('introGame') #setting game's name
clock = pygame.time.Clock() #creating a Clock obj to cap the game's fps
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #params: font,size

#surfaces
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = test_font.render('My game', False, 'Green') #params: 'text itself', AntiAliasin, colour
#adding a movable surface
snail_surface = pygame.image.load('graphics/snail/snail1.png')
snail_x_pos = 600

while True: #keeps the game running indefinetly. Draw all elements and update everything
    for event in pygame.event.get(): #event catcher
        if event.type == pygame.QUIT: #it's QUIT, not quit.
            pygame.quit() #for the user to quit the game. This creates an error because python can't keep up, but it's solved with the "exit" function
            exit() #ends the game. at least on windows
#blit == block image transfer, meaning putting one surface on other 
    screen.blit(ground_surface,(0,300)) #params: surface object, position
    screen.blit(sky_surface,(0,0))   
    screen.blit(text_surface,(300,50))
    snail_x_pos -= 4 #to move the snail
    if snail_x_pos < -100:
        snail_x_pos = 800
    screen.blit(snail_surface,(snail_x_pos,275))

    pygame.display.update() #updates the display surface
    clock.tick(60) #frames per seccond capped to 60
