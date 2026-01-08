import os
import pygame
from sys import exit
from random import randint

# --------------------------------------------------
# Path handling (IMPORTANT)
# --------------------------------------------------
BASE_PATH = os.path.dirname(__file__)

def resource_path(*path):
    return os.path.join(BASE_PATH, *path)

# --------------------------------------------------
# Functions
# --------------------------------------------------
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_index, player_surface
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

# --------------------------------------------------
# Pygame setup
# --------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('RUNNER')
clock = pygame.time.Clock()

test_font = pygame.font.Font(
    resource_path('assets', 'font', 'Pixeltype.ttf'), 50
)

game_active = True
start_time = 0
score = 0

# --------------------------------------------------
# Audio
# --------------------------------------------------
bg_music = pygame.mixer.Sound(
    resource_path('assets', 'audio', 'music.wav')
)
bg_music.play(loops=-1)
bg_music.set_volume(0.2)

jump_sound = pygame.mixer.Sound(
    resource_path('assets', 'audio', 'audio_jump.mp3')
)

# --------------------------------------------------
# Background
# --------------------------------------------------
sky_surface = pygame.image.load(
    resource_path('assets', 'images', 'Sky.png')
).convert()

ground_surface = pygame.image.load(
    resource_path('assets', 'images', 'ground.png')
).convert()

# --------------------------------------------------
# Obstacles
# --------------------------------------------------
snail_frames = [
    pygame.image.load(resource_path('assets', 'images', 'snail1.png')).convert_alpha(),
    pygame.image.load(resource_path('assets', 'images', 'snail2.png')).convert_alpha()
]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frames = [
    pygame.image.load(resource_path('assets', 'images', 'fly1.png')).convert_alpha(),
    pygame.image.load(resource_path('assets', 'images', 'fly2.png')).convert_alpha()
]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# --------------------------------------------------
# Player
# --------------------------------------------------
player_walk = [
    pygame.image.load(resource_path('assets', 'images', 'player_walk_1.png')).convert_alpha(),
    pygame.image.load(resource_path('assets', 'images', 'player_walk_2.png')).convert_alpha()
]
player_index = 0
player_surface = player_walk[player_index]

player_jump = pygame.image.load(
    resource_path('assets', 'images', 'jump.png')
).convert_alpha()

player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# --------------------------------------------------
# Intro screen
# --------------------------------------------------
player_stand = pygame.image.load(
    resource_path('assets', 'images', 'player_stand.png')
).convert_alpha()

player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand_scaled.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_msg = test_font.render('Press space to start again', False, (111, 196, 169))
game_msg_rect = game_msg.get_rect(center=(400, 360))

# --------------------------------------------------
# Timers
# --------------------------------------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# --------------------------------------------------
# Game loop
# --------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(
                        snail_surface.get_rect(bottomright=(randint(900, 1100), 300))
                    )
                else:
                    obstacle_rect_list.append(
                        fly_surf.get_rect(bottomright=(randint(900, 1100), 210))
                    )

            if event.type == snail_animation_timer:
                snail_frame_index = 1 - snail_frame_index
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                fly_frame_index = 1 - fly_frame_index
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()
        screen.blit(player_surface, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)

        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_msg = test_font.render(f'Your score : {score}', False, (111, 196, 169))
        score_msg_rect = score_msg.get_rect(center=(400, 330))

        screen.blit(game_name, game_name_rect)
        screen.blit(game_msg, game_msg_rect)
        screen.blit(score_msg, score_msg_rect)

    pygame.display.update()
    clock.tick(60)
