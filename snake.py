# snake game in python
import pygame
import random
import time

# grid layout for blocks
# 1   2   3   ...   25
# 26  27  28  ...   50
# .                 .
# .                 .
# .                 .
# 601               626
# ex: block 28 location:  
# 28 % 25 = 3 then (3 * 20) + 10 = 70 (so offset in 70px right)
# 28 // 25 = 1 then (1* 20) + 10 = 30 (so offset in 30px down)

# game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 520, 600 # screen size (25 x 25 blocks) 
BLOCK_SIZE = 20 # block / grid size
SNAKE_BLOCK_HEIGHT = 12 # snake block height
SNAKE_BLOCK_WIDTH = 20 # snake block width 
APPLE = (255, 0, 0) # apple color (red)
SNAKE = (255, 255, 0) # snake color
SNAKE_HEAD = (255, 255, 25) # color of snake head
GREY = (211, 211, 211) # grid colour
BLACK = (0, 0, 0) # background color
BOMB = (255, 165, 0) # bomb will be an orange with a red (apple) centre
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80

# current direction, 1=left, 2=down, 3=right, 4=up (1 is default)
currentDirection = 1
# player score
score = 0
# game speed (.075 is default)
gameSpeed = 0.075

# bomb location
bombInt = 0
bombX = 0
bombY = 0

# array of pairs having each coordinate (x,y) and last direction (1,2,3 or 4)
snakeLocation = []

# Functions for handling game logic
def checkCollision():
    global running
    global score
    global gameSpeed
    # Check if the snake hit border
    if snakeLocation[0][0] <= 10 or snakeLocation[0][0] >= SCREEN_WIDTH - 10:
        running = False
    if snakeLocation[0][1] <= 10 or snakeLocation[0][1] >= SCREEN_HEIGHT - 90:
        running = False
    
    # check if snake hit itself
    for i in range(len(snakeLocation)):
        for j in range(len(snakeLocation)):
            if snakeLocation[i] == snakeLocation[j] and i != j:
                running = False

    # check if snake hit bomb
    if snakeLocation[0][0] >= bombX - 20 and snakeLocation[0][0] <= bombX + 20 and snakeLocation[0][1] >= bombY - 20 and snakeLocation[0][1] <= bombY + 20:
        running = False

    # apple hit, change score
    if snakeLocation[0][0] == appleX:
        if snakeLocation[0][1] == appleY:
            score += 1
            addSnake()
            newApple()
            # game speed increases based on score
            if score == 4:
                gameSpeed = 0.05
            elif score == 8:
                gameSpeed = 0.04
            elif score == 12:
                gameSpeed = 0.03

# legthen snake 
def addSnake():
    if currentDirection == 1: # left
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] + 5, snakeLocation[len(snakeLocation) - 1][1], 1])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] + 5, snakeLocation[len(snakeLocation) - 1][1], 1])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] + 5, snakeLocation[len(snakeLocation) - 1][1], 1])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] + 5, snakeLocation[len(snakeLocation) - 1][1], 1])
    elif currentDirection == 2: # down
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] - 5, 2])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] - 5, 2])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] - 5, 2])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] - 5, 2])
    elif currentDirection == 3: # right
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] - 5, snakeLocation[(len(snakeLocation) - 1)][1], 3])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] - 5, snakeLocation[(len(snakeLocation) - 1)][1], 3])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] - 5, snakeLocation[(len(snakeLocation) - 1)][1], 3])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] - 5, snakeLocation[(len(snakeLocation) - 1)][1], 3])
    else: # up
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] + 5, 4])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] + 5, 4])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] + 5, 4])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0], snakeLocation[(len(snakeLocation) - 1)][1] + 5, 4])

