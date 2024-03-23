import pygame #adding the pygame lib to use as a game engine.
from sys import exit #to safely interrupt code from running (helps quiting the game)
from random import randint #to create random obstacle's spawn

def display_score():
    current_time = int (pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] #(list comprehension)deletes obstacle from list after pos -100 
        
        return obstacle_list
    else:
        return []

pygame.init() #initializing pygame lib
screen = pygame.display.set_mode((800,400)) #creating a display surface for pygame with 1 fps rendered and an 800x400 screen size(width and height). 
pygame.display.set_caption('introGame') #setting game's name
clock = pygame.time.Clock() #creating a Clock obj to cap the game's fps
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #params: font,size
game_active = False #adding a game status to get check if the game is running
start_time = 0
score = 0

#surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#creating a score
# score_surf = test_font.render('Score', False, (64,64,64)) #params: 'text itself', AntiAliasing, colour
# score_rect = score_surf.get_rect(center = (400,50))

#obstacles (enemies)
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()

fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

#player surface
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom =(80,300)) #create a rectangle using the surface's size
player_grav = 0 #gravity to improve falling feel

#intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha() #image of our hero at the start
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('introGame', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to Run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))

#timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 1500)

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
                    start_time = int (pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100),300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100),210)))


    if game_active: #the game part
        #screen blit == block image transfer, meaning putting one surface on other 
        screen.blit(ground_surface,(0,300)) #params: surface object, position
        screen.blit(sky_surface,(0,0))   
        # pygame.draw.rect(screen, '#c0e8ec', score_rect) #params: display surface, colour, object, size
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) #to add margins
        # screen.blit(score_surf,score_rect)
        score = display_score()

        #snail blit
        # snail_rect.x -= 6
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf,(snail_rect))

        #player blit
        player_grav += 1 #to get a constant downforce to our player
        player_rect.y += player_grav #to get a "real" gravity for falling
        if player_rect.bottom >= 300: #to add a "collision with ground" without using collisions to save resources.
            player_rect.bottom = 300 
        screen.blit(player_surf,player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    #adding a game over
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
    else: #intro part of our game
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        #making a global score
        score_message = test_font.render(f'Your Score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center= (400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update() #updates the display surface
    clock.tick(60) #frames per seccond capped to 60
