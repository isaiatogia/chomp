import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fight Game Experiment") # name displayed atop game window

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]# player scores, [Knight 1, Knight 2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
K1_SIZE_X = 120
K1_SIZE_Y = 80
K1_SCALE = 3.5
K1_DATA = [K1_SIZE_X, K1_SIZE_Y, K1_SCALE]
K2_SIZE_X = 120
K2_SIZE_Y = 80
K2_SCALE = 3.5
K2_DATA = [K2_SIZE_X, K2_SIZE_Y, K2_SCALE]

# load music and sounds
pygame.mixer.music.load("../Final Fight Game/assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("../Final Fight Game/assets/audio/sword.wav")
sword_fx.set_volume(0.5)

# load background image
bg_image = pygame.image.load("../Final Fight Game/assets/images/background/Forest.png").convert_alpha()

# load fighter spritesheets
k1_sheet = pygame.image.load("../Final Fight Game/assets/images/knight_1/full_k1_spritesheet.png").convert_alpha()
k2_sheet = pygame.image.load("../Final Fight Game/assets/images/knight_2/full_k2_spritesheet.png").convert_alpha()

# define number of steps in each animation
K1_ANIMATION_STEPS = [4, 6, 6, 10, 10, 4, 1, 4, 3, 1, 8, 2, 10, 10, 3, 1, 10, 3, 2, 12, 10, 2, 4, 1, 1, 3, 7, 7, 1, 3]
K2_ANIMATION_STEPS = [4, 6, 6, 10, 10, 4, 1, 4, 3, 1, 8, 2, 10, 10, 3, 1, 10, 3, 2, 12, 10, 2, 4, 1, 1, 3, 7, 7, 1, 3]
# define font
victory_font = pygame.font.Font("../Final Fight Game/assets/fonts/Canterbury.ttf", 100)
count_font = pygame.font.Font("../Final Fight Game/assets/fonts/Canterbury.ttf", 80)
score_font = pygame.font.Font("../Final Fight Game/assets/fonts/Canterbury.ttf", 30)

# load victory image
victory_1 = victory_font.render("Knight 1 Wins", True, (255, 0, 0))
victory_2 = victory_font.render("Knight 2 Wins", True, (255, 0, 0))

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) #scale image to screen dimensions
    screen.blit(scaled_bg, (0, 0))

# function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x -2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

# create two instances of fighters
fighter_1 = Fighter(1,200, 395, False, K1_DATA, k1_sheet, K1_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2,800, 395, True, K2_DATA, k2_sheet, K2_ANIMATION_STEPS, sword_fx)

# game loop
running = True
while running:

    # limit FPS
    clock.tick(FPS)

    # draw background
    draw_bg()

    # show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("Knight 1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("Knight 2: " + str(score[1]), score_font, RED, 580, 60)

    # update countdown
    if intro_count <= 0:
        # enable fighter movement after countdown
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) > 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            print(intro_count)

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            screen.blit(victory_2,(SCREEN_WIDTH / 2 - victory_2.get_width() / 2, SCREEN_HEIGHT / 8 - victory_2.get_height() / 2))
            round_over_time = pygame.time.get_ticks()

        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            screen.blit(victory_1,(SCREEN_WIDTH / 2 - victory_1.get_width() / 2, SCREEN_HEIGHT / 8 - victory_1.get_height() / 2))
            round_over_time = pygame.time.get_ticks()

    else:
        # display victory image
        if fighter_1.alive == False:
            screen.blit(victory_2, (230, 150))
        elif fighter_2.alive == False:
            screen.blit(victory_1, (230, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 200, 395, False, K1_DATA, k1_sheet, K1_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 800, 395, True, K2_DATA, k2_sheet, K2_ANIMATION_STEPS, sword_fx)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # update display
    pygame.display.update()

# exit pygame
pygame.quit()