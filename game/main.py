import pygame, random
pygame.init()
surface = pygame.display.set_mode((1600,900))
pygame.display.set_caption('the most annoying game ever created')

path = 'assets/'
#如果你以某种方式翻译这个，我们中间的你好太酷了需要这个在鱿鱼游戏中
up_arrow = pygame.image.load(path + '/up.png')
arrow_rect = up_arrow.get_rect(center = (800,450))
down_arrow = pygame.image.load(path + 'down.png')
among_us = pygame.image.load(path + 'among_us_wide.jpg')
among_us_rect = among_us.get_rect(center = (800, 884))

def show_score():
    score_test = pygame.font.Font('freesansbold.ttf', 32).render('Score: '+str(score),True, ('black'))
    surface.blit(score_test, (10,10))

def starting_ending_text():
    starting_test = pygame.font.Font('freesansbold.ttf', 32).render('Press Space to start, and do NOT touch the wide among us. Make sure to stay on the platform',True, ('black'))
    starting_test_rect= starting_test.get_rect(center = (800, 450))
    surface.blit(starting_test, starting_test_rect)

score = 1
start = True

class Guy(pygame.sprite.Sprite):
    def __init__(self, group):
        self.y_vel = -1
        self.x_vel = 1
   
        super().__init__(group)
        self.image = pygame.image.load(path + 'happy.png')
        self.rect = self.image.get_rect(center = (800,450))
        self.among_us_sfx = pygame.mixer.Sound(path + 'among_us.ogg')
        self.lose = False
    def physics(self):

        global score

        self.y_vel += self.y_vel/24

        if self.rect.left <= -64:
            self.rect.right = 1663
        elif self.rect.right >= 1664:
            self.rect.left = -63

        self.rect.right += self.x_vel

        if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x_vel += -1
        elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x_vel += 1
        else: self.x_vel /= 1.1

        if self.y_vel >= 1: #bottom
            surface.blit(down_arrow,arrow_rect)
            self.rect.bottom += self.y_vel
            if self.rect.bottom > 900:
                self.rect.bottom = 900
                self.y_vel = -1

            if self.rect.bottom > platform.rect.top and self.rect.right > platform.rect.left and self.rect.left < platform.rect.right:
                self.rect.bottom = 838
                self.y_vel = -1
        else: # top
            self.rect.bottom += self.y_vel
            surface.blit(up_arrow,arrow_rect)
            if self.rect.top <= 0:
                score += 1
                self.rect.top = 1
                self.y_vel = 1

        if guy.rect.bottom > among_us_rect.top:
            global start
            self.among_us_sfx.play()
            self.lose = True
            start = False
            self.rect.center = 800,450
            self.y_vel = -1
            score = 0
            platform.x_vel = -1
    def update(self):
        self.physics()

guy_group = pygame.sprite.Group()
guy = Guy(guy_group)

class Platform(pygame.sprite.Sprite):
    def __init__(self, group):
        self.x_vel = -1
        super().__init__ (group)
        self.image = pygame.image.load(path + 'platform.png')
        self.rect = self.image.get_rect(center = (random.randint(0,1600), 852))

    def physics(self):
        if self.rect.left <= -128:
            self.rect.right = 1727
        elif self.rect.right >= 1728:
            self.rect.left = -127

        self.x_vel += random.randint(-2,2)
        self.rect.left += self.x_vel
        if self.x_vel > 20:
            self.x_vel = 10
        elif self.x_vel < -20:
            self.x_vel = -10 

        
    def update(self):
        self.physics()

platform_group = pygame.sprite.Group()
platform = Platform(platform_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        start = False
        guy.lose = False    

    surface.fill('white')

    if guy.lose == False and start == False:
        surface.blit(among_us,among_us_rect)

        platform.update()
        platform_group.draw(surface)
    
        guy.update()
        guy_group.draw(surface)

        show_score()
    else:
        starting_ending_text()
    print(platform.x_vel)
    pygame.display.update()
    pygame.time.Clock().tick(120)