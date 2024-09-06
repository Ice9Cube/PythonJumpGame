import pygame
import random
import os

pygame.init()

width = 400
height = 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jumpyly")

white = (255, 255, 255)
black = (0, 0, 0)
panel = (153, 217, 234)


# game variable
game_over = False
scrol_thresh = 200
scroll= 0
bg_scroll = 0
gravity = 1
max_platform = 10
fade_counder = 0
score = 0

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# define font
font_small = pygame.font.SysFont('Lusida Sans', 30)
font_big = pygame.font.SysFont('Lusida Sans', 35)

image_screen = pygame.image.load('Jumpy/cloud.png')
player_jampy = pygame.image.load('Jumpy/player.png')
platform_jampy = pygame.image.load('Jumpy/rock.png')

# function for outpuyying text into the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing into panel
def draw_panel():
    pygame.draw.rect(screen, panel, (0, 0, width, 20))
    pygame.draw.line(screen, black, (0, 20), (width, 20), 2)
    draw_text('Score: ' +str(score), font_small, black, 0, 0)


# function for drawing the backround
def draw_bg(bg_scroll):
    screen.blit(image_screen, (0, 0 + bg_scroll))
    screen.blit(image_screen, (0, -600 + bg_scroll))


#set frame rate
clock = pygame.time.Clock()
FPS = 55

# Player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_jampy, (45, 50))
        self.width = 30
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def move(self):
        #reset variable
        scroll = 0
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        #gravity
        self.vel_y += gravity# --> player falls down
        dy += self.vel_y

        #check collision with platform
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                         self.rect.bottom = platform.rect.top
                         dy = 0
                         self.vel_y = -20

        # check if the player  bousend the top of the screen
        if self.rect.top <= scrol_thresh:
            if self.vel_y < 0:
                scroll = -dy 

        # setting plater doesn't go off the edge of screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left 
        if self.rect.right + dx > width:
            dx = width - self.rect.right
        
        # uptade possition
        self.rect.x += dx
        self.rect.y += dy + scroll 

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 8, self.rect.y - 5))
        pygame.draw.rect(screen, white, self.rect, 2)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_jampy, (width, 30))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, scroll):
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > width:
            self.direction *= -1
            self.move_counter = 0
        # update platform's vertical position
        self.rect.y += scroll

        #check if platform has gone off the screen
        if self.rect.top > height:
            self.kill()


# player instance
jump = Player(width // 2, height - 150)

# create sprite groups
platform_group = pygame.sprite.Group()

#create temporary platforms
platform = Platform(width // 2 - 50, height - 50, 100, False)
platform_group.add(platform)

run = True
while run:
    #spead player
    clock.tick(FPS)
    if game_over == False:
        
        draw_bg(bg_scroll)

        scroll = jump.move()

        # generate platforms
        if len(platform_group) < max_platform:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, width - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random. randint(1, 2)
            if p_type == 1 and score > 500:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)


        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0

        # update platform
        platform_group.update(scroll)

        # update score
        if scroll > 0:
            score += scroll

        # draw line at previous high score
        pygame.draw.line(screen, black, (0, score - high_score + scrol_thresh), (width, score - high_score + scrol_thresh))
        draw_text('high score', font_small, black, width - 130, score - high_score + scrol_thresh)
        # draw sprites
        platform_group.draw(screen)
        jump.draw()

        # draw panel
        draw_panel()

        # check game over
        if jump.rect.top > height:
            game_over = True

    else:
        if fade_counder < width:
            fade_counder += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, black, (0, y * 100, fade_counder, 100))
                pygame.draw.rect(screen, black, (width - fade_counder, (y + 1) * 100, width, 100))
        else:
            draw_text('Game Over!', font_big, white, 140, 200)
            draw_text('Score: ' + str(score), font_big, white, 140, 250)
            draw_text('Press space to play again', font_big, white, 70, 300)
            # update high score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game_over = False
                score = 0
                scroll = 0
                fade_counder = 0
                # reposition jump
                jump.rect.center = (width // 2, height - 150)
                # resent platform
                platform_group.empty()
                #create starting platform
                platform = Platform(width // 2 - 50, height - 50, 100, False)
                platform_group.add(platform)


    #basic comand for scrren
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False

    pygame.display.update()

pygame.quit()