# generate new apple
def newApple():
    global appleInt
    global appleX
    global appleY

    valid = False
    while not valid:
        appleInt = random.randint(1, 625)
        appleX = (((appleInt % 25) - 1) * 20) + 20
        if appleInt % 25 == 0:
            appleX = 500
        
        # minus 1 b/c of 25 becoming 1 when should be 0 and so on
        appleY = (((appleInt-1) // 25) * 20) + 20

        for i in snakeLocation:
            if appleX != i[0] and appleY != i[1]:
                valid = True
    # draw apple
    pygame.draw.circle(screen, APPLE, (appleX, appleY), 6)

# draw apple
def drawApple():
    pygame.draw.circle(screen, APPLE, (appleX, appleY), 6)

# draw snake
def drawSnake():
    # screen, circle color, circle centre, circle radius (6 b/c = 12 then 2 px gap each side)
    # pygame.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))
    if currentDirection == 1: # left bot left top left
        pygame.draw.rect(screen, SNAKE, (snakeLocation[0][0]-10, snakeLocation[0][1]-10, 20, 20), border_bottom_left_radius=10, border_top_left_radius=10,)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]-4, snakeLocation[0][1]-4), 2) # eye
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]-4, snakeLocation[0][1]+4), 2) # eye
        pygame.draw.circle(screen, APPLE, (snakeLocation[0][0]+4, snakeLocation[0][1]), 4)  # Large circle mouth
        pygame.draw.circle(screen, SNAKE, (snakeLocation[0][0]+2, snakeLocation[0][1]), 4)  # Smaller circle (overlapping) mouth
    elif currentDirection == 2: # down bot left bot right
        pygame.draw.rect(screen, SNAKE, (snakeLocation[0][0]-10, snakeLocation[0][1]-10, 20, 20), border_bottom_left_radius=10, border_bottom_right_radius=10)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]+4, snakeLocation[0][1]+4), 2)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]-4, snakeLocation[0][1]+4), 2)
        pygame.draw.circle(screen, APPLE, (snakeLocation[0][0], snakeLocation[0][1]-4), 4)  # Large circle
        pygame.draw.circle(screen, SNAKE, (snakeLocation[0][0], snakeLocation[0][1]-2), 4)  # Smaller circle (overlapping)
    elif currentDirection == 3: # right bot right top right
        pygame.draw.rect(screen, SNAKE, (snakeLocation[0][0]-10, snakeLocation[0][1]-10, 20, 20), border_bottom_right_radius=10, border_top_right_radius=10)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]+4, snakeLocation[0][1]-4), 2)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]+4, snakeLocation[0][1]+4), 2)
        pygame.draw.circle(screen, APPLE, (snakeLocation[0][0]-4, snakeLocation[0][1]), 4)  # Large circle
        pygame.draw.circle(screen, SNAKE, (snakeLocation[0][0]-2, snakeLocation[0][1]), 4)  # Smaller circle (overlapping)
    else: # up top left top right
        pygame.draw.rect(screen, SNAKE, (snakeLocation[0][0]-10, snakeLocation[0][1]-10, 20, 20), border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]-4, snakeLocation[0][1]-4), 2)
        pygame.draw.circle(screen, BLACK, (snakeLocation[0][0]+4, snakeLocation[0][1]-4), 2)
        pygame.draw.circle(screen, APPLE, (snakeLocation[0][0], snakeLocation[0][1]+4), 4)  # Large circle
        pygame.draw.circle(screen, SNAKE, (snakeLocation[0][0], snakeLocation[0][1]+2), 4)  # Smaller circle (overlapping)

    last = 1
    for i in snakeLocation[1:]:
        if i[2] == 1: #left
            if last != 1:
                pygame.draw.rect(screen, SNAKE, (i[0]+5, i[1]-10, 10, 20))
            else:
                pygame.draw.rect(screen, SNAKE, (i[0]+5, i[1]-10, 5, 20))
        elif i[2] == 2: # down
            if last != 2:
                pygame.draw.rect(screen, SNAKE, (i[0]-10, i[1]-15, 20, 10))
            else:
                pygame.draw.rect(screen, SNAKE, (i[0]-10, i[1]-10, 20, 5))
        elif i[2] == 3: # right
            if last != 3:
                pygame.draw.rect(screen, SNAKE, (i[0]-15, i[1]-10, 10, 20))
            else:
                pygame.draw.rect(screen, SNAKE, (i[0]-10, i[1]-10, 5, 20))
        else: # up
            if last != 4:
                pygame.draw.rect(screen, SNAKE, (i[0]-10, i[1]+5, 20, 10))
            else:
                pygame.draw.rect(screen, SNAKE, (i[0]-10, i[1]+5, 20, 5))
        last = i[2]

