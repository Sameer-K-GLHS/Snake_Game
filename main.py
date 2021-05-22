import pygame, random
# Initializing pygame
pygame.init()

# Defining variables
width = 600
height = 600
green = (50, 225, 50)
blue = (50, 50, 225)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
fps = 7
snake_width = 30
snake_height = 30
vel = 30
highscore = 0
heading = "down"
foodX = random.randint(0, 19)*snake_width
foodY = random.randint(0, 19)*snake_width
win = pygame.display.set_mode((width, height))
eatSound = pygame.mixer.Sound('eat.mp3')
pygame.display.set_caption("Snake")
appleImg = pygame.image.load("apple.png")
apple = pygame.transform.smoothscale(appleImg.convert_alpha(), (32, 32))
titleImg = pygame.image.load("title.png")
title = pygame.transform.smoothscale(titleImg.convert_alpha(), (550, 185))
win.fill(green)

# Entire snake
class Snake():
    def __init__(self, x, y):
        self.tail = []
        snakebody = body(x, y)
        self.tail.append(snakebody)

# Individual body parts of snake
class body():
    def __init__(self, x, y):
        self.x = x
        self.y = y

snake = Snake(0, 0)

# Drawing to screen
def draw():
    global snakebody, color, fps
    if start == True: # Checking if start of game
        startscreen()
    else: # drawing main game screen, snake, and food
        win.fill(green)
        font = pygame.font.SysFont("lucidasans", 30)
        score = font.render('Score: ' + str(len(snake.tail) - 1), True, black)
        score2 = font.render('Score: ' + str(len(snake.tail) - 1), True, white)
        win.blit(score, (248, 2))
        win.blit(score2, (250, 1))
        if len(snake.tail) - 1 >= 30: # Increases speed based on score
            fps = 16
        elif len(snake.tail) - 1 >= 20:
            fps = 13
        elif len(snake.tail) - 1 >= 10:
            fps = 10
        else:
            pass
        direction()
        drawSnake()
        bordercollision()
        snakecollision()
        if end == False:
            drawFood()
        temp = snake.tail[0]
        for snakebody in range(0, len(snake.tail)): # Changes position of each body part to the one in front
            temp2 = body(0,0)
            temp2.x = snake.tail[snakebody].x
            temp2.y = snake.tail[snakebody].y
            snake.tail[snakebody].x = temp.x
            snake.tail[snakebody].y = temp.y
            temp = temp2
    pygame.display.update()

# Draws each body part of snake
def drawSnake():
    for snakebody in snake.tail:
        pygame.draw.rect(win, blue, pygame.Rect(snakebody.x, snakebody.y, snake_width, snake_height))

# Makes sure food does not spawn on top of snake
def checkfood():
    global snakebody, foodX, foodY
    for i in range(0, len(snake.tail)):
        snakebody = snake.tail[i]
        while snakebody.x == foodX and snakebody.y == foodY:
            foodX = random.randint(0, 19)*snake_width
            foodY = random.randint(0, 19)*snake_width

# Draws food inside window, end checks for collision with head of snake
def drawFood():
    global foodX, foodY, color
    if snake.tail[0].x == foodX and snake.tail[0].y == foodY:
        snake.tail.append(body(snake.tail[len(snake.tail)-1].x, snake.tail[len(snake.tail)-1].y))
        foodX = random.randint(0, 19)*snake_width
        foodY = random.randint(0, 19)*snake_width
        checkfood()
        eatSound.play()
    pygame.draw.rect(win, green, pygame.Rect(foodX, foodY, snake_width, snake_height))
    win.blit(apple, (foodX, foodY))

# Moves snake continuously based on direction
def direction():
    if heading == "up":
        snake.tail[0].y -= vel
    if heading == "down":
        snake.tail[0].y += vel
    if heading == "left":
        snake.tail[0].x -= vel
    if heading == "right":
        snake.tail[0].x += vel

# Displays the start screen
def startscreen():
    global start
    font2 = pygame.font.SysFont("lucidasans", 55)
    img2 = font2.render("Press 'Space' to start", True, black)
    img3 = font2.render("Press 'Space' to start", True, white)
    win.fill(green)
    win.blit(title, (25, 100))
    win.blit(img2, (23, 362))
    win.blit(img3, (25, 360))
    
# Displays game over screen, and checks for highscore
def endscreen():
    global end, highscore
    end = True
    if len(snake.tail) - 1 > highscore:
        highscore = len(snake.tail) - 1
    font = pygame.font.SysFont("lucidasans", 96)
    font2 = pygame.font.SysFont("lucidasans", 72)
    font3 = pygame.font.SysFont("lucidasans", 55)
    img = font.render("Game Over", True, black)
    img1 = font.render("Game Over", True, white)
    img2 = font2.render("Score: " + str(len(snake.tail) - 1), True, black)
    img2_2 = font2.render("Score: " + str(len(snake.tail) - 1), True, white)
    img3 = font2.render("Highscore: " + str(highscore), True, black)
    img3_2 = font2.render("Highscore: " + str(highscore), True, white)
    img4 = font3.render("Press 'Space' to retry", True, black)
    img4_2 = font3.render("Press 'Space' to retry", True, white)
    win.fill(red)
    win.blit(img, (38, 52))
    win.blit(img1, (40, 50))
    win.blit(img2, (18, 227))
    win.blit(img2_2, (20, 225))
    win.blit(img3, (18, 327))
    win.blit(img3_2, (20, 325))
    win.blit(img4, (18, 452))
    win.blit(img4_2, (20, 450))

# Restarts the game, reseting score, speed, and length of snake
def restart():
    global end, snake, heading, fps
    end = False
    for i in snake.tail:
        snake.tail.remove(i)
    snake = Snake(0, 0)
    heading = "down"
    fps = 7

# Checks if snake head collides with the border of the screen
def bordercollision():
    if snake.tail[0].x > 570 or snake.tail[0].x < 0 or snake.tail[0].y > 570 or snake.tail[0].y < 0:
        endscreen()

# Checks if snake head collides with a body part of the snake
def snakecollision():
    global snakebody
    for i in range(1, len(snake.tail)):
        snakebody = snake.tail[i]
        if snake.tail[0].x == snakebody.x and snake.tail[0].y == snakebody.y:
            endscreen()

# Game loop           
def main():
    global heading, end, start, snake
    clock = pygame.time.Clock()
    running = True
    end = False
    start = True
    while running:
        pygame.time.delay(50)
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN: # Movement, makes sure snake does not go in opposite direction
                if start == False:
                    if event.key == pygame.K_w:
                        if heading != "down":
                            heading = "up"
                    if event.key == pygame.K_s:
                        if heading != "up":
                            heading = "down"
                    if event.key == pygame.K_a:
                        if heading != "right":
                            heading = "left"
                    if event.key == pygame.K_d:
                        if heading != "left":
                            heading = "right"
                    if end == True:
                        if event.key == pygame.K_SPACE:
                            restart()
                if event.key == pygame.K_SPACE:
                    start = False
        if end == False:
            draw()
           
    pygame.quit()


if __name__ == "__main__":
    
    main()