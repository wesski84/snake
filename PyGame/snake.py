import pygame
import time
import random

pygame.init()

white =(255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)
silver = (192,192,192)

display_height = 600
display_width = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('Slither')

icon = pygame.image.load('images/snakehead.png')
pygame.display.set_icon(icon,)

img_head = pygame.image.load('images/snakehead_small_up.png')
img_body = pygame.image.load('images/snakebody_small.png')
img_apple = pygame.image.load('images/apple_small.png')
img_mouse = pygame.image.load('images/mouse_small.png')
img_victory = pygame.image.load('images/snake_med.png')
img_speedup = pygame.image.load('images/speedup.png')
img_slowdown = pygame.image.load('images/slowdown.png')



clock = pygame.time.Clock()

block_size = 20
FPS = 15

direction = 'Right'

fontSize = 30

xsmallfont = pygame.font.SysFont(None, 15)
smallfont = pygame.font.SysFont(None, 25)
medfont = pygame.font.SysFont(None, 50)
largefont = pygame.font.SysFont(None, 80)

appleThickness = 30


def victory():

    victory = True

    while victory:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    victory = False
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Congratulations! You win!", blue, -250, 'medium')
        gameDisplay.blit(img_victory, [275, 100])
        message_to_screen("Press 'C' to start a new game or 'Q' to quit.", black, 215, 'small')

        pygame.display.update()
        clock.tick(5)


def pause():

    paused = True

    message_to_screen("Paused", black, -100, 'large')
    message_to_screen("Press 'C' to continue or 'Q' to quit.", black, 25, 'small')
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c or event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        # gameDisplay.fill(silver)


        clock.tick(5)

def score(score):
    text = smallfont.render("Score: " + str(score),True, black)
    gameDisplay.blit(text,[10,10])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - appleThickness))  # / 10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height - appleThickness))  # / 10.0) * 10.0
    return randAppleX, randAppleY

def randPowerGen():
    randPowerX = round(random.randrange(0, display_width - appleThickness))  # / 10.0) * 10.0
    randPowerY = round(random.randrange(0, display_height - appleThickness))  # / 10.0) * 10.0
    return randPowerX, randPowerY


def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither", blue, -100, 'large')
        message_to_screen("The objective is to eat mice and grow larger", black, -30, 'small')
        message_to_screen("The more mice you eat, the longer you get", black, 10, 'small')
        message_to_screen("It's game over if you run into the edges, or yourself.", black, 50, 'small')
        message_to_screen("Press 'C' to play or 'Q' to quit.", black, 180, 'small')
        message_to_screen("Press 'P' or hit the Spacebar to pause.", black, 220, 'small')
        message_to_screen("© 2017 Mark Wesolowski", black, 280, 'xsmall')

        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):

    if direction == 'Right':
        head = pygame.transform.rotate(img_head,270)
    elif direction == 'Left':
        head = pygame.transform.rotate(img_head, 90)
    elif direction == 'Down':
        head = pygame.transform.rotate(img_head, 180)
    elif direction == "Up":
        head = img_head

    gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
    for XnY in snakeList[:-1]:
        # pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])
        gameDisplay.blit(img_body, [XnY[0], XnY[1]])

def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    elif size == 'medium':
        textSurface = medfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
    elif size == 'xsmall':
        textSurface = xsmallfont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg,color, y_displace=0, size = 'small'):
    textSurf, textRect = text_objects(msg, color, size)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text,[display_width/2 - msglen, display_height/2])
    textRect.center = (display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def gameLoop():
    global direction
    direction = 'Right'

    speed = 10
    speed_factor = 1

    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = speed
    lead_y_change = 0

    snakeList = []
    snakeLength = 1


    randAppleX, randAppleY = randAppleGen()
    randPowerX, randPowerY = randPowerGen()

    while not gameExit:

        if gameOver == True:
            message_to_screen("Game Over", red, -50, size='large')
            message_to_screen("Press 'C' to Continue, or 'Q' to Quit", blue, 50, size='medium')
            pygame.display.update()

        while gameOver == True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = 'Left'
                    lead_x_change =  -speed * speed_factor
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = 'Right'
                    lead_x_change = +speed * speed_factor
                    lead_y_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = 'Up'
                    lead_y_change = -speed * speed_factor
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = 'Down'
                    lead_y_change = +speed * speed_factor
                    lead_x_change = 0
                elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        gameDisplay.blit(img_mouse, [randAppleX, randAppleY])

        # if snakeLength%2 == 0:
        #     gameDisplay.blit(img_speedup, [randPowerX, randPowerY])
        # elif snakeLength-1%2 == 0:
        #     gameDisplay.blit(img_slowdown, [randPowerX, randPowerY])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size, snakeList)
        score(snakeLength-1)

        pygame.display.update()


        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
                if speed_factor < 2:
                    speed_factor += .1
                if snakeLength-1 == 200:
                    victory()

        # if lead_x > randPowerX and lead_x < randPowerX + block_size or lead_x + block_size > randPowerX and lead_x + block_size < randPowerX + block_size:
        #     if lead_y > randPowerY and lead_y < randPowerY + block_size or lead_y + block_size > randPowerY and lead_y + block_size < randPowerY + block_size:
        #         randPowerX, randPowerY = (-20,-20)
        #         speed_factor -= 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()