def newBomb():
    global bombX
    global bombY
    global bombInt

    valid = False
    while not valid:
        random.seed(random.randint(1,300))
        bombInt = random.randint(1, 625)
        bombX = (((bombInt % 25) - 1) * 20) + 20
        # minus 1 b/c of 25 becoming 1 when should be 0 and so on
        bombY = (((bombInt-1) // 25) * 20) + 20

        # checking border proximity
        if bombX - 40 <= 10:
            bombX += 40
        elif bombX + 40 >= 490:
            bombX -= 40
        if bombY - 40 <= 10:
            bombY += 40
        elif bombY + 40 >= 490:
            bombY -= 40
        
        # checking snake proximity
        for i in snakeLocation:
            if bombX - 80 >= i[0] and bombX + 80 <= i[0] and bombY - 80 >= i[1] and bombY + 80 <= i[1]:
                valid = False
        
        # check apple proximity
        if bombX - 40 >= appleX and bombX + 40 <= appleX and bombY - 40 >= appleY and bombY + 40 <= appleY:
            valid = False
        
        # all checks passed, valid true
        valid = True
        
    # draw bomb (outside)
    pygame.draw.circle(screen, BOMB, (bombX, bombY), 28)
    # draw bomb (middle)
    pygame.draw.circle(screen, APPLE, (bombX, bombY), 10)

def drawBomb():
    # dont draw at the start of game 
    if bombInt != 0:
        # draw bomb (outside)
        pygame.draw.circle(screen, BOMB, (bombX, bombY), 28)
        # draw bomb (middle)
        pygame.draw.circle(screen, APPLE, (bombX, bombY), 10)

# Function to draw the game grid
def draw_grid():
    for row in range(int((SCREEN_WIDTH - 20) / BLOCK_SIZE)):
        for col in range(int((SCREEN_HEIGHT - 90) / BLOCK_SIZE)):
            # pygame.draw.rect(target, color, width, height, line width, line height, line thickness)
            pygame.draw.rect(screen, GREY, ((col * BLOCK_SIZE) + 10, (row * BLOCK_SIZE) + 10, BLOCK_SIZE, BLOCK_SIZE), 1)

# -->>>> Game Logic <<<<--
# ---------------------- Lobby Screen ----------------------
# initialize pygame
pygame.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Snake")

font = pygame.font.Font(None, 100)
text = font.render("Snake", True, GREY)
textRect = text.get_rect()
textRect = (80, 20)

font2 = pygame.font.Font(None, 40)
text2 = font2.render("SPACE to start", True, GREY)
textRect2 = text2.get_rect()
textRect2 = (100,120)

# coloring in display
screen.fill(BLACK)
# drawing text
screen.blit(text, textRect)
screen.blit(text2, textRect2)

# Draw game elements
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
                break

# ---------------------- Main Game ----------------------
# creating game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

firstOpen = True
bombCount = 0 # bomb counter to reroll every couple seconds
running = True
while running:
    time.sleep(gameSpeed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # initialize snake when first run
    if firstOpen:
        # Update the display
        screen.fill(BLACK)
        # drawing grid on screen
        draw_grid()
        # initialize snake 
        current_x = SCREEN_HEIGHT / 2 - 40
        current_y = SCREEN_WIDTH / 2
        snakeLocation = [[current_x, current_y, 1], [current_x + 5, current_y, 1]]
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] + 10, snakeLocation[len(snakeLocation) - 1][1], 1])
        snakeLocation.append([snakeLocation[(len(snakeLocation) - 1)][0] + 15, snakeLocation[len(snakeLocation) - 1][1], 1])
        drawSnake()
        newApple()
        # end first open
        firstOpen = False

    # texts
    font = pygame.font.Font(None, 80)
    text = font.render("Score: " + str(score), True, GREY)
    textRect = text.get_rect()
    textRect = (20,540)

    # Handle user input for movement (cannot move in opposite direction (left to right))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if currentDirection != 3 and snakeLocation[0][0]%20==0 and snakeLocation[0][1]%20==0:
            currentDirection = 1
    if keys[pygame.K_RIGHT]:
        if currentDirection != 1 and snakeLocation[0][0]%20==0 and snakeLocation[0][1]%20==0:
            currentDirection = 3  
    if keys[pygame.K_DOWN]:
        if currentDirection != 4 and snakeLocation[0][0]%20==0 and snakeLocation[0][1]%20==0:
            currentDirection = 2
    if keys[pygame.K_UP]:
        if currentDirection != 2 and snakeLocation[0][0]%20==0 and snakeLocation[0][1]%20==0:
            currentDirection = 4

    # Game logic goes here
    if currentDirection == 1: # left
        for i in reversed(range(1,len(snakeLocation))):
            snakeLocation[i][0] = int(snakeLocation[i-1][0])
            snakeLocation[i][1] = int(snakeLocation[i-1][1])
            snakeLocation[i][2] = int(snakeLocation[i-1][2])
        snakeLocation[0][0] -= 5
        snakeLocation[0][2] = currentDirection

    elif currentDirection == 2: # down
        for i in reversed(range(1, len(snakeLocation))):
            snakeLocation[i][0] = int(snakeLocation[i-1][0])
            snakeLocation[i][1] = int(snakeLocation[i-1][1])
            snakeLocation[i][2] = int(snakeLocation[i-1][2])
        snakeLocation[0][1] += 5
        snakeLocation[0][2] = currentDirection

    elif currentDirection == 3: # right
        for i in reversed(range(1, len(snakeLocation))):
            snakeLocation[i][0] = int(snakeLocation[i-1][0])
            snakeLocation[i][1] = int(snakeLocation[i-1][1])
            snakeLocation[i][2] = int(snakeLocation[i-1][2])
        snakeLocation[0][0] += 5
        snakeLocation[0][2] = currentDirection

    else: # up
        for i in reversed(range(1, len(snakeLocation))):
            snakeLocation[i][0] = int(snakeLocation[i-1][0])
            snakeLocation[i][1] = int(snakeLocation[i-1][1])
            snakeLocation[i][2] = int(snakeLocation[i-1][2])
        snakeLocation[0][1] -= 5
        snakeLocation[0][2] = currentDirection

    # Update the display
    screen.fill(BLACK)
    # drawing grid on screen
    draw_grid()

    # drawing apple then snake
    drawApple()
    drawSnake()

    bombCount += 1
    if bombCount == 60:
        newBomb()
        bombCount = 0
    else:
        drawBomb()
    
    # drawing text
    screen.blit(text, textRect)

    # checking collision
    checkCollision()

    # Draw game elements
    pygame.display.update()

# ---------------------- Game Over ----------------------
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Game Over :(")

font = pygame.font.Font(None, 100)
text = font.render("Game Over", True, GREY)
textRect = text.get_rect()
textRect = (10, 20)

font2 = pygame.font.Font(None, 40)
text2 = font2.render("ESC to exit", True, GREY)
textRect2 = text2.get_rect()
textRect2 = (120,120)

# drawing text
screen.blit(text, textRect)
screen.blit(text2, textRect2)

# Draw game elements
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

# Quit the game
pygame.quit()