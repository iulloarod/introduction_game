import pygame #adding the pygame lib to use as a game engine.
from sys import exit #to safely interrupt code from running (helps quiting the game)
from random import randint, choice #to create random obstacle's spawn

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0 #to pick wich surface to use
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom <300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

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

#adding a collider detector
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation(): #plays walking if player is on floor, and jumping if not on floor
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init() #initializing pygame lib
screen = pygame.display.set_mode((800,400)) #creating a display surface for pygame with 1 fps rendered and an 800x400 screen size(width and height). 
pygame.display.set_caption('introGame') #setting game's name
clock = pygame.time.Clock() #creating a Clock obj to cap the game's fps
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #params: font,size
game_active = False #adding a game status to get check if the game is running
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.2)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#static surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

#obstacles (enemies) surfaces
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = [] #to create a set of enemies rendered on screen

#player surface
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 #to pick wish surface to use
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
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

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer, 200)

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
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]



    if game_active: #the game part
        screen.blit(ground_surface,(0,300)) #params: surface object, position
        screen.blit(sky_surface,(0,0))   
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collisions   
        game_active = collision_sprite()

    else: #intro part of our game
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_grav = 0
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
