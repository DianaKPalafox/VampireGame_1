import pygame
import os
import random

pygame.font.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VampireGame")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
SIZERL = 5
BULLET_VEL = 1
ENEMY_VEL = 5
MAX_BULLETS = 10



CROSSBOW_WIDTH, CROSSBOW_HEIGHT = 70, 60
BALL_WIDTH, BALL_HEIGHT = 50, 50
PLASMA_BALL_WIDTH, PLASMA_BALL_HEIGHT = 40,40

CROSSBOW_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join('Images', 'image2.png')),(CROSSBOW_WIDTH,CROSSBOW_HEIGHT)),90)
MAIN_MENU = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'main_menu.jpg')), (WIDTH, HEIGHT))

LEVEL_ONE_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'levelOne.jpg')), (WIDTH, HEIGHT))

RED_BALL_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'ball.png')),
                                        (BALL_WIDTH, BALL_HEIGHT))

PLASMA_BALL = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'plasma.png')),
                                        (PLASMA_BALL_WIDTH, PLASMA_BALL_HEIGHT))


class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = PLASMA_BALL
        self.mask = pygame.mask.from_surface(self.img)

    def draw (self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y += vel
    def off_screen(self,height):
        return not self.y <= height and self.y >= 0
    def collision(self,obj):
         return collide(self,obj)



class Status:
    COOLDOWN = 40
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ball_img = None
        self.cross_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw_cross(self, window):
        window.blit(self.cross_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -=1
                self.lasers.remove(laser)

    # ball One
    def draw_ball(self, window):
        window.blit(self.ball_img, (self.x, self.y))

    #of the bullet
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def bullet(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Status):
   def __init__(self, x, y, health=100):
       super().__init__(x, y, health)
       self.cross_img = CROSSBOW_IMAGE
       self.lasers_img = PLASMA_BALL
       self.mask = pygame.mask.from_surface(self.cross_img)
       self.max_health = health

   def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)


class Enemy(Status):
    def __init__(self,x,y,health = 100):
        super().__init__(x,y,health)
        self.ball_img = RED_BALL_IMAGE
        self.mask = pygame.mask.from_surface(self.ball_img)
        self.health = 1

    def move(self,vel):
        self.y += vel




def crossbow_movement(keys_pressed,player):
    if keys_pressed[pygame.K_a] and player.x - SIZERL > 0:  # LEFT
        player.x -= SIZERL
    if keys_pressed[pygame.K_d] and player.x + SIZERL < 840:  # RIGHT
        player.x += SIZERL




def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None



def main():
    player = Player(500, 400)

    enemies=[]
    wave_length = 5

    enemy_vel = 1
    laser_vel = 1
    level = 0
    lives = 1
    font = pygame.font.SysFont("Verdana", 45)
    lost_font = pygame.font.SysFont("Verdana", 50)

    clock = pygame.time.Clock()
    run = True
    FPS = 60
    lost = False
    count = 0

    def draw_window():

        WINDOW.blit(LEVEL_ONE_IMAGE, (0, 0))

        lives_label = font.render(f"Live: {lives}", True, (255, 255, 255))
        level_label = font.render(f"Level:{level}", True, (255, 255, 255))

        WINDOW.blit(lives_label, (5, 5))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 5, 5))



        for enemy in enemies:
            enemy.draw_ball(WINDOW)
        player.draw_cross(WINDOW)

        if lost:
            lost_lost = lost_font.render("You Lost?",1,(255,0,0))
            WINDOW.blit(lost_lost,(WIDTH/2 -lost_lost.get_width()/2,350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        draw_window()

        if lives <= 0 or player.health<= 0:
            lost = True
            count += 1
        if lost:
            if count > FPS * 2:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50,WIDTH-100),random.randrange(-1500,-100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys_pressed = pygame.key.get_pressed()


        if keys_pressed[pygame.K_SPACE]:
            player.bullet()

        crossbow_movement(keys_pressed, player)

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_laser(laser_vel,player)

            if collide(enemy, player):
                lives -= 1
                enemies.remove(enemy)
            elif enemy.y > HEIGHT:
                lives -= 1
                enemies.remove(enemy)



            player.move_laser(-laser_vel, enemies)



def main_menu():
    title_font = pygame.font.SysFont("Verdana",60)
    run = True
    while run:
        WINDOW.blit(MAIN_MENU,(0,0))
        title_label = title_font.render("Press the Up key to start?",1 ,(255,255,255))
        WINDOW.blit(title_label,(WIDTH/2 - title_label.get_width()/2,350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                main()
    pygame.quit()

main_menu()