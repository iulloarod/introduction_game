import pygame #adding the pygame lib to use as a game engine.
from sys import exit #to safely interrupt code from running (helps quiting the game)

def display_score():
    current_time = int (pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)

pygame.init() #initializing pygame lib
screen = pygame.display.set_mode((800,400)) #creating a display surface for pygame with 1 fps rendered and an 800x400 screen size(width and height). 
pygame.display.set_caption('introGame') #setting game's name
clock = pygame.time.Clock() #creating a Clock obj to cap the game's fps
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #params: font,size
game_active = True #adding a game status to get check if the game is running
start_time = 0

#surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#creating a score
# score_surf = test_font.render('Score', False, (64,64,64)) #params: 'text itself', AntiAliasing, colour
# score_rect = score_surf.get_rect(center = (400,50))

#adding a movable surface
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright = (600,300))

#adding a player surface
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom =(80,300)) #create a rectangle using the surface's size
player_grav = 0 #gravity to improve falling feel

while True: #keeps the game running indefinetly. Draw all elements and update everything
    for event in pygame.event.get(): #event catcher
        if event.type == pygame.QUIT: #it's QUIT, not quit.
            pygame.quit() #for the user to quit the game. This creates an error because python can't keep up, but it's solved with the "exit" function
            exit() #ends the game. at least on windows
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300: #to jump AND jumping only if the player is at ground level
                if player_rect.collidepoint(event.pos):
                    player_grav = -20 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: #to jump AND jumping only if the player is at ground level    
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 800
                    start_time = int (pygame.time.get_ticks() / 1000)

    if game_active: #the game part
        #screen blit == block image transfer, meaning putting one surface on other 
        screen.blit(ground_surface,(0,300)) #params: surface object, position
        screen.blit(sky_surface,(0,0))   
        # pygame.draw.rect(screen, '#c0e8ec', score_rect) #params: display surface, colour, object, size
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) #to add margins
        # screen.blit(score_surf,score_rect)
        display_score()

        #snail blit
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surf,(snail_rect))

        #player blit
        player_grav += 1 #to get a constant downforce to our player
        player_rect.y += player_grav #to get a "real" gravity for falling
        if player_rect.bottom >= 300: #to add a "collision with ground" without using collisions to save resources.
            player_rect.bottom = 300 
        screen.blit(player_surf,player_rect)

    #adding a game over
        if snail_rect.colliderect(player_rect):
            game_active = False
    else: #intro part of our game
        screen.fill('Black')

    pygame.display.update() #updates the display surface
    clock.tick(60) #frames per seccond capped to 60
