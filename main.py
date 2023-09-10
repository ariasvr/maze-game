from pygame import *
from pygame.sprite import Group
init()
clock = time.Clock()


window = display.set_mode((700, 500))
display.set_caption('The maze game')
bg = transform.scale(image.load('E:\Algorithmics\PTPY1\maze game\\background.jpg'), (700, 500))

VWalls = []
HWalls = []

class GameSprite(sprite.Sprite):
    def __init__(self, picture, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, width, height, x, y, x_speed, y_speed):
        super().__init__(picture, width, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def collideWall1(self):
        platforms_touched = sprite.spritecollide(self, walls, False)

        #Horizontal collision handling
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
                self.y_speed = 0
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
                self.y_speed = 0
        
        #Verticle collision handling
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                self.x_speed = 0
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
                self.x_speed = 0

    def collideWall2(self):
        platforms_touched = sprite.spritecollide(self, walls, False)

        #Horizontal collision handling
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.x -= 5
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.x += 5
        
        #Verticle collision handling
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.y -= 5
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.y += 5

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.x < 0:
            self.rect.x += 5
        if self.rect.y < 0:
            self.rect.y += 5
        if self.rect.x > 650:
            self.rect.x -= 5
        if self.rect.y > 450:
            self.rect.y -= 5

    def fire(self):
        bullet = Bullet('E:\Algorithmics\PTPY1\maze game\leaf.png', self.rect.right, self.rect.centery, 20, 15, 4)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
        self.width = width
        self.height = height
    
    def update(self):
        if self.rect.x <= 300:
            self.direction = "right"
            self.image = transform.scale(image.load('E:\Algorithmics\PTPY1\maze game\\monsterR.png'), (self.width, self.height))
        if self.rect.x >= 680 - 100:
            self.direction = "left"
            self.image = transform.scale(image.load('E:\Algorithmics\PTPY1\maze game\\monsterL.png'), (self.width, self.height))
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(sprite.Sprite):
    def __init__(self, picture, x, y, width, heigth, speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, heigth))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def update(self):
        self.rect.x += self.speed
        
        #disappears after touching the walls
        platforms_touched = sprite.spritecollide(self, walls, False)
        for p in platforms_touched:
            self.kill()
        
        # disappears after reaching the edge of the screen           
        if self.rect.x > 700 + 10:
            self.kill()             

def createMaze(): 
    global walls

    #Create all vertical walls
    VWall1 = GameSprite('E:\Algorithmics\PTPY1\maze game\\vwall.png', 50, 180, 220, 300)
    walls.add(VWall1)
    VWall2 = GameSprite('E:\Algorithmics\PTPY1\maze game\\vwall.png', 50, 180, 220, 150)
    walls.add(VWall2)
    VWall3 = GameSprite('E:\Algorithmics\PTPY1\maze game\\vwall.png', 50, 190, 400, 25)
    walls.add(VWall3)
    VWall4 = GameSprite('E:\Algorithmics\PTPY1\maze game\\vwall.png', 50, 160, 430, 320)
    walls.add(VWall4)
    VWall5 = GameSprite('E:\Algorithmics\PTPY1\maze game\\vwall.png', 50, 320, 630, 90)
    walls.add(VWall5)
    VWall6 = GameSprite('E:\Algorithmics\PTPY1\maze game\\vwall.png', 50, 180, 20, 8)
    walls.add(VWall6)

    #Create all horizontal walls
    HWall1 = GameSprite('E:\Algorithmics\PTPY1\maze game\\hwall.png', 180, 50, 90, 280)
    walls.add(HWall1)
    HWall2 = GameSprite('E:\Algorithmics\PTPY1\maze game\\hwall.png', 320, 50, 280, 10)
    walls.add(HWall2)
    HWall3 = GameSprite('E:\Algorithmics\PTPY1\maze game\\hwall.png', 200, 50, 360, 300)
    walls.add(HWall3)
    HWall4 = GameSprite('E:\Algorithmics\PTPY1\maze game\\hwall.png', 120, 50, 550, 150)
    walls.add(HWall4)
    HWall5 = GameSprite('E:\Algorithmics\PTPY1\maze game\\hwall.png', 180, 50, 20, 10)
    walls.add(HWall5)

def finalResult(win):
    if win == True:
        window.blit(bg, (0, 0))
        tfont = font.Font(None, 100)
        text = tfont.render('YOU WIN!', True, (255, 193, 7))
        window.blit(text, (180, 200))
    else:
        window.blit(bg, (0, 0))
        tfont = font.Font(None, 100)
        text = tfont.render('YOU LOSE!', True, (255, 193, 7))
        window.blit(text, (160, 200))

character = Player('E:\Algorithmics\PTPY1\maze game\\avatar.png', 50, 50, 30, 430, 0, 0)
walls = sprite.Group()
bullets = sprite.Group()
createMaze()
monster = Enemy('E:\Algorithmics\PTPY1\maze game\\monsterR.png', 50, 50, 270, 250, 4)
monsters = sprite.Group()
monsters.add(monster)
goal = GameSprite('E:\Algorithmics\PTPY1\maze game\\star.png', 50, 50, 500, 400)

run = True
win = False
while run:
    #Catch keypressed
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_UP:
                character.y_speed = -4
            if e.key == K_DOWN:
                character.y_speed = 4
            if e.key == K_LEFT:
                character.x_speed = -4
            if e.key == K_RIGHT:
                character.x_speed = 4
            if e.key == K_SPACE:
                character.fire()                
        if e.type == KEYUP:
            if e.key == K_UP or e.key == K_DOWN:
                character.y_speed = 0
            if e.key == K_LEFT or e.key == K_RIGHT:
                character.x_speed = 0
    
    #Character collides with a monster    
    for m in monsters.sprites():
        if character.rect.colliderect(m.rect):
            print('here')
            win = False
            run = False
            break

    #Shoot a monster
    for b in bullets.sprites():
        for m in monsters.sprites():
            if b.rect.colliderect(m):
                m.kill()
                monsters.remove(m)
        
    #Reach the goal
    if  character.rect.colliderect(goal.rect):
        win = True
        break

    #Draw graphics
    window.blit(bg, (0, 0))
    walls.draw(window)
    character.reset()
    goal.reset()
    bullets.draw(window)
    monsters.draw(window)

    bullets.update()
    character.update()
    monsters.update()

    #Check if character collides with the walls
    #character.collideWall1()
    character.collideWall2()

    clock.tick(40)
    display.update()

run = True
while run:
    #Catch keypressed
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    finalResult(win)
    clock.tick(40)
    display.update()
