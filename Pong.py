import pygame

pygame.mixer.pre_init(44100, -16, 1, 512) #used to fix sound delay
pygame.init()
pongball = pygame.image.load('pongball.png')
pygame.display.set_icon(pongball)
pygame.display.set_caption('Pong!')
screen_height = 425
screen_width = 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pongsound = pygame.mixer.Sound("pongsound.wav")
failsound = pygame.mixer.Sound("pongfail.wav")
gameover = False

class Paddle():
    def __init__(self, x, y, holding_ball):
        self.x = x
        self.y = round(y)
        self.width = 5
        self.height = 50
        self.velocity = 5
        self.holding_ball = holding_ball
        self.score = 0

class Ball():
    def __init__(self, x, y, side):
        self.x = x
        self.y = round(y)
        self.velocity = 5
        if side == 'Left':
            self.horizontal = 'Right'
            self.vertical = 'Down'
        elif side == 'Right':
            self.horizontal = 'Left'
            self.vertical = 'Up'

left_paddle = Paddle(2, (screen_height/2)-25, True)
right_paddle = Paddle(493, (screen_height/2)-25, False)
ball = Ball(15, (screen_height/2), 'Left')

def redraw():
    screen.fill((0,0,0))
    x_axis = 50
    for x in range(1,6):
        if x <= left_paddle.score:
            pygame.draw.circle(screen, (255,255,255), (x_axis, 410), 6, 0)
        else:
            pygame.draw.circle(screen, (255,255,255), (x_axis, 410), 6, 1)
        x_axis+=10
    x_axis = 400
    for x in range(1,6):
        if x <= right_paddle.score:
            pygame.draw.circle(screen, (255,255,255), (x_axis, 410), 6, 0)
        else:
            pygame.draw.circle(screen, (255,255,255), (x_axis, 410), 6, 1)
        x_axis += 10 
    pygame.draw.rect(screen, (235,235,235), (left_paddle.x, left_paddle.y, left_paddle.width, left_paddle.height))
    pygame.draw.rect(screen, (235,235,235), (right_paddle.x, right_paddle.y, right_paddle.width, right_paddle.height))
    pygame.draw.circle(screen, (255,255,255), (ball.x, ball.y), 8)
    pygame.display.update()

def draw_gameover_screen():
    screen.fill((0,0,0))
    winner = 'Player 1 Wins!' if left_paddle.score > right_paddle.score else 'Player 2 Wins!' 
    font1 = pygame.font.Font(pygame.font.get_default_font(), 24)
    text1 = font1.render(winner, True, (255,255,255))
    screen.blit(text1, (screen_width/2-text1.get_width()/2, screen_height/2-text1.get_height()))
    font2 = pygame.font.Font(pygame.font.get_default_font(), 16)
    text2 = font2.render("(Press Enter to Play Again)", True, (255,255,255))
    screen.blit(text2, (screen_width/2-text2.get_width()/2, (screen_height/2-text1.get_height())+30))
    pygame.display.update()

def reset():
    left_paddle.score = 0
    left_paddle.holding_ball = True
    left_paddle.y = (screen_height/2)-25
    right_paddle.score = 0
    right_paddle.holding_ball = False
    right_paddle.y = (screen_height/2)-25
    ball.x = 15
    ball.y = round((screen_height/2))
    ball.horizontal = 'Right'

game_running = True
while game_running:
    #frames per second
    clock.tick(30)
    #keystrokes
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            game_running = False
    if game_running == False:
        break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if left_paddle.holding_ball == True:
            left_paddle.holding_ball = False
        elif right_paddle.holding_ball == True:
            right_paddle.holding_ball = False
    if keys[pygame.K_UP]:
        if right_paddle.y > 0:
            right_paddle.y -= right_paddle.velocity
            if right_paddle.holding_ball == True:
                ball.y -= right_paddle.velocity
    if keys[pygame.K_DOWN]:
        if right_paddle.y < (screen_height-right_paddle.height):
            right_paddle.y += right_paddle.velocity
            if right_paddle.holding_ball == True:
                ball.y += right_paddle.velocity
    if keys[pygame.K_a]:
        if left_paddle.y > 0:
            left_paddle.y -= left_paddle.velocity
            if left_paddle.holding_ball == True:
                ball.y -= left_paddle.velocity
    if keys[pygame.K_z]:
        if left_paddle.y < (screen_height-left_paddle.height):
            left_paddle.y += left_paddle.velocity
            if left_paddle.holding_ball == True:
                ball.y += left_paddle.velocity

    #sets initial vertical direction
    if left_paddle.holding_ball == True:
        if left_paddle.y < screen_height/2:
            ball.vertical = 'Up'
        else:
            ball.vertical = 'Down'
    elif right_paddle.holding_ball == True:
        if right_paddle.y < screen_height/2:
            ball.vertical = 'Up'
        else:
            ball.vertical = 'Down'
        
    #bounces ball off top/bottom boundaries
    if left_paddle.holding_ball == False and right_paddle.holding_ball == False:
        if ball.horizontal == 'Right':
            ball.x += ball.velocity
            if ball.y <= 0:
                ball.vertical = 'Down'
            elif ball.y >= screen_height:
                ball.vertical = 'Up'
            if ball.vertical == 'Down':
                ball.y += ball.velocity
            elif ball.vertical == 'Up':
                ball.y -= ball.velocity
        elif ball.horizontal == 'Left':
            ball.x -= ball.velocity
            if ball.y <= 0:
                ball.vertical = 'Down'
            elif ball.y >= screen_height:
                ball.vertical = 'Up'
            if ball.vertical == 'Down':
                ball.y += ball.velocity
            elif ball.vertical == 'Up':
                ball.y -= ball.velocity

    #detects collision w/ paddle or whether or not ball got through
    if ball.horizontal == 'Left' and left_paddle.holding_ball == False:
        if ball.x > 0 and ball.x <= (left_paddle.x+left_paddle.width):
            if ball.y >= left_paddle.y and ball.y <= (left_paddle.y+left_paddle.height):
                pygame.mixer.Sound.play(pongsound)
                ball.horizontal = 'Right'
        elif ball.x < 0:
            pygame.mixer.Sound.play(failsound)
            right_paddle.score += 1
            ball.x = 15
            ball.y = left_paddle.y+round(left_paddle.height/2)
            left_paddle.holding_ball = True
            ball.horizontal = 'Right'
    elif ball.horizontal == 'Right' and right_paddle.holding_ball == False:
        if ball.x < screen_width and ball.x >= (right_paddle.x-right_paddle.width):
            if ball.y >= right_paddle.y and ball.y <= (right_paddle.y+right_paddle.height):
                pygame.mixer.Sound.play(pongsound)
                ball.horizontal = 'Left'
        elif ball.x > screen_width:
            pygame.mixer.Sound.play(failsound)
            left_paddle.score += 1
            ball.x = 485
            ball.y = right_paddle.y+round(right_paddle.height/2)
            right_paddle.holding_ball = True
            ball.horizontal = 'Left'

    #checks if gameover
    if left_paddle.score == 5:
        gameover = True
    elif right_paddle.score == 5:
        gameover = True

    #restarts game
    if keys[pygame.K_RETURN] and gameover == True:
        reset()
        gameover = False

    #redraws screen
    if gameover == True:
        draw_gameover_screen()
    else:
        redraw()
